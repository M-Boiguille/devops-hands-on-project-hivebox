# 02: Gestion de Projet Logiciel (Agile)

## 1. Pourquoi l'Agile en DevOps ?
L'approche traditionnelle (Waterfall/Cycle en V) est trop rigide et lente. L'Agile privilégie **l'adaptation au changement** plutôt que le suivi d'un plan fixe.
*   **Manifeste Agile (Version DevOps)** :
    *   Les individus et leurs interactions > Les processus et les outils.
    *   Un logiciel fonctionnel > Une documentation exhaustive.
    *   La collaboration avec le client > La négociation contractuelle.
    *   L'adaptation au changement > Le suivi d'un plan.

## 2. Le Cycle de Vie (SDLC Modernisé)
Le cycle n'est plus une ligne droite mais une boucle infinie (symbole ∞ DevOps).
1.  **Plan** : Définir le "Quoi" (Requirements) et le "Pourquoi".
2.  **Code** : Développement modulaire.
3.  **Build** : Compilation et packaging (Docker images).
4.  **Test** : Tests unitaires, d'intégration, de sécurité (automatisés).
5.  **Release** : Déploiement en staging/prod.
6.  **Deploy/Operate** : Infrastructure as Code, Orchestration.
7.  **Monitor** : Feedback loop (Logs, Metrics). -> *Retour à Plan*.

## 3. Le Mindset MVP (Minimum Viable Product)
C'est la stratégie recommandée pour les projets DevOps (ex: projet HiveBox).
*   **Principe** : Ne pas construire la "Ferrari" tout de suite. Construire d'abord un skateboard, puis une trottinette, puis un vélo.
*   **Mantra** : *"Make it work, make it right, make it fast"* (Fais-le marcher, fais-le proprement, optimise-le).
    *   *Junior* : Veut tout optimiser dès le début (Over-engineering).
    *   *Senior* : Livrer une version V0.1 fonctionnelle rapidement pour avoir du feedback.

---
**Sources & Références :**
*   [DevOpsRoadmap.io] Module 3 & 7: Planning & Capstone Project

---
_Contenu produit par Perplexity AI et enrichi par ma propre contribution._
