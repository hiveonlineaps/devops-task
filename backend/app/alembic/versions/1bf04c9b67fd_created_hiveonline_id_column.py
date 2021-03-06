"""created_hiveonline_id column

Revision ID: 1bf04c9b67fd
Revises: 011b7cac841e
Create Date: 2020-11-09 15:53:00.194342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bf04c9b67fd'
down_revision = '011b7cac841e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hiveonline_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_user_hiveonline_id'), 'user', ['hiveonline_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_hiveonline_id'), table_name='user')
    op.drop_column('user', 'hiveonline_id')
    # ### end Alembic commands ###
