# Décision d'architecture : NGINX comme Reverse Proxy

## Contexte

Mon architecture nécessite un point d’entrée HTTP unique pour router les requêtes vers les services backend (API, frontend, etc.), tout en assurant la gestion du TLS, des en-têtes, de la compression et du load balancing.

## Décision

J'ai choisi **NGINX** comme reverse proxy et gestionnaire des connexions entrantes.

## Justification

- Très haute performance et faible empreinte mémoire
- Grande maturité et stabilité
- Support de TLS, HTTP/2, GZIP, etc.
- Utilisé en production dans de nombreux environnements
- Configuration simple mais puissante
- Large communauté et documentation abondante

## Conséquences

- Les développeurs et DevOps doivent savoir écrire et lire des fichiers de configuration NGINX
- Le déploiement nécessite un monitoring minimal (fichiers logs, redémarrage, rechargement dynamique)