from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Shared properties
class GrpRepBase(BaseModel):
    coop_id: Optional[int] = None
    reputation_score: Optional[float] = None
    created_date: datetime = None


# Properties to receive on item creation
class GrpRepCreate(GrpRepBase):
    coop_id: int
    reputation_score: float


# Properties to receive on item update
class GrpRepUpdate(GrpRepBase):
    pass


# Properties shared by models stored in DB
class GrpRepInDBBase(GrpRepBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to return to client
class GrpRep(GrpRepInDBBase):
    pass


# Properties properties stored in DB
class GrpRepInDB(GrpRepInDBBase):
    pass
