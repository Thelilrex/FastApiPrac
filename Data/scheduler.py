# Databases
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base


class NewsLetterSubscriptionDB(Base):
    __tablename__ = "newsletter"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    language = Column(String)
    name = Column(String)
    consent = Column(Boolean)
    status = Column(String)
    received = Column(DateTime, default=datetime.datetime.utcnow)


class ContactFormDB(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(String)
    received = Column(DateTime, default=datetime.datetime.utcnow)
