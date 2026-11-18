# 04 - Plan d'implémentation et CI/CD

## Socle Django + GitHub + Vercel + Neon + Cloudflare

| Champ | Valeur |
|---|---|
| Document | `04_PLAN_IMPLEMENTATION_ET_CI_CD.md` |
| Version | 1.0 |
| Date | 18 novembre 2026 |
| Statut | **Plan opérationnel proposé, non exécuté** |
| Projet de référence | `django-cloud-starter` (nom provisoire) |
| Documents amont | `00_DJANGO_GITHUB_VERCEL_NEON_CLOUDFLARE_EXPRESSION_DU_BESOIN.md`, `01_ARCHITECTURE_ET_DECISIONS.md`, `02_BACKLOG_ET_USER_STORIES.md`, `03_STRUCTURE_PROJET_ET_CONFIGURATION.md` |
| Périmètre de livraison | R0 à R3 : MVP Django, GitHub, Vercel et Neon ; R4/R5 conditionnels |
| Objectif | Obtenir un cycle `développement -> PR -> CI -> Preview isolée -> fusion -> production -> vérification` démontrable |
| Gouvernance | Les créations de ressources, dépenses, migrations et mises en production requièrent les autorisations du propriétaire |

> Ce fichier est une **spécification d'exécution**, pas un compte rendu d'une implémentation déjà réalisée. Les exemples de workflows et de commandes sont des **gabarits à adapter au dépôt réel**. Aucune ressource GitHub, Vercel, Neon ou Cloudflare n'a été créée ni modifiée lors de sa rédaction.
>
> **Principe central :** l'automatisation du déploiement du code n'autorise pas l'automatisation aveugle des migrations PostgreSQL. Les schémas et les données suivent un processus de release contrôlé.

---

## 1. Résumé des décisions applicables

| Référence | Décision de mise en oeuvre | Conséquence |
|---|---|---|
| ADR-001 | Monolithe Django modulaire | Un seul service Python HTTP pour le MVP |
| ADR-002 | Templates Django + Admin | Pas de frontend React ou API DRF obligatoire |
| ADR-003 | GitHub et pull requests | `main` est la branche de référence |
| ADR-004 | Déploiement Django natif Vercel | Détection de `manage.py`, sans `/api/index.py` historique |
| ADR-005 | PostgreSQL Neon | DB distante persistante hors fonctions web |
| ADR-006 | Isolation stricte des Previews | Aucune Preview ne doit pointer sur Production |
| ADR-007 | Migrations hors build Vercel | Job de migration séparé, autorisé, vérifié |
| ADR-008 | Auth native Django | Autorisations côté serveur et Admin |
| ADR-009 | WSGI initial | `config.wsgi.application`, pas d'ASGI actif par défaut |
| ADR-010 | Statiques depuis CDN Vercel | `STATIC_ROOT` et collecte au build natif |
| ADR-011/012 | Cloudflare selon besoin | DNS-only en cas de domaine ; R2/Turnstile optionnels |
| ADR-013 | Dépendances verrouillées | Python 3.12 / Django 5.2 LTS candidats, `uv.lock` |
| ADR-014/015 | Pas de workers ou Py**Kit imposés | Industrialisation justifiée par l'usage |
| ADR-016/017 | Plan et région conformes | Arbitrage préalable sur usage commercial et résidence des données |
| ADR-018 | Preuves d'acceptation | `CA-01` à `CA-13` avant GO MVP |

### 1.1 Hypothèses R0 encore ouvertes

- `OA-01` : usage personnel/prototype ou commercial, donc plan Vercel adéquat.
- `OA-02/03` : compte GitHub, dépôt, visibilité, nom final.
- `OA-04` : démonstrateur `Record` et règles de permission.
- `OA-05` : versions Python/Django et outil de packaging.
- `OA-06` : régions Vercel et Neon.
- `OA-07` : stratégie Preview avec **données synthétiques**.
- `OA-08` : étape de migration Production et politique de promotion.
- `OA-09/10` : domaine, coûts et enveloppe budgétaire.
- `OA-11/12` : capacités de restauration, fonctionnalités différées.

**Valeurs de départ proposées :** dépôt `django-cloud-starter`, Python 3.12, Django 5.2 LTS, `uv`, modèle `Record`, domaine Vercel natif, DB PostgreSQL Neon et données synthétiques. Ces valeurs restent à **valider** avant des actions externes.

---

## 2. Résultat observable et chaîne de livraison

```mermaid
flowchart TD
    L[Développement local Django] --> B[Branche feat ou fix]
    B --> PR[Pull request GitHub]
    PR --> CI[CI GitHub Actions : lint, tests, PostgreSQL temporaire]
    PR --> PV[Vercel Preview]
    PV --> DBPV[(Neon Preview isolé ou DB synthétique dédiée)]
    CI --> Q{Contrôles requis réussis ?}
    Q -->|Non| FIX[Corriger la PR]
    FIX --> PR
    Q -->|Oui| RV[Revue et fusion autorisée]
    RV --> MAIN[main]
    MAIN --> BLD[Vercel construit une release]
    MAIN --> REL[Planifier migrations compatibles via étape séparée]
    REL --> GATE{Release et schéma compatibles ?}
    BLD --> GATE
    GATE -->|Non| HOLD[Ne pas promouvoir / corriger]
    GATE -->|Oui| PROD[Vercel Production HTTPS]
    PROD --> DB[(Neon Production)]
    PROD --> SMOKE[Smoke test et observation]
    SMOKE --> REC[Preuves CA et décision GO / NO-GO]
```

**Nuance :** en configuration Git/Vercel standard, Vercel peut créer le déploiement dès le push, indépendamment du statut CI. Les règles de fusion de `main` sont le premier garde-fou. Si un véritable blocage **avant exposition** est requis, configurer et tester des *Deployment Checks* Vercel ou une autre politique de promotion disponible sur le plan choisi. Une CI verte sur la PR ne suffit pas, à elle seule, à garantir qu'une production n'exposera jamais un mauvais commit.

### 2.1 Deux modes de livraison

**Mode A - MVP sans modification incompatible de schéma :** première migration Neon effectuée avant l'exposition de l'application ; ensuite, code sur `main` -> Vercel Production automatiquement ; chaque évolution de schéma suit une procédure séparée et compatible avant/après la publication.

**Mode B - Contrôle de promotion renforcé :** Vercel construit une release candidate ; tests de déploiement et migration compatible sont vérifiés avant que la release ne soit promue. Ce mode **n'est activé qu'après vérification des fonctionnalités et du plan Vercel réellement disponibles**. En son absence, ne pas prétendre que le déploiement est bloqué par un contrôle qu'aucun service n'applique.

---

## 3. Plan de réalisation par jalons

