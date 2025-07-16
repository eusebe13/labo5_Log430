# router.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
import json
import redis
import os

from models import Client
from database import get_db
from schemas import ClientCreate, ClientUpdate, ClientLogin, ClientOut

# Redis setup
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)

router = APIRouter()

@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter_by(email=client.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed = bcrypt.hash(client.mot_de_passe)
    new_client = Client(
        nom=client.nom,
        prenom=client.prenom,
        email=client.email,
        mot_de_passe=hashed,
        adresse=client.adresse,
        telephone=client.telephone
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    invalidate_cache("clients:all")
    return new_client

@router.post("/connexion", response_model=ClientOut)
def login_client(credentials: ClientLogin, db: Session = Depends(get_db)):
    client = db.query(Client).filter_by(email=credentials.email).first()
    if not client or not bcrypt.verify(credentials.mot_de_passe, client.mot_de_passe):
        raise HTTPException(status_code=401, detail="Email ou mot de passe invalide")
    return client

@router.get("/", response_model=list[ClientOut])
def get_all_clients(db: Session = Depends(get_db)):
    cached = get_cache("clients:all")
    if cached:
        return json.loads(cached)

    clients = db.query(Client).all()
    result = [ClientOut.from_orm(c) for c in clients]
    set_cache("clients:all", json.dumps([c.dict() for c in result]), ttl=300)
    return result

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    key = f"client:{client_id}"
    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    result = ClientOut.from_orm(client)
    set_cache(key, json.dumps(result.dict()), ttl=300)
    return result

@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, update: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    if update.nom is not None:
        client.nom = update.nom
    if update.prenom is not None:
        client.prenom = update.prenom
    if update.adresse is not None:
        client.adresse = update.adresse
    if update.telephone is not None:
        client.telephone = update.telephone
    if update.mot_de_passe is not None:
        client.mot_de_passe = bcrypt.hash(update.mot_de_passe)

    db.commit()
    db.refresh(client)

    invalidate_cache(f"client:{client_id}")
    invalidate_cache("clients:all")

    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    db.delete(client)
    db.commit()

    invalidate_cache(f"client:{client_id}")
    invalidate_cache("clients:all")
