from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import expense as schemas
from app.services.expense_service import ExpenseService
from app.deps import get_db
from app.deps import get_current_user

# Router blueprint for expenses
router = APIRouter(prefix="/expense", tags=["expenses"])

# -------------------------------
# Create Expense
# -------------------------------


@router.post("/", response_model=schemas.ExpenseOut)
def create_expense(expense_in: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = ExpenseService(db)
    return service.create_expense(expense_in, user_id=current_user["id"])

# -------------------------------
# List All Expenses (for user)
# -------------------------------


@router.get("/", response_model=List[schemas.ExpenseOut])
def list_expenses(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = ExpenseService(db)
    return service.list_expenses(user_id=current_user["id"])

# -------------------------------
# Get Single Expense by ID
# -------------------------------


@router.get("/{expense_id}", response_model=schemas.ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = ExpenseService(db)
    expense = service.get_expense(expense_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this expense")

    return expense

# -------------------------------
# Update Expense
# -------------------------------


@router.put("/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(expense_id: int, expense_update: schemas.ExpenseUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = ExpenseService(db)
    expense = service.update_expense(expense_update, expense_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this expense")

    return expense

# -------------------------------
# Delete Expense
# -------------------------------


@router.delete("/{expense_id}", response_model=schemas.ExpenseOut)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = ExpenseService(db)
    expense = service.get_expense(expense_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this expense")

    return service.delete_expense(expense_id)
