import uvicorn
import os
from dotenv import load_dotenv
from app.main import app  # Import the app object from app.main

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    ) 