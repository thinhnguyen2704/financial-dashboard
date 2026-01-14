from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.domain.models import PortfolioState, Position
from app.services.portfolio_registry import portfolio_runtimes
from app.services.portfolio_runtime import PortfolioRuntime

def get_or_create_runtime(
    db: Session,
    portfolio_id: int
) -> PortfolioRuntime:

    if portfolio_id in portfolio_runtimes:
        return portfolio_runtimes[portfolio_id]

    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .one()
    )

    positions = {
        p.symbol: Position(
            symbol=p.symbol,
            quantity=p.quantity,
            avg_price=p.avg_price,
        )
        for p in portfolio.positions
    }

    state = PortfolioState(
        cash=portfolio.cash,
        positions=positions,
        realized_pnl=portfolio.realized_pnl,
    )

    runtime = PortfolioRuntime(state)
    portfolio_runtimes[portfolio_id] = runtime
    return runtime
