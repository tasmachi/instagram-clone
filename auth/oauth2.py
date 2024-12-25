from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from db.database import get_db
from jose import JWTError, jwt
from datetime import datetime, timedelta
from db import db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = '964ef439fdf658941c2cda61b3738b39bb11d27b23f549962cdba03ab6487cdc'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str=Depends(oauth2_scheme),db: Session=Depends(get_db)):
  credentials_exception=HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Could not validate credentials',
    headers={'www-Authenticate':'Bearer'}
  )
  try:
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    username: str=payload.get('username')
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user=db_user.get_user_by_username(db,username)

  if user is None:
    raise credentials_exception
  
  return user
  