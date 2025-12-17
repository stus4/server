from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models import Work, WorkTag, Category, Tag, WorkStatus, User   # інші імпорти як потрібно
from database import get_sync_db  # синхронна сесія
from uuid import UUID
from datetime import datetime
import logging
import os
from .user_profile import get_current_user_id as get_current_user
from pathlib import Path
from sqlalchemy.orm import joinedload
from schemas import WorkResponseSchema, WorkCreateSchema, WorkUpdateSchema
router = APIRouter(prefix="/works", tags=["Works"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=WorkResponseSchema)
def create_work(work_data: WorkCreateSchema, db: Session = Depends(get_sync_db)):
    try:
        new_work = Work(
            title=work_data.title,
            author=work_data.author_id,
            description=work_data.description,
            cover_path=work_data.cover_path,
            file_path=work_data.file_path,
            category_id=work_data.category_id,
            status_id=work_data.status_id,
            age_limit=work_data.age_limit,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(new_work)
        db.commit()
        db.refresh(new_work)

        BASE_DIR = Path(__file__).resolve().parent.parent
        works_dir = BASE_DIR / "works"
        work_folder = works_dir / str(new_work.id)
        os.makedirs(work_folder, exist_ok=True)

        if work_data.tag_ids:
            for tag_id in work_data.tag_ids:
                db.add(WorkTag(work_id=new_work.id, tag_id=tag_id))
            db.commit()

        return new_work

    except Exception as e:
        db.rollback()
        logger.error(f"Error while creating work: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while creating work."
        )



@router.get("/", response_model=list)  # або можна залишити WorkResponseSchema, якщо Pydantic сумісний
def get_all_works(db: Session = Depends(get_sync_db)):
    works = db.query(Work)\
        .options(
            joinedload(Work.category),
            joinedload(Work.status),
            joinedload(Work.tags),
            joinedload(Work.author_user)
        ).all()

    result = []
    for work in works:
        result.append({
            "id": work.id,
            "title": work.title,
            "description": work.description,
            "cover_path": work.cover_path,
            "file_path": work.file_path,
            "created_at": work.created_at,
            "updated_at": work.updated_at,
            "age_limit": work.age_limit,
            "category": {
                "id": work.category.id,
                "name": work.category.name,
                "description": work.category.description
            } if work.category else None,
            "status": {
                "id": work.status.id,
                "name": work.status.name
            } if work.status else None,
            "tags": [{"id": tag.id, "name": tag.name} for tag in work.tags],
            "author": {
                "id": work.author_user.id,
                "name": work.author_user.name,
                "last_name": work.author_user.last_name,
                "username": work.author_user.username,
                "avatar_path": work.author_user.avatar_path
            } if work.author_user else None
        })
    return result



@router.get("/{work_id}", response_model=dict)  # або WorkResponseSchema, якщо сумісний
def get_work(work_id: str, db: Session = Depends(get_sync_db)):
    work = db.query(Work)\
        .options(
            joinedload(Work.category),
            joinedload(Work.status),
            joinedload(Work.tags),
            joinedload(Work.author_user)
        ).filter(Work.id == work_id).first()

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    return {
        "id": work.id,
        "title": work.title,
        "description": work.description,
        "cover_path": work.cover_path,
        "file_path": work.file_path,
        "created_at": work.created_at,
        "updated_at": work.updated_at,
        "age_limit": work.age_limit,
        "category": {
            "id": work.category.id,
            "name": work.category.name,
            "description": work.category.description
        } if work.category else None,
        "status": {
            "id": work.status.id,
            "name": work.status.name
        } if work.status else None,
        "tags": [{"id": tag.id, "name": tag.name} for tag in work.tags],
        "author": {
            "id": work.author_user.id,
            "name": work.author_user.name,
            "last_name": work.author_user.last_name,
            "username": work.author_user.username,
            "avatar_path": work.author_user.avatar_path
        } if work.author_user else None
    }


@router.put("/{work_id}", response_model=WorkResponseSchema)
def update_work(
    work_id: str,
    update_data: WorkUpdateSchema,
    db: Session = Depends(get_sync_db),
    current_user: User = Depends(get_current_user)  # поточний автор
):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    # Перевірка, що користувач є автором твору
    if not work or work.author != current_user:
        raise HTTPException(status_code=403, detail="You are not the author of this work")

    data = update_data.dict(exclude_unset=True)

    # Перевірка зовнішніх ключів
    if "category_id" in data and data["category_id"] is not None:
        category = db.query(Category).get(data["category_id"])
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
        work.category_id = data["category_id"]

    if "status_id" in data and data["status_id"] is not None:
        status = db.query(WorkStatus).get(data["status_id"])
        if not status:
            raise HTTPException(status_code=400, detail="Status not found")
        work.status_id = data["status_id"]

    # Оновлення звичайних полів
    for key, value in data.items():
        if key not in ("tags", "category_id", "status_id"):
            setattr(work, key, value)

    # Оновлення тегів
    if "tags" in data:
        work.tags.clear()
        for tag_id in data["tags"]:
            tag = db.query(Tag).get(tag_id)
            if tag:
                work.tags.append(tag)

    work.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(work)
    return work



@router.delete("/{work_id}")
def delete_work(
    work_id: str,
    db: Session = Depends(get_sync_db),
    current_user: User = Depends(get_current_user)
):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    if not work or work.author != current_user:
        raise HTTPException(status_code=403, detail="You are not the author of this work")

    db.delete(work)
    db.commit()
    return {"detail": "Work deleted successfully"}

