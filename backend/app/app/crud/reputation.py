from typing import List, Optional
from itertools import groupby
from operator import itemgetter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
import collections
import datetime

from app.models.database import Reputation, User, Commitment, Transaction, CommitmentCategory
from app.schemas.reputation import ReputationCreate, ReputationInDB, ReputationUpdate


def get_reputation(db: Session, skip: int = 0, limit: int = 100) ->List[Reputation]:
    return db.query(Reputation).offset(skip).limit(limit).all()


def get_reputation_by_user(db: Session, user_id: int):
    return db.query(Reputation).filter(Reputation.user_id == user_id).order_by(Reputation.id.desc()).first()


def get_reputations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Reputation).filter(Reputation.user_id == user_id).offset(skip).limit(limit).all()


def create(
     db: Session, *, obj_in: ReputationCreate
) -> Reputation:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Reputation(**obj_in_data)
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
    results = db.query(Transaction.commitment_id, Commitment.deliverer, Commitment.category_id, Commitment.commitment_value,
                       func.sum(Transaction.delivery_value)).join(Transaction, Commitment.deliverer == Transaction.deliverer, isouter=True).\
                       group_by(Transaction.commitment_id, Commitment.category_id, Commitment.deliverer, Commitment.commitment_value).all()

    cols = ['commitment_id','deliverer', 'category_id', 'commitment_value', 'delivery_value']
    results = [dict(zip(cols, l)) for l in results]

    for result in results:
        # score commitments
        result['score'] = score_commitment(result['commitment_value'], result['delivery_value'])

    grouper = itemgetter("deliverer", "category_id")
    result = []

    # get an average score per user per category
    for key, grp in groupby(sorted(results, key=grouper), grouper):
        temp_dict = dict(zip(["deliverer", "category_id"], key))
        temp_list = [item["score"] for item in grp]
        temp_dict["score"] = sum(temp_list) / len(temp_list)
        result.append(temp_dict)

    counters = []
    for d in result:
        # determine which users have both (loan or production plan)
        counters.append(d['deliverer'])
    freq = dict(collections.Counter(counters))

    both = [] # have both loan and production plans
    single = [] # have either of the plans

    for k,v in freq.items():
        if v > 1:
            both.append(k)
        else:
            single.append(k)

    keys_to_remove = ['category_id', 'score'] # not needed for the final output

    counter = collections.Counter()

    for i in result:
        if i['deliverer'] in both:
            # multiply the score with weight
            i['final_score'] = i['score'] * get_category_weight(db=db, category_id=i['category_id'])[0] # returned as a tuple
        else:
            i['final_score'] = i['score']
        for k in keys_to_remove:
            try:
                del i[k]
            except KeyError:
                pass

        # sum up the final score
        counter[i['deliverer']] += i['final_score']

    finaldict = dict(counter)
    for key, value in finaldict.items():
        data = {
            'user_id': key,
            'reputation_score': value,
            'created_date':datetime.datetime.now()

        }
        create(db=db, obj_in=data)








