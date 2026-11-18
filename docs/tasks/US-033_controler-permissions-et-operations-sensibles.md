---
id: US-033
epic: EP-05
phase: R1/R3
gate: R1/R3
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-009/010.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-033 - Contrôler permissions et opérations sensibles

## Contexte

limiter chaque action CRUD aux profils autorisés.

## Criteres d acceptation

- [ ] AC-01 : un utilisateur anonyme ne peut pas exécuter d'opération interdite.
- [ ] AC-02 : un utilisateur authentifié sans permission ne peut pas lire ou modifier des données hors de son périmètre.
- [ ] AC-03 : les contrôles sont effectués côté serveur et non seulement dans les templates.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`config/settings.py`](../../config/settings.py) | modifier | Reglages de securite |
| [`.env.example`](../../.env.example) | modifier | Variables sans secret |
| [`apps/records/views.py`](../../apps/records/views.py) | modifier | Contrroles d acces |

## Exemples de code

Extrait representatif pour EP-05 :

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- tests d'autorisation positifs et négatifs.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-009/010.
- Tracabilite : `CA-09`, `EF-07`, `ADR-008`.
