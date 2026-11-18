---
id: US-016
epic: EP-02
phase: R1/R2
gate: R1/R2
priority: P0
size: M
status: todo
owner: tawounfouet (humain)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-003, US-014.]
blocks: []
commits: ["bbf58a8"]
evidence: ["2026-11-18: check quality-and-tests documente dans README.md", "regle de fusion a appliquer dans GitHub"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-016 - Rendre la fusion conditionnelle aux contrôles

## Contexte

réduire la probabilité d'un déploiement automatique d'une modification invalide.

## Criteres d acceptation

- [x] AC-01 : la politique de fusion inclut revue adaptée et vérifications requises selon les capacités du dépôt.
- [ ] AC-02 : un changement avec CI rouge n'est pas fusionné via le parcours normal.
- [x] AC-03 : si les règles natives sont indisponibles, l'écart et la mesure de mitigation sont documentés ; le risque est arbitré avant GO.

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

- essai de PR non conforme et capture/règle GitHub.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |
| 2026-11-18 | Politique documentee, regle GitHub en attente | `bbf58a8` |

## Notes

- Dependances : US-003, US-014.
- Tracabilite : `CA-06`, `ADR-003`, `AT-03`.
