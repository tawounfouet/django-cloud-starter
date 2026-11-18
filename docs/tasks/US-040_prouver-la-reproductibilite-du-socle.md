---
id: US-040
epic: EP-06
phase: R3/R5
gate: R3/R5
priority: P1, recommandée avant réutilisation
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-017/034/038.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-040 - Prouver la reproductibilité du socle

## Contexte

pouvoir démarrer une deuxième application sans dupliquer des secrets ou données.

## Criteres d acceptation

- [ ] AC-01 : un clone neuf permet un nouveau démarrage avec configuration propre.
- [ ] AC-02 : aucun identifiant de projet Neon/Vercel n'est codé en dur dans le starter.
- [ ] AC-03 : le nouveau projet dispose de ses propres secrets et d'une base distincte.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`config/settings.py`](../../config/settings.py) | modifier | Logs et diagnostic |
| [`README.md`](../../README.md) | modifier | Procedure d exploitation |
| [`docs/specs/07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md`](../specs/07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md) | modifier | Runbook |

## Exemples de code

Extrait representatif pour EP-06 :

```python
LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- exercice de duplication documenté.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-017/034/038.
- Tracabilite : `UC-07`, `ADR-015`, `CA-01`.
