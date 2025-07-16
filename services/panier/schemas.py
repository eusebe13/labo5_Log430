# schemas.py pour /panier
from pydantic import BaseModel
from typing import List

class ArticlePanierCreate(BaseModel):
    produit_id: int
    quantite: int

class ArticlePanierOut(BaseModel):
    produit_id: int
    quantite: int

class PanierOut(BaseModel):
    id: int
    client_id: int
    articles: List[ArticlePanierOut]
