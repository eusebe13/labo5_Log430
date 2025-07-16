from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
import redis
import os
import json
import datetime

from models import Vente
from database import get_db
from schemas import VenteOut

router = APIRouter()

# Redis
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)


@router.post("/", response_model=VenteOut, status_code=status.HTTP_201_CREATED)
async def enregistrer_vente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    vente = Vente(
        produit_id=data["produit_id"],
        magasin_id=data["magasin_id"],
        quantite=data["quantite"],
        prix_total=data["prix_total"],
        date=datetime.datetime.utcnow()
    )
    db.add(vente)
    db.commit()
    db.refresh(vente)
    invalidate_cache("ventes:all")
    return vente


@router.get("/", response_model=list[VenteOut])
def get_all_ventes(db: Session = Depends(get_db)):
    cached = get_cache("ventes:all")
    if cached:
        return json.loads(cached)
    ventes = db.query(Vente).all()
    result = [VenteOut.from_orm(v) for v in ventes]
    set_cache("ventes:all", json.dumps([v.dict() for v in result]), ttl=300)
    return result


@router.get("/{vente_id}", response_model=VenteOut)
def get_vente(vente_id: int, db: Session = Depends(get_db)):
    key = f"vente:{vente_id}"
    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    vente = db.query(Vente).get(vente_id)
    if not vente:
        raise HTTPException(status_code=404, detail="Vente non trouvée")
    result = VenteOut.from_orm(vente)
    set_cache(key, result.json(), ttl=300)
    return result


@router.delete("/{vente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vente(vente_id: int, db: Session = Depends(get_db)):
    vente = db.query(Vente).get(vente_id)
    if not vente:
        raise HTTPException(status_code=404, detail="Vente non trouvée")
    db.delete(vente)
    db.commit()
    invalidate_cache(f"vente:{vente_id}")
    invalidate_cache("ventes:all")
