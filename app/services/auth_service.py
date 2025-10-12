from app.utils.auth import PasswordManager, JWTManager
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserBase, UserCreate, UserLogin, UserOut


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id):
        user = self.db.query(User).filter(
            User.id == user_id).first()
        return user

    def sign_up(self, user_create: UserCreate):
        user = self.db.query(User).filter(
            User.email == user_create.email).first()
        if user:
            return None

        username = user_create.username
        email = user_create.email
        password = PasswordManager.hash_password(user_create.password)

        user = User(username=username, email=email,
                    hashed_password=password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def sign_in(self, user_in: UserLogin):
        email = user_in.email

        user = self.db.query(User).filter(
            User.email == email).first()
        if not user or not PasswordManager.verify_password(user_in.password, user.hashed_password):
            return None

        token = JWTManager.create_access_token(data={"sub": user.email})

        return {"access_token": token, "token_type": "bearer"}
