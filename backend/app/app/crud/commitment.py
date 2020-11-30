from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.database import Commitment
from app.schemas.commitment import CommitmentCreate, CommitmentInDB, CommitmentUpdate


class CRUDItem(CRUDBase[Commitment, CommitmentInDB, CommitmentCreate]):
    def create(
            self, db: Session, *, obj_in: CommitmentCreate
    ) -> Commitment:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Commitment]:
        return (
            db.query(self.model)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_commitment_by_plan_id(self, db: Session, *, plan_id: int) -> Optional[Commitment]:
        return (
            db.query(self.model)
                .filter(Commitment.plan_id == plan_id)
                .first()
        )

    def get_commitment_by_deliverer(self, db: Session, *, deliverer: int) -> List[Commitment]:
        return (
            db.query(self.model)
                .filter(Commitment.deliverer == deliverer)
                .all()
        )


commitment = CRUDItem(Commitment)
