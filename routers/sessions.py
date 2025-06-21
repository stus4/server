import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Session as SessionModel  # твій клас Session з models.py
from models import User

SESSION_DURATION_HOURS = 24  # тривалість сесії

def create_session(db: Session, user_id: str, ip_address: str = None, user_agent: str = None) -> SessionModel:
    """
    Генерує нову сесію для користувача.
    """
    now = datetime.utcnow()
    session = SessionModel(
        id=str(uuid.uuid4()),
        user_id=user_id,
        created_at=now,
        expires_at=now + timedelta(hours=SESSION_DURATION_HOURS),
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def refresh_session(db: Session, session_id: str) -> bool:
    """
    Оновлює час дії сесії, продовжуючи її життя.
    Повертає True якщо сесія існує та оновлена, False якщо сесії немає.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        return False

    now = datetime.utcnow()
    session.expires_at = now + timedelta(hours=SESSION_DURATION_HOURS)
    db.commit()
    return True

def validate_session(db: Session, session_id: str) -> bool:
    """
    Перевіряє чи існує сесія і чи не закінчився її час.
    """
    now = datetime.utcnow()
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.expires_at > now
    ).first()
    return session is not None

def logout_session(db: Session, session_id: str) -> bool:
    """
    Видаляє сесію (вихід з системи).
    Повертає True якщо сесія видалена, False якщо сесії не було.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        return False

    db.delete(session)
    db.commit()
    return True
