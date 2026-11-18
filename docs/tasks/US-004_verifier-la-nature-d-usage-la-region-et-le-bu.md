---
id: US-004
epic: EP-00
phase: R0
gate: R0
priority: P0
size: M
status: done
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: []
blocks: []
commits: [77afb64]
evidence: [docs/specs/00, docs/specs/01]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-004 - Vérifier la nature d'usage, la région et le budget

## Contexte

en tant que responsable, je veux choisir des services et un plan conformes à l'usage et aux contraintes de données.

## Criteres d acceptation

- [x] AC-01 : usage personnel, expérimental ou commercial confirmé.
- [x] AC-02 : le plan Vercel retenu autorise cet usage ; l'offre Hobby n'est pas supposée compatible avec un produit commercial.
- [x] AC-03 : les régions applicative et PostgreSQL sont sélectionnées avec justification de latence/résidence des données.
- [x] AC-04 : coûts et seuils de surveillance initiaux sont consignés.

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
- Tracabilite : `CA-13`, `AT-14`, `AT-15`, `OA-01`, `OA-06`, `OA-10`, `ADR-016/017`.
