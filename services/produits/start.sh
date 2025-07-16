#!/bin/sh

echo "Attente que la base de données soit prête..."
sleep 3

# Initialiser les données si un script init existe
if [ -f init_produits.py ]; then
  echo "Initialisation des données..."
  python init_produits.py
fi

# Lancer le serveur FastAPI
echo "Démarrage de l'API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
