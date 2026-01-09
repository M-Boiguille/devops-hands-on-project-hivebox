# Notes de développement HiveBox

## 9 janvier 2026 - Correction des erreurs d'import Python

### ❌ Ce que j'ai fait de mal

1. **Imports relatifs mal utilisés**
   - J'ai utilisé `from . import helpers` dans [app/main.py](app/main.py)
   - Les imports relatifs (avec `.`) ne fonctionnent QUE quand le module est importé comme partie d'un package
   - Quand on exécute directement `python app/main.py`, Python ne sait pas que `app` est un package
   - Erreur: `ImportError: attempted relative import with no known parent package`

2. **Test mal conçu**
   - Le test exécutait `python app/main.py` directement
   - Cette méthode ne respecte pas la structure de package Python
   - Ça fonctionnerait en développement local mais échoue dans CI/CD

3. **Pas de point d'entrée CLI**
   - Le fichier [main.py](app/main.py) n'avait pas de bloc `if __name__ == "__main__":`
   - Impossible de tester l'application en ligne de commande
   - Pas de message de version affiché au démarrage

### ✅ Ce que j'ai corrigé

1. **Import absolu au lieu de relatif**
   ```python
   # Avant (❌)
   from . import helpers
   
   # Après (✅)
   from app import helpers
   ```
   - L'import absolu fonctionne dans tous les contextes
   - Compatible avec l'exécution en module (`python -m app.main`)
   - Compatible avec l'import standard (`from app.main import app`)

2. **Ajout du bloc `__main__`**
   ```python
   if __name__ == "__main__":
       # Charge config, affiche version, démarre serveur
   ```
   - Permet d'exécuter le module avec `python -m app.main`
   - Affiche la version au démarrage
   - Point d'entrée propre pour les tests

3. **Correction du test**
   ```python
   # Avant (❌)
   subprocess.run(["python", "app/main.py"], ...)
   
   # Après (✅)
   subprocess.run([sys.executable, "-c", "import..."], ...)
   ```
   - Utilise `sys.executable` pour avoir le bon interpréteur Python
   - Évite de démarrer le serveur qui bloquerait le test
   - Teste simplement que les imports fonctionnent et que la version s'affiche
   - Configure le `cwd` (current working directory) correctement pour les imports

### 📚 Ce que je dois apprendre

#### 1. **Structure de package Python professionnelle**
   - Toujours traiter `app/` comme un package avec `__init__.py`
   - Utiliser des imports absolus pour le code réutilisable
   - Réserver les imports relatifs pour des cas très spécifiques

#### 2. **Méthodes d'exécution Python**
   ```bash
   # ❌ N'utilise pas les packages correctement
   python app/main.py
   
   # ✅ Exécute comme module (recommandé)
   python -m app.main
   
   # ✅ Alternative avec uvicorn
   uvicorn app.main:app --reload
   ```

#### 3. **Différence entre script et module**
   - **Script**: fichier Python exécuté directement → pas de contexte package
   - **Module**: partie d'un package Python → contexte package complet
   - Un fichier peut être les deux avec un bon bloc `__main__`

#### 4. **Best practices pour imports**
   - **Imports absolus**: pour code partagé et API publique
   - **Imports relatifs**: uniquement à l'intérieur d'un package pour éviter les dépendances circulaires
   - Toujours tester avec `python -m` pour valider la structure

#### 5. **Tests et CI/CD**
   - Les tests doivent refléter l'utilisation réelle du code
   - Ne pas se fier aux comportements "qui marchent localement"
   - Toujours tester comme si le code était installé en tant que package
   - **Utiliser `sys.executable`** dans subprocess plutôt que `"python"` hardcodé
   - Éviter de démarrer des serveurs dans les tests unitaires (utiliser des mocks ou imports simples)

#### 6. **Point d'entrée d'application**
   - Toujours fournir un `if __name__ == "__main__":` pour les applications
   - Afficher les informations de version/démarrage
   - Gérer proprement les erreurs de configuration

### 🎯 Résumé des règles à suivre

1. ✅ Utiliser `from app import helpers` (import absolu)
2. ✅ Exécuter avec `python -m app.main` (pas `python app/main.py`)
3. ✅ Toujours ajouter un bloc `__main__` aux points d'entrée
4. ✅ Structurer le projet comme un vrai package Python
5. ✅ Tester avec les mêmes commandes que la CI/CD utilisera

