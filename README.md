# django-cloud-starter

Starter Django 5.2 reproductible, basé sur `uv` et Python 3.12.

## Prérequis

- [uv](https://docs.astral.sh/uv/) installé
- Python 3.12 (installé automatiquement par `uv python install 3.12` si besoin)

## Bootstrap

```bash
uv python install 3.12
uv sync --locked
cp .env.example .env
```

Générer une clé secrète locale puis remplacer la valeur dans `.env` :

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
uv run python manage.py migrate --noinput
uv run python manage.py runserver
```

L'application répond sur http://127.0.0.1:8000/ et l'admin sur http://127.0.0.1:8000/admin/ (créer un superuser avec `uv run python manage.py createsuperuser`).

## Vérifications

```bash
uv run python manage.py check
uv run pytest -q
uv run ruff check .
uv lock --check
```

## Configuration

La configuration est lue depuis l'environnement, avec `.env` chargé automatiquement depuis la racine du projet :

| Variable | Défaut local | Rôle |
|---|---|---|
| `APP_ENV` | `local` | Environnement (`local`, `staging`, `production`) |
| `DJANGO_SECRET_KEY` | clé insecure locale | Secret Django, obligatoire et réel hors `local` |
| `DJANGO_DEBUG` | `true` si `APP_ENV=local` | Mode debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts autorisés, séparés par des virgules |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | vide | Origines CSRF, séparées par des virgules |
| `DJANGO_LOG_LEVEL` | `INFO` | Niveau de log racine |
| `DATABASE_URL` | SQLite local | URL PostgreSQL ou autre, via `dj-database-url` |

`.env` est ignoré par Git et ne doit jamais être commité. `.env.example` ne contient que des valeurs d'exemple.

## Structure

```text
config/       projet Django (settings, urls, asgi, wsgi)
tests/        tests pytest / pytest-django
pyproject.toml  dépendances et configuration des outils
uv.lock       lockfile, source de vérité des versions
```
