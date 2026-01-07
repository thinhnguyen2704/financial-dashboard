from fastapi import APIRouter, Depends
from pydantic import BaseModel
import numpy as np

from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/risk", tags=["Risk"])


class RiskRequest(BaseModel):
    equity_curve: list[float]


class RiskResponse(BaseModel):
    sharpe: float
    max_drawdown: float


def calculate_sharpe(equity: list[float]) -> float:
    returns = np.diff(equity) / equity[:-1]
    if returns.std() == 0:
        return 0.0
    return float((returns.mean() / returns.std()) * np.sqrt(252))


def calculate_max_drawdown(equity: list[float]) -> float:
    curve = np.array(equity)
    peak = np.maximum.accumulate(curve)
    drawdown = (curve - peak) / peak
    return float(drawdown.min())


@router.post("/metrics", response_model=RiskResponse)
def risk_metrics(
    data: RiskRequest,
    user: User = Depends(get_current_user),
):
    sharpe = calculate_sharpe(data.equity_curve)
    max_dd = calculate_max_drawdown(data.equity_curve)

    return {
        "sharpe": sharpe,
        "max_drawdown": max_dd,
    }
