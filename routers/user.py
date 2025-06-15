from fastapi import APIRouter, Depends, HTTPException, Query, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db  # твоє підключення до БД
from models import User, UserInteraction, Work  # модель User
from fastapi.responses import JSONResponse
from typing import List, Optional
from schemas import WorkOut
from sqlalchemy.orm import joinedload
from fastapi.encoders import jsonable_encoder

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



@router.get("/saved_works/{user_id}")
def get_saved_works(user_id: UUID, db: Session = Depends(get_db)):
    try:
        saved_interactions = db.query(UserInteraction).options(
            joinedload(UserInteraction.work).joinedload(Work.author_user)
        ).filter(
            UserInteraction.user_id == user_id,
            UserInteraction.is_saved == True
        ).all()

        works = [interaction.work for interaction in saved_interactions]

        # Коректне кодування в JSON з підтримкою кирилиці
        encoded = jsonable_encoder(works)
        return JSONResponse(content=encoded, media_type="application/json; charset=utf-8")

    except Exception as e:
        print(f"Error fetching saved works for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Помилка сервера при отриманні збережених робіт")

@router.get("/liked_works/{user_id}")
def get_liked_works(user_id: UUID, db: Session = Depends(get_db)):
    try:
        liked_interactions = db.query(UserInteraction).options(
            joinedload(UserInteraction.work).joinedload(Work.author_user)
        ).filter(
            UserInteraction.user_id == user_id,
            UserInteraction.is_liked == True
        ).all()

        works = [interaction.work for interaction in liked_interactions]

        encoded = jsonable_encoder(works)
        return JSONResponse(content=encoded, media_type="application/json; charset=utf-8")

    except Exception as e:
        print(f"Error fetching liked works for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Помилка сервера при отриманні уподобаних робіт")

@router.get("/history/{user_id}")
def get_history(user_id: UUID, db: Session = Depends(get_db)):
    try:
        viewed_interactions = db.query(UserInteraction).options(
            joinedload(UserInteraction.work).joinedload(Work.author_user)
        ).filter(
            UserInteraction.user_id == user_id,
            UserInteraction.is_viewed == True
        ).order_by(UserInteraction.id.desc()).all()  # сортуємо по id за спаданням

        works = [interaction.work for interaction in viewed_interactions]

        encoded = jsonable_encoder(works)
        return JSONResponse(content=encoded, media_type="application/json; charset=utf-8")

    except Exception as e:
        print(f"Error fetching view history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Помилка сервера при отриманні історії переглядів")
