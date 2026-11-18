---
id: US-014
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-011]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-014 - Configurer GitHub Actions pour les pull requests

## Contexte

lancer automatiquement lint, tests et contrôles de sécurité lors d'une PR.

## Criteres d acceptation

- [ ] AC-01 : ouverture et modification d'une PR déclenchent la CI.
- [ ] AC-02 : les statuts réussis/échoués sont visibles dans la PR.
- [ ] AC-03 : la CI n'utilise aucune base de production ni secret de production.
- [ ] AC-04 : le workflow applique les permissions minimales nécessaires et maîtrise l'exécution de code non fiable.

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

- deux exécutions contrôlées, succès et échec.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-011 à US-013.
- Tracabilite : `EF-03`, `CA-05`, `AT-03`, `ADR-003`.
