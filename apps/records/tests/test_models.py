import pytest
from django.core.exceptions import ValidationError

from apps.records.models import Record

from .factories import create_record, create_user


@pytest.mark.django_db
def test_record_str_returns_title():
    record = create_record(create_user(), title="Titre modele")

    assert str(record) == "Titre modele"


@pytest.mark.django_db
def test_record_defaults_to_draft():
    record = create_record(create_user())

    assert record.status == Record.Status.DRAFT
    assert record.description == ""


@pytest.mark.django_db
def test_record_rejects_unknown_status():
    record = create_record(create_user(), status="inconnu")

    with pytest.raises(ValidationError):
        record.full_clean()


@pytest.mark.django_db
def test_record_requires_title():
    record = create_record(create_user(), title="")

    with pytest.raises(ValidationError):
        record.full_clean()
