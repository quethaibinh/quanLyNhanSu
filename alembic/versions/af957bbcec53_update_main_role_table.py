"""update main_role table

Revision ID: af957bbcec53
Revises: 08a541fa56e6
Create Date: 2025-01-31 16:14:08.204915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af957bbcec53'
down_revision: Union[str, None] = '08a541fa56e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('main_role_id_fkey', 'main_role', type_='foreignkey')
    op.add_column('users', sa.Column('role_account_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'main_role', ['role_account_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_account_id')
    op.create_foreign_key('main_role_id_fkey', 'main_role', 'users', ['id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
