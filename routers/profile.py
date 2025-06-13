from sqlalchemy.orm import Session
from models import User, Work, UserInteraction, Comment
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
router = APIRouter()

@router.get("/me")
def read_current_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    user = get_user_profile(db, user_uuid)
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
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    user = get_user_profile(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.id

def get_user_profile(db: Session, user_id: uuid.UUID) -> Optional[User]:
    """
    Отримати інформацію про користувача (аватар, біо та інші поля).
    Повертає None, якщо користувача не знайдено.
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user_profile(db: Session, user_id: uuid.UUID, name: Optional[str] = None,
                        last_name: Optional[str] = None, username: Optional[str] = None,
                        email: Optional[str] = None, phone_number: Optional[str] = None,
                        avatar_path: Optional[str] = None, birth: Optional[int] = None,
                        bio: Optional[str] = None):
    """
    Оновити профіль користувача. Передаються тільки ті поля, які потрібно змінити.
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


def get_own_works(db: Session, user_id: uuid.UUID) -> List[Work]:
    """
    Отримати список власних творів користувача.
    """
    return db.query(Work).filter(Work.author == user_id).all()


def get_saved_works(db: Session, user_id: uuid.UUID) -> List[Work]:
    """
    Отримати список творів, які користувач зберіг (is_saved=True).
    """
    return (
        db.query(Work)
        .join(UserInteraction, UserInteraction.work_id == Work.id)
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_saved == True)
        .all()
    )


def get_liked_works(db: Session, user_id: uuid.UUID) -> List[Work]:
    """
    Отримати список творів, які користувач лайкнув (is_liked=True).
    """
    return (
        db.query(Work)
        .join(UserInteraction, UserInteraction.work_id == Work.id)
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_liked == True)
        .all()
    )


from models import Chapter

def get_commented_works(db: Session, user_id: uuid.UUID) -> List[Work]:
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
def get_viewed_works(db: Session, user_id: uuid.UUID) -> List[Work]:
    """
    Отримати список творів, які користувач переглянув (is_viewed=True).
    """
    return (
        db.query(Work)
        .join(UserInteraction, UserInteraction.work_id == Work.id)
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_viewed == True)
        .all()
    )



