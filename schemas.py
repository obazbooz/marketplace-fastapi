from pydantic import  EmailStr ,TypeAdapter,ConfigDict , field_validator, BaseModel, model_validator # or field_validator, ValidationInfo
from fastapi import HTTPException, status ,Form
from decimal import Decimal
from typing import Optional
from db.models import AdvStatus,RatingScore,AdvCategory
from datetime import datetime , date
import re

#Pydantic schema

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
                detail='Invalid email, expected format like: example@gmail.com')

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


class AdvertisementBase(BaseModel):
    title: str
    description: str
    category: AdvCategory
    price: Optional[Decimal]
    location: Optional[str]
    @classmethod
    def as_form(
        cls,
        title: str = Form(..., description="Advertisement title"),
        description: str = Form(..., description="Detailed description"),
        category: AdvCategory = Form(..., description="Category (e.g., Cars, Electronics)"),
        price: Optional[Decimal] = Form(..., description="Price"),
        location: Optional[str] = Form(..., description="City/area"),
    ):
        return cls(
            title=title,
            description=description,
            category=category,
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


class MessageBase(BaseModel):
    receiver_id : int
    advertisement_id : int
    content : str

    @classmethod
    def as_form(
            cls,
            receiver_id: int = Form(...),
            advertisement_id: int = Form(...),
            content: str = Form(...),
                ):
        return cls(
            receiver_id=receiver_id,
            advertisement_id=advertisement_id,
            content=content
        )


class TransactionBase(BaseModel):
    advertisement_id: int
    buyer_id: int
    @classmethod
    def as_form(
            cls,
            advertisement_id:int = Form(...),
            buyer_id: int = Form(...),
    ):
        return cls(advertisement_id=advertisement_id,buyer_id=buyer_id)


class RatingBase(BaseModel):
    transaction_id : int
    score: RatingScore
    @classmethod
    def as_form(
            cls,
            transaction_id: int = Form(...),
            score: RatingScore = Form(..., description='1 - 5 stars')
    ):
        return cls(
            transaction_id=transaction_id,
            score=score
        )


class SearchFilterBase(BaseModel):
    title: str
    category: AdvCategory
    start_date: Optional[date] = None
    end_date:Optional[date] = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='end_date must be on or after start_date')
        return self

    @classmethod
    def as_form(
            cls,
            title: str = Form(..., description="Search words contained in the title (case-insensitive)"),
            category: AdvCategory = Form(..., description="Category (Exact category"),
            start_date: Optional[date] = Form(..., description="YYYY-MM-DD"),
            end_date: Optional[date] = Form(..., description="YYYY-MM-DD"),

    ):
        return cls(
            title=title,
            category=category,
            start_date=start_date,
            end_date=end_date,
        )


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    # items: List[Article] = []
    # convert from datebase type in models into our user display automaticly
    model_config = ConfigDict(from_attributes=True)


class AdvertisementDisplay(BaseModel):
    id: int
    owner_id: int
    title: str
    description: str
    category: AdvCategory
    status:AdvStatus
    price: Optional[Decimal] = None
    location: Optional[str] = None
    created_at: date
    image_path: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class MessageDisplay(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    advertisement_id: int
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TransactionDisplay(BaseModel):
    id : int
    advertisement_id : int
    buyer_id : int
    seller_id : int
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)


class RatingDisplay(BaseModel):
    id: int
    transaction_id: int
    rater_id: int
    ratee_id: int
    score: RatingScore
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


