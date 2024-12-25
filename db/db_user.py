from sqlalchemy.orm.session import Session
from routers.schemas import UserBase
from .models import DbUser
from fastapi import HTTPException,status
from .hashing import Hash

def create_user(db:Session,request:UserBase):
    new_user=DbUser(
        username=request.username,
        email=request.email,
        password=Hash.hash_password(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db:Session,username:str):
    user=db.query(DbUser).filter(DbUser.username==username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with {username} not found')
    return user