import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vente(Base):
    __tablename__ = 'ventes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    quantite = Column(Integer, nullable=False)
    prix_total = Column(Float, nullable=False)
