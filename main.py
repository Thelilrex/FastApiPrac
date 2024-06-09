from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from Data import scheduler
from Data.database import engine, SessionLocal, get_db
from Data.scheduler import ContactFormDB
from Data.schemas import ContactForm

app = FastAPI()
scheduler.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.post(f"/contact/")
def create_a_contact(contact: ContactForm, db: db_dependency):
    db_contact = ContactFormDB(email=contact.email, name=contact.name, subject=contact.subject, message=contact.message)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)