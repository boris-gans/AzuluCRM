from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from .. import models, schemas, database, dependencies

router = APIRouter(
    prefix="/mailing-list",
    tags=["mailing-list"]
)

@router.post("/subscribe", response_model=schemas.MailingListEntry)
async def subscribe_to_mailing_list(
    entry: schemas.MailingListEntryCreate,
    db: Session = Depends(database.get_db)
):
    """Public endpoint for users to subscribe to the mailing list"""
    try:
        # Check if email already exists but unsubscribed
        existing_entry = db.query(models.MailingListEntry).filter(
            models.MailingListEntry.email == entry.email
        ).first()
        
        if existing_entry:
            if existing_entry.subscribed:
                # Already subscribed
                return existing_entry
            else:
                # Re-subscribe
                existing_entry.subscribed = True
                existing_entry.name = entry.name  # Update name if changed
                db.commit()
                db.refresh(existing_entry)
                return existing_entry
        
        # Create new entry
        db_entry = models.MailingListEntry(
            name=entry.name,
            email=entry.email
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    except IntegrityError:
        # Handle potential race condition
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already subscribed"
        )

@router.get("/unsubscribe/{email}", status_code=status.HTTP_200_OK)
async def unsubscribe_from_mailing_list(
    email: str,
    db: Session = Depends(database.get_db)
):
    """Public endpoint for users to unsubscribe from the mailing list"""
    db_entry = db.query(models.MailingListEntry).filter(
        models.MailingListEntry.email == email
    ).first()
    
    if not db_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found in mailing list"
        )
    
    db_entry.subscribed = False
    db.commit()
    return {"message": "Successfully unsubscribed"}

# Admin endpoints below - all require authentication

@router.get("/", response_model=List[schemas.MailingListEntry])
async def get_all_mailing_list_entries(
    skip: int = 0,
    limit: int = 100,
    subscribed_only: bool = True,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    """Admin endpoint to get all mailing list entries"""
    query = db.query(models.MailingListEntry)
    
    if subscribed_only:
        query = query.filter(models.MailingListEntry.subscribed == True)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{entry_id}", response_model=schemas.MailingListEntry)
async def get_mailing_list_entry(
    entry_id: int,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    """Admin endpoint to get a specific mailing list entry"""
    db_entry = db.query(models.MailingListEntry).filter(
        models.MailingListEntry.id == entry_id
    ).first()
    
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mailing list entry with ID {entry_id} not found"
        )
    
    return db_entry

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mailing_list_entry(
    entry_id: int,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    """Admin endpoint to delete a mailing list entry"""
    db_entry = db.query(models.MailingListEntry).filter(
        models.MailingListEntry.id == entry_id
    ).first()
    
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mailing list entry with ID {entry_id} not found"
        )
    
    db.delete(db_entry)
    db.commit()
    return None 