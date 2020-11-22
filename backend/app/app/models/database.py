from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, DateTime, Text, Boolean
import datetime
from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    identity_user_id = Column(Integer, index=True, unique=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean())
    is_superuser = Column(Boolean(), default=False)
    hiveonline_id = Column(String, unique=True, index=True)


class CommitmentCategory(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    weight = Column(Float)


class Memberships(Base):
    id = Column(Integer, primary_key=True, index=True)
    coop_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey(User.identity_user_id), index=True)


class Commitment(Base):
    id = Column(Integer, primary_key=True, index=True)
    commitment_value = Column(Float)
    category_id = Column(Integer, ForeignKey(CommitmentCategory.id))
    plan_id = Column(Integer, unique=True, index=True)
    description = Column(Text)
    delivery_date = Column(Date)
    deliverer = Column(Integer, ForeignKey(User.identity_user_id))
    reporter = Column(Integer, ForeignKey(User.identity_user_id))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey(Commitment.plan_id))
    commitment_id = Column(Integer, ForeignKey(Commitment.id))
    delivery_value = Column(Float)
    delivery_date = Column(Date)
    deliverer = Column(Integer, ForeignKey(User.identity_user_id))  # user id from identity service


class Reputation(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.identity_user_id))  # user id from identity service
    reputation_score = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
