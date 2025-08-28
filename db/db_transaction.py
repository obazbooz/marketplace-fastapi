from schemas import TransactionBase
from db.models import DbTransaction, DbAdvertisement,AdvStatus, DbUser
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session


def create_transaction(db:Session,request:TransactionBase, seller_id:int):
    ad = db.query(DbAdvertisement).join(DbUser, DbUser.id == DbAdvertisement.owner_id).filter(DbAdvertisement.id == request.advertisement_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")

        # Seller must own the advertisement
    if ad.owner_id != seller_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not the owner of this advertisement")

        # Ad must be available
    if ad.status != AdvStatus.AVAILABLE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement is not available for sale")

    buyer = db.query(DbUser).filter(DbUser.id == request.buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")

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

