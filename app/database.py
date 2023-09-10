import sqlite3
from contextlib import contextmanager

DATABASE_URL = "topics.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL, timeout=10)  # wait up to 10 seconds for the lock
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        # 创建topic_table表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS topic_table (
            topic_id INTEGER PRIMARY KEY,
            meaningful_topic_name TEXT
        );
        ''')

        # 创建text_table表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_table (
            text_id INTEGER PRIMARY KEY,
            url TEXT,
            text TEXT,
            topic_id INTEGER,
            FOREIGN KEY (topic_id) REFERENCES topic_table (topic_id)
        );
        ''')

        conn.commit()