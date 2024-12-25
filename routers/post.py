from fastapi import APIRouter,Depends,File,UploadFile
from .schemas import PostDisplay,PostBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from auth.oauth2 import get_current_user
from db import db_post
from .schemas import UserAuth
import shutil
import random
from typing import List
import string
import os

router=APIRouter(
    prefix='/post',
    tags=['post']
)

@router.post('',response_model=PostDisplay)
def create_post(request:PostBase,db:Session=Depends(get_db),current_user:UserAuth=Depends(get_current_user)):
    return db_post.create_post(db,request)

@router.get('/all',response_model=List[PostDisplay])
def posts(db:Session=Depends(get_db)):
    return db_post.get_all_posts(db)

@router.post('/image')
async def upload_file(image:UploadFile=File(...),current_user:UserAuth=Depends(get_current_user)):
    letter=string.ascii_letters
    rand_str=''.join(random.choices(letter,k=6))
    new=f'_{rand_str}.'
    filename=new.join(image.filename.rsplit('.',1))
    path=os.path.join('media',filename)

    with open(path,'wb+') as buffer:
        shutil.copyfileobj(image.file,buffer)

    return {'filename':path}
    
@router.get('/delete/{id}')
def delete(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return db_post.delete(db,id,current_user.id)