from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.utils.auth import JWTManager
from app.models.user import User
from fastapi import HTTPException, status
from app.db import SessionLocal


def get_db():
    """
    Provides a database session for FastAPI routes.
    Ensures the session is closed after the request finishes.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")

    token = token.replace("Bearer ", "")
    try:
        payload = JWTManager.decode_access_token(token)
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
