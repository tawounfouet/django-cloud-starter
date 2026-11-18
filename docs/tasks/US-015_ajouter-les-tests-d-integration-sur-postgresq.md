---
id: US-015
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: M
status: done
owner: opencode/big-pickle (agent)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-008, US-014]
blocks: []
commits: ["bbf58a8", "0c6f29d", "d85b444"]
evidence: ["2026-11-18: migrations appliquees et 25 tests verts sur PostgreSQL 17 dans GitHub Actions", "https://github.com/tawounfouet/django-cloud-starter/actions/runs/44282007106"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-015 - Ajouter les tests d'intégration sur PostgreSQL isolé

## Contexte

vérifier que les migrations et modèles Django fonctionnent sur le moteur utilisé en production.

## Criteres d acceptation

- [x] AC-01 : les tests utilisent PostgreSQL temporaire ou une branche/base Neon dédiée à la CI, jamais la production.
- [x] AC-02 : le test installe les migrations dans cet environnement.
- [x] AC-03 : le job échoue si le modèle ou la migration est incompatible.

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

- run d'intégration reproductible.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |
| 2026-11-18 | Integration PostgreSQL ajoutee au workflow | `bbf58a8` |
| 2026-11-18 | Integration PostgreSQL validee | `44282007106` |

## Notes

- Dependances : US-008, US-014 ; peut être finalisé avec US-025.
- Tracabilite : `EF-05/10`, `AT-11`, `ADR-005/007`.
