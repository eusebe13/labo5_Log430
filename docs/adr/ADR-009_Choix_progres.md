# Décision d'architecture : PostgreSQL comme base de données relationnelle

## Contexte

mon application a besoin d’une base de données relationnelle robuste, avec support avancé du SQL, gestion de la concurrence, sécurité et extension possible.

## Décision

J'ai choisi **PostgreSQL** comme moteur de base de données principal.

## Justification

- Open-source, robuste, très largement utilisé
- Compatible ACID et transactions fiables
- Support des types JSON, recherche textuelle, extensions comme PostGIS
- Outils de sauvegarde/restauration intégrés
- Intégration facile avec les ORM (SQLAlchemy)

## Conséquences

- Requiert une gestion active des migrations et versions de schéma
- Les performances doivent être monitorées (indexation, requêtes lentes)
