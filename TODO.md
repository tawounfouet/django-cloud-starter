# TODO

| Champ | Valeur |
|---|---|
| Version | 1.0 |
| Date | 18 novembre 2026 |
| Source de verite | `docs/specs/02_BACKLOG_ET_USER_STORIES.md` |
| Plan associe | `docs/plans/00_INDEX.md` |
| Suivi SDLC | `SDLC.md` |
| Journal des changements | `CHANGELOG.md` |

> Ce fichier est une vue locale et datée de l'avancement. Le backlog reste la source de verite : ne decris ici que l'etat, jamais les criteres d'acceptation.

## Contributeurs

| Identifiant | Type | Role ou modele |
|---|---|---|
| `Thomas (humain)` | humain | arbitrage, recette et decision GO / NO-GO |
| `tawounfouet (humain)` | humain | compte GitHub, comptes Vercel et Neon |
| `opencode/big-pickle (agent)` | agent de code | implementation, documentation et tests, modele `opencode/big-pickle` |

## Regles de mise a jour

- Cocher une story uniquement si la Definition of Done est respectee : `docs/specs/02_BACKLOG_ET_USER_STORIES.md`, section 2.5.
- Format d'une ligne terminee : `| US-xxx | titre court | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | abcdef0 |`.
- Les stories actives possedent une fiche detaillee dans `docs/tasks/` ; le lien est place dans la colonne `Story`.
- La colonne `Statut` contient `[x]` ou `[ ]` ; elle reste la premiere colonne a lire lors d'un inventaire.
- Ajouter une entree dans `CHANGELOG.md` des qu'un livrable ou un comportement change.
- Mise a jour a chaque commit, revue rapide quotidienne, inventaire hebdomadaire, bilan a chaque gate.
- Une story partielle reste `[ ]` avec la mention `(partiel : ...)` dans la colonne `Preuve / note`.

## Progression

| Epic | Phase | Terminees | Stories | Etat |
|---|---|---:|---:|---|
| EP-00 | R0 | 4 | 4 | terminé |
| EP-01 | R1 | 7 | 7 | termine |
| EP-02 | R1/R2 | 1 | 6 | en cours |
| EP-03 | R2 | 0 | 6 | a demarrer |
| EP-04 | R3 | 0 | 8 | a demarrer |
| EP-05 | R1/R3 | 0 | 4 | a demarrer |
| EP-06 | R3/R5 | 0 | 5 | a demarrer |
| EP-07 | R3/R5 | 0 | 4 | a demarrer |
| EP-08 | R4 | 0 | 4 | conditionnel P2 |
| EP-09 | R5 | 0 | 4 | conditionnel P2 |
| **Total** | | **12** | **52** | **23 %** |

## Timeline ASCII

Legend : `#` fait, `>` position courante, `.` restant. Chaque barre represente 20 caracteres.

```text
Jalon  Epic  Avancement             Fait/Total  Pourcent  Etat
R0     EP-00 |####################|   4/4        100 %    termine
R1     EP-01 |####################|   7/7        100 %    termine
R1/R2  EP-02 |#>..................|   1/6          17 %    en cours
R2     EP-03 |>...................|   0/6          0 %    a demarrer
R3     EP-04 |>...................|   0/8          0 %    a demarrer
R1/R3  EP-05 |>...................|   0/4          0 %    a demarrer
R3/R5  EP-06 |>...................|   0/5          0 %    a demarrer
R3/R5  EP-07 |>...................|   0/4          0 %    a demarrer
R4     EP-08 |>...................|   0/4          0 %    conditionnel P2
R5     EP-09 |>...................|   0/4          0 %    conditionnel P2
TOTAL  TOUS  |####>...............|  12/52        23 %    en cours
```

## Suivi hebdomadaire

Une ligne par semaine. Les lignes `cible` sont indicatives et doivent etre remplacees par un releve reel.

```text
Semaine  Releve      Fait/Total  Barre                Delta  Note
2026-W47 2026-11-18 12/52        |####>...............|  +5   base R1.1, docs, R1.2 et CI locale
2026-W48 a remplir   -/52        |....................|   -   cible : R1.2
2026-W49 a remplir   -/52        |....................|   -   cible : CI GitHub
```

## Rapport rapide

```bash
rg -n '^\| US-[0-9]{3}.*\| \[x\] \|' TODO.md
rg -c '^\| US-[0-9]{3}.*\| \[[ x]\] \|' TODO.md
rg -c '^\| US-[0-9]{3}.*\| \[ \] \|' TODO.md
```

