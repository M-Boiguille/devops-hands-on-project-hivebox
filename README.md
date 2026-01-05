# HiveBox

> Ce repository est un fork pédagogique du projet HiveBox du parcours **Dynamic DevOps Roadmap**, adapté pour mon portfolio et mon apprentissage personnel. [web:3]

L’objectif est de construire, étape par étape, une plateforme fictive de type “HiveBox” en appliquant les bonnes pratiques DevOps modernes (MVP, automatisation, feedback loop). [web:3]

---
# PHASE 2

## Objectifs d’apprentissage

- Mettre en pratique un **projet DevOps de bout en bout** sur un cas réaliste.
- Apprendre à travailler par **petites itérations** (MVP, amélioration continue).
- Structurer le travail en **phases graduelles** plutôt qu’en gros “one shot”.

## Application
- Version actuelle : **v0.0.1**
- Versioning : **Semantic Versioning**
- #Docker, #Python, #Makefile

app/
├── Makefile
├── README.md
├── app
├── Dockerfile
└── main.py

L’application se limite volontairement à un **MVP minimal** :
- peut se lancer avec un Makefile
- application exécutée dans un conteneur Docker
- affiche la version courante
- quitte immédiatement

### Utilisation

#### Construire l’image **hivebox:0.0.1**:
```bash
make build
````
---

#### Lancer l’application

```bash
make run
```

Résultat attendu :

```
v0.0.1
```

Le conteneur s’exécute puis s’arrête immédiatement.

---

#### Lancer avec nettoyage automatique

* Nettoyage avant exécution :

```bash
make forced_run
```

* Nettoyage après exécution :

```bash
make temp_run
```

---

#### Nettoyer manuellement

```bash
make clean
```

Supprime le conteneur `hivebox` s’il existe.

---

### Tests

Le test consiste à vérifier que :

* le conteneur démarre correctement
* l’application affiche bien la version attendue
* le processus se termine sans erreur

Ce test est volontairement simple à ce stade (Phase initiale / MVP).

---

## 📌 Notes

* Le dépôt suit un **workflow par phases**
* Chaque phase est livrée via une **Pull Request vers `main`**
* Aucun push direct sur `main`

---

## 📚 Référence

Projet original :
[https://devopsroadmap.io/projects/hivebox/](https://devopsroadmap.io/projects/hivebox/)
