# Schemas
from pydantic import BaseModel, EmailStr


class NewsLetterSubscription(BaseModel):
    email: EmailStr
    language: str
    name: str
    privacyConsentCheck: bool
    status: str


class ContactForm(BaseModel):
    email: EmailStr
    name: str
    subject: str
    message: str