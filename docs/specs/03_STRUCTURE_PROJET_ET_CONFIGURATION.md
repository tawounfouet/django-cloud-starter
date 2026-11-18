# 03 - Structure du projet et configuration

## Socle Django + GitHub + Vercel + Neon + Cloudflare

| Champ | Valeur |
|---|---|
| Document | `03_STRUCTURE_PROJET_ET_CONFIGURATION.md` |
| Version | 1.0 |
| Date | 18 novembre 2026 |
| Statut | **Proposition technique pré-implémentation** |
| Projet de référence | `django-cloud-starter` (nom provisoire, OA-03) |
| Documents amont | `00_DJANGO_GITHUB_VERCEL_NEON_CLOUDFLARE_EXPRESSION_DU_BESOIN.md` ; `01_ARCHITECTURE_ET_DECISIONS.md` ; `02_BACKLOG_ET_USER_STORIES.md` |
| Périmètre principal | R1 : Django local ; préparation de R2 : GitHub/Vercel ; R3 : Neon |
| Principe directeur | **Un monolithe Django modulaire, réutilisable et peu configuré** |

> **Objet** : préciser la structure cible du dépôt, les conventions de code, les composants indispensables, les fichiers de configuration, les paramètres d'exécution et les règles d'isolation. Le document contient des exemples de fichiers servant de spécification d'implémentation ; **il n'affirme pas que le projet ou les services ont déjà été créés**.
>
> **Décision essentielle** : utiliser le fonctionnement natif Django détecté par Vercel, sans ajouter l'ancienne structure `/api/`, sans `vercel.json` par défaut, sans React, sans Docker d'application obligatoire et sans Cloudflare dans le chemin HTTP par défaut.

---

## 1. Positionnement de ce document

### 1.1 Objectifs

1. Permettre un **clone vierge** puis un lancement local reproductible.
2. Établir une structure lisible, suffisamment modulaire pour accueillir de futures applications.
3. Fournir un **unique système de configuration par variables d'environnement** pour `local`, `ci`, `preview`, `production`.
4. Définir la séparation entre code Django, persistance Neon et déploiement Vercel.
5. Empêcher que des secrets, des données ou des migrations de production soient accidentellement utilisés dans un contexte non productif.
6. Préparer les user stories R1 et R2 sans faire dépendre le développement local de comptes externes.

### 1.2 Résultat observable

À la sortie du jalon R1, le mainteneur peut installer le projet, configurer un environnement de développement, lancer Django, créer un compte administrateur, afficher une page publique, gérer un `Record` de démonstration et exécuter les tests.

L'accès public HTTPS, les previews Vercel, les branches Neon et les migrations de production constituent des preuves complémentaires R2/R3, **pas des prérequis pour vérifier le squelette local**.

### 1.3 Choix confirmé et choix restant ouverts

| Sujet | Proposition opérationnelle | Statut |
|---|---|---|
| Organisation du dépôt | Monorepo contenant une seule application Django | Retenue pour starter |
| Domaine d'exemple | `records`, modèle `Record` | Hypothèse OA-04 |
| Backend | Django 5.2 LTS | Version candidate, confirmer OA-05 avant verrouillage |
| Python | Python 3.12 | Version candidate compatible Vercel, confirmer OA-05 |
| Gestionnaire Python | `uv` et `uv.lock` | Recommandation à valider |
| Frontend | Django Templates et CSS, JavaScript ciblé | Retenue |
| Administration et utilisateurs | Django Admin et Django Auth | Retenue |
| Configuration Django | `config/settings.py` unique et variables explicites | Retenue pour simplifier R1 |
| DB locale | SQLite autorisé uniquement en local ; PostgreSQL en CI/Preview/Production | Retenue |
| Entrée Vercel | WSGI via `config.wsgi.application` | Retenue |
| Écriture de fichiers | Statiques de build ; pas de médias utilisateurs au MVP | Retenue |
| Cloudflare | Aucun service requis au lancement | Retenue |
| Repository GitHub | Compte, nom et visibilité à confirmer | OA-02/OA-03 |
| Utilisation commerciale | À confirmer avant choix du plan Vercel | OA-01 |

Le choix d'un `settings.py` unique affine l'arborescence illustrative du document `01`, **sans changement d'ADR** : le projet est petit, et les quatre environnements restent séparés par configuration. Un package `config/settings/` avec `base.py`, `local.py`, `ci.py`, `preview.py`, `production.py` sera introduit uniquement si le fichier devient difficile à maintenir.

---

## 2. Architecture logique et frontières

```mermaid
flowchart LR
    DEV[Développeur Python] -->|Commit / PR| G[GitHub]
    G -->|CI| A[GitHub Actions]
    G -->|Intégration Git| V[Vercel]
    U[Utilisateurs] -->|HTTPS| V
    V --> D[Django WSGI]
    D --> T[Templates / Admin / Auth]
    D --> S[Services métier simples]
    S --> O[Django ORM]
    O <-->|PostgreSQL chiffré| N[(Neon)]
    CF[Cloudflare DNS - optionnel] -. Résolution DNS .-> V
    R2[Stockage objet - optionnel] -. Médias ultérieurs .-> D
```

**Frontières à respecter :**

- GitHub versionne les sources, la configuration non sensible et les migrations.
- GitHub Actions teste, contrôle et prépare les releases ; il ne détient pas par défaut l'accès à la base de production pour les jobs de pull request.
- Vercel construit et exécute l'application ; ses instances web ne sont pas une source de stockage durable.
- Django est responsable du domaine, des requêtes HTTP, des formulaires, des permissions et des transactions.
- Neon conserve les données transactionnelles et fournit les environnements PostgreSQL séparés.
- Cloudflare ne doit être activé que pour un besoin identifié : nom de domaine, Turnstile ou stockage objet notamment.

---

## 3. Arborescence cible du dépôt

```text
django-cloud-starter/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                      # CI de qualité et tests des PR
│   │   └── release-migrate.yml         # P1/R3, migration séparée et autorisée
│   ├── ISSUE_TEMPLATE/
│   │   └── user-story.md               # P1, reprise des stories du document 02
│   └── pull_request_template.md        # P1
│
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_home.py
│   └── records/
│       ├── __init__.py
│       ├── apps.py
│       ├── admin.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       ├── views.py
│       ├── services.py                  # Seulement si un cas métier le justifie
│       ├── migrations/
│       │   └── __init__.py
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py
│           ├── test_forms.py
│           ├── test_views.py
│           └── test_permissions.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py                       # Configuration canonique, par APP_ENV
│   ├── urls.py                           # URLConf racine
│   ├── wsgi.py                           # Entrée HTTP retenue pour Vercel
│   └── asgi.py                           # Réservé à une évolution ASGI
│
├── templates/
│   ├── base.html
│   ├── core/
│   │   └── home.html
│   ├── registration/
│   │   └── login.html
│   └── records/
│       ├── record_list.html
│       ├── record_detail.html
│       ├── record_form.html
│       └── record_confirm_delete.html
│
├── static/
│   └── css/
│       └── app.css
│
├── docs/
│   ├── 00_DJANGO_GITHUB_VERCEL_NEON_CLOUDFLARE_EXPRESSION_DU_BESOIN.md
│   ├── 01_ARCHITECTURE_ET_DECISIONS.md
│   ├── 02_BACKLOG_ET_USER_STORIES.md
│   ├── 03_STRUCTURE_PROJET_ET_CONFIGURATION.md
│   └── operations/                     # R3, procédures de release et incidents
│
├── scripts/
│   └── README.md                        # Scripts facultatifs, pas de secret
│
├── .env.example                         # Exemple public, valeurs factices
├── .gitignore
├── .python-version                       # Version Python explicite
├── .pre-commit-config.yaml              # Optionnel, à adopter si utile
├── manage.py
├── pyproject.toml
├── uv.lock                               # Résolution complète verrouillée
├── README.md
└── LICENSE                               # Selon visibilité et licence choisies

# Artefacts locaux générés, à NE PAS versionner :
# .env, .env.local, .venv/, db.sqlite3, staticfiles/, .pytest_cache/, .ruff_cache/
```

