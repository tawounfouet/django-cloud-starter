---
id: US-011
epic: EP-01
phase: R1
gate: R1.2
priority: P0
size: M
status: done
owner: opencode/big-pickle (agent)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-008, US-009, US-010]
blocks: []
commits: ["3d1bf9b"]
evidence: ["2026-11-18: check, makemigrations --check --dry-run, pytest 25 passed, ruff check", "apps/records/migrations/0001_initial.py"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/02_R1_SOCLE_LOCAL.md
---

# US-011 - Couvrir les vues et le parcours metier par les tests

## Contexte

Detecter les regressions sur la vertical slice avec des donnees generees, sans dependance aux donnees de production.

## Criteres d'acceptation

- [x] AC-01 : tests de modele, formulaire, routes, CRUD et permissions.
- [x] AC-02 : les donnees de test sont generees.
- [x] AC-03 : la suite se lance par une commande documentee.
- [x] AC-04 : les cas negatifs sont couverts.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/tests/factories.py`](../../apps/records/tests/factories.py) | creer | Genere utilisateurs et records de test. |
| [`apps/records/tests/test_models.py`](../../apps/records/tests/test_models.py) | creer | Teste le modele et les contraintes. |
| [`apps/records/tests/test_forms.py`](../../apps/records/tests/test_forms.py) | creer | Teste la validation du formulaire. |
| [`apps/records/tests/test_views.py`](../../apps/records/tests/test_views.py) | creer | Teste les routes et le CRUD. |
| [`apps/records/tests/test_permissions.py`](../../apps/records/tests/test_permissions.py) | creer | Teste les refus d'acces. |
| [`README.md`](../../README.md) | modifier | Documente `uv run pytest -q`. |

## Exemples de code

`apps/records/tests/factories.py` :

```python
from django.contrib.auth import get_user_model
from apps.records.models import Record


def create_user(username="tester", password="test-pass-123"):
    return get_user_model().objects.create_user(username=username, password=password)


def create_record(owner, **overrides):
    defaults = {"title": "Record de test", "status": "draft"}
    defaults.update(overrides)
    return Record.objects.create(created_by=owner, **defaults)
```

`apps/records/tests/test_views.py`, cas negatif minimal :

```python
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_anonymous_user_is_redirected_to_login(client):
    response = client.get(reverse("record_list"))
    assert response.status_code == 302
    assert reverse("login") in response.url
```

## Plan d'action

1. Factoriser les factories ou fixtures de test.
2. Ajouter les tests de vue et de permissions.
3. Verifier la couverture du parcours complet.
4. Documenter la commande de lancement.

## Preuves attendues

- `uv run pytest -q`
- Rapport de tests local.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche creee | ADR-019 |
| 2026-11-18 | R1.2 implemente | `3d1bf9b` |

## Notes

Cette story ferme le gate R1.2 avec US-008 a US-010.
