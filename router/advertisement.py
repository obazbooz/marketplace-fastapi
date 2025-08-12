from fastapi import APIRouter, Depends, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
from schemas import AdvertisementDisplay,AdvertisementBase
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_advertisement

router = APIRouter(
    prefix='/advertisement',
    tags=['advertisement']
)


@router.post('/new',response_model=AdvertisementDisplay)
def create_advertisement(request: AdvertisementBase,db: Session = Depends(get_db)):
    return db_advertisement.create_advertisement(db, request)

@router.post('/update/{id}')
def update_advertisement(id:int, request: AdvertisementBase,db: Session = Depends(get_db)):
    return db_advertisement.update_advertisement(db,id,request)

@router.delete('/delete/{id}')
def delete_advertisement(id: int, db: Session = Depends(get_db)):
    return db_advertisement.delete_advertisement(db,id)

