from typing import List
from itertools import groupby
from operator import itemgetter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
import collections
import datetime
from app import schemas
from pprint import pprint

from app.models.database import Reputation, User, Commitment, Transaction, CommitmentCategory, Memberships
from app.schemas.reputation import ReputationCreate, ReputationInDB, ReputationUpdate
from app.schemas.group_reputation import GrpRepCreate


def get_reputation(db: Session, skip: int = 0, limit: int = 100) -> List[Reputation]:
    return db.query(Reputation).offset(skip).limit(limit).all()


def get_reputation_by_user(db: Session, user_id: int):
    return db.query(Reputation).filter(Reputation.user_id == user_id).order_by(Reputation.id.desc()).first()

# def calculate_group_reputation(db: Session):


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


def create_group_reputation(
        db: Session, *, obj_in: GrpRepCreate
) -> Reputation:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Reputation(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_group_reputation_score(db: Session):
    result = db.query(func.max(Reputation.user_id), Memberships.coop_id, Reputation.reputation_score). \
        filter(Reputation.user_id == Memberships.user_id).group_by(Memberships.coop_id,
                                                                   Reputation.reputation_score).all()
    cols = ['user_id', 'coop_id', 'reputation_score']
    results = [dict(zip(cols, l)) for l in result]

    counter = collections.Counter()

    count = 0
    for record in results:
        counter[record['coop_id']] += record['reputation_score']

        finaldict = dict(counter)

        for key, value in finaldict.items():
            record_in = schemas.GrpRepCreate(
                coop_id=key,
                reputation_score=value,
                created_at=datetime.datetime.now()
            )
            create_group_reputation(db=db, obj_in=record_in)
            count += 1

    return {"msg": "{} new member records added to reputation table!".format(count)}


def get_group_reputation_score_by_id(db: Session, coop_id: int):
    result = db.query(func.max(Reputation.user_id), Memberships.coop_id, Reputation.reputation_score). \
        filter(Reputation.user_id == Memberships.user_id).filter(Memberships.coop_id == coop_id).group_by \
        (Memberships.coop_id, Reputation.reputation_score).all()
    cols = ['user_id', 'coop_id', 'reputation_score']
    results = [dict(zip(cols, l)) for l in result]
    return results


def get_reputation_by_deliverer(self, db: Session, *, deliverer: int) -> List[Reputation]:
    return (
        db.query(self.model)
            .filter(Reputation.deliverer == deliverer)
            .all()
    )


def score_commitment(committed, delivered):
    if committed > int(0 if delivered is None else delivered):
        score = round((1 - abs(round(((int(0 if delivered is None else delivered) - committed) / committed), 4))), 4)
        return score
    elif committed <= int(0 if delivered is None else delivered):
        if committed == 0 and delivered == 0:
            score = 0.0
        else:
            score = 1.0
        return score


def get_category_weight(db: Session, category_id) -> CommitmentCategory:
    return db.query(CommitmentCategory.weight). \
        filter(CommitmentCategory.id == category_id). \
        first()


def get_user_commitment_ids(db: Session) -> List[Commitment]:
    return db.query(Commitment.deliverer, Commitment.category_id).all()


def compute_reputation(db: Session):
    results = db.query(Transaction.plan_id, Commitment.deliverer, Commitment.category_id,
                       Commitment.commitment_value, func.sum(Transaction.delivery_value)). \
        join(Transaction, Commitment.plan_id == Transaction.plan_id, isouter=True). \
        group_by(Transaction.plan_id, Commitment.category_id, Commitment.deliverer,
                 Commitment.commitment_value).all()

    cols = ['plan_id', 'deliverer', 'category_id', 'commitment_value', 'delivery_value']

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

    both = []  # have both loan and production plans
    single = []  # have either of the plans

    for k, v in freq.items():
        if v > 1:
            both.append(k)
        else:
            single.append(k)

    keys_to_remove = ['category_id', 'score']  # not needed for the final output

    counter = collections.Counter()

    for i in result:
        if i['deliverer'] in both:
            # multiply the score with weight
            i['final_score'] = i['score'] * get_category_weight(db=db, category_id=i['category_id'])[
                0]  # returned as a tuple
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
            'created_date': datetime.datetime.now()

        }
        #create(db=db, obj_in=data)

# def compute_group_reputation(db: Session):
