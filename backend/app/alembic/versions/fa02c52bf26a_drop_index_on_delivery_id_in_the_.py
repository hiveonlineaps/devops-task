"""drop index on delivery_id in the transaction model

Revision ID: fa02c52bf26a
Revises: 7902afe95fc3
Create Date: 2020-12-07 09:08:03.923155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa02c52bf26a'
down_revision = '7902afe95fc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_transaction_delivery_id', table_name='transaction')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_transaction_delivery_id', 'transaction', ['delivery_id'], unique=False)
    # ### end Alembic commands ###
