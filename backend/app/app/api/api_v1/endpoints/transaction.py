import os
import requests
from typing import Any, List
import datetime
from dateutil import parser

from fastapi import APIRouter, Depends
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
        transaction = crud.transaction.create(db=db, obj_in=item_in, commitment_id=commitment_id)
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


@router.post("/delivery/updates", response_model=schemas.Msg)
def get_delivery_from_identity(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),

) -> Any:
    """
    Populate delivery data from identity
    """
    environ = os.environ.get("IDENTITY_DOMAIN__ENV")
    identity_delivery_endpoint = settings.get_env(env=environ) + 'delivery/?limit=10000'
    generate_token_url = settings.get_env(env=environ) + 'login/access-token'

    headers = {
        'Authorization': 'Bearer ' + settings.get_access_token(url=generate_token_url),
        'Content-Type': 'application/json; charset=utf-8'
    }
    res = requests.get(identity_delivery_endpoint, headers=headers)
    data = res.json()

    count = 0

    time_diff = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d%H:%M:%S.%f")
    print(time_diff)
    delivery_date = crud.transaction.get_max_tx_date(db=db)
    print(time_diff)
    if delivery_date is None:
        for member in data:
            # print(">>>>>>>>>>>>>>>>", member)

            delivery_in = schemas.TransactionCreate(
                plan_id=member['plan_id'],
                delivery_value=member['quantity'] * member['px_kg'],
                delivery_date=member['delivery_date'],
            )
            user = crud.transaction.create(db, obj_in=delivery_in)
            count += 1

    else:
        for member in data:
            print(member["created_at"])
            if time_diff > member["created_at"]:
                print(">>>>>>>>>>>>>>>>", member)

    # delivery_date[0] > datetime.datetime.now():
     #    print("TRUES")
     #    for member in data:
     #        delivery_in = schemas.TransactionCreate(
     #            plan_id=member['plan_id'],
     #            delivery_value=member['quantity'] * member['px_kg'],
     #            delivery_date=member['delivery_date'],
     #        )
     #        user = crud.transaction.create(db, obj_in=delivery_in)
     #        count += 1

    return {"msg": "{} new records added to transactions table!".format(count)}