| Jalon | Résultat concret | Stories majeures | Dépendance | Preuve de sortie |
|---|---|---|---|---|
| **R0 - Cadrage** | Hypothèses et plan d'hébergement arbitrés | US-001 à US-004 | Documents `00` à `03` | Registre OA validé |
| **R1.1 - Bootstrap** | Django démarre, projet versionné localement | US-005 à US-007, US-017 | R0 | `runserver`, page HTML, `check` |
| **R1.2 - Vertical slice** | `Record` + Admin + Auth + CRUD + tests | US-008 à US-011, US-033 | R1.1 | Tests d'usage et de permissions |
| **R2.1 - GitHub/CI** | PR avec statut qualité bloquant | US-012 à US-016, US-031 | R1.2 | Runs vert/rouge, règle de fusion |
| **R2.2 - Vercel HTTP** | Django, statiques et HTTPS en ligne | US-018 à US-020, US-022/023 | R2.1 | URL et SHA de production |
| **R3.1 - Neon** | Configuration PostgreSQL isolée et durable | US-024/025, US-031/034 | R0, R1.2 | Connexion sécurisée |
| **R3.2 - Previews** | Environnements PR sans données Production | US-021/026, US-035 | R2.2, R3.1 | Test sentinelles |
| **R3.3 - Release DB** | Migrations contrôlées, persistance prouvée | US-027 à US-030 | R3.1/R3.2 | Migration test, données après redeploy |
| **R3.4 - Exploitation** | Sécurité, rollback, recette, runbook | US-032, US-036 à US-043 | R2/R3 | `CA-01` à `CA-13` + GO |
| **R4 - Cloudflare** | Domaine, Turnstile ou stockage si besoin | US-045 à US-048 | R3 + besoin | Test du service ajouté |
| **R5 - Réutilisation** | Starter réutilisable, améliorations utiles | US-039/040/044, US-049 à US-052 | MVP validé | Deuxième bootstrap, ADR évolutives |

Aucun délai arbitraire n'est attribué à ces jalons. Un jalon est clos sur des **preuves**, pas au terme d'une semaine prédéterminée.

---

## 4. R0 - Préparation et prérequis

### 4.1 Contrôle des accès et des contraintes

- [ ] Confirmer le propriétaire du dépôt, son caractère public/privé, les personnes autorisées à fusionner et le nom de `main`.
- [ ] Confirmer que le plan Vercel autorise effectivement la nature de l'activité ; **Hobby ne doit pas être retenu par défaut pour une application commerciale**.
- [ ] Confirmer la région d'exécution Vercel et la région PostgreSQL Neon, idéalement proches et compatibles avec les exigences de données.
- [ ] Vérifier les plans Neon et Vercel, limites, éventuels moyens de paiement et protections disponibles pour les Previews.
- [ ] Définir si des données personnelles existent. Pour le starter MVP, utiliser **uniquement des données synthétiques**.
- [ ] Décider si le domaine personnalisé est différé à R4, ce qui est recommandé.
- [ ] Définir un responsable des secrets, migrations, releases et tests GO / NO-GO.

### 4.2 Outils locaux à réunir

| Outil | Rôle | Vérification |
|---|---|---|
| Git | Historique et push | `git --version` |
| Python 3.12 candidat | Runtime local | `python3 --version` ou `uv run python --version` |
| `uv` | Dépendances et lockfile | `uv --version` |
| PostgreSQL local (facultatif) | Test d'intégration développeur | `psql --version` |
| GitHub | Dépôt/PR | Accès au dépôt validé |
| Vercel | Hébergement | Compte et plan vérifiés |
| Neon | PostgreSQL | Projet/plan/région validés |

**Sortie R0 :** décisions OA bloquantes tranchées et accès disponibles. Aucune ressource payante n'est créée implicitement.

---

## 5. R1.1 - Initialisation reproductible de Django

### 5.1 Structure cible minimale

```text
django-cloud-starter/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release-migrate.yml          # R3 uniquement
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   └── records/
│       ├── __init__.py
│       ├── apps.py
│       ├── admin.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       ├── views.py
│       ├── migrations/
│       └── tests/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py                 # Présent éventuellement, sans ASGI_APPLICATION actif
├── templates/
│   ├── base.html
│   ├── core/
│   ├── records/
│   └── registration/
├── static/css/
├── docs/
├── .env.example
├── .gitignore
├── .python-version
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md
```

Les fichiers réellement présents dépendront de l'incrément. Se reporter au document `03` pour les responsabilités des modules et des réglages.

### 5.2 Bootstrap de référence

Le dépôt et les versions doivent avoir été décidés en R0. L'extrait suivant illustre **une initialisation dans un répertoire neuf**, sans écraser de fichiers existants.

```bash
mkdir django-cloud-starter
cd django-cloud-starter

git init -b main
uv python install 3.12
uv init --no-package --python 3.12
uv add "Django>=5.2,<5.3" "psycopg[binary]>=3.2,<4" \
  "dj-database-url>=2.2,<4" "python-dotenv>=1,<2"
uv add --dev pytest pytest-django ruff
uv lock
uv sync --locked
uv run django-admin startproject config .
```

Après le bootstrap, **adapter** `config/settings.py`, les apps, l'URLConf, le modèle `Record`, les templates et le `pyproject.toml` aux choix du document `03` : il n'est pas attendu que la commande `startproject` produise toute l'arborescence à elle seule.

Le fichier `pyproject.toml` cible conserve une version mineure de Python fixe (`>=3.12,<3.13`) et une plage Django LTS (`>=5.2,<5.3`) jusqu'à l'arbitrage de compatibilité ; `uv.lock` est toujours versionné.

### 5.3 Contrat de configuration

```dotenv
# .env.example - NE JAMAIS ajouter de vrais secrets
APP_ENV=local
DJANGO_SECRET_KEY=REPLACE_WITH_LOCAL_RANDOM_SECRET
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DJANGO_LOG_LEVEL=INFO
# DATABASE_URL=postgresql://local_user:local_password@localhost:5432/local_db
```

- `.env` est ignoré par Git ; `python-dotenv` le charge uniquement en mode `local` selon le document `03`.
- `APP_ENV` prend exactement `local`, `ci`, `preview` ou `production`.
- En `ci`, `preview` et `production`, une `DATABASE_URL` PostgreSQL explicite est requise, jamais une SQLite de repli.
- `DJANGO_SECRET_KEY` et `DJANGO_ALLOWED_HOSTS` sont propres aux environnements.
- Le processus refuse un `APP_ENV` distant implicite ou une clé de démonstration.
- Le modèle d'authentification reste **Django Auth**, pas Neon Auth dans le MVP.

### 5.4 Commandes de vérification R1.1

```bash
cp .env.example .env
# Générer une vraie clé locale unique et remplacer le placeholder dans .env.
# Ne pas commiter ce fichier.
uv sync --locked
uv run python manage.py check
uv run python manage.py migrate --noinput
uv run python manage.py runserver
```

