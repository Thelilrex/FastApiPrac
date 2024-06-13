from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool


class Config:
    orm_mode = True


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoInDB(TodoCreate):
    owner_id: int


class TodoGet(BaseModel):
    id: int
    title: str
    description: str