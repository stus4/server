import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
import pyotp
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
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
        id=str(uuid.uuid4()),
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

    # 1. перевірка пароля
    if user is None or not verify_password(request.password, user.password):
        logging.warning(f"[LOGIN] Невірний логін або пароль: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний логін або пароль",
        )

    # 2. 🔐 перевірка 2FA
    if user.twofa_enabled:
        logging.info(f"[LOGIN] 2FA required for user: {user.email}")

        return {
            "success": True,
            "message": "Потрібна двофакторна автентифікація",
            "need_2fa": True,
            "userId": str(user.id)
        }

    # 3. якщо 2FA немає → звичайний логін
    logging.info(f"[LOGIN] Успішний вхід без 2FA: {request.email}")

    return {
        "success": True,
        "message": "Успішний вхід",
        "need_2fa": False,
        "userId": str(user.id)
    }
@router.post("/2fa/verify-login")
def verify_login_2fa(user_id: str, code: str, db: Session = Depends(get_db)):
    logging.info(f"[2FA LOGIN] Перевірка коду для user_id: {user_id}")

    # 1. шукаємо користувача
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. перевіряємо чи 2FA взагалі увімкнена
    if not user.twofa_enabled or not user.twofa_secret:
        raise HTTPException(status_code=400, detail="2FA not enabled")

    # 3. чистимо код (щоб не падало через пробіли)
    code = code.replace(" ", "")

    # 4. перевірка OTP
    totp = pyotp.TOTP(user.twofa_secret)

    if not totp.verify(code):
        logging.warning(f"[2FA LOGIN] Invalid code for user: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid code")

    # 5. успішний логін
    logging.info(f"[2FA LOGIN] Success for user: {user.email}")

    return {
        "success": True,
        "message": "2FA login successful",
        "userId": str(user.id)
    }
@router.post("/2fa/setup")
def setup_2fa(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. генеруємо secret
    secret = pyotp.random_base32()

    # 2. зберігаємо в БД (ПОКИ НЕ ВМИКАЄМО 2FA)
    user.twofa_secret = secret
    db.commit()

    # 3. створюємо TOTP URI
    totp = pyotp.TOTP(secret)

    uri = totp.provisioning_uri(
        name=user.email,
        issuer_name="2read"
    )

    # 4. генеруємо QR
    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

def check_2fa_code(user: User, code: str) -> bool:
    if not user.twofa_secret:
        return False

    totp = pyotp.TOTP(user.twofa_secret)
    return totp.verify(code)
@router.post("/2fa/enable")
def enable_2fa(user_id: str, code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    # 1. перевірка чи існує user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. перевірка чи взагалі 2FA ініціалізована
    if not user.twofa_secret:
        raise HTTPException(status_code=400, detail="2FA not initialized")

    # 3. перевірка чи вже включена
    if user.twofa_enabled:
        return {
            "success": False,
            "message": "2FA already enabled"
        }

    # 4. перевірка коду
    if not check_2fa_code(user, code):
        raise HTTPException(status_code=400, detail="Invalid code")

    # 5. активуємо 2FA
    user.twofa_enabled = True
    db.commit()

    return {
        "success": True,
        "message": "2FA successfully enabled"
    }
