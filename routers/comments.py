from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Comment
from pydantic import BaseModel

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

# ---------- Pydantic schemas ----------

class CommentCreate(BaseModel):
    user_id: str
    chapter_id: str
    text: str


class CommentUpdate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    user_id: str
    chapter_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic v2


# ---------- Endpoints ----------

# ➕ Створити коментар
@router.post(
    "/",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    new_comment = Comment(
        user_id=comment.user_id,
        chapter_id=comment.chapter_id,
        text=comment.text,
        created_at=datetime.utcnow()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# 📄 Отримати всі коментарі до розділу
@router.get(
    "/chapter/{chapter_id}",
    response_model=List[CommentResponse]
)
def get_comments_by_chapter(
    chapter_id: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(Comment)
        .filter(Comment.chapter_id == chapter_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


# 📄 Отримати всі коментарі користувача
@router.get(
    "/user/{user_id}",
    response_model=List[CommentResponse]
)
def get_comments_by_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(Comment)
        .filter(Comment.user_id == user_id)
        .order_by(Comment.created_at.desc())
        .all()
    )


# ✏️ Оновити коментар
@router.put(
    "/{comment_id}",
    response_model=CommentResponse
)
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.text = data.text
    db.commit()
    db.refresh(comment)
    return comment


# ❌ Видалити коментар
@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()