### 3.1 Arborescence progressive et non dogmatique

La structure ci-dessus est la **cible logique**. Elle n'oblige pas à créer dès R1 les workflows de migration, les templates non encore utilisés, les scripts ou les répertoires d'opérations. Les fichiers réellement créés doivent correspondre aux stories implémentées et aux chemins référencés dans les réglages.

### 3.2 Convention de nommage

| Objet | Convention | Exemple |
|---|---|---|
| Dépôt | `kebab-case` | `django-cloud-starter` |
| Package Python | `snake_case` | `config`, `apps.records` |
| App Django | Nom métier au pluriel si naturel | `records` |
| Modèle | PascalCase, singulier | `Record` |
| Fonction / module | `snake_case` | `create_record` |
| Template | Dossier métier, nom explicite | `records/record_form.html` |
| Variable d'environnement | `UPPER_SNAKE_CASE` | `DJANGO_ALLOWED_HOSTS` |
| Test | `test_<behavior>.py` | `test_permissions.py` |
| Migrations | Générées par Django | `0001_initial.py` |
| Documentation | Préfixe numérique et sujet | `03_STRUCTURE_PROJET_ET_CONFIGURATION.md` |

Ne pas employer `core` comme fourre-tout métier. `core` représente les routes et composants transverses **très limités**, par exemple accueil et page d'état simple. Les règles de `Record` restent dans `records`.

---

## 4. Responsabilités des packages et dépendances

| Emplacement | Responsabilité | Autorisé | À éviter |
|---|---|---|---|
| `config/` | Entrées WSGI/ASGI, URL racine, paramètres | Configuration, composition | Règles métier |
| `apps/core/` | Page d'accueil et composants simples communs | Vue, URL, helpers ciblés | Dépôt de code de tous les modules |
| `apps/records/models.py` | Schéma ORM et invariants simples | `Model`, contraintes, méthodes courtes | Appels HTTP externes |
| `apps/records/forms.py` | Validation de saisie et formulaires | `ModelForm`, contrôles de champs | Politique métier contradictoire avec modèle |
| `apps/records/views.py` | Entrée HTTP, permissions, orchestration courte | CBV/FBV Django, `login_required` | Transactions transversales complexes |
| `apps/records/services.py` | Cas d'usage à plusieurs étapes, si besoin | `transaction.atomic`, règles coordonnées | Wrapper artificiel pour chaque méthode ORM |
| `apps/records/admin.py` | Administration native | `ModelAdmin` | Contournement des invariants métier |
| `apps/records/tests/` | Cas métier et contrôles de sécurité | Tests déterministes | Dépendance à la base Production |
| `templates/` | Affichage et formulaires | Templates Django, `csrf_token` | Décisions d'autorisation seulement côté HTML |
| `static/` | Code CSS/JS et images de distribution | Ressources versionnées | Fichiers utilisateur, secrets |
| `scripts/` | Opérations explicites | Vérifications, outils idempotents | Migrations automatiques au build |

### 4.1 Flux d'un CRUD

```mermaid
sequenceDiagram
    participant B as Navigateur
    participant V as Vue Django
    participant F as Formulaire Django
    participant S as Service optionnel
    participant O as ORM
    participant N as PostgreSQL
    B->>V: POST /records/new/
    V->>V: Authentification et permission
    V->>F: Valider les données
    alt Formulaire invalide
        F-->>V: Erreurs de validation
        V-->>B: Page avec erreurs
    else Formulaire valide
        F-->>V: Données validées
        V->>S: Cas d'usage si nécessaire
        S->>O: Écriture transactionnelle
        O->>N: INSERT
        N-->>O: Identifiant du Record
        O-->>S: Record persistant
        S-->>V: Résultat
        V-->>B: Redirection vers fiche
    end
```

**Règle d'économie d'abstraction** : les opérations CRUD simples peuvent utiliser directement `ModelForm`, vues génériques et ORM Django. La couche `services.py` n'est pas obligatoire tant qu'elle ne porte pas un cas d'usage identifiable.

---

## 5. Domaine de démonstration `records`

### 5.1 Entité minimale

| Champ | Type logique | Règle |
|---|---|---|
| `id` | Identifiant natif Django | Immuable, unique |
| `title` | Texte court | Obligatoire, taille limitée |
| `description` | Texte long | Facultatif |
| `status` | Enum | `draft`, `active`, `archived` |
| `created_at` | Datetime | Attribution serveur à la création |
| `updated_at` | Datetime | Mise à jour serveur |
| `created_by` | FK utilisateur, si nécessaire | Option explicite à trancher avant les permissions objet |

### 5.2 Exemple de modèle cible

```python
# apps/records/models.py
from django.conf import settings
from django.db import models


class Record(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        ACTIVE = "active", "Actif"
        ARCHIVED = "archived", "Archivé"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_records",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
```

**Remarque :** cet exemple fait de l'utilisateur créateur un élément obligatoire. Si le scénario de référence est un simple catalogue partagé, il est possible de retirer `created_by` lors du cadrage R0. En revanche, les tests de sécurité devront refléter le modèle effectivement choisi.

### 5.3 Principes d'autorisation

- La lecture et l'écriture doivent être déterminées **côté serveur**.
- Un visiteur anonyme ne peut pas créer, modifier ou supprimer un `Record` protégé.
- Si les `Record` sont privés à leur auteur, filtrer les `QuerySet` par `created_by=request.user` et refuser les modifications d'un objet étranger, y compris en manipulant une URL.
- Les comptes `staff` et `superuser` n'ont pas à être publics ; leur création relève d'une commande administrateur contrôlée.
- Les templates ne remplacent jamais la vérification des permissions.

---

## 6. Politique de versions et dépendances

### 6.1 Versions candidates au 18 novembre 2026

| Élément | Cible recommandée | Motif |
|---|---|---|
| Python | **3.12** | Version mature, officiellement supportée par le runtime Vercel |
| Django | **5.2 LTS**, série `>=5.2,<5.3` | Maintien long et stabilité pour le starter |
| PostgreSQL | Version fournie par Neon, à relever | Moteur transactionnel réel |
| `psycopg` | Série 3 | Driver PostgreSQL maintenu |
| `dj-database-url` | Version compatible Django retenu | Configuration depuis `DATABASE_URL` |
| `python-dotenv` | Version maintenue | Chargement du `.env` **uniquement local** |
| `pytest` / `pytest-django` | Versions compatibles | Tests lisibles et reproductibles |
| `ruff` | Version verrouillée | Lint/format rapides |
| `uv` | Version d'outil documentée | Gestion de projet et lockfile |

Les versions exactes des dépendances seront produites dans `uv.lock` lors de l'implémentation. La fourchette Django indiquée est une **proposition**, non une preuve que toutes les bibliothèques sont compatibles. Vérifier OA-05 avant intégration R1.

### 6.2 Dépendances MVP

```toml
# pyproject.toml - exemple cible, à résoudre par uv
[project]
name = "django-cloud-starter"
version = "0.1.0"
description = "Socle Django pour GitHub, Vercel et Neon"
requires-python = ">=3.12,<3.13"
dependencies = [
  "Django>=5.2,<5.3",
  "psycopg[binary]>=3.2,<4",
  "dj-database-url>=2.2,<4",
  "python-dotenv>=1,<2",
]

[dependency-groups]
dev = [
  "pytest",
  "pytest-django",
  "ruff",
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings"
testpaths = ["apps"]
python_files = ["test_*.py"]

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]
```

