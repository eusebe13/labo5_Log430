# router.py pour /panier
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
import redis
import os

from models import Panier, ArticlePanier
from database import get_db
from schemas import PanierOut, ArticlePanierOut, ArticlePanierCreate

# Connexion Redis
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)

router = APIRouter()

@router.get("/{client_id}", response_model=PanierOut)
def get_panier(client_id: int, db: Session = Depends(get_db)):
    key = f"panier:{client_id}"
    cached = get_cache(key)
    if cached:
        return PanierOut.parse_raw(cached)

    panier = db.query(Panier).options(joinedload(Panier.articles)).filter_by(client_id=client_id).first()
    if not panier:
        raise HTTPException(status_code=404, detail="Panier non trouvé")

    articles = [
        ArticlePanierOut(
            produit_id=a.produit_id,
            quantite=a.quantite
        ) for a in panier.articles
    ]
    result = PanierOut(id=panier.id, client_id=panier.client_id, articles=articles)
    set_cache(key, result.json())
    return result

@router.post("/{client_id}/ajouter", response_model=PanierOut)
def ajouter_au_panier(client_id: int, item: ArticlePanierCreate, db: Session = Depends(get_db)):
    panier = db.query(Panier).filter_by(client_id=client_id).first()
    if not panier:
        panier = Panier(client_id=client_id)
        db.add(panier)
        db.commit()
        db.refresh(panier)

    article = next((a for a in panier.articles if a.produit_id == item.produit_id), None)
    if article:
        article.quantite += item.quantite
    else:
        new_article = ArticlePanier(produit_id=item.produit_id, quantite=item.quantite, panier_id=panier.id)
        db.add(new_article)

    db.commit()
    db.refresh(panier)
    invalidate_cache(f"panier:{client_id}")
    return get_panier(client_id, db)

@router.delete("/{client_id}/vider", status_code=status.HTTP_204_NO_CONTENT)
def vider_panier(client_id: int, db: Session = Depends(get_db)):
    panier = db.query(Panier).filter_by(client_id=client_id).first()
    if not panier:
        raise HTTPException(status_code=404, detail="Panier non trouvé")

    for a in panier.articles:
        db.delete(a)
    db.commit()
    invalidate_cache(f"panier:{client_id}")
