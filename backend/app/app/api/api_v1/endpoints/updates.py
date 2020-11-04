from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from settings import url

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
    resp = requests.get(api,  
            auth = HTTPDigestAuth('dev@hivenetwork.online', 'b6e1b95b4014b48746eff931d16fb3d4a53279600c06605f8397d9962e0a6ad9'))

    return (resp.json)