### Gate R1.1

- [ ] Le serveur local répond avec une page publique.
- [ ] Le clone + installation ne nécessite aucun service externe pour afficher la page.
- [ ] Les fichiers `.env` et `db.sqlite3` sont ignorés.
- [ ] `manage.py check` ne remonte aucune erreur bloquante.
- [ ] `uv.lock` et `.python-version` sont versionnés.

**Preuves :** commande de lancement, page publique, sortie de `manage.py check`, statut Git.

---

## 6. R1.2 - Première vertical slice métier

### 6.1 Scénario

Le modèle `Record` (cf. `03`) possède `title`, `description`, `status`, `created_by`, `created_at`, `updated_at`. Les routes permettent la liste, le détail, la création, la modification et la suppression des enregistrements autorisés.

| Tâche | Livrable | Contrôle de sécurité | US |
|---|---|---|---|
| Modèle | `apps/records/models.py` et migrations | Contraintes et propriété des objets | US-008 |
| Administration | `admin.py` | Accès `is_staff` et permissions | US-010 |
| Interface | Formulaires, vues et templates | CSRF et validation côté serveur | US-007/009 |
| Auth | Connexion et déconnexion Django | Sessions, login obligatoire | US-010 |
| Autorisations | QuerySet filtrés et vérification de propriétaire | IDOR, modification d'un objet d'autrui refusée | US-009/033 |
| Tests | Modèles, formulaires, vues, permissions | Cas positifs et négatifs | US-011 |

### 6.2 Commandes de contrôle

```bash
uv run python manage.py makemigrations records
uv run python manage.py migrate --noinput
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py test
uv run ruff check .
uv run ruff format --check .
```

> L'app Django doit être déclarée `apps.records` dans `INSTALLED_APPS` avec le label `records`. Les utilisateurs de test et les données `Record` doivent être **générés**, sans importer de données réelles.

### Gate R1.2

- [ ] Les opérations CRUD fonctionnent localement.
- [ ] Un utilisateur anonyme ne peut pas écrire.
- [ ] Un utilisateur ne peut pas modifier un enregistrement non autorisé.
- [ ] Les migrations sont versionnées et aucune migration n'est oubliée.
- [ ] Les tests R1 réussissent.

**Preuves :** rapport tests + liste des migrations + démonstration d'un refus d'accès.

---

## 7. R2.1 - GitHub : dépôt, PR et règles de fusion

### 7.1 Publication du dépôt

1. Créer le dépôt approuvé, avec visibilité et propriétaire validés.
2. Vérifier le `.gitignore`, les licences éventuelles, les fichiers source et la documentation.
3. Publier le commit initial sur `main` avec une origine GitHub configurée.
4. Activer les fonctionnalités de revue et de contrôle disponibles selon le plan GitHub.
5. Exiger le passage par des branches `feat/*`, `fix/*`, `docs/*` pour le travail courant.
6. Documenter les exceptions de maintenance et les droits de contournement éventuels.

**Exemple de publication** (nécessite un dépôt GitHub existant et une URL autorisée) :

```bash
git status --short
git add .
git commit -m "chore: bootstrap Django cloud starter"
git remote add origin <URL_GITHUB_CONFIRME>
git push -u origin main
```

`<URL_GITHUB_CONFIRME>` représente un paramètre à substituer, **pas une URL utilisable telle quelle**.

### 7.2 Politique PR minimale

- Vérifications obligatoires : lint/format, tests Django, intégration PostgreSQL, migrations en attente.
- Revue de PR selon la taille de l'équipe et le plan GitHub.
- Aucun secret Production dans la CI PR, y compris pour une contribution issue d'un fork.
- **Ne pas utiliser `pull_request_target` pour exécuter du code non fiable avec des secrets privilégiés.**
- `main` ne reçoit pas normalement de pushes directs ; contrôler les rôles pouvant contourner les règles.
- Une release n'est pas validée par le seul fait qu'un build Vercel a réussi.

### 7.3 Preuves attendues

- PR valide : tous les checks deviennent verts.
- PR invalide : défaut volontaire de test ou de lint, check rouge.
- Règle de fusion : impossibilité de fusionner la PR invalide via la voie normale, ou écart explicite si le plan GitHub ne permet pas l'application technique de la règle.

---

## 8. R2.1 - Workflow CI de référence

### 8.1 Fichier `.github/workflows/ci.yml`

Cet exemple est destiné à être **copié puis adapté**. Il démarre un PostgreSQL temporaire *dans le runner GitHub*, sans service Neon ni identifiant réel. Les valeurs `ci_user/ci_password` ci-dessous ne servent qu'au conteneur jetable du job : elles ne doivent pas être réutilisées ailleurs.

```yaml
name: Django CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: django-ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality-and-tests:
    name: quality-and-tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
    env:
      APP_ENV: ci
      DJANGO_SECRET_KEY: ci-only-ephemeral-test-key-not-for-production
      DJANGO_DEBUG: "false"
      DJANGO_ALLOWED_HOSTS: localhost,127.0.0.1,testserver
      DATABASE_URL: postgresql://ci_user:ci_password@127.0.0.1:5432/ci_db
      CI: "true"

    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_DB: ci_db
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ci_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U ci_user -d ci_db"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v10
        with:
          enable-cache: true

      - name: Set up Python 3.12
        run: uv python install 3.12

      - name: Install locked dependencies
        run: uv sync --frozen --group dev

      - name: Lint
        run: uv run --frozen ruff check .

      - name: Format
        run: uv run --frozen ruff format --check .

      - name: Django system checks
        run: uv run --frozen python manage.py check

      - name: Ensure migrations are committed
        run: uv run --frozen python manage.py makemigrations --check --dry-run

      - name: Test PostgreSQL migrations
        run: uv run --frozen python manage.py migrate --noinput

      - name: Run application tests
        run: uv run --frozen python manage.py test

      - name: Validate static collection
        run: uv run --frozen python manage.py collectstatic --noinput
```

### 8.2 Commentaires de sécurité et d'exécution

1. Le déclencheur `pull_request` utilise le modèle standard, **sans** `pull_request_target`.
2. `permissions: contents: read` impose un jeton GitHub restreint.
3. Les tests utilisent uniquement le conteneur PostgreSQL du job.
4. Les variables `DJANGO_SECRET_KEY`, `DATABASE_URL` du workflow ne sont **pas** des clés ou des identifiants Neon ; elles sont locales au runner temporaire.
5. `uv.lock` doit être commité et correspondre au `pyproject.toml` ; vérifier la politique de groupe de dépendances lors de l'implémentation.
6. Les versions des GitHub Actions doivent idéalement être **verrouillées par SHA complet** lors du durcissement de la chaîne d'approvisionnement ; les tags majeurs ci-dessus privilégient la lisibilité de ce modèle.
7. La commande `collectstatic` en CI n'est qu'un contrôle. Vercel sait exécuter la collecte au build : **ne pas créer un script Vercel personnalisé qui la relance sans nécessité**.
8. La durée de `timeout-minutes` est une garde de CI, à mesurer puis ajuster ; ce n'est pas une estimation de travail.
9. Une suite `pytest` peut remplacer `manage.py test` si la configuration et les tests sont adaptés ; ne pas imposer deux runners pour le même corpus.
10. Le workflow ci-dessus ne fournit **aucun** secret de production à une PR ou un fork.

