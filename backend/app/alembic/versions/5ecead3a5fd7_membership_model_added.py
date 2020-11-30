"""membership model added

Revision ID: 5ecead3a5fd7
Revises: 1bf04c9b67fd
Create Date: 2020-11-17 12:16:37.968093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ecead3a5fd7'
down_revision = '1bf04c9b67fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memberships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coop_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_memberships_coop_id'), 'memberships', ['coop_id'], unique=False)
    op.create_index(op.f('ix_memberships_id'), 'memberships', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_memberships_id'), table_name='memberships')
    op.drop_index(op.f('ix_memberships_coop_id'), table_name='memberships')
    op.drop_table('memberships')
    # ### end Alembic commands ###
