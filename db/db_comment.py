from sqlalchemy.orm.session import Session
from routers.schemas import CommentBase
from .models import DbComment
from datetime import datetime

def create(db: Session, request:CommentBase):
    new_comment=DbComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db:Session,post_id):
    return db.query(DbComment).filter(DbComment.post_id==post_id).all()