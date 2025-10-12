from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserBase, UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=List[UserOut])
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def sign_up(user_in: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    register_result = service.sign_up(user_in)

    if not register_result:
        raise HTTPException(status_code=409, detail="User already exists")

    return register_result


@router.post("/signin")
def sign_in(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    auth_result = service.sign_in(user_in)

    if not auth_result:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    token = auth_result["access_token"]
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {"message": "Login successful"}


@router.post("/signout")
def sign_out(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
