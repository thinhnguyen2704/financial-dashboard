from decimal import Decimal
from datetime import datetime, timezone

import pytest

from app.domain.portfolio_engine import PortfolioEngine
from app.domain.models import PortfolioState, Trade
from app.domain.exceptions import InsufficientCash, InvalidTrade


def make_state(cash=Decimal("100000")):
    return PortfolioState(cash=cash, positions={})


def make_trade(
    symbol="AAPL",
    side="BUY",
    qty="10",
    price="100",
    fee="1",
    slippage="0",
):
    return Trade(
        symbol=symbol,
        side=side,
        quantity=Decimal(qty),
        price=Decimal(price),
        fee=Decimal(fee),
        slippage=Decimal(slippage),
        timestamp=datetime.now(timezone.utc),
    )


# -----------------------
# BASIC LONG FLOW
# -----------------------


def test_buy_creates_long_position():
    state = make_state()
    trade = make_trade(side="BUY")

    new_state = PortfolioEngine.apply_trade(state, trade)

    assert new_state.cash == Decimal("98999")  # 100000 - (100*10) - 1
    assert "AAPL" in new_state.positions
    assert new_state.positions["AAPL"].quantity == Decimal("10")
    assert new_state.positions["AAPL"].avg_price == Decimal("100")


def test_sell_closes_long_position():
    state = make_state()
    state = PortfolioEngine.apply_trade(state, make_trade(side="BUY"))

    sell = make_trade(side="SELL", qty="10", price="110", fee="1")
    state = PortfolioEngine.apply_trade(state, sell)

    assert state.cash == Decimal("100098")  # profit realized
    assert state.positions == {}


# -----------------------
# SHORT FLOW
# -----------------------


def test_sell_opens_short_position():
    state = make_state()
    trade = make_trade(side="SELL", qty="5", price="200", fee="2")

    state = PortfolioEngine.apply_trade(state, trade)

    assert state.cash == Decimal("100998")  # proceeds - fee
    assert state.positions["AAPL"].quantity == Decimal("-5")
    assert state.positions["AAPL"].avg_price == Decimal("200")


def test_buy_covers_short_position():
    state = make_state()
    state = PortfolioEngine.apply_trade(
        state, make_trade(side="SELL", qty="5", price="200", fee="2")
    )

    cover = make_trade(side="BUY", qty="5", price="180", fee="2")
    state = PortfolioEngine.apply_trade(state, cover)

    assert state.cash == Decimal("100096")  # short profit
    assert state.positions == {}


# -----------------------
# PARTIAL CLOSE
# -----------------------


def test_partial_sell_reduces_long_position():
    state = make_state()
    state = PortfolioEngine.apply_trade(state, make_trade(qty="10"))

    sell = make_trade(side="SELL", qty="4", price="120", fee="1")
    state = PortfolioEngine.apply_trade(state, sell)

    pos = state.positions["AAPL"]
    assert pos.quantity == Decimal("6")
    assert pos.avg_price == Decimal("100")  # unchanged


# -----------------------
# FEES & SLIPPAGE
# -----------------------


def test_fee_and_slippage_reduce_cash():
    state = make_state()
    trade = make_trade(qty="1", price="100", fee="5", slippage="3")

    state = PortfolioEngine.apply_trade(state, trade)

    assert state.cash == Decimal("99892")  # 100000 - 100 - 5 - 3


# -----------------------
# EQUITY
# -----------------------


def test_equity_calculation():
    state = make_state()
    state = PortfolioEngine.apply_trade(state, make_trade(qty="10", price="100"))

    prices = {"AAPL": Decimal("110")}
    equity = PortfolioEngine.calculate_equity(state, prices)

    assert equity == Decimal("100099")  # cash + unrealized PnL


# -----------------------
# VALIDATION
# -----------------------


def test_reject_zero_quantity():
    state = make_state()

    with pytest.raises(InvalidTrade):
        PortfolioEngine.apply_trade(state, make_trade(qty="0"))


def test_reject_insufficient_cash():
    state = make_state(cash=Decimal("100"))

    with pytest.raises(InsufficientCash):
        PortfolioEngine.apply_trade(state, make_trade(qty="2", price="100"))
