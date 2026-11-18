# Plan 04 - R3.1 et R3.2 - Neon et migrations

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 10. R3.1 - Neon et séparation des environnements

### 10.1 Matrice des environnements

| Environnement | Exécution | Base | Données autorisées | Autorisation de migration |
|---|---|---|---|---|
| Local | Machine développeur | SQLite local ou PostgreSQL dédié | Synthétiques uniquement au MVP | Développeur, base locale |
| CI | GitHub Actions | PostgreSQL éphémère du job | Synthétiques uniquement | Automatique, DB éphémère |
| Preview | Vercel par PR | Branche Neon non productive ou DB isolée | **Synthétiques uniquement** | Procédure Preview isolée |
| Production | Vercel / Neon | Neon Production | Données réelles selon usage validé | Job de release autorisé uniquement |

### 10.2 Initialisation Neon

1. Créer le projet Neon **après validation du plan et de la région**.
2. Créer/identifier la branche Production et ses rôles.
3. Utiliser une connexion poolée pour le trafic web si validé avec Django/Neon ; utiliser les connexions directes appropriées pour les opérations administratives ou migrations, selon la documentation applicable.
4. Protéger les URL, avec TLS et accès minimaux.
5. Mettre en place une source Preview **synthétique** distincte de Production.
6. Intégrer la base aux variables Vercel Production et Preview sous les scopes appropriés.
7. Consigner un moyen de restauration et ses limites réelles.

### 10.3 Neon Branching : bénéfice et piège de confidentialité

L'intégration Neon/Vercel peut créer une branche PostgreSQL pour chaque Preview. **Une branche Neon peut copier les données de sa branche parente** : elle fournit une isolation des **écritures**, mais pas automatiquement une isolation des **données personnelles**.

Dans ce starter :

- **Recommandation de départ :** utiliser une branche parente synthétique ou une DB Preview dédiée entièrement sans données réelles.
- **Ne pas activer aveuglément** une intégration de branching qui dérive Preview d'une Production contenant des données sensibles.
- Vérifier le parent réel configuré, les permissions, les URLs injectées et la politique de nettoyage.
- Les capacités d'anonymisation Neon peuvent être évaluées ultérieurement, avec validation du résultat, mais ne remplacent pas une politique de confidentialité.
- Si le plan ou l'intégration ne permet pas d'assurer cela, choisir une base dédiée de test et **désactiver la Preview dynamique** plutôt que de prendre un risque.

### 10.4 Tests d'isolation obligatoires

**Sentinelles** : insérer une donnée distincte `PROD_ONLY` sur Production et `PREVIEW_ONLY` sur Preview, avec des identifiants et données fictifs.

1. Vérifier que Preview ne voit pas `PROD_ONLY` et que Production ne voit pas `PREVIEW_ONLY`.
2. Modifier un `Record` sur Preview.
3. Vérifier l'absence de changement en Production.
4. Vérifier que les secrets, rôles et URLs DB sont distincts **sans journaliser leur valeur**.
5. Vérifier la suppression/expiration des branches Preview selon la politique configurée.

**Gate Neon :** une simple comparaison de chaînes d'URL ne suffit pas. L'isolation doit être démontrée sur les ressources et les données effectivement accessibles.

---

## 11. R3.2 - Migrations PostgreSQL indépendantes du build

### 11.1 Contrat non négociable

**Interdit en Production :**

- `manage.py migrate` dans `settings.py`, `wsgi.py`, `asgi.py`, une vue, un middleware ou le chargement d'une fonction Vercel.
- `manage.py migrate` dans un `buildCommand` Vercel ou un script `collectstatic`.
- Exécution d'une migration de Production depuis une PR non approuvée.
- Migration destructive non testée ou sans stratégie de reprise.

**Exigé :**

- Migrations versionnées, relues et testées sur PostgreSQL CI/Preview isolé.
- Étape de migration Production distincte et autorisée, avec logs et identité du commit.
- Restauration et plan de reprise explicités ; rollback applicatif et restauration DB traités séparément.
- Changements de schéma compatibles avec les versions simultanément déployées lorsque nécessaire.

### 11.2 Workflow GitHub Actions de migration (modèle de départ)

