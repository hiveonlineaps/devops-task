from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ReputationBase(BaseModel):
    user_id: Optional[int] = None
    #full_name: Optional[str] = None
    reputation_score: Optional[float] = None
    created_date:  Optional[datetime] = None


# Properties to receive on item creation
class ReputationCreate(ReputationBase):
    user_id: int
    #full_name: str
    reputation_score: float


# Properties to receive on item update
class ReputationUpdate(ReputationBase):
    pass


# Properties shared by models stored in DB
class ReputationInDBBase(ReputationBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Reputation(ReputationInDBBase):
    pass


# Properties properties stored in DB
class ReputationInDB(ReputationInDBBase):
    pass
