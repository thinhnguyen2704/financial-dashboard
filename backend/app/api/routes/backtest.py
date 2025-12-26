from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def run_backtest():
    return {"status": "Backtest executed"}
