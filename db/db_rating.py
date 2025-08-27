from schemas import RatingBase
from db.models import  DbTransaction, DbRating, DbUser
from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from sqlalchemy import func

def add_rating(db:Session, request:RatingBase , rater_id: int):
    transaction = db.query(DbTransaction).filter(request.transaction_id == DbTransaction.id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    #Only buyer can rate
    if rater_id != transaction.buyer_id:
        raise HTTPException(status_code=403, detail="Only the buyer can rate this transaction")

    # always seller
    ratee_id  = transaction.seller_id

    # Prevent duplicate from this buyer for this transaction
    exists = db.query(DbRating).filter(
        DbRating.transaction_id == transaction.id,
        DbRating.rater_id == rater_id
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="You already rated this transaction")


    rating = DbRating (
        transaction_id = transaction.id,
        rater_id = rater_id,
        ratee_id = ratee_id,
        score = int(request.score)
    )

    db.add(rating)
    db.commit()
    db.refresh(rating)

    # Recompute seller aggregates
    avg, count = db.query(
        func.avg(DbRating.score), func.count(DbRating.id)
    ).filter(DbRating.ratee_id == ratee_id).first()

    seller = db.query(DbUser).filter(DbUser.id == ratee_id).first()

    if seller:
        seller.rating_avg = round (float(avg),2) if avg is not None else None
        seller.rating_count = int (count or 0)
        db.commit()


    return rating






