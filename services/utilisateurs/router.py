from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
import redis
import os
import json

from models import Utilisateur
from database import get_db
from schemas import UtilisateurOut

router = APIRouter()

# Redis
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    r.set(key, value, ex=ttl)

def invalidate_cache(key: str):
    r.delete(key)


@router.post("/", response_model=UtilisateurOut, status_code=status.HTTP_201_CREATED)
async def create_utilisateur(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    existing = db.query(Utilisateur).filter_by(nom=data["nom"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

    hashed = bcrypt.hash(data["mot_de_passe"])
    utilisateur = Utilisateur(
        nom=data["nom"],
        role=data["role"],
        mot_de_passe=hashed,
        magasin_id=data.get("magasin_id")
    )
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)
    invalidate_cache("utilisateurs:all")
    return utilisateur


@router.post("/connexion", response_model=UtilisateurOut)
async def login_utilisateur(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    utilisateur = db.query(Utilisateur).filter_by(nom=data["nom"]).first()
    if not utilisateur or not bcrypt.verify(data["mot_de_passe"], utilisateur.mot_de_passe):
        raise HTTPException(status_code=401, detail="Nom ou mot de passe invalide")
    return utilisateur


@router.get("/", response_model=list[UtilisateurOut])
def get_all_utilisateurs(db: Session = Depends(get_db)):
    cached = get_cache("utilisateurs:all")
    if cached:
        return json.loads(cached)
    utilisateurs = db.query(Utilisateur).all()
    result = [UtilisateurOut.from_orm(u) for u in utilisateurs]
    set_cache("utilisateurs:all", json.dumps([u.dict() for u in result]), ttl=300)
    return result


@router.get("/{utilisateur_id}", response_model=UtilisateurOut)
def get_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    key = f"utilisateur:{utilisateur_id}"
    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    utilisateur = db.query(Utilisateur).get(utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    result = UtilisateurOut.from_orm(utilisateur)
    set_cache(key, result.json(), ttl=300)
    return result


@router.put("/{utilisateur_id}", response_model=UtilisateurOut)
async def update_utilisateur(utilisateur_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    utilisateur = db.query(Utilisateur).get(utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    utilisateur.nom = data.get("nom", utilisateur.nom)
    utilisateur.role = data.get("role", utilisateur.role)
    if data.get("mot_de_passe"):
        utilisateur.mot_de_passe = bcrypt.hash(data["mot_de_passe"])
    utilisateur.magasin_id = data.get("magasin_id", utilisateur.magasin_id)

    db.commit()
    db.refresh(utilisateur)
    invalidate_cache(f"utilisateur:{utilisateur_id}")
    invalidate_cache("utilisateurs:all")
    return utilisateur


@router.delete("/{utilisateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = db.query(Utilisateur).get(utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    db.delete(utilisateur)
    db.commit()
    invalidate_cache(f"utilisateur:{utilisateur_id}")
    invalidate_cache("utilisateurs:all")
