import cloudinary
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def generate_upload_signature():
    """
    Generate a signature for direct frontend uploads to Cloudinary
    This can be exposed via an API endpoint to allow secure direct uploads from the frontend
    """
    timestamp = int(time.time())
    
    # You might want to add more parameters like folder, allowed formats, etc.
    params = {
        "timestamp": timestamp
    }
    
    signature = cloudinary.utils.api_sign_request(
        params,
        cloudinary.config().api_secret
    )
    
    return {
        "signature": signature,
        "timestamp": timestamp,
        "cloudName": cloudinary.config().cloud_name,
        "apiKey": cloudinary.config().api_key
    } 