### 8.3 Variante de contrôle de sécurité

- Exécuter `manage.py check --deploy` avec une **configuration fictive de type production**, pour analyser les avertissements Django. Si la politique finale de proxy HTTPS et HSTS n'est pas encore arbitrée, ne pas ignorer aveuglément les avertissements.
- Ajouter une analyse de secrets et de dépendances selon les possibilités du dépôt ; choisir des outils versionnés et adapter les seuils d'alerte.
- Les contrôles bloquants sur `main` doivent être définis sur le **nom exact du job** (ici `quality-and-tests`) et vérifiés après chaque renommage.

### 8.4 Gate CI

- [ ] Un commit correct produit un run vert.
- [ ] Une erreur Ruff ou Django produit un run rouge.
- [ ] Une migration de modèle oubliée produit un run rouge.
- [ ] Une base CI neuve reçoit les migrations et les tests passent.
- [ ] Aucun credential Production n'est disponible dans le job.

---

## 9. R2.2 - Connexion et déploiement Django sur Vercel

### 9.1 Préconditions

- Dépôt GitHub et branche `main` prêts.
- `manage.py` à la racine du projet ; `config/settings.py` et `config/wsgi.py` cohérents.
- Version Python prise en charge et `uv.lock` verrouillé.
- `WSGI_APPLICATION = "config.wsgi.application"` dans les settings actives.
- `ASGI_APPLICATION` **non défini** tant que WSGI reste la cible, car Vercel peut privilégier ASGI si les deux sont configurés.
- `STATIC_ROOT` défini ; `STATIC_URL` correct.
- Plan Vercel adapté à l'usage réel.

### 9.2 Parcours de configuration Vercel

1. Importer le dépôt GitHub dans un projet Vercel approuvé.
2. Vérifier la racine du projet : elle doit contenir le `manage.py` et le `pyproject.toml` attendus.
3. Laisser Vercel détecter Django nativement. **Pas de `vercel.json`, `/api/`, Dockerfile ni configuration de réécriture par défaut.**
4. Définir la région retenue et la version Python via les fichiers versionnés.
5. Renseigner explicitement les variables Preview et Production, **sans réutiliser la DB Production en Preview**.
6. Vérifier le build, les logs et les URLs attribuées.
7. Vérifier la page HTML, l'Admin, l'authentification et les statiques.
8. Associer le déploiement au commit exact et consigner le résultat.

### 9.3 Contrat des variables Vercel

| Variable | Production | Preview | Commentaire |
|---|---|---|---|
| `APP_ENV` | `production` | `preview` | Doit être explicite |
| `DJANGO_SECRET_KEY` | Secret Production | Secret Preview distinct | Ne jamais partager le secret entre scopes |
| `DJANGO_DEBUG` | `false` | `false` | Aucun traceback public |
| `DJANGO_ALLOWED_HOSTS` | Domaine(s) réel(s) | Domaine(s) Preview autorisé(s) | Pas de `*` global |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origines HTTPS de Production | Origines HTTPS Preview autorisées | Vérifier POST et cookies |
| `DATABASE_URL` | Neon Production | Neon Preview isolée | **Interdiction absolue de réemploi** |
| `DJANGO_LOG_LEVEL` | Niveau approprié | Niveau approprié | Journaux sans secrets |

**Attention aux URLs dynamiques** : `VERCEL_URL` peut varier selon chaque déploiement. La stratégie de noms d'hôtes autorisés doit être explicite et testée ; ne pas mettre un wildcard général pour contourner un problème de Preview. La présence de `APP_ENV=preview` **ne prouve pas** que la `DATABASE_URL` est sûre.

### 9.4 Statiques et première mise en ligne

La documentation Vercel indique que si `STATIC_ROOT` est défini, Vercel exécute `collectstatic` lors du build et sert les fichiers collectés depuis son CDN. Valider via une requête HTTP réelle vers les fichiers CSS.

La première migration Neon doit être effectuée via une procédure séparée avant l'ouverture d'une interface nécessitant les tables correspondantes. **Un build réussi sans tables PostgreSQL n'est pas une recette fonctionnelle.**

### 9.5 Contrôle du déploiement en présence de la CI

- GitHub : les checks requis bloquent les **fusions normales** sur `main`.
- Vercel : la connexion Git déclenche la construction du déploiement sur push/merge.
- Si un contrôle de promotion en production est nécessaire, configurer des **Deployment Checks** basés sur les statuts GitHub appropriés ou le mécanisme équivalent disponible. Tester une release volontairement invalide et vérifier que le domaine de production **ne bascule pas**.
- Ne pas confondre « déploiement créé » et « nouveau déploiement promu au domaine de production ».
- Les check jobs GitHub utilisés comme Deployment Checks doivent avoir des **noms uniques et stables**, pour éviter les collisions de statuts.

### Gate Vercel

- [ ] URL Production en HTTPS.
- [ ] Version en ligne correspond au SHA Git.
- [ ] Fichiers statiques accessibles.
- [ ] Admin protégé ; DEBUG désactivé.
- [ ] Variables Preview et Production distinctes.
- [ ] Règle réelle de promotion vérifiée si cette fonction a été retenue.

---

## 10. R3.1 - Neon et séparation des environnements

### 10.1 Matrice des environnements

| Environnement | Exécution | Base | Données autorisées | Autorisation de migration |
|---|---|---|---|---|
| Local | Machine développeur | SQLite local ou PostgreSQL dédié | Synthétiques uniquement au MVP | Développeur, base locale |
| CI | GitHub Actions | PostgreSQL éphémère du job | Synthétiques uniquement | Automatique, DB éphémère |
| Preview | Vercel par PR | Branche Neon non productive ou DB isolée | **Synthétiques uniquement** | Procédure Preview isolée |
| Production | Vercel / Neon | Neon Production | Données réelles selon usage validé | Job de release autorisé uniquement |

### 10.2 Initialisation Neon

1. Créer le projet Neon **après validation du plan et de la région**.
2. Créer/identifier la branche Production et ses rôles.
3. Utiliser une connexion poolée pour le trafic web si validé avec Django/Neon ; utiliser les connexions directes appropriées pour les opérations administratives ou migrations, selon la documentation applicable.
4. Protéger les URL, avec TLS et accès minimaux.
5. Mettre en place une source Preview **synthétique** distincte de Production.
6. Intégrer la base aux variables Vercel Production et Preview sous les scopes appropriés.
7. Consigner un moyen de restauration et ses limites réelles.

