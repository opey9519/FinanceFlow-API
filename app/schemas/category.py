from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
    user_id: int
