# Plan 04 - Gates, gouvernance et risques

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 16. Points de contrôle et GO / NO-GO

### 16.1 Gates par phase

| Gate | Condition obligatoire | Preuve | Bloque si |
|---|---|---|---|
| G0 | OA critiques, plan/région/dépôt confirmés | Décision R0 | Usage/plan non conformes |
| G1 | Django local CRUD/Auth/tests opérationnel | Tests, bootstrap | CRUD/permissions défaillants |
| G2 | PR CI verte/rouge testée, fusion protégée, URL Vercel HTTPS | Runs, déploiement, SHA | CI non bloquante ou secrets exposés |
| G3 | Neon persistant, Preview isolée, migrations séparées et maîtrisées | Test sentinelles, migration, persistance | Preview sur Prod, migration risquée |
| G4 | `CA-01` à `CA-13` conformes, runbook et rollback testés | PV GO / NO-GO | Critère critique non validé |

### 16.2 Matrice de traçabilité des 13 critères MVP

| Critère | Ce qui doit être démontré | Étape | Stories |
|---|---|---|---|
| CA-01 | Clone vierge, installation et démarrage local | R1.1 | US-005, US-017 |
| CA-02 | Application Django accessible en HTTPS | R2.2 | US-018, US-019 |
| CA-03 | CRUD connecté à PostgreSQL Neon | R3.1 | US-008/009, US-025 |
| CA-04 | Données conservées après redéploiement | R3.3 | US-020, US-028 |
| CA-05 | CI automatique sur PR | R2.1 | US-013/014 |
| CA-06 | Règles de fusion réellement bloquantes | R2.1 | US-016 |
| CA-07 | Déploiement sur `main` démontré | R2.2 | US-020 |
| CA-08 | Preview n'écrit pas sur Production | R3.1/R3.2 | US-021/026/031 |
| CA-09 | Auth/Admin/permissions sécurisés | R1.2/R3.4 | US-010/032/033 |
| CA-10 | Aucun secret réel dans Git | R1.1/R2.1 | US-006/013/034 |
| CA-11 | Migrations indépendantes et contrôlées | R3.2 | US-015/027 |
| CA-12 | Diagnostic, rollback et exploitation documentés | R3.4 | US-023/036/037/043 |
| CA-13 | Plan d'hébergement compatible avec l'usage | R0 | US-004/038 |

### 16.3 Conditions de NO-GO immédiat

- Preview configurée avec une URL de la base Production ou données sensibles non autorisées.
- Job PR disposant d'un secret Production ou droits privilégiés non justifiés.
- Migrations exécutées depuis un build Vercel ou au démarrage Django.
- Absence de contrôle des permissions pour l'Admin ou les écritures métier.
- Secret exposé dans les sources, un log ou une variable publique.
- Offre d'hébergement incompatible avec la nature réelle de l'application.
- Une modification de schéma invalide est rendue visible sans politique de compatibilité ou gate effectif.
- Critère d'acceptation obligatoire non démontré.

---

## 17. Dépendances, responsabilités et décisions

### 17.1 RACI simplifié

| Activité | Responsable de décision | Exécutant | Validation |
|---|---|---|---|
| Dépôt et accès GitHub | Propriétaire | Mainteneur | Politique de permissions |
| Choix du plan Vercel/Neon | Propriétaire | Mainteneur | Conformité et budget |
| Code Django et tests | Mainteneur | Développeur | CI et revue |
| Secret Production et migrations | Propriétaire/exploitant habilité | Workflow autorisé | Approbation + logs |
| Intégration Preview | Mainteneur | Vercel/Neon configurés | Test d'isolation |
| GO / NO-GO | Propriétaire désigné | Équipe de recette | PV de recette |

Une même personne peut tenir plusieurs rôles pour ce starter, mais la décision sensible reste distincte de l'exécution automatique.

### 17.2 Dépendances non techniques

- Consentement à toute création de service ou facturation potentielle.
- Conditions de licences du code et de publication du dépôt.
- Résidence et confidentialité des données selon l'application future.
- Disponibilité réelle des protections de branches, d'environnements GitHub et des Deployment Checks dans les plans utilisés.

---

## 18. Risques, tests négatifs et mesures préventives

| Risque | Niveau | Détection | Mesure / responsable |
|---|---|---|---|
| Preview rattachée à Production | Critique | Sentinelles, audit credentials/scope | US-026, responsable des données |
| Branches Neon contenant une copie de données personnelles | Critique | Vérification du parent et du dataset | Source synthétique, US-035 |
| Migration au build ou lors du bootstrap HTTP | Critique | Revue config, tests négatifs | Workflow séparé US-027 |
| Release code/schéma incompatible | Critique | Matrice de compatibilité et smoke test | Expand/migrate/contract, gates |
| Déploiement exposé avant résultat CI | Élevé | Test release volontairement invalide | Protection main + gate Vercel si requis |
| Secret dans Git/Actions/tracebacks | Élevé | Scan et revue | Scopes séparés, rotation |
| Rollback code supposé restaurer données | Élevé | Exercice de reprise | Procédure DB indépendante |
| Problèmes pool PostgreSQL et cold start | Moyen | Logs, connexion, latence | Pooling et mesure |
| Dépassement quotas / plan inadéquat | Moyen/élevé | Revue mensuelle ou au changement | Registre des plans |
| Double proxy Cloudflare/Vercel | Moyen | Essai HTTP/DNS | DNS-only par défaut |

---
