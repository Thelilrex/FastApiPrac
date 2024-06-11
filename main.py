from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Data import scheduler
from Data.database import engine, SessionLocal, get_db
from Data.scheduler import ContactFormDB, UserDB
from Data.schemas import ContactForm, NewsLetterSubscription
from Data.users_Schema import UserCreate
from Security import security
from Security.security import get_password_hash, authenticate_user
from Settings.config import settings  # Import settings
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
scheduler.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.post(f"/contact/")
def create_a_contact(contact: ContactForm, db: db_dependency):
    db_contact = ContactFormDB(email=contact.email, name=contact.name, subject=contact.subject, message=contact.message)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)


@app.get("/contact/search_contacts/mail/{email}")
def get_contact_by_mail(email: str, db: db_dependency):
    result = db.query(scheduler.ContactFormDB).filter(scheduler.ContactFormDB.email == email).all()
    if not result:
        raise HTTPException(status_code=404, detail="email not found")
    return result


@app.get("/contact/search_contacts/id/{contact_id}")
def get_contact_by_id(contact_id: int, db: db_dependency):
    result = db.query(scheduler.ContactFormDB).filter(scheduler.ContactFormDB.id == contact_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="contact not found")
    return result


@app.delete("/contact/delete_contact/{contact_id}")
def delete_user_by_id(contact_id: int, db: db_dependency):
    result = db.query(scheduler.ContactFormDB).filter(scheduler.ContactFormDB.id == contact_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="contact not found")
    db.delete(result)
    db.commit()
    return f"contact {contact_id} has been successfully deleted"


@app.post("/newsletter/subscribe")
def subscribe_newsletter(newsletter: NewsLetterSubscription, db: db_dependency):
    db_newsletter = scheduler.NewsLetterSubscriptionDB(email=newsletter.email, name=newsletter.name,
                                                       status=newsletter.status, language=newsletter.language,
                                                       consent=newsletter.privacyConsentCheck)
    db.add(db_newsletter)
    db.commit()
    db.refresh(db_newsletter)
    return "confirmation mail sent to the email"


@app.post("/users/signup/")
async def create_a_user(user: UserCreate, db: db_dependency):
    result = db.query(scheduler.UserDB).filter(scheduler.UserDB.email == user.email).first()
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    db_user = UserDB(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return "User has been added"


@app.get("/users/login/{username}, {password}")
async def user_login(username: str, password: str, db: db_dependency):
    if not (authenticate_user(db, username, password)):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return "User logged in"
