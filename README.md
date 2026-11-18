# django-cloud-starter

Starter Django 5.2 reproductible, basé sur `uv` et Python 3.12 (`>=3.12,<3.13`).

## Prérequis

- [uv](https://docs.astral.sh/uv/) installé
- Python 3.12 (installé automatiquement par `uv python install 3.12` si besoin)

## Bootstrap depuis un clone vierge

```bash
uv python install 3.12
uv sync --locked
cp .env.example .env
```

Générer une clé secrète locale puis remplacer le placeholder dans `.env` :

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
uv run python manage.py migrate --noinput
uv run python manage.py runserver
```

La page publique répond sur http://127.0.0.1:8000/ avec la feuille de style `static/css/app.css`.
L'admin répond sur http://127.0.0.1:8000/admin/ (créer un superuser avec `uv run python manage.py createsuperuser`).

Aucun service externe n'est nécessaire au démarrage local : SQLite est utilisé par défaut.

La vertical slice `records` est disponible sur http://127.0.0.1:8000/records/ après connexion. Chaque utilisateur ne voit que ses propres enregistrements. Les comptes sont gérés par Django Auth ; aucun mot de passe partagé n'est documenté.

## Vérifications

```bash
uv sync --frozen --group dev
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py collectstatic --noinput --dry-run
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv lock --check
```

## Intégration continue

Le workflow `.github/workflows/ci.yml` se déclenche sur les pull requests vers `main`, sur les pushes vers `main` et manuellement. Le job s'appelle `quality-and-tests` : c'est ce nom exact qui doit être exigé dans les règles de fusion GitHub.

La CI installe les dépendances depuis `uv.lock`, vérifie l'hygiène du dépôt, lance Ruff, contrôle le lockfile, exécute les checks Django, vérifie les migrations, applique les migrations sur un PostgreSQL 17 jetable, lance `pytest` et valide `collectstatic`. Aucun secret de production n'est exposé aux pull requests, y compris issues d'un fork : le workflow utilise uniquement des valeurs éphémères et `pull_request_target` n'est pas utilisé.

La protection de `main`, la revue requise et les vérifications obligatoires se configurent dans les paramètres du dépôt GitHub. Le dépôt doit être publié et le workflow poussé avant que ces règles puissent être appliquées.

## Dépannage

| Symptôme | Diagnostic |
|---|---|
| `APP_ENV est requis en déploiement ou en CI` | Définir `APP_ENV=local` dans `.env` ou `APP_ENV=ci` dans l'environnement CI. |
| `DJANGO_SECRET_KEY absent ou factice` | Remplacer le placeholder de `.env.example` par une clé générée localement. |
| `DATABASE_URL PostgreSQL est requis hors local` | Fournir une URL PostgreSQL hors `local` ; SQLite reste réservé au développement. |
| `You have unapplied migrations` | Exécuter `uv run python manage.py migrate` avant de lancer le serveur. |
| `ruff format --check .` échoue | Exécuter `uv run ruff format .` puis committer le résultat. |
| `uv lock --check` échoue | Exécuter `uv lock` après un changement de `pyproject.toml`. |

## Configuration

La configuration est lue depuis l'environnement. `.env` n'est chargé qu'en mode `local`, avec `override=False`.

| Variable | Local | Hors local | Rôle |
|---|---|---|---|
| `APP_ENV` | `local` par défaut | obligatoire sur CI/Vercel | `local`, `ci`, `preview`, `production` |
| `DJANGO_SECRET_KEY` | obligatoire, jamais de placeholder | obligatoire | Secret Django |
| `DJANGO_DEBUG` | `false` par défaut | toujours `false` | Mode debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` par défaut | obligatoire en `preview`/`production`, `*` interdit | Hosts autorisés, séparés par des virgules |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | vide | selon la plateforme | Origines CSRF, séparées par des virgules |
| `DJANGO_LOG_LEVEL` | `INFO` | `INFO` | Niveau de log racine |
| `DATABASE_URL` | SQLite local par défaut | PostgreSQL obligatoire | URL parsée par `dj-database-url`, TLS imposé en `preview`/`production` |

Le démarrage échoue explicitement si `APP_ENV` est inconnu, si la clé est absente ou factice, si `DATABASE_URL` manque hors local, ou si `ALLOWED_HOSTS` contient `*` hors local.

`.env`, `.venv`, `db.sqlite3` et `archives/` sont ignorés par Git. `.env.example` ne contient aucune valeur sensible.

## Structure

```text
.github/workflows/ workflow CI GitHub Actions
apps/core/        vue d'accueil, URLConf, tests
apps/records/     modèle Record, CRUD web, admin et tests
config/           réglages, URLConf racine, WSGI et ASGI
templates/        base.html, templates des apps core, records et registration
static/css/       feuille de style de la page publique
docs/             documents de cadrage et plan d'implémentation
pyproject.toml    dépendances, pytest et ruff
uv.lock           lockfile, source de vérité des versions
```
