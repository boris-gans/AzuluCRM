import cloudinary
import cloudinary.uploader
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

def upload_image(file, folder="event_posters"):
    """
    Upload an image directly to Cloudinary from the backend
    
    Args:
        file: UploadFile from FastAPI
        folder: Cloudinary folder where the image should be stored
        
    Returns:
        dict: Contains the image URL and other upload information
    """
    try:
        # Read the file content
        file_content = file.file.read()
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            resource_type="image"
        )
        
        # Return the upload result (contains secure_url, public_id, etc.)
        return {
            "success": True,
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "format": result["format"],
            "width": result["width"],
            "height": result["height"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        # Reset file cursor to beginning
        file.file.seek(0) 