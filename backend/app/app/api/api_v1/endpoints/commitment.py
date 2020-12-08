from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
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
        category = crud.category.get_commitment_category_by_id(db=db, category_id=item_in.category_id)
        if category is None:
            raise HTTPException(
                status_code=404,
                detail="This commitment category ID does not exit"
            )
        deliverer = crud.user.get_by_identity_user_id(db=db, identity_user_id=item_in.deliverer)
        if not deliverer:
            raise HTTPException(
                status_code=404,
                detail="Deliverer with this identity user ID does not exit in the user table"
            )
        reporter = crud.user.get_by_identity_user_id(db=db, identity_user_id=item_in.reporter)
        if not reporter:
            raise HTTPException(
                status_code=404,
                detail="Reporter with this identity user ID does not exit in the user table"
            )

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


@router.get("/{plan_id}", response_model=schemas.Commitment)
def read_commitment_by_plan_id(
    plan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve commitment by plan id
    """
    if current_user:
        commitment = crud.commitment.get_commitment_by_plan_id(db=db, plan_id=plan_id)
        return commitment


@router.post("/estimate/updates", response_model=schemas.Msg)
def get_commitment_from_identity(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),

) -> Any:
    """
    Populate users from identity into reputation
    """
    environ = os.environ.get("IDENTITY_DOMAIN_ENV")
    identity_commitment_endpoint = settings.get_env(env=environ) + 'estimate/commitments/'
    generate_token_url = settings.get_env(env=environ) + 'login/access-token'

    headers = {
        'Authorization': 'Bearer ' + settings.get_access_token(url=generate_token_url),
        'Content-Type': 'application/json; charset=utf-8'
    }
    res = requests.get(identity_commitment_endpoint, headers=headers)
    data = res.json()

    count = 0

    for member in data:
        commitment = crud.commitment.get_commitment_by_plan_id(db=db, plan_id=member['plan_id'])
        if not commitment:
            commitment_in = schemas.CommitmentCreate(
                category_id=1,
                plan_id = member['plan_id'],
                commitment_value=member['quantity'] * member['price'],
                delivery_date=member['delivery_date'],
                deliverer=member['member_id'],
                reporter=member['creator_id'],
                description=""
            )
            member = crud.commitment.create(db, obj_in=commitment_in)
            count += 1

    return {"msg": "{} new records added to commitments table!".format(count)}