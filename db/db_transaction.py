from schemas import TransactionBase
from db.models import DbTransaction, DbAdvertisement,AdvStatus
from fastapi import HTTPException
from sqlalchemy.orm.session import Session


def create_transaction(db:Session,request:TransactionBase, seller_id:int):
    ad = db.query(DbAdvertisement).filter(DbAdvertisement.id == request.advertisement_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

        # Seller must own the advertisement
    if ad.owner_id != seller_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this advertisement")

        # Ad must be available
    if ad.status != AdvStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="Advertisement is not available for sale")

    transaction = DbTransaction(
        advertisement_id = request.advertisement_id,
        buyer_id = request.buyer_id,
        seller_id= seller_id
    )

    db.add(transaction)

    ad.status = AdvStatus.SOLD

    db.commit()
    db.refresh(transaction)
    return transaction



def get_user_transactions(db: Session, user_id: int):
    return db.query(DbTransaction).filter(
        (DbTransaction.buyer_id == user_id) | (DbTransaction.seller_id == user_id)
    ).all()

