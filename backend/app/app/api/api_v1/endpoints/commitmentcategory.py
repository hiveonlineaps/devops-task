from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve commitment categories.
    """

    category = crud.category.get_multi(db, skip=skip, limit=limit)

    return category


@router.post("/", response_model=schemas.Category)
def create_commitment_category(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new commitment category
    """
    category = crud.category.create(db, obj_in=item_in)
    return category


