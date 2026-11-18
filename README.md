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

## Vérifications

```bash
uv run python manage.py check
uv run python manage.py collectstatic --noinput --dry-run
uv run pytest -q
uv run ruff check .
uv lock --check
```

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
apps/core/        vue d'accueil, URLConf, tests
config/           réglages, URLConf racine, WSGI et ASGI
templates/        base.html et templates de l'app core
static/css/       feuille de style de la page publique
docs/             documents de cadrage et plan d'implémentation
pyproject.toml    dépendances, pytest et ruff
uv.lock           lockfile, source de vérité des versions
```