### 📖 Ressources à étudier
- [PEP 8 - Imports](https://pep8.org/#imports)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Real Python - Absolute vs Relative Imports](https://realpython.com/absolute-vs-relative-python-imports/)
- [Python's `-m` flag](https://docs.python.org/3/using/cmdline.html#cmdoption-m)

---

## 9 janvier 2026 - Correction des warnings Pylint (10/10)

### ❌ Ce que j'ai fait de mal

1. **Redéfinition de noms (W0621: redefined-outer-name)**
   - J'ai utilisé `config` comme paramètre dans les fonctions `get_version()` et `get_temperature()`
   - Puis j'ai réutilisé `config` dans le bloc `__main__` au niveau module
   - Même problème avec `app_version`
   - Pylint détecte que je redéfinis des noms qui existent dans la portée externe
   - Rend le code confus et peut causer des bugs subtils

2. **Exception trop générale (W0718: broad-exception-caught)**
   ```python
   except Exception as e:  # ❌ Trop vague
   ```
   - Capturer `Exception` attrape TOUS les types d'erreurs
   - Cache des bugs que je devrais voir (TypeError, AttributeError, etc.)
   - Empêche le débogage efficace
   - Mauvaise pratique en production

3. **Utilisation de exit() au lieu de sys.exit() (R1722: consider-using-sys-exit)**
   ```python
   exit(1)  # ❌ Builtin non standard
   ```
   - `exit()` est un builtin pour le shell interactif
   - `sys.exit()` est la méthode standard pour les scripts
   - `exit()` peut ne pas être disponible dans tous les contextes

### ✅ Ce que j'ai corrigé

1. **Renommage des variables pour éviter les collisions**
   ```python
   # Avant (❌)
   if __name__ == "__main__":
       config = helpers.load_config()
       app_version = os.getenv("APP_VERSION")
   
   # Après (✅)
   if __name__ == "__main__":
       startup_config = helpers.load_config()
       startup_version = os.getenv("APP_VERSION")
   ```
   - Les noms sont maintenant uniques et descriptifs
   - Pas de confusion avec les paramètres de fonction
   - Le code est plus clair

2. **Exceptions spécifiques au lieu d'Exception générique**
   ```python
   # Avant (❌)
   except Exception as e:
       print(f"Error: {e}")
   
   # Après (✅)
   except (FileNotFoundError, ValueError, OSError) as e:
       print(f"Error: {e}")
   ```
   - Ne capture que les erreurs attendues et gérables
   - Laisse passer les vraies erreurs de programmation
   - Meilleur debugging et maintenance

3. **Import et utilisation de sys.exit()**
   ```python
   # Avant (❌)
   exit(1)
   
   # Après (✅)
   import sys
   sys.exit(1)
   ```
   - Méthode standard et portable
   - Explicite et professionnel
   - Compatible avec tous les contextes d'exécution

### 📚 Ce que je dois apprendre

#### 1. **Portée des variables (Scope) en Python**
   - **Module scope**: Variables au niveau du fichier (globales)
   - **Function scope**: Paramètres et variables locales
   - **Block scope**: N'existe pas en Python (contrairement à JS/Java)
   - Éviter de réutiliser des noms entre différentes portées
   - Rend le code plus lisible et évite les bugs

#### 2. **Hiérarchie des exceptions Python**
   ```
   BaseException
   ├── SystemExit
   ├── KeyboardInterrupt
   └── Exception
       ├── ValueError
       ├── TypeError
       ├── OSError
       │   ├── FileNotFoundError
       │   └── PermissionError
       └── ...
   ```
   - **Toujours capturer l'exception la plus spécifique possible**
   - Ne JAMAIS capturer `BaseException` (sauf cas très rares)
   - Éviter de capturer `Exception` sauf si vraiment nécessaire
   - Préférer: `except (ValueError, TypeError) as e:`

#### 3. **Gestion d'erreurs professionnelle**
   ```python
   # ❌ Mauvais - cache tout
   try:
       do_something()
   except Exception:
       pass
   
   # ✅ Bon - gère ce qu'on attend
   try:
       with open(config_file) as f:
           config = json.load(f)
   except FileNotFoundError:
       print("Config file not found")
       sys.exit(1)
   except json.JSONDecodeError as e:
       print(f"Invalid JSON: {e}")
       sys.exit(1)
   ```

#### 4. **Builtin vs module standard library**
   - `exit()` et `quit()` : **builtins** pour usage interactif uniquement
   - `sys.exit()` : **standard** pour les scripts et applications
   - Autres exemples: `input()` (builtin) vs `sys.stdin.read()` (standard)
   - Toujours préférer les modules de la stdlib pour le code production

#### 5. **Conventions de nommage Python (PEP 8)**
   - Variables locales: `snake_case`
   - Constantes: `UPPER_CASE`
   - Ajouter des préfixes descriptifs pour éviter les collisions:
     - `startup_config` vs `config` (paramètre)
     - `user_input` vs `input` (builtin)
     - `temp_file` vs `file` (builtin)

#### 6. **Outils de qualité de code**
   - **pylint**: analyse statique complète, détecte bugs et mauvaises pratiques
   - **flake8**: vérification PEP 8 et erreurs basiques
   - **mypy**: vérification de types statiques
   - **black**: formatage automatique
   - Intégrer dans CI/CD pour maintenir la qualité

### 🎯 Règles à suivre pour la qualité du code

1. ✅ Ne jamais réutiliser des noms de variables entre différentes portées
2. ✅ Capturer uniquement les exceptions spécifiques attendues
3. ✅ Utiliser `sys.exit()` au lieu de `exit()` dans les scripts
4. ✅ Viser 10/10 sur pylint avant de commit
5. ✅ Laisser passer les vraies erreurs de programmation (bugs)
6. ✅ Nommer les variables de façon descriptive et sans ambiguïté

### 📊 Score obtenu
- **Avant**: 9.51/10 (5 warnings)
- **Après**: 10.00/10 (0 warnings) ✅

### 📖 Ressources à étudier
- [PEP 8 - Naming Conventions](https://pep8.org/#naming-conventions)
- [Python Exception Hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
- [Pylint Messages](http://pylint-messages.wikidot.com/)
- [Best Practices for Exception Handling](https://realpython.com/python-exceptions/)
- [Python's sys module](https://docs.python.org/3/library/sys.html)
