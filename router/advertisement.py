from schemas import AdvertisementDisplay,AdvertisementBase
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_advertisement
from schemas import UserBase
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/advertisements',
    tags=['advertisements']
)


@router.post('/new',
             response_model=AdvertisementDisplay,
             summary='Create an advertisement',
             description=' This API call create a new advertisement',
             response_description='Advertisement information',
             status_code=status.HTTP_201_CREATED
             )
def create_advertisement(request: AdvertisementBase = Depends(AdvertisementBase.as_form),
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.create_advertisement(db, request ,current_user.id)


@router.get('/{id}',
            response_model=AdvertisementDisplay,
            summary='View advertisement details',
            description=' This API call view the details of a specified advertisement by ID',
            response_description='Advertisement information',
            status_code=status.HTTP_201_CREATED

            )
def get_advertisement(id: int,
                      db: Session = Depends(get_db),
                      current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.get_advertisement(db,id)


@router.put('/update/{id}',
             summary='Update advertisement',
             description=' This API call update a specified advertisement by ID',
             response_description='Indicates whether the update was successfully completed.',
             status_code=status.HTTP_200_OK
             )
def update_advertisement(id:int,
                         request: AdvertisementBase = Depends(AdvertisementBase.as_form),
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.update_advertisement(db,id,request, current_user.id)


@router.patch('/status-update/{id}',
             summary='Update advertisement status',
             description=' This API call update a specified advertisement status',
             response_description='Indicates whether the status update was successfully completed.',
             status_code=status.HTTP_200_OK
             )
def update_advertisement(id:int,
                         request: AdvertisementBase = Depends(AdvertisementBase.as_form),
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.update_advertisement(db,id,request, current_user.id)


@router.delete('/delete/{id}',
               summary='Delete advertisement',
               description=' This API call delete a specified advertisement by ID',
               response_description='Indicates whether the deletion was successfully completed.',
               status_code=status.HTTP_204_NO_CONTENT
               )
def delete_advertisement(id: int,
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.delete_advertisement(db,id,current_user.id)

