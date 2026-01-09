import asyncio
from collections import defaultdict
from datetime import datetime

from app.services.equity import broadcast_equity
from app.api.routes.websocket import ws_manager
from app.db.session import SessionLocal

THROTTLE_INTERVAL = 1.0  # seconds


class EquityThrottle:
    def __init__(self):
        self._last_sent = defaultdict(lambda: datetime.min)
        self._pending_tasks: dict[int, asyncio.Task] = {}

    async def trigger(self, portfolio_id: int):
        now = datetime.utcnow()
        elapsed = (now - self._last_sent[portfolio_id]).total_seconds()

        if elapsed >= THROTTLE_INTERVAL:
            await self._send(portfolio_id)
        else:
            if portfolio_id not in self._pending_tasks:
                delay = THROTTLE_INTERVAL - elapsed
                self._pending_tasks[portfolio_id] = asyncio.create_task(
                    self._delayed_send(portfolio_id, delay)
                )

    async def _delayed_send(self, portfolio_id: int, delay: float):
        await asyncio.sleep(delay)
        await self._send(portfolio_id)
        self._pending_tasks.pop(portfolio_id, None)

    async def _send(self, portfolio_id: int):
        db = SessionLocal()
        try:
            await broadcast_equity(
                db=db,
                portfolio_id=portfolio_id,
                ws_manager=ws_manager,
            )
            self._last_sent[portfolio_id] = datetime.utcnow()
        finally:
            db.close()


equity_throttle = EquityThrottle()
