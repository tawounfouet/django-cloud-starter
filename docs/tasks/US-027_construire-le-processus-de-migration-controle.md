---
id: US-027
epic: EP-04
phase: R3
gate: R3
priority: **P0 bloquant**
size: L, à découper
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-015, US-025/026.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-027 - Construire le processus de migration contrôlée

## Contexte

faire évoluer le schéma sans migration destructrice ni exécution depuis les fonctions web.

## Criteres d acceptation

- [ ] AC-01 : les migrations Django sont versionnées et testées sur une base isolée.
- [ ] AC-02 : aucune migration de production n'est exécutée dans `build`, `collectstatic`, une importation, ou au démarrage d'une instance web.
- [ ] AC-03 : la migration de production fait partie d'une étape de release explicite, autorisée et journalisée.
- [ ] AC-04 : les changements incompatibles suivent si nécessaire une stratégie `expand -> migrate -> contract`.
- [ ] AC-05 : le traitement d'un échec et le plan de reprise des données sont documentés ; un rollback du code n'est pas réputé annuler automatiquement une migration.

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

- rapport de migration non productive et procédure de release.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-015, US-025/026.
- Tracabilite : `EF-10`, `CA-11`, `AT-11`, `ADR-007`.
