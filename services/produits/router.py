# router.py (dans le service produits)

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import redis
import os
import json

from models import Produit
from database import get_db
from schemas import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()

# Redis
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Produit(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock or 0
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    invalidate_cache("produits:all")
    return new_product

@router.get("/", response_model=list[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    cached = get_cache("produits:all")
    if cached:
        return json.loads(cached)

    produits = db.query(Produit).all()
    result = [
        ProductOut(
            id=p.id,
            name=p.name,
            category=p.category,
            price=p.price,
            stock=p.stock
        ) for p in produits
    ]
    set_cache("produits:all", json.dumps([r.dict() for r in result]), ttl=300)
    return result

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    key = f"produit:{product_id}"
    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    product = db.query(Produit).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    result = ProductOut.from_orm(product)
    set_cache(key, result.json(), ttl=300)
    return result

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Produit).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    if update.name:
        product.name = update.name
    if update.category:
        product.category = update.category
    if update.price is not None:
        product.price = update.price
    if update.stock is not None:
        product.stock = update.stock

    db.commit()
    db.refresh(product)

    invalidate_cache(f"produit:{product_id}")
    invalidate_cache("produits:all")

    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Produit).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    db.delete(product)
    db.commit()

    invalidate_cache(f"produit:{product_id}")
    invalidate_cache("produits:all")
