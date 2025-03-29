from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.types import TypeDecorator
import json
from .database import Base

class JSONList(TypeDecorator):
    """Custom type for storing lists as JSON strings"""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    venue_name = Column(String)
    address = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    ticket_status = Column(String)  # "Available", "Sold Out", "Sold At The Door"
    ticket_link = Column(String, nullable=True)
    lineup = Column(JSONList, default=[])
    genres = Column(JSONList, default=[])
    description = Column(Text)
    poster_url = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String, default="USD")

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    string_collection = Column(JSONList, default=[])
    big_string = Column(Text, nullable=True) 