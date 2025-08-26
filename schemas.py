# schemas.py
from __future__ import annotations

from datetime import datetime
from typing import Optional
import re

from fastapi import Form, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator, TypeAdapter, condecimal

from db.models import AdvStatus  # Enum: available | reserved | sold


# Reusable EmailStr adapter for custom validation messages
_email_adapter = TypeAdapter(EmailStr)

# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]{3,30}$", v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be 3–30 chars and only letters, numbers, - or _.",
            )
        return v

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v):
        # Coerce/validate to EmailStr with a friendly error message
        try:
            return _email_adapter.validate_python(v)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email. Expected format like: example@gmail.com",
            )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long.",
            )
        if not re.search(r"[A-Z]", v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter.",
            )
        if not re.search(r"[a-z]", v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one lowercase letter.",
            )
        if not re.search(r"[0-9]", v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one digit.",
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one special character.",
            )
        return v

    @classmethod
    def as_form(
        cls,
        username: str = Form(..., description="Username"),
        email: EmailStr = Form(..., description="Email address"),
        password: str = Form(..., description="Password"),
    ) -> "UserBase":
        return cls(username=username, email=email, password=password)


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        # Pydantic v2 replacement for orm_mode = True
        from_attributes = True


# ---------------------------------------------------------------------------
# Advertisements
# ---------------------------------------------------------------------------

PriceType = condecimal(max_digits=12, decimal_places=2)

class AdvertisementBase(BaseModel):
    title: str
    description: str
    category: str
    status: AdvStatus = AdvStatus.AVAILABLE
    price: Optional[PriceType] = None
    location: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(..., description="Advertisement title"),
        description: str = Form(..., description="Detailed description"),
        category: str = Form(..., description="Category (e.g., Cars, Electronics)"),
        status: AdvStatus = Form(
            AdvStatus.AVAILABLE, description="Status (available, reserved, sold)"
        ),
        price: Optional[PriceType] = Form(None, description="Price"),
        location: Optional[str] = Form(None, description="City/area"),
    ) -> "AdvertisementBase":
        return cls(
            title=title,
            description=description,
            category=category,
            status=status,
            price=price,
            location=location,
        )


class AdvertisementDisplay(BaseModel):
    # Core fields
    id: int
    title: str
    description: str
    category: str
    status: AdvStatus
    owner_id: int
    price: Optional[PriceType] = None
    location: Optional[str] = None

    # Server-managed fields (read-only in API)
    created_at: datetime
    updated_at: datetime
    reserved_at: Optional[datetime] = None
    sold_at: Optional[datetime] = None
    seller_rating_avg: Optional[float] = None
    seller_rating_count: Optional[int] = None

    class Config:
        # Pydantic v2 mapping from ORM objects
        from_attributes = True
