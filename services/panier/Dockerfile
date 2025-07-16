# Dockerfile
FROM python:3.11-slim

# Installer les dépendances système nécessaires à certains paquets Python (ex: SQLAlchemy)
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers du service
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Rendre le script de démarrage exécutable
RUN chmod +x start.sh

# Commande de lancement
CMD ["sh", "start.sh"]