**Pourquoi `<3.13` pour Python ici ?** L'exemple cible **une seule version mineure** pour éviter une divergence local/CI/Vercel durant le POC. Ce n'est pas une limite générale de Django ou Vercel : Python 3.13/3.14 peuvent être évalués après les tests de compatibilité.

### 6.3 Ajout et mise à jour des dépendances

```bash
# Installation de uv : suivre la documentation officielle du système utilisé
uv python install 3.12
uv init --no-package --python 3.12
uv add "Django>=5.2,<5.3" "psycopg[binary]>=3.2,<4" \
  "dj-database-url>=2.2,<4" "python-dotenv>=1,<2"
uv add --dev pytest pytest-django ruff
uv lock
uv sync --locked
```

Dans un dépôt existant, **ne pas relancer `uv init`**. Cet exemple illustre le bootstrap d'un dépôt vierge ; le code et les versions effectives seront ajoutés pendant R1.

### 6.4 Règles de verrouillage

- Versionner `pyproject.toml`, `uv.lock` et `.python-version`.
- Utiliser `uv sync --locked` en CI pour détecter un lockfile incohérent.
- Garder les dépendances de production minimales ; séparer lint et test dans le groupe `dev`.
- Ne pas laisser une mise à jour implicite de dépendances décider de la version publiée.
- Examiner les changements de version et la sécurité des packages par pull request.
- Vérifier le comportement du builder Vercel avec le duo `pyproject.toml` et `uv.lock` réellement livré.

---

## 7. Stratégie de configuration par environnement

### 7.1 Un seul module canonique

Le MVP emploie `config/settings.py`. Les différences entre environnements **ne sont pas codées par URL de déploiement ou par branche Git** mais explicitées au moyen de variables contrôlées.

```mermaid
flowchart TD
    S[config/settings.py] --> E{APP_ENV}
    E --> L[local]
    E --> C[ci]
    E --> P[preview]
    E --> R[production]
    L --> LS[.env local ou variables shell]
    C --> CS[GitHub Actions + PostgreSQL isolé]
    P --> PS[Vercel Preview + base synthétique isolée]
    R --> RS[Vercel Production + Neon Production]
```

### 7.2 Contrat des quatre environnements

| Critère | `local` | `ci` | `preview` | `production` |
|---|---|---|---|---|
| Runtime | `runserver` | GitHub Actions | Vercel | Vercel |
| `DJANGO_DEBUG` | Peut être vrai | Faux | **Faux** | **Faux** |
| `DATABASE_URL` | Facultative ; SQLite local toléré | **Requise**, PostgreSQL isolé | **Requise**, Neon isolé | **Requise**, Neon prod |
| `DJANGO_SECRET_KEY` | Requise | Requise, valeur de test | Requise, dédiée | Requise, dédiée |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hôtes de test | Hôtes Preview exacts | Hôtes Production exacts |
| Migrations | Locales explicites | Base jetable | Base Preview exclusivement | Release indépendante du build |
| Données | Synthétiques | Synthétiques | **Synthétiques** | Réelles seulement si nécessaires |
| Cookies sécurisés | Selon HTTPS local | Mode test | Oui | Oui |
| HSTS | Désactivé local | Non pertinent | Évaluer prudemment | Activer progressivement après audit HTTPS |
| Secrets accessibles aux PR externes | Non | Aucun secret prod | Non | Non applicable |

### 7.3 Catalogue des variables

| Variable | Environnement | Secret ? | Obligatoire | Rôle / format |
|---|---|---:|---|---|
| `APP_ENV` | Tous | Non | Oui sur plateforme | `local`, `ci`, `preview`, `production` |
| `DJANGO_SECRET_KEY` | Tous | **Oui** | Oui | Secret Django unique par environnement |
| `DJANGO_DEBUG` | Local | Non | Non | `true` ou `false` ; ignoré hors local |
| `DJANGO_ALLOWED_HOSTS` | Tous | Non | Oui hors local | Hôtes séparés par virgule, **sans** schéma |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Public | Non | Si origins cross-host | Origines avec schéma, séparées par virgule |
| `DATABASE_URL` | Tous | **Oui** | Oui hors local | URI PostgreSQL de l'environnement, TLS |
| `DATABASE_URL_UNPOOLED` | R3, opérations | **Oui** | Selon procédure | URI Neon directe pour migration ou maintenance |
| `VERCEL_URL` | Vercel | Non | Fourni par Vercel | URL de déploiement, **pas une preuve d'autorisation** |
| `DJANGO_LOG_LEVEL` | Tous | Non | Non | `INFO`, `WARNING`, etc. |
| `DJANGO_SECURE_SSL_REDIRECT` | En ligne | Non | Après vérification proxy | Redirection HTTPS, à tester avec Vercel |
| `TURNSTILE_SITE_KEY` | R4 | Non | Seulement si Turnstile | Clé publique anti-bot |
| `TURNSTILE_SECRET_KEY` | R4 | **Oui** | Seulement si Turnstile | Vérification serveur des tokens |
| `R2_ACCOUNT_ID` | R4 | Non | Seulement si R2 | Compte Cloudflare |
| `R2_ACCESS_KEY_ID` | R4 | **Oui** | Seulement si R2 | Identifiant d'accès objet |
| `R2_SECRET_ACCESS_KEY` | R4 | **Oui** | Seulement si R2 | Secret d'accès objet |
| `R2_BUCKET_NAME` | R4 | Non | Seulement si R2 | Bucket médias |

**Convention :** utiliser `DJANGO_` pour les réglages propres au framework, `DATABASE_` pour la persistance et les noms explicites des fournisseurs pour les fonctions additionnelles. Ne pas créer des variantes personnelles (`DB_CONN`, `POSTGRES_DSN`, `PG_URL`) sans nécessité.

### 7.4 Exemple `.env.example`

```dotenv
# Copier en .env, puis remplacer toutes les valeurs locales.
# Ce fichier est public, ne jamais y écrire de vrai secret.
APP_ENV=local
DJANGO_SECRET_KEY=REPLACE_WITH_LOCAL_RANDOM_SECRET
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DJANGO_LOG_LEVEL=INFO

# Facultatif localement : laisser commenté pour SQLite de développement.
# DATABASE_URL=postgresql://local_user:local_password@localhost:5432/local_db

# Les variables réelles Neon Production, CI, Preview et les clés Cloudflare
# ne doivent pas figurer dans le .env.example.
```

**Important :** le marqueur `REPLACE_WITH_LOCAL_RANDOM_SECRET` est un placeholder, **pas un secret à utiliser en environnement exposé**. Une clé aléatoire peut être générée avec `django.core.management.utils.get_random_secret_key` dans un environnement local isolé, sans l'imprimer dans un journal partagé.

### 7.5 Exemple `.gitignore`

```gitignore
# Variables sensibles et environnements
.env
.env.*
!.env.example
.venv/
venv/

# Python et caches
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# SQLite local et fichiers produits
db.sqlite3
db.sqlite3-journal
staticfiles/
media/

# IDE, OS, outils
.idea/
.vscode/
.DS_Store
.vercel/
```

En complément, une vérification de secrets doit être exécutée en CI (US-013/034). Un `.gitignore` ne supprime pas un secret déjà présent dans l'historique Git : la révocation et la rotation restent nécessaires.

---

## 8. Spécification de `config/settings.py`

### 8.1 Principes impératifs

