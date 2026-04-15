"""empty message

Revision ID: 320026521d4e
Revises: 54888cad0b2d
Create Date: 2026-04-14 19:13:05.856404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '320026521d4e'
down_revision: Union[str, Sequence[str], None] = '54888cad0b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
