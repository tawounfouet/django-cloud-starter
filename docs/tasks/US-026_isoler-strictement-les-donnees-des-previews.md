---
id: US-026
epic: EP-04
phase: R3
gate: R3
priority: **P0 bloquant**
size: L, à découper si nécessaire
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-018, US-024/025, US-031.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-026 - Isoler strictement les données des Previews

## Contexte

garantir qu'un environnement de PR ne peut ni modifier ni exposer la production.

## Criteres d acceptation

- [ ] AC-01 : chaque Preview autorisée dispose d'une base/branche isolée ou d'une isolation équivalente réellement démontrée.
- [ ] AC-02 : l'URL DB de Preview ne pointe jamais vers l'environnement de production.
- [ ] AC-03 : les comptes et données de Preview sont synthétiques et sans données personnelles réelles.
- [ ] AC-04 : un test négatif avec sentinelles distinctes prouve l'absence d'écriture en production.
- [ ] AC-05 : les créations/suppressions de branches, expirations et droits sont maîtrisés.
- [ ] AC-06 : une branche Neon issue d'une branche contenant des données de production est interdite par défaut : le branching peut copier des données et doit être revu du point de vue confidentialité.

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

- rapport de tests d'isolation et configuration expurgée.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-018, US-024/025, US-031.
- Tracabilite : `CA-08`, `AT-05`, `OA-07`, `ADR-006`.
