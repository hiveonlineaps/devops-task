from typing import Optional
from datetime import date
#import datetime

from pydantic import BaseModel


# Shared properties
class CommitmentBase(BaseModel):
    category_id: Optional[int] = None
    commitment_value: Optional[float] = None
    description: Optional[str] = None
    delivery_date: Optional[date] = None
    deliverer: Optional[int] = None
    reporter: Optional[int] = None


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
