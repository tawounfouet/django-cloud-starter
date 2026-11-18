---
id: US-036
epic: EP-06
phase: R3/R5
gate: R3/R5
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-023, US-025.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-036 - Rendre l'application diagnostiquable

## Contexte

comprendre les échecs applicatifs à partir d'une version et de journaux exploitables.

## Criteres d acceptation

- [ ] AC-01 : erreurs applicatives avec niveau, contexte utile et identifiant de déploiement lorsque disponible.
- [ ] AC-02 : logs sans mots de passe, tokens, URLs DB complètes ou données sensibles.
- [ ] AC-03 : une panne simulée est localisée et interprétée.

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

- procédure de diagnostic et exemple expurgé.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-023, US-025.
- Tracabilite : `CA-12`, `AT-12`, `EF-13`.
