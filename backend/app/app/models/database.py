from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, DateTime, Text, Boolean
import datetime
from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)


class CommitmentCategory(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    weight = Column(Float)


class Commitment(Base):
    id = Column(Integer, primary_key=True, index=True)
    commitment_value = Column(Float)
    category_id = Column(Integer, ForeignKey(CommitmentCategory.id))
    description = Column(Text)
    delivery_date = Column(Date)
    deliverer = Column(Integer, ForeignKey(User.id))
    reporter = Column(Integer, ForeignKey(User.id))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    commitment_id = Column(Integer, ForeignKey(Commitment.id))
    delivery_value = Column(Float)
    delivery_date = Column(Date)
    deliverer = Column(Integer, ForeignKey(User.id))  # user id from identity service


class Reputation(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))  # user id from identity service
    reputation_score = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
