---
id: US-032
epic: EP-05
phase: R1/R3
gate: R1/R3
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-006, US-018.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-032 - Durcir les réglages Django en production

## Contexte

réduire les vulnérabilités courantes d'une application Django accessible sur Internet.

## Criteres d acceptation

- [ ] AC-01 : `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, cookies et redirections HTTPS sont adaptés aux domaines effectivement utilisés.
- [ ] AC-02 : `python manage.py check --deploy` et les tests pertinents sont exécutés et analysés.
- [ ] AC-03 : les erreurs publiques n'exposent pas de secrets ou de tracebacks sensibles.

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

- rapport de contrôle sécurité.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-006, US-018.
- Tracabilite : `CA-09/10`, `ADR-008`, `AT-09/10`.
