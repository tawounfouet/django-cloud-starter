import pytest
from django.urls import reverse

from apps.records.models import Record

from .factories import create_record, create_user


@pytest.mark.django_db
def test_anonymous_user_is_redirected_to_login(client):
    response = client.get(reverse("record_list"))

    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_list_only_shows_owner_records(client):
    owner = create_user("owner")
    other = create_user("other")
    create_record(owner, title="A moi")
    create_record(other, title="A autrui")
    client.force_login(owner)

    response = client.get(reverse("record_list"))

    assert response.status_code == 200
    assert "A moi" in response.content.decode()
    assert "A autrui" not in response.content.decode()


@pytest.mark.django_db
def test_create_assigns_owner_and_redirects(client):
    owner = create_user("owner")
    client.force_login(owner)

    response = client.post(
        reverse("record_create"),
        {"title": "Nouveau", "description": "", "status": "draft"},
    )

    record = Record.objects.get(title="Nouveau")
    assert response.status_code == 302
    assert record.created_by == owner
    assert response.url == reverse("record_detail", kwargs={"pk": record.pk})


@pytest.mark.django_db
def test_create_rejects_invalid_form(client):
    owner = create_user("owner")
    client.force_login(owner)

    response = client.post(reverse("record_create"), {"title": ""})

    assert response.status_code == 200
    assert not Record.objects.exists()


@pytest.mark.django_db
def test_detail_update_and_delete_owner_record(client):
    owner = create_user("owner")
    record = create_record(owner, title="Modifiable")
    client.force_login(owner)

    detail = client.get(reverse("record_detail", kwargs={"pk": record.pk}))
    update = client.post(
        reverse("record_update", kwargs={"pk": record.pk}),
        {"title": "Modifie", "description": "", "status": "active"},
    )

    assert detail.status_code == 200
    assert update.status_code == 302
    record.refresh_from_db()
    assert record.title == "Modifie"

    delete = client.post(reverse("record_delete", kwargs={"pk": record.pk}))

    assert delete.status_code == 302
    assert not Record.objects.filter(pk=record.pk).exists()
