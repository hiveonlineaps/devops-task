from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.database import Transaction, Commitment
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class CRUDItem(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_commitment_by_id(self, db: Session, *, commitment_id: int) -> Commitment:
        return (
            db.query(Commitment)
                .filter(Commitment.id == commitment_id)
                .first()
        )

    def create(self, db: Session, *, obj_in: TransactionCreate) -> Transaction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Transaction]:
        return (
            db.query(self.model)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_transaction_by_plan_id(self, db: Session, *, plan_id: int) -> List[Transaction]:
        return (
            db.query(self.model)
                .filter(Transaction.plan_id == plan_id)
                .all()
        )

    def get_transaction_by_delivery_id(self, db: Session, *, delivery_id: int) -> Optional[Transaction]:
        return (
            db.query(self.model)
                .filter(Transaction.delivery_id == delivery_id)
                .first()
        )

    def get_transactions_by_deliverer(self, db: Session, *, deliverer: int) -> List[Transaction]:
        return (
            db.query(self.model)
                .filter(Transaction.deliverer == deliverer)
                .all()
        )


transaction = CRUDItem(Transaction)
