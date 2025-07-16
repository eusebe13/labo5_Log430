from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, RapportTendance
import datetime

def init_db():
    # Création des tables
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Vider la table existante
    db.query(RapportTendance).delete()
    db.commit()

    # Données fictives
    rapports = [
        RapportTendance(titre="RapportTendance Mensuel Juin", contenu="Ventes totales: 12000$", date=datetime.datetime(2025, 6, 30)),
        RapportTendance(titre="RapportTendance Hebdo 27", contenu="Stocks critiques: 5 articles", date=datetime.datetime(2025, 7, 7))
    ]

    db.add_all(rapports)
    db.commit()
    print("RapportTendances : données initialisées.")
    db.close()

if __name__ == "__main__":
    init_db()
