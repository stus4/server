from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models import Work, WorkTag, Tag  # інші імпорти як потрібно
from database import get_sync_db  # синхронна сесія
from uuid import UUID
from datetime import datetime
import logging
import os
from pathlib import Path
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


@router.get("/", response_model=list[WorkResponseSchema])
def get_all_works(db: Session = Depends(get_sync_db)):
    works = db.query(Work).all()
    return works


@router.get("/{work_id}", response_model=WorkResponseSchema)
def get_work(work_id: UUID, db: Session = Depends(get_sync_db)):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    return work


@router.put("/{work_id}", response_model=WorkResponseSchema)
def update_work(work_id: UUID, update_data: WorkUpdateSchema, db: Session = Depends(get_sync_db)):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    data = update_data.dict(exclude_unset=True)

    # Оновлення звичайних полів
    for key, value in data.items():
        if key != "tags":
            setattr(work, key, value)


    if "tags" in data:
        work.tags.clear()  # видаляємо всі поточні зв’язки
        for tag_id in data["tags"]:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                work.tags.append(tag)

    work.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(work)
    return work



@router.delete("/{work_id}")
def delete_work(work_id: UUID, db: Session = Depends(get_sync_db)):
    work = db.query(Work).filter(Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    db.delete(work)
    db.commit()
    return {"detail": "Work deleted successfully"}
