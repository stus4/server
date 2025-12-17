from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database import get_db
from models import Rating
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Work
from schemas import RatingCreate, RatingUpdate, RatingOut, RatingResponse
from .user_profile import get_current_user_id as get_current_user

router = APIRouter(prefix="/ratings", tags=["Ratings"])
@router.post("/", response_model=RatingOut)
def rate_work(
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # 1️⃣ Перевірка існування твору
    work = db.query(Work).filter(Work.id == data.work_id).first()
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )

    # 2️⃣ Перевірка чи вже є рейтинг
    rating = db.query(Rating).filter(
        Rating.work_id == data.work_id,
        Rating.user_id == current_user
    ).first()

    if rating:
        rating.rating = data.rating
    else:
        rating = Rating(
            work_id=data.work_id,
            user_id=current_user,
            rating=data.rating
        )
        db.add(rating)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to save rating"
        )

    db.refresh(rating)
    return rating
@router.get("/my/{work_id}", response_model=RatingOut)
def get_my_rating(
    work_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    rating = db.query(Rating).filter(
        Rating.work_id == work_id,
        Rating.user_id == current_user
    ).first()

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )

    return rating
@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    work_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    rating = db.query(Rating).filter(
        Rating.work_id == work_id,
        Rating.user_id == current_user
    ).first()

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )

    db.delete(rating)
    db.commit()
from sqlalchemy import func

@router.get("/works/{work_id}/ratings", response_model=List[RatingResponse])
def get_ratings_for_work(work_id: str, db: Session = Depends(get_db)):
    result = db.execute(select(Rating).where(Rating.work_id == work_id))
    ratings = result.scalars().all()
    return ratings

@router.get("/average/{work_id}")
def get_average_rating(
    work_id: str,
    db: Session = Depends(get_db),
):
    avg_rating = db.query(func.avg(Rating.rating)).filter(
        Rating.work_id == work_id
    ).scalar()

    return {
        "work_id": work_id,
        "average_rating": round(avg_rating, 2) if avg_rating else None
    }
