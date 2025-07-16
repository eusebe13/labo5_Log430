from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    mot_de_passe: str
    adresse: Optional[str] = None
    telephone: Optional[str] = None

class ClientOut(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr
    adresse: Optional[str] = None
    telephone: Optional[str] = None

    class Config:
        orm_mode = True

class ClientLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str

class ClientUpdate(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    adresse: Optional[str]
    telephone: Optional[str]
    mot_de_passe: Optional[str]
