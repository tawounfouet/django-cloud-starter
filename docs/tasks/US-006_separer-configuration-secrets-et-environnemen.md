---
id: US-006
epic: EP-01
phase: R1
gate: R1.1
priority: P0
size: M
status: done
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-005.]
blocks: []
commits: [d2b3a10]
evidence: [config/settings.py, .env.example]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-006 - Séparer configuration, secrets et environnements

## Contexte

en tant que développeur, je veux distinguer réglages applicatifs et secrets pour éviter les erreurs de publication.

## Criteres d acceptation

- [x] AC-01 : `.env.example` documente les variables sans valeur sensible.
- [x] AC-02 : `DEBUG`, `SECRET_KEY`, domaines autorisés, CSRF et URL PostgreSQL utilisent une configuration appropriée à chaque environnement.
- [x] AC-03 : l'application échoue explicitement lorsqu'une configuration critique de production manque.
- [x] AC-04 : aucun secret n'est conservé dans Git.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/models.py`](../../apps/records/models.py) | creer ou modifier | Modele metier |
| [`apps/records/views.py`](../../apps/records/views.py) | creer ou modifier | Vues et permissions |
| [`config/settings.py`](../../config/settings.py) | modifier | INSTALLED_APPS et reglages |

## Exemples de code

Extrait representatif pour EP-01 :

```python
from django.db import models


class Record(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- tests de configuration et revue du dépôt.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Implementation existante | d2b3a10 |

## Notes

- Dependances : US-005.
- Tracabilite : `EF-09`, `CA-10`, `ADR-013`, `AT-09`.
