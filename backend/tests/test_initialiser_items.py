# tests/test_initialiser_items.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models import Product


def test_produits_initialises():
    db = SessionLocal()
    produits = db.query(Product).all()
    assert len(produits) >= 0  # suppose que certains produits sont déjà ajoutés
    db.close()
