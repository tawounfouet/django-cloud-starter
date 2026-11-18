---
id: US-029
epic: EP-04
phase: R3
gate: R3
priority: P0 pour restaurabilité minimale
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-024/027.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-029 - Tester sauvegarde, restauration et limites du service

## Contexte

ne pas supposer qu'une sauvegarde ou un point de restauration est utilisable sans exercice.

## Criteres d acceptation

- [ ] AC-01 : capacités réelles de restauration Neon et limites du plan documentées.
- [ ] AC-02 : une restauration est exercée sur un environnement non productif lorsque le plan le permet.
- [ ] AC-03 : les limites de récupération (fenêtre, perte de données possible, rôle, responsabilités) sont consignées.
- [ ] AC-04 : aucun exercice destructeur n'est déclenché sur Production.

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

- compte rendu d'exercice et runbook.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-024/027.
- Tracabilite : `OA-11`, `ENF-03`, `ADR-005`, `AT-13`.
