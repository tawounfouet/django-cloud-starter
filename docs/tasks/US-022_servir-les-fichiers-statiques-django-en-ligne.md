---
id: US-022
epic: EP-03
phase: R2
gate: R2
priority: P0
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-007, US-018.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-022 - Servir les fichiers statiques Django en ligne

## Contexte

obtenir une interface HTML/CSS complète lors du déploiement.

## Criteres d acceptation

- [ ] AC-01 : `collectstatic` est exécuté dans le cadre du build configuré pour Django.
- [ ] AC-02 : `STATIC_ROOT`, chemins et comportement des assets sont compatibles avec Vercel.
- [ ] AC-03 : le CSS s'affiche sur Production et Preview sans dépendre d'un stockage local persistant.

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

- requêtes HTTP sur les statiques, rendu visuel.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-007, US-018.
- Tracabilite : `AT-08`, `ADR-010`.
