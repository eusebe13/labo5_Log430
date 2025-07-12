# backend/Dockerfile
FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y build-essential

# Créer le répertoire d'application
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
