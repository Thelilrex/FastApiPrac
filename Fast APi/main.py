from datetime import timedelta
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from Data import scheduler
from Data.database import engine, get_db
from Data.scheduler import ContactFormDB, Todo, UserDB
from Data.schemas import ContactForm, NewsLetterSubscription
from Data.users_Schema import UserCreate, TodoGet, TodoCreate, Token
from Security.security import get_password_hash, authenticate_user, user_dependency, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
scheduler.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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


@app.post("/register", response_model=Token)
def register(user: UserCreate, db: db_dependency):
    db_user = db.query(scheduler.UserDB).filter(scheduler.UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(username=user.username, hashed_password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta= access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserCreate)
def read_users_me(current_user: user_dependency):
    return current_user


@app.post("/todos/", response_model=TodoCreate)
def create_todo(todo: TodoCreate, db: db_dependency, current_user: user_dependency):
    db_todo = Todo(**todo.model_dump(), owner_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: db_dependency, current_user: user_dependency):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}


@app.get("/todos/", response_model=List[TodoGet])
def read_todos(db: db_dependency, current_user: user_dependency, skip: int = 0, limit: int = 10):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).offset(skip).limit(limit).all()
    return todos
