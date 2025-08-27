from schemas import UserBase , TransactionBase , TransactionDisplay
from fastapi import APIRouter,Depends,status, Response
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

#default response status
@router.get('/my',
           response_model=List[TransactionDisplay],
           status_code=status.HTTP_200_OK)

def get_transactions(db:Session=Depends(get_db),current_user:UserBase =Depends(get_current_user)):
    transactions_list =  db_transaction.get_user_transactions(db,current_user.id)
    empty_list = ['You do not have any transactions yet']
    if not transactions_list:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return transactions_list
