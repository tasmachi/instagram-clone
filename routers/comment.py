from fastapi import APIRouter,Depends
from .schemas import Comment,CommentBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user
from .schemas import UserAuth
from db import db_comment

router=APIRouter(
    prefix='/comment',
    tags=['comments']
)

@router.post('/create',response_model=Comment)
def create_comment(request:CommentBase,db:Session=Depends(get_db),current_user:UserAuth=Depends(get_current_user)):
    return db_comment.create(db,request)

@router.get('/all/{post_id}',response_model=List[Comment])
def get_all(post_id:int,db:Session=Depends(get_db)):
    return db_comment.get_all(db,post_id)