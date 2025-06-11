from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from models import Chapter, Work, User
from database import get_db
from schemas import ChapterCreate, ChapterUpdate, ChapterOut
from dependencies import get_current_user

router = APIRouter(prefix="/chapters", tags=["Chapters"])


@router.get("/work/{work_id}", response_model=List[ChapterOut])
def get_chapters_for_work(work_id: UUID, db: Session = Depends(get_db)):
    """Отримання списку розділів твору"""
    return db.query(Chapter).filter(Chapter.work_id == work_id).order_by(Chapter.order).all()


@router.get("/{chapter_id}", response_model=ChapterOut)
def get_chapter(chapter_id: UUID, db: Session = Depends(get_db)):
    """Завантаження вмісту окремого розділу"""
    chapter = db.query(Chapter).get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Розділ не знайдено")
    return chapter


@router.post("/", response_model=ChapterOut, status_code=status.HTTP_201_CREATED)
def create_chapter(
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Додавання нового розділу (автором), з можливістю створення чернетки"""
    work = db.query(Work).get(chapter_data.work_id)
    if not work or work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на додавання розділу")

    new_chapter = Chapter(**chapter_data.dict())
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter


@router.put("/{chapter_id}", response_model=ChapterOut)
def update_chapter(
    chapter_id: UUID,
    chapter_data: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Редагування розділу (автором)"""
    chapter = db.query(Chapter).get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Розділ не знайдено")

    work = db.query(Work).get(chapter.work_id)
    if work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на редагування")

    for key, value in chapter_data.dict(exclude_unset=True).items():
        setattr(chapter, key, value)

    db.commit()
    db.refresh(chapter)
    return chapter


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Видалення розділу (автором)"""
    chapter = db.query(Chapter).get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Розділ не знайдено")

    work = db.query(Work).get(chapter.work_id)
    if work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на видалення")

    db.delete(chapter)
    db.commit()
    return
