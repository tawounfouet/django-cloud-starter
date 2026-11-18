---
id: US-013
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: M
status: done
owner: opencode/big-pickle (agent)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-002, US-012.]
blocks: []
commits: ["bbf58a8", "0c6f29d", "d85b444"]
evidence: ["2026-11-18: ruff, format, lock et hygiene verts sur GitHub", "defauts volontaires rouges en local", "https://github.com/tawounfouet/django-cloud-starter/actions/runs/44282007106"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-013 - Établir les contrôles statiques et de dépendances

## Contexte

détecter les problèmes de format, lint, configuration et dépendances avant fusion.

## Criteres d acceptation

- [x] AC-01 : commandes de vérification documentées, avec versions figées.
- [x] AC-02 : un défaut volontaire fait échouer le job concerné.
- [x] AC-03 : un scan des secrets et des fichiers interdits est présent.

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

- run CI positif et run de défaut contrôlé.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |
| 2026-11-18 | Controles locaux et hygiene ajoutes au workflow | `bbf58a8` |
| 2026-11-18 | Run CI vert | `44282007106` |

## Notes

- Dependances : US-002, US-012.
- Tracabilite : `ENF-02/04`, `CA-05/10`, `ADR-013`.
