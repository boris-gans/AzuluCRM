from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship
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
    name = Column(String(255), index=True)
    venue_name = Column(String(255))
    address = Column(String(255))
    start_date = Column(DateTime)  # Stores date portion only in UTC
    start_time = Column(String(5))  # Format: "HH:MM" in local time
    end_time = Column(String(5))  # Format: "HH:MM" in local time
    time_zone = Column(String(255))  # IANA time zone name
    ticket_status = Column(String(255))  # "Available", "Sold Out", "Sold At The Door"
    ticket_link = Column(String(255), nullable=True)
    lineup = Column(JSONList, default=[])
    genres = Column(JSONList, default=[])
    description = Column(Text)
    poster_url = Column(String(255), nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True)
    string_collection = Column(JSONList, default=[])
    big_string = Column(Text, nullable=True)

class MailingListEntry(Base):
    __tablename__ = "mailing_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)  # Ensure emails are unique
    created_at = Column(DateTime, default=datetime.utcnow)
    subscribed = Column(Boolean, default=True)  # To allow users to unsubscribe 



class DjSocials(Base):
    __tablename__ = "dj_socials"

    id = Column(Integer, primary_key=True, index=True)
    instagram = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    spotify = Column(String, nullable=True)
    soundcloud = Column(String, nullable=True)
    youtube = Column(String, nullable=True)
    apple_music = Column(String, nullable=True)

class Dj(Base):
    __tablename__ = "djs"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, nullable=False)
    profile_url = Column(String, nullable=False)
    social_id = Column(Integer, ForeignKey("dj_socials.id"))
    
    socials = relationship("DjSocials")
