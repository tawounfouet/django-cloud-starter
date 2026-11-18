---
id: US-020
epic: EP-03
phase: R2
gate: R2
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-014/016/018.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-020 - Déclencher le déploiement de production sur `main`

## Contexte

publier une modification validée sans étape manuelle d'hébergement.

## Criteres d acceptation

- [ ] AC-01 : une fusion éligible sur `main` produit un nouveau déploiement.
- [ ] AC-02 : la version déployée correspond au commit intégré.
- [ ] AC-03 : les tests bloquants de PR sont terminés avant fusion ; les contrôles de déploiement additionnels sont configurés si nécessaires et disponibles.
- [ ] AC-04 : un nouveau déploiement ne déclenche pas automatiquement une migration de production pendant le build.

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

- PR fusionnée, SHA et journal Vercel correspondant.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-014/016/018.
- Tracabilite : `EF-04`, `CA-07`, `AT-06`, `ADR-003/004/007`.
