from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.api import deps

router = APIRouter()

from app import crud, models, schemas, reputation


@router.get("/", response_model=List[schemas.Reputation])
def read_reputations(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    reputations = reputation.get_reputations(db, skip=skip, limit=limit)
    return reputations


@router.get("/reputation/{user_id}", response_model=schemas.Reputation)
def get_reputation(user_id: int, db: Session = Depends(deps.get_db)):
    db_reputation = reputation.get_reputation_by_user(db, user_id=user_id)
    if db_reputation is None:
        raise HTTPException(status_code=404, detail="User's reputation not found")
    return db_reputation


@router.get("/reputation/{user_id}/all/", response_model=List[schemas.Reputation])
def get_reputations(user_id: int, db: Session = Depends(deps.get_db)):
    reputations = reputation.get_reputations_by_user(db, user_id=user_id)
    return reputations


@router.get("/reputation_/", response_model=str)
def compute_reputation(db: Session = Depends(deps.get_db)):
    reputations = crud.computation.compute_reputation(db)
    return reputations
