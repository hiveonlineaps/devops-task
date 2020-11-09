from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.api.api_v1.endpoints.settings import (session, headers, url)

import os 

import requests

from requests.auth import HTTPBasicAuth, HTTPDigestAuth

router = APIRouter()

token = "Bearer "+os.environ.get("BEARER_TOKEN", "Some Token")

## Get Users
@router.get("/users", response_model=schemas.Msg)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users from Identity and Write to the Reputation Db.
    """
    api = url+'users/?skip='+str(skip)+'&limit='+str(limit)
    print (api)
    resp = session.get(
                        api,  
                        headers = {"Authorization": token}
                    )
    count = 0
    for user in resp.json():
        user_ = crud.user.get_by_email(db, email=user["email"])
        if not user_:
            user_in = schemas.UserCreate(
                email=user["email"],
                full_name=user["full_name"],
                password="",
                hiveonline_id=user["hiveonline_id"],
                is_superuser=False,
                is_active=False
            )
            user = crud.user.create(db, obj_in=user_in)
            count += 1
    
    return {"msg": "{} new users added to users table!".format(count)}
