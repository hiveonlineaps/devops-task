from typing import Optional

from pydantic import BaseModel


# Shared properties
class MembershipBase(BaseModel):
    coop_id: Optional[int] = None
    user_id: Optional[int] = None


# Properties to receive on item creation
class MembershipCreate(MembershipBase):
    coop_id: int
    user_id: int


# Properties to receive on item update
class MembershipUpdate(MembershipBase):
    pass


# Properties shared by models stored in DB
class MembershipInDBBase(MembershipBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Membership(MembershipInDBBase):
    pass


# Properties properties stored in DB
class MembershipInDB(MembershipInDBBase):
    pass