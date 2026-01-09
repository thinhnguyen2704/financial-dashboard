from decimal import Decimal
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.portfolio import Portfolio
from app.core.security import hash_password
from app.models.role import Role


def seed_users(db: Session):
    admin = db.query(User).filter(User.email == "admin@local.dev").first()
    if not admin:
        admin = User(
            email="admin@local.dev",
            hashed_password=hash_password("admin123"),
            role=Role.admin,

        )
        db.add(admin)

    user = db.query(User).filter(User.email == "user@local.dev").first()
    if not user:
        user = User(
            email="user@local.dev",
            hashed_password=hash_password("user123"),
            role=Role.user,
        )
        db.add(user)

    db.commit()
    return admin, user


def seed_portfolios(db: Session, user: User):
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user.id)
        .first()
    )

    if not portfolio:
        portfolio = Portfolio(
            name="Demo Portfolio",
            user_id=user.id,
            base_currency="USD",
            cash=Decimal("100000"),
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

    return portfolio


def main():
    db = SessionLocal()
    try:
        admin, user = seed_users(db)
        seed_portfolios(db, user)
        print("✅ Development database seeded successfully")
    finally:
        db.close()


if __name__ == "__main__":
    main()
