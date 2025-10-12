from pydantic import BaseModel, ConfigDict
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
