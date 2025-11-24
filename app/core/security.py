from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings

# Prefer Argon2 for hashing when available. If Argon2 is not installed,
# fall back to bcrypt. When Argon2 is available we avoid loading bcrypt
# to prevent issues with a broken/older bcrypt wheel.
try:
	import argon2  # type: ignore
	_schemes = ["argon2"]
except Exception:
	_schemes = ["bcrypt"]

pwd_context = CryptContext(schemes=_schemes, deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
	return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
	return encoded_jwt
