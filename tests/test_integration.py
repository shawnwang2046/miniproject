from main import extract_topic,init_app
from crud import insert_into_topic_table, get_topic
import pandas as pd

def setup_module(module):
    init_app()

def test_extract_topic_integration():
    url = 'https://www.sec.gov/Archives/edgar/data/87347/000156459019000928/slb-10k_20181231.htm'
    result = extract_topic(url)
    
    # Replace the following line with your actual verification logic
    assert result is not None  # Or whatever condition you expect

def test_insert_and_get_topic():
    # Create a sample dataframe
#    data = {
#        'Topic': [1, 2],
#        'meaningful_topic_name': ['TopicA', 'TopicB']
#    }
#    df = pd.DataFrame(data)
    
    # Insert data
 #   insert_into_topic_table(df)
    
    # Retrieve a topic and verify
    topic = get_topic(1)
    assert topic is not None
    assert topic["topic_id"] == 1
    assert topic["meaningful_topic_name"] == 'Assessing and Reporting Impairment of Goodwill: A Comprehensive Analysis of Qualitative and Quantitative Approaches'
