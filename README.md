# Labo 5 — Passage à une Architecture Microservices avec API Gateway et Observabilité

## Description du projet

Ce projet est l'évolution de l'application POS (Point Of Sale) du **Labo 4**, transformée en architecture **microservices** avec des services dédiés, une **API Gateway (KrakenD)**, un **monitoring avancé** et du **load balancing dynamique**. L'objectif est d'augmenter la **scalabilité**, la **séparation des responsabilités**, et la **résilience**.

---
## Arborescence du projet

```bash
C:.
├───.github
│   └───workflows              # CI/CD 
├───docs                       # Documentation technique
│   ├───adr                    # Architecture Decision Records
│   ├───image                  # Images d'illustration
│   └───uml                    # Modèles UML
│       ├───code
│       └───png
├───frontend                   # Interface utilisateur
│  └───src
│      ├───api
│      ├───assets
│      ├───components
│      ├───pages
│      └───public
├───gateway                    # API Gateway
│   ├───krakend.json           # Configuration KrakenD
│   └───nginx.conf             # Configuration NGINX
├───grafana                    # Monitoring avec Grafana
│   ├───dashboards
│   └───provisioning
├───k6                         # Tests de charge avec K6
│   ├───stock_test.js
│   └───README.md
├───services                   # Microservices FastAPI
│   ├───.ruff_cache
│   │   └───0.11.12
│   ├───client
│   │   └───__pycache__
│   ├───commande
│   │   └───__pycache__
│   ├───panier
│   ├───produits
│   │   └───__pycache__
│   ├───rapport
│   ├───stock
│   │   ├───main.py
│   │   └───Dockerfile
│   ├───utilisateurs
│   └───ventes
```

## Différences avec le Labo 4

| Aspect                    | Labo 4                                  | Labo 5 (actuel)                                                                 |
|--------------------------|-----------------------------------------|----------------------------------------------------------------------------------|
| Architecture             | Monolithique (FastAPI unique)           | Microservices isolés, déployables indépendamment                                |
| Communication            | Appels directs frontend-backend         | Accès via une API Gateway unique (KrakenD)                                       |
| Observabilité            | Prometheus/Grafana sur FastAPI unique    | Métriques agrégées par KrakenD + multi-instances backend                          |
| Load balancing           | Avec Nginx entre 2 backends FastAPI     | Load balancing natif KrakenD (round-robin)                                      |
| Flexibilité              | Faible séparation des composants        | Services modulables, extensibles facilement                                     |
| Sécurité/API            | JWT standard                           | KrakenD ajoute des entêtes, gestion d'API Keys et CORS                         |
| Scalabilité              | Limitée à 2-3 conteneurs              | Extensible horizontalement (Docker Compose multi-services)                      |

---

## Services Microservices définis

- `authentification` — Gestion JWT et création de comptes clients
- `clientele` — Gestion du panier et du profil client
- `travailleur` — Employés, gestionnaires et responsables
- `magasin` — Produits, ventes, stock, rapports, checkout

Chaque service dispose de son propre : `models.py`, `router.py`, `schemas.py`, `init_db.py`, `main.py`, etc.

---

## Lancement de l'application

```bash
docker-compose down
COMPOSE_PROFILES=full docker-compose up --build
```

*KrakenD écoute sur `http://localhost:8081` et redirige vers les microservices.*

---

## API Gateway avec KrakenD

KrakenD est utilisé pour regrouper tous les services derrière une **interface unique**.

### Fonctionnalités mises en place :
- 🏦 **Routage dynamique** entre les services `travailleur`, `magasin`, `authentification`, `clientele`
- 📅 **Ajout d'en-têtes personnalisés** (éventuellement avec des clés API ou autorisation)
- 📰 **Logging centralisé** via stdout + Prometheus exposé par KrakenD
- ❄️ **Load balancing** round-robin sur deux instances du service panier

---

## Load Balancing du service Panier

- KrakenD est configuré pour distribuer les requêtes entre deux conteneurs Docker `panier1` et `panier2`.
- Algorithme utilisé : `round_robin`

### Test de charge avec `k6`

Créer un fichier `load_test.js` :
```js
import http from 'k6/http';
export default function () {
  http.get('http://localhost:8081/api/panier/items');
}
```
Lancer :
```bash
k6 run load_test.js
```

### Bonus : Visualisation Prometheus/Grafana

- **Prometheus scrape** les métriques sur `http://krakend:8081/__debug/metrics`
- **Grafana** présente le répartiteur de charge, erreurs, latence, etc.

---

## Sécurité

- JWT via le service `authentification`
- KrakenD ajoute des entêtes ou clés API sur demande
- **Règles CORS activées** dans `krakend.json`

---

## Avancement des étapes du Labo 5

| Étape                                                     | Statut       |
|------------------------------------------------------------|--------------|
| 1. Découpage logique du système                          |  Fait     |
| 2. API Gateway (KrakenD)                                   |  Fait     |
| 3. Load balancing + test de charge (panier)                |  Fait     |
| 4. Logging/API Keys/CORS                                   |  Fait     |
| 5. Observabilité (Prometheus + Grafana)                   |  Fait     |
| 6. Comparaison avec Labo 4 (latence, visibilité, etc.)     |  Partiel |
| 7. Documentation Swagger + tests Postman à jour           | Fait |
| 8. Dashboards Grafana présentés dans le livrable           |  à faire |

---

## Accès aux outils

| Service       | URL                                      |
|---------------|-------------------------------------------|
| API Gateway   | http://localhost:8081                     |
| Frontend      | http://localhost:5173                     |
| Swagger API   | http://localhost:8081/docs                |
| KrakenD Admin | http://localhost:8081/__debug/metrics     |
| Prometheus    | http://localhost:9090                     |
| Grafana       | http://localhost:3000                     |

---

## Aide-mémoire

- `krakend.json` décrit tous les endpoints déclenchables
- `docker-compose.yml` active plusieurs profils (frontend, backend, gateway, observabilité)
- `k6`, `Grafana`, `Prometheus` permettent de valider les perfs et la répartition de charge

---

## Swagger & API Docs

- Accéder via : http://localhost:8081/docs
- Ou utiliser **Postman** avec les requêtes à jour pour chaque microservice via l'API Gateway.

---

**Remarque :** Pour une démo claire, ajouter un dashboard Grafana montrant le **nombre de requêtes par instance** (panier1 vs panier2).

