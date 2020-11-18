from typing import List, Any

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.core.config import settings
import requests

import os

router = APIRouter()


@router.post("/identity", response_model=schemas.Msg)
def get_membership_from_identity(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),

) -> Any:
    """
    Populate users from identity into reputation
    """
    environ = os.environ.get("IDENTITY_DOMAIN__ENV")
    identity_membership_endpoint = settings.get_env(env=environ) + 'membership/?limit=10000'
    generate_token_url = settings.get_env(env=environ) + 'login/access-token'

    headers = {
        'Authorization': 'Bearer ' + settings.get_access_token(url=generate_token_url),
        'Content-Type': 'application/json; charset=utf-8'
    }
    res = requests.get(identity_membership_endpoint, headers=headers)
    data = res.json()

    count = 0
    for user in data:
        membership = crud.membership.get_memberships(db=db, user_id=user["member_id"])
        if not membership:
            user_in = schemas.MembershipCreate(
                coop_id=user["coop_id"],
                user_id=user["member_id"]
            )
            user = crud.membership.create(db=db, obj_in=user_in)
            count += 1

    return {"msg": "{} new users added to the membership table!".format(count)}


@router.get("/", response_model=List[schemas.Membership])
def read_group_member_data(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve membership data.
    """
    membership = crud.membership.get_multi(db, skip=skip, limit=limit)
    return membership

