from typing import List, Tuple, Dict
from fastapi import FastAPI, HTTPException
from sqlite_utils import Database
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np
import swifter
import cleantext
import csv
import nltk
from tqdm import tqdm
from gensim import corpora
from gensim.models import LdaModel
from bertopic import BERTopic
from bertopic.representation import OpenAI
import requests
from finbert_embedding.embedding import FinbertEmbedding
import openai


app = FastAPI()
db = Database("topics_db.sqlite")
loaded_model = BERTopic.load("my_model")
    


class Topic(BaseModel):
    id: int
    url: str
    body_text: str
    topic: str

def merge_sentences(paragraph: str, min_words: int = 500) -> List[str]:
    """Merge sentences in a paragraph so that each merged sentence contains at least min_words words."""
    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(paragraph)

    # Merge sentences together based on word count
    merged_sentences = []
    current_sentence = []
    current_word_count = 0
    for sentence in sentences:
        words = word_tokenize(sentence)
        current_word_count += len(words)
        current_sentence.append(sentence)
        if current_word_count >= min_words:
            merged_sentences.append(' '.join(current_sentence))
            current_sentence = []
            current_word_count = 0

    # If there are any remaining sentences that didn't reach the desired length, add them as well
    if current_sentence:
        merged_sentences.append(' '.join(current_sentence))

    return merged_sentences


def remove_stopwords(text: str) -> str:
    """Remove stopwords and non-alphabetic characters from the input text."""
    custom_stopwords = ['may', 'million', 'financial', 'business','could','operations','company','net','products','cash',
                     'december', 'value', 'year', 'tax', 'could', 'including', 'products','results','customers']
    stop_words = set(stopwords.words('english'))
    stop_words.update(custom_stopwords)  # Add custom stop words
    tokens = word_tokenize(text.lower()) # Convert to lowercase and tokenize
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words and word not in string.punctuation]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def extract_text_from_url(url: str) -> str:
    """Extract text from a webpage given its URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return " ".join([p.text for p in soup.find_all("span")])
    except Exception as e:
        raise Exception(str(e))


def extract_topic(url: str) -> List[str]:
    """Extract and clean the text from a URL, and then return paragraphs."""
    text = extract_text_from_url(url)
    paragraphs = merge_sentences(text)
    cleaned_paragraphs = [remove_stopwords(paragraph) for paragraph in paragraphs]

    topic_data = loaded_model.transform(cleaned_paragraphs)
    topic_ids, weights = topic_data

    for topic_id, weight in zip(topic_ids, weights):
        topic_weight_sum[topic_id] += weight

        # Sort the topic_ids based on the accumulated weights in descending order
    sorted_topic_ids = sorted(topic_weight_sum.keys(), key=lambda x: topic_weight_sum[x], reverse=True)

        # Get the top 5 topic_ids based on the accumulated weights
    top_5_topic_ids = sorted_topic_ids[:5]

    conn = sqlite3.connect('topics_db.sqlite')
    cursor = conn.cursor()

    # Create a parameterized query string
    query = "SELECT meaningful_topic_name FROM topics WHERE Topic IN ({})".format(','.join('?' * len(top_5_topic_ids)))

    # Execute the query
    cursor.execute(query, top_5_topic_ids)

    # Fetch the results
    results = cursor.fetchall()

    # Extract the topic names
    topic_names = [result[0] for result in results]

    # Close the connection
    conn.close()

    return topic_names



@app.post("/extract_topic")
async def extract_topic_from_url(url: str):
    """
    Extract topics from a given URL.

    Args:
        url (str): The URL to extract topics from.

    Returns:
        dict: A dictionary containing the URL and the extracted topics.

    Raises:
        HTTPException: If an error occurs while extracting topics.
    """
    try:
        # Extract text
        topics = extract_topic(url)

        return {
            "url": url,
            "topics": topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_topic_names/")
async def get_topic_names(topic_ids: List[int]):
    """
    Get meaningful topic names by topic IDs.

    Args:
        topic_ids (List[int]): A list of topic IDs.

    Returns:
        list: A list of meaningful topic names.
    """
    db = Database("topics_db.sqlite")
    query = db["topics"].find(id__in=topic_ids, select=["meaningful_topic_name"])
    result = [row["meaningful_topic_name"] for row in query]
    return result


@app.get("/get_articles_by_topic_id")
async def get_articles_by_topic_id(topic_id: int):
    """
    Get articles by topic ID.

    Args:
        topic_id (int): The topic ID to retrieve articles for.

    Returns:
        list: A list of articles related to the given topic ID.
    """
    db = Database("topics_db.sqlite")
    query = db["articles"].find(topic_ids__contains=str(topic_id))
    articles = [row for row in query]
    return articles

@app.on_event("startup")
async def startup_event():
    # Read the CSV file
    topics = pd.read_csv("topics.csv")


    # Create a new table called 'topics' and insert the DataFrame into it
    db["topics"].insert_all(topics.to_dict("records"), replace=True)