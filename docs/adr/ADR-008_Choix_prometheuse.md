# Décision d'architecture : Prometheus pour la collecte des métriques

## Contexte

J'ai besoin de collecter des métriques applicatives et système pour analyser la performance, détecter les anomalies, et alimenter nos outils de visualisation.

## Décision

J'ai choisi **Prometheus** comme système principal de collecte de métriques.

## Justification

- Pull-based model simple et efficace
- Support natif de Kubernetes (service discovery)
- Langage PromQL puissant pour les requêtes
- Intégration directe avec Grafana
- Alertmanager pour les notifications

## Conséquences

- Nécessite l’instrumentation des services (exporters, libraries)
- Stockage limité dans le temps (nécessite un long terme comme Thanos si besoin)