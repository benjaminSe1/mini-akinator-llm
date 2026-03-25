Je construis un projet Python : un mini Akinator hybride avec moteur logique + LLM.

Contexte :
- Dev expérimenté (plutôt JS / web)
- Reprise de Python après longtemps
- Environnement : Windows + WSL
- Je veux comprendre, pas copier-coller

Objectif du projet :
- dataset de personnages (JSON)
- moteur logique qui :
  - garde des candidats
  - choisit la meilleure question (split optimal)
  - filtre selon réponse (yes/no/unknown)
- LLM local (Ollama) pour :
  - reformuler les questions
  - interpréter les réponses utilisateur
- CLI jouable

Stack :
- Python 3.12+
- uv
- ruff
- pytest
- pydantic
- typer (plus tard)
- ollama (plus tard)

État actuel du projet :

✅ Setup
- projet initialisé avec uv
- pyproject.toml configuré
- venv OK

✅ Tooling
- ruff OK
- mypy OK
- pytest OK
- format + lint auto dans VS Code

✅ Structure
- src/ layout en place
- data/characters/
- tests/

✅ Models (Pydantic)
- Character
- AnswerValue (StrEnum)
- ParsedAnswer

✅ Dataset
- 10 personnages Harry Potter en JSON

✅ Loader
- load_characters(Path) → list[Character]

✅ Engine (terminé)
- Question (dataclass)
- GameState (dataclass)
- QUESTION_BANK
- pick_best_question (algo de split)
- apply_answer (filtrage immuable)
- should_guess

⏳ En cours
- écrire les tests du moteur (pytest)

🔜 Prochaines étapes
1. tests/test_engine.py
2. valider moteur
3. ajouter couche LLM (ollama)
4. CLI (typer)
5. boucle de jeu complète

Ce que j’attends de toi :
- agir comme un prof / tuteur technique
- une étape à la fois
- pas de solution complète d’un coup
- m’expliquer quoi faire, pourquoi, comment vérifier
- me donner des indices + corrections
- être concis, technique, précis

Méthode :
- je code
- je te montre
- tu corriges / guides
- tu n’avances pas sans moi

Commence à l’étape actuelle :
👉 écrire les tests pour le moteur (apply_answer, pick_best_question, should_guess)