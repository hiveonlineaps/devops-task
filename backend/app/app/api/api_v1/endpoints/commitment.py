from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Commitment])
def read_commitments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve commitment data.
    """
    if current_user:
        commitment = crud.commitment.get_multi(db=db, skip=skip, limit=limit)
        return commitment


@router.post("/", response_model=schemas.Commitment)
def create_commitment(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.CommitmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new commitment.
    """

    if current_user:
        commitment = crud.commitment.create(db=db, obj_in=item_in)
        return commitment


@router.get("/{deliverer}", response_model=Optional[schemas.Commitment])
def read_commitment_by_deliverer(
    deliverer: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve commitment data per deliverer
    """
    if current_user:
        commitment = crud.commitment.get_commitment_by_deliverer(db=db, deliverer=deliverer)
        return commitment


@router.get("/reputation/test", response_model=List[schemas.Rep])
def read_commitment_by_deliverer(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),

) -> Any:
    """
    Retrieve commitment data per deliverer
    """

    reputation = crud.reputation.compute_reputation(db=db)
    return reputation
