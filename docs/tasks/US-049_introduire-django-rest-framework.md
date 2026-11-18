---
id: US-049
epic: EP-09
phase: R5
gate: R5
priority: P2
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: []
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-049 - Introduire Django REST Framework

## Contexte

Voir le backlog pour le besoin detaille.

## Criteres d acceptation

- [ ] AC-01 : ressources et contrats API définis ; authentification et permissions testées.
- [ ] AC-02 : réutilisation de la logique métier existante, sans duplication.
- [ ] AC-03 : aucune API publique ajoutée sans usage démontré.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/api/`](../../apps/api/) | creer | API optionnelle |
| [`frontend/`](../../frontend/) | creer | Frontend separe |
| [`pyproject.toml`](../../pyproject.toml) | modifier | Dependances optionnelles |

## Exemples de code

Extrait representatif pour EP-09 :

```python
from rest_framework import serializers


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ["id", "title", "status"]
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- contrat OpenAPI ou équivalent et tests.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : aucune
- Tracabilite : `EF-18`, `OA-12`.
