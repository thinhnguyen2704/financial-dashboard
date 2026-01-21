"""add_portfolio_base_currency

Revision ID: be4af642ade0
Revises: 705b179a08a5
Create Date: 2026-01-21 11:02:59.883191

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "be4af642ade0"
down_revision: Union[str, Sequence[str], None] = "705b179a08a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "portfolios",
        sa.Column(
            "base_currency",
            sa.String(length=3),
            nullable=False,
            server_default="USD",
        ),
    )
    op.alter_column("portfolios", "base_currency", server_default=None)


def downgrade() -> None:
    op.drop_column("portfolios", "base_currency")
