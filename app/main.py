from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from . import models, database, cloudinary_setup
from .routers import events, content
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