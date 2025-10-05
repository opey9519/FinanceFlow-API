from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    email: str
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
