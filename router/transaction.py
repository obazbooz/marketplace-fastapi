from schemas import UserBase , TransactionBase , TransactionDisplay
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_transaction
from auth.oauth2 import get_current_user
from typing import List


router = APIRouter (
    prefix='/transactions',
    tags=['transactions']
)


@router.post('/new',
            response_model=TransactionDisplay,
            status_code=status.HTTP_201_CREATED)

def create_transaction(request:TransactionBase = Depends(TransactionBase.as_form),
                       db : Session = Depends(get_db),
                       current_user: UserBase = Depends(get_current_user)):
    return db_transaction.create_transaction(db , request,current_user.id)


@router.get('/my',
           response_model=List[TransactionDisplay],
           status_code=status.HTTP_200_OK)

def get_transactions(db:Session=Depends(get_db),current_user:UserBase =Depends(get_current_user)):
    return db_transaction.get_user_transactions(db,current_user.id)
