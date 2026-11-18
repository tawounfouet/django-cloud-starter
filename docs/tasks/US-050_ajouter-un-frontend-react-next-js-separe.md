---
id: US-050
epic: EP-09
phase: R5
gate: R5
priority: P2
size: L
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

# US-050 - Ajouter un frontend React / Next.js séparé

## Contexte

Voir le backlog pour le besoin detaille.

## Criteres d acceptation

- [ ] AC-01 : justification du frontend distinct.
- [ ] AC-02 : stratégie CORS, cookies, authentification et contrats API explicitée.
- [ ] AC-03 : choix mono-repo ou multi-repo formalisé.

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

- ADR et premier parcours fonctionnel.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : aucune
- Tracabilite : `ADR-002`, `OA-12`.
