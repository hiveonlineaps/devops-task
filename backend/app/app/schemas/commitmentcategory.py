from typing import Optional

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    weight: float = None


# Properties to receive on item creation
class CategoryCreate(CategoryBase):
    name: str
    description: str
    weight: float


# Properties to receive on item update
class CategoryUpdate(CategoryBase):
    name: str
    description: str
    weight: float


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
