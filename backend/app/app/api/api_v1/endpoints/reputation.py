from typing import List, Any

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Reputation])
def read_reputations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Read all reputation data
    """

    if current_user:
        reputations = crud.reputation.get_reputation(db, skip=skip, limit=limit)
    return reputations


@router.get("/reputation/user/{deliverer}", response_model=schemas.Reputation)
def get_reputation_by_user_id(
    deliverer: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Read current reputation score for a user
    """
    if current_user:
        db_reputation = crud.reputation.get_reputation_by_user(db, user_id=deliverer)
        if db_reputation is None:
            raise HTTPException(
                status_code=404,
                detail="No reputation found for user"
            )
        return db_reputation


@router.get("/reputation/history/{deliverer}", response_model=List[schemas.Reputation])
def get_reputation_history_by_user_id(
    deliverer: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve reputation history for user
    """
    if current_user:
        reputation = crud.reputation.get_reputations_by_user(db, user_id=deliverer)
        if reputation is None:
            raise HTTPException(
                status_code=404,
                detail="No reputation found for user"
            )
        return reputation


@router.post("/", response_model=schemas.Msg)
def compute_reputation(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Computation to populate reputation database
    """
    if current_user:
        reputation = crud.reputation.compute_reputation(db=db)
        return {"msg": "Reputation computed successfully"}

