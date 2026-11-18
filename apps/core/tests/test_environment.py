import os
import subprocess
import sys

from django.conf import settings

BASE_ENV = {
    **os.environ,
    "DJANGO_SETTINGS_MODULE": "config.settings",
    "PYTHONPATH": str(settings.BASE_DIR),
}


def boot(**overrides):
    env = {**BASE_ENV, **{key: str(value) for key, value in overrides.items()}}
    return subprocess.run(
        [sys.executable, "-c", "import django; django.setup()"],
        cwd=settings.BASE_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_unknown_app_env_is_rejected():
    result = boot(APP_ENV="inconnu")

    assert result.returncode != 0
    assert "APP_ENV non autorisé" in result.stderr


def test_ci_without_app_env_is_rejected():
    result = boot(CI="1", APP_ENV="")

    assert result.returncode != 0
    assert "APP_ENV est requis" in result.stderr


def test_production_without_database_url_is_rejected():
    result = boot(
        APP_ENV="production",
        DJANGO_SECRET_KEY="test-secret-key",
        DJANGO_ALLOWED_HOSTS="example.com",
    )

    assert result.returncode != 0
    assert "DATABASE_URL PostgreSQL est requis" in result.stderr


def test_preview_without_secret_key_is_rejected():
    result = boot(
        APP_ENV="preview",
        DATABASE_URL="postgresql://user:password@localhost:5432/db",
        DJANGO_SECRET_KEY="",
    )

    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY absent ou factice" in result.stderr
