from fastapi import APIRouter,Depends
from schemas import UserBase,MessageBase,MessageDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_message
from auth.oauth2 import get_current_user

from typing import List


router = APIRouter(
    prefix= '/messages',
    tags=['messages']
)


#create message
@router.post('/send',
             response_model= MessageDisplay,
             summary='Send a new message',
             description=' This API call sends a message from user to another user about product',
             response_description='Message details'
             )
def send_message(
        request :MessageBase = Depends(MessageBase.as_form),
        db : Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)):
    return db_message.send_message(db, request, current_user.id)



#get conversation
@router.get('/conversations/{user_id}/{advertisement_id}',
             response_model= List[MessageDisplay],
             summary='Get a conversation',
             description=' This API call gets a conversation between user1 and user2 about product',
             response_description='conversation details'
             )
def get_conversation(
        user_id: int,
        advertisement_id: int,
        db : Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),
):
    return db_message.get_conversation(db, current_user.id ,user_id, advertisement_id)