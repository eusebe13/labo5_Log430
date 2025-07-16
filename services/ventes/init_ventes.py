from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Vente
import datetime

def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    db.query(Vente).delete()
    db.commit()

    ventes = [
        Vente(produit_id=1, quantite=2, prix_total=179.98, date_vente=datetime.datetime(2025, 7, 12)),
        Vente(produit_id=2, quantite=1, prix_total=59.90, date_vente=datetime.datetime(2025, 7, 13))
    ]

    db.add_all(ventes)
    db.commit()
    print("Ventes : données initialisées.")
    db.close()

if __name__ == "__main__":
    init_db()