### 10.3 Neon Branching : bénéfice et piège de confidentialité

L'intégration Neon/Vercel peut créer une branche PostgreSQL pour chaque Preview. **Une branche Neon peut copier les données de sa branche parente** : elle fournit une isolation des **écritures**, mais pas automatiquement une isolation des **données personnelles**.

Dans ce starter :

- **Recommandation de départ :** utiliser une branche parente synthétique ou une DB Preview dédiée entièrement sans données réelles.
- **Ne pas activer aveuglément** une intégration de branching qui dérive Preview d'une Production contenant des données sensibles.
- Vérifier le parent réel configuré, les permissions, les URLs injectées et la politique de nettoyage.
- Les capacités d'anonymisation Neon peuvent être évaluées ultérieurement, avec validation du résultat, mais ne remplacent pas une politique de confidentialité.
- Si le plan ou l'intégration ne permet pas d'assurer cela, choisir une base dédiée de test et **désactiver la Preview dynamique** plutôt que de prendre un risque.

### 10.4 Tests d'isolation obligatoires

**Sentinelles** : insérer une donnée distincte `PROD_ONLY` sur Production et `PREVIEW_ONLY` sur Preview, avec des identifiants et données fictifs.

1. Vérifier que Preview ne voit pas `PROD_ONLY` et que Production ne voit pas `PREVIEW_ONLY`.
2. Modifier un `Record` sur Preview.
3. Vérifier l'absence de changement en Production.
4. Vérifier que les secrets, rôles et URLs DB sont distincts **sans journaliser leur valeur**.
5. Vérifier la suppression/expiration des branches Preview selon la politique configurée.

**Gate Neon :** une simple comparaison de chaînes d'URL ne suffit pas. L'isolation doit être démontrée sur les ressources et les données effectivement accessibles.

---

## 11. R3.2 - Migrations PostgreSQL indépendantes du build

### 11.1 Contrat non négociable

**Interdit en Production :**

- `manage.py migrate` dans `settings.py`, `wsgi.py`, `asgi.py`, une vue, un middleware ou le chargement d'une fonction Vercel.
- `manage.py migrate` dans un `buildCommand` Vercel ou un script `collectstatic`.
- Exécution d'une migration de Production depuis une PR non approuvée.
- Migration destructive non testée ou sans stratégie de reprise.

**Exigé :**

- Migrations versionnées, relues et testées sur PostgreSQL CI/Preview isolé.
- Étape de migration Production distincte et autorisée, avec logs et identité du commit.
- Restauration et plan de reprise explicités ; rollback applicatif et restauration DB traités séparément.
- Changements de schéma compatibles avec les versions simultanément déployées lorsque nécessaire.

### 11.2 Workflow GitHub Actions de migration (modèle de départ)

Ce fichier n'est **pas** un déclencheur automatique sur push : il est exécuté manuellement par un opérateur habilité. Il présuppose un environnement GitHub nommé `production-db`, protégé par les approbations disponibles, avec un secret `DATABASE_URL_UNPOOLED` limité aux responsables de production. La mise à disposition d'un secret au runner suppose que l'environnement GitHub a été approuvé et que la configuration réseau Neon permet la connexion depuis le runner autorisé.

```yaml
name: Production DB migration

on:
  workflow_dispatch:
    inputs:
      confirmation:
        description: 'Saisir MIGRATE_PRODUCTION pour confirmer'
        required: true
        type: string

permissions:
  contents: read

concurrency:
  group: production-db-migrations
  cancel-in-progress: false

jobs:
  migrate:
    name: migrate-production-db
    if: github.ref == 'refs/heads/main' && inputs.confirmation == 'MIGRATE_PRODUCTION'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: production-db
    env:
      APP_ENV: production
      DJANGO_DEBUG: 'false'
      DJANGO_SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
      DATABASE_URL: ${{ secrets.DATABASE_URL_UNPOOLED }}
      DJANGO_ALLOWED_HOSTS: ${{ vars.DJANGO_ALLOWED_HOSTS }}
      DJANGO_CSRF_TRUSTED_ORIGINS: ${{ vars.DJANGO_CSRF_TRUSTED_ORIGINS }}

    steps:
      - name: Checkout validated main
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v10

      - name: Set up Python
        run: uv python install 3.12

      - name: Install locked dependencies
        run: uv sync --frozen

      - name: Check Django settings
        run: uv run --frozen python manage.py check

      - name: Display migration plan
        run: uv run --frozen python manage.py migrate --plan

      - name: Apply authorized migrations
        run: uv run --frozen python manage.py migrate --noinput

      - name: Verify migration history
        run: uv run --frozen python manage.py showmigrations --plan
```

**Limites et conditions de sécurité du modèle :**

- Le fichier YAML ne crée pas automatiquement la protection `production-db` : elle doit être configurée, vérifiée et testée selon les fonctionnalités du dépôt/plan GitHub.
- L'`if` limite la branche, mais **n'est pas un substitut** à la revue du commit, à un environnement protégé et aux permissions GitHub.
- Vérifier la configuration réelle des variables de l'environnement GitHub. Toute variable absente doit produire un échec avant modification.
- Les migrations peuvent nécessiter des opérations préparatoires et des verrous applicatifs que ce gabarit n'implémente pas ; documenter les migrations à risque dans `05_STRATEGIE_DONNEES_ET_MIGRATIONS.md`.
- Ce workflow doit utiliser la **révision effectivement destinée à la mise en production** et être coordonné avec les versions applicatives. Un lancement manuel depuis `main` alors que plusieurs releases se succèdent n'est pas intrinsèquement sûr.
- Ne pas exécuter le workflow sur une base Production tant que les modes d'autorisation, de restauration et de promotion n'ont pas été testés dans une base de validation.

### 11.3 Politique `expand -> migrate -> contract`

| Phase | Changement | Compatibilité | Vérification |
|---|---|---|---|
| Expand | Ajouter une colonne nullable ou table compatible | Ancienne et nouvelle versions | Migration non destructive sur base de recette |
| Migrate | Déployer code compatible et, si nécessaire, réécrire les données | Ancienne + nouvelle versions durant transition | E2E et contrôle de migration |
| Contract | Supprimer ancien champ ou contrainte après transition | Nouvelle version uniquement | Fenêtre de maintenance/validation adaptée |

Ne pas confondre les migrations Django du modèle et une transaction applicative : certaines opérations PostgreSQL et certains volumes peuvent nécessiter un plan dédié, un `RunPython` maîtrisé ou un job de traitement séparé.