1. `APP_ENV` est une valeur autorisée, jamais une chaîne arbitraire.
2. Le `.env` n'est lu automatiquement **qu'en mode local**.
3. Le mode `ci`, `preview` ou `production` échoue si `DATABASE_URL` ou `DJANGO_SECRET_KEY` manque ; l'absence d'`APP_ENV` sur une plateforme Vercel ou un runner CI est également rejetée.
4. Le mode `preview` doit avoir sa propre source de données isolée. `APP_ENV=preview` n'est **pas** à lui seul une preuve d'isolation.
5. `DEBUG=True` est impossible en CI, Preview et Production.
6. `ALLOWED_HOSTS` n'est jamais ouvert à `*` en environnement public.
7. Les statiques sont préparés dans `STATIC_ROOT`, sans dépendance à un répertoire média local durable.
8. Les réglages réseau sensibles (proxy HTTPS, HSTS) ne sont activés qu'après vérification de leur comportement effectif.

### 8.2 Extrait de configuration de référence

Le code ci-dessous est un **squelette pédagogique complet sur les points structurants**, pas un fichier à utiliser sans revue. Le projet effectif devra ajouter et adapter les réglages générés par `startproject` (templates, internationalisation, middleware, etc.).

```python
# config/settings.py - extrait cible
import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

VALID_ENVS = {"local", "ci", "preview", "production"}

# L'environnement doit être explicite sur une plateforme distante.
if (os.getenv("VERCEL") or os.getenv("CI")) and not os.getenv("APP_ENV"):
    raise ImproperlyConfigured("APP_ENV est requis en déploiement ou en CI")

APP_ENV = os.getenv("APP_ENV", "local")
if APP_ENV not in VALID_ENVS:
    raise ImproperlyConfigured(f"APP_ENV non autorisé : {APP_ENV}")

if APP_ENV == "local":
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env", override=False)
    APP_ENV = os.getenv("APP_ENV", "local")
    if APP_ENV != "local":
        raise ImproperlyConfigured("Le .env local ne peut pas sélectionner un autre APP_ENV")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY or SECRET_KEY.startswith("REPLACE_WITH_"):
    raise ImproperlyConfigured("DJANGO_SECRET_KEY absent ou factice")

DEBUG = APP_ENV == "local" and os.getenv(
    "DJANGO_DEBUG", "false"
).strip().lower() == "true"


def csv_setting(name: str) -> list[str]:
    value = os.getenv(name, "")
    return [item.strip() for item in value.split(",") if item.strip()]


ALLOWED_HOSTS = csv_setting("DJANGO_ALLOWED_HOSTS")
if APP_ENV == "local" and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if APP_ENV in {"preview", "production"} and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS requis en ligne")
if APP_ENV != "local" and "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS wildcard interdit hors local")

CSRF_TRUSTED_ORIGINS = csv_setting("DJANGO_CSRF_TRUSTED_ORIGINS")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            ssl_require=APP_ENV in {"preview", "production"},
        )
    }
elif APP_ENV == "local":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    raise ImproperlyConfigured("DATABASE_URL PostgreSQL est requis hors local")

# Pour l'instant : une seule entrée WSGI active.
WSGI_APPLICATION = "config.wsgi.application"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

SESSION_COOKIE_SECURE = APP_ENV in {"preview", "production"}
CSRF_COOKIE_SECURE = APP_ENV in {"preview", "production"}
SECURE_CONTENT_TYPE_NOSNIFF = True

# Ne pas activer HSTS ou le réglage de proxy par hypothèse.
SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = False

# Exemples : INSTALLED_APPS, MIDDLEWARE, TEMPLATES,
# AUTH_PASSWORD_VALIDATORS et LOGGING sont définis dans le fichier réel.
```

### 8.3 Trois limites de cet extrait à connaître

**1. Base de données CI** : le garde-fou exige `DATABASE_URL` mais n'en vérifie pas à lui seul la propriété. Le workflow GitHub doit fournir un Postgres jetable et les tests négatifs doivent prouver l'absence d'accès à la base Production.

**2. Connexion Neon** : avec `ssl_require=True`, le parseur impose TLS sur Preview et Production. Les URL et exigences TLS doivent être comparées au format réellement fourni par Neon, sans afficher les identifiants. Pour les connexions locales à PostgreSQL, les règles TLS doivent être adaptées à l'environnement, pas présumées.

**3. HTTPS et proxy** : `SECURE_SSL_REDIRECT=False` et HSTS désactivé sont des **valeurs prudentes pour le premier bootstrap**, pas la politique finale de sécurité. Il faut vérifier le TLS terminé par Vercel, la reconnaissance de `request.is_secure()`, la configuration de proxy de confiance et les redirections avant de choisir les valeurs définitives. Ne jamais fixer `SECURE_PROXY_SSL_HEADER` sans vérifier qui peut injecter les en-têtes correspondants.

### 8.4 Fichier réel : réglages Django à conserver

Un `startproject` crée plusieurs réglages que l'extrait ci-dessus n'affiche pas :

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.records",
]

ROOT_URLCONF = "config.urls"
LOGIN_REDIRECT_URL = "/records/"
LOGOUT_REDIRECT_URL = "/"

# Conserver les middlewares standards Django (sécurité, sessions,
# CommonMiddleware, CSRF, authentification, messages, clickjacking)
# dans un ordre cohérent avec la version utilisée.

