from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut:
    id: int
    user_id: int

    class Config:
        orm_mode = True
