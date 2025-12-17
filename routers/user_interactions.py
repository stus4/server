from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import UserInteraction, Work
from .user_profile import get_current_user_id
from uuid import UUID
from schemas import WorkResponseSchema
from typing import List


router = APIRouter(prefix="/interactions", tags=["User Interactions"])


def get_or_create_interaction(db: Session, user_id: str, work_id: str) -> UserInteraction:
    """Повертає існуючу взаємодію користувача з твором або створює нову"""
    interaction = db.query(UserInteraction).filter_by(user_id=user_id, work_id=work_id).first()
    if not interaction:
        interaction = UserInteraction(user_id=user_id, work_id=work_id)
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
    return interaction


@router.post("/{work_id}/like")
def toggle_like(
    work_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_id)
):
    interaction = get_or_create_interaction(db, current_user, work_id)
    interaction.is_liked = not interaction.is_liked
    db.commit()

    likes = db.query(UserInteraction).filter_by(work_id=work_id, is_liked=True).count()
    return {"likes": likes, "is_liked": interaction.is_liked}


@router.post("/{work_id}/save")
def toggle_save(
    work_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_id)
):
    interaction = get_or_create_interaction(db, current_user, work_id)
    interaction.is_saved = not interaction.is_saved
    db.commit()

    saved = db.query(UserInteraction).filter_by(work_id=work_id, is_saved=True).count()
    return {"saved": saved, "is_saved": interaction.is_saved}


@router.post("/{work_id}/view")
def mark_as_viewed(
    work_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_id)
):
    interaction = get_or_create_interaction(db, current_user, work_id)
    if not interaction.is_viewed:
        interaction.is_viewed = True
        db.commit()

    return {"message": "Viewed status recorded", "is_viewed": interaction.is_viewed}



@router.post("/{work_id}/read")
def mark_as_read(
    work_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_id)
):
    """Позначити твір як прочитаний"""
    if not is_valid_uuid(work_id):
        raise HTTPException(status_code=400, detail="Invalid work_id format")
    if not is_valid_uuid(current_user):
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    interaction = get_or_create_interaction(db, current_user, work_id)
    if not interaction.is_read:
        interaction.is_read = True
        db.commit()

    return {"message": "Read status recorded", "is_read": interaction.is_read}


@router.get("/{work_id}/status")
def get_interaction_status(
    work_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_id)
):
    interaction = db.query(UserInteraction).filter_by(user_id=current_user, work_id=work_id).first()

    return {
        "likes": db.query(UserInteraction).filter_by(work_id=work_id, is_liked=True).count(),
        "views": db.query(UserInteraction).filter_by(work_id=work_id, is_viewed=True).count(),
        "reads": db.query(UserInteraction).filter_by(work_id=work_id, is_read=True).count(),
        "saved": db.query(UserInteraction).filter_by(work_id=work_id, is_saved=True).count(),
        "is_liked": interaction.is_liked if interaction else False,
        "is_saved": interaction.is_saved if interaction else False,
        "is_viewed": interaction.is_viewed if interaction else False
    }
def is_valid_uuid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except ValueError:
        return False