### 11.4 Exigence de séquencement avec le déploiement automatique

**Premier lancement :** appliquer le schéma initial à une base Neon dédiée avant de rendre l'interface CRUD accessible sur Production. Enregistrer le SHA et le résultat de la migration.

**Évolution compatible :** réaliser la migration `expand` au bon moment, puis laisser le déploiement automatique publier le code compatible. Le test de compatibilité doit couvrir la version actuellement servie et la version future.

**Évolution incompatible :** ne pas se contenter d'un push sur `main`. Ajouter une politique de **promotion tenue en attente**, ou organiser une release manuelle/maintenance avec séquence explicitement validée. Le mécanisme effectif est à confirmer dans le runbook et doit empêcher l'exposition d'une combinaison code/schéma invalide.

---

## 12. R3.3 - Pipeline de livraison et smoke tests

### 12.1 Scénario de pull request de référence

```mermaid
sequenceDiagram
    autonumber
    actor D as Développeur
    participant G as GitHub
    participant A as GitHub Actions
    participant V as Vercel Preview
    participant N as Neon Preview isolé
    D->>G: Push feat/records puis PR
    G->>A: Exécuter CI
    A->>A: Lint, tests, migration CI PostgreSQL
    G->>V: Créer Preview
    V->>N: Connexion DB Preview uniquement
    D->>V: Tester CRUD synthétique
    D->>G: Revue et corrections
    A-->>G: Checks requis réussis
    G-->>D: PR éligible à la fusion
```

### 12.2 Scénario de production de référence

```mermaid
sequenceDiagram
    autonumber
    actor O as Mainteneur
    participant G as GitHub
    participant R as Migration contrôlée
    participant V as Vercel
    participant N as Neon Production
    O->>G: Fusion PR validée sur main
    G->>V: Construction du nouveau déploiement
    opt Changement de schéma
        O->>R: Autoriser migration compatible au moment prévu
        R->>N: Application contrôlée des migrations
        N-->>R: Historique et contrôle de résultat
    end
    V->>V: Promotion selon gates réellement configurés
    O->>V: Smoke test HTTPS et Admin
    V->>N: Lire Record de test autorisé
    N-->>V: Record conservé
    O->>O: Enregistrer SHA, release, preuves, GO/NO-GO
```

> Le diagramme illustre une séquence de release **coordonnée**, pas la garantie qu'une intégration standard Vercel attendra le job de migration. En cas de changement incompatible, la promotion doit être effectivement contrôlée avant que le domaine cible ne pointe vers le nouveau code.

### 12.3 Smoke tests obligatoires

| ID | Scénario | Attendu |
|---|---|---|
| SM-01 | `GET /` en HTTPS | HTTP 200 et page HTML attendue |
| SM-02 | Asset `/static/css/app.css` | HTTP 200, ressource CSS |
| SM-03 | `GET /admin/` anonyme | Redirection/authentification, aucune donnée ouverte |
| SM-04 | Connexion avec compte test autorisé | Session fonctionne et cookies adaptés |
| SM-05 | Création d'un `Record` fictif | Persistance sur Neon correspondant à l'environnement |
| SM-06 | Redéploiement d'une version compatible | Même Record retrouvé sans changement inattendu |
| SM-07 | Preview modifie son Record | Aucune modification ni lecture non autorisée en Production |
| SM-08 | Logs et version | SHA et erreurs consultables sans secret |
| SM-09 | Mise en échec de CI | Fusion normale refusée |
| SM-10 | Mauvaise release contrôlée sur environnement de test | Procédure de rollback code démontrée |

Les scénarios qui créent des données doivent utiliser des environnements et des comptes dédiés à la recette, ou des données explicitement autorisées, sans risque de pollution de la production réelle.

### 12.4 Preuves de déploiement

Pour chaque tentative de release, conserver au minimum :

```text
Release ID :
Date / heure :
GitHub PR :
SHA Git :
CI GitHub Actions : PASS / FAIL
Vercel Deployment ID :
Environnement : Preview / Production
Neon branch / database (identifiant NON secret) :
Migrations requises : OUI / NON
Migration job / approbateur :
Smoke tests : PASS / FAIL
Anomalies :
Décision : GO / NO-GO
```

Ne jamais consigner des URL de connexion PostgreSQL contenant un mot de passe dans ce registre.

---

## 13. R3.4 - Exploitation, observabilité et retour arrière

### 13.1 Journaux et traçabilité

- Relier chaque release à un SHA GitHub et à l'identifiant de déploiement Vercel.
- Collecter les logs de build, de fonction Django et de tests CI dans leurs interfaces respectives.
- Ne pas journaliser les `DATABASE_URL`, `DJANGO_SECRET_KEY`, cookies, tokens ou données métier sensibles.
- Prévoir des diagnostics de connexion PostgreSQL, erreurs HTTP et erreurs de migrations.
- Mesurer progressivement les quotas de fonctions, les connexions DB et les coûts.

### 13.2 Retour arrière applicatif

1. Identifier le dernier déploiement sain et les éventuelles migrations effectuées entre-temps.
2. Déterminer si le schéma actuel reste compatible avec l'ancienne version du code.
3. Utiliser le mécanisme de rollback/promotion Vercel autorisé pour revenir au code sain.
4. Réexécuter les smoke tests et contrôler les écritures.
5. Si le schéma n'est pas compatible, appliquer le **plan de reprise des données prévu**, ne pas improviser un `migrate <ancienne_version>` ou une suppression de tables.
6. Documenter l'incident, le responsable, les pertes ou risques et les mesures correctives.

### 13.3 Sauvegarde et reprise des données

- Connaître les capacités de restauration associées au **plan Neon réellement choisi**, la fenêtre de récupération et les restrictions.
- Tester une restauration sur une base **non productive** et comparer les données attendues.
- Ne jamais supposer qu'un rollback Vercel restaure la base PostgreSQL : **les deux opérations sont indépendantes**.
- Définir la responsabilité de décision sur tout écrasement ou perte de données.

### 13.4 Budget et quotas

Le tableau de suivi reprend les plans réellement souscrits, les quotas consommés et la date de dernière vérification. Une application commerciale doit utiliser une offre et des conditions d'exploitation compatibles avec son usage, même si un prototype technique fonctionnerait avec des quotas gratuits.

---

## 14. R4 - Cloudflare optionnel

| Besoin observé | Service Cloudflare envisageable | Décision de départ |
|---|---|---|
| Domaine personnalisé | DNS Cloudflare | Activer en **DNS-only** pour les enregistrements liés à Vercel |
| Formulaire public exposé aux abus | Turnstile | Vérification serveur obligatoire si activé |
| Téléversements utilisateurs | R2 (ou stockage objet alternatif) | Comparer les solutions et en choisir une |
| Exigence edge supplémentaire prouvée | Proxy/WAF Cloudflare | Étudier les interactions avec Vercel avant activation |

