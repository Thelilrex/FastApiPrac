from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from Data import scheduler
from Data.database import engine, SessionLocal, get_db
from Data.scheduler import ContactFormDB
from Data.schemas import ContactForm
from Settings.config import settings  # Import settings
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
scheduler.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

print(f"Database URL: {settings.database_url}")
print(f"Secret Key: {settings.secret_key}")
print(f"Algorithm: {settings.algorithm}")
print(f"Access Token Expire Minutes: {settings.access_token_expire_minutes}")

@app.post(f"/contact/")
def create_a_contact(contact: ContactForm, db: db_dependency):
    db_contact = ContactFormDB(email=contact.email, name=contact.name, subject=contact.subject, message=contact.message)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)