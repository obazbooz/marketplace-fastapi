# Added by Prof. Ali: lightweight debug endpoints (public)
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.database import get_db
from db.models import DbAdvertisement
from schemas import AdvertisementDisplay

# Public router. No auth dependency here.
# If you later want to protect these endpoints, add a dependency that enforces auth.
router = APIRouter(
    prefix="/debug",
    tags=["debug - ads"]
)

@router.get("/ads/summary", summary="Distinct categories and statuses with counts")
def ads_summary(db: Session = Depends(get_db)):
    cats = [
        r[0] for r in db.query(DbAdvertisement.category)
                       .distinct()
                       .order_by(DbAdvertisement.category)
                       .all()
    ]
    stats = [
        r[0] for r in db.query(DbAdvertisement.status)
                       .distinct()
                       .order_by(DbAdvertisement.status)
                       .all()
    ]

    by_status = [
        {"status": s, "count": c}
        for s, c in db.query(DbAdvertisement.status, func.count(DbAdvertisement.id))
                      .group_by(DbAdvertisement.status)
                      .order_by(DbAdvertisement.status)
                      .all()
    ]
    by_category = [
        {"category": cat, "count": c}
        for cat, c in db.query(DbAdvertisement.category, func.count(DbAdvertisement.id))
                        .group_by(DbAdvertisement.category)
                        .order_by(DbAdvertisement.category)
                        .all()
    ]

    return {
        "distinct_categories": cats,
        "distinct_statuses": stats,
        "count_by_status": by_status,
        "count_by_category": by_category,
    }

@router.get(
    "/ads/sample",
    response_model=List[AdvertisementDisplay],
    summary="Sample latest ads"
)
def ads_sample(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50)
):
    return (db.query(DbAdvertisement)
              .order_by(DbAdvertisement.created_at.desc())
              .limit(limit)
              .all())
