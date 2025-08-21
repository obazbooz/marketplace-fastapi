#This file contain the functionality to put data in the database
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException,status

# functionality to put data into our database

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    #send operation to DB
    db.commit()
    #refresh for getting the ID for the new user in the DB
    db.refresh(new_user)
    return new_user


#Read all elements
def get_all_users(db: Session):
    return db.query(DbUser).all()

#Read one user
def get_user(db:Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found!')
    return user

#Read one user by username
def get_user_by_username(db:Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {username} not found!')
    return user

#Update a user
def update_user(db:Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found!')
    user.update(
        {
            DbUser.username : request.username,
            DbUser.email: request.email,
            DbUser.password: Hash.bcrypt(request.password)
        }
    )
    db.commit()
    return "Update successful!"

#Delete a user
def delete_user(db:Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found!')
    db.delete(user)
    db.commit()
    return "Delete successful!"


