---
id: US-034
epic: EP-05
phase: R1/R3
gate: R1/R3
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-006, US-012/014/024.]
blocks: []
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/00_INDEX.md
---

# US-034 - Protéger les variables et accès aux fournisseurs

## Contexte

compartimenter les clés, tokens et droits d'administration.

## Criteres d acceptation

- [ ] AC-01 : secrets distincts entre Production et Preview / CI.
- [ ] AC-02 : permissions minimales sur GitHub Actions, Vercel, Neon et comptes associés.
- [ ] AC-03 : règles de rotation et procédure de révocation décrites.
- [ ] AC-04 : contrôle automatique de non-présence de secrets dans les commits.

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

- matrice de secrets expurgée et résultat du scan.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche generee depuis le backlog | ADR-019 |

## Notes

- Dependances : US-006, US-012/014/024.
- Tracabilite : `CA-10`, `AT-09`, `ENF-02`, `ADR-006`.
