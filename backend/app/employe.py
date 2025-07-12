import json
from typing import Dict, List

import redis
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse

from app.database import SessionLocal
from app.models import Magasin, Product, ProduitParMagasin, Reaprovisionnement, Vente

router = APIRouter()
r = redis.Redis(host="redis", port=6379)

# Utilitaire pour mettre et récupérer du cache
def get_cache(key: str):
    cached = r.get(key)
    return json.loads(cached) if cached else None

def set_cache(key: str, data, expire: int = 60):
    r.set(key, json.dumps(data), ex=expire)

def invalidate_cache(keys: List[str]):
    for key in keys:
        r.delete(key)


@router.get("/produits", status_code=status.HTTP_200_OK)
def consulter_product():
    cache = get_cache("produits")
    if cache:
        return cache

    session = SessionLocal()
    produits = session.query(Product).all()
    result = [{"id": p.id, "name": p.name, "category": p.category, "price": p.price} for p in produits]
    session.close()
    set_cache("produits", result)
    return result


@router.get("/magasin/{magasin_id}/produits", status_code=status.HTTP_200_OK)
def consulter_produit_par_magasin(magasin_id: int):
    cache_key = f"magasin:{magasin_id}:produits"
    cache = get_cache(cache_key)
    if cache:
        return cache

    session = SessionLocal()
    try:
        produits = session.query(ProduitParMagasin).filter_by(magasin_id=magasin_id).all()
        if not produits:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Aucun produit trouvé pour ce magasin."}
            )
        result = [{"produit": p.produit.name, "quantite": p.quantite} for p in produits]
        set_cache(cache_key, result)
        return result
    finally:
        session.close()


@router.get("/stock/{produit_id}/magasin/{magasin_id}", status_code=status.HTTP_200_OK)
def verifier_stock(produit_id: int, magasin_id: int):
    cache_key = f"stock:{produit_id}:{magasin_id}"
    cache = get_cache(cache_key)
    if cache:
        return cache

    session = SessionLocal()
    try:
        stock = session.query(ProduitParMagasin).filter_by(
            produit_id=produit_id, magasin_id=magasin_id
        ).first()
        produit = session.query(Product).get(produit_id)
        magasin = session.query(Magasin).get(magasin_id)

        if not produit or not magasin:
            raise HTTPException(status_code=404, detail="Produit ou magasin introuvable.")

        if not stock:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": f"{produit.name} ({magasin.nom}) : stock non disponible."}
            )

        result = {
            "produit": produit.name,
            "magasin": magasin.nom,
            "quantite": stock.quantite
        }
        set_cache(cache_key, result)
        return result
    finally:
        session.close()


@router.get("/stockcentral/produits", status_code=status.HTTP_200_OK)
def consulter_stock_central_complet():
    cache = get_cache("stockcentral")
    if cache:
        return cache

    session = SessionLocal()
    try:
        produits = session.query(Product).all()
        result = [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "stock_central": p.stock_central.quantite if p.stock_central else 0
            } for p in produits
        ]
        set_cache("stockcentral", result)
        return result
    finally:
        session.close()


@router.post("/acheter/{magasin_id}", status_code=status.HTTP_200_OK)
def acheter_produit(magasin_id: int, liste_produit: List[Dict] = Body(...)):
    session = SessionLocal()
    try:
        messages = []
        for item in liste_produit:
            produit_id = item.get("produit_id")
            quantite = item.get("quantite", 0)

            stock = session.query(ProduitParMagasin).filter_by(
                produit_id=produit_id, magasin_id=magasin_id
            ).first()
            produit = session.query(Product).get(produit_id)

            if not produit or not stock:
                messages.append(f"Produit ID {produit_id} indisponible.")
                continue

            if stock.quantite < quantite:
                messages.append(f"{produit.name} : stock insuffisant ({stock.quantite} dispo).")
                continue

            stock.quantite -= quantite
            session.add(Vente(
                produit_id=produit_id,
                magasin_id=magasin_id,
                quantite=quantite,
                prix_total=produit.price * quantite
            ))
            messages.append(f"{produit.name} : achat de {quantite} unités confirmé.")

            # Invalider les caches concernés
            invalidate_cache([
                f"stock:{produit_id}:{magasin_id}",
                f"magasin:{magasin_id}:produits",
                "produits",
                "stockcentral"
            ])

        session.commit()
        return {"resultats": messages}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'achat : {str(e)}"
        )
    finally:
        session.close()


@router.post("/reapprovisionner/produit/{produit_id}/quantite/{quantite}/magasin/{magasin_id}", status_code=status.HTTP_201_CREATED)
def demander_reapprovisionnement(produit_id: int, quantite: int, magasin_id: int):
    session = SessionLocal()
    try:
        produit = session.query(Product).get(produit_id)
        magasin = session.query(Magasin).get(magasin_id)

        if not produit or not magasin:
            raise HTTPException(status_code=404, detail="Produit ou magasin introuvable.")

        demande_existante = session.query(Reaprovisionnement).filter_by(
            produit_id=produit_id, magasin_id=magasin_id, approuved=False
        ).first()

        if demande_existante:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": f"Une demande de réapprovisionnement pour {produit.name} existe déjà."}
            )

        session.add(Reaprovisionnement(
            produit_id=produit_id,
            magasin_id=magasin_id,
            quantite=quantite,
            approuved=False
        ))
        session.commit()

        # Invalider les caches pertinents
        invalidate_cache([
            f"stock:{produit_id}:{magasin_id}",
            f"magasin:{magasin_id}:produits",
            "stockcentral"
        ])

        return {
            "message": f"Demande de réapprovisionnement pour {produit.name} envoyée."
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la demande : {str(e)}"
        )
    finally:
        session.close()
