"""add main_role table

Revision ID: 08a541fa56e6
Revises: b29d070952a5
Create Date: 2025-01-31 15:59:31.373211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08a541fa56e6'
down_revision: Union[str, None] = 'b29d070952a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('main_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_code', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('main_role')
    # ### end Alembic commands ###
