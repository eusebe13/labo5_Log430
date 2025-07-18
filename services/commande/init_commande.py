# init_commande.py
from database import engine, SessionLocal
from models import Base, Commande, LigneCommande
from sqlalchemy.orm import Session


def init_db():
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        commandes = [
            {
                "client_id": 1,
                "statut": "en_cours",
                "lignes": [
                    {"produit_id": 101, "quantite": 2, "prix_unitaire": 10.99},
                    {"produit_id": 102, "quantite": 1, "prix_unitaire": 5.49}
                ]
            },
            {
                "client_id": 2,
                "statut": "livree",
                "lignes": [
                    {"produit_id": 103, "quantite": 3, "prix_unitaire": 7.25}
                ]
            }
        ]

        for c in commandes:
            commande = Commande(
                client_id=c["client_id"],
                statut=c["statut"],
                total=sum(ligne["quantite"] * ligne["prix_unitaire"] for ligne in c["lignes"])  # auto-calcule total
            )
            db.add(commande)
            db.flush()  # pour commande.id

            for ligne in c["lignes"]:
                ligne_commande = LigneCommande(
                    commande_id=commande.id,
                    produit_id=ligne["produit_id"],
                    quantite=ligne["quantite"],
                    prix_unitaire=ligne["prix_unitaire"]
                )
                db.add(ligne_commande)

        db.commit()
        print("Données commandes initialisées.")
    except Exception as e:
        db.rollback()
        print("Erreur lors de l'initialisation des commandes :", e)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
