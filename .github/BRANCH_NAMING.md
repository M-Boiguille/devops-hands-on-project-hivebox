# Convention de nommage des branches

## Structure actuelle du projet

### Branches principales
- **`main`** : Branche principale stable avec code de production

### Branches de phases (workflow établi)
Le projet suit un workflow par phases numérotées. Chaque phase représente une étape majeure du développement.

**Format:** `phase-N-descriptif`
- `N` : Numéro de la phase (1, 2, 3, ...)
- `descriptif` : Description courte de l'objectif de la phase

### Branches existantes

#### Phase 1 - Initial Setup
- **`phase-1-initial-setup`** : Configuration initiale du projet
  - Setup de base
  - Structure du repository
  - Configuration Git et outils

#### Phase 2 - Docker & Container
- **`phase-2-docker-setup`** : Préparation Docker
  - Configuration initiale Docker
  - Setup de l'environnement de développement
  
- **`phase-2-container`** : Containerisation (release phase 2)
  - Image Docker finalisée
  - Makefile pour build et run
  - Documentation Docker

#### Phase 3 - API & Quality
- **`phase-3-api-quality`** : API FastAPI et qualité du code (en cours)
  - Routes `/version` et `/temperature`
  - Tests unitaires (10/10 ✅)
  - Score Pylint 10/10 ✅
  - CI/CD avec GitHub Actions
  - Documentation complète (notes.md, CHANGELOG.md)

## Règles générales

### ✅ À FAIRE
- Utiliser des tirets (`-`) pour séparer les mots
- Utiliser des minuscules uniquement
- Être descriptif mais concis
- Suivre le format `phase-N-descriptif`
- Supprimer les branches mergées après validation

### ❌ À ÉVITER
- Accents ou caractères spéciaux (~~tâche~~)
- Espaces
- CamelCase ou PascalCase
- Noms vagues comme "test", "fix", "temp"
- Branches personnelles sur origin

## Workflow des branches

```
main (production)
 │
 ├─ phase-1-initial-setup → merged to main
 │
 ├─ phase-2-docker-setup → merged to phase-2-container
 │   └─ phase-2-container → merged to main
 │
 └─ phase-3-api-quality (active)
     └─ merge to main when ready
```

## Commandes utiles

### Renommer une branche locale
```bash
git branch -m ancien-nom nouveau-nom
```

### Renommer une branche sur origin
```bash
# Pousser la nouvelle branche
git push origin nouveau-nom

# Supprimer l'ancienne branche
git push origin :ancien-nom

# Mettre à jour le tracking
git branch -u origin/nouveau-nom nouveau-nom
```

### Nettoyer les références distantes obsolètes
```bash
git fetch --prune
```

## Historique des renommages

### 2026-01-09 - Standardisation des noms
- `tâche-1-démarrage` → `phase-1-initial-setup`
- `tâche-2-préparation` → `phase-2-docker-setup`
- `phase-2` → `phase-2-container`
- `phase-3` → `phase-3-api-quality`

**Raison:** Uniformiser la nomenclature, supprimer les accents, rendre les noms plus descriptifs et professionnels.
