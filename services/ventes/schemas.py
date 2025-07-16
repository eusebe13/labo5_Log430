from pydantic import BaseModel
from datetime import datetime

class VenteCreate(BaseModel):
    produit_id: int
    magasin_id: int
    quantite: int
    prix_total: float

class VenteOut(BaseModel):
    id: int
    produit_id: int
    magasin_id: int
    quantite: int
    prix_total: float
    date: datetime

    class Config:
        orm_mode = True
