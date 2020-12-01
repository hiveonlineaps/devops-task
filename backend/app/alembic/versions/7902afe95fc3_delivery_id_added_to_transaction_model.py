"""delivery_id added to transaction model


Revision ID: 7902afe95fc3
Revises: 1d5a2984dc46
Create Date: 2020-11-30 20:14:13.929351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7902afe95fc3'
down_revision = '1d5a2984dc46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('delivery_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_transaction_delivery_id'), 'transaction', ['delivery_id'], unique=False)
    op.create_index(op.f('ix_transaction_plan_id'), 'transaction', ['plan_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_plan_id'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_delivery_id'), table_name='transaction')
    op.drop_column('transaction', 'delivery_id')
    # ### end Alembic commands ###