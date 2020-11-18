from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
import requests
import os

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


@router.get("/user/{deliverer}", response_model=List[schemas.Commitment])
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


@router.get("/{commitment_id}", response_model=schemas.Commitment)
def read_commitment_by_id(
    commitment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve commitment by id
    """
    if current_user:
        commitment = crud.transaction.get_commitment_by_id(db=db, commitment_id=commitment_id)
        return commitment


@router.post("/identity/updates", response_model=schemas.Msg)
def get_commitment_from_identity(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),

) -> Any:
    """
    Populate users from identity into reputation
    """
    environ = os.environ.get("IDENTITY_DOMAIN__ENV")
    identity_commitment_endpoint = settings.get_env(env=environ) + 'users/?limit=10000'
    generate_token_url = settings.get_env(env=environ) + 'login/access-token'

    headers = {
        'Authorization': 'Bearer ' + settings.get_access_token(url=generate_token_url),
        'Content-Type': 'application/json; charset=utf-8'
    }
    res = requests.get(identity_commitment_endpoint, headers=headers)
    data = res.json()

    count = 0
    for user in data:
        user_ = crud.user.get_emails(db=db, email=user["email"])
        if not user_:
            user_in = schemas.UserCreate(
                email=user["email"],
                full_name=user["full_name"],
                identity_user_id=user["id"],
                password="",
                hiveonline_id=user["hiveonline_id"],
                is_superuser=False,
                is_active=False
            )
            user = crud.user.create(db, obj_in=user_in)
            count += 1

    return {"msg": "{} new users added to users table!".format(count)}