# ADR-019 - Suivi local des taches avec fiches Markdown

- **Statut** : Retenue pour experimentation.
- **Contexte** : le projet doit inventorier les taches effectuees a une frequence quotidienne, hebdomadaire ou en fin de jalon, tout en gardant le backlog comme source de verite et en se preparant a une migration future vers GitHub Issues.
- **Decision** : utiliser `TODO.md` comme vue d'ensemble, `CHANGELOG.md` comme journal des livrables, et `docs/tasks/` avec une fiche Markdown par tache active ou complexe. Le demarrage initial etait limite a US-008, US-009, US-010 et US-011, puis etendu aux 52 stories a la demande de l utilisateur.
- **Alternatives** : `TODO.md` seul, GitHub Issues/Projects immediate, ajout de toutes les fiches des le depart.
- **Consequences** : contexte et preuves tracables par tache ; mise a jour supplementaire a chaque commit ; migration future facilitee par un frontmatter stable.
- **Revoir si** : le nombre de fiches actives depasse 15, la synchronisation devient une charge, ou le besoin de collaboration multi-utilisateur justifie GitHub Issues.
- **Liens** : `docs/analysis/2026-11-18_suivi-taches-markdown-vers-github.md`, `TODO.md`, `CHANGELOG.md`, `docs/tasks/`.
