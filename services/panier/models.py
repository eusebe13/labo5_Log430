from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Panier(Base):
    __tablename__ = "paniers"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False, unique=True)
    total = Column(Integer, nullable=False, default=0)

    articles = relationship("ArticlePanier", back_populates="panier", cascade="all, delete-orphan")

class ArticlePanier(Base):
    __tablename__ = "articles_panier"

    id = Column(Integer, primary_key=True)
    panier_id = Column(Integer, ForeignKey("paniers.id"), nullable=False)  # ✅ ForeignKey ajouté ici
    produit_id = Column(Integer, nullable=False)
    quantite = Column(Integer, nullable=False)

    panier = relationship("Panier", back_populates="articles")
