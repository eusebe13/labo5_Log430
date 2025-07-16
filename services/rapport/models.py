
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RapportTendance(Base):
    __tablename__ = 'rapport_tendance'
    id = Column(Integer, primary_key=True)
    region = Column(String, nullable=False)
    total_ventes = Column(Float)
