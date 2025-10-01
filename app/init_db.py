from .database import Base, engine
from app.models import Event, Content, MailingListEntry, Dj, DjSocials, JSONList# noqa: F401 ensures metadata is populated


Base.metadata.create_all(bind=engine)
print("Database initialized.")