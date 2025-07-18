# Décision d'architecture : k6 pour les tests de charge

## Contexte

J'ai valider la performance et la stabilité de nos APIs avant leur mise en production. Les tests de charge doivent pouvoir être intégrés dans le pipeline CI/CD.

## Décision

J'ai choisi **k6** comme outil de test de charge et de performance.

## Justification

- Écriture des tests en JavaScript (simple et expressif)
- Résultats lisibles et exportables (JSON, InfluxDB, Grafana)
- Intégration facile avec CI/CD
- Support des scénarios complexes (VU, ramp-up, etc.)
- Léger, sans dépendances complexes

## Conséquences

- Les développeurs doivent apprendre les bases de l’écriture de scripts en k6
- Prévoir un environnement isolé pour lancer les tests sans impacter la production