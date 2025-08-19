from fastapi import APIRouter, Depends, status
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List
from schemas import UserBase



router = APIRouter(
    prefix='/user',
    tags=['user']
)

# ✅ Create user
@router.post('/new', response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# ✅ Read all users
#@router.get('/', response_model=List[UserDisplay], status_code=status.HTTP_200_OK)
#def get_all_users(db: Session = Depends(get_db)):
#    return db_user.get_all_users(db)


# ✅ Read one user by ID
#@router.get('/{id}', response_model=UserDisplay, status_code=status.HTTP_200_OK)
#def get_user(id: int, db: Session = Depends(get_db)):
#    return db_user.get_user(db, id)


# ✅ Update user
#@router.put('/{id}', response_model=UserDisplay, status_code=status.HTTP_200_OK)
#def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
#    return db_user.update_user(db, id, request)


# ✅ Delete user
#@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
#def delete_user(id: int, db: Session = Depends(get_db)):
#    db_user.delete_user(db, id)
#    return  