from typing import List, Optional
from itertools import groupby
from operator import itemgetter
from pprint import pprint
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.database import Reputation, User, Commitment, Transaction, CommitmentCategory
from app.schemas.reputation import ReputationCreate, ReputationInDB, ReputationUpdate



def create(
        self, db: Session, *, obj_in: ReputationCreate
) -> ReputationCreate:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_reputation_by_deliverer(self, db: Session, *, deliverer: int) -> List[Reputation]:
    return (
        db.query(self.model)
            .filter(Reputation.deliverer == deliverer)
            .all()
    )

def score_commitment(committed, delivered):
    if committed > int(0 if delivered is None else delivered):
        score = round((1 - abs(round(((int(0 if delivered is None else delivered) - committed) / committed), 4))), 2)
        return score
    elif committed <= int(0 if delivered is None else delivered):
        if committed == 0 and delivered == 0:
            score = 0.0
        else:
            score = 1.0
        return score

def get_category_weight(db: Session, category_id) -> CommitmentCategory:
    return db.query(CommitmentCategory.weight).\
        filter(CommitmentCategory.id == category_id).\
        first()

def get_user_commitment_ids(db: Session) -> List[Commitment]:
    return db.query(Commitment.deliverer, Commitment.category_id).all()

def compute_reputation(db: Session):
    results = db.query(Commitment.deliverer, Commitment.category_id, Commitment.commitment_value,
                       func.sum(Transaction.delivery_value)).join(Transaction, Commitment.deliverer == Transaction.deliverer, isouter= True).\
                       group_by(Commitment.category_id, Commitment.deliverer, Commitment.commitment_value).all()

    cols = ['deliverer', 'category_id', 'commitment_value', 'delivery_value']
    results = [dict(zip(cols, l)) for l in results]

    print(results)

    #ids = get_user_commitment_ids(db=db) # get user ids from commitment table
    #ids = list(set([i[0] for i in ids])) # convert list of tuples to list
    # print(ids)
    #
    # keys = ("deliverer", "category_id")
    # ids = [dict(zip(keys, values)) for values in ids]
    #
    # bar = {
    #     k: [d.get(k) for d in ids]
    #     for k in set().union(*ids)
    # }
    #
    # pprint(bar)


    for result in results:

        result['score'] = score_commitment(result['commitment_value'], result['delivery_value']) * get_category_weight(db=db,
                      category_id=result['category_id'])[0] # returned as a tuple



    # grouper = itemgetter("deliverer", "score")
    # result = []
    # for key, grp in groupby(sorted(results, key=grouper), grouper):
    #     temp_dict = dict(zip(["deliverer", "score"], key))
    #     temp_dict["score"] = sum(item["score"] for item in grp)
    #     result.append(temp_dict)

    #pprint(results)





