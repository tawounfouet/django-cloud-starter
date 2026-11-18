---
id: US-008
epic: EP-01
phase: R1
gate: R1.2
priority: P0
size: M
status: done
owner: opencode/big-pickle (agent)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-001, US-005]
blocks: [US-009, US-010, US-011]
commits: ["3d1bf9b"]
evidence: ["2026-11-18: check, makemigrations --check --dry-run, pytest 25 passed, ruff check", "apps/records/migrations/0001_initial.py"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/02_R1_SOCLE_LOCAL.md
---

# US-008 - Implementer le modele Record et ses migrations

## Contexte

Fournir un modele metier minimal pour demontrer l'ORM Django, les migrations versionnees et les contraintes de donnees, sans dependance a un service externe.

## Criteres d'acceptation

- [x] AC-01 : `Record` possede `title`, `description`, `status`, `created_by`, `created_at` et `updated_at`.
- [x] AC-02 : les validations et contraintes sont testees.
- [x] AC-03 : les migrations sont generees et versionnees.
- [x] AC-04 : aucune donnee reelle n'est importee.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/__init__.py`](../../apps/records/__init__.py) | creer | Declare le package Python. |
| [`apps/records/apps.py`](../../apps/records/apps.py) | creer | Configure `RecordsConfig`. |
| [`apps/records/models.py`](../../apps/records/models.py) | creer | Definit le modele `Record`. |
| [`apps/records/migrations/0001_initial.py`](../../apps/records/migrations/0001_initial.py) | generer | Versionne le schema initial. |
| [`apps/records/tests/test_models.py`](../../apps/records/tests/test_models.py) | creer | Teste les contraintes et `__str__`. |
| [`config/settings.py`](../../config/settings.py) | modifier | Ajoute `apps.records` a `INSTALLED_APPS`, voir lignes 68 a 76. |

## Exemples de code

`apps/records/apps.py` :

```python
from django.apps import AppConfig


class RecordsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.records"
```

`apps/records/models.py` :

```python
from django.conf import settings
from django.db import models


class Record(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="records",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
```

`config/settings.py`, ajout dans `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    # ... apps existantes
    "apps.core",
    "apps.records",
]
```

## Plan d'action

1. Creer l'application `apps.records` avec le label `records`.
2. Definir le modele, les contraintes et le `__str__`.
3. Generer la migration initiale.
4. Ajouter les tests de modele.

## Preuves attendues

- `uv run python manage.py makemigrations --check --dry-run`
- `uv run pytest -q apps/records`
- Liste des migrations versionnees.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche creee | ADR-019 |
| 2026-11-18 | R1.2 implemente | `3d1bf9b` |

## Notes

Voir la section 6 du plan R1.2 pour les commandes de controle et le gate associe.
