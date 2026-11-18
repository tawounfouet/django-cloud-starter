---
id: US-007
epic: EP-01
phase: R1
gate: R1.1
priority: P0
size: S
status: done
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-005.]
blocks: []
commits: [d2b3a10]
evidence: [templates/core/home.html, static/css/app.css]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-007 - Construire la page publique et les statiques

## Contexte

en tant que visiteur, je veux accéder à une page web présentant l'application.

## Criteres d acceptation

- [x] AC-01 : une URL publique affiche un template Django.
- [x] AC-02 : les fichiers CSS et les autres ressources statiques se chargent en local.
- [x] AC-03 : les templates ne révèlent pas de configuration sensible.

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

- test HTTP et rendu visuel.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Implementation existante | d2b3a10 |

## Notes

- Dependances : US-005.
- Tracabilite : `EF-01`, `AT-02/08`, `ADR-002/010`.
