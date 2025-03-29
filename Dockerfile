FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a directory for the database if it doesn't exist
RUN mkdir -p /data

# Set environment variable for database
ENV DATABASE_URL=sqlite:////data/azulu.db

# Set environment variables for Cloudinary
ENV CLOUDINARY_CLOUD_NAME=dsjkhhpbl
ENV CLOUDINARY_API_KEY=519823698438478
ENV CLOUDINARY_API_SECRET=p4Vmj0mNDgU-64MHs1gB9hRzSJY

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 