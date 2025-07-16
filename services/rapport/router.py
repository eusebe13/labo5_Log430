# router.py (dans le service rapport)

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import redis
import os
import json

from models import RapportTendance
from database import get_db
from schemas import RapportCreate, RapportOut

router = APIRouter()

# Redis setup
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)

@router.post("/", response_model=RapportOut, status_code=status.HTTP_201_CREATED)
def create_rapport(rapport: RapportCreate, db: Session = Depends(get_db)):
    new_rapport = RapportTendance(
        region=rapport.region,
        total_ventes=rapport.total_ventes
    )
    db.add(new_rapport)
    db.commit()
    db.refresh(new_rapport)

    invalidate_cache("rapports:all")
    return new_rapport

@router.get("/", response_model=list[RapportOut])
def get_all_rapports(db: Session = Depends(get_db)):
    cached = get_cache("rapports:all")
    if cached:
        return json.loads(cached)

    rapports = db.query(RapportTendance).all()
    result = [RapportOut.from_orm(r) for r in rapports]
    set_cache("rapports:all", json.dumps([r.dict() for r in result]), ttl=300)
    return result

@router.get("/{rapport_id}", response_model=RapportOut)
def get_rapport(rapport_id: int, db: Session = Depends(get_db)):
    key = f"rapport:{rapport_id}"
    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    rapport = db.query(RapportTendance).get(rapport_id)
    if not rapport:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")

    result = RapportOut.from_orm(rapport)
    set_cache(key, result.json(), ttl=300)
    return result

@router.delete("/{rapport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rapport(rapport_id: int, db: Session = Depends(get_db)):
    rapport = db.query(RapportTendance).get(rapport_id)
    if not rapport:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")

    db.delete(rapport)
    db.commit()

    invalidate_cache(f"rapport:{rapport_id}")
    invalidate_cache("rapports:all")
