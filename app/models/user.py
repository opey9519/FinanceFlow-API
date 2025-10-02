from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    expenses = relationship(
        "Expense", back_populates="user", cascade="all, delete")
    categories = relationship(
        "Category", back_populates="user", cascade="all, delete")
