from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, database, dependencies

router = APIRouter(
    prefix="/content",
    tags=["content"]
)

@router.post("/", response_model=schemas.Content)
async def create_content(
    content: schemas.ContentCreate,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    # Check if content with this key already exists
    db_content = db.query(models.Content).filter(models.Content.key == content.key).first()
    if db_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content with key '{content.key}' already exists"
        )
    
    db_content = models.Content(
        key=content.key,
        string_collection=content.string_collection,
        big_string=content.big_string
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    print(f"Db_content: {db_content}")
    return db_content

@router.get("/", response_model=List[schemas.Content])
async def read_all_content(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return db.query(models.Content).offset(skip).limit(limit).all()

@router.get("/{key}", response_model=schemas.Content)
async def read_content_by_key(key: str, db: Session = Depends(database.get_db)):
    db_content = db.query(models.Content).filter(models.Content.key == key).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail=f"Content with key '{key}' not found")
    return db_content

@router.put("/{key}", response_model=schemas.Content)
async def update_content(
    key: str,
    content: schemas.ContentUpdate,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    db_content = db.query(models.Content).filter(models.Content.key == key).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail=f"Content with key '{key}' not found")
    
    # Update content attributes
    content_data = content.dict(exclude_unset=True)
    for key, value in content_data.items():
        setattr(db_content, key, value)
    
    db.commit()
    db.refresh(db_content)
    return db_content

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    key: str,
    db: Session = Depends(database.get_db),
    _: bool = Depends(dependencies.verify_admin)
):
    db_content = db.query(models.Content).filter(models.Content.key == key).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail=f"Content with key '{key}' not found")
    
    db.delete(db_content)
    db.commit()
    return None 