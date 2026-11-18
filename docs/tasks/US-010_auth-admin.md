---
id: US-010
epic: EP-01
phase: R1
gate: R1.2
priority: P0
size: M
status: done
owner: opencode/big-pickle (agent)
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-008]
blocks: [US-009, US-011]
commits: ["3d1bf9b"]
evidence: ["2026-11-18: check, makemigrations --check --dry-run, pytest 25 passed, ruff check", "apps/records/migrations/0001_initial.py"]
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/02_R1_SOCLE_LOCAL.md
---

# US-010 - Configurer l'authentification et Django Admin

## Contexte

Utiliser Django Auth et l'admin natif pour gerer les comptes et les enregistrements autorises, sans interface d'identite supplementaire.

## Criteres d'acceptation

- [x] AC-01 : connexion et deconnexion fonctionnent.
- [x] AC-02 : l'admin exige `is_staff` et les permissions appropriees.
- [x] AC-03 : un compte non autorise recoit un refus explicite.
- [x] AC-04 : la creation du superutilisateur est documentee sans mot de passe partage.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/admin.py`](../../apps/records/admin.py) | creer | Enregistre `Record` dans l'admin. |
| [`templates/registration/login.html`](../../templates/registration/login.html) | creer | Page de connexion Django Auth. |
| [`apps/records/tests/test_permissions.py`](../../apps/records/tests/test_permissions.py) | creer | Verifie les refus d'acces. |
| [`config/urls.py`](../../config/urls.py) | modifier | Monte `django.contrib.auth.urls` sous `accounts/`. |
| [`config/settings.py`](../../config/settings.py) | modifier | Definit `LOGIN_URL`, `LOGIN_REDIRECT_URL` et `LOGOUT_REDIRECT_URL`. |
| [`README.md`](../../README.md) | modifier | Documente `createsuperuser` sans secret partage. |

## Exemples de code

`apps/records/admin.py` :

```python
from django.contrib import admin
from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_by", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
```

`config/urls.py`, ajout des URLs d'authentification :

```python
urlpatterns = [path("accounts/", include("django.contrib.auth.urls"))]
```

`config/settings.py`, ajout en fin de fichier :

```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "record_list"
LOGOUT_REDIRECT_URL = "home"
```

## Plan d'action

1. Activer les URLs d'authentification Django.
2. Enregistrer `Record` dans l'admin avec les droits adaptes.
3. Ajouter les tests d'autorisation.
4. Documenter la commande `createsuperuser`.

## Preuves attendues

- Tests d'autorisation.
- Demonstration d'acces admin refusee pour un compte non autorise.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche creee | ADR-019 |
| 2026-11-18 | R1.2 implemente | `3d1bf9b` |

## Notes

Aucun mot de passe ni secret ne doit etre ecrit dans la documentation.
