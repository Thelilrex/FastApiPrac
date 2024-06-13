# Schemas
from pydantic import BaseModel


class NewsLetterSubscription(BaseModel):
    email: str
    language: str
    name: str
    privacyConsentCheck: bool
    status: str


class ContactForm(BaseModel):
    email: str
    name: str
    subject: str
    message: str