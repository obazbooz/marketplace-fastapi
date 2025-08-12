from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from schemas import AdvertisementBase
from db.models import DbAdvertisement


def create_advertisement(db: Session , request: AdvertisementBase):
        new_advertisement = DbAdvertisement(
            title= request.title,
            description= request.description,
            category= request.category,
            id = request.id,
            is_reserved = request.is_reserved,
            is_sold = request.is_sold,
            owner_id = request.owner_id
        )
        db.add(new_advertisement)
        # send operation to DB
        db.commit()
        # refresh for getting the ID for the new user in the DB
        db.refresh(new_advertisement)
        return new_advertisement


def update_advertisement(db: Session, id: int , request: AdvertisementBase):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id)
    if not advertisement.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Advertisement with the ID {id} is not found'
                            )
    advertisement.update(
        {
            DbAdvertisement.title : request.title,
            DbAdvertisement.description: request.description,
            DbAdvertisement.category: request.category,
            DbAdvertisement.is_reserved: request.is_reserved,
            DbAdvertisement.is_sold: request.is_sold,
        }
    )
    # send operation to DB
    db.commit()
    return "Update successful"


def delete_advertisement(db: Session, id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Advertisement with the ID {id} is not found'
                            )
    db.delete(advertisement)
    # send operation to DB
    db.commit()
    return "Delete successful"