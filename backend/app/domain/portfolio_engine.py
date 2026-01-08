from decimal import Decimal, getcontext
from app.domain.models import Trade, Position, PortfolioState
from app.domain.exceptions import InsufficientCash, InvalidTrade

getcontext().prec = 28


class PortfolioEngine:

    @staticmethod
    def apply_trade(state: PortfolioState, trade: Trade) -> PortfolioState:
        if trade.quantity <= 0:
            raise InvalidTrade("Quantity must be positive")

        side_mult = Decimal("1") if trade.side == "BUY" else Decimal("-1")
        signed_qty = trade.quantity * side_mult

        trade_value = trade.price * trade.quantity
        cash_delta = -(trade_value * side_mult) - trade.fee - trade.slippage

        if state.cash + cash_delta < Decimal("0"):
            raise InsufficientCash("Not enough cash for trade")

        new_cash = state.cash + cash_delta
        new_positions = dict(state.positions)
        realized_pnl = state.realized_pnl

        pos = new_positions.get(trade.symbol)

        # --------------------------------------------------
        # NO EXISTING POSITION
        # --------------------------------------------------
        if pos is None:
            new_positions[trade.symbol] = Position(
                symbol=trade.symbol,
                quantity=signed_qty,
                avg_price=trade.price,
            )

        else:
            new_qty = pos.quantity + signed_qty

            # --------------------------------------------------
            # REALIZED PNL (ONLY WHEN REDUCING / CLOSING)
            # --------------------------------------------------

            # SELL closing LONG
            if trade.side == "SELL" and pos.quantity > 0:
                closed_qty = min(pos.quantity, trade.quantity)
                realized_pnl += (trade.price - pos.avg_price) * closed_qty

            # BUY closing SHORT
            elif trade.side == "BUY" and pos.quantity < 0:
                closed_qty = min(abs(pos.quantity), trade.quantity)
                realized_pnl += (pos.avg_price - trade.price) * closed_qty

            # --------------------------------------------------
            # POSITION UPDATE LOGIC
            # --------------------------------------------------

            # Same direction → increase
            if pos.quantity * signed_qty > 0:
                total_cost = pos.avg_price * abs(pos.quantity) + trade.price * abs(
                    signed_qty
                )
                avg_price = total_cost / abs(new_qty)
                new_positions[trade.symbol] = Position(
                    symbol=trade.symbol,
                    quantity=new_qty,
                    avg_price=avg_price,
                )

            # Partial close → avg price unchanged
            elif abs(signed_qty) < abs(pos.quantity):
                new_positions[trade.symbol] = Position(
                    symbol=trade.symbol,
                    quantity=new_qty,
                    avg_price=pos.avg_price,
                )

            # Full close
            elif new_qty == 0:
                del new_positions[trade.symbol]

            # Flip direction → new avg price
            else:
                new_positions[trade.symbol] = Position(
                    symbol=trade.symbol,
                    quantity=new_qty,
                    avg_price=trade.price,
                )

        return PortfolioState(
            cash=new_cash,
            positions=new_positions,
            realized_pnl=realized_pnl,
        )

    @staticmethod
    def calculate_equity(state: PortfolioState, prices: dict[str, Decimal]) -> Decimal:
        equity = state.cash
        for pos in state.positions.values():
            equity += pos.quantity * prices[pos.symbol]
        return equity
