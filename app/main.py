from typing import List, Tuple, Dict
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import nltk
from bertopic import BERTopic
import requests
from crud import get_topic,insert_into_topic_table, insert_text_and_topic, get_texts_by_topic_id
from database import init_db
import uvicorn
from fastapi.openapi.models import OpenAPI

   
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
        #print(response.text)
        
        return " ".join([p.text for p in soup.find_all("p")])
    except Exception as e:
        raise Exception(str(e))
    

def get_top_topic(topic_data: List) -> int:
    topic_ids = topic_data[0]
    weights = topic_data[1]
    print(topic_ids)
    print(weights)
    topic_weight_sum = {topic_id: 0 for topic_id in topic_ids}
    for topic_id, weight in zip(topic_ids, weights):
        topic_weight_sum[topic_id] += weight

    # Sort the topic_ids based on the accumulated weights in descending order
    sorted_topic_ids = sorted(topic_weight_sum.keys(), key=lambda x: topic_weight_sum[x], reverse=True)

    top_topic_id = int(sorted_topic_ids[0])
    return top_topic_id
    
def extract_topic(url: str) -> str:
    text = extract_text_from_url(url)
    paragraphs = merge_sentences(text)
    cleaned_paragraphs = [remove_stopwords(paragraph) for paragraph in paragraphs]
    topic_data = topic_model.transform(cleaned_paragraphs)
    top_topic_id = get_top_topic(topic_data)
    print(f"top_topic_id {top_topic_id}".format())
    topic_name = get_topic(top_topic_id)
    print(f"topic {topic_name}")
    return top_topic_id, topic_name, text


def init_app():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    print('init db')
    init_db()
    global topic_model
    topic_model = BERTopic.load("model")
    print('topic loaded')
    df = pd.read_csv('topics.csv')
    insert_into_topic_table(df)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_app()


@app.get("/article_from_topic_id",
         summary="Retrieve articles based on topic ID",
         description="Given a topic ID, this endpoint retrieves associated articles from the database.")
def get_article_from_topic_id(topic_id: str):
    texts = get_texts_by_topic_id(topic_id)
    if not texts:
        raise HTTPException(status_code=404, detail=f"No articles found for topic_id: {topic_id}")
    return {"texts": texts}


@app.get("/topic_from_url",
         summary="Extract topic from a given URL",
         description="Given a URL, this endpoint extracts the topic, saves the associated text, and returns the topic name.")
def get_topic_from_url(url: str):
    top_topic_id, topic_name, text = extract_topic(url)
    if topic_name is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    insert_text_and_topic(text, top_topic_id, url)
    return {"topic_name": topic_name}


@app.get("/openapi.json")
def get_openapi_schema():
    openapi_schema = OpenAPI(**app.openapi())
    return openapi_schema.dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)