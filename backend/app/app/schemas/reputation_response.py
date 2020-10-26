from pydantic import BaseModel


# Shared properties
class RepBase(BaseModel):
    deliverer: int = None
    category_id: int = None
    commitment_value: float = None
    delivery_value: float = None
    score: float = None


# Properties to receive on item creation
class RepCreate(RepBase):
    pass


# Properties to receive on item update
class RepUpdate(RepBase):
    pass


# Properties to return to client
class Rep(RepBase):
    pass


# Properties properties stored in DB
class RepInDB(RepBase):
    pass
