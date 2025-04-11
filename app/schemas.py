from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class EventBase(BaseModel):
    name: str = Field(..., description="Name of the event")
    venue_name: str = Field(..., description="Name of the venue")
    address: str = Field(..., description="Address of the venue")
    start_date: datetime = Field(..., description="Start date of the event")
    start_time: str = Field(..., description="Time in format 'HH:MM'")
    end_time: str = Field(..., description="Time in format 'HH:MM'")
    time_zone: str = Field(..., description="IANA time zone name (e.g., 'America/New_York')")
    ticket_status: str = Field(..., description="Available, Sold Out, or Sold At The Door")
    ticket_link: Optional[str] = Field(None, description="Link to the ticket page")
    lineup: Optional[List[str]] = Field(..., description="List of artists performing")
    genres: Optional[List[str]] = Field(..., description="List of genres")
    description: str = Field(..., description="Description of the event")
    poster_url: Optional[str] = Field(None, description="URL of the event poster")
    price: Optional[float] = Field(None, description="Price of the event")
    currency: Optional[str] = Field(..., description="Currency of the event")

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
    id: int = Field(..., description="Unique identifier for the event")

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




class DjSocialsBase(BaseModel):
    instagram: Optional[str] = Field(None, description="Instagram handle")
    tiktok: Optional[str] = Field(None, description="TikTok handle")
    spotify: Optional[str] = Field(None, description="Spotify profile link")
    soundcloud: Optional[str] = Field(None, description="SoundCloud profile link")
    youtube: Optional[str] = Field(None, description="YouTube channel")
    apple_music: Optional[str] = Field(None, description="Apple Music profile link")

class DjSocialsCreate(DjSocialsBase):
    pass

class DjSocialsUpdate(DjSocialsBase):
    pass

class DjSocials(DjSocialsBase):
    id: int
    class Config:
        orm_mode = True

class DjBase(BaseModel):
    alias: str = Field(..., description="Public alias or stage name of the DJ")
    profile_url: str = Field(..., description="URL to the DJ's profile or bio page")

class DjCreate(DjBase):
    socials: Optional[DjSocialsCreate] = Field(None, description="Social media links")

class DjUpdate(BaseModel):
    alias: Optional[str] = Field(None, description="Public alias or stage name of the DJ")
    profile_url: Optional[str] = Field(None, description="URL to the DJ's profile or bio page")
    social_id: Optional[int] = Field(None, description="Reference to associated socials")
    socials: Optional[DjSocialsUpdate] = Field(None, description="Updated social media links")

class Dj(DjBase):
    id: int = Field(..., description="Unique identifier for the DJ")
    social_id: Optional[int] = Field(None, description="Reference to associated socials")
    socials: Optional[DjSocials] = Field(None, description="Nested social media profile")

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