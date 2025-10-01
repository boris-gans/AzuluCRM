import sqlalchemy
from sqlalchemy import create_engine, exc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import time
import logging
from typing import Generator
from contextlib import contextmanager
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
# MySQL connection details
MYSQL_HOST = os.getenv("MYSQL_HOST", "")
MYSQL_PORT = os.getenv("MYSQL_PORT", "")
MYSQL_USER = os.getenv("MYSQL_USER", "")  # Default user, change as needed
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")  # Set your password through env variable
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "")
# DATABASE_URL = os.getenv("DATABASE_URL")

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Construct MySQL connection URL
# DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////var/data/azulu.db")
DATABASE_URL = "sqlite:////var/data/azulu.db"

# If using Render with persistent disk, construct the path
RENDER_DISK_PATH = os.getenv("RENDER_DISK_PATH")
# if RENDER_DISK_PATH:
#     DATABASE_URL = f"sqlite:///{RENDER_DISK_PATH}/azulu.db"

# Create SQLAlchemy engine with connection pool
# engine = create_engine(
#     DATABASE_URL,
#     poolclass=sqlalchemy.pool.NullPool,
#     connect_args={"connect_timeout": 10}
# )

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Context manager for handling db sessions with retry logic
@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Get a database session with retry logic for common database errors.
    """
    session = SessionLocal()
    retry_count = 0
    
    while retry_count < MAX_RETRIES:
        try:
            yield session
            break
        except exc.OperationalError as e:
            retry_count += 1
            if retry_count < MAX_RETRIES:
                logger.warning(f"Database connection error: {str(e)}. Retrying {retry_count}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY * retry_count)  # Exponential backoff
                continue
            else:
                logger.error(f"Failed to connect to database after {MAX_RETRIES} attempts: {str(e)}")
                raise
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()

# FastAPI dependency for getting db session
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session to route handlers.
    """
    with get_db_session() as session:
        yield session

# Verify database connection on startup
def verify_database_connection() -> bool:
    """
    Verify database connection is working.
    Returns True if connection successful, raises exception otherwise.
    """
    try:
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
        return True
    except exc.OperationalError as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise 