# Décision d'architecture : KrakenD comme API Gateway

## Contexte

Mon architecture microservices nécessite une passerelle API capable d’agréger plusieurs services backend, de transformer des réponses JSON, de sécuriser les accès, et de simplifier l’exposition vers le frontend.

## Décision

J'ai choisi **KrakenD** comme API Gateway.

## Justification

- Haute performance, compilée (Go), pas de runtime
- Agrégation de services et transformation de réponses
- Configuration déclarative (fichiers JSON ou YAML)
- Plugins pour auth, quotas, validation de schéma, etc.
- Faible latence comparée à des alternatives Node.js

## Conséquences

- La complexité de configuration initiale peut être élevée
- Les erreurs de transformation ou d’agrégation peuvent être difficiles à diagnostiquer sans bons logs