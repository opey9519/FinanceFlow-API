from passlib.hash import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import settings
# Password Manager object to hash + salt passwords & verify passwords


class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)


# Environment Variables
# CHANGE THESE FROM EMPTY/NULL
SECRET_KEY = settings.JWT_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# JSON Web Token Manager to encode & decode JWT tokens


class JWTManager:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
