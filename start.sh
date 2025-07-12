#!/bin/bash

# === Initialisation de la base de données ===
echo "Initialisation de la base de données..."
cd backend || { echo "Dossier 'backend' introuvable."; exit 1; }

python app/init_db.py
if [ $? -ne 0 ]; then
    echo "Échec de l'initialisation de la base de données."
    exit 1
fi

# === Lancement du backend avec Uvicorn ===
echo "Démarrage du backend (Uvicorn)..."
uvicorn app.main:app --reload &
BACKEND_PID=$!

# Retour à la racine du projet
cd ..

# === Lancement du frontend ===
echo "Démarrage du frontend (Vite)..."
cd frontend || { echo "Dossier 'frontend' introuvable."; kill $BACKEND_PID; exit 1; }

npm run dev &
FRONTEND_PID=$!

cd ..

# === Gestion de l’arrêt propre avec Ctrl+C ===
trap "echo 'Arrêt en cours...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Attente des processus
wait
