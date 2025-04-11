from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Date
from typing import List, Optional
from datetime import datetime, date
import pytz

from .. import models, schemas, database, dependencies

router = APIRouter(
    prefix="/djs",
    tags=["djs"]
)

@router.post("/", response_model=schemas.Dj)
async def create_dj(
    dj: schemas.DjCreate,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    # Create socials first if provided
    print(dj)
    socials = None
    if dj.socials:
        socials = models.DjSocials(**dj.socials.dict())
        db.add(socials)
        db.flush()  # Get the socials ID without committing
    print(f"Dj: {dj}")
    print(f"Socials: {socials}")

    # Create DJ with optional socials reference
    db_dj = models.Dj(
        alias=dj.alias,
        profile_url=dj.profile_url,
        social_id=socials.id if socials else None
    )
    db.add(db_dj)
    db.commit()
    db.refresh(db_dj)
    return db_dj

@router.get("/", response_model=List[schemas.Dj])
async def read_djs(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return db.query(models.Dj).offset(skip).limit(limit).all()

@router.get("/{dj_id}", response_model=schemas.Dj)
async def read_dj(dj_id: int, db: Session = Depends(database.get_db)):
    db_dj = db.query(models.Dj).filter(models.Dj.id == dj_id).first()
    if db_dj is None:
        raise HTTPException(status_code=404, detail="DJ not found")
    return db_dj

@router.put("/{dj_id}", response_model=schemas.Dj)
async def update_dj(
    dj_id: int,
    dj: schemas.DjUpdate,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    db_dj = db.query(models.Dj).filter(models.Dj.id == dj_id).first()
    if db_dj is None:
        raise HTTPException(status_code=404, detail="DJ not found")
    
    # Update DJ attributes
    dj_data = dj.dict(exclude_unset=True)
    for key, value in dj_data.items():
        if key == 'socials' and value is not None:
            # Handle socials update
            if db_dj.social_id:
                # Update existing socials
                db_socials = db.query(models.DjSocials).filter(models.DjSocials.id == db_dj.social_id).first()
                for social_key, social_value in value.items():
                    setattr(db_socials, social_key, social_value)
            else:
                # Create new socials
                socials = models.DjSocials(**value.dict())
                db.add(socials)
                db.flush()
                db_dj.social_id = socials.id
        else:
            setattr(db_dj, key, value)
    
    db.commit()
    db.refresh(db_dj)
    return db_dj

@router.delete("/{dj_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dj(
    dj_id: int,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    db_dj = db.query(models.Dj).filter(models.Dj.id == dj_id).first()
    if db_dj is None:
        raise HTTPException(status_code=404, detail="DJ not found")
    
    # Delete associated socials if they exist
    if db_dj.social_id:
        db_socials = db.query(models.DjSocials).filter(models.DjSocials.id == db_dj.social_id).first()
        if db_socials:
            db.delete(db_socials)
    
    db.delete(db_dj)
    db.commit()
    return None
