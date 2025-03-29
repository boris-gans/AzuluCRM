from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EventBase(BaseModel):
    name: str
    venue_name: str
    address: str
    start_time: datetime
    end_time: datetime
    ticket_status: str = Field(..., description="Available, Sold Out, or Sold At The Door")
    ticket_link: Optional[str] = None
    lineup: List[str] = []
    genres: List[str] = []
    description: str
    poster_url: Optional[str] = None
    price: Optional[float] = None
    currency: str = "USD"

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    name: Optional[str] = None
    venue_name: Optional[str] = None
    address: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    ticket_status: Optional[str] = None
    ticket_link: Optional[str] = None
    lineup: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True

class ContentBase(BaseModel):
    key: str
    string_collection: List[str] = []
    big_string: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    string_collection: Optional[List[str]] = None
    big_string: Optional[str] = None

class Content(ContentBase):
    id: int

    class Config:
        orm_mode = True 