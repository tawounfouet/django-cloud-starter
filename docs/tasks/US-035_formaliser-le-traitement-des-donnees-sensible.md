---
id: US-035
epic: EP-05
phase: R1/R3
gate: R1/R3
priority: P0 pour données réelles
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-004, US-026/031.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-035 - Formaliser le traitement des données sensibles

## Contexte

empêcher le transfert involontaire de données personnelles ou financières vers des environnements non autorisés.

## Criteres d acceptation

- [ ] AC-01 : une politique explicite interdit l'usage de données réelles en Preview/CI sans revue et accord.
- [ ] AC-02 : la visibilité des URLs Preview et des journaux est prise en compte.
- [ ] AC-03 : toute évolution vers une application métier contenant des données sensibles déclenche une revue spécifique de résidence, rétention, habilitations, sauvegardes et obligations applicables.

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

- politique des données et checklist de revue.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-004, US-026/031.
- Tracabilite : `OA-07`, `ADR-006/017`, `ENF-07`.
