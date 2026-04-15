"""empty message

Revision ID: 963cdf6e77da
Revises: e1c8f5278ee8
Create Date: 2026-04-15 14:20:11.719303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '963cdf6e77da'
down_revision: Union[str, Sequence[str], None] = 'e1c8f5278ee8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
