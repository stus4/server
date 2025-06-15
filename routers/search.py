from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_, or_
from models import Work, User, Tag, WorkTag, Rating
from typing import List, Optional
from fastapi import APIRouter, Depends
from schemas import WorkOut
from database import get_db

def search_works(db: Session,
                 title: Optional[str] = None,
                 author_name: Optional[str] = None,
                 tag_names: Optional[List[str]] = None,
                 genre_id: Optional[int] = None,
                 status_id: Optional[int] = None,
                 order_by_popularity: bool = False) -> List[Work]:

    query = db.query(Work).options(
        joinedload(Work.author_user)  # Завантажуємо пов'язаного автора
    )

    # Пошук за назвою
    if title:
        query = query.filter(Work.title.ilike(f"%{title}%"))

    # Пошук за автором (ім'я або username)
    if author_name:
        # Припускаємо, що у Work є relationship author -> User
        query = query.join(Work.author_user).filter(
    or_(
        User.name.ilike(f"%{author_name}%"),
        User.username.ilike(f"%{author_name}%")
    )
)


    # Фільтр за жанром
    if genre_id:
        query = query.filter(Work.category_id == genre_id)

    # Фільтр за статусом
    if status_id:
        query = query.filter(Work.status_id == status_id)

    # Фільтр за тегами (твір має містити ВСІ теги з tag_names)
    if tag_names:
        # Приєднуємо таблиці тегів
        query = query.join(WorkTag).join(Tag)
        # Фільтруємо теги, які відповідають списку
        query = query.filter(Tag.name.in_(tag_names))
        # Групуємо по твору і відбираємо ті, у яких кількість тегів співпадає з довжиною списку тегів
        query = query.group_by(Work.id).having(func.count(Tag.id) == len(tag_names))

    # Сортування за популярністю (середній рейтинг)
    if order_by_popularity:
        avg_rating = func.avg(Rating.rating)
        query = query.outerjoin(Rating).group_by(Work.id).order_by(desc(avg_rating))

    return query.all()

router = APIRouter(prefix="/search", tags=["Search"])
@router.get("/search", response_model=List[WorkOut])
def search_works_route(
    title: Optional[str] = None,
    author_name: Optional[str] = None,
    tag_names: Optional[List[str]] = None,
    genre_id: Optional[int] = None,
    status_id: Optional[int] = None,
    order_by_popularity: bool = False,
    db: Session = Depends(get_db),
):
    return search_works(
        db=db,
        title=title,
        author_name=author_name,
        tag_names=tag_names,
        genre_id=genre_id,
        status_id=status_id,
        order_by_popularity=order_by_popularity
    )

