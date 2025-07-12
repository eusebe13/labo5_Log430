from typing import List, Literal, Optional

from pydantic import BaseModel, Field

# ======= AUTHENTIFICATION =======

class ConnexionRequest(BaseModel):
    nom: str
    mot_de_passe: str

class ConnexionResponse(BaseModel):
    message: str
    nom: str
    role: str
    token: str

# ======= PRODUIT =======

class ProduitBase(BaseModel):
    name: str
    category: str
    price: float


class ProduitCreate(ProduitBase):
    stock: Optional[int] = 0


class ProduitResponse(ProduitBase):
    id: int
    stock: int

    class Config:
        orm_mode = True


# ======= ACHAT / VENTE =======

class ProduitAchat(BaseModel):
    produit_id: int
    quantite: int = Field(..., gt=0)


class AchatRequest(BaseModel):
    produits: List[ProduitAchat]


class AchatResponse(BaseModel):
    resultats: List[str]


# ======= STOCK =======

class StockMagasinResponse(BaseModel):
    produit_id: int
    produit: str
    magasin_id: int
    magasin: str
    quantite: int


class StockCentralResponse(BaseModel):
    id: int
    name: str
    stock_central: int


# ======= REAPPROVISIONNEMENT =======

class ReapprovisionnementRequest(BaseModel):
    produit_id: int
    quantite: int
    magasin_id: int


class ReapprovisionnementResponse(BaseModel):
    message: str

class ReapprovisionnementEtat(BaseModel):
    id: int
    produit: str
    magasin: str
    quantite: int
    approuved: bool

# ======= RAPPORTS =======

class RapportCreate(BaseModel):
    region: str


class RapportResponse(BaseModel):
    id: int
    region: str
    total_ventes: Optional[float] = 0.0

    class Config:
        orm_mode = True


# ======= MISE À JOUR PRODUIT =======

class UpdateChampProduit(BaseModel):
    champ: Literal["name", "price", "category"]  # ← Limité aux champs modifiables
    valeur: str

# ======= ALERTES RUPTURE =======

class AlerteRupture(BaseModel):
    id: int
    produit: str
    seuil: int
    regler: bool
