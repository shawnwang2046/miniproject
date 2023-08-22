from pydantic import BaseModel

class Topic(BaseModel):
    topic_id: int
    meaningful_topic_name: str

class Text(BaseModel):
    text_id: int
    text: str
    topic_id: int