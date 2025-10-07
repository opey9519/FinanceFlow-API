from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, category, expense

app = FastAPI(
    title="FinanceFlow API",
    description="Backend API for Expense Tracker",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(expense.router)


@app.get('/')
def root():
    return {"message": "Expense Tracker API running!"}
