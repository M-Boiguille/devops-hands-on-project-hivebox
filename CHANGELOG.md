# Changelog HiveBox

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [3.4.3] - 2026-01-09 (phase 3.4 - Final)

### Fixed
- Ajout de patch.dict pour mocker APP_VERSION dans test_version_ok
- Correction de l'erreur 500 causée par une variable d'environnement manquante
- L'environnement de test correspond maintenant aux exigences de production

### Tests
- Tous les tests passent : 10/10 ✅

## [3.4.2] - 2026-01-09

### Changed
- Renommage des variables dans __main__ pour éviter les conflits de portée (startup_config, startup_version)
- Remplacement de l'exception générale Exception par des exceptions spécifiques (FileNotFoundError, ValueError, OSError)
- Utilisation de sys.exit() au lieu de exit() pour une terminaison appropriée du script

### Added
- Documentation complète des meilleures pratiques dans notes.md
- Documentation des patterns de gestion d'erreurs et conventions Python

### Quality
- Score Pylint : 9.51/10 → 10.00/10 ✅

## [3.4.1] - 2026-01-09

### Fixed
- Changement d'import relatif vers import absolu (`from . import helpers` → `from app import helpers`)
- Ajout du bloc `__main__` à main.py pour une exécution CLI appropriée avec affichage de version
- Correction du test pour utiliser sys.executable au lieu de la commande 'python' codée en dur
- Amélioration du test pour éviter le démarrage du serveur en testant uniquement les imports
- Structure de package appropriée pour la compatibilité CI/CD

### Tests
- Tous les tests passent : 10/10 ✅

## [3.3.7] - 2026-01-08

### Changed
- Display pylint score in CI output
- Add score=y flag for better visibility
- Help track code quality metrics

## [3.3.6] - 2026-01-08

### Changed
- Remove redundant workflow steps
- Streamline CI configuration
- Improve workflow efficiency

## [3.3.5] - 2026-01-08

### Added
- Add pylint step to CI/CD pipeline with score threshold
- Install pylint in workflow
- Run pylint on app directory to enforce code quality
- Ensure 8/10 minimum score requirement

## [3.3.4] - 2026-01-08

### Changed
- Remove commented code in helpers.py
- Add blank line after docstring in main.py
- Improve line breaks for HTTPException for better readability
- Fix spacing around function definitions

## [3.3.3] - 2026-01-08

### Fixed
- Fix last remaining trailing whitespace in helpers.py
- Complete PEP 8 compliance for whitespace

## [3.3.2] - 2026-01-08

### Fixed
- Clean up trailing whitespace issues for PEP 8 compliance
- Add missing test case in test_unit.py

## [3.3.1] - 2026-01-08

### Fixed
- Replace bare except with specific exceptions (requests.RequestException, ValueError, KeyError)
- Fix trailing whitespaces and indentation for PEP 8 compliance
- Improve code readability in helpers.py and main.py

## [3.3.0] - 2026-01-08

### Added
- Meilleures pratiques Docker
- Amélioration de la robustesse de l'application

## [3.2.0] - 2026-01-08

### Added
- Route API `/temperature` pour récupérer la température moyenne des senseBox
- Route API `/version` pour vérifier la version de l'application
- Tests unitaires complets pour toutes les routes
- Intégration avec l'API OpenSenseMap

## [3.1.0] - 2026-01-08

### Added
- API FastAPI de base avec endpoint `/`
- Structure du projet phase-3
- Configuration Docker
