---
id: US-045
epic: EP-08
phase: R4
gate: R4
priority: P2
size: S
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: []
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-045 - Associer un domaine via Cloudflare DNS

## Contexte

Voir le backlog pour le besoin detaille.

## Criteres d acceptation

- [ ] AC-01 : le domaine est ajouté dans Vercel et les entrées DNS sont configurées conformément à Vercel.
- [ ] AC-02 : Cloudflare est initialement en mode DNS-only pour les entrées concernées.
- [ ] AC-03 : résolution DNS et certificat HTTPS validés.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`vercel.json`](../../vercel.json) | modifier | Regles DNS et proxy |
| [`config/settings.py`](../../config/settings.py) | modifier | Reglages conditionnels |
| [`docs/specs/08_OPTIONS_CLOUDFLARE_ET_EVOLUTIONS.md`](../specs/08_OPTIONS_CLOUDFLARE_ET_EVOLUTIONS.md) | modifier | Options Cloudflare |

## Exemples de code

Extrait representatif pour EP-08 :

```text
Type: CNAME
Name: exemple
Value: cname.vercel-dns.com
Proxy: DNS only
```

## Plan d action

1. Lire le backlog, le plan associe et les dependances.
2. Implementer les criteres d acceptation.
3. Ajouter ou verifier les preuves.
4. Mettre a jour `TODO.md` et `CHANGELOG.md`.

## Preuves attendues

- tests DNS/HTTPS.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : aucune
- Tracabilite : `EF-15`, `ADR-011`, `OA-09`.
