# 05: Docker – Bonnes Pratiques & Images de Production

## 1. Objectif de Docker en contexte DevOps
Docker n’est pas un outil de virtualisation, mais un **outil de packaging applicatif**.
* **Objectif principal** : Garantir la **reproductibilité** entre dev, CI et prod.
* **Erreur classique** : Traiter une image Docker comme une VM (SSH, systemd, tools inutiles).

---

## 2. Images Docker : principes fondamentaux

### 2.1 Une image = une responsabilité
* Une image doit exécuter **un seul process principal**.
* Pas de cron, pas de supervisor, pas de multitâche.
* Pattern recommandé : **1 container = 1 service**.

### 2.2 Images petites = images sûres
* Moins de surface d’attaque
* Téléchargement plus rapide
* Démarrage plus rapide

**Règle** :  
> Si ton image dépasse ce qui est nécessaire à l’exécution → elle est trop grosse.

---

## 3. Base image : choix stratégique

### 3.1 Préférer les images officielles
* Maintenues
* Scannées
* Documentées

Exemples :
* `python:3.12-slim`
* `node:20-alpine`
* `nginx:alpine`

### 3.2 Éviter `latest`
* `latest` n’est **pas déterministe**
* Peut casser ta prod sans changement de code

✅ Bon :
```dockerfile
FROM python:3.12-slim
````

❌ Mauvais :

```dockerfile
FROM python:latest
```

---

## 4. Dockerfile : bonnes pratiques essentielles

### 4.1 Ordre des instructions (cache Docker)

Docker met en cache chaque couche.

**Principe** :

* Ce qui change le moins → en haut
* Ce qui change le plus → en bas

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

---

### 4.2 Ne jamais installer en root en prod

* Le container tourne **par défaut en root**
* C’est un **risque de sécurité majeur**

```dockerfile
RUN useradd -m appuser
USER appuser
```

---

### 4.3 Nettoyer après installation

Toujours supprimer les caches inutiles.

❌ Mauvais :

```dockerfile
RUN apt-get update && apt-get install -y curl
```

✅ Bon :

```dockerfile
RUN apt-get update \
 && apt-get install -y curl \
 && rm -rf /var/lib/apt/lists/*
```

---

## 5. Multi-stage builds (OBLIGATOIRE en prod)

### 5.1 Problème

* Outils de build (gcc, pip, npm) inutiles en prod
* Augmentent taille + surface d’attaque

### 5.2 Solution : multi-stage

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

---

## 6. Configuration & secrets

### 6.1 Jamais dans l’image

❌ Ne jamais :

* hardcoder des secrets
* copier `.env` dans l’image
* stocker des clés API dans le Dockerfile

### 6.2 Utiliser les variables d’environnement

```bash
docker run -e APP_ENV=prod myapp
```

Ou via :

* GitHub Actions secrets
* Kubernetes Secrets
* Vault

---

## 7. Docker et CI/CD

### 7.1 Dockerfile = artefact critique

Il doit être :

* linté (`hadolint`)
* testé
* versionné

### 7.2 Étapes CI recommandées

1. Lint Dockerfile
2. Build image
3. Scanner sécurité
4. Lancer tests
5. Publier image

---

## 8. Erreurs courantes à éviter (très important)

* ❌ Installer vim, curl, ping “au cas où”
* ❌ Debugger en SSH dans le container
* ❌ Utiliser `CMD bash`
* ❌ Coupler build et runtime
* ❌ Ignorer le cache Docker

---

## 9. Ce qu’un DevOps senior maîtrise vraiment

* Comprend **le cycle de vie complet** d’une image
* Sait expliquer **pourquoi** une image est mauvaise
* Pense **sécurité + performance + maintenabilité**
* Optimise pour la CI autant que pour la prod

---

**Sources & Références :**

* Ahmed AbouZaid – Docker Best Practices Workshop
* Docker Official Documentation
* Google SRE – Container Best Practices

---

*Contenu synthétisé et structuré à des fins pédagogiques DevOps.*
