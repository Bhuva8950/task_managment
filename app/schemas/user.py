import email
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.user import User, UserRole
from typing import Optional


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:UserRole

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    name:str
    role:UserRole

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name:Optional[str] = None
    email:Optional[EmailStr] = None
    role:Optional[UserRole] = None
    password:Optional[str] = None


class LogingSchema(BaseModel):
    email : EmailStr
    password : str