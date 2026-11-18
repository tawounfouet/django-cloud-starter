---
id: US-030
epic: EP-04
phase: R3
gate: R3
priority: P1, promu P0 si instabilité
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-025, US-036.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-030 - Vérifier connexions, pooling et comportement serverless

## Contexte

éviter un épuisement des connexions à PostgreSQL et maîtriser les requêtes.

## Criteres d acceptation

- [ ] AC-01 : nombre de connexions, latence et erreurs sont examinés sur une charge de démonstration.
- [ ] AC-02 : stratégie URL poolée / directe et paramètres Django sont justifiés par l'usage.
- [ ] AC-03 : aucun secret de connexion n'est affiché dans les rapports.

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

- compte rendu de mesure simple.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-025, US-036.
- Tracabilite : `ENF-05`, `ADR-005`.
