from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.types import TypeDecorator
import json
from .database import Base
from datetime import datetime

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
    start_date = Column(DateTime)  # Stores date portion only in UTC
    start_time = Column(String)  # Format: "HH:MM" in local time
    end_time = Column(String)  # Format: "HH:MM" in local time
    time_zone = Column(String)  # IANA time zone name
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

class MailingListEntry(Base):
    __tablename__ = "mailing_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)  # Ensure emails are unique
    created_at = Column(DateTime, default=datetime.utcnow)
    subscribed = Column(Boolean, default=True)  # To allow users to unsubscribe 