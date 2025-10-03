from pydantic import BaseModel
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True  # Allows Pydantic to read SQLAlchemy objects