## EP-00 - Cadrage et decisions executables

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-001](docs/tasks/US-001_fixer-le-cas-d-usage-et-la-demonstration-mini.md) | Fixer le cas d'usage et la demonstration minimale | P0 | R0 | [x] | 2026-11-18 | Thomas (humain) | 2026-11-18, `77afb64` |
| [US-002](docs/tasks/US-002_valider-les-versions-python-django-et-le-mode.md) | Valider les versions Python/Django et le mode de packaging | P0 | R0 | [x] | 2026-11-18 | Thomas (humain) | 2026-11-18, `77afb64` |
| [US-003](docs/tasks/US-003_choisir-le-depot-les-droits-et-les-regles-de.md) | Choisir le depot, les droits et les regles de contribution | P0 | R0 | [x] | 2026-11-18 | Thomas (humain) | 2026-11-18, `77afb64` |
| [US-004](docs/tasks/US-004_verifier-la-nature-d-usage-la-region-et-le-bu.md) | Verifier la nature d'usage, la region et le budget | P0 | R0 | [x] | 2026-11-18 | Thomas (humain) | 2026-11-18, `77afb64` |

## EP-01 - Django local et fonctionnalite verticale

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-005](docs/tasks/US-005_initialiser-un-projet-django-modulaire.md) | Initialiser un projet Django modulaire | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `d2b3a10` |
| [US-006](docs/tasks/US-006_separer-configuration-secrets-et-environnemen.md) | Separer configuration, secrets et environnements | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `d2b3a10` |
| [US-007](docs/tasks/US-007_construire-la-page-publique-et-les-statiques.md) | Construire la page publique et les statiques | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `d2b3a10` |
| [US-008](docs/tasks/US-008_modele-record.md) | Implementer le modele Record et ses migrations | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `3d1bf9b` |
| [US-009](docs/tasks/US-009_crud-web.md) | Implementer un CRUD web complet | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `3d1bf9b` |
| [US-010](docs/tasks/US-010_auth-admin.md) | Configurer l'authentification et Django Admin | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `3d1bf9b` |
| [US-011](docs/tasks/US-011_tests-parcours.md) | Couvrir les vues et le parcours metier par les tests | P0 | R1 | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `3d1bf9b` |

## EP-02 - Qualite, tests et collaboration GitHub

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-012](docs/tasks/US-012_publier-le-projet-dans-le-depot-github-choisi.md) | Publier le projet dans le depot GitHub choisi | P0 | R1/R2 | [ ] | 2026-11-18 | tawounfouet (humain) | (partiel : remote configure, 8 commits locaux, push non autorise) |
| [US-013](docs/tasks/US-013_etablir-les-controles-statiques-et-de-dependa.md) | Etablir les controles statiques et de dependances | P0 | R1/R2 | [ ] | 2026-11-18 | opencode/big-pickle (agent) | (partiel : controles locaux et hygiene valides, run GitHub a valider, `bbf58a8`) |
| [US-014](docs/tasks/US-014_configurer-github-actions-pour-les-pull-reque.md) | Configurer GitHub Actions pour les pull requests | P0 | R1/R2 | [ ] | 2026-11-18 | opencode/big-pickle (agent) | (partiel : workflow cree, statuts PR a valider, `bbf58a8`) |
| [US-015](docs/tasks/US-015_ajouter-les-tests-d-integration-sur-postgresq.md) | Ajouter les tests d'integration sur PostgreSQL isole | P0 | R1/R2 | [ ] | 2026-11-18 | opencode/big-pickle (agent) | (partiel : service PostgreSQL 17 dans le workflow, run GitHub a valider, `bbf58a8`) |
| [US-016](docs/tasks/US-016_rendre-la-fusion-conditionnelle-aux-controles.md) | Rendre la fusion conditionnelle aux controles | P0 | R1/R2 | [ ] | 2026-11-18 | tawounfouet (humain) | (partiel : check `quality-and-tests` documente, regle a appliquer dans GitHub) |
| [US-017](docs/tasks/US-017_documenter-l-onboarding-et-les-commandes-cour.md) | Documenter l'onboarding et les commandes courantes | P0 | R1/R2 | [x] | 2026-11-18 | opencode/big-pickle (agent) | README CI et depannage, clone vierge valide, `bbf58a8` |

