from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session as DbSession
from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
from database import get_db
from models import Session as SessionModel, User
from schemas import SessionCreate, SessionResponse  # Потрібно створити відповідні Pydantic схеми
from .user_profile import get_current_user_id as get_current_user # залежність для отримання поточного користувача

router = APIRouter(prefix="/sessions", tags=["sessions"])
@router.post("/sessions")
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    new_session = SessionModel(
        user_id=session.user_id,
        ip_address=session.ip_address,
        user_agent=session.user_agent,
        expires_at=session.expires_at or datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session
# --- Отримання сесій користувача ---
@router.get("/user/{user_id}", response_model=list[SessionResponse])
def get_user_sessions(user_id: str, db: DbSession = Depends(get_db)):
    sessions = db.query(SessionModel).filter_by(user_id=user_id).all()
    return sessions


# --- Перевірка дійсності сесії ---
@router.get("/validate/{session_id}")
def validate_session(session_id: str, db: DbSession = Depends(get_db)):
    session = db.query(SessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    is_valid = session.expires_at > datetime.utcnow()
    return {"session_id": session.id, "valid": is_valid}


# --- Видалення конкретної сесії (лог-аут) ---
@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, db: DbSession = Depends(get_db)):
    session = db.query(SessionModel).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    db.delete(session)
    db.commit()
    return


# --- Масове видалення сесій користувача ---
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_user_sessions(user_id: str, db: DbSession = Depends(get_db)):
    db.query(SessionModel).filter_by(user_id=user_id).delete()
    db.commit()
    return
