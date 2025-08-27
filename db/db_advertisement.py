from fastapi import HTTPException,status,Depends
from sqlalchemy.orm.session import Session
from schemas import AdvertisementBase,AdvertisementStatusBase , SearchFilterBase
from db.models import DbAdvertisement, DbUser
from sqlalchemy import desc, func
from db.models import AdvStatus
from typing import Optional, List



def create_advertisement(db: Session , request: AdvertisementBase,owner_id: int):
        new_advertisement = DbAdvertisement(
            title= request.title,
            description= request.description,
            category= request.category,
            # status=request.status,
            owner_id = owner_id,
            price=request.price,
            location=request.location
        )
        db.add(new_advertisement)
        # send operation to DB
        db.commit()
        # refresh for getting the ID for the new user in the DB
        db.refresh(new_advertisement)
        return new_advertisement


def get_advertisement(db: Session, id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Advertisement with id {id} not found!')
    #note if the raise get executed the rest of the code will not continue with
    #we stop at the error handling section
    return advertisement

def update_advertisement(db: Session, id: int , request: AdvertisementBase, current_user_id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id)

    if not advertisement.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Advertisement with the ID {id} is not found')

    if advertisement.first().owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to update this advertisement")

    advertisement.update(
        {
            DbAdvertisement.title : request.title,
            DbAdvertisement.description: request.description,
            DbAdvertisement.category: request.category,
            DbAdvertisement.price: request.price,
            DbAdvertisement.location: request.location
        }
    )
    # send operation to DB
    db.commit()
    return "Update successful"

def update_advertisement_status(db: Session, id: int , request: AdvertisementStatusBase, current_user_id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id)

    if not advertisement.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Advertisement with the ID {id} is not found')

    if advertisement.first().owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to update this advertisement")

    advertisement.update(
        {
            DbAdvertisement.status : request.status
        }
    )
    # send operation to DB
    db.commit()
    return "Update successful"

def delete_advertisement(db: Session, id: int, current_user_id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Advertisement with the ID {id} is not found')

    if advertisement.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this advertisement"
        )

    db.delete(advertisement)
    # send operation to DB
    db.commit()
    return "Delete successful"

def get_ranked_advertisements(db: Session, limit : int = 20 , offset : int = 0):
    ranked_advertisements = ((db.query(DbAdvertisement)
                             .join(DbUser, DbUser.id == DbAdvertisement.owner_id))
                             .filter(DbAdvertisement.status == AdvStatus.AVAILABLE)
                             .order_by(
        desc(DbAdvertisement.created_at),
        desc(func.coalesce(DbUser.rating_avg, 0.0)),
        desc(func.coalesce(DbUser.rating_count, 0))
        )
    )
    return ranked_advertisements.limit(limit).offset(offset).all()

def search_filter_advertisements(db:Session, request: SearchFilterBase,limit : int = 20, offset : int = 0):
    search_filter_results = db.query(DbAdvertisement).join(DbUser, DbUser.id == DbAdvertisement.owner_id)
    search_filter_results = search_filter_results.filter(DbAdvertisement.title.ilike(f"%{request.title}%"))
    search_filter_results = search_filter_results.filter(DbAdvertisement.category == request.category)
    search_filter_results=  search_filter_results.filter(DbAdvertisement.status == AdvStatus.AVAILABLE)

    if request.start_date and request.end_date:
        search_filter_results = search_filter_results.filter(func.date(DbAdvertisement.created_at).between(request.start_date, request.end_date))
    elif request.start_date:
        search_filter_results = search_filter_results.filter(func.date(DbAdvertisement.created_at) >= request.start_date)
    elif request.end_date:
        search_filter_results = search_filter_results.filter(func.date(DbAdvertisement.created_at) <= request.end_date)
    search_filter_results = search_filter_results.order_by(
        desc(DbAdvertisement.created_at),
        desc(func.coalesce(DbUser.rating_avg, 0.0)),
        desc(func.coalesce(DbUser.rating_count, 0))
    )

    return search_filter_results.limit(limit).offset(offset).all()