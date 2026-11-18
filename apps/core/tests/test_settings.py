from django.conf import settings


def test_settings_are_loaded():
    assert settings.configured
    assert settings.ROOT_URLCONF == "config.urls"
    assert settings.DEFAULT_AUTO_FIELD == "django.db.models.BigAutoField"


def test_database_is_configured():
    database = settings.DATABASES["default"]
    assert database["ENGINE"]
    assert database["NAME"]


def test_secret_key_is_not_placeholder():
    assert settings.SECRET_KEY
    assert not settings.SECRET_KEY.startswith("REPLACE_WITH_")


def test_static_settings_are_configured():
    assert settings.STATIC_URL == "/static/"
    assert settings.STATIC_ROOT
    assert settings.STATICFILES_DIRS
