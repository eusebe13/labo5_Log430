
from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class StockCentral(Base):
    __tablename__ = 'stock_central'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, unique=True)
    quantite = Column(Integer, nullable=False)
