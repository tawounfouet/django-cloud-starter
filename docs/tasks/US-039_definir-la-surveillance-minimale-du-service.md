---
id: US-039
epic: EP-06
phase: R3/R5
gate: R3/R5
priority: P1
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-036.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-039 - Définir la surveillance minimale du service

## Contexte

détecter une anomalie avant que l'usage ne devienne critique.

## Criteres d acceptation

- [ ] AC-01 : parcours de vérification de santé public sans fuite de secrets.
- [ ] AC-02 : erreurs, taux d'échec des déploiements et métriques élémentaires sont identifiés.
- [ ] AC-03 : alertes ajoutées uniquement si des événements utiles et leur destinataire sont définis.

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

- tableau d'observation et test d'alerte si retenue.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-036.
- Tracabilite : `ENF-06`, `ADR-018`.
