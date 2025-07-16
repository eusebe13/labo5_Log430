from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Produit

def init_db():
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    # Ouvrir une session
    db: Session = SessionLocal()

    # Supprimer les anciens produits (optionnel)
    db.query(Produit).delete()
    db.commit()

    # Produits à insérer
    # Produits à insérer
    produits = [
        Produit(name="Clavier mécanique", category="Périphérique", price=89.99, stock=15),
        Produit(name="Souris gaming", category="Périphérique", price=59.90, stock=30),
        Produit(name="Écran 27 pouces", category="Affichage", price=249.99, stock=10),
        Produit(name="Casque audio", category="Audio", price=129.50, stock=20)
    ]

    # Insertion
    db.add_all(produits)
    db.commit()

    print("Produits : données initialisées.")
    db.close()

if __name__ == "__main__":
    init_db()
