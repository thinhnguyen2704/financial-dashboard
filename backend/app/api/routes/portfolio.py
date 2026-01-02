from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.portfolio import Portfolio

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("/")
def create_portfolio(
    name: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    portfolio = Portfolio(name=name, owner_id=user.id)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.get("/")
def list_portfolios(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.query(Portfolio).filter(Portfolio.owner_id == user.id).all()