# TEMPLATES doit inclure BASE_DIR / "templates" dans DIRS,
# et garder les context processors nécessaires à Admin et Auth.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"
```

**Ne pas remplacer aveuglément** `MIDDLEWARE` ou `TEMPLATES` par un exemple tronqué. La configuration effective doit être vérifiée avec `manage.py check` et `manage.py check --deploy`.

### 8.5 `config/wsgi.py` et `manage.py`

```python
# config/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
```

```python
# manage.py - principe du point d'entrée CLI
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```

**Sélection du point d'entrée sur Vercel** : garder `WSGI_APPLICATION="config.wsgi.application"` dans les settings. Le fichier `asgi.py` peut exister mais **ne pas définir `ASGI_APPLICATION` dans les settings actives**. Si les deux variables sont définies, Vercel peut sélectionner ASGI. Une sélection explicite optionnelle est possible :

```toml
# Uniquement si la détection automatique n'est pas appropriée.
[tool.vercel]
entrypoint = "config.wsgi:application"
```

Le cas général ne nécessite ni dossier `/api/` ni `vercel.json`.

---

## 9. URLConf, templates, statiques et Administration

### 9.1 URLConf racine

```python
# config/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("records/", include("apps.records.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
```

Enregistrer `apps.core` et `apps.records` avec leur `AppConfig` correct ; veiller à ce que `apps/` contienne un `__init__.py` et que `name="apps.records"` pour l'application correspondante.

### 9.2 Conventions web

| Route | Rôle | Accès cible |
|---|---|---|
| `/` | Page d'accueil | Public |
| `/accounts/login/` | Connexion native Django | Public, rate limiting si besoin |
| `/accounts/logout/` | Déconnexion native | Selon comportement de la version Django |
| `/records/` | Liste | Authentifié |
| `/records/new/` | Création | Autorisé |
| `/records/<id>/` | Détail | Autorisé pour cet objet |
| `/records/<id>/edit/` | Modification | Autorisé pour cet objet |
| `/records/<id>/delete/` | Suppression | Autorisé, méthode POST confirmée |
| `/admin/` | Django Admin | `is_staff` / permissions administrateur |

**Attention** : l'URL et les attributs d'accès sont des contrats proposés ; leur disponibilité réelle doit être confirmée par les vues et les tests R1.

### 9.3 Templates

- Créer `base.html` comme enveloppe des pages.
- Utiliser `{% load static %}` et `{% static 'css/app.css' %}` pour charger CSS.
- Utiliser `{% csrf_token %}` dans les formulaires POST.
- Éviter de placer du JavaScript lourd ou des calculs métier dans les templates.
- Ne pas servir des `Record` privés en cache public sans stratégie adaptée.

### 9.4 Statiques vs médias

| Catégorie | Exemples | Emplacement MVP | Durabilité |
|---|---|---|---|
| Statiques versionnés | CSS, JS, logos | `static/` puis `STATIC_ROOT` à build | Versionnés, servis par Vercel CDN |
| Templates | HTML Django | `templates/` | Livrés avec le code |
| Médias utilisateurs | Factures, avatars, documents | **Hors périmètre MVP** | Exiger un stockage objet externe si introduits |
| Fichiers temporaires | Exports intermédiaires | Mémoire ou temporaire maîtrisé | Non durables |
| Base de données | `Record`, utilisateurs, sessions persistées | PostgreSQL Neon en ligne | Durable selon plan et sauvegardes |

Vercel détecte `STATIC_ROOT` et exécute **automatiquement `collectstatic`** sur un déploiement Django standard. Il ne faut pas ajouter un second `collectstatic` au build sans besoin démontré. Il ne faut surtout pas y chaîner `migrate`.

---

## 10. PostgreSQL Neon : configuration et isolation

### 10.1 Choix initial

- **Local** : SQLite en développement léger, ou PostgreSQL local si des fonctionnalités spécifiques sont testées.
- **CI** : PostgreSQL jetable, par exemple service PostgreSQL sur GitHub Actions.
- **Preview** : branche/base Neon indépendante, **créée depuis un jeu synthétique** et non un miroir contenant des données réelles.
- **Production** : branche/base Neon dédiée, credentials distincts.

### 10.2 URL poolée et directe

| Usage | Variable | Recommandation |
|---|---|---|
| Django HTTP sur Vercel | `DATABASE_URL` | Connexion poolée Neon quand compatible, comportement testé |
| Migrations administratives | `DATABASE_URL_UNPOOLED` | Connexion directe Neon, dans un job explicite et autorisé |
| Tests CI | `DATABASE_URL` propre au job | PostgreSQL isolé, jamais URL prod |
| Preview | `DATABASE_URL` de la Preview | Ne peut pas atteindre Production |

Le pooler Neon est basé sur PgBouncer en mode transactionnel. Les mécanismes dépendant d'un **état de session Postgres** doivent être examinés ; ne pas supposer que toutes les opérations d'administration supportent la connexion poolée.

### 10.3 Trois garde-fous distincts

1. **Séparation des secrets** : jamais de variable de connexion Production dans les configurations CI ou Preview.
2. **Séparation des ressources** : accès à la DB Preview indépendant, branche Neon explicite ou base dédiée, cycle de vie documenté.
3. **Test indépendant** : injecter des marqueurs distincts et vérifier qu'une écriture depuis la Preview ne modifie pas Production. Une différence d'`APP_ENV` ou de nom de variable ne constitue pas une preuve.

### 10.4 Données réelles et branching Neon

Une branche Neon créée à partir d'une branche source peut hériter du **schéma et des données de la source**. Une branche « isolée en écriture » n'est donc pas nécessairement « isolée du point de vue confidentialité ».

Pour un futur produit de comptabilité ou de gestion client, ne pas dériver une Preview de Production sans anonymisation, contrôle des habilitations et décision explicite. La politique par défaut de ce starter est **données synthétiques seulement**.

### 10.5 Migrations

- Versionner les fichiers `apps/*/migrations/`.
- Exécuter `makemigrations --check --dry-run` en CI pour détecter les changements non migrés.
- Tester `migrate --noinput` sur la base isolée de CI.
- Appliquer les migrations Preview sur **leur base propre** avant de considérer la Preview fonctionnelle.
- Déployer les migrations Production via une étape de release autorisée, **indépendante** des builds Vercel.
- Ne pas lancer `migrate` dans `config/wsgi.py`, `settings.py`, le `build`, `collectstatic`, ou le démarrage HTTP.
- Prévoir `expand -> migrate -> contract` pour les changements incompatibles et distinguer rollback code/restauration DB.

Le mécanisme exact du job de migration Production est défini dans `05_STRATEGIE_DONNEES_ET_MIGRATIONS.md` et `04_PLAN_IMPLEMENTATION_ET_CI_CD.md`, avant toute mise en service.

---

## 11. Intégration Vercel : contrat de déploiement

### 11.1 Prérequis structurants

- `manage.py` à la racine du projet Vercel.
- `pyproject.toml` et `uv.lock` versionnés.
- Version Python explicite.
- `DJANGO_SETTINGS_MODULE=config.settings` dans `manage.py` et `wsgi.py`.
- `WSGI_APPLICATION=config.wsgi.application` dans Django.
- `STATIC_ROOT` configuré.
- Variables d'environnement du **bon scope** Vercel : Preview et Production distincts.
- Base PostgreSQL Neon connectée en ligne et credentials adéquats.

### 11.2 Détection automatique

Le framework Django est pris en charge nativement par Vercel depuis 2026. Pour ce layout standard, **aucun `vercel.json` n'est requis** et aucun fichier `/api/index.py` n'est nécessaire. Un `vercel.json` pourra être ajouté lorsqu'un besoin technique concret le justifie : réglage de durée, exclusions de fichiers, comportement particulier confirmé par les docs, etc.

### 11.3 Variables par scope Vercel

| Scope Vercel | `APP_ENV` | `DATABASE_URL` | `DJANGO_SECRET_KEY` | `DJANGO_ALLOWED_HOSTS` |
|---|---|---|---|---|
| Preview | `preview` | URL DB isolée et synthétique | Secret Preview | Domaine(s) Preview réels |
| Production | `production` | URL Neon Production | Secret Production distinct | Domaine(s) Production réels |

**Attention aux URLs Preview dynamiques :** Vercel produit des domaines par déploiement. Il faut définir une politique `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` qui fonctionne pour les domaines effectivement attribués **sans ouvrir un wildcard non validé**. Une option consiste à construire des valeurs exactes depuis `VERCEL_URL` après contrôle que la variable provient bien du contexte de déploiement attendu, et à intégrer les domaines alias autorisés. Cette politique doit être testée, notamment pour les formulaires POST et les cookies.

### 11.4 Protection des previews

- Contrôler leur visibilité et la disponibilité d'une protection d'accès Vercel selon le plan.
- Ne jamais injecter de données personnelles réelles par commodité.
- Ne pas rendre des opérations d'administration accessibles anonymement.
- Empêcher une Preview de démarrer avec une URL Production.
- Appliquer les migrations uniquement sur la DB de la Preview.

### 11.5 Ne pas confondre déploiement et mise à jour de schéma

La connexion GitHub -> Vercel met automatiquement à jour **le code de l'application**. Elle ne constitue pas une procédure complète de modification de schéma PostgreSQL. Les migrations sont une étape de livraison séparée, conçue et testée en R3.

---

## 12. GitHub Actions : structure et configuration CI

### 12.1 Workflow minimal

Le fichier `.github/workflows/ci.yml` devra notamment :

1. Se déclencher sur les pull requests et sur les pushes à `main`.
2. Obtenir le dépôt avec les permissions minimales.
3. Installer la version Python convenue et `uv`.
4. Installer les dépendances de manière verrouillée.
5. Exécuter Ruff.
6. Exécuter `manage.py check`.
7. Vérifier l'absence de migrations oubliées.
8. Tester les modèles, vues et permissions sur **PostgreSQL isolé**.
9. Conserver un résultat lisible dans le statut de la PR.
10. Ne jamais utiliser les secrets de Neon Production.

### 12.2 Contrat d'environnement CI

```dotenv
# Exemple conceptuel de valeurs non sensibles du runner CI.
APP_ENV=ci
DJANGO_SECRET_KEY=CI_ONLY_RANDOM_TEST_VALUE_NOT_FOR_PUBLIC_USE
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,testserver
DATABASE_URL=postgresql://ci_user:ci_password@localhost:5432/ci_database
```

Les identifiants ci-dessus sont des exemples destinés à un Postgres **jetable appartenant au job**, et non à un service externe. Les secrets réels restent gérés dans les mécanismes appropriés.

### 12.3 Commandes de qualité

```bash
uv sync --locked
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync python manage.py check
uv run --no-sync python manage.py makemigrations --check --dry-run
uv run --no-sync python manage.py migrate --noinput
uv run --no-sync pytest
```

Ces commandes supposent que les variables CI et le service PostgreSQL isolé ont été configurés. Elles ne doivent pas être exécutées contre la base de production.

### 12.4 Gouvernance des PR

- Une PR doit référencer les user stories et les changements de migration éventuels.
- La branche `main` doit être protégée par les contrôles disponibles selon le compte et le dépôt.
- Si la protection native souhaitée n'est pas disponible, documenter la limitation et une mitigation avant GO.
- Limiter les permissions de `GITHUB_TOKEN` et la diffusion de secrets aux workflows de confiance.
- Séparer la CI des événements capables de déclencher des opérations Production sensibles.

### 12.5 Schéma de chaîne de livraison

```mermaid
flowchart LR
    C[Commit] --> PR[Pull request]
    PR --> CI[Lint + Tests + Migrations CI]
    CI -->|Succès| PV[Preview Vercel]
    PV --> IS[Validation isolation Neon]
    IS --> M[Fusion dans main]
    M --> RM[Étape release migration contrôlée si nécessaire]
    RM --> PROD[Déploiement Vercel / promotion compatible]
    PROD --> SM[Smoke test + vérification DB]
```

**Attention :** le diagramme représente un **ordre logique de sécurité**, pas l'ordre garanti par défaut des événements fournisseurs. L'intégration Git Vercel peut lancer les builds dès la PR et dès la fusion. Les contrôles bloquants, les validations de Preview et l'ordonnancement migrations/code doivent être configurés explicitement dans le plan CI/CD R2/R3.

---

## 13. Cloudflare : points d'extension, pas de dépendance initiale

### 13.1 DNS

- Dès qu'un domaine personnalisé est nécessaire, utiliser Cloudflare comme DNS autoritatif si ce service est retenu.
- Faire pointer les enregistrements vers Vercel selon les instructions du projet Vercel.
- **Privilégier DNS-only** au départ : le trafic HTTP arrive directement chez Vercel, Cloudflare ne fournit alors pas de WAF proxy pour cette requête.
- N'activer le proxy Cloudflare qu'après étude des en-têtes de confiance, du cache, des certificats et des doubles couches de sécurité.

### 13.2 Turnstile

Introduire Turnstile uniquement lorsqu'un formulaire public bénéficie d'une protection supplémentaire contre l'automatisation. Toujours vérifier le token côté serveur. Turnstile **ne remplace pas** la validation Django, les permissions ou une protection contre les abus applicatifs.

### 13.3 Stockage objet

Lorsque des fichiers utilisateurs apparaîtront, comparer au moins R2, Neon Object Storage et toute offre déjà disponible. Choisir **un** service pour le besoin, adapter les permissions et utiliser un transfert direct lorsque la taille des fichiers l'impose.

### 13.4 Variables optionnelles

Les variables Cloudflare listées en §7.3 ne doivent **pas** être obligatoires tant que la fonctionnalité qui les utilise n'existe pas. Le starter doit fonctionner sans compte Cloudflare.

---

## 14. Observabilité, journaux et erreurs

### 14.1 Journaux MVP

- Préférer les logs structurés ou semi-structurés sur `stdout`/`stderr`, exploitables par Vercel.
- Inclure niveau, horodatage, module et identifiant de release lorsque disponible.
- Ne jamais logger les `Authorization`, cookies, tokens, `DATABASE_URL`, `SECRET_KEY` ou le corps de formulaires sensibles.
- Utiliser des erreurs publiques sobres et les détails techniques dans des logs restreints.
- Prévoir un identifiant de version traçable vers le commit Git, sans dépendre du format d'un fournisseur particulier.

### 14.2 Page d'état

Une page d'état publique peut retourner un statut simple sans informations internes. Un contrôle de santé **qui interroge la base** ne doit être ajouté qu'avec un besoin réel et sans exposer la configuration ni effectuer d'écriture. Ne pas publier une page d'état affichant les noms de tables, les branches Neon ou les secrets.

### 14.3 Coûts et quotas

En R0/R2/R3, documenter les plans effectivement retenus, les quotas de build/fonctions, stockage et connexions, puis la méthode de lecture de l'usage. Les conditions de Vercel Hobby doivent être comparées à la **nature réelle** du projet avant tout usage commercial.

---

## 15. Ordre de création des fichiers

### Itération A - Bootstrap sans fournisseur externe

| Ordre | Fichiers | Story | Preuve |
|---|---|---|---|
| A1 | `pyproject.toml`, `uv.lock`, `.python-version` | US-002/005 | `uv sync --locked` réussit |
| A2 | `manage.py`, `config/settings.py`, `config/urls.py`, `wsgi.py` | US-005/006 | `manage.py check` passe |
| A3 | `.env.example`, `.gitignore`, `README.md` | US-006/017 | Reproduction locale sans secrets Git |
| A4 | `apps/core`, `templates/base.html`, `static/css/app.css` | US-007 | Accueil local visible |
| A5 | `apps/records/models.py`, migrations, admin | US-008/010 | Modèle et Admin fonctionnels |
| A6 | `forms.py`, vues, templates et URL `records` | US-009/033 | CRUD protégé fonctionnel |
| A7 | `apps/**/tests` | US-011/032 | Tests positifs et négatifs |

### Itération B - Qualité et livraison

| Ordre | Fichiers / configuration | Story | Preuve |
|---|---|---|---|
| B1 | `.github/workflows/ci.yml` | US-013 à US-015 | Lint, tests PostgreSQL et migrations |
| B2 | Règles de branche GitHub | US-016 | PR non conforme bloquée ou risque arbitré |
| B3 | Projet Vercel et scope d'environnement | US-018/019 | URL HTTPS, CSS, Admin |
| B4 | Previews isolées | US-021/026 | Test de sentinelles |
| B5 | Étape de migration contrôlée | US-027 | Procédure et dry-run sur DB isolée |
| B6 | Smoke test et release | US-020/028 | Commit déployé et donnée persistante |

### Itération C - Exploitation

Documenter logs, rotation des secrets, restauration, rollback et coûts. Tester les procédures sur des environnements non productifs avant GO MVP.

---

## 16. Commandes d'initialisation proposées

Le scénario ci-dessous est indicatif et **ne remplace pas la revue des versions, du dépôt et de la DB**.

```bash
# 1. Créer un répertoire de projet et l'initialiser.
mkdir django-cloud-starter
cd django-cloud-starter
uv init --no-package --python 3.12

