from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, StockCentral

def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    db.query(StockCentral).delete()
    db.commit()

    stocks = [
        StockCentral(produit_id=1, quantite=20),
        StockCentral(produit_id=2, quantite=35),
        StockCentral(produit_id=3, quantite=15),
        StockCentral(produit_id=4, quantite=40)
    ]

    db.add_all(stocks)
    db.commit()
    print("StockCentral : données initialisées.")
    db.close()

if __name__ == "__main__":
    init_db()
