import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from schemas import LoginRequest, RegisterRequest
from database import get_db
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

router = APIRouter()

@router.post('/register')
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    logging.info(f"[REGISTER] Запит на реєстрацію користувача: {request.email}")

    if db.query(User).filter(User.email == request.email).first():
        logging.warning(f"[REGISTER] Спроба реєстрації з існуючим email: {request.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email вже використовується")

    if db.query(User).filter(User.username == request.username).first():
        logging.warning(f"[REGISTER] Спроба реєстрації з існуючим username: {request.username}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ім'я користувача вже використовується")

    birth_year = None
    if request.birth:
        try:
            dt = datetime.strptime(request.birth.split("T")[0], "%Y-%m-%d")
            birth_year = dt.year
        except ValueError:
            logging.error(f"[REGISTER] Невірний формат дати народження: {request.birth}")
            raise HTTPException(status_code=400, detail="Невірний формат дати народження.")

    new_user = User(
        id=uuid.uuid4(),
        name=request.name,
        last_name=request.last_name,
        username=request.username,
        email=request.email,
        password=hash_password(request.password),
        phone_number=request.phone_number,
        avatar_path=request.avatar_path,
        birth=birth_year,
        bio=request.bio
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logging.info(f"[REGISTER] Користувач успішно зареєстрований: {request.email} (ID: {new_user.id})")

    return {
        "success": True,
        "message": "Успішна реєстрація",
        "userId": str(new_user.id)
    }

@router.post('/login')
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    logging.info(f"[LOGIN] Спроба входу користувача: {request.email}")

    user = db.query(User).filter(User.email == request.email).first()

    if user is None or not verify_password(request.password, user.password):
        logging.warning(f"[LOGIN] Невірний логін або пароль для email: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний логін або пароль",
        )

    logging.info(f"[LOGIN] Користувач увійшов успішно: {request.email} (ID: {user.id})")

    return {
        "success": True,
        "message": "Успішний вхід",
        "userId": str(user.id)
    }
