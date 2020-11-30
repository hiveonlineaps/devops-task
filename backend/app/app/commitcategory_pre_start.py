from app.db.session import db_session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from app.models.database import CommitmentCategory


def load_data():
    # query category types already existent in the database
    category = db_session.query(CommitmentCategory.name).first()

    if category is None:
        production = CommitmentCategory(id=1, name="Production", description="", weight="0.5")
        loan = CommitmentCategory(id=2, name="Loan", description="", weight="0.5")
        db_session.add_all([production, loan])
        db_session.commit()
    else:
        pass


def main() -> None:
    load_data()
    logger.info("Commitment categories loaded")


if __name__ == "__main__":
    main()
