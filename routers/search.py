from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_
from models import Work, User, Tag, WorkTag, Rating
from typing import List, Optional
from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter(prefix="/search", tags=["Search"])

def search_works(db: Session,
                 title: Optional[str] = None,
                 author_name: Optional[str] = None,
                 tag_names: Optional[List[str]] = None,
                 genre_id: Optional[int] = None,
                 status_id: Optional[int] = None,
                 order_by_popularity: bool = False) -> List[Work]:

    query = db.query(Work).options(
        joinedload(Work.author_user),
        joinedload(Work.category),
        joinedload(Work.status),
        joinedload(Work.tags)
    )

    if title:
        query = query.filter(Work.title.ilike(f"%{title}%"))

    if author_name:
        query = query.join(Work.author_user).filter(
            or_(
                User.name.ilike(f"%{author_name}%"),
                User.username.ilike(f"%{author_name}%")
            )
        )

    if genre_id:
        query = query.filter(Work.category_id == genre_id)

    if status_id:
        query = query.filter(Work.status_id == status_id)

    if tag_names:
        query = query.join(WorkTag).join(Tag)
        query = query.filter(Tag.name.in_(tag_names))
        query = query.group_by(Work.id).having(func.count(Tag.id) == len(tag_names))

    if order_by_popularity:
        avg_rating = func.avg(Rating.rating)
        query = query.outerjoin(Rating).group_by(Work.id).order_by(desc(avg_rating))

    return query.all()


@router.get("/search")
def search_works_route(
    title: Optional[str] = None,
    author_name: Optional[str] = None,
    tag_names: Optional[List[str]] = None,
    genre_id: Optional[int] = None,
    status_id: Optional[int] = None,
    order_by_popularity: bool = False,
    db: Session = Depends(get_db),
):
    works = search_works(
        db=db,
        title=title,
        author_name=author_name,
        tag_names=tag_names,
        genre_id=genre_id,
        status_id=status_id,
        order_by_popularity=order_by_popularity
    )

    result = []
    for work in works:
        result.append({
            "id": work.id,
            "title": work.title,
            "description": work.description,
            "cover_path": work.cover_path,
            "file_path": work.file_path,
            "created_at": work.created_at,
            "updated_at": work.updated_at,
            "age_limit": work.age_limit,
            "category": {
                "id": work.category.id,
                "name": work.category.name,
                "description": work.category.description
            } if work.category else None,
            "status": {
                "id": work.status.id,
                "name": work.status.name
            } if work.status else None,
            "tags": [{"id": tag.id, "name": tag.name} for tag in work.tags],
            "author": {
                "id": work.author_user.id,
                "name": work.author_user.name,
                "last_name": work.author_user.last_name,
                "username": work.author_user.username,
                "avatar_path": work.author_user.avatar_path
            } if work.author_user else None
        })
    return result


