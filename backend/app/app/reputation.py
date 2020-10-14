from sqlalchemy.orm import Session

from . import models, crud
import datetime


def get_reputations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reputation).offset(skip).limit(limit).all()


def get_reputation_by_user(db: Session, user_id: int):
    return db.query(models.Reputation).filter(models.Reputation.user_id == user_id).order_by(models.Reputation.id.desc()).first()


def get_reputations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Reputation).filter(models.Reputation.user_id == user_id).offset(skip).limit(limit).all()


def score_commitment(commited_, delivered):
    if commited_ > delivered:
        score = round((1 - abs(round(((delivered - commited_) / commited_), 4))), 2)
        return score
    elif commited_ <= delivered:
        if commited_ == 0 and delivered == 0:
            score = 0.0
        else:
            score = 1.0
        return score


def get_commitment_score(db_session: Session):
    user_commitment = []
    users = db_session.query(models.Commitment.id, models.Commitment.deliverer).offset(0).limit(
        100).all()
    result = [list(elem) for elem in users]
    col = ['id', 'deliverer']
    result = [dict(zip(col, l)) for l in result]

    for user in result:
        id_ = user['deliverer']
        commitments = crud.commitment.get_commitment_by_deliverer(db_session, user['deliverer'])

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
        crud.create_reputation(db_session, data)