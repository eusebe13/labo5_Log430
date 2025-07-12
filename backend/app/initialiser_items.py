import random

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    Magasin,
    Product,
    ProduitParMagasin,
    RoleEnum,
    StockCentral,
    Utilisateur,
)


def init_data():
    session: Session = SessionLocal()

    if session.query(Magasin).count() > 0:
        print(" Données déjà présentes. Ignoré.")
        session.close()
        return

    # MAISON MÈRE
    maison_mere = Magasin(nom="Magasin Central", region="QC", is_maison_mere=True)
    session.add(maison_mere)
    session.commit()

    # 2 MAGASINS SECONDAIRES
    magasin1 = Magasin(nom="Magasin Laval", region="QC", maison_mere_id=maison_mere.id)
    magasin2 = Magasin(nom="Magasin Montréal", region="QC", maison_mere_id=maison_mere.id)
    session.add_all([magasin1, magasin2])
    session.commit()

    # UTILISATEURS
    users = [
        Utilisateur(nom="Alice", role=RoleEnum.gestionnaire, mot_de_passe="admin", magasin_id=magasin1.id),
        Utilisateur(nom="Bob", role=RoleEnum.employe, mot_de_passe="1234", magasin_id=magasin1.id),
        Utilisateur(nom="Charlie", role=RoleEnum.responsable, mot_de_passe="root", magasin_id=maison_mere.id)
    ]
    session.add_all(users)

    # 20 PRODUITS
    categories = ["Fruit", "legumes", "electronique", "vetements", "meubles", "jouets", "livres", "beauté", "sport", "alimentation", "laitier"]
    produits = []
    for i in range(1, 21):
        p = Product(
            name=f"Produit {i}",
            category=random.choice(categories),
            price=round(random.uniform(5, 100), 2),
            stock=0  # On gère le stock dans StockCentral et ProduitParMagasin
        )
        produits.append(p)
    session.add_all(produits)
    session.commit()

    # STOCK CENTRAL
    stocks_centrals = []
    for produit in produits:
        stock = StockCentral(produit_id=produit.id, quantite=random.randint(30, 100))
        stocks_centrals.append(stock)
    session.add_all(stocks_centrals)

    # STOCKS EN MAGASINS
    stocks_magasin = []
    for produit in produits:
        stocks_magasin.append(ProduitParMagasin(
            produit_id=produit.id,
            magasin_id=magasin1.id,
            quantite=random.randint(0, 20)
        ))
        stocks_magasin.append(ProduitParMagasin(
            produit_id=produit.id,
            magasin_id=magasin2.id,
            quantite=random.randint(0, 20)
        ))
    session.add_all(stocks_magasin)

    session.commit()
    session.close()
    print(" Données initiales insérées.")
