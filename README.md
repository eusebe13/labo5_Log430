# Labo 5 -  Passage ` a une Architecture Microservices avec API Gateway et Observabilité

## Description du projet

Ce projet constitue une extension d’un système de gestion multi-magasins, enrichi par une API REST développée avec **FastAPI** côté backend, et **React.js** côté frontend. Il respecte les principes du modèle **MVC** (voire **hexagonal**), avec une séparation claire entre la logique métier, les routes REST, la documentation, les tests, la CI/CD, ainsi qu'une authentification sécurisée via **JWT**.

De nouvelles fonctionnalités avancées ont été intégrées pour répondre aux exigences du **Labo 4** :

* **Observabilité** avec Prometheus & Grafana
* **Mise à l’échelle horizontale** avec plusieurs backends FastAPI
* **Load balancing** via Nginx
* **Mise en cache Redis** pour optimiser les performances

---

## Structure du projet

```
.
├── backend
│   ├── app
│   │   ├── auth.py
│   │   ├── employe.py
│   │   ├── gestionnaire.py
│   │   ├── responsable.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── router.py
│   │   ├── init_db.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   └── api
│   ├── public
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── nginx.conf
├── prometheus.yml
├── docs
└── .github/workflows/ci.yml
```

---

## Lancement du projet

### Prérequis

* Python 3.11
* Node.js 20+
* Docker

### Démarrer manuellement (hors Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
python app/init_db.py
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Démarrer avec Docker (recommandé)

```bash
docker-compose down
docker-compose up --build
```

---

## Nouvelles fonctionnalités (Labo 4)

### Load Balancing avec Nginx

* Deux instances backend (`backend1`, `backend2`) sont mises en place.
* Nginx répartit les requêtes entre elles grâce à un **upstream** configuré.
* Permet une **répartition de charge** et une **haute disponibilité**.

### Caching avec Redis

* Les routes `/rapports`, `/dashboard` utilisent un cache Redis.
* Les données sont mises en cache pour **améliorer la vitesse de réponse**.
* Moins de pression sur la base de données.

### Observabilité avec Prometheus et Grafana

* Prometheus scrape les métriques FastAPI sur `/metrics`.
* Grafana affiche les données temps réel : **latence**, **requêtes**, **erreurs**, etc.
* Permet une **analyse des performances** et **détection des anomalies**.

---

## Comptes utilisateurs

| Rôle         | Nom d’utilisateur | Mot de passe |
| ------------ | ----------------- | ------------ |
| Employé      | Bob               | 1234         |
| Gestionnaire | Alice             | admin        |
| Responsable  | Charlie           | root         |

Chaque rôle dispose d’une interface dédiée avec des permissions spécifiques.

---

## Cas d’usage principaux

* **UC1** : Générer un rapport consolidé des ventes
* **UC2** : Consulter le stock d’un magasin
* **UC3** : Visualiser les performances globales des magasins
* **UC4** : Mettre à jour les informations d’un produit

---

## Authentification & Sécurité

* Authentification via **JWT**
* Middleware de protection des routes privées
* **CORS** activé (autorise l’accès depuis `http://localhost:5173`)

---

## Documentation Swagger

Accès via : [http://localhost:8080/docs](http://localhost:8080/docs)

Chaque endpoint y est documenté avec :

* Les méthodes HTTP disponibles
* Les formats d’entrée/sortie attendus
* Les codes de réponse standardisés
* Des exemples de requêtes

---

## Accès aux services Docker

| Service     | URL                                                            |
| ----------- | -------------------------------------------------------------- |
| Backend     | [http://localhost:8080](http://localhost:8080)                 |
| Frontend    | [http://localhost:5173](http://localhost:5173)                 |
| Prometheus  | [http://localhost:9090](http://localhost:9090)                 |
| Grafana     | [http://localhost:3000](http://localhost:3000)                 |
| Swagger API | [http://localhost:8080/docs](http://localhost:8080/docs)       |
| Metrics     | [http://localhost:8080/metrics](http://localhost:8080/metrics) |

---
Voici une version améliorée et finalisée de ton `README.md` incluant une explication claire des nouvelles fonctionnalités **(Prometheus, Grafana, Nginx, multiples backends avec load balancing)** et **leur utilité** dans le système :

---

# Système POS — Labo 4 (LOG430)

Ce projet met en œuvre un système de point de vente (POS) distribué avec **observabilité**, **mise à l’échelle**, **cache Redis**, et **monitoring temps réel** à l’aide de Prometheus et Grafana.

---

## Technologies utilisées

| Composant               | Image/Port                   | Description                                                              |
| ----------------------- | ---------------------------- | ------------------------------------------------------------------------ |
| `frontend`              | Port `5173`                  | Interface utilisateur en React                                           |
| `backend1` → `backend5` | Port exposé `8000` (interne) | Instances FastAPI (5) pour la scalabilité avec Nginx comme load balancer |
| `nginx`                 | `nginx:latest`, `8080:80`    | Load balancer pour distribuer les requêtes vers les 5 backends           |
| `redis`                 | `redis:alpine`, `6379`       | Cache pour les rapports et les données de dashboard                      |
| `postgres`              | `postgres:15`, `5433:5432`   | Base de données relationnelle PostgreSQL                                 |
| `prometheus`            | `prom/prometheus`, `9090`    | Collecte de métriques des backends via `/metrics`                        |
| `grafana`               | `grafana/grafana`, `3000`    | Visualisation des métriques via dashboards interactifs                   |

---

### Observabilité (Prometheus + Grafana)

* **Prometheus** est utilisé pour **collecter des métriques** exposées par FastAPI via `/metrics`.
* **Grafana** permet de **visualiser en temps réel** ces métriques : taux d’erreur, temps de réponse, charge, etc.
* *Utile pour diagnostiquer les ralentissements, surveiller l’usage, anticiper les incidents.*

### Scalabilité avec Nginx et plusieurs backends

* Déploiement de **2 instances FastAPI (`backend1` et `backend2`)** derrière un **reverse proxy Nginx**.
* Nginx utilise le **load balancing** pour répartir les requêtes, améliorant la **résilience** et la **scalabilité**.
* *Utile pour supporter plus d’utilisateurs simultanés ou tolérer une panne d’une instance.*

### Caching avec Redis

* Les endpoints coûteux (rapports, dashboard) utilisent un **cache Redis** pour éviter les requêtes répétitives.
* Améliore significativement les **performances** et **réduit la charge** sur la base de données.
* *Utile pour améliorer le temps de réponse des requêtes fréquentes.*

## Accès à Grafana

* **URL :** [http://localhost:3000](http://localhost:3000)
* **Login par défaut :**

  * utilisateur : `admin`
  * mot de passe : `admin` (à changer)

**Configurer une datasource Prometheus :**

* URL : `http://prometheus:9090`
* Ensuite, importer un dashboard avec l'ID 11074 (FastAPI metrics par exemple).

---

## Tests

```bash
pytest
```

Inclut des tests pour l'authentification, les rôles (employé, gestionnaire, responsable), et la vérification du fonctionnement de Redis.

---

## Compléments du Labo 4

* Test de performance et de scalabilité (ex: Locust)
* Monitoring des erreurs serveur avec `/metrics`
* Cache Redis intégré aux endpoints stratégiques
* Dashboards Grafana personnalisables
