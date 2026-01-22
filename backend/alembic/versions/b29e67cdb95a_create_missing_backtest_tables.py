"""create_missing_backtest_tables

Revision ID: b29e67cdb95a
Revises: 4f2b9f48be2a
Create Date: 2026-01-22 09:53:23.259268

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b29e67cdb95a"
down_revision: Union[str, Sequence[str], None] = "4f2b9f48be2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------- backtest_runs ----------
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "backtest_runs" not in inspector.get_table_names():
        op.create_table(
            "backtest_runs",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "backtest_id",
                sa.Integer(),
                sa.ForeignKey("backtests.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        )

    # ---------- backtest_trades ----------
    if "backtest_trades" not in inspector.get_table_names():
            op.create_table(
                "backtest_trades",
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column(
                    "backtest_id",
                    sa.Integer(),
                    sa.ForeignKey("backtests.id", ondelete="CASCADE"),
                    nullable=False,
                ),
                sa.Column("symbol", sa.String(), nullable=False),
                sa.Column("side", sa.String(), nullable=False),
                sa.Column("quantity", sa.Float(), nullable=False),
                sa.Column("price", sa.Float(), nullable=False),
                sa.Column("fee", sa.Float(), nullable=False),
                sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
            )

    # ---------- backtest_equity ----------
    if "backtest_equity" not in inspector.get_table_names():
        op.create_table(
            "backtest_equity",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "backtest_id",
                sa.Integer(),
                sa.ForeignKey("backtests.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
            sa.Column("equity", sa.Float(), nullable=False),
            sa.Column("cash", sa.Float(), nullable=False),
        )


def downgrade() -> None:
    op.drop_table("backtest_equity")
    op.drop_table("backtest_trades")
    op.drop_table("backtest_runs")
