---
id: US-024
epic: EP-04
phase: R3
gate: R3
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-004/006.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-024 - Préparer le projet Neon et ses accès

## Contexte

disposer d'une base PostgreSQL managée indépendante des instances Django.

## Criteres d acceptation

- [ ] AC-01 : projet, base, région et rôles d'accès sont définis.
- [ ] AC-02 : secrets et URL de connexion ne sont pas présents dans Git.
- [ ] AC-03 : un accès de production est distinct des accès CI/Preview.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/migrations/`](../../apps/records/migrations/) | creer ou modifier | Migrations versionnees |
| [`config/settings.py`](../../config/settings.py) | modifier | DATABASE_URL et TLS |
| [`docs/specs/05_STRATEGIE_DONNEES_ET_MIGRATIONS.md`](../specs/05_STRATEGIE_DONNEES_ET_MIGRATIONS.md) | modifier | Strategie de donnees |

## Exemples de code

Extrait representatif pour EP-04 :

```python
DATABASES = {
    "default": dj_database_url.parse(
        os.environ["DATABASE_URL"], ssl_require=True
    )
}
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- fiche de configuration expurgée et test de connexion.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-004/006.
- Tracabilite : `EF-05/09`, `ADR-005/017`.
