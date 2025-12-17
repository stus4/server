# subscriptions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from database import get_db  # ваша функція для отримання сесії DB
from models import Subscription, User, Work  # ваші моделі
from .user_profile import get_current_user_id as get_current_user # залежність для отримання поточного користувача

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

# --------------------------------------
# Підписка на твір
# --------------------------------------
@router.post("/{work_id}")
def subscribe_to_work(
    work_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Перевірка, чи твір існує
    work = db.query(Work).filter_by(id=work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Твір не знайдено")

    # Перевірка, чи вже підписаний
    existing = db.query(Subscription).filter_by(user_id=current_user, work_id=work_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Вже підписаний на цей твір")

    subscription = Subscription(
    id=str(uuid4()),
    user_id=current_user,
    work_id=work_id,
    created_at=datetime.utcnow()
)

    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return {"message": "Підписка успішно створена", "subscription_id": subscription.id}

# --------------------------------------
# Відписка від твору
# --------------------------------------
@router.delete("/{work_id}")
def unsubscribe_from_work(
    work_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter_by(user_id=current_user, work_id=work_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Підписка не знайдена")

    db.delete(subscription)
    db.commit()
    return {"message": "Ви відписались від твору"}

# --------------------------------------
# Отримати список всіх підписок користувача
# --------------------------------------
@router.get("/")
def get_user_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscriptions = db.query(Subscription).filter_by(user_id=current_user).all()

    return [
        {
            "work_id": sub.work_id,
            "work_title": sub.work.title if sub.work else None,
            "created_at": sub.created_at
        }
        for sub in subscriptions
    ]

# --------------------------------------
# Отримати кількість підписників для певного твору
# --------------------------------------
@router.get("/count/{work_id}")
def get_subscription_count(work_id: str, db: Session = Depends(get_db)):
    count = db.query(Subscription).filter_by(work_id=work_id).count()
    return {"work_id": work_id, "subscribers_count": count}
