# Plan 04 - R2.1 - GitHub et CI

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 7. R2.1 - GitHub : dépôt, PR et règles de fusion

### 7.1 Publication du dépôt

1. Créer le dépôt approuvé, avec visibilité et propriétaire validés.
2. Vérifier le `.gitignore`, les licences éventuelles, les fichiers source et la documentation.
3. Publier le commit initial sur `main` avec une origine GitHub configurée.
4. Activer les fonctionnalités de revue et de contrôle disponibles selon le plan GitHub.
5. Exiger le passage par des branches `feat/*`, `fix/*`, `docs/*` pour le travail courant.
6. Documenter les exceptions de maintenance et les droits de contournement éventuels.

**Exemple de publication** (nécessite un dépôt GitHub existant et une URL autorisée) :

```bash
git status --short
git add .
git commit -m "chore: bootstrap Django cloud starter"
git remote add origin <URL_GITHUB_CONFIRME>
git push -u origin main
```

`<URL_GITHUB_CONFIRME>` représente un paramètre à substituer, **pas une URL utilisable telle quelle**.

### 7.2 Politique PR minimale

- Vérifications obligatoires : lint/format, tests Django, intégration PostgreSQL, migrations en attente.
- Revue de PR selon la taille de l'équipe et le plan GitHub.
- Aucun secret Production dans la CI PR, y compris pour une contribution issue d'un fork.
- **Ne pas utiliser `pull_request_target` pour exécuter du code non fiable avec des secrets privilégiés.**
- `main` ne reçoit pas normalement de pushes directs ; contrôler les rôles pouvant contourner les règles.
- Une release n'est pas validée par le seul fait qu'un build Vercel a réussi.

### 7.3 Preuves attendues

- PR valide : tous les checks deviennent verts.
- PR invalide : défaut volontaire de test ou de lint, check rouge.
- Règle de fusion : impossibilité de fusionner la PR invalide via la voie normale, ou écart explicite si le plan GitHub ne permet pas l'application technique de la règle.

---

## 8. R2.1 - Workflow CI de référence

### 8.1 Fichier `.github/workflows/ci.yml`

Cet exemple est destiné à être **copié puis adapté**. Il démarre un PostgreSQL temporaire *dans le runner GitHub*, sans service Neon ni identifiant réel. Les valeurs `ci_user/ci_password` ci-dessous ne servent qu'au conteneur jetable du job : elles ne doivent pas être réutilisées ailleurs.

```yaml
name: Django CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: django-ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality-and-tests:
    name: quality-and-tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
    env:
      APP_ENV: ci
      DJANGO_SECRET_KEY: ci-only-ephemeral-test-key-not-for-production
      DJANGO_DEBUG: "false"
      DJANGO_ALLOWED_HOSTS: localhost,127.0.0.1,testserver
      DATABASE_URL: postgresql://ci_user:ci_password@127.0.0.1:5432/ci_db
      CI: "true"

    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_DB: ci_db
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ci_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U ci_user -d ci_db"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v10
        with:
          enable-cache: true

      - name: Set up Python 3.12
        run: uv python install 3.12

      - name: Install locked dependencies
        run: uv sync --frozen --group dev

      - name: Lint
        run: uv run --frozen ruff check .

      - name: Format
        run: uv run --frozen ruff format --check .

      - name: Django system checks
        run: uv run --frozen python manage.py check

      - name: Ensure migrations are committed
        run: uv run --frozen python manage.py makemigrations --check --dry-run

      - name: Test PostgreSQL migrations
        run: uv run --frozen python manage.py migrate --noinput

      - name: Run application tests
        run: uv run --frozen python manage.py test

      - name: Validate static collection
        run: uv run --frozen python manage.py collectstatic --noinput
```

### 8.2 Commentaires de sécurité et d'exécution

1. Le déclencheur `pull_request` utilise le modèle standard, **sans** `pull_request_target`.
2. `permissions: contents: read` impose un jeton GitHub restreint.
3. Les tests utilisent uniquement le conteneur PostgreSQL du job.
4. Les variables `DJANGO_SECRET_KEY`, `DATABASE_URL` du workflow ne sont **pas** des clés ou des identifiants Neon ; elles sont locales au runner temporaire.
5. `uv.lock` doit être commité et correspondre au `pyproject.toml` ; vérifier la politique de groupe de dépendances lors de l'implémentation.
6. Les versions des GitHub Actions doivent idéalement être **verrouillées par SHA complet** lors du durcissement de la chaîne d'approvisionnement ; les tags majeurs ci-dessus privilégient la lisibilité de ce modèle.
7. La commande `collectstatic` en CI n'est qu'un contrôle. Vercel sait exécuter la collecte au build : **ne pas créer un script Vercel personnalisé qui la relance sans nécessité**.
8. La durée de `timeout-minutes` est une garde de CI, à mesurer puis ajuster ; ce n'est pas une estimation de travail.
9. Une suite `pytest` peut remplacer `manage.py test` si la configuration et les tests sont adaptés ; ne pas imposer deux runners pour le même corpus.
10. Le workflow ci-dessus ne fournit **aucun** secret de production à une PR ou un fork.

### 8.3 Variante de contrôle de sécurité

- Exécuter `manage.py check --deploy` avec une **configuration fictive de type production**, pour analyser les avertissements Django. Si la politique finale de proxy HTTPS et HSTS n'est pas encore arbitrée, ne pas ignorer aveuglément les avertissements.
- Ajouter une analyse de secrets et de dépendances selon les possibilités du dépôt ; choisir des outils versionnés et adapter les seuils d'alerte.
- Les contrôles bloquants sur `main` doivent être définis sur le **nom exact du job** (ici `quality-and-tests`) et vérifiés après chaque renommage.

### 8.4 Gate CI

- [ ] Un commit correct produit un run vert.
- [ ] Une erreur Ruff ou Django produit un run rouge.
- [ ] Une migration de modèle oubliée produit un run rouge.
- [ ] Une base CI neuve reçoit les migrations et les tests passent.
- [ ] Aucun credential Production n'est disponible dans le job.

---
