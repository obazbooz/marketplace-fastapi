from schemas import UserBase, RatingBase, RatingDisplay
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_rating
from auth.oauth2 import get_current_user


router = APIRouter (
    prefix='/ratings',
    tags=['ratings']
)

@router.post('/add',response_model=RatingDisplay,status_code=status.HTTP_201_CREATED)
def create_rating(request:RatingBase=Depends(RatingBase.as_form),
                  db:Session = Depends(get_db),
                  current_user : UserBase = Depends(get_current_user)):
    return db_rating.add_rating(db,request,current_user.id)
