---
id: US-009
epic: EP-01
phase: R1
gate: R1.2
priority: P0
size: M
status: todo
owner: null
created: 2026-11-18
updated: 2026-11-18
depends_on: [US-008, US-010]
blocks: [US-011]
commits: []
evidence: []
backlog: ../specs/02_BACKLOG_ET_USER_STORIES.md
plan: ../plans/02_R1_SOCLE_LOCAL.md
---

# US-009 - Implementer un CRUD web complet

## Contexte

Permettre a un utilisateur autorise de creer, consulter, modifier et supprimer ses enregistrements de demonstration depuis des vues Django.

## Criteres d'acceptation

- [ ] AC-01 : chaque operation possede une route et un test.
- [ ] AC-02 : les formulaires valident les champs sans divulguer de donnees techniques.
- [ ] AC-03 : les ecritures exigent une connexion et le droit proprietaire.
- [ ] AC-04 : une demande invalide et un refus d'acces sont testes.

## Fichiers a creer ou modifier

| Fichier | Action | Role |
|---|---|---|
| [`apps/records/forms.py`](../../apps/records/forms.py) | creer | Formulaire `RecordForm`. |
| [`apps/records/views.py`](../../apps/records/views.py) | creer | Vues liste, detail, creation, edition, suppression. |
| [`apps/records/urls.py`](../../apps/records/urls.py) | creer | Routes du module. |
| [`templates/records/record_list.html`](../../templates/records/record_list.html) | creer | Affiche les enregistrements. |
| [`templates/records/record_form.html`](../../templates/records/record_form.html) | creer | Formulaire de creation et d'edition. |
| [`templates/records/record_detail.html`](../../templates/records/record_detail.html) | creer | Detail d'un enregistrement. |
| [`templates/records/record_confirm_delete.html`](../../templates/records/record_confirm_delete.html) | creer | Confirmation de suppression. |
| [`config/urls.py`](../../config/urls.py) | modifier | Monte `apps.records.urls` sous `records/`. |

## Exemples de code

`apps/records/forms.py` :

```python
from django import forms
from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["title", "description", "status"]
```

`apps/records/views.py`, exemple de filtrage proprietaire :

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Record


class RecordListView(LoginRequiredMixin, ListView):
    model = Record
    template_name = "records/record_list.html"
    context_object_name = "records"

    def get_queryset(self):
        return Record.objects.filter(created_by=self.request.user)
```

`config/urls.py`, ajout de l'include :

```python
path("records/", include("apps.records.urls")),
```

## Plan d'action

1. Definir les routes liste, detail, creation, modification et suppression.
2. Ecrire les formulaires ModelForm.
3. Filtrer les QuerySet par proprietaire.
4. Ajouter les templates et les messages d'erreur.
5. Couvrir les cas positifs et negatifs.

## Preuves attendues

- Suite de tests CRUD.
- Scenario manuel de refus d'acces a un objet d'autrui.

## Journal

| Date | Evenement | Reference |
|---|---|---|
| 2026-11-18 | Fiche creee | ADR-019 |

## Notes

Le modele d'autorisation doit rester base sur Django Auth et la propriete de l'objet.
