# Analyse - Suivi local des taches et migration vers GitHub Issues

| Champ | Valeur |
|---|---|
| Date | 18 novembre 2026 |
| Statut | Retenu pour experimentation, voir `ADR-019` |
| Perimetre | Suivi d'avancement, inventaire periodique et preparation GitHub Issues |
| Liens | `TODO.md`, `CHANGELOG.md`, `docs/tasks/`, `ADR-019` |

## 1. Question posee

Comment inventorier les taches effectuees a une frequence donnee, quotidienne, hebdomadaire ou en fin de projet, sans creer une source de verite parallele ni alourdir le depot ?

## 2. Options envisagees

| Option | Avantages | Risques | Verdict |
|---|---|---|---|
| `TODO.md` seul avec cases a cocher | Simple et lisible | Perd le contexte, liste plate | Insuffisant seul |
| `TODO.md` + `CHANGELOG.md` | Separe etat et historique | Ne dit pas pourquoi ni comment la tache a ete prouvee | Utile mais incomplet |
| `docs/tasks/` + `TODO.md` + `CHANGELOG.md` | Contexte riche, metadonnees, preuves, liens sources | 52 fiches des le depart = charge de maintenance | Retenu avec demarrage progressif |
| GitHub Issues/Projects immediat | Collaboration native et automatisations | Depend du compte GitHub, migration prematuree | Differe |

## 3. Recommendation retenue

1. `docs/specs/02_BACKLOG_ET_USER_STORIES.md` reste la source de verite des besoins et criteres d'acceptation.
2. `docs/tasks/` contient une fiche par tache active ou complexe, avec frontmatter et preuves.
3. `TODO.md` sert de vue d'ensemble et `CHANGELOG.md` de journal des livrables.

Le demarrage initial etait limite aux quatre stories R1.2. La demande suivante etend le dispositif aux 52 stories, y compris celles deja implementees, tout en gardant le backlog comme source de verite.

## 4. Modele de fiche

| Champ | Type | Usage |
|---|---|---|
| `id` | texte | Identifiant stable, par exemple `US-008` |
| `epic`, `phase`, `gate` | texte | Rattachement au backlog et au jalon |
| `priority`, `size` | texte | Priorisation et dimensionnement |
| `status` | texte | `todo`, `doing`, `review`, `done`, `blocked` |
| `owner` | texte ou `null` | Responsable courant |
| `depends_on`, `blocks` | liste | Graphe de dependances |
| `commits`, `evidence` | liste | Tracabilite apres execution |
| `backlog`, `plan` | chemin | Liens vers les documents sources |

Le corps contient : contexte, criteres d'acceptation, plan d'action, preuves attendues, journal et notes.

## 5. Rythme de mise a jour

| Frequence | Action | Fichier concerne |
|---|---|---|
| A chaque commit | Completer `commits` et `evidence`, cocher la story | `docs/tasks/`, `TODO.md` |
| Quotidien | Verifier les fiches `doing` et les bloquants | `docs/tasks/` |
| Hebdomadaire | Lire le suivi ASCII et inventarier les cases cochees | `TODO.md`, `CHANGELOG.md` |
| A chaque gate | Comparer les stories `done` avec les criteres de sortie | `docs/plans/00_INDEX.md` |
| En fin de projet | Archiver l'etat et basculer vers GitHub Issues | `docs/tasks/`, `CHANGELOG.md` |

## 6. Migration vers GitHub Issues

| Champ local | Champ GitHub |
|---|---|
| `id` plus titre | Titre prefixe |
| `epic`, `phase`, `priority` | Labels |
| `owner` | Assigne |
| `status` | Champ de projet |
| `commits`, `evidence` | Commentaire ou attachement |

## 7. Risques et mesures

| Risque | Mesure |
|---|---|
| Fiches non mises a jour | Mise a jour obligatoire dans la DoD locale |
| Duplication avec le backlog | Le backlog garde les criteres, la fiche garde l'execution |
| Trop de fiches des le depart | Demarrage limite a R1.2 |
| Migration GitHub complexe | Frontmatter stable et mapping simple |

## 8. Decision

Voir `docs/adr/ADR-019_suivi-taches-markdown-local.md` pour la decision formelle et les conditions de reexamen.
