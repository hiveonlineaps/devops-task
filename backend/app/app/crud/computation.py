# from main import app
from sqlalchemy import func

from sqlalchemy.orm import Session
from . import models, crud
from reputation import Reputation

import numpy as np
import datetime


def score_commitment(committed, delivered):
    if committed > delivered:
        score = round((1 - np.abs(round(((delivered - committed) / committed), 4))), 2)
        return score
    elif committed <= delivered:
        if committed == 0 and delivered == 0:
            score = 0.0
        else:
            score = 1.0
        return score


def get_commitment_score(db_session: Session):
    user_commitment = []
    users = db_session.query(models.User.id, models.User.full_name, models.User.hiveonline_id).offset(0).limit(
        100).all()
    result = [list(elem) for elem in users]
    col = ['id', 'full_name', 'hiveonline_id']
    result = [dict(zip(col, l)) for l in result]
    for user in result:
        id_ = user['id']
        commitments = crud.get_commitments_by_user(db_session, user['id'])

        prod_val = 0
        loan_val = 0

        prod_del = 0
        loan_del = 0

        for commitment in list(commitments):

            if commitment.category_id == 1:
                prod_val += commitment.commitment_value
            if commitment.category_id == 2:
                loan_val += commitment.commitment_value

            weight = crud.get_commitment_category_by_id(db_session, commitment.category_id).weight
            transactions = crud.get_transactions_by_commitment(db_session, commitment.id)
            for transaction in list(transactions):

                if commitment.category_id == 1:
                    prod_del += transaction.delivery_value
                if commitment.category_id == 2:
                    loan_del += transaction.delivery_value

        prod_score = score_commitment(prod_val, prod_del)
        loan_score = score_commitment(loan_val, loan_del)

        print(id_, prod_score, loan_score)

        prod_score = prod_score * weight
        loan_score = loan_score * weight

        score = prod_score + loan_score
        score = score * 0.5

        user_commitment.append([id_, score])
    return user_commitment


def compute_reputation(db_session: Session):
    kyc_score = 0.5
    commitment_scores = get_commitment_score(db_session)
    for pair in commitment_scores:
        user = pair[0]
        c_score = pair[1]
        today = datetime.datetime.now().strftime("%x")
        data = {
            'user': user,
            'reputation_score': kyc_score + c_score,
            'created_date': datetime.datetime.now()
        }
        # print (data['user'])
        crud.create_reputation(db_session, data)


