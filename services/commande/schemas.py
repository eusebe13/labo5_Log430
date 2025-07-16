# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class LigneCommandeCreate(BaseModel):
    produit_id: int
    quantite: int
    prix_unitaire: float

class LigneCommandeOut(LigneCommandeCreate):
    id: int

    class Config:
        orm_mode = True

class CommandeCreate(BaseModel):
    client_id: int
    statut: str
    total: float
    lignes_commande: List[LigneCommandeCreate]

class CommandeUpdate(BaseModel):
    statut: Optional[str] = None
    total: Optional[float] = None

class CommandeOut(BaseModel):
    id: int
    client_id: int
    statut: str
    total: float
    lignes: List[LigneCommandeOut]

    class Config:
        orm_mode = True
