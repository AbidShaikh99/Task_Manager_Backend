from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db.database import get_db
from app.db import models

# ========================
# CONFIG
# ========================
SECRET_KEY = "secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# ========================
# CUSTOM EXCEPTION
# ========================
class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


# ========================
# PASSWORD FUNCTIONS
# ========================
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ========================
# TOKEN
# ========================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ========================
# AUTH FUNCTIONS
# ========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise CustomException("Invalid token", 401)

    except JWTError:
        raise CustomException("Invalid token", 401)

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise CustomException("User not found", 401)

    return user


def get_current_manager(current_user = Depends(get_current_user)):
    if current_user.role != "manager":
        raise CustomException("Only managers can perform this action", 403)
    return current_user


def get_current_developer(current_user = Depends(get_current_user)):
    if current_user.role != "developer":
        raise CustomException("Only developers can perform this action", 403)
    return current_user


# ========================
# OPTIONAL: DIRECT RESPONSE HELPER
# ========================
def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": False,
            "message": message
        }
    )