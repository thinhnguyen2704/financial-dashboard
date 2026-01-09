"""align portfolios cash column

Revision ID: 705b179a08a5
Revises: 1831b28a5514
Create Date: 2026-01-09 10:41:38.743917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '705b179a08a5'
down_revision: Union[str, Sequence[str], None] = '1831b28a5514'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
