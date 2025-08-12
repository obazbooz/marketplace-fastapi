from typing import List
from pydantic import BaseModel


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
