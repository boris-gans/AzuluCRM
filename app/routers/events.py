from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Date
from typing import List, Optional
from datetime import datetime, date
import pytz

from .. import models, schemas, database, dependencies

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.post("/", response_model=schemas.Event)
async def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    # Only store the date portion in UTC
    db_event = models.Event(
        name=event.name,
        venue_name=event.venue_name,
        address=event.address,
        start_date=event.start_date,
        start_time=event.start_time,
        end_time=event.end_time,
        time_zone=event.time_zone,
        ticket_status=event.ticket_status,
        ticket_link=event.ticket_link,
        lineup=event.lineup,
        genres=event.genres,
        description=event.description,
        poster_url=event.poster_url,
        price=event.price,
        currency=event.currency
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[schemas.Event])
async def read_events(
    skip: int = 0, 
    limit: int = 100,
    upcoming: bool = False,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Event)

    if upcoming:
        # Compare only the date portion for upcoming events
        today_utc = datetime.now(pytz.UTC).date()
        query = query.filter(models.Event.start_date >= today_utc)
    else:
        today_utc = datetime.now(pytz.UTC).date()
        query = query.filter(models.Event.start_date < today_utc)
    
    return query.order_by(models.Event.start_date).offset(skip).limit(limit).all()

@router.get("/{event_id}", response_model=schemas.Event)
async def read_event(event_id: int, db: Session = Depends(database.get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.put("/{event_id}", response_model=schemas.Event)
async def update_event(
    event_id: int,
    event: schemas.EventUpdate,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update event attributes
    event_data = event.dict(exclude_unset=True)
    for key, value in event_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return None 