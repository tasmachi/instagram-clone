from fastapi import APIRouter,Depends
from .schemas import UserDisplay,UserBase
from db.database import get_db
from auth import oauth2
from sqlalchemy.orm.session import Session
from db import db_user

router=APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/signup')
def create_user(request:UserBase,db:Session=Depends(get_db)):
    user=db_user.create_user(db,request)

    access_token=oauth2.create_access_token(data={'username':user.username})

    return {
        'access_token':access_token,
        'token_type':'bearer',
        'user_id':user.id,
        'username':user.username
    }
