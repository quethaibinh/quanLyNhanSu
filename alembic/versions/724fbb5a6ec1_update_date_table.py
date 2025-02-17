from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '724fbb5a6ec1'
down_revision: Union[str, None] = '7aa09931af21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Xóa ràng buộc khóa ngoại trước khi xóa bảng 'dates'
    op.drop_constraint('users_birth_date_id_fkey', 'users', type_='foreignkey')

    # Tạo lại bảng 'date'
    op.create_table(
        'date',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('day', sa.Integer(), nullable=False),
        sa.Column('mon', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Xóa bảng 'dates' (vì bảng 'date' đã tồn tại, bạn có thể xóa bảng 'dates')
    op.drop_table('dates')

    # Tạo lại khóa ngoại từ bảng 'users' tới bảng 'date'
    op.create_foreign_key(
        None, 'users', 'date', ['birth_date_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    # Xóa khóa ngoại từ 'users' đến bảng 'date'
    op.drop_constraint(None, 'users', type_='foreignkey')

    # Tạo lại khóa ngoại từ bảng 'users' đến bảng 'dates' (nếu cần quay lại phiên bản trước)
    op.create_foreign_key(
        'users_birth_date_id_fkey', 'users', 'dates', ['birth_date_id'], ['id'], ondelete='CASCADE'
    )

    # Tạo lại bảng 'dates' nếu cần quay lại
    op.create_table(
        'dates',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('day', sa.INTEGER(), nullable=False),
        sa.Column('mon', sa.INTEGER(), nullable=False),
        sa.Column('year', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['users.id'], name='dates_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='dates_pkey')
    )

    # Xóa bảng 'date'
    op.drop_table('date')