# 2. Installer les dépendances et le verrouillage.
uv add "Django>=5.2,<5.3" "psycopg[binary]>=3.2,<4" \
  "dj-database-url>=2.2,<4" "python-dotenv>=1,<2"
uv add --dev pytest pytest-django ruff
uv lock

# 3. Générer l'ossature Django dans la racine du dépôt.
uv run django-admin startproject config .

# 4. Créer les packages des modules.
mkdir -p apps/core apps/records
# Créer apps/__init__.py avant l'enregistrement des modules.
touch apps/__init__.py
uv run python manage.py startapp core apps/core
uv run python manage.py startapp records apps/records

# 5. Réviser les AppConfig pour les modules sous apps/ :
# name = "apps.core" et name = "apps.records".
# Mettre à jour config/settings.py, config/urls.py,
# puis créer .env à partir du modèle documenté.

# 6. Contrôles locaux, après configuration des variables.
uv run python manage.py check
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py runserver
```

**Important pour cette séquence :** `startproject` génère d'abord un `settings.py` standard. Les contrôles de configuration stricte et la variable `DJANGO_SECRET_KEY` doivent être ajoutés ensuite, avant le premier `check` final et le lancement métier. Si `uv init` a déjà créé un `README.md` ou un fichier principal, adapter plutôt que supprimer aveuglément. Le `touch` affiché convient aux environnements Unix/macOS ; sous Windows, créer le fichier vide autrement.

### 16.1 Commandes usuelles après initialisation

```bash
uv sync --locked
uv run python manage.py check
uv run python manage.py runserver
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

