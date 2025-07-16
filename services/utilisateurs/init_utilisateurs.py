from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Utilisateur

def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    db.query(Utilisateur).delete()
    db.commit()

    utilisateurs = [
        Utilisateur(nom="Alice", email="alice@example.com", mot_de_passe="hashed123", role="employe"),
        Utilisateur(nom="Bob", email="bob@example.com", mot_de_passe="hashed456", role="gestionnaire"),
        Utilisateur(nom="Charlie", email="charlie@example.com", mot_de_passe="hashed789", role="responsable")
    ]

    db.add_all(utilisateurs)
    db.commit()
    print("Utilisateurs : données initialisées.")
    db.close()

if __name__ == "__main__":
    init_db()
