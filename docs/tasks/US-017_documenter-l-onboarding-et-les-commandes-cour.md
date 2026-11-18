---
id: US-017
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-005/006/011.]
blocks: []
commits: []
evidence: [README present, preuve clone vierge a consigner]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-017 - Documenter l'onboarding et les commandes courantes

## Contexte

permettre à un nouvel utilisateur technique de reproduire le projet.

## Criteres d acceptation

- [ ] AC-01 : le README couvre prérequis, installation, `.env.example`, tests et lancement.
- [ ] AC-02 : les commandes sont testées depuis un clone vierge.
- [ ] AC-03 : les erreurs fréquentes et leur diagnostic sont indiqués.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | creer | Pipeline GitHub Actions |
| [`pyproject.toml`](../../pyproject.toml) | modifier | Outils et scripts |
| [`README.md`](../../README.md) | modifier | Commandes et onboarding |

## Exemples de code

Extrait representatif pour EP-02 :

```yaml
name: ci
on:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- exercice de bootstrap consigné.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-005/006/011.
- Tracabilite : `CA-01`, `AT-01`, `ADR-015`.
