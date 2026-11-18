---
id: US-005
epic: EP-01
phase: R1
gate: R1.1
priority: P0
size: M
status: done
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-002.]
blocks: []
commits: [d2b3a10]
evidence: [manage.py, config/, apps/core/]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-005 - Initialiser un projet Django modulaire

## Contexte

en tant que développeur, je veux un squelette Django ordonné pour ajouter des modules sans restructuration immédiate.

## Criteres d acceptation

- [x] AC-01 : `manage.py`, `config/`, `apps/`, `templates/`, `static/` et `tests/` sont présents.
- [x] AC-02 : un environnement propre installe les dépendances verrouillées et lance Django.
- [x] AC-03 : aucune connexion à une base de production n'est nécessaire au simple démarrage local.

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

- commande d'installation et `runserver` reproductibles.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Implementation existante | d2b3a10 |

## Notes

- Dependances : US-002.
- Tracabilite : `CA-01`, `AT-01`, `ADR-001/013`.
