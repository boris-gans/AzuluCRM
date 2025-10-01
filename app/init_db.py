from app.database import Base, engine
import app.models  # import so models are registered

Base.metadata.create_all(bind=engine)
print("Database initialized.")