from pydantic import BaseModel
from typing import Optional

class TopicRegistration(BaseModel):
    topic: str

class ProducerRegistration(BaseModel):
    topic: str
    producer_id: Optional[str] = None  # optional label for logging

class ConsumerRegistration(BaseModel):
    topic: str
    consumer_id: Optional[str] = None  # if None, broker generates one

class PublishRequest(BaseModel):
    topic: str
    value: str  # keep it simple (string payload)
    key: Optional[str] = None

class ConsumeRequest(BaseModel):
    consumer_id: str

class Message(BaseModel):
    topic: str
    offset: int
    value: str
    key: Optional[str] = None
