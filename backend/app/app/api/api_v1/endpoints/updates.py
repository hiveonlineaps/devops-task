from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from settings import (session, headers, url, auth, token)

import requests

from requests.auth import HTTPBasicAuth, HTTPDigestAuth

## Get Users
@router.get("/users", response_model=schemas.msg)
def read_users(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users from Identity.
    """
    api = url+'/api/v1/users/?skip='+skip+'&limit='+limit
    resp = session.get(
                        api,  
                        auth = HTTPDigestAuth(auth["user"], auth["password"]), 
                        headers = {"Authorization": token}
                    )

    return (resp.json())
