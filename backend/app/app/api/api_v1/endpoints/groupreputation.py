from typing import List, Any

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.GrpRep])
def read_group_reputations(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Read all group reputation data
    """

    if current_user:
        group_reputation = crud.reputation.get_group_reputation_score(db=db)
    return group_reputation


@router.get("/{coop_id}", response_model=List[schemas.GrpRep])
def get_reputation_by_coop_id(
    coop_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Read member reputation scores within a cooperative
    """
    if current_user:
        group_reputation = crud.reputation.get_group_reputation_score_by_id(db=db, coop_id=coop_id)
        # if group_reputation is None:
        #     raise HTTPException(
        #         status_code=404,
        #         detail="No reputation scores found for this coop_id"
        #     )
        return group_reputation
