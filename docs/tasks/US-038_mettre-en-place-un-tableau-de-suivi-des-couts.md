---
id: US-038
epic: EP-06
phase: R3/R5
gate: R3/R5
priority: P0 pour choix de plan, P1 pour suivi approfondi
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-004, US-018/024.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-038 - Mettre en place un tableau de suivi des coûts et quotas

## Contexte

éviter un coût imprévu ou un blocage de quota.

## Criteres d acceptation

- [ ] AC-01 : plans réellement activés et principaux quotas de Vercel, Neon et Cloudflare sont consignés.
- [ ] AC-02 : le responsable sait où consulter usage et facturation.
- [ ] AC-03 : les seuils, alertes ou contrôles manuels pertinents sont définis selon les possibilités des offres.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`config/settings.py`](../../config/settings.py) | modifier | Logs et diagnostic |
| [`README.md`](../../README.md) | modifier | Procedure d exploitation |
| [`docs/specs/07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md`](../specs/07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md) | modifier | Runbook |

## Exemples de code

Extrait representatif pour EP-06 :

```python
LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- registre de suivi mis à jour.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-004, US-018/024.
- Tracabilite : `CA-13`, `AT-14/15`, `OA-10`.
