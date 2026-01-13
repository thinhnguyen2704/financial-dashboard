from sqlalchemy.orm import Session
from app.models.trade import Trade


def get_portfolio_symbols(
    db: Session,
    portfolio_id: int,
) -> list[str]:
    """
    Returns all distinct symbols traded by the portfolio.
    Used to register market-data dependencies.
    """
    rows = (
        db.query(Trade.symbol)
        .filter(Trade.portfolio_id == portfolio_id)
        .distinct()
        .all()
    )
    return [r[0] for r in rows]