## EP-03 - Deploiement Vercel et previsualisations

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-018](docs/tasks/US-018_connecter-le-depot-github-a-vercel.md) | Connecter le depot GitHub a Vercel | P0 | R2 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-019](docs/tasks/US-019_fournir-une-url-https-de-production.md) | Fournir une URL HTTPS de production | P0 | R2 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-020](docs/tasks/US-020_declencher-le-deploiement-de-production-sur-m.md) | Declencher le deploiement de production sur `main` | P0 | R2 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-021](docs/tasks/US-021_produire-une-preview-par-pull-request.md) | Produire une Preview par pull request | P0 | R2 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-022](docs/tasks/US-022_servir-les-fichiers-statiques-django-en-ligne.md) | Servir les fichiers statiques Django en ligne | P0 | R2 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-023](docs/tasks/US-023_rattacher-logs-et-commit-au-deploiement.md) | Rattacher logs et commit au deploiement | P0 | R2 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |

## EP-04 - PostgreSQL Neon, donnees et migrations

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-024](docs/tasks/US-024_preparer-le-projet-neon-et-ses-acces.md) | Preparer le projet Neon et ses acces | P0 | R3 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-025](docs/tasks/US-025_raccorder-django-a-postgresql-neon.md) | Raccorder Django a PostgreSQL Neon | P0 | R3 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-026](docs/tasks/US-026_isoler-strictement-les-donnees-des-previews.md) | Isoler strictement les donnees des Previews | P0 | R3 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-027](docs/tasks/US-027_construire-le-processus-de-migration-controle.md) | Construire le processus de migration controlee | P0 | R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-028](docs/tasks/US-028_prouver-la-persistance-apres-redeploiement.md) | Prouver la persistance apres redeploiement | P0 | R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-029](docs/tasks/US-029_tester-sauvegarde-restauration-et-limites-du.md) | Tester sauvegarde, restauration et limites du service | P0 | R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-030](docs/tasks/US-030_verifier-connexions-pooling-et-comportement-s.md) | Verifier connexions, pooling et comportement serverless | P0 | R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-031](docs/tasks/US-031_isoler-et-securiser-la-base-de-ci.md) | Isoler et securiser la base de CI | P0 | R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |

## EP-05 - Securite et confidentialite

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-032](docs/tasks/US-032_durcir-les-reglages-django-en-production.md) | Durcir les reglages Django en production | P0 | R1/R3 | [ ] | a planifier | Thomas (humain) | a faire |
| [US-033](docs/tasks/US-033_controler-permissions-et-operations-sensibles.md) | Controler permissions et operations sensibles | P0 | R1/R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-034](docs/tasks/US-034_proteger-les-variables-et-acces-aux-fournisse.md) | Proteger les variables et acces aux fournisseurs | P0 | R1/R3 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-035](docs/tasks/US-035_formaliser-le-traitement-des-donnees-sensible.md) | Formaliser le traitement des donnees sensibles | P0 | R1/R3 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |

## EP-06 - Exploitation, reprise et maitrise des couts

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-036](docs/tasks/US-036_rendre-l-application-diagnostiquable.md) | Rendre l'application diagnostiquable | P0/P1 | R3/R5 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-037](docs/tasks/US-037_documenter-et-tester-le-retour-arriere-du-cod.md) | Documenter et tester le retour arriere du code | P0/P1 | R3/R5 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-038](docs/tasks/US-038_mettre-en-place-un-tableau-de-suivi-des-couts.md) | Mettre en place un tableau de suivi des couts et quotas | P0/P1 | R3/R5 | [ ] | a planifier | tawounfouet (humain) | a faire |
| [US-039](docs/tasks/US-039_definir-la-surveillance-minimale-du-service.md) | Definir la surveillance minimale du service | P0/P1 | R3/R5 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |
| [US-040](docs/tasks/US-040_prouver-la-reproductibilite-du-socle.md) | Prouver la reproductibilite du socle | P0/P1 | R3/R5 | [ ] | a planifier | opencode/big-pickle (agent) | a faire |

## EP-07 - Recette, release et starter reutilisable

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-041](docs/tasks/US-041_executer-la-campagne-de-recette-mvp.md) | Executer la campagne de recette MVP | P0/P1 | R3/R5 | [ ] | a planifier | Thomas (humain) | a faire |
| [US-042](docs/tasks/US-042_emettre-une-decision-go-no-go-fondee-sur-les.md) | Emettre une decision GO / NO-GO fondee sur les preuves | P0/P1 | R3/R5 | [ ] | a planifier | Thomas (humain) | a faire |
| [US-043](docs/tasks/US-043_produire-le-runbook-d-exploitation-initial.md) | Produire le runbook d'exploitation initial | P0/P1 | R3/R5 | [ ] | a planifier | Thomas (humain) | a faire |
| [US-044](docs/tasks/US-044_preparer-le-starter-pour-une-premiere-reutili.md) | Preparer le starter pour une premiere reutilisation | P0/P1 | R3/R5 | [ ] | a planifier | Thomas (humain) | a faire |

