from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, Integer
from database import get_db
from models import Work, UserInteraction

router = APIRouter()

@router.get("/popular")
def get_popular_works(db: Session = Depends(get_db)):
    # Підзапит: підрахунок всіх дій користувача по творах
    interaction_counts = (
    db.query(
        UserInteraction.work_id,
        func.sum(UserInteraction.is_viewed.cast(Integer)).label("views"),
        func.sum(UserInteraction.is_liked.cast(Integer)).label("likes"),
        func.sum(UserInteraction.is_read.cast(Integer)).label("reads"),
        func.sum(UserInteraction.is_saved.cast(Integer)).label("saves"),
    )
    .group_by(UserInteraction.work_id)
    .subquery()
)


    # Основний запит з приєднаними таблицями
    works_with_data = (
        db.query(Work,
                 interaction_counts.c.views,
                 interaction_counts.c.likes,
                 interaction_counts.c.reads,
                 interaction_counts.c.saves)
        .join(interaction_counts, Work.id == interaction_counts.c.work_id)
        .options(
            joinedload(Work.author_user),
            joinedload(Work.category),
            joinedload(Work.tags)
        )
        .order_by(desc(interaction_counts.c.views))  # можна змінити на будь-яке інше сортування
        .all()
    )

    # Формування результату
    result = []
    for work, views, likes, reads, saves in works_with_data:
        result.append({
            "id": str(work.id),
            "title": work.title,
            "description": work.description,
            "author": work.author_user.name if work.author_user else "Невідомий автор",
            "genres": [work.category.name] if work.category else [],
            "tags": [tag.name for tag in work.tags],
            "views": views,
            "likes": likes,
            "reads": reads,
            "saves": saves
        })

    return result
