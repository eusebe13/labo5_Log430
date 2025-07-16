# router
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List

from models import Commande, LigneCommande
from database import get_db
from schemas import CommandeCreate, CommandeUpdate, CommandeOut

router = APIRouter()

@router.get("/test", status_code=status.HTTP_200_OK)
def test_endpoint():
    return {"message": "Endpoint de test pour le service de commande fonctionne correctement."}

@router.post("/", response_model=CommandeOut, status_code=status.HTTP_201_CREATED)
def create_commande(commande_in: CommandeCreate, db: Session = Depends(get_db)):
    nouvelle_commande = Commande(
        client_id=commande_in.client_id,
        statut=commande_in.statut,
        total=commande_in.total
    )
    db.add(nouvelle_commande)
    db.commit()
    db.refresh(nouvelle_commande)

    lignes = []
    for ligne in commande_in.lignes_commande:
        nouvelle_ligne = LigneCommande(
            commande_id=nouvelle_commande.id,
            produit_id=ligne.produit_id,
            quantite=ligne.quantite,
            prix_unitaire=ligne.prix_unitaire
        )
        db.add(nouvelle_ligne)
        lignes.append(nouvelle_ligne)

    db.commit()
    # Attacher manuellement les lignes à la commande pour le retour
    nouvelle_commande.lignes = lignes
    return nouvelle_commande

@router.get("/", response_model=List[CommandeOut])
def get_all_commandes(db: Session = Depends(get_db)):
    commandes = db.query(Commande).options(joinedload(Commande.lignes)).all()
    return commandes

@router.get("/{commande_id}", response_model=CommandeOut)
def get_commande(commande_id: int, db: Session = Depends(get_db)):
    commande = db.query(Commande).options(joinedload(Commande.lignes)).filter(Commande.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande

@router.put("/{commande_id}", response_model=CommandeOut)
def update_commande(commande_id: int, commande_update: CommandeUpdate, db: Session = Depends(get_db)):
    commande = db.query(Commande).options(joinedload(Commande.lignes)).filter(Commande.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    if commande_update.statut is not None:
        commande.statut = commande_update.statut
    if commande_update.total is not None:
        commande.total = commande_update.total

    db.commit()
    db.refresh(commande)
    return commande

@router.delete("/{commande_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commande(commande_id: int, db: Session = Depends(get_db)):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    db.delete(commande)
    db.commit()
