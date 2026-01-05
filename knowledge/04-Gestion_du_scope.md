# Fiche 04: Gestion du Scope & Scope Creep

## 1. Définition du Scope Creep
C'est la dérive des objectifs du projet.
*   *Exemple* : Vous deviez monter un serveur web simple. Finalement, on vous demande d'ajouter du monitoring avancé, puis un load balancer, puis une base de données répliquée... Résultat : rien n'est livré après 3 semaines.

## 2. La Méthode MoSCoW (Priorisation)
Pour éviter la dérive, classez chaque demande dans une de ces catégories :
*   **M - Must Have** : Vital. Si on l'enlève, le projet ne sert à rien. (C'est le MVP).
*   **S - Should Have** : Important mais pas vital. Peut attendre un peu.
*   **C - Could Have** : "Nice to have". On le fait seulement s'il reste du temps.
*   **W - Won't Have** : Hors scope pour cette fois. Peut-être plus tard.

## 3. DoR vs DoD (Définir les bornes)
Pour éviter les malentendus ("Je croyais que c'était fini !"), utilisez ces contrats :
*   **DoR (Definition of Ready)** : Critères pour *commencer* une tâche.
    *   *Exemple* : Le ticket est clair, les accès sont fournis, la maquette existe.
    *   *But* : Éviter de commencer un travail flou qui va s'éterniser.
*   **DoD (Definition of Done)** : Critères pour considérer la tâche *terminée*.
    *   *Exemple* : Code commité, Tests passés, Documentation écrite, Validé en staging.
    *   *But* : Éviter la "dette technique" et le faux travail fini ("C'est bon sur ma machine").

## 4. Stratégies Anti-Scope Creep pour DevOps
1.  **Dire "Non" (ou "Pas maintenant")** : La compétence n°1 du senior. Si une demande arrive et qu'elle n'est pas "Must Have", elle va dans le Backlog, pas dans le flux actuel.
2.  **Timeboxing** : Fixer une limite de temps stricte. "Je consacre 4h à setup le monitoring. Ce qui est fait est fait, ensuite je passe à autre chose."
3.  **Documentation des choix** : Noter pourquoi une feature a été rejetée ou reportée pour éviter qu'elle ne revienne par la fenêtre.

---
**Sources & Références :**
*   [DevOpsRoadmap.io] Alertes répétées sur le Scope Creep dans les modules 1, 3 et 4.
*   [KodeKloud] Soft Skills: Defining Scope and Managing Change.

---
_Contenu produit par Perplexity AI et enrichi par ma propre contribution._
