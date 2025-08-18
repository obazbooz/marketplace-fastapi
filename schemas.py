from typing import List
from pydantic import BaseModel, EmailStr, validator
import re

class UserBase(BaseModel):
    username: str
    email: EmailStr 
    password: str

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', v):
            raise ValueError('Username must be 3-30 characters and only contain letters, numbers, - or _')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserDisplay(BaseModel):
    username: str
    email: str
    # items: List[Article] = []
    # convert from datebase type in models into our user display automaticly
    class Config():
        orm_mode = True

#Datatype
class AdvertisementBase(BaseModel):
    title: str
    description: str
    category: str
    id: int
    is_reserved: bool
    is_sold: bool
    owner_id: int


class AdvertisementDisplay(BaseModel):
    title: str
    description: str
    category: str
    id: int
    is_reserved: bool
    is_sold: bool
    owner_id: int