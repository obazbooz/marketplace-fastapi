# router/search_filter.py
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import DbAdvertisement, AdvStatus
from schemas import AdvertisementDisplay

router = APIRouter(prefix="/search", tags=["search_filter"])

# Recency window (created_at)
class Recency(str, Enum):
    day = "day"
    week = "week"
    month = "month"

# Stars (minimum seller rating)
class Stars(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

def _recency_start(window: Recency) -> datetime:
    now = datetime.utcnow()
    if window == Recency.day:
        return now - timedelta(days=1)
    if window == Recency.week:
        return now - timedelta(days=7)
    return now - timedelta(days=30)  # month

@router.get(
    "/ads",
    response_model=List[AdvertisementDisplay],
    summary="Search & filter advertisements by category, status, recency, and stars",
    status_code=status.HTTP_200_OK,
)
def search_ads(
    category: Optional[str] = Query(
        default=None,
        description="Filter by exact category (case-insensitive)."
    ),
    status_: Optional[AdvStatus] = Query(
        default=None,
        alias="status",
        description="Filter by ad status."
    ),
    recency: Optional[Recency] = Query(
        default=None,
        description="Filter by created time window."
    ),
    stars: Optional[Stars] = Query(
        default=None,
        description="Minimum seller rating (stars)."
    ),
    skip: int = Query(0, ge=0, description="Pagination start index."),
    limit: int = Query(10, ge=1, le=100, description="Page size (max 100)."),
    db: Session = Depends(get_db),
):
    """
    Filters by optional `category`, `status`, `recency` (created_at window), and
    `stars` (minimum seller_rating_avg). Results are ordered by `created_at` DESC.
    Only ads with at least one rating are included when `stars` is used.
    """
    q = db.query(DbAdvertisement)

    if category:
        q = q.filter(func.lower(DbAdvertisement.category) == func.lower(category))

    if status_ is not None:
        q = q.filter(DbAdvertisement.status == status_)

    if recency is not None:
        q = q.filter(DbAdvertisement.created_at >= _recency_start(recency))

    if stars is not None:
        q = q.filter(
            DbAdvertisement.seller_rating_count.isnot(None),
            DbAdvertisement.seller_rating_count > 0,
            DbAdvertisement.seller_rating_avg.isnot(None),
            DbAdvertisement.seller_rating_avg >= int(stars),
        )

    q = q.order_by(DbAdvertisement.created_at.desc())
    return q.offset(skip).limit(limit).all()
