from django.conf import settings


def test_settings_are_loaded():
    assert settings.configured
    assert settings.ROOT_URLCONF == "config.urls"
    assert settings.DEFAULT_AUTO_FIELD == "django.db.models.BigAutoField"


def test_database_is_configured():
    database = settings.DATABASES["default"]
    assert database["ENGINE"]
    assert database["NAME"]


def test_local_secret_key_is_not_placeholder():
    assert settings.SECRET_KEY
    assert settings.SECRET_KEY != "REPLACE_WITH_LOCAL_RANDOM_SECRET"
