# Plan 04 - R4 et R5 - Cloudflare et industrialisation

> Extrait de `docs/specs/04_PLAN_IMPLEMENTATION_ET_CI_CD.md`. Retour à l'index : [`00_INDEX.md`](00_INDEX.md).

## 14. R4 - Cloudflare optionnel

| Besoin observé | Service Cloudflare envisageable | Décision de départ |
|---|---|---|
| Domaine personnalisé | DNS Cloudflare | Activer en **DNS-only** pour les enregistrements liés à Vercel |
| Formulaire public exposé aux abus | Turnstile | Vérification serveur obligatoire si activé |
| Téléversements utilisateurs | R2 (ou stockage objet alternatif) | Comparer les solutions et en choisir une |
| Exigence edge supplémentaire prouvée | Proxy/WAF Cloudflare | Étudier les interactions avec Vercel avant activation |

**Ne pas mettre Cloudflare en proxy orange par automatisme.** Une configuration DNS-only ne place pas le WAF Cloudflare sur le trajet HTTP. Vercel assure alors directement HTTPS/CDN pour l'application. R2 n'est pas nécessaire pour `collectstatic` ; son usage concerne les médias persistants des utilisateurs si ce besoin apparaît.

---

## 15. R5 - Industrialisation proportionnée

- Réexécuter le bootstrap depuis un clone vierge et établir un guide de réutilisation.
- Étudier les améliorations de sécurité de la chaîne CI : actions figées sur SHA, revue des dépendances, droits GitHub réduits, journaux conservés.
- Améliorer la qualité du runtime avec quelques mesures réelles : latence, cold start, échecs, connexions PostgreSQL, coût.
- N'introduire DRF, React, un worker, un workflow durable ou un Py**Kit que si une story métier et ses critères d'acceptation le justifient.
- Ne pas transformer le starter en framework maison généraliste avant d'avoir au moins une première application utilisatrice.

---
