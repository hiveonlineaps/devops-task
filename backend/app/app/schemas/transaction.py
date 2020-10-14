from typing import Optional
from datetime import date

from pydantic import BaseModel


# Shared properties
class TransactionBase(BaseModel):
    deliverer: int
    commitment_id: int
    delivery_value: float
    delivery_date: date


# Properties to receive on item creation
class TransactionCreate(TransactionBase):
    deliverer: int
    commitment_id: int
    delivery_value: float
    delivery_date: date


# Properties to receive on item update
class TransactionUpdate(TransactionBase):
    deliverer: int
    commitment_id: int
    delivery_value: float
    delivery_date: date


# Properties shared by models stored in DB
class TransactionInDBBase(TransactionBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Transaction(TransactionInDBBase):
    pass


# Properties properties stored in DB
class TransactionInDB(TransactionInDBBase):
    pass
