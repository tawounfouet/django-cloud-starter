import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
VALID_ENVS = {"local", "ci", "preview", "production"}

if (os.getenv("VERCEL") or os.getenv("CI")) and not os.getenv("APP_ENV"):
    raise ImproperlyConfigured("APP_ENV est requis en déploiement ou en CI")

APP_ENV = os.getenv("APP_ENV", "local")
if APP_ENV not in VALID_ENVS:
    raise ImproperlyConfigured(f"APP_ENV non autorisé : {APP_ENV}")

if APP_ENV == "local":
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
    return [item.strip() for item in os.getenv(name, "").split(",") if item.strip()]


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
    if APP_ENV != "local" and not DATABASE_URL.startswith(("postgres://", "postgresql://")):
        raise ImproperlyConfigured("DATABASE_URL PostgreSQL est requis hors local")
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

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

SESSION_COOKIE_SECURE = APP_ENV in {"preview", "production"}
CSRF_COOKIE_SECURE = APP_ENV in {"preview", "production"}
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = False

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}
