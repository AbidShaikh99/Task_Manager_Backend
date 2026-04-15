"""empty message

Revision ID: 72915f758e17
Revises: 963cdf6e77da
Create Date: 2026-04-15 14:21:06.047566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72915f758e17'
down_revision: Union[str, Sequence[str], None] = '963cdf6e77da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
