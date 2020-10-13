from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.database import CommitmentCategory
from app.schemas.commitmentcategory import CategoryCreate, Category, CategoryUpdate


class CRUDItem(CRUDBase[CategoryCreate, Category, CategoryUpdate]):
    def create(
            self, db: Session, *, obj_in: CategoryCreate
    ) -> CommitmentCategory:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[CommitmentCategory]:
        return (
            db.query(self.model)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_commitment_category_by_id(
            self, db: Session, category_id: int) -> CommitmentCategory:
        return (
            db.query(self.model)
            .filter(CommitmentCategory.id == category_id)
            .first()
        )


category = CRUDItem(CommitmentCategory)
