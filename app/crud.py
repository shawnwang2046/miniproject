from database import get_db
import pandas as pd

def get_topic(topic_id):
    print(type(topic_id))
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM topic_table WHERE topic_id=?", (topic_id,))
        row = cur.fetchone()
    print(row)
    return {"topic_id": row[0], "meaningful_topic_name": row[1]}

def insert_into_topic_table(df):
    with get_db() as conn:
        cursor = conn.cursor()

        # 将dataframe中的数据插入到topic_table表中
        for index, row in df.iterrows():
            cursor.execute('''
            INSERT INTO topic_table (topic_id, meaningful_topic_name)
            VALUES (?, ?);
            ''', (row['Topic'], row['meaningful_topic_name']))

        # 提交更改
        conn.commit()

def get_all_data():
    with get_db() as conn:
        # Use a pandas DataFrame to store and display the data
        df = pd.read_sql_query("SELECT * from topic_table", conn)
        
        # Close the connection
        conn.close()
        return df