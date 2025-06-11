from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Category, Tag, WorkStatus
from .profile import get_viewed_works
from typing import List, Optional
from schemas import WorkOut
from uuid import UUID
from .search import search_works
router = APIRouter()

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [{"id": c.id, "name": c.name, "description": c.description} for c in categories]

@router.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [{"id": t.id, "name": t.name, "description": t.description} for t in tags]

@router.get("/work-statuses")
def get_work_statuses(db: Session = Depends(get_db)):
    statuses = db.query(WorkStatus).all()
    return [{"id": s.id, "name": s.name} for s in statuses]

@router.get("/history/{user_id}", response_model=List[WorkOut])
def get_history(user_id: UUID, db: Session = Depends(get_db)):
    return get_viewed_works(db, user_id)
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

