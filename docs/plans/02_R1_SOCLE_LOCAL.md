# Plan 04 - R1.1 et R1.2 - Socle local

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 5. R1.1 - Initialisation reproductible de Django

### 5.1 Structure cible minimale

```text
django-cloud-starter/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release-migrate.yml          # R3 uniquement
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   └── records/
│       ├── __init__.py
│       ├── apps.py
│       ├── admin.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       ├── views.py
│       ├── migrations/
│       └── tests/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py                 # Présent éventuellement, sans ASGI_APPLICATION actif
├── templates/
│   ├── base.html
│   ├── core/
│   ├── records/
│   └── registration/
├── static/css/
├── docs/
├── .env.example
├── .gitignore
├── .python-version
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md
```

Les fichiers réellement présents dépendront de l'incrément. Se reporter au document `03` pour les responsabilités des modules et des réglages.

### 5.2 Bootstrap de référence

Le dépôt et les versions doivent avoir été décidés en R0. L'extrait suivant illustre **une initialisation dans un répertoire neuf**, sans écraser de fichiers existants.

```bash
mkdir django-cloud-starter
cd django-cloud-starter

git init -b main
uv python install 3.12
uv init --no-package --python 3.12
uv add "Django>=5.2,<5.3" "psycopg[binary]>=3.2,<4" \
  "dj-database-url>=2.2,<4" "python-dotenv>=1,<2"
uv add --dev pytest pytest-django ruff
uv lock
uv sync --locked
uv run django-admin startproject config .
```

Après le bootstrap, **adapter** `config/settings.py`, les apps, l'URLConf, le modèle `Record`, les templates et le `pyproject.toml` aux choix du document `03` : il n'est pas attendu que la commande `startproject` produise toute l'arborescence à elle seule.

Le fichier `pyproject.toml` cible conserve une version mineure de Python fixe (`>=3.12,<3.13`) et une plage Django LTS (`>=5.2,<5.3`) jusqu'à l'arbitrage de compatibilité ; `uv.lock` est toujours versionné.

### 5.3 Contrat de configuration

```dotenv
# .env.example - NE JAMAIS ajouter de vrais secrets
APP_ENV=local
DJANGO_SECRET_KEY=REPLACE_WITH_LOCAL_RANDOM_SECRET
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DJANGO_LOG_LEVEL=INFO
# DATABASE_URL=postgresql://local_user:local_password@localhost:5432/local_db
```

- `.env` est ignoré par Git ; `python-dotenv` le charge uniquement en mode `local` selon le document `03`.
- `APP_ENV` prend exactement `local`, `ci`, `preview` ou `production`.
- En `ci`, `preview` et `production`, une `DATABASE_URL` PostgreSQL explicite est requise, jamais une SQLite de repli.
- `DJANGO_SECRET_KEY` et `DJANGO_ALLOWED_HOSTS` sont propres aux environnements.
- Le processus refuse un `APP_ENV` distant implicite ou une clé de démonstration.
- Le modèle d'authentification reste **Django Auth**, pas Neon Auth dans le MVP.

### 5.4 Commandes de vérification R1.1

```bash
cp .env.example .env
# Générer une vraie clé locale unique et remplacer le placeholder dans .env.
# Ne pas commiter ce fichier.
uv sync --locked
uv run python manage.py check
uv run python manage.py migrate --noinput
uv run python manage.py runserver
```

### Gate R1.1

- [ ] Le serveur local répond avec une page publique.
- [ ] Le clone + installation ne nécessite aucun service externe pour afficher la page.
- [ ] Les fichiers `.env` et `db.sqlite3` sont ignorés.
- [ ] `manage.py check` ne remonte aucune erreur bloquante.
- [ ] `uv.lock` et `.python-version` sont versionnés.

**Preuves :** commande de lancement, page publique, sortie de `manage.py check`, statut Git.

---

## 6. R1.2 - Première vertical slice métier

### 6.1 Scénario

Le modèle `Record` (cf. `03`) possède `title`, `description`, `status`, `created_by`, `created_at`, `updated_at`. Les routes permettent la liste, le détail, la création, la modification et la suppression des enregistrements autorisés.

| Tâche | Livrable | Contrôle de sécurité | US |
|---|---|---|---|
| Modèle | `apps/records/models.py` et migrations | Contraintes et propriété des objets | US-008 |
| Administration | `admin.py` | Accès `is_staff` et permissions | US-010 |
| Interface | Formulaires, vues et templates | CSRF et validation côté serveur | US-007/009 |
| Auth | Connexion et déconnexion Django | Sessions, login obligatoire | US-010 |
| Autorisations | QuerySet filtrés et vérification de propriétaire | IDOR, modification d'un objet d'autrui refusée | US-009/033 |
| Tests | Modèles, formulaires, vues, permissions | Cas positifs et négatifs | US-011 |

### 6.2 Commandes de contrôle

```bash
uv run python manage.py makemigrations records
uv run python manage.py migrate --noinput
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py test
uv run ruff check .
uv run ruff format --check .
```

> L'app Django doit être déclarée `apps.records` dans `INSTALLED_APPS` avec le label `records`. Les utilisateurs de test et les données `Record` doivent être **générés**, sans importer de données réelles.

### Gate R1.2

- [ ] Les opérations CRUD fonctionnent localement.
- [ ] Un utilisateur anonyme ne peut pas écrire.
- [ ] Un utilisateur ne peut pas modifier un enregistrement non autorisé.
- [ ] Les migrations sont versionnées et aucune migration n'est oubliée.
- [ ] Les tests R1 réussissent.

**Preuves :** rapport tests + liste des migrations + démonstration d'un refus d'accès.

---
