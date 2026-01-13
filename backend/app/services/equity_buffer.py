from collections import deque

from app.models.equity import EquitySnapshot

MAX_POINTS = 300  # ~5 minutes @ 1s


class EquityBuffer:
    def __init__(self):
        self._buffers: dict[int, deque[EquitySnapshot]] = {}

    def append(self, portfolio_id: int, snapshot: EquitySnapshot):
        buf = self._buffers.setdefault(
            portfolio_id, deque(maxlen=MAX_POINTS)
        )
        buf.append(snapshot)

    def get_series(self, portfolio_id: int) -> list[EquitySnapshot]:
        return list(self._buffers.get(portfolio_id, []))


equity_buffer = EquityBuffer()
