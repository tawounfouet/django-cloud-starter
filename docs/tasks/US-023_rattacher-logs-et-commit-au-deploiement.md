---
id: US-023
epic: EP-03
phase: R2
gate: R2
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-018/020.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-023 - Rattacher logs et commit au déploiement

## Contexte

retrouver rapidement la version active et comprendre un échec.

## Criteres d acceptation

- [ ] AC-01 : chaque déploiement est corrélé à un commit SHA ou identifiant de release.
- [ ] AC-02 : les logs de build et d'exécution sont consultables.
- [ ] AC-03 : un échec contrôlé est identifiable sans divulgation de secret.

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

- exemple de diagnostic sur un déploiement de test.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-018/020.
- Tracabilite : `EF-13`, `AT-12`, `ADR-018`.
