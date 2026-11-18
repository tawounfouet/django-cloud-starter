# SDLC - django-cloud-starter

| Champ | Valeur |
|---|---|
| Version | 1.0 |
| Date | 18 novembre 2026 |
| Branche | `main` |
| Remote | `git@github.com:tawounfouet/django-cloud-starter.git` |
| Tags | aucun |
| Phase courante | 7 - Maintenance |
| Prochaine phase | 2 - Developpement (R1.2) |

## 1. Diagnostic du 18 novembre 2026

| Controle | Resultat |
|---|---|
| `git status --short` | 9 fichiers `docs/0*.md` supprimes a la racine, `docs/specs/` et `docs/plans/` non suivis, rien de stage |
| `git diff --cached --stat` | vide |
| `uv run pytest -q` | 9 passed |
| `uv run ruff check .` | All checks passed |
| `uv run python manage.py check` | 0 erreur |
| `git log --oneline -5` | 58fd7b1, d2b3a10, 77afb64, 796a408, 8ad5fb4 |
| `git tag --list` | vide |

Lecture : le code est stable et verifie, le travail en cours est purement documentaire. Cela correspond a la phase 7, avec une transition imminente vers la phase 2 pour la vertical slice `records`.

## 2. Cartographie des phases

| Phase | Objectif | Outils favoris |
|---|---|---|
| 1 - Planification et conception | Comprendre le systeme, arreter l'architecture, ecrire les specs | Mode `architect`, agent `plan`, `@docs-writer` |
| 2 - Developpement | Implementer les fonctionnalites et corriger les defauts | Agent `build`, `/refactor`, `@refactor-assistant`, `git-hygiene` |
| 3 - Tests | Verifier le comportement et couvrir les cas limites | `/test`, `@test-scaffolder`, `uv run pytest -q`, `uv run ruff check .` |
| 4 - Revue | Valider la qualite, la securite et la preparation PL | `/review`, `/pr-review`, `@code-reviewer`, mode `security-audit` |
| 5 - Release | Versionner, generer le changelog, taguer | `/release`, `@release-prep`, `diff-summary` |
| 6 - Deploiement | Commiter, pusher, deployer | `/commit`, `git-hygiene`, verification finale, protection des secrets |
| 7 - Maintenance | Documenter, traiter la dette, supporter | `/docs`, `@docs-writer`, `find-todos`, `git-hygiene` |

## 3. Etat du projet

- R1.1 socle local termine et commite : `8ad5fb4`, `d2b3a10`, `58fd7b1`.
- Documents de cadrage commites : `77afb64`.
- Documentation restructuree en attente de commit : anciens `docs/0*.md` deplacees vers `docs/specs/`, plan decoupe dans `docs/plans/`.
- Point d'entree du plan : `docs/plans/00_INDEX.md`.
- Prochain jalon fonctionnel : R1.2, premiere vertical slice `records`, decrite dans `docs/plans/02_R1_SOCLE_LOCAL.md`.

## 4. Prochaines actions

1. Phase 7 : committer la restructuration documentaire via `/commit` avec le message `docs: restructurer la documentation et le plan d'implementation`.
2. Phase 2 : implementer R1.2 en suivant `docs/plans/02_R1_SOCLE_LOCAL.md` et `docs/specs/02_BACKLOG_ET_USER_STORIES.md`.
3. Phase 3 : lancer `/test` ou `@test-scaffolder`, puis la verification equivalent : `uv run ruff check . && uv run pytest -q`.
4. Phase 4 : lancer `/review` avec `@code-reviewer`, puis corriger les remarques en revenant en phase 2 si necessaire.
5. Phase 5 et 6 : preparer la release avec `/release`, puis committer et pusher avec `/commit`.

## 5. Regles de cycle

- Une CI rouge renvoie immediatement en phase 2.
- Un hotfix peut court-circuiter la phase 4 vers les phases 5 et 6.
- Les referrences aux sections du plan d'origine restent valides grace au stub `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md` et a `docs/plans/00_INDEX.md`.
- Le dossier `archives/` est ignore par Git : ne jamais le committer.
- Aucun secret ne doit etre ajoute aux fichiers suivis.
