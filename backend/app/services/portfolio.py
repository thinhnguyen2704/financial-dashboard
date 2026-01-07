from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.portfolio import Portfolio
from app.models.user import User


def load_portfolio(
    db: Session,
    portfolio_id: int,
    user: User,
) -> Portfolio:
    """
    Load a portfolio with positions and enforce ownership.
    """

    portfolio = (
        db.query(Portfolio)
        .options(joinedload(Portfolio.positions))
        .filter(Portfolio.id == portfolio_id)
        .first()
    )

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    if portfolio.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    return portfolio
