from django.contrib.auth import get_user_model

from apps.records.models import Record


def create_user(username="tester", password="test-pass-123", **overrides):
    defaults = {"username": username}
    defaults.update(overrides)
    return get_user_model().objects.create_user(password=password, **defaults)


def create_record(owner, **overrides):
    defaults = {"title": "Record de test", "status": Record.Status.DRAFT}
    defaults.update(overrides)
    return Record.objects.create(created_by=owner, **defaults)
