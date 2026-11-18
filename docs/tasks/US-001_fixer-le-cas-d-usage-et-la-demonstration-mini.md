---
id: US-001
epic: EP-00
phase: R0
gate: R0
priority: P0
size: S
status: done
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: []
blocks: []
commits: [77afb64]
evidence: [docs/specs/00, docs/specs/02]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-001 - Fixer le cas d'usage et la démonstration minimale

## Contexte

en tant que responsable du projet, je veux définir un scénario CRUD minimal pour démontrer concrètement le socle.

## Criteres d acceptation

- [x] AC-01 : le modèle de démonstration, les rôles et les quatre opérations CRUD sont décrits.
- [x] AC-02 : les données utilisées dans les tests et les previews sont synthétiques.
- [x] AC-03 : le périmètre exclut clairement le développement d'un produit métier complet.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`docs/specs/00_DJANGO_GITHUB_VERCEL_NEON_CLOUDFLARE_EXPRESSION_DU_BESOIN.md`](../specs/00_DJANGO_GITHUB_VERCEL_NEON_CLOUDFLARE_EXPRESSION_DU_BESOIN.md) | modifier | Contexte metier |
| [`docs/specs/01_ARCHITECTURE_ET_DECISIONS.md`](../specs/01_ARCHITECTURE_ET_DECISIONS.md) | modifier | ADR associes |
| [`docs/specs/02_BACKLOG_ET_USER_STORIES.md`](../specs/02_BACKLOG_ET_USER_STORIES.md) | modifier | Criteres d acceptation |

## Exemples de code

Extrait representatif pour EP-00 :

```markdown
| Decision | Statut |
|---|---|
| ADR-001 | retenue |
| ADR-019 | experimentation |
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- Voir les elements `evidence` du frontmatter et le commit du journal.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Implementation existante | 77afb64 |

## Notes

- Dependances : aucune
- Tracabilite : `DEC-01`, `OA-04`, `EF-06`, `AT-02`.
