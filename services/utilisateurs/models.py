import enum

from sqlalchemy import (
    Column,
    Enum,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RoleEnum(enum.Enum):
    gestionnaire = "gestionnaire"
    employe = "employe"
    responsable = "responsable"


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    mot_de_passe = Column(String, nullable=False)
    magasin_id = Column(Integer, nullable=True)
