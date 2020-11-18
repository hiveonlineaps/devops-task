from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.database import Memberships
from app.schemas.membership import MembershipCreate, MembershipUpdate


class CRUDUser(CRUDBase[Memberships, MembershipCreate, MembershipUpdate]):
    def create(self, db: Session, *, obj_in: MembershipCreate) -> Memberships:
        db_obj = Memberships(
            coop_id=obj_in.coop_id,
            user_id=obj_in.user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Memberships]:
        return (
            db.query(self.model)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_memberships(
            self, db: Session, *, user_id: int
    ) -> Optional[Memberships]:
        return (
            db.query(Memberships)
                .filter(Memberships.user_id == user_id)
                .all()
        )


membership = CRUDUser(Memberships)
