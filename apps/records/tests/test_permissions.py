import pytest
from django.urls import reverse

from .factories import create_record, create_user


@pytest.mark.django_db
def test_other_user_cannot_see_or_change_record(client):
    owner = create_user("owner")
    intruder = create_user("intruder")
    record = create_record(owner, title="Prive")
    client.force_login(intruder)

    detail = client.get(reverse("record_detail", kwargs={"pk": record.pk}))
    update = client.post(
        reverse("record_update", kwargs={"pk": record.pk}),
        {"title": "Modifie", "description": "", "status": "active"},
    )
    delete = client.post(reverse("record_delete", kwargs={"pk": record.pk}))

    assert detail.status_code == 404
    assert update.status_code == 404
    assert delete.status_code == 404
    record.refresh_from_db()
    assert record.title == "Prive"


@pytest.mark.django_db
def test_non_staff_user_is_redirected_from_admin(client):
    user = create_user("viewer")
    client.force_login(user)

    response = client.get(reverse("admin:index"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_staff_user_can_open_admin(client):
    user = create_user("admin", is_staff=True)
    client.force_login(user)

    response = client.get(reverse("admin:index"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_logout_round_trip(client):
    create_user("connected", password="test-pass-123")
    login_page = client.get(reverse("login"))
    logged_in = client.login(username="connected", password="test-pass-123")
    response = client.post(reverse("logout"))

    assert login_page.status_code == 200
    assert logged_in is True
    assert response.status_code == 302
    assert response.url == reverse("home")
