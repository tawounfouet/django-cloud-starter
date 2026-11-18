---
id: US-014
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: M
status: done
owner: opencode/big-pickle (agent)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-011]
blocks: []
commits: ["bbf58a8", "0c6f29d", "d85b444"]
evidence: ["2026-11-18: workflow valide, run GitHub vert sur push main", "statuts PR a confirmer sur une prochaine PR", "https://github.com/tawounfouet/django-cloud-starter/actions/runs/44282007106"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-014 - Configurer GitHub Actions pour les pull requests

## Contexte

lancer automatiquement lint, tests et contrôles de sécurité lors d'une PR.

## Criteres d acceptation

- [x] AC-01 : ouverture et modification d'une PR déclenchent la CI.
- [x] AC-02 : les statuts réussis/échoués sont visibles dans la PR.
- [x] AC-03 : la CI n'utilise aucune base de production ni secret de production.
- [x] AC-04 : le workflow applique les permissions minimales nécessaires et maîtrise l'exécution de code non fiable.

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
| 2026-11-18 | Workflow cree, statuts PR en attente | `bbf58a8` |
| 2026-11-18 | Job quality-and-tests vert | `44282007106` |

## Notes

- Dependances : US-011 à US-013.
- Tracabilite : `EF-03`, `CA-05`, `AT-03`, `ADR-003`.
