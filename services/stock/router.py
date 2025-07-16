from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import redis
import os
import json

from models import StockCentral
from database import get_db
from schemas import StockCentralOut, StockUpdate

router = APIRouter()

# Redis setup
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)

@router.get("/", response_model=list[StockCentralOut])
def get_all_stock(db: Session = Depends(get_db)):
    cached = get_cache("stock:all")
    if cached:
        return json.loads(cached)

    stocks = db.query(StockCentral).all()
    result = [StockCentralOut.from_orm(s) for s in stocks]
    set_cache("stock:all", json.dumps([s.dict() for s in result]), ttl=300)
    return result

@router.get("/{produit_id}", response_model=StockCentralOut)
def get_stock_produit(produit_id: int, db: Session = Depends(get_db)):
    key = f"stock:{produit_id}"
    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    stock = db.query(StockCentral).filter_by(produit_id=produit_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock non trouvé")

    result = StockCentralOut.from_orm(stock)
    set_cache(key, result.json(), ttl=300)
    return result

@router.post("/{produit_id}", response_model=StockCentralOut)
def reapprovisionner_stock(produit_id: int, update: StockUpdate, db: Session = Depends(get_db)):
    stock = db.query(StockCentral).filter_by(produit_id=produit_id).first()
    if not stock:
        stock = StockCentral(produit_id=produit_id, quantite=update.quantite)
        db.add(stock)
    else:
        stock.quantite += update.quantite

    db.commit()
    db.refresh(stock)

    invalidate_cache(f"stock:{produit_id}")
    invalidate_cache("stock:all")
    return stock
