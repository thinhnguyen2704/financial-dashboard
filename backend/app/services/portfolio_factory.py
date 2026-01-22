from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.backtest import Backtest


class VirtualPortfolioFactory:
    @staticmethod
    def for_live(db: Session, portfolio_id: int) -> Portfolio:
        portfolio = (
            db.query(Portfolio)
            .filter(Portfolio.id == portfolio_id)
            .with_for_update()
            .one()
        )
        return portfolio

    @staticmethod
    def for_backtest(
        *,
        user_id: int,
        name: str,
        initial_cash: float,
        base_currency: str = "USD",
    ) -> Portfolio:
        return Portfolio(
            id=None,
            user_id=user_id,
            name=f"[BT] {name}",
            base_currency=base_currency,
            cash=initial_cash,
            realized_pnl=0.0,
        )

    @staticmethod
    def for_replay(db: Session, backtest_id: int) -> Portfolio:
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).one()

        return Portfolio(
            id=None,
            user_id=backtest.user_id,
            name=f"[REPLAY] {backtest.name}",
            base_currency=backtest.base_currency,
            cash=backtest.initial_cash,
            realized_pnl=0.0,
        )
