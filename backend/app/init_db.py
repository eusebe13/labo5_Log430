import os
import sys

# Ajouter le chemin du dossier parent pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine
from app.initialiser_items import init_data
from app.models import Base


def init_db():
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)

    print("Insertion des données initiales...")
    init_data()
    print("Initialisation terminée.")

if __name__ == "__main__":
    init_db()
