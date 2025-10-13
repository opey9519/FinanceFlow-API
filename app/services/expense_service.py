from sqlalchemy.orm import Session
from app import models
from app.schemas.expense import ExpenseBase, ExpenseCreate, ExpenseOut, ExpenseUpdate

# Collection of services related to the Expense Routes


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db

    def create_expense(self, user_id: int, expense_in: ExpenseCreate):
        # Creates expense object from Expense model using user_id
        expense = models.Expense(description=expense_in.description,
                                 amount=expense_in.amount,
                                 category_id=expense_in.category_id,
                                 user_id=user_id)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_expense(self, expense_id):
        return self.db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    def list_expenses(self, user_id: int):
        return self.db.query(models.Expense).filter(models.Expense.user_id == user_id).all()

    def update_expense(self, expense_update: ExpenseUpdate, expense_id: int):
        expense = self.get_expense(expense_id)
        if not expense:
            return None

        for field, value in expense_update.dict(exclude_unset=True).items():
            setattr(expense, field, value)

        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete_expense(self, expense_id: int):
        expense = self.get_expense(expense_id)
        if expense:
            self.db.delete(expense)
            self.db.commit()

        return expense
