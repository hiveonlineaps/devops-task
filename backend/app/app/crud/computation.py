from sqlalchemy.orm import Session
from app.models.database import User, Commitment, CommitmentCategory, Transaction, Reputation
from app.schemas.reputation import ReputationCreate
from fastapi.encoders import jsonable_encoder

from typing import List


def get_commitment_by_deliverer(db: Session, *, deliverer: int) -> List[Commitment]:
    return (
        db.query(Commitment)
            .filter(Commitment.deliverer == deliverer)
            .all())


def get_commitment_category_by_id(db: Session, * category_id: int) -> CommitmentCategory:
    return (db.query(CommitmentCategory)
            .filter(CommitmentCategory.id == category_id)
            .first())

def get_transaction_by_commitment_id(db: Session, *, commitment_id: int) -> List[Transaction]:
    return (
        db.query(Transaction)
            .filter(Transaction.commitment_id == commitment_id)
            .all())

def create_reputation(db: Session, *, obj_in:ReputationCreate) -> Reputation:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Reputation(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def score_commitment(committed, delivered):
    if committed > delivered:
        score = round((1 - abs(round(((delivered - committed) / committed), 4))), 2)
        return score
    elif committed <= delivered:
        if committed == 0 and delivered == 0:
            score = 0.0
        else:
            score = 1.0
        return score


def get_commitment_score(db_session: Session):
    user_commitment = []
    users = db_session.query(User.id, User.full_name, User.email).all()
    result = [list(elem) for elem in users]
    col = ['id', 'full_name', 'email']
    result = [dict(zip(col, l)) for l in result]
    for user in result:
        id_ = user['id']
        commitments = get_commitment_by_deliverer(db = db_session, deliverer=user['id'])

        prod_val = 0
        loan_val = 0

        prod_del = 0
        loan_del = 0

        for commitment in list(commitments):

            if commitment.category_id == 1:
                prod_val += commitment.commitment_value
            if commitment.category_id == 2:
                loan_val += commitment.commitment_value

            weight = get_commitment_category_by_id(db_session, commitment.category_id).weight #both weights are 0.5

            transactions = get_transaction_by_commitment_id(db = db_session, commitment_id=commitment.id)
            for transaction in list(transactions):

                if commitment.category_id == 1:
                    prod_del += transaction.delivery_value
                if commitment.category_id == 2:
                    loan_del += transaction.delivery_value

        print("**************", prod_val, prod_val)

        prod_score = score_commitment(prod_val, prod_del)
        loan_score = score_commitment(loan_val, loan_del)



        #print(id_, prod_score)

        prod_score = prod_score * weight
        loan_score = loan_score * weight

        score = prod_score + loan_score
        #score = score * 0.5

        #print("SCORE -------", score)

        user_commitment.append([id_, score])
    return user_commitment


def compute_reputation(db_session: Session):
    kyc_score = 0.5
    commitment_scores = get_commitment_score(db_session)
    for pair in commitment_scores:
        pass
        # user = pair[0]
        # c_score = pair[1]
        # data = {
        #     'user_id': user,
        #     'reputation_score': kyc_score + c_score,
        #     'created_date': datetime.datetime.now()
        # }
        # create_reputation(db = db_session, obj_in = data)