Ce fichier n'est **pas** un déclencheur automatique sur push : il est exécuté manuellement par un opérateur habilité. Il présuppose un environnement GitHub nommé `production-db`, protégé par les approbations disponibles, avec un secret `DATABASE_URL_UNPOOLED` limité aux responsables de production. La mise à disposition d'un secret au runner suppose que l'environnement GitHub a été approuvé et que la configuration réseau Neon permet la connexion depuis le runner autorisé.

```yaml
name: Production DB migration

on:
  workflow_dispatch:
    inputs:
      confirmation:
        description: 'Saisir MIGRATE_PRODUCTION pour confirmer'
        required: true
        type: string

permissions:
  contents: read

concurrency:
  group: production-db-migrations
  cancel-in-progress: false

jobs:
  migrate:
    name: migrate-production-db
    if: github.ref == 'refs/heads/main' && inputs.confirmation == 'MIGRATE_PRODUCTION'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: production-db
    env:
      APP_ENV: production
      DJANGO_DEBUG: 'false'
      DJANGO_SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
      DATABASE_URL: ${{ secrets.DATABASE_URL_UNPOOLED }}
      DJANGO_ALLOWED_HOSTS: ${{ vars.DJANGO_ALLOWED_HOSTS }}
      DJANGO_CSRF_TRUSTED_ORIGINS: ${{ vars.DJANGO_CSRF_TRUSTED_ORIGINS }}

    steps:
      - name: Checkout validated main
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v10

      - name: Set up Python
        run: uv python install 3.12

      - name: Install locked dependencies
        run: uv sync --frozen

      - name: Check Django settings
        run: uv run --frozen python manage.py check

      - name: Display migration plan
        run: uv run --frozen python manage.py migrate --plan

      - name: Apply authorized migrations
        run: uv run --frozen python manage.py migrate --noinput

      - name: Verify migration history
        run: uv run --frozen python manage.py showmigrations --plan
```

**Limites et conditions de sécurité du modèle :**

- Le fichier YAML ne crée pas automatiquement la protection `production-db` : elle doit être configurée, vérifiée et testée selon les fonctionnalités du dépôt/plan GitHub.
- L'`if` limite la branche, mais **n'est pas un substitut** à la revue du commit, à un environnement protégé et aux permissions GitHub.
- Vérifier la configuration réelle des variables de l'environnement GitHub. Toute variable absente doit produire un échec avant modification.
- Les migrations peuvent nécessiter des opérations préparatoires et des verrous applicatifs que ce gabarit n'implémente pas ; documenter les migrations à risque dans `05_STRATEGIE_DONNEES_ET_MIGRATIONS.md`.
- Ce workflow doit utiliser la **révision effectivement destinée à la mise en production** et être coordonné avec les versions applicatives. Un lancement manuel depuis `main` alors que plusieurs releases se succèdent n'est pas intrinsèquement sûr.
- Ne pas exécuter le workflow sur une base Production tant que les modes d'autorisation, de restauration et de promotion n'ont pas été testés dans une base de validation.

### 11.3 Politique `expand -> migrate -> contract`

| Phase | Changement | Compatibilité | Vérification |
|---|---|---|---|
| Expand | Ajouter une colonne nullable ou table compatible | Ancienne et nouvelle versions | Migration non destructive sur base de recette |
| Migrate | Déployer code compatible et, si nécessaire, réécrire les données | Ancienne + nouvelle versions durant transition | E2E et contrôle de migration |
| Contract | Supprimer ancien champ ou contrainte après transition | Nouvelle version uniquement | Fenêtre de maintenance/validation adaptée |

Ne pas confondre les migrations Django du modèle et une transaction applicative : certaines opérations PostgreSQL et certains volumes peuvent nécessiter un plan dédié, un `RunPython` maîtrisé ou un job de traitement séparé.

### 11.4 Exigence de séquencement avec le déploiement automatique

**Premier lancement :** appliquer le schéma initial à une base Neon dédiée avant de rendre l'interface CRUD accessible sur Production. Enregistrer le SHA et le résultat de la migration.

**Évolution compatible :** réaliser la migration `expand` au bon moment, puis laisser le déploiement automatique publier le code compatible. Le test de compatibilité doit couvrir la version actuellement servie et la version future.

**Évolution incompatible :** ne pas se contenter d'un push sur `main`. Ajouter une politique de **promotion tenue en attente**, ou organiser une release manuelle/maintenance avec séquence explicitement validée. Le mécanisme effectif est à confirmer dans le runbook et doit empêcher l'exposition d'une combinaison code/schéma invalide.

---
