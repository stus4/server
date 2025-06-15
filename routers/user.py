from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db  # твоє підключення до БД
from models import User  # модель User
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
def get_user_profile(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers_count = 0  # замінити на реальні дані, якщо є таблиці
    following_count = 0

    # Формуємо список творів користувача
    works_data = []
    for work in user.works:
        works_data.append({
            "id": str(work.id),
            "title": work.title,
            "description": work.description or "",
            "cover_path": work.cover_path or "",
            "category": work.category.name if work.category else None,
            "tags": [tag.name for tag in work.tags],
            "status": work.status.name if work.status else None,
        })

    return JSONResponse(
        content={
            "id": str(user.id),
            "name": user.name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "avatar_path": user.avatar_path,
            "birth": user.birth,
            "bio": user.bio,
            "followers": followers_count,
            "following": following_count,
            "works_count": len(user.works),
            "works": works_data,
        },
        media_type="application/json; charset=utf-8"
    )

