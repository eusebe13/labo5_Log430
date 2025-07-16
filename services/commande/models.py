# models.py
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    statut = Column(String, nullable=False)
    total = Column(Float, nullable=False)

    lignes = relationship("LigneCommande", back_populates="commande", cascade="all, delete-orphan")

class LigneCommande(Base):
    __tablename__ = "lignes_commande"

    id = Column(Integer, primary_key=True, index=True)
    commande_id = Column(Integer, ForeignKey("commandes.id"))
    produit_id = Column(Integer)
    quantite = Column(Integer)
    prix_unitaire = Column(Float)

    commande = relationship("Commande", back_populates="lignes")