**Ne pas mettre Cloudflare en proxy orange par automatisme.** Une configuration DNS-only ne place pas le WAF Cloudflare sur le trajet HTTP. Vercel assure alors directement HTTPS/CDN pour l'application. R2 n'est pas nécessaire pour `collectstatic` ; son usage concerne les médias persistants des utilisateurs si ce besoin apparaît.

---

## 15. R5 - Industrialisation proportionnée

- Réexécuter le bootstrap depuis un clone vierge et établir un guide de réutilisation.
- Étudier les améliorations de sécurité de la chaîne CI : actions figées sur SHA, revue des dépendances, droits GitHub réduits, journaux conservés.
- Améliorer la qualité du runtime avec quelques mesures réelles : latence, cold start, échecs, connexions PostgreSQL, coût.
- N'introduire DRF, React, un worker, un workflow durable ou un Py**Kit que si une story métier et ses critères d'acceptation le justifient.
- Ne pas transformer le starter en framework maison généraliste avant d'avoir au moins une première application utilisatrice.

---

## 16. Points de contrôle et GO / NO-GO

### 16.1 Gates par phase

| Gate | Condition obligatoire | Preuve | Bloque si |
|---|---|---|---|
| G0 | OA critiques, plan/région/dépôt confirmés | Décision R0 | Usage/plan non conformes |
| G1 | Django local CRUD/Auth/tests opérationnel | Tests, bootstrap | CRUD/permissions défaillants |
| G2 | PR CI verte/rouge testée, fusion protégée, URL Vercel HTTPS | Runs, déploiement, SHA | CI non bloquante ou secrets exposés |
| G3 | Neon persistant, Preview isolée, migrations séparées et maîtrisées | Test sentinelles, migration, persistance | Preview sur Prod, migration risquée |
| G4 | `CA-01` à `CA-13` conformes, runbook et rollback testés | PV GO / NO-GO | Critère critique non validé |

### 16.2 Matrice de traçabilité des 13 critères MVP

| Critère | Ce qui doit être démontré | Étape | Stories |
|---|---|---|---|
| CA-01 | Clone vierge, installation et démarrage local | R1.1 | US-005, US-017 |
| CA-02 | Application Django accessible en HTTPS | R2.2 | US-018, US-019 |
| CA-03 | CRUD connecté à PostgreSQL Neon | R3.1 | US-008/009, US-025 |
| CA-04 | Données conservées après redéploiement | R3.3 | US-020, US-028 |
| CA-05 | CI automatique sur PR | R2.1 | US-013/014 |
| CA-06 | Règles de fusion réellement bloquantes | R2.1 | US-016 |
| CA-07 | Déploiement sur `main` démontré | R2.2 | US-020 |
| CA-08 | Preview n'écrit pas sur Production | R3.1/R3.2 | US-021/026/031 |
| CA-09 | Auth/Admin/permissions sécurisés | R1.2/R3.4 | US-010/032/033 |
| CA-10 | Aucun secret réel dans Git | R1.1/R2.1 | US-006/013/034 |
| CA-11 | Migrations indépendantes et contrôlées | R3.2 | US-015/027 |
| CA-12 | Diagnostic, rollback et exploitation documentés | R3.4 | US-023/036/037/043 |
| CA-13 | Plan d'hébergement compatible avec l'usage | R0 | US-004/038 |

### 16.3 Conditions de NO-GO immédiat

- Preview configurée avec une URL de la base Production ou données sensibles non autorisées.
- Job PR disposant d'un secret Production ou droits privilégiés non justifiés.
- Migrations exécutées depuis un build Vercel ou au démarrage Django.
- Absence de contrôle des permissions pour l'Admin ou les écritures métier.
- Secret exposé dans les sources, un log ou une variable publique.
- Offre d'hébergement incompatible avec la nature réelle de l'application.
- Une modification de schéma invalide est rendue visible sans politique de compatibilité ou gate effectif.
- Critère d'acceptation obligatoire non démontré.

---

## 17. Dépendances, responsabilités et décisions

### 17.1 RACI simplifié

| Activité | Responsable de décision | Exécutant | Validation |
|---|---|---|---|
| Dépôt et accès GitHub | Propriétaire | Mainteneur | Politique de permissions |
| Choix du plan Vercel/Neon | Propriétaire | Mainteneur | Conformité et budget |
| Code Django et tests | Mainteneur | Développeur | CI et revue |
| Secret Production et migrations | Propriétaire/exploitant habilité | Workflow autorisé | Approbation + logs |
| Intégration Preview | Mainteneur | Vercel/Neon configurés | Test d'isolation |
| GO / NO-GO | Propriétaire désigné | Équipe de recette | PV de recette |

Une même personne peut tenir plusieurs rôles pour ce starter, mais la décision sensible reste distincte de l'exécution automatique.

### 17.2 Dépendances non techniques

- Consentement à toute création de service ou facturation potentielle.
- Conditions de licences du code et de publication du dépôt.
- Résidence et confidentialité des données selon l'application future.
- Disponibilité réelle des protections de branches, d'environnements GitHub et des Deployment Checks dans les plans utilisés.

---

## 18. Risques, tests négatifs et mesures préventives

| Risque | Niveau | Détection | Mesure / responsable |
|---|---|---|---|
| Preview rattachée à Production | Critique | Sentinelles, audit credentials/scope | US-026, responsable des données |
| Branches Neon contenant une copie de données personnelles | Critique | Vérification du parent et du dataset | Source synthétique, US-035 |
| Migration au build ou lors du bootstrap HTTP | Critique | Revue config, tests négatifs | Workflow séparé US-027 |
| Release code/schéma incompatible | Critique | Matrice de compatibilité et smoke test | Expand/migrate/contract, gates |
| Déploiement exposé avant résultat CI | Élevé | Test release volontairement invalide | Protection main + gate Vercel si requis |
| Secret dans Git/Actions/tracebacks | Élevé | Scan et revue | Scopes séparés, rotation |
| Rollback code supposé restaurer données | Élevé | Exercice de reprise | Procédure DB indépendante |
| Problèmes pool PostgreSQL et cold start | Moyen | Logs, connexion, latence | Pooling et mesure |
| Dépassement quotas / plan inadéquat | Moyen/élevé | Revue mensuelle ou au changement | Registre des plans |
| Double proxy Cloudflare/Vercel | Moyen | Essai HTTP/DNS | DNS-only par défaut |

---

## 19. Plan d'exécution immédiat : première tranche

**Tranche à réaliser en priorité, avant toute infrastructure externe :**

