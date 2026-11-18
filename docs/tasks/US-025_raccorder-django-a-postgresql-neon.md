---
id: US-025
epic: EP-04
phase: R3
gate: R3
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-008, US-024.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-025 - Raccorder Django à PostgreSQL Neon

## Contexte

remplacer la persistance de démonstration locale par un stockage PostgreSQL réel.

## Criteres d acceptation

- [ ] AC-01 : Django utilise une `DATABASE_URL` appropriée à l'environnement.
- [ ] AC-02 : TLS, droits de connexion et éventuel pooling sont configurés conformément au fournisseur et au client Django.
- [ ] AC-03 : le modèle `Record` fonctionne après application contrôlée des migrations.

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

- lecture/écriture sur base dédiée, sans exposer l'URL.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-008, US-024.
- Tracabilite : `CA-03`, `AT-07`, `ADR-005`.
