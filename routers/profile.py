from sqlalchemy.orm import Session
from models import User, Work, UserInteraction, Comment
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_db
from schemas import UserProfileOut

router = APIRouter()

@router.get("/me", response_model=UserProfileOut, description="Отримати профіль користувача за user_id")
def read_current_user(user_id: str = Query(..., description="UUID користувача"), db: Session = Depends(get_db)):
    # Перевірка формату user_id — просто перевірка рядка, без конвертації в UUID
    if not isinstance(user_id, str) or len(user_id) == 0:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(user.id),
        "name": user.name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "avatar_path": user.avatar_path,
        "birth": user.birth,
        "bio": user.bio
    }

@router.get("/me/id")
def get_current_user_id(user_id: str, db: Session = Depends(get_db)):
    if not isinstance(user_id, str) or len(user_id) == 0:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    user = get_user_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.id

def get_user_profile(db: Session, user_id: str) -> Optional[User]:
    """
    Отримати інформацію про користувача.
    """
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(db: Session, user_id: str, name: Optional[str] = None,
                        last_name: Optional[str] = None, username: Optional[str] = None,
                        email: Optional[str] = None, phone_number: Optional[str] = None,
                        avatar_path: Optional[str] = None, birth: Optional[int] = None,
                        bio: Optional[str] = None):
    """
    Оновити профіль користувача.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    if name is not None:
        user.name = name
    if last_name is not None:
        user.last_name = last_name
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if phone_number is not None:
        user.phone_number = phone_number
    if avatar_path is not None:
        user.avatar_path = avatar_path
    if birth is not None:
        user.birth = birth
    if bio is not None:
        user.bio = bio

    db.commit()
    return user

def get_own_works(db: Session, user_id: str) -> List[Work]:
    """
    Отримати список власних творів користувача.
    """
    return db.query(Work).filter(Work.author == user_id).all()

def get_saved_works(db: Session, user_id: str) -> List[Work]:
    """
    Отримати список творів, які користувач зберіг (is_saved=True).
    """
    return (
        db.query(Work)
        .join(UserInteraction, UserInteraction.work_id == Work.id)
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_saved == True)
        .all()
    )

def get_liked_works(db: Session, user_id: str) -> List[Work]:
    """
    Отримати список творів, які користувач лайкнув (is_liked=True).
    """
    return (
        db.query(Work)
        .join(UserInteraction, UserInteraction.work_id == Work.id)
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_liked == True)
        .all()
    )

def get_viewed_works(db: Session, user_id: str) -> List[Work]:
    """
    Отримати список творів, які користувач переглянув (is_viewed=True).
    """
    return (
        db.query(Work)
        .join(UserInteraction, UserInteraction.work_id == Work.id)
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_viewed == True)
        .all()
    )

from models import Chapter

def get_commented_works(db: Session, user_id: str) -> List[Work]:
    """
    Отримати список творів, в яких користувач залишив коментарі.
    """
    return (
        db.query(Work)
        .join(Chapter, Chapter.work_id == Work.id)
        .join(Comment, Comment.chapter_id == Chapter.id)
        .filter(Comment.user_id == user_id)
        .distinct()
        .all()
    )

def has_interacted(db: Session, user_id: str, work_id: str, interaction_type: str) -> bool:
    interaction = db.query(UserInteraction).filter_by(
        user_id=user_id,
        work_id=work_id
    ).first()

    if not interaction:
        return False

    if interaction_type == "like":
        return interaction.is_liked
    elif interaction_type == "save":
        return interaction.is_saved
    elif interaction_type == "view":
        return interaction.is_viewed
    elif interaction_type == "read":
        return interaction.is_read
    else:
        return False
