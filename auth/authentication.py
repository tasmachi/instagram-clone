from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import DbUser
from auth import oauth2
from db.hashing import Hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=['authentations']
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(DbUser).filter(DbUser.username==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid credentails!')
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='incorrect password!')
    
    access_token=oauth2.create_access_token(data={'username':user.username})
    return {
        'access_token':access_token,
        'token_type':'bearer',
        'user_id':user.id,
        'username':user.username
    }