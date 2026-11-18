---
id: US-041
epic: EP-07
phase: R3/R5
gate: R3/R5
priority: P0
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

# US-041 - Exécuter la campagne de recette MVP

## Contexte

démontrer tous les critères `CA-01` à `CA-13` avant l'acceptation.

## Criteres d acceptation

- [ ] AC-01 : chaque `CA` dispose d'un statut `Pass`, `Fail`, `Blocked` ou `Not tested`.
- [ ] AC-02 : une preuve datée et un environnement sont associés à chaque succès.
- [ ] AC-03 : les anomalies et risques résiduels sont enregistrés.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`docs/specs/06_STRATEGIE_TESTS_ET_ACCEPTATION.md`](../specs/06_STRATEGIE_TESTS_ET_ACCEPTATION.md) | modifier | Campagne de recette |
| [`docs/specs/07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md`](../specs/07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md) | modifier | Exploitation |
| [`README.md`](../../README.md) | modifier | Reutilisation du starter |

## Exemples de code

Extrait representatif pour EP-07 :

```markdown
- [ ] Preuves de recette
- [ ] Decision GO / NO-GO
- [ ] Runbook a jour
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- matrice de recette complétée.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : epics EP-00 à EP-06, suivant les critères concernés.
- Tracabilite : `ADR-018`, `CA-01` à `CA-13`, `AT-01` à `AT-15`.
