# Azulu CRM

A FastAPI application for managing events and content for Azulu Events.

## Features

- Event management (create, read, update, delete)
- Content management for dynamic website content
- Simple admin authentication
- SQLite database for simple deployment
- Ready for deployment on Fly.io with persistent storage

## Requirements

- Python 3.9+
- FastAPI
- SQLAlchemy
- Cloudinary (for image hosting)

## Local Development

### Option 1: Using Docker Compose (Recommended)

1. Make sure you have Docker and Docker Compose installed
2. Clone the repository:
```bash
git clone https://github.com/yourusername/azuluCRM.git
cd azuluCRM
```

3. Start the application with Docker Compose:
```bash
docker-compose up
```

4. Access the API documentation at http://localhost:8000/docs

### Option 2: Direct Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/azuluCRM.git
cd azuluCRM
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set environment variables (you can create a .env file):
```
ADMIN_PASSWORD=your_secure_password
CLOUDINARY_CLOUD_NAME=dsjkhhpbl
CLOUDINARY_API_KEY=519823698438478
CLOUDINARY_API_SECRET=p4Vmj0mNDgU-64MHs1gB9hRzSJY
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Access the API documentation at http://localhost:8000/docs

## API Authentication

Protected endpoints require an `X-Admin-Password` header with the admin password.

## Database

The application uses SQLite as the database. The database file is automatically created in the application directory (or in the `/data` directory in Docker/Fly.io).

## Deployment on Fly.io

1. Install the Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to Fly:
```bash
fly auth login
```

3. Create a persistent volume for the database:
```bash
fly volumes create azulu_db --size 1
```

4. Deploy the application:
```bash
fly deploy
```

5. Set environment variables (if not already in fly.toml):
```bash
fly secrets set ADMIN_PASSWORD=your_secure_password
```

## Image Hosting with Cloudinary

The application uses Cloudinary for image hosting with the following credentials:
- Cloud Name: dsjkhhpbl
- API Key: 519823698438478
- API Secret: p4Vmj0mNDgU-64MHs1gB9hRzSJY

For uploading images through the frontend, you can use Cloudinary's upload widget or direct upload functionality. The backend will only store the URL of the image.

## Deploying to Render with Persistent Disk

This project can be deployed to Render with a persistent disk to preserve data across deployments.

### Setup

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service with these settings:
   - **Name**: azulucrm (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn run:app --host 0.0.0.0 --port $PORT`

4. Add the following environment variables:
   - `ADMIN_PASSWORD`: Your admin password
   - `CLOUDINARY_CLOUD_NAME`: Your Cloudinary cloud name
   - `CLOUDINARY_API_KEY`: Your Cloudinary API key
   - `CLOUDINARY_API_SECRET`: Your Cloudinary API secret
   - `RENDER_DISK_PATH`: `/var/data`

5. Add a persistent disk:
   - **Mount Path**: `/var/data`
   - **Size**: 1 GB (or adjust as needed)

### Using the render.yaml file

Alternatively, you can use the included `render.yaml` file for deployment using Render Blueprints:

1. Push the `render.yaml` file to your GitHub repository
2. Go to the Render Dashboard → Blueprints → New Blueprint Instance
3. Connect your GitHub repository
4. Configure the environment variables that are marked with `sync: false` in the Blueprint

### Data Migration

To migrate your existing SQLite database to Render:

1. Deploy the service first
2. Use the Render shell to access your service
3. Create the data directory: `mkdir -p /var/data`
4. Upload your existing database to the persistent disk using SFTP or the Render shell

## License

MIT 