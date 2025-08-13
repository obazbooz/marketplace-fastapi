from typing import List
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

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
