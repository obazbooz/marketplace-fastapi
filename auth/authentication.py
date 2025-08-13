# We want to implement the token endpoint , so we need to create
#antoher route  in our main file to have an exposed endpoint that's called token.


from fastapi import APIRouter,HTTPException,status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from db import models
from db.hash import Hash
from auth import oauth2


router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def get_token(
        request : OAuth2PasswordRequestForm = Depends(),
        db : Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()
    if not user:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Invalid credentials',
                             headers={"WWW-Authenticate": "Bearer"},
                             )
    if not Hash.verify(user.password, request.password):
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Incorrect password',
                             headers={"WWW-Authenticate": "Bearer"},
                             )
    access_token = oauth2.create_access_token(
        data={'sub': user.username}
    )
    return {
        'access_token':access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'user_name': user.username
    }