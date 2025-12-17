from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Category, Tag, WorkStatus, UserInteraction
from .user_profile import get_viewed_works, get_saved_works
from .search import search_works
from crud import get_liked_works
from typing import List, Optional
from schemas import WorkOut
from sqlalchemy import func
from fastapi.responses import JSONResponse


def get_interaction_stats(db: Session, work_id: str) -> dict:
    return {
        "likes": count_likes(db, work_id),
        "views": count_views(db, work_id),
        "reads": count_reads(db, work_id),
        "saved": count_saves(db, work_id),
    }

def count_likes(db: Session, work_id: str) -> int:
    return db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.work_id == work_id,
        UserInteraction.is_liked == True
    ).scalar() or 0

def count_views(db: Session, work_id: str) -> int:
    return db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.work_id == work_id,
        UserInteraction.is_viewed == True
    ).scalar() or 0

def count_reads(db: Session, work_id: str) -> int:
    return db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.work_id == work_id,
        UserInteraction.is_read == True
    ).scalar() or 0

def count_saves(db: Session, work_id: str) -> int:
    return db.query(func.count(UserInteraction.id)).filter(
        UserInteraction.work_id == work_id,
        UserInteraction.is_saved == True
    ).scalar() or 0

router = APIRouter()
@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    result = [{"id": c.id, "name": c.name, "description": c.description} for c in categories]
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")

@router.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    result = []
    for t in tags:
        result.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "category_name": t.category.name if t.category else None
        })
    return result

@router.get("/users/{user_id}/liked")
def liked_works(user_id: str, db: Session = Depends(get_db)):
    return get_liked_works(db, user_id)

@router.get("/work-statuses")
def get_work_statuses(db: Session = Depends(get_db)):
    statuses = db.query(WorkStatus).all()
    return [{"id": s.id, "name": s.name} for s in statuses]



@router.get("/saved/{user_id}", description="Отримати список збережених творів користувача")
def get_saved(user_id: str, db: Session = Depends(get_db)):
    works = get_saved_works(db, user_id)
    if not works:
        raise HTTPException(status_code=404, detail="Works not found")
    return works


@router.get("/search", response_model=List[WorkOut])
def search_works_endpoint(
    title: Optional[str] = Query(None, description="Пошук за назвою твору"),
    author_name: Optional[str] = Query(None, description="Пошук за ім'ям або ніком автора"),
    tag_names: Optional[List[str]] = Query(None, description="Фільтр за тегами"),
    genre_id: Optional[int] = Query(None, description="Фільтр за жанром"),
    status_id: Optional[int] = Query(None, description="Фільтр за статусом твору"),
    order_by_popularity: bool = Query(False, description="Сортування за популярністю (середній рейтинг)"),
    db: Session = Depends(get_db)
):
    # Виклик функції пошуку з переданими параметрами
    results = search_works(
        db=db,
        title=title,
        author_name=author_name,
        tag_names=tag_names,
        genre_id=genre_id,
        status_id=status_id,
        order_by_popularity=order_by_popularity
    )
    return [
    {
        **work.__dict__,
        "author": work.author_user.username  # просто рядок, ніби нік автора
    } for work in results
]

