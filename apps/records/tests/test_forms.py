import pytest

from apps.records.forms import RecordForm


@pytest.mark.django_db
def test_record_form_accepts_editable_fields():
    form = RecordForm(
        data={
            "title": "Formulaire valide",
            "description": "Description",
            "status": "active",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_record_form_requires_title():
    form = RecordForm(data={"title": "", "description": "", "status": "draft"})

    assert not form.is_valid()
    assert "title" in form.errors


@pytest.mark.django_db
def test_record_form_does_not_expose_owner_or_timestamps():
    assert set(RecordForm().fields) == {"title", "description", "status"}
