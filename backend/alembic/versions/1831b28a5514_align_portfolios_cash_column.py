"""align portfolios cash column

Revision ID: 1831b28a5514
Revises: 2c279c9ecea7
Create Date: 2026-01-09 10:41:34.200558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1831b28a5514'
down_revision: Union[str, Sequence[str], None] = '2c279c9ecea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
