import json

import redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    AlerteRupture,
    Product,
    ProduitParMagasin,
    Reaprovisionnement,
    StockCentral,
)
from app.schemas import UpdateChampProduit

router = APIRouter()
r = redis.Redis(host="redis", port=6379)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cache(key: str):
    val = r.get(key)
    return json.loads(val) if val else None

def set_cache(key: str, data, expire: int = 60):
    r.set(key, json.dumps(data), ex=expire)

def invalidate_cache(keys):
    for key in keys:
        r.delete(key)

@router.get("/stock", status_code=status.HTTP_200_OK)
def consulter_stock(db: Session = Depends(get_db)):
    cache_key = "responsable:stock"
    cache = get_cache(cache_key)
    if cache:
        return cache

    try:
        produits = db.query(Product).all()
        result = [
            {
                "id": p.id,
                "name": p.name,
                "stock_central": p.stock_central.quantite if p.stock_central else 0
            } for p in produits
        ]
        set_cache(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

@router.put("/produits/{produit_id}", status_code=status.HTTP_200_OK)
def mettre_a_jour_produit(produit_id: int, data: UpdateChampProduit, db: Session = Depends(get_db)):
    produit = db.query(Product).get(produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    if not hasattr(produit, data.champ):
        raise HTTPException(status_code=400, detail=f"Champ {data.champ} invalide")

    setattr(produit, data.champ, data.valeur)

    for stock in produit.produit_par_magasin:
        setattr(stock.produit, data.champ, data.valeur)

    db.commit()
    db.refresh(produit)

    # Invalider le cache produit
    invalidate_cache(["responsable:stock"])

    return {"message": f"Produit {produit.name} mis à jour : {data.champ} = {data.valeur}"}

@router.get("/reapprovisionnements", status_code=status.HTTP_200_OK)
def get_demandes_reapprovisionnement(db: Session = Depends(get_db)):
    cache_key = "responsable:reapprovisionnements"
    cache = get_cache(cache_key)
    if cache:
        return cache

    demandes = db.query(Reaprovisionnement).all()
    result = [
        {
            "id": d.id,
            "produit": d.produit.name,
            "magasin": d.magasin.nom,
            "quantite": d.quantite,
            "approuved": d.approuved
        } for d in demandes
    ]
    set_cache(cache_key, result)
    return result

@router.post("/reapprovisionner/{reappro_id}/approuver", status_code=status.HTTP_200_OK)
def approuver_reapprovisionnement(reappro_id: int, db: Session = Depends(get_db)):
    demande = db.query(Reaprovisionnement).get(reappro_id)
    if not demande:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    if demande.approuved:
        return {"message": "Demande déjà approuvée."}

    stock_central = db.query(StockCentral).filter_by(produit_id=demande.produit_id).first()
    if not stock_central or stock_central.quantite < demande.quantite:
        raise HTTPException(
            status_code=400,
            detail=f"Stock central insuffisant. Disponible : {stock_central.quantite if stock_central else 0}"
        )

    stock_magasin = db.query(ProduitParMagasin).filter_by(
        produit_id=demande.produit_id,
        magasin_id=demande.magasin_id
    ).first()

    stock_central.quantite -= demande.quantite
    if stock_magasin:
        stock_magasin.quantite += demande.quantite
    else:
        nouveau_stock = ProduitParMagasin(
            produit_id=demande.produit_id,
            magasin_id=demande.magasin_id,
            quantite=demande.quantite
        )
        db.add(nouveau_stock)

    demande.approuved = True
    db.commit()

    # Invalider les caches concernés
    invalidate_cache([
        "responsable:stock",
        "responsable:reapprovisionnements"
    ])

    return {
        "message": f"{demande.quantite} unités de {demande.produit.name} transférées à {demande.magasin.nom}"
    }

@router.post("/reapprovisionner/{reappro_id}/refuser", status_code=status.HTTP_200_OK)
def refuser_reapprovisionnement(reappro_id: int, db: Session = Depends(get_db)):
    demande = db.query(Reaprovisionnement).get(reappro_id)
    if not demande:
        raise HTTPException(status_code=404, detail="Demande non trouvée")

    if demande.approuved:
        raise HTTPException(status_code=400, detail="Impossible de refuser une demande déjà approuvée.")

    demande.approuved = False
    db.commit()

    # Invalider cache
    invalidate_cache(["responsable:reapprovisionnements"])

    return {"message": "Demande de réapprovisionnement refusée."}

@router.delete("/reapprovisionner/{reappro_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_reapprovisionnement(reappro_id: int, db: Session = Depends(get_db)):
    demande = db.query(Reaprovisionnement).get(reappro_id)
    if not demande:
        raise HTTPException(status_code=404, detail="Demande non trouvée")

    db.delete(demande)
    db.commit()

    # Invalider cache
    invalidate_cache(["responsable:reapprovisionnements"])

    return

@router.get("/magasin/{magasin_id}/produits", status_code=status.HTTP_200_OK)
def get_produits_par_magasin(magasin_id: int, db: Session = Depends(get_db)):
    cache_key = f"responsable:magasin:{magasin_id}:produits"
    cache = get_cache(cache_key)
    if cache:
        return cache

    stocks = db.query(ProduitParMagasin).filter_by(magasin_id=magasin_id).all()
    if not stocks:
        raise HTTPException(status_code=404, detail="Aucun produit trouvé pour ce magasin.")

    result = [
        {
            "produit_id": s.produit_id,
            "nom": s.produit.name,
            "quantite": s.quantite
        } for s in stocks
    ]
    set_cache(cache_key, result)
    return result

@router.get("/alertes-rupture", status_code=status.HTTP_200_OK)
def get_alertes_rupture(db: Session = Depends(get_db)):
    cache_key = "responsable:alertes-rupture"
    cache = get_cache(cache_key)
    if cache:
        return cache

    alertes = db.query(AlerteRupture).filter_by(regler=False).all()
    result = [
        {
            "id": a.id,
            "produit": a.produit.name,
            "seuil": a.seuil,
            "regler": a.regler
        } for a in alertes
    ]
    set_cache(cache_key, result)
    return result
