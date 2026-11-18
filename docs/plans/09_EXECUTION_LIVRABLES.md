# Plan 04 - Première tranche et livrables

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 19. Plan d'exécution immédiat : première tranche

**Tranche à réaliser en priorité, avant toute infrastructure externe :**

1. Valider les OA bloquants R0 et le cas `Record`.
2. Initialiser `django-cloud-starter` avec Python 3.12, Django 5.2 LTS, `uv` et `uv.lock` si les versions sont confirmées.
3. Mettre en place `config/settings.py` et `.env.example` conformes à `03`.
4. Créer `apps.core` et `apps.records`, la page d'accueil, la première migration et l'Admin.
5. Ajouter login/logout, permissions, tests des modèles, des formulaires et des routes.
6. Exécuter Ruff, `makemigrations --check`, `manage.py check` et tests locaux.
7. Documenter la commande de démarrage depuis un clone neuf.
8. Enregistrer les preuves R1.1 et R1.2, puis seulement **ouvrir l'intégration GitHub/Vercel**.

### 19.1 Check-list de première tranche

- [ ] `pyproject.toml` vérifié, `uv.lock` créé, Python minor fixé.
- [ ] `manage.py` à la racine, config WSGI valide.
- [ ] `APP_ENV=local`, `.env` ignoré et clé locale générée.
- [ ] `Record` et migration initiale disponibles.
- [ ] Formulaires et CRUD testés.
- [ ] Auth/Admin et contrôle d'accès testés.
- [ ] `uv run ruff check .` réussi.
- [ ] `uv run python manage.py test` réussi.
- [ ] `uv run python manage.py makemigrations --check --dry-run` réussi.
- [ ] README reproductible.

**Condition d'arrêt :** ne pas créer de services externes juste pour résoudre un défaut de configuration ou de conception qui peut être testé localement.

---

## 20. Livrables attendus par phase

| Phase | Livrables techniques | Livrables probants |
|---|---|---|
| R0 | Arbitrages OA ; choix versions, dépôt, région, plan | Registre de décision approuvé |
| R1 | Django, templates, Auth/Admin, modèles, migrations, tests | Tests locaux et bootstrap |
| R2 | `.github/workflows/ci.yml`, dépôt, intégration Vercel | PR CI verte/rouge, URL, SHA |
| R3 | Neon isolé, release migrations, smoke tests, logs | Test sentinelles, rapport de persistance, exercice rollback |
| R4 | Configuration DNS/Turnstile/objet seulement si demandée | Tests spécifiques et coût/risque |
| R5 | Starter durci, guide de réutilisation, mesures | Deuxième bootstrap, décisions de maintenance |

---
