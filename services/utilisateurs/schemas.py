from pydantic import BaseModel
from typing import Optional
import enum

class RoleEnum(str, enum.Enum):
    gestionnaire = "gestionnaire"
    employe = "employe"
    responsable = "responsable"

class UtilisateurCreate(BaseModel):
    nom: str
    mot_de_passe: str
    role: RoleEnum
    magasin_id: Optional[int]

class UtilisateurLogin(BaseModel):
    nom: str
    mot_de_passe: str

class UtilisateurUpdate(BaseModel):
    nom: Optional[str]
    mot_de_passe: Optional[str]
    role: Optional[RoleEnum]
    magasin_id: Optional[int]

class UtilisateurOut(BaseModel):
    id: int
    nom: str
    role: RoleEnum
    magasin_id: Optional[int]

    class Config:
        orm_mode = True
