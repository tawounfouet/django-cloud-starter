# Changelog

Toutes les modifications notables du projet sont documentees ici.

Le format est chronologique et lie chaque entree a son commit. Aucune version semantique n'est annoncee tant qu'aucun tag de release n'existe.

## [Non publie] - 2026-11-18

### Ajoute

- `bbf58a8` : workflow GitHub Actions avec hygiene du depot, checks Django, migrations, PostgreSQL jetable, pytest et collectstatic.
- `6c212b0` : formatage des 15 fichiers deja suivis pour rendre le controle `ruff format --check .` vert.
- `3d1bf9b` : vertical slice `records` avec modele, migration, CRUD web, auth, admin et tests.
- `39eeb1a` : `docs/tasks/` avec modele, index et 52 fiches, y compris les stories deja implementees.
- `98ebd5b` : analyse du suivi Markdown local et `ADR-019` pour la migration future vers GitHub Issues.
- `98ebd5b` : analyse du nommage des archives de session et `ADR-020` pour la convention date, projet, rang et sujet.
- `2b87a2e` : `SDLC.md` avec diagnostic de phase, cartographie des 7 phases et prochaines actions.
- `2b87a2e` : plan d'implementation decoupe en 10 fichiers sous `docs/plans/`, avec `00_INDEX.md` comme point d'entree.
- `2b87a2e` : stub de redirection `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md` pour preserver les references croisees.
- `58fd7b1` : README documentant le bootstrap, les commandes courantes et la conformite R1.1.
- `d2b3a10` : application `apps.core`, page publique, template de base et feuille de style.
- `d2b3a10` : tests de configuration et de vue pour verrouiller le contrat R1.1.
- `8ad5fb4` : projet Django initialise avec `uv`, `uv.lock`, Python 3.12 et configuration de base.

### Modifie

- `3d1bf9b` : `config/urls.py` monte les URLs `accounts/` et `records/` ; `config/settings.py` ajoute `apps.records` et les redirections de connexion.
- `bbf58a8` : `README.md` documente la CI, le check requis `quality-and-tests` et le depannage courant.
- `2b87a2e` : specifications deplacees de `docs/` vers `docs/specs/` sans changement de contenu.
- `d2b3a10` : `config/settings.py` passe a une configuration stricte pilotee par `APP_ENV`.
- `d2b3a10` : `pyproject.toml` verrouille sur Python 3.12 et ajoute les outils de test et de lint.
- `98ebd5b` : convention de nommage des archives de session applicable avec date, projet, rang et sujet ; quatre archives existantes renommees et references croisees corrigees.
- `796a408` : `.gitignore` exclut le dossier `archives/` du suivi Git.

### Corrige

- `d2b3a10` : chargement de `.env` limite au mode `local` avec `override=False`.
- `d2b3a10` : secret local obligatoire, aucun placeholder utilise au demarrage.
- `d2b3a10` : `DATABASE_URL` PostgreSQL rendue obligatoire hors du mode `local`.

### Supprime

- `2b87a2e` : ancien fichier unique `docs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`, remplace par le stub et les extraits dans `docs/plans/`.

## Lien avec TODO.md

- `TODO.md` repond a la question : qu'est-ce qui est fait et qu'est-ce qui reste ?
- `CHANGELOG.md` repond a la question : qu'est-ce qui a change et quand ?
- Cocher une case dans `TODO.md` n'ecrit pas automatiquement dans ce fichier : ajouter une entree lorsque le changement est livrable ou visible.
- Pour un rapport hebdomadaire, croiser les cases cochees de `TODO.md` avec les entrees de `CHANGELOG.md`.
