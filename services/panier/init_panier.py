from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Panier, ArticlePanier

def init_db():
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    # Session DB
    db: Session = SessionLocal()

    # Nettoyage des anciennes données
    db.query(ArticlePanier).delete()
    db.query(Panier).delete()
    db.commit()

    # Création de paniers fictifs
    paniers = [
        Panier(client_id=1, total=1000),
        Panier(client_id=2, total=500),
        Panier(client_id=3, total=10),
    ]
    db.add_all(paniers)
    db.commit()

    # Création d'articles dans les paniers
    articles = [
        ArticlePanier(panier_id=1, produit_id=1, quantite=2),
        ArticlePanier(panier_id=1, produit_id=2, quantite=1),
        ArticlePanier(panier_id=2, produit_id=3, quantite=1),
    ]
    db.add_all(articles)
    db.commit()

    print("Panier et ArticlesPanier : données initialisées.")
    db.close()

if __name__ == "__main__":
    init_db()
