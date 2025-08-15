from typing import List
from pydantic import BaseModel
from fastapi import Form


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    @classmethod
    def as_form(
        cls,
        username: str = Form(..., description="Username"),
        email: str = Form(..., description="Email address"),
        password: str = Form(..., description="Password"),
    ):
        # Note: Swagger won't mask this field like a password box unless you use OAuth2PasswordRequestForm.
        return cls(username=username, email=email, password=password)



# Datatype
class AdvertisementBase(BaseModel):
    title: str
    description: str
    category: str
    is_reserved: bool
    is_sold: bool
    @classmethod
    def as_form(
        cls,
        title: str = Form(..., description="Advertisement title"),
        description: str = Form(..., description="Detailed description"),
        category: str = Form(..., description="Category (e.g., Cars, Electronics)"),
        is_reserved: bool = Form(False, description="Mark as reserved"),
        is_sold: bool = Form(False, description="Mark as sold"),
    ):
        return cls(
            title=title,
            description=description,
            category=category,
            is_reserved=is_reserved,
            is_sold=is_sold,
        )

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    # items: List[Article] = []
    # convert from datebase type in models into our user display automaticly
    class Config():
        orm_mode = True

class AdvertisementDisplay(BaseModel):
    id: int
    title: str
    description: str
    category: str
    is_reserved: bool
    is_sold: bool
    owner_id: int
