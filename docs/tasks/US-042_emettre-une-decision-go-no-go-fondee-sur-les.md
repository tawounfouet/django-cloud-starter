---
id: US-042
epic: EP-07
phase: R3/R5
gate: R3/R5
priority: P0
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-041.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-042 - Émettre une décision GO / NO-GO fondée sur les preuves

## Contexte

éviter de qualifier le socle de prêt sur la seule base d'une page web en ligne.

## Criteres d acceptation

- [ ] AC-01 : les treize critères CA sont examinés.
- [ ] AC-02 : les risques critiques de secrets, production/preview et migration ont un statut explicite.
- [ ] AC-03 : un `NO-GO` est prononcé si une condition bloquante n'est pas remplie.
- [ ] AC-04 : toute dérogation est signée par le responsable et ne contourne pas une mesure de sécurité obligatoire.

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

- procès-verbal GO / NO-GO.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-041.
- Tracabilite : `ADR-018`, `CA-01` à `CA-13`.
