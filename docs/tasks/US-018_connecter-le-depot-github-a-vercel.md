---
id: US-018
epic: EP-03
phase: R2
gate: R2
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-004, US-012, US-017.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-018 - Connecter le dépôt GitHub à Vercel

## Contexte

héberger directement le Django HTTP sans configuration héritée inutile.

## Criteres d acceptation

- [ ] AC-01 : le projet est reconnu comme Django par Vercel et la construction réussit.
- [ ] AC-02 : le point d'entrée Django est identifié et les dépendances sont installées.
- [ ] AC-03 : aucun secret n'apparaît dans les logs de build.
- [ ] AC-04 : les choix de runtime et région correspondent aux décisions R0.

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

- URL de déploiement et logs de build sans secrets.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-004, US-012, US-017.
- Tracabilite : `EF-04/08`, `AT-06`, `ADR-004/009`.
