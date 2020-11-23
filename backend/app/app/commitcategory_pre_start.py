from app.db.session import db_session
from app.models.database import CommitmentCategory

types = ["Production", "Loan"]

# query category types already existent in the database
category = db_session.query(CommitmentCategory.name)

if category:
    pass
else:
    db_session.bulk_insert_mappings(CommitmentCategory,
                                    [dict(name="Production", weight="0.5"),
                                     dict(name="Loan", weight="0.5")])
