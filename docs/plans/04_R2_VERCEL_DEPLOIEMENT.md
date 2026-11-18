# Plan 04 - R2.2 - Déploiement Vercel

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 9. R2.2 - Connexion et déploiement Django sur Vercel

### 9.1 Préconditions

- Dépôt GitHub et branche `main` prêts.
- `manage.py` à la racine du projet ; `config/settings.py` et `config/wsgi.py` cohérents.
- Version Python prise en charge et `uv.lock` verrouillé.
- `WSGI_APPLICATION = "config.wsgi.application"` dans les settings actives.
- `ASGI_APPLICATION` **non défini** tant que WSGI reste la cible, car Vercel peut privilégier ASGI si les deux sont configurés.
- `STATIC_ROOT` défini ; `STATIC_URL` correct.
- Plan Vercel adapté à l'usage réel.

### 9.2 Parcours de configuration Vercel

1. Importer le dépôt GitHub dans un projet Vercel approuvé.
2. Vérifier la racine du projet : elle doit contenir le `manage.py` et le `pyproject.toml` attendus.
3. Laisser Vercel détecter Django nativement. **Pas de `vercel.json`, `/api/`, Dockerfile ni configuration de réécriture par défaut.**
4. Définir la région retenue et la version Python via les fichiers versionnés.
5. Renseigner explicitement les variables Preview et Production, **sans réutiliser la DB Production en Preview**.
6. Vérifier le build, les logs et les URLs attribuées.
7. Vérifier la page HTML, l'Admin, l'authentification et les statiques.
8. Associer le déploiement au commit exact et consigner le résultat.

### 9.3 Contrat des variables Vercel

| Variable | Production | Preview | Commentaire |
|---|---|---|---|
| `APP_ENV` | `production` | `preview` | Doit être explicite |
| `DJANGO_SECRET_KEY` | Secret Production | Secret Preview distinct | Ne jamais partager le secret entre scopes |
| `DJANGO_DEBUG` | `false` | `false` | Aucun traceback public |
| `DJANGO_ALLOWED_HOSTS` | Domaine(s) réel(s) | Domaine(s) Preview autorisé(s) | Pas de `*` global |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origines HTTPS de Production | Origines HTTPS Preview autorisées | Vérifier POST et cookies |
| `DATABASE_URL` | Neon Production | Neon Preview isolée | **Interdiction absolue de réemploi** |
| `DJANGO_LOG_LEVEL` | Niveau approprié | Niveau approprié | Journaux sans secrets |

**Attention aux URLs dynamiques** : `VERCEL_URL` peut varier selon chaque déploiement. La stratégie de noms d'hôtes autorisés doit être explicite et testée ; ne pas mettre un wildcard général pour contourner un problème de Preview. La présence de `APP_ENV=preview` **ne prouve pas** que la `DATABASE_URL` est sûre.

### 9.4 Statiques et première mise en ligne

La documentation Vercel indique que si `STATIC_ROOT` est défini, Vercel exécute `collectstatic` lors du build et sert les fichiers collectés depuis son CDN. Valider via une requête HTTP réelle vers les fichiers CSS.

La première migration Neon doit être effectuée via une procédure séparée avant l'ouverture d'une interface nécessitant les tables correspondantes. **Un build réussi sans tables PostgreSQL n'est pas une recette fonctionnelle.**

### 9.5 Contrôle du déploiement en présence de la CI

- GitHub : les checks requis bloquent les **fusions normales** sur `main`.
- Vercel : la connexion Git déclenche la construction du déploiement sur push/merge.
- Si un contrôle de promotion en production est nécessaire, configurer des **Deployment Checks** basés sur les statuts GitHub appropriés ou le mécanisme équivalent disponible. Tester une release volontairement invalide et vérifier que le domaine de production **ne bascule pas**.
- Ne pas confondre « déploiement créé » et « nouveau déploiement promu au domaine de production ».
- Les check jobs GitHub utilisés comme Deployment Checks doivent avoir des **noms uniques et stables**, pour éviter les collisions de statuts.

### Gate Vercel

- [ ] URL Production en HTTPS.
- [ ] Version en ligne correspond au SHA Git.
- [ ] Fichiers statiques accessibles.
- [ ] Admin protégé ; DEBUG désactivé.
- [ ] Variables Preview et Production distinctes.
- [ ] Règle réelle de promotion vérifiée si cette fonction a été retenue.

---
