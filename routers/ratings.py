from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Rating
import uuid

def set_rating(db: Session, work_id: uuid.UUID, user_id: uuid.UUID, rating: int):
    """
    Додати або оновити оцінку користувача для твору.
    rating має бути від 1 до 5.
    """
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")

    existing_rating = (
        db.query(Rating)
        .filter(Rating.work_id == work_id, Rating.user_id == user_id)
        .first()
    )

    if existing_rating:
        existing_rating.rating = rating
    else:
        new_rating = Rating(work_id=work_id, user_id=user_id, rating=rating)
        db.add(new_rating)

    db.commit()


def get_average_rating(db: Session, work_id: uuid.UUID) -> float:
    """
    Повертає середню оцінку твору (float) або 0.0, якщо оцінок немає.
    """
    avg = db.query(func.avg(Rating.rating)).filter(Rating.work_id == work_id).scalar()
    return float(avg) if avg is not None else 0.0


def get_user_rating(db: Session, work_id: uuid.UUID, user_id: uuid.UUID) -> int | None:
    """
    Повертає оцінку користувача для певного твору, або None, якщо оцінка відсутня.
    """
    rating = (
        db.query(Rating.rating)
        .filter(Rating.work_id == work_id, Rating.user_id == user_id)
        .scalar()
    )
    return rating