1. Valider les OA bloquants R0 et le cas `Record`.
2. Initialiser `django-cloud-starter` avec Python 3.12, Django 5.2 LTS, `uv` et `uv.lock` si les versions sont confirmées.
3. Mettre en place `config/settings.py` et `.env.example` conformes à `03`.
4. Créer `apps.core` et `apps.records`, la page d'accueil, la première migration et l'Admin.
5. Ajouter login/logout, permissions, tests des modèles, des formulaires et des routes.
6. Exécuter Ruff, `makemigrations --check`, `manage.py check` et tests locaux.
7. Documenter la commande de démarrage depuis un clone neuf.
8. Enregistrer les preuves R1.1 et R1.2, puis seulement **ouvrir l'intégration GitHub/Vercel**.

### 19.1 Check-list de première tranche

- [ ] `pyproject.toml` vérifié, `uv.lock` créé, Python minor fixé.
- [ ] `manage.py` à la racine, config WSGI valide.
- [ ] `APP_ENV=local`, `.env` ignoré et clé locale générée.
- [ ] `Record` et migration initiale disponibles.
- [ ] Formulaires et CRUD testés.
- [ ] Auth/Admin et contrôle d'accès testés.
- [ ] `uv run ruff check .` réussi.
- [ ] `uv run python manage.py test` réussi.
- [ ] `uv run python manage.py makemigrations --check --dry-run` réussi.
- [ ] README reproductible.

**Condition d'arrêt :** ne pas créer de services externes juste pour résoudre un défaut de configuration ou de conception qui peut être testé localement.

---

## 20. Livrables attendus par phase

| Phase | Livrables techniques | Livrables probants |
|---|---|---|
| R0 | Arbitrages OA ; choix versions, dépôt, région, plan | Registre de décision approuvé |
| R1 | Django, templates, Auth/Admin, modèles, migrations, tests | Tests locaux et bootstrap |
| R2 | `.github/workflows/ci.yml`, dépôt, intégration Vercel | PR CI verte/rouge, URL, SHA |
| R3 | Neon isolé, release migrations, smoke tests, logs | Test sentinelles, rapport de persistance, exercice rollback |
| R4 | Configuration DNS/Turnstile/objet seulement si demandée | Tests spécifiques et coût/risque |
| R5 | Starter durci, guide de réutilisation, mesures | Deuxième bootstrap, décisions de maintenance |

---

## 21. Documents suivants et limites

### 21.1 Documentation à produire au bon moment

| Document | Rôle | Avant quelle activité ? |
|---|---|---|
| `05_STRATEGIE_DONNEES_ET_MIGRATIONS.md` | Détail des branches Neon, contrats de données, rôles, opérations de migration, reprise et tests de restauration | Avant R3 et toute migration Production |
| `06_STRATEGIE_TESTS_ET_ACCEPTATION.md` | Cas de tests, jeux de données, preuves et recette `CA-01` à `CA-13` | Avant la recette GO / NO-GO |
| `07_RUNBOOK_DEPLOIEMENT_ET_EXPLOITATION.md` | Exploitation réelle, déploiements, incidents, rollback, coûts et contact d'astreinte si applicable | Avant le GO MVP |
| `08_OPTIONS_CLOUDFLARE_ET_EVOLUTIONS.md` | Arbitrage DNS, Turnstile, stockage objet et évolution de l'architecture | Au besoin R4/R5 |

Le présent plan **ne crée pas automatiquement** le dépôt, les projets Vercel/Neon, les secrets, les protections GitHub ou le code Django. Il précise leur ordre de mise en oeuvre et les preuves nécessaires pour les déclarer livrés.

### 21.2 Critère de réussite du document

Ce plan est prêt à être utilisé si le mainteneur peut :

- Sélectionner le prochain travail sans ambiguïté.
- Associer une tâche à une user story et à un critère CA.
- Savoir quelle variable appartient à quel environnement.
- Expliquer pourquoi **CI réussie**, **déploiement créé**, **promotion Production** et **migration appliquée** sont des événements différents.
- Détecter un risque critique de Preview ou de migration avant de déployer.
- Consigner une preuve et arrêter une release en NO-GO lorsque nécessaire.

---

## Annexe A - Exemples de commandes de recette

```bash
# Sur une machine de développement propre
uv sync --locked
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py test
uv run ruff check .
uv run ruff format --check .

# Depuis un environnement dédié de recette, avec les variables appropriées
uv run python manage.py migrate --plan
uv run python manage.py showmigrations --plan

# Exemple de consultation HTTP : remplacer l'URL par un domaine vérifié
curl -I https://<DOMAINE_VERIFIE>/
curl -I https://<DOMAINE_VERIFIE>/static/css/app.css
```

**Précaution :** les placeholders `<...>` ne sont pas des URL réelles. Ne pas substituer des secrets ni des URL PostgreSQL dans des lignes de commande conservées dans un historique public.

## Annexe B - Sources techniques vérifiées au 18 novembre 2026

1. **Django sur Vercel** : https://vercel.com/docs/frameworks/full-stack/django
   - Détection de Django avec `manage.py`, WSGI/ASGI et collecte automatique des fichiers statiques si `STATIC_ROOT` est défini.
2. **Runtime Python Vercel** : https://vercel.com/docs/functions/runtimes/python
   - Versions Python prises en charge et `pyproject.toml`/`uv.lock`.
3. **Intégration Git Vercel** : https://vercel.com/docs/git/vercel-for-github
   - Déploiements sur commits et pull requests.
4. **Vercel Deployment Checks** : https://vercel.com/docs/deployment-checks
   - Possibilité de retenir la promotion jusqu'à validation de checks GitHub, avec contraintes de configuration.
5. **Neon Native Vercel Integration** : https://neon.com/blog/neon-vercel-native-integration
   - Branches de prévisualisation, options de connexion et risques liés au parent des branches.
6. **Neon Branching & Data Privacy** : https://neon.com/blog/branching-environments-anonymized-pii
   - Les branches peuvent reproduire les données et le schéma du parent ; anonymisation possible sous conditions.
7. **Django deployment checklist** : https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
   - Vérifications sécurité avant déploiement, `manage.py check --deploy`.
8. **GitHub Actions PostgreSQL service** : https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers
   - PostgreSQL de CI via conteneur de service.
9. **uv dans GitHub Actions** : https://github.com/astral-sh/setup-uv
   - Installation de `uv` et options de cache.
10. **Vercel Hobby** : https://vercel.com/docs/plans/hobby
   - Vérifier les conditions d'utilisation de l'offre choisie avant toute activité commerciale.

**Politique d'actualité :** les fonctionnalités des plans, limites, intégrations et prérequis des GitHub Actions évoluent. Revalider ces documents lors de l'implémentation et avant toute modification sur des comptes réels.

## Annexe C - Journal des versions

| Version | Date | Changement |
|---|---|---|
| 1.0 | 18 novembre 2026 | Plan R0-R5, workflow CI PostgreSQL temporaire, modèle de migration manuelle et autorisée, politique de promotion, tests et gates. |
