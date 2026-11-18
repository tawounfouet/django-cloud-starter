---
id: US-019
epic: EP-03
phase: R2
gate: R2
priority: P0
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-018, US-010, US-032.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-019 - Fournir une URL HTTPS de production

## Contexte

donner accès publiquement à l'application via une URL Vercel.

## Criteres d acceptation

- [ ] AC-01 : la page d'accueil répond en HTTPS.
- [ ] AC-02 : l'environnement Production fonctionne avec `DEBUG=False` et une politique de domaines cohérente.
- [ ] AC-03 : la page Admin ne contourne pas l'authentification.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`vercel.json`](../../vercel.json) | creer ou modifier | Configuration Vercel |
| [`config/settings.py`](../../config/settings.py) | modifier | Reglages de production |
| [`README.md`](../../README.md) | modifier | URLs et deploiement |

## Exemples de code

Extrait representatif pour EP-03 :

```json
{
  "builds": [
    { "src": "config/wsgi.py", "use": "@vercel/python" }
  ]
}
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- requêtes HTTP et tests de sécurité sur URL de production.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-018, US-010, US-032.
- Tracabilite : `CA-02/09`, `AT-02/10`, `ADR-004`.
