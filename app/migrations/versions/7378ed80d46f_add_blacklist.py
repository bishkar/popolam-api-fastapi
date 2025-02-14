"""add blacklist

Revision ID: 7378ed80d46f
Revises: 5acbac5028dd
Create Date: 2024-06-27 00:50:49.429640

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7378ed80d46f'
down_revision: Union[str, None] = '5acbac5028dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('on_blacklist', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'on_blacklist')
    # ### end Alembic commands ###
