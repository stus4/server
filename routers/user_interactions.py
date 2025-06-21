from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models import UserInteraction, Work
from .profile import get_current_user_id
from .work_metadata import get_interaction_stats
from schemas import InteractionStats

router = APIRouter(prefix="/interactions", tags=["User Interactions"])

@router.post("/{work_id}/like")
def toggle_like(work_id: str, user_id: str = Body(...), db: Session = Depends(get_db)):
    interaction = db.query(UserInteraction).filter_by(user_id=user_id, work_id=work_id).first()

    if interaction:
        interaction.is_liked = not interaction.is_liked
        action = "прибрав лайк" if not interaction.is_liked else "поставив лайк"
        print(f"Користувач {user_id} {action} твору {work_id}")
    else:
        interaction = UserInteraction(
            user_id=user_id,
            work_id=work_id,
            is_liked=True
        )
        db.add(interaction)
        print(f"Користувач {user_id} поставив лайк твору {work_id}")

    db.commit()

    likes = db.query(UserInteraction).filter_by(work_id=work_id, is_liked=True).count()
    return {
        "likes": likes,
    }

@router.post("/{work_id}/save")
def toggle_save(work_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user_id)):
    interaction = db.query(UserInteraction).filter_by(user_id=current_user, work_id=work_id).first()

    if interaction:
        interaction.is_saved = not interaction.is_saved
    else:
        interaction = UserInteraction(
            user_id=current_user,
            work_id=work_id,
            is_saved=True
        )
        db.add(interaction)

    db.commit()

    saved = db.query(UserInteraction).filter_by(work_id=work_id, is_saved=True).count()
    return {"saved": saved}

@router.get("/{work_id}/status")
def get_interaction_status(
    work_id: str,
    user_id: str = Query(...),  # ← приймаємо user_id з параметрів
    db: Session = Depends(get_db)
):
    interaction = db.query(UserInteraction).filter_by(user_id=user_id, work_id=work_id).first()

    total_likes = db.query(UserInteraction).filter_by(work_id=work_id, is_liked=True).count()
    total_views = db.query(UserInteraction).filter_by(work_id=work_id, is_viewed=True).count()
    total_reads = db.query(UserInteraction).filter_by(work_id=work_id, is_read=True).count()
    total_saved = db.query(UserInteraction).filter_by(work_id=work_id, is_saved=True).count()

    return {
        "likes": total_likes,
        "views": total_views,
        "reads": total_reads,
        "saved": total_saved,
        "is_liked": interaction.is_liked if interaction else False,
        "is_saved": interaction.is_saved if interaction else False
    }
@router.post("/{work_id}/view")
def mark_as_viewed(
    work_id: str,
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    interaction = db.query(UserInteraction).filter_by(work_id=work_id, user_id=user_id).first()

    if interaction:
        if not interaction.is_viewed:
            interaction.is_viewed = True
            db.commit()
    else:
        new_interaction = UserInteraction(
            work_id=work_id,
            user_id=user_id,
            is_viewed=True
        )
        db.add(new_interaction)
        db.commit()

    return {"message": "Viewed status recorded"}
