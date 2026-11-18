---
id: US-044
epic: EP-07
phase: R3/R5
gate: R3/R5
priority: P1
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-040/042.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-044 - Préparer le starter pour une première réutilisation

## Contexte

transformer le démonstrateur accepté en modèle de départ réellement utile.

## Criteres d acceptation

- [ ] AC-01 : les éléments spécifiques à `Record` sont identifiés et simples à remplacer.
- [ ] AC-02 : conventions de modules, tests et configuration expliquées.
- [ ] AC-03 : l'onboarding a été éprouvé par un deuxième clone ou projet.

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

- guide de réutilisation et matrice de points personnalisables.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-040/042.
- Tracabilite : `UC-07`, `ADR-015`.
