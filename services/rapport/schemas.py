# schemas.py (dans le service rapport ou partagé)

from pydantic import BaseModel
from typing import Optional

class RapportCreate(BaseModel):
    region: str
    total_ventes: Optional[float] = 0.0

class RapportOut(BaseModel):
    id: int
    region: str
    total_ventes: float

    class Config:
        orm_mode = True