## EP-08 - Cloudflare a la demande

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-045](docs/tasks/US-045_associer-un-domaine-via-cloudflare-dns.md) | Associer un domaine via Cloudflare DNS | P2 | R4 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |
| [US-046](docs/tasks/US-046_proteger-un-formulaire-avec-turnstile.md) | Proteger un formulaire avec Turnstile | P2 | R4 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |
| [US-047](docs/tasks/US-047_ajouter-un-stockage-objet-pour-les-medias-uti.md) | Ajouter un stockage objet pour les medias utilisateurs | P2 | R4 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |
| [US-048](docs/tasks/US-048_evaluer-le-proxy-cloudflare-avant-activation.md) | Evaluer le proxy Cloudflare avant activation | P2 | R4 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |

## EP-09 - Extensions applicatives conditionnelles

| Story | Tache | Priorite | Gate | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|---|---|---|
| [US-049](docs/tasks/US-049_introduire-django-rest-framework.md) | Introduire Django REST Framework | P2 | R5 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |
| [US-050](docs/tasks/US-050_ajouter-un-frontend-react-next-js-separe.md) | Ajouter un frontend React / Next.js separe | P2 | R5 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |
| [US-051](docs/tasks/US-051_externaliser-les-traitements-longs.md) | Externaliser les traitements longs | P2 | R5 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |
| [US-052](docs/tasks/US-052_integrer-un-py-kit-si-son-benefice-est-demont.md) | Integrer un `Py**Kit` si son benefice est demontre | P2 | R5 | [ ] | a planifier | opencode/big-pickle (agent) | conditionnel |

## Hors backlog

| Element | Statut | Date | Assigne a | Preuve / note |
|---|---|---|---|---|
| Repository GitHub initialise et remote `origin` configure | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `8ad5fb4` |
| Archives locales ignorees via `.gitignore` | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `796a408` |
| Documents de cadrage ajoutes | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `77afb64` |
| Plan d'implementation decoupe dans `docs/plans/` avec stub de redirection | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, `2b87a2e` |
| `SDLC.md`, `TODO.md` et `CHANGELOG.md` mis en place | [x] | 2026-11-18 | opencode/big-pickle (agent) | 2026-11-18, non encore committé |

## Prochaines actions

| Action | Lien | Statut | Date | Assigne a | Note |
|---|---|---|---|---|---|
| Implementer R1.2 | `docs/plans/02_R1_SOCLE_LOCAL.md` | [x] | 2026-11-18 | opencode/big-pickle (agent) | US-008 a US-011, `3d1bf9b` |
| Configurer la CI GitHub Actions | `docs/plans/03_R2_GITHUB_CI.md` | [ ] | 2026-11-18 | opencode/big-pickle (agent) | workflow local `bbf58a8`, validation GitHub apres push |
| Consigner la preuve de clone vierge | `docs/specs/02_BACKLOG_ET_USER_STORIES.md` | [x] | 2026-11-18 | opencode/big-pickle (agent) | [US-017](docs/tasks/US-017_documenter-l-onboarding-et-les-commandes-cour.md), `bbf58a8` |
| Creer le workflow GitHub Actions | `docs/plans/03_R2_GITHUB_CI.md` | [ ] | 2026-11-18 | opencode/big-pickle (agent) | [US-014](docs/tasks/US-014_configurer-github-actions-pour-les-pull-reque.md), `bbf58a8` |
| Mettre a jour le journal des changements | `CHANGELOG.md` | [x] | 2026-11-18 | opencode/big-pickle (agent) | `bbf58a8`, `6c212b0` |
| Pousser `main` et valider le run CI | `git@github.com:tawounfouet/django-cloud-starter.git` | [ ] | a planifier | tawounfouet (humain) | autorisation de push requise |
| Appliquer la protection de `main` | `https://github.com/tawounfouet/django-cloud-starter/settings/branches` | [ ] | a planifier | tawounfouet (humain) | check requis : `quality-and-tests` |
