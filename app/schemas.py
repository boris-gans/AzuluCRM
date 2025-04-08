from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class EventBase(BaseModel):
    name: str
    venue_name: str
    address: str
    start_date: datetime
    start_time: str = Field(..., description="Time in format 'HH:MM'")
    end_time: str = Field(..., description="Time in format 'HH:MM'")
    time_zone: str = Field(..., description="IANA time zone name (e.g., 'America/New_York')")
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
    start_date: Optional[datetime] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    time_zone: Optional[str] = None
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

class MailingListEntryBase(BaseModel):
    name: str
    email: EmailStr

class MailingListEntryCreate(MailingListEntryBase):
    pass

class MailingListEntryUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    subscribed: Optional[bool] = None

class MailingListEntry(MailingListEntryBase):
    id: int
    created_at: datetime
    subscribed: bool

    class Config:
        orm_mode = True 