### 16.2 Création de superutilisateur

```bash
# Local uniquement, après migrations et création d'un .env local valide.
uv run python manage.py createsuperuser
```

Ne pas créer le compte initial Production au moyen d'un script de build Vercel. Prévoir une opération administrateur maîtrisée, traçable et documentée ; ne jamais stocker le mot de passe dans le code, un workflow ou un ticket.

---

## 17. Tests spécifiques à la structure et à la configuration

| ID | Scénario | Résultat attendu | Story / critère |
|---|---|---|---|
| CFG-01 | Cloner et exécuter `uv sync --locked` | Installation reproductible | US-005, CA-01 |
| CFG-02 | Démarrer avec `.env` local valide | Accueil disponible | US-006/007, AT-01 |
| CFG-03 | Définir `APP_ENV=inconnu` | Arrêt explicite | US-006 |
| CFG-04 | Définir `APP_ENV=production` sans `DATABASE_URL` | Échec avant lancement | US-006/024 |
| CFG-05 | Définir `APP_ENV=preview` sans `DJANGO_SECRET_KEY` | Échec avant lancement | US-006/034 |
| CFG-06 | Demander `DJANGO_DEBUG=true` en Production | `DEBUG=False` effectif | US-032, CA-09 |
| CFG-07 | Utiliser `DJANGO_ALLOWED_HOSTS=*` en Production | Configuration rejetée | US-032 |
| CFG-08 | Fournir `.env` à un runner `ci` | Le fichier local n'est pas chargé par la configuration | US-034 |
| CFG-09 | Vérifier l'application `records` sous `apps/` | `AppConfig` et migrations détectés | US-008 |
| CFG-10 | Générer un changement de modèle sans migration | `makemigrations --check --dry-run` échoue | US-015/027 |
| CFG-11 | Lancer CI avec un Postgres isolé | Tests et migrations réussis | US-015/031 |
| CFG-12 | Afficher les statiques sur Vercel | CSS disponible en HTTPS | US-022, CA-02 |
| CFG-13 | Déployer une PR | URL Preview avec base distincte | US-021/026, CA-08 |
| CFG-14 | Tenter d'écrire depuis Preview vers Production | Aucune écriture Production | US-026, AT-05 |
| CFG-15 | Redéployer le code | Donnée Neon persistante | US-028, CA-04 |
| CFG-16 | Chercher les secrets dans le dépôt | Aucune valeur réelle trouvée | US-013/034, CA-10 |
| CFG-17 | Exécuter `check --deploy` avec settings Production | Avertissements examinés et traités | US-032 |
| CFG-18 | Construire l'app Vercel | Aucun `migrate` Production automatique | US-027, CA-11 |
| CFG-19 | Faire varier le domaine Preview | Hôte autorisé sans wildcard dangereux | US-021/032 |
| CFG-20 | Exécuter une requête de donnée non autorisée | Accès refusé côté serveur | US-033, CA-09 |

**Principe de preuve** : pour tout test d'infrastructure, conserver une trace expurgée du commit, de l'environnement et du résultat. Les tests nécessitant des comptes ou des ressources en ligne ne sont **pas validés** par les seuls exemples de ce document.

---

## 18. Registre des risques propres à la configuration

| Risque | Gravité | Exemple d'échec | Contrôle associé |
|---|---|---|---|
| `DATABASE_URL` Production injectée en Preview | Critique | PR modifie des données réelles | Isolation et test sentinelles CFG-13/14 |
| Copie de données privées par branching Neon | Critique | Preview lit les données Production | Branche synthétique, revue de source |
| Migration lors du build | Critique | Build Vercel altère le schéma prod | CFG-18, migration en release dédiée |
| Mode DEBUG actif en ligne | Élevée | Traceback/variables sensibles visibles | CFG-06, `check --deploy` |
| Wildcard hôtes non maîtrisé | Élevée | Host header non contrôlé | CFG-07/19 |
| Secret affiché dans un log | Élevée | Credentials compromis | Scan et redaction |
| SQLite en Production | Élevée | Données perdues au redéploiement | Obligation `DATABASE_URL` |
| Redirection HTTPS mal configurée | Moyenne/élevée | Boucles de redirection | Test Vercel/proxy avant activation |
| Mélange `STATIC_ROOT`/médias | Élevée | Uploads perdus | Statics CDN, médias externes |
| Sélection ASGI involontaire | Moyenne | Entrée de runtime inattendue | WSGI explicite, test build |
| Versions non identiques | Moyenne | Fonctionne local mais pas en ligne | Python explicite et `uv.lock` |
| Sur-ingénierie des modules | Moyenne | Starter difficile à maintenir | Django natif, services seulement utiles |
| Conditions de plan inadaptées | Élevée | Usage commercial sur plan incompatible | OA-01 et revue US-004 |

---

## 19. Conventions de conception applicables aux futurs modules

Le socle a vocation à être réutilisé, mais **pas** à imposer une architecture hexagonale complète pour un simple CRUD.

### 19.1 Strates minimales

- **Présentation** : URLConf, vues, formulaires, templates et Admin.
- **Application** : services lorsque plusieurs opérations doivent être coordonnées.
- **Domaine** : modèles, états et invariants.
- **Infrastructure** : ORM Django, stockage et adaptateurs lorsqu'ils existent.

### 19.2 Points d'extension explicites

| Besoin futur | Extension envisageable | Déclencheur |
|---|---|---|
| API externe ou mobile | Django REST Framework | Consommateur API réel |
| UI fortement interactive | HTMX, puis React si justifié | Besoin UX vérifié |
| Plusieurs contextes métiers | `apps/<domain>/` | Nouveau domaine et frontières claires |
| Moteur comptable | PyAccountingKit ou module métier natif | Contrat, validation et bénéfice démontrés |
| Intégration LLM | PyLLMKit ou fournisseur adapté | Cas métier, contrôle coûts et données |
| Exécution durable/longue | Queue / workflow / worker dédié | Durée, reprise, idempotence réelles |
| Médias | Stockage objet | Présence de fichiers utilisateur |
| Protection anti-bot | Turnstile | Formulaire public exposé |
| Identité tierce | Fournisseur d'identité externe | Exigence produit non satisfaite par Auth Django |

### 19.3 Tests et découpage

Les règles simples restent dans les modèles et formulaires. Les services apparaissent lorsqu'une transaction implique plusieurs objets, une coordination entre modules, des effets externes ou des invariants nécessitant un point d'entrée métier unique. Éviter les interfaces génériques et repositories supplémentaires qui ne fournissent aucune capacité de substitution utile.

---

## 20. Décisions finales et arbitrages avant de coder

| ID | Question | Proposition | Action attendue |
|---|---|---|---|
| OA-01 | Utilisation personnelle, POC ou commerciale ? | POC personnel initial | Confirmer avant Vercel |
| OA-02 | Quel compte GitHub ? | Compte ou organisation choisi par le propriétaire | Confirmer |
| OA-03 | Nom du dépôt ? | `django-cloud-starter` | Confirmer |
| OA-04 | `Record` doit-il être privé par créateur ? | Oui pour prouver les permissions objet | Confirmer avant modèle |
| OA-05 | Python/Django/uv ? | 3.12 / 5.2 LTS / uv | Valider versions et compatibilités |
| OA-06 | Région Vercel/Neon ? | Régions proches et compatibles données | Confirmer |
| OA-07 | Preview Neon ? | DB isolée, données synthétiques | Configurer et démontrer |
| OA-08 | Migrations Production ? | Release contrôlée, hors build | Définir en document 04/05 |
| OA-09 | Domaine Cloudflare ? | Après URL Vercel | Différer |
| OA-10 | Plan et budget ? | Avant activation production | Confirmer |
| OA-11 | Politique de restauration ? | Exercice sur base non prod | Définir en document 05 |
| OA-12 | API, workers, médias ? | Hors MVP | Réexaminer sur besoin |

Ne pas bloquer la mise au point locale sur OA-06 ou OA-09 ; en revanche, ne pas raccorder une base réelle ni publier un environnement exposé en laissant OA-01, OA-07 ou OA-08 sans politique.

---

## 21. Traçabilité vers les epics et user stories

| Sections | Stories principales | ADR | Preuves |
|---|---|---|---|
| §3-5 Arborescence, modèles, responsabilités | US-001, US-005, US-007 à US-011 | ADR-001, ADR-002, ADR-008, ADR-015 | CA-01, CA-03, CA-09 |
| §6 Dépendances et runtime | US-002, US-013, US-017 | ADR-013 | CA-01, CA-05 |
| §7-8 Configuration et secrets | US-006, US-032/034 | ADR-006, ADR-008, ADR-017 | CA-09/10 |
| §9 Interface et statiques | US-007/009/010/022 | ADR-002, ADR-010 | CA-02, CA-09 |
| §10 Neon et migration | US-024 à US-031 | ADR-005/006/007 | CA-03/04/08/11 |
| §11 Vercel | US-018 à US-023 | ADR-004/009/010 | CA-02/07 |
| §12 CI | US-012 à US-017 | ADR-003/013 | CA-05/06 |
| §13 Cloudflare optionnel | US-045 à US-048 | ADR-011/012 | Hors MVP sans besoin |
| §14 Observabilité | US-036 à US-040 | ADR-018 | CA-12/13 |
| §17 Tests et acceptation | US-041 à US-043 | ADR-018 | CA-01 à CA-13 |
| §19 Extensions | US-049 à US-052 | ADR-014/015 | P2 conditionnel |

---

## 22. Gate GO / NO-GO pour la transition R1 vers R2

### Gate R1 - Starter Django local

- [ ] Versions Python et Django fixées, `uv.lock` commité.
- [ ] `config/settings.py` propre, avec gestion explicite d'`APP_ENV`.
- [ ] `.env.example` sans secret réel, `.env` ignoré.
- [ ] Application `apps.core` et page publique disponibles.
- [ ] Application `apps.records` avec modèle, Admin, formulaires, vues, templates et routes.
- [ ] CRUD vérifié et permissions serveur testées.
- [ ] Migrations générées et reproductibles localement.
- [ ] `uv run pytest`, Ruff et `manage.py check` réussissent.
- [ ] README reproductible depuis un clone vierge.
- [ ] Aucun compte ou accès Neon/Vercel Production nécessaire à R1.

### Gate R2 - Préparation du déploiement

- [ ] Dépôt et politique de branches décidés.
- [ ] Workflow CI sur PostgreSQL jetable conçu et testé.
- [ ] Version Python compatible avec Vercel vérifiée.
- [ ] Variables Vercel Preview/Production séparées.
- [ ] Plan compatible avec la nature d'usage confirmé.
- [ ] Stratégie de Preview sans données réelles approuvée.
- [ ] Mécanisme de migration Production **séparé** identifié avant toute modification de schéma en ligne.

### NO-GO immédiat

Déclarer `NO-GO` si un secret est présent dans le dépôt, si une Preview peut utiliser Production, si les builds peuvent migrer Production, si Django démarre avec `DEBUG=True` en public, si le stockage durable n'est pas configuré pour les données réelles, ou si le plan d'hébergement ne permet pas l'usage projeté.

---

## 23. Prochain document

**`04_PLAN_IMPLEMENTATION_ET_CI_CD.md`** transformera la structure proposée en séquence d'implémentation et de contrôles : initialisation du repo, commandes exactes, PR et protections GitHub, GitHub Actions, intégration Vercel, environnements Preview, stratégie de release, preuves d'acceptation et conditions de rollback.

Ensuite, **`05_STRATEGIE_DONNEES_ET_MIGRATIONS.md`** détaillera les ressources Neon, les cycles de branches, la confidentialité des données, le schéma, les opérations de migration, la restauration et les garde-fous de production.

---

## Annexe A - Références officielles vérifiées

Ces pages servent de base aux décisions techniques. Vérifier de nouveau les détails dépendants des versions et des plans lors de l'exécution.

- Django, deployment checklist : https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- Django, settings : https://docs.djangoproject.com/en/5.2/ref/settings/
- Django, writing and running tests : https://docs.djangoproject.com/en/5.2/topics/testing/
- Vercel, déployer Django : https://vercel.com/docs/frameworks/full-stack/django
- Vercel, runtime Python : https://vercel.com/docs/functions/runtimes/python
- Vercel, intégration GitHub : https://vercel.com/docs/git/vercel-for-github
- Vercel, restrictions des Functions : https://vercel.com/docs/functions/limitations
- Neon, documentation : https://neon.com/docs
- Neon, branchement et connexion : https://neon.com/docs/introduction/branching
- Neon, intégration Vercel : https://vercel.com/marketplace/neon
- uv, projets Python : https://docs.astral.sh/uv/guides/projects/
- Cloudflare, DNS : https://developers.cloudflare.com/dns/
- Cloudflare, Turnstile : https://developers.cloudflare.com/turnstile/
- Cloudflare, R2 : https://developers.cloudflare.com/r2/

### Notes de fraîcheur au 18 novembre 2026

1. Vercel prend en charge la détection native Django via `manage.py`, utilise les settings WSGI/ASGI et collecte automatiquement les statiques si `STATIC_ROOT` est défini.
2. La documentation Vercel du runtime Python décrit Python 3.12, 3.13 et 3.14 comme versions disponibles au moment de la consultation. La sélection 3.12 dans ce document vise la stabilité du starter.
3. Neon peut fournir des URLs poolées et directes ; une connexion poolée et une branche de base doivent être vérifiées dans le contexte réellement configuré.
4. Aucune offre gratuite n'est présumée autoriser l'exploitation commerciale. Le plan Vercel Hobby exige une vérification des conditions en vigueur avant un tel usage.

---

## Annexe B - Historique

| Version | Date | Changements |
|---|---|---|
| 1.0 | 18 novembre 2026 | Arborescence, périmètre `records`, conventions de modules, versions candidates, `pyproject.toml`, variables, `.env.example`, `.gitignore`, configuration Django, WSGI, Vercel, Neon, CI, contrôle de sécurité, ordre d'implémentation et matrice de traçabilité. |
