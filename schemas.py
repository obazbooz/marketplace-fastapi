from pydantic import BaseModel , EmailStr ,field_validator,TypeAdapter,condecimal
from fastapi import Form,HTTPException, status
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from fastapi import Form
from db.models import AdvStatus
import re

_email_adapter = TypeAdapter(EmailStr)  # reuse across validations

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', v):
            raise HTTPException (
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username must be 3-30 characters and only contain letters, numbers, - or _')
        return v

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v):
        # Accept only strings; coerce/validate to EmailStr, with custom message on failure
        try:
            return _email_adapter.validate_python(v)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid email. Expected format like: example@gmail.com')

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must be at least 8 characters long')
            raise ValueError()
        if not re.search(r'[A-Z]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must contain at least one special character')
        return v

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
    # status: AdvStatus = AdvStatus.AVAILABLE
    price: Optional[Decimal]
    location: Optional[str]
    @classmethod
    def as_form(
        cls,
        title: str = Form(..., description="Advertisement title"),
        description: str = Form(..., description="Detailed description"),
        category: str = Form(..., description="Category (e.g., Cars, Electronics)"),
        # status: AdvStatus = Form(AdvStatus.AVAILABLE, description="Status (available, reserved, sold)"),
        price: Optional[Decimal] = Form(..., description="Price"),
        location: Optional[str] = Form(..., description="City/area"),

    ):
        return cls(
            title=title,
            description=description,
            category=category,
            # status=status,
            # is_reserved=is_reserved,
            # is_sold=is_sold,
            # is_available = is_available,
            price=price,
            location=location,
        )

class AdvertisementStatusBase(BaseModel):
    status: AdvStatus = AdvStatus.AVAILABLE
    @classmethod
    def as_form(
        cls,
        status: AdvStatus = Form(AdvStatus.AVAILABLE, description="Status (available, reserved, sold)")
    ):
        return cls(
            status=status,
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
    status:AdvStatus
    owner_id: int
    price: Optional[Decimal] = None
    location: Optional[str] = None
    class Config:
        from_attributes = True
