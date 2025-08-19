from fastapi import APIRouter, Depends, Header, Cookie, Form, status
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
from schemas import AdvertisementDisplay,AdvertisementBase
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_advertisement
from schemas import UserBase
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/advertisement',
    tags=['advertisement']
)


@router.post('/new',response_model=AdvertisementDisplay, status_code=status.HTTP_201_CREATED)
def create_advertisement(request: AdvertisementBase,
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.create_advertisement(db, request)

@router.get('/{id}', response_model=AdvertisementDisplay, status_code=status.HTTP_200_OK)
def get_advertisement(id: int,
                      db: Session = Depends(get_db),
                      current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.get_advertisement(db,id)



@router.post('/update/{id}', status_code=status.HTTP_200_OK, response_model=AdvertisementDisplay)
def update_advertisement(id:int,
                         request: AdvertisementBase,
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.update_advertisement(db,id,request)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(id: int,
                         db: Session = Depends(get_db),
                         current_user: UserBase = Depends(get_current_user)):
    return db_advertisement.delete_advertisement(db,id)

