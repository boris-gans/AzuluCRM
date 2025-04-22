import uvicorn
import os
from dotenv import load_dotenv
from app.main import app  # Import the app object from app.main

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = os.getenv("PORT")
    if port is not None and port.isdigit():
        port = int(port)
    else:
        port = 8000

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    ) 