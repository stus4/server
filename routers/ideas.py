from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Idea, IdeaWork
from schemas import IdeaCreate, IdeaResponse, IdeaWorkCreate, IdeaWorkResponse
from .user_profile import get_current_user_id as get_current_user

router = APIRouter(prefix="/idea-works", tags=["idea-works"])
# Створити нову ідею
@router.post("/", response_model=IdeaResponse)
def create_idea(idea: IdeaCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_idea = Idea(
        user_id=current_user,
        title=idea.title,
        description=idea.description
    )
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    return new_idea

# Отримати всі ідеї
@router.get("/", response_model=List[IdeaResponse])
def get_all_ideas(db: Session = Depends(get_db)):
    ideas = db.query(Idea).all()
    return ideas

# Отримати одну ідею по id
@router.get("/{idea_id}", response_model=IdeaResponse)
def get_idea(idea_id: str, db: Session = Depends(get_db)):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea

# Прив'язати твір до ідеї
@router.post("/add-work", response_model=IdeaWorkResponse)
def add_work_to_idea(data: IdeaWorkCreate, db: Session = Depends(get_db)):
    # Перевірка, чи такий зв'язок вже існує
    exists = db.query(IdeaWork).filter(
        IdeaWork.idea_id == data.idea_id,
        IdeaWork.work_id == data.work_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="This work is already linked to the idea")

    idea_work = IdeaWork(idea_id=data.idea_id, work_id=data.work_id)
    db.add(idea_work)
    db.commit()
    db.refresh(idea_work)
    return idea_work

# Отримати всі твори за ідеєю
@router.get("/{idea_id}/works", response_model=List[IdeaWorkResponse])
def get_works_for_idea(idea_id: str, db: Session = Depends(get_db)):
    works = db.query(IdeaWork).filter(IdeaWork.idea_id == idea_id).all()
    return works

