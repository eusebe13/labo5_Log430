from pydantic import BaseModel

class StockUpdate(BaseModel):
    quantite: int

class StockCentralOut(BaseModel):
    id: int
    produit_id: int
    quantite: int

    class Config:
        orm_mode = True
