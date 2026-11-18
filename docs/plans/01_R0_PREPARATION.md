# Plan 04 - R0 - Préparation et prérequis

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 4. R0 - Préparation et prérequis

### 4.1 Contrôle des accès et des contraintes

- [ ] Confirmer le propriétaire du dépôt, son caractère public/privé, les personnes autorisées à fusionner et le nom de `main`.
- [ ] Confirmer que le plan Vercel autorise effectivement la nature de l'activité ; **Hobby ne doit pas être retenu par défaut pour une application commerciale**.
- [ ] Confirmer la région d'exécution Vercel et la région PostgreSQL Neon, idéalement proches et compatibles avec les exigences de données.
- [ ] Vérifier les plans Neon et Vercel, limites, éventuels moyens de paiement et protections disponibles pour les Previews.
- [ ] Définir si des données personnelles existent. Pour le starter MVP, utiliser **uniquement des données synthétiques**.
- [ ] Décider si le domaine personnalisé est différé à R4, ce qui est recommandé.
- [ ] Définir un responsable des secrets, migrations, releases et tests GO / NO-GO.

### 4.2 Outils locaux à réunir

| Outil | Rôle | Vérification |
|---|---|---|
| Git | Historique et push | `git --version` |
| Python 3.12 candidat | Runtime local | `python3 --version` ou `uv run python --version` |
| `uv` | Dépendances et lockfile | `uv --version` |
| PostgreSQL local (facultatif) | Test d'intégration développeur | `psql --version` |
| GitHub | Dépôt/PR | Accès au dépôt validé |
| Vercel | Hébergement | Compte et plan vérifiés |
| Neon | PostgreSQL | Projet/plan/région validés |

**Sortie R0 :** décisions OA bloquantes tranchées et accès disponibles. Aucune ressource payante n'est créée implicitement.

---
