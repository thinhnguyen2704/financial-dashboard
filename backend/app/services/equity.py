from decimal import Decimal
from app.market_data.cache import price_cache
# from app.domain.portfolio_engine import PortfolioEngine

def compute_equity_snapshot(state):
    positions = []

    unrealized = Decimal("0")

    for sym, pos in state.positions.items():
        market = price_cache.get(sym)
        if market is None:
            continue  # no price yet

        pnl = (market - pos.avg_price) * pos.quantity
        unrealized += pnl

        positions.append({
            "symbol": sym,
            "quantity": str(pos.quantity),
            "avg_price": str(pos.avg_price),
            "market_price": str(market),
            "unrealized_pnl": str(pnl),
        })

    equity = state.cash + unrealized

    return {
        "cash": str(state.cash),
        "equity": str(equity),
        "unrealized_pnl": str(unrealized),
        "positions": positions,
    }
