---
id: US-012
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: S
status: done
owner: tawounfouet (humain)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-003, US-005/006.]
blocks: []
commits: ["58e4447", "0c6f29d", "d85b444"]
evidence: ["2026-11-18: push main effectue, run CI vert `44282007106`", "https://github.com/tawounfouet/django-cloud-starter/actions/runs/44282007106"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-012 - Publier le projet dans le dépôt GitHub choisi

## Contexte

disposer d'une source de vérité et d'un historique contrôlé.

## Criteres d acceptation

- [x] AC-01 : dépôt initialisé sur la branche déterminée, contenu cohérent et `.gitignore` correct.
- [x] AC-02 : aucun `.env` sensible, identifiant ou clé d'accès n'est versionné.
- [x] AC-03 : README, licence si applicable et conventions de contribution sont visibles.

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

- dépôt et commit initial.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |
| 2026-11-18 | Implementation locale, push en attente | `bbf58a8` |
| 2026-11-18 | Publication validee | `44282007106` |

## Notes

- Dependances : US-003, US-005/006.
- Tracabilite : `EF-02/09`, `ADR-003`, `CA-10`.
