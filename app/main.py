from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from . import models, database, cloudinary_setup
from .routers import events, content, mailing_list
from .dependencies import verify_admin


# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Create FastAPI app
app = FastAPI(
    title="Azulu CRM API",
    description="API for managing events and content for Azulu Events",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router)
app.include_router(content.router)
app.include_router(mailing_list.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Azulu CRM API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

@app.get("/cloudinary/signature")
async def get_cloudinary_signature(_: bool = Depends(verify_admin)):
    """Get signature for direct uploads to Cloudinary"""
    return cloudinary_setup.generate_upload_signature()

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...), _: bool = Depends(verify_admin)):
    """
    Upload an image directly through the backend
    
    This endpoint handles the full image upload process to Cloudinary,
    bypassing the need for frontend signature handling.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check if the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Upload image to Cloudinary
    result = cloudinary_setup.upload_image(file)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"Upload failed: {result.get('error', 'Unknown error')}")
    
    return result 