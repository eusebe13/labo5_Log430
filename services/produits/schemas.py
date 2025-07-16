# schemas.py (dans le service produits ou partagé)

from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: Optional[int] = 0

class ProductUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    price: Optional[float]
    stock: Optional[int]

class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int

    class Config:
        orm_mode = True
