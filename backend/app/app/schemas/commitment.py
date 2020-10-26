from typing import Optional
from datetime import date
#import datetime

from pydantic import BaseModel


# Shared properties
class CommitmentBase(BaseModel):
    category_id: int = None
    commitment_value: float = None
    description: Optional[str] = None
    delivery_date: date = None
    deliverer: int = None
    reporter: int = None


# Properties to receive on item creation
class CommitmentCreate(CommitmentBase):
    category_id: int
    commitment_value: float
    description: str
    delivery_date: date
    deliverer: int
    reporter: int


# Properties to receive on item update
class CommitmentUpdate(CommitmentBase):
    commitment_value: float
    category_id: int
    delivery_date: date


# Properties shared by models stored in DB
class CommitmentInDBBase(CommitmentBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Commitment(CommitmentInDBBase):
    pass


# Properties properties stored in DB
class CommitmentInDB(CommitmentInDBBase):
    pass
