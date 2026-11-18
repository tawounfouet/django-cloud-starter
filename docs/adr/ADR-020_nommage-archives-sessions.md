# ADR-020 - Nommage date, projet, rang et sujet des archives de session

- **Statut** : Acceptee.
- **Contexte** : les archives etaient nommees `YYYY-MM-DD_session_<topic>.md`, sans nom de projet, et le tri alphabetique ne refletait pas l'ordre de creation. L'utilisateur devait renommer manuellement les fichiers pour ajouter le projet, et un rang etait necessaire pour ordonner les sessions d'une meme journee.
- **Decision** : adopter `YYYY-MM-DD_session_<project-slug>_<NNN>_<topic-slug>.md`. La date reste en premier, le projet suit le separateur `session`, le rang sur trois chiffres vient juste avant le sujet, et chaque archive porte `**Rang**: NNN` dans son en-tete.
- **Alternatives** : conserve le nom court sans projet, prefixer le rang avant la date, utiliser un horodatage complet a la place du rang.
- **Consequences** : les fichiers se trient par date puis par ordre de creation ; les references croisees doivent etre mises a jour lors d'un renommage ; le skill global `session-archive` a ete modifie et doit etre recharge par un redemarrage d'opencode.
- **Revoir si** : le projet change de nom, les sessions ne tiennent plus dans trois chiffres, ou un outil externe exige un format different.
- **Liens** : `docs/analysis/2026-11-18_nommage-archives-sessions.md`, `archives/chats/`, `~/.config/opencode/skills/session-archive/SKILL.md`.
