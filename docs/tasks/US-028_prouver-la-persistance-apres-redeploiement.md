---
id: US-028
epic: EP-04
phase: R3
gate: R3
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-020, US-025, US-027.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-028 - Prouver la persistance après redéploiement

## Contexte

vérifier que le déploiement d'une nouvelle version n'efface pas les données utilisateur.

## Criteres d acceptation

- [ ] AC-01 : un `Record` est créé en Production dans Neon.
- [ ] AC-02 : un changement de code sans migration destructive est publié.
- [ ] AC-03 : le même identifiant et les mêmes valeurs sont retrouvés après publication.
- [ ] AC-04 : le test vérifie également la non-utilisation d'un fichier SQLite local en production.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/migrations/`](../../apps/records/migrations/) | creer ou modifier | Migrations versionnees |
| [`config/settings.py`](../../config/settings.py) | modifier | DATABASE_URL et TLS |
| [`docs/specs/05_STRATEGIE_DONNEES_ET_MIGRATIONS.md`](../specs/05_STRATEGIE_DONNEES_ET_MIGRATIONS.md) | modifier | Strategie de donnees |

## Exemples de code

Extrait representatif pour EP-04 :

```python
DATABASES = {"default": dj_database_url.parse(os.environ["DATABASE_URL"], ssl_require=True)}
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- journal E2E avant/après et identifiant expurgé.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-020, US-025, US-027.
- Tracabilite : `CA-03/04`, `AT-07`, `ADR-005`.
