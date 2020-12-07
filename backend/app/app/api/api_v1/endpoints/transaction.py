import os
import requests
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

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


@router.post("/", response_model=schemas.Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.TransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new transaction.
    """

    if current_user:
        transaction = crud.commitment.get_commitment_by_plan_id(db=db, plan_id=item_in.plan_id)
        if not transaction:
            raise HTTPException(
                status_code=400,
                detail="Plan ID for this commitment does not exit",
            )
        transaction = crud.transaction.create(db=db, obj_in=item_in)
        return transaction


@router.get("/{plan_id}/", response_model=List[schemas.Transaction])
def read_transaction_by_plan_id(
        *,
        plan_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve production deliveries by plan id
    """
    if current_user:
        transaction = crud.transaction.get_transaction_by_plan_id(db, plan_id=plan_id)
        return transaction


@router.post("/delivery/updates", response_model=schemas.Msg)
def get_delivery_from_identity(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),

) -> Any:
    """
    Populate delivery data from identity
    """
    environ = os.environ.get("IDENTITY_DOMAIN_ENV")
    identity_delivery_endpoint = settings.get_env(env=environ) + 'delivery/?limit=10000'
    generate_token_url = settings.get_env(env=environ) + 'login/access-token'

    headers = {
        'Authorization': 'Bearer ' + settings.get_access_token(url=generate_token_url),
        'Content-Type': 'application/json; charset=utf-8'
    }
    res = requests.get(identity_delivery_endpoint, headers=headers)
    data = res.json()

    count = 0
    for member in data:
        delivery = crud.transaction.get_transaction_by_delivery_id(db=db, delivery_id=member["id"])
        if not delivery:
            delivery_in = schemas.TransactionCreate(
                plan_id=member['plan_id'],
                delivery_id=member['id'],
                delivery_value=member['quantity'] * member['px_kg'],
                delivery_date=member['delivery_date'],
            )
            member = crud.transaction.create(db, obj_in=delivery_in)
            count += 1

    return {"msg": "{} new records added to transactions table!".format(count)}
