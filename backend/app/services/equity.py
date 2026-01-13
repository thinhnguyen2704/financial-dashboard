from decimal import Decimal
from app.market_data.cache import price_cache
from app.domain.portfolio_engine import PortfolioEngine
from app.domain.models import PortfolioState
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.services.portfolio_state import rebuild_portfolio_state
from app.api.websockets.manager import TradeWebSocketManager
from app.services.equity_buffer import equity_buffer
from app.models.equity import EquitySnapshot


def build_equity_snapshot(
    state: PortfolioState,
    prices: dict[str, Decimal],
) -> dict:
    equity = PortfolioEngine.calculate_equity(state, prices)

    unrealized = Decimal("0")
    for pos in state.positions.values():
        unrealized += (prices[pos.symbol] - pos.avg_price) * pos.quantity

    return {
        "type": "equity_update",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "equity": str(equity),
        "cash": str(state.cash),
        "realized_pnl": str(state.realized_pnl),
        "unrealized_pnl": str(unrealized),
    }


async def broadcast_equity(
    *, db: Session, portfolio_id: int, ws_manager: TradeWebSocketManager
):
    """
    Rebuild portfolio state from DB, compute equity, and broadcast to clients.
    Must be called AFTER trade commit.
    """
    state = rebuild_portfolio_state(db, portfolio_id)
    snapshot = build_equity_snapshot(state)

    equity_buffer.append(
        portfolio_id,
        EquitySnapshot(
            timestamp=datetime.now(timezone.utc),
            equity=snapshot["equity"],
            cash=snapshot["cash"],
            unrealized_pnl=snapshot["unreal1ized_pnl"],
            realized_pnl=snapshot["realized_pnl"],
        ),
    )

    await ws_manager.broadcast(portfolio_id, snapshot)


def compute_equity_snapshot(state):
    positions = []

    unrealized = Decimal("0")

    for sym, pos in state.positions.items():
        market = price_cache.get(sym)
        if market is None:
            continue  # no price yet

        pnl = (market - pos.avg_price) * pos.quantity
        unrealized += pnl

        positions.append(
            {
                "symbol": sym,
                "quantity": str(pos.quantity),
                "avg_price": str(pos.avg_price),
                "market_price": str(market),
                "unrealized_pnl": str(pnl),
            }
        )

    equity = state.cash + unrealized

    return {
        "cash": str(state.cash),
        "equity": str(equity),
        "realized_pnl": str(state.realized_pnl),
        "unrealized_pnl": str(unrealized),
        "positions": positions,
    }
