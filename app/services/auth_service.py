from app.utils import PasswordManager, JWTManager
from sqlalchemy.orm import Session
from app import models, schemas


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id):
        user = self.db.query(models.User).filter(
            models.User.id == user_id).first()
        return user

    def sign_up(self, user_create: schemas.UserCreate):
        username = user_create.username
        email = user_create.email
        password = PasswordManager.hash_password(user_create.password)

        user = models.User(username=username, email=email,
                           hashed_password=password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def sign_in(self, user_in: schemas.UserLogin):
        email = user_in.email

        user = self.db.query(models.User).filter(
            models.User.email == email).first()
        if not user or not PasswordManager.verify_password(user_in.password, user.hashed_password):
            return None

        token = JWTManager.create_access_token(data={"sub": user.email})

        return {"access_token": token, "token_type": "bearer"}
