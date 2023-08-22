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
import sqlite3
from crud import get_topic,insert_into_topic_table,get_all_data
from database import init_db

app = FastAPI()
topic_model = BERTopic.load("my_model")
    
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
    paragraphs = merge_sentences(text)
    cleaned_paragraphs = [remove_stopwords(paragraph) for paragraph in paragraphs]
    topic_data = topic_model.transform(cleaned_paragraphs)
    top_topic_id = get_top_topic(topic_data)
    return get_topic(top_topic_id)

@app.get("/topics")
def read_topic(url: URL, db=Depends(get_db)):
    topic_name = extract_topic(db, url)
    if topic_name is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"topic_name": topic_name}