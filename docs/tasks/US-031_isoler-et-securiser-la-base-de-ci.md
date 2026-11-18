---
id: US-031
epic: EP-04
phase: R3
gate: R3
priority: P0
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-014/015, US-024.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-031 - Isoler et sécuriser la base de CI

## Contexte

garantir que les jobs CI exécutent les tests et migrations sans droits sur Production.

## Criteres d acceptation

- [ ] AC-01 : la CI utilise PostgreSQL éphémère ou une base dédiée.
- [ ] AC-02 : les credentials CI ne permettent pas l'accès en écriture à la base de production.
- [ ] AC-03 : les jobs ne consomment pas de données réelles sans justification explicite.

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

- test de séparation et revue des permissions.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-014/015, US-024.
- Tracabilite : `CA-08`, `AT-05`, `ADR-006`.
