from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve transaction data.
    """
    if current_user:
        transaction = crud.transaction.get_multi(db=db, skip=skip, limit=limit)
        return transaction


@router.post("/{commitment_id}", response_model=schemas.Transaction)
def create_transaction(
    *,
    commitment_id: int,
    db: Session = Depends(deps.get_db),
    item_in: schemas.TransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new transaction.
    """

    if current_user:
        transaction = crud.transaction.create(db=db, obj_in=item_in, commitment_id = commitment_id)
        return transaction


@router.get("/{commitment_id}/", response_model=schemas.Transaction)
def read_commitment_by_commitment_id(
    *,
    commitment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Transaction data per commitment ID
    """
    if current_user:
        transaction = crud.transaction.get_transaction_by_commitment_id(db, commitment_id=commitment_id)
        return transaction


@router.get("/commitment/{deliverer}/", response_model=List[schemas.Transaction])
def read_commitment_by_deliverer(
    *,
    deliverer: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Transaction data per deliverer
    """
    if current_user:
        transaction = crud.transaction.get_transactions_by_deliverer(db, deliverer=deliverer)
        return transaction

