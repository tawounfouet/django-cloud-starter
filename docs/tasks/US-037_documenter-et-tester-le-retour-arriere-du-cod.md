---
id: US-037
epic: EP-06
phase: R3/R5
gate: R3/R5
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-020/023/027.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-037 - Documenter et tester le retour arrière du code

## Contexte

revenir à une version applicative fonctionnelle après une mauvaise release.

## Criteres d acceptation

- [ ] AC-01 : procédure de rollback Vercel décrite pour le plan et les mécanismes disponibles.
- [ ] AC-02 : un incident non destructif est simulé sur une version de test.
- [ ] AC-03 : le document distingue rollback du code et restauration / compatibilité du schéma PostgreSQL.
- [ ] AC-04 : critères d'escalade et vérifications après reprise définis.

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

- exercice de rollback et runbook.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-020/023/027.
- Tracabilite : `CA-12`, `AT-13`, `EF-14`, `ADR-007`.
