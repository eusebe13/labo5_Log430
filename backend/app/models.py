import datetime
import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RoleEnum(enum.Enum):
    gestionnaire = "gestionnaire"
    employe = "employe"
    responsable = "responsable"

rapport_product_assoc = Table(
    'rapport_product_assoc', Base.metadata,
    Column('rapport_id', Integer, ForeignKey('rapport_tendance.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    mot_de_passe = Column(String, nullable=False)
    magasin_id = Column(Integer, ForeignKey('magasins.id'), nullable=True)

    magasin = relationship("Magasin", back_populates="utilisateurs")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)  # haché
    adresse = Column(String, nullable=True)
    telephone = Column(String, nullable=True)

    commandes = relationship("Commande", back_populates="client", cascade="all, delete-orphan")
    panier = relationship("Panier", back_populates="client", uselist=False, cascade="all, delete-orphan")

class Magasin(Base):
    __tablename__ = 'magasins'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    region = Column(String, nullable=False)
    is_maison_mere = Column(Boolean, default=False)
    maison_mere_id = Column(Integer, ForeignKey('magasins.id'), nullable=True)

    ventes = relationship("Vente", back_populates="magasin")
    produit_par_magasin = relationship("ProduitParMagasin", back_populates="magasin")
    utilisateurs = relationship("Utilisateur", back_populates="magasin")
    maison_mere = relationship("Magasin", remote_side=[id], backref="magasins_filles")
    reaprovisionnements = relationship("Reaprovisionnement", back_populates="magasin")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    ventes = relationship("Vente", back_populates="produit")
    produit_par_magasin = relationship("ProduitParMagasin", back_populates="produit")
    rapports = relationship("RapportTendance", secondary=rapport_product_assoc, back_populates="produits")
    stock_central = relationship("StockCentral", back_populates="produit", uselist=False)
    alertes = relationship("AlerteRupture", back_populates="produit")
    reaprovisionnements = relationship("Reaprovisionnement", back_populates="produit")

class Vente(Base):
    __tablename__ = 'ventes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    quantite = Column(Integer, nullable=False)
    prix_total = Column(Float, nullable=False)

    produit_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    magasin_id = Column(Integer, ForeignKey('magasins.id'), nullable=False)

    produit = relationship("Product", back_populates="ventes")
    magasin = relationship("Magasin", back_populates="ventes")

class RapportTendance(Base):
    __tablename__ = 'rapport_tendance'
    id = Column(Integer, primary_key=True)
    region = Column(String, nullable=False)
    total_ventes = Column(Float)

    produits = relationship("Product", secondary=rapport_product_assoc, back_populates="rapports")

class ProduitParMagasin(Base):
    __tablename__ = 'produit_par_magasin'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    magasin_id = Column(Integer, ForeignKey('magasins.id'), nullable=False)
    quantite = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('produit_id', 'magasin_id', name='uq_produit_magasin'),
    )

    produit = relationship("Product", back_populates="produit_par_magasin")
    magasin = relationship("Magasin", back_populates="produit_par_magasin")

class StockCentral(Base):
    __tablename__ = 'stock_central'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('products.id'), unique=True)
    quantite = Column(Integer, nullable=False)

    produit = relationship("Product", back_populates="stock_central")

class Reaprovisionnement(Base):
    __tablename__ = "reaprovisionnement"
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    magasin_id = Column(Integer, ForeignKey('magasins.id'), nullable=False)
    quantite = Column(Integer, nullable=False)
    approuved = Column(Boolean, nullable=True, default=None)

    produit = relationship("Product", back_populates="reaprovisionnements")
    magasin = relationship("Magasin", back_populates="reaprovisionnements")

# Alerte Rupture
class AlerteRupture(Base):
    __tablename__ = 'alertes_rupture'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('products.id'), unique=True)
    seuil = Column(Integer, nullable=False)
    regler = Column(Boolean, default=False)

    produit = relationship("Product", back_populates="alertes")

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    date_commande = Column(DateTime, default=datetime.datetime.utcnow)
    statut = Column(String, default="en_attente")  # ex : en_attente, payée, annulée
    total = Column(Float, nullable=False)

    client = relationship("Client", backref="commandes")
    lignes_commande = relationship("LigneCommande", back_populates="commande", cascade="all, delete")

class LigneCommande(Base):
    __tablename__ = "lignes_commande"

    id = Column(Integer, primary_key=True)
    commande_id = Column(Integer, ForeignKey("commandes.id"), nullable=False)
    produit_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    commande = relationship("Commande", back_populates="lignes_commande")
    produit = relationship("Product")

class Panier(Base):
    __tablename__ = "paniers"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, unique=True)

    client = relationship("Client", back_populates="panier")
    articles = relationship("ArticlePanier", back_populates="panier", cascade="all, delete")

class ArticlePanier(Base):
    __tablename__ = "articles_panier"

    id = Column(Integer, primary_key=True)
    panier_id = Column(Integer, ForeignKey("paniers.id"), nullable=False)
    produit_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantite = Column(Integer, nullable=False)

    panier = relationship("Panier", back_populates="articles")
    produit = relationship("Product")


# Mise à jour des modèles précédents pour compléter les relations :

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)  # haché
    adresse = Column(String, nullable=True)
    telephone = Column(String, nullable=True)

    commandes = relationship("Commande", back_populates="client", cascade="all, delete-orphan")
    panier = relationship("Panier", back_populates="client", uselist=False, cascade="all, delete-orphan")


class Panier(Base):
    __tablename__ = "paniers"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, unique=True)

    client = relationship("Client", back_populates="panier")
    articles = relationship("ArticlePanier", back_populates="panier", cascade="all, delete")


class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    date_commande = Column(DateTime, default=datetime.datetime.utcnow)
    statut = Column(String, default="en_attente")  # ex : en_attente, payée, annulée
    total = Column(Float, nullable=False)

    client = relationship("Client", back_populates="commandes")
    lignes_commande = relationship("LigneCommande", back_populates="commande", cascade="all, delete")


class LigneCommande(Base):
    __tablename__ = "lignes_commande"

    id = Column(Integer, primary_key=True)
    commande_id = Column(Integer, ForeignKey("commandes.id"), nullable=False)
    produit_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    commande = relationship("Commande", back_populates="lignes_commande")
    produit = relationship("Product")
