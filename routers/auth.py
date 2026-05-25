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
from fido2.webauthn import (
    AuthenticatorAssertionResponse,
    PublicKeyCredentialRequestOptions
)
from fido2.server import Fido2Server
from fido2.webauthn import AttestationObject
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
    user = db.query(User).filter(User.email == request.email).first()

    if user is None or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    # 🔐 якщо є 2FA або passkey
    if user.twofa_enabled:
        return {
            "success": True,
            "need_2fa": True,
            "methods": ["totp", "passkey"],
            "userId": str(user.id)
        }

    return {
        "success": True,
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
@router.post("/2fa/disable")
def disable_2fa(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.twofa_enabled = False
    user.twofa_secret = None

    db.commit()

    return {
        "success": True,
        "message": "2FA disabled"
    }
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity

rp = PublicKeyCredentialRpEntity(id="localhost", name="2read")
fido2_server = Fido2Server(rp)

active_challenges = {}
@router.post("/passkey/register/begin")
def passkey_register_begin(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user_identity = {
        "id": user.id.encode(),
        "name": user.email,
        "display_name": user.username
    }

    data, state = fido2_server.register_begin(
        user_identity,
        credentials=[]
    )

    active_challenges[f"reg:{user_id}"] = state

    return data
@router.post("/passkey/register/finish")
def passkey_register_finish(
    user_id: str,
    client_data: dict,
    attestation_object: dict,
    db: Session = Depends(get_db)
):
    state = active_challenges.get(f"reg:{user_id}")
    if not state:
        raise HTTPException(400, "Challenge expired")

    auth_data = fido2_server.register_complete(
        state,
        client_data,
        attestation_object
    )

    # ⚠️ ВАЖЛИВО: тут потрібна твоя SQL модель
    credential = PasskeyCredential(
        id=str(uuid.uuid4()),
        user_id=user_id,
        credential_id=auth_data.credential_data.credential_id.hex(),
        public_key=auth_data.credential_data.public_key,
        sign_count=auth_data.credential_data.sign_count
    )

    db.add(credential)
    db.commit()

    del active_challenges[f"reg:{user_id}"]

    return {"success": True}
@router.post("/passkey/login/begin")
def passkey_login_begin(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")

    creds = db.query(PasskeyCredential).filter(
        PasskeyCredential.user_id == user.id
    ).all()

    allow_credentials = [
        {"id": c.credential_id}
        for c in creds
    ]

    data, state = fido2_server.authenticate_begin(allow_credentials)

    active_challenges[f"auth:{user.id}"] = state

    return {
        "userId": user.id,
        "options": data
    }

@router.post("/passkey/login/finish")
def passkey_login_finish(
    user_id: str,
    credential_id: str,
    client_data: dict,
    authenticator_data: dict,
    signature: str,
    db: Session = Depends(get_db)
):
    cred = db.query(PasskeyCredential).filter(
        PasskeyCredential.credential_id == credential_id
    ).first()

    if not cred:
        raise HTTPException(400, "Unknown credential")

    state = active_challenges.get(f"auth:{user_id}")
    if not state:
        raise HTTPException(400, "Challenge expired")
