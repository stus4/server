from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from models import Comment, User, Work, Chapter
from database import get_db
from schemas import CommentCreate, CommentOut, ReportCommentRequest
from dependencies import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Додавання коментарів до творів або розділів"""
    if not comment_data.work_id and not comment_data.chapter_id:
        raise HTTPException(status_code=400, detail="Потрібно вказати або work_id, або chapter_id")

    if comment_data.work_id:
        if not db.query(Work).filter_by(id=comment_data.work_id).first():
            raise HTTPException(status_code=404, detail="Твір не знайдено")
    if comment_data.chapter_id:
        if not db.query(Chapter).filter_by(id=comment_data.chapter_id).first():
            raise HTTPException(status_code=404, detail="Розділ не знайдено")

    comment = Comment(
        user_id=current_user.id,
        work_id=comment_data.work_id,
        chapter_id=comment_data.chapter_id,
        content=comment_data.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=List[CommentOut])
def get_comments(
    work_id: Optional[UUID] = Query(default=None),
    chapter_id: Optional[UUID] = Query(default=None),
    db: Session = Depends(get_db)
):
    """Перегляд коментарів для твору або розділу"""
    query = db.query(Comment)

    if work_id:
        query = query.filter(Comment.work_id == work_id)
    if chapter_id:
        query = query.filter(Comment.chapter_id == chapter_id)

    return query.order_by(Comment.created_at).all()


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Видалення коментаря (автором або модератором)"""
    comment = db.query(Comment).get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")

    if comment.user_id != current_user.id and not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Немає прав для видалення")

    db.delete(comment)
    db.commit()
    return


@router.post("/{comment_id}/report", status_code=status.HTTP_202_ACCEPTED)
def report_comment(
    comment_id: UUID,
    report: ReportCommentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Скарга на коментар"""
    comment = db.query(Comment).get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")

    # У таблиці скарг зберігаємо id користувача, коментаря, причину
    db.execute(
        """
        INSERT INTO comment_reports (comment_id, user_id, reason)
        VALUES (:comment_id, :user_id, :reason)
        """,
        {"comment_id": str(comment_id), "user_id": str(current_user.id), "reason": report.reason}
    )
    db.commit()
    return {"message": "Скарга прийнята"}
