# Analyse - Nommage des archives de session

| Champ | Valeur |
|---|---|
| Date | 18 novembre 2026 |
| Statut | Retenu, voir `ADR-020` |
| Perimetre | Nommage, classement et reference croisee des archives de session |
| Liens | `ADR-020`, `archives/chats/`, skill global `session-archive` |

## 1. Question posee

Comment nommer les archives de session pour que l'ordre lexicographique des fichiers corresponde a l'ordre de creation, tout en gardant la date en premier et en rendant le projet explicitement visible ?

## 2. Constat

Le skill global `session-archive` produisait `YYYY-MM-DD_session_<topic-slug>.md`. Le nom de projet n'etait pas inclus : il etait ajoute manuellement apres coup. De plus, quatre archives du 18 novembre 2026 etaient triees par ordre alphabetique, ce qui placait `docs-restructuration-sdlc` avant `r11-conformite` alors que la conformite R1.1 avait ete archivee plus tot.

## 3. Options envisagees

| Option | Avantages | Risques | Verdict |
|---|---|---|---|
| `YYYY-MM-DD_session_<topic>.md` | Court, deja documente dans le skill | Pas de projet, ordre alphabetique trompeur | Rejete |
| `NNN_YYYY-MM-DD_session_<projet>_<sujet>.md` | Le rang trie immediatement | La date n'est plus en premier, convention cassee | Rejete |
| `YYYY-MM-DD_session_<projet>_<NNN>_<sujet>.md` | Date d'abord, projet explicite, rang avant le sujet | Le rang doit etre calcule a chaque archive | Retenu |

## 4. Convention retenue

```text
YYYY-MM-DD_session_<project-slug>_<NNN>_<topic-slug>.md
```

| Element | Regle | Exemple |
|---|---|---|
| `YYYY-MM-DD` | Date ISO, toujours en premier | `2026-11-18` |
| `session` | Separateur fixe apres la date | `session` |
| `<project-slug>` | Nom du depot ou du dossier de travail, minuscule et hyphenne | `django-cloud-starter` |
| `<NNN>` | Rang sur trois chiffres, attribue par ordre de creation | `001` |
| `<topic-slug>` | Sujet minuscule, hyphenne, 30 caracteres maximum | `bootstrap-r11` |

Le rang se calcule en scannant `archives/chats/` pour le projet concerne et en prenant `max(ranks) + 1`, avec zero padding sur trois chiffres. Comme la date vient avant le rang, le tri lexicographique reste d'abord chronologique, puis le rang ordonne les sessions d'un meme jour.

## 5. Application aux archives existantes

| Rang | Fichier | Ordre de creation |
|---|---|---|
| 001 | `2026-11-18_session_django-cloud-starter_001_bootstrap-r11.md` | 09:10 |
| 002 | `2026-11-18_session_django-cloud-starter_002_r11-conformite.md` | 09:19 |
| 003 | `2026-11-18_session_django-cloud-starter_003_docs-restructuration-sdlc.md` | 09:49 |
| 004 | `2026-11-18_session_django-cloud-starter_004_suivi-taches-et-adr.md` | 10:25 |

Les references croisees dans les quatre archives ont ete mises a jour, ainsi que les doubles prefixes temporaires apparus pendant la migration. Chaque archive porte aussi `**Rang**: NNN` dans son en-tete.

## 6. Consequences

| Effet | Detail |
|---|---|
| Plus de renommage manuel | Le skill global `session-archive` genere directement le projet et le rang |
| Tri fiable | `ls archives/chats/*.md` suit l'ordre de creation |
| lisibilite | Le projet est visible sans ouvrir le fichier |
| Maintenance | Le rang doit etre recalcule si une archive est inseree ou renommee |
| Configuration | Le skill etant global, un redemarrage d'opencode est necessaire |

## 7. Risques et mesures

| Risque | Mesure |
|---|---|
| Deux sessions concurrentes obtiennent le meme rang | Verifier les fichiers existants juste avant l'ecriture |
| Changement de nom de projet | Garder le slug existant pour les archives passees |
| Reference obsolete apres renommage | Mettre a jour toutes les sections `Related Sessions` dans le meme temps |
| `archives/` ignore par Git | La convention reste documentee ici et dans le skill global |

## 8. Decision

Voir `docs/adr/ADR-020_nommage-archives-sessions.md` pour la decision formelle et les conditions de reexamen.
