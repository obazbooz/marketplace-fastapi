from fastapi import APIRouter,Depends
from schemas import UserBase,UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List


router = APIRouter(
    prefix= '/user',
    tags=['user']
)


#create user
@router.post('/new',
             response_model= UserDisplay,
             summary='Register a user',
             description=' This API call register new user in the DB',
             response_description='User information:ID-Username-Password'
             )
def create_user(request :UserBase = Depends(UserBase.as_form), db : Session = Depends(get_db)):
    return db_user.create_user(db, request)


#Read all users
# @router.get('/', response_model=List[UserDisplay])
# def get_all_users(db: Session = Depends(get_db)):
#     return db_user.get_all_users(db)

#Read one user
# @router.get('/{id}',response_model=UserDisplay)
# def get_user(id: int, db: Session = Depends(get_db)):
#     return db_user.get_user(db,id)


#Update user
# @router.post('/{id}/update')
# def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
#     return db_user.update_user(db,id, request)


#Delete user
# @router.post('/delete/{id}')
# def delete(id: int, db: Session = Depends(get_db)):
#     return db_user.delete_user(db,id)