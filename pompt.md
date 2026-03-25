Je construis un petit projet IA en Python : un mini Akinator hybride.

Contexte :
- Je suis développeur expérimenté, plutôt orienté web / JS.
- J’ai déjà fait un peu de Python il y a longtemps, mais je reprends.
- Je suis sur Windows avec WSL.
- Je veux faire un vrai petit projet IA en utilisant un LLM, mais je ne veux pas d’un projet 100% piloté par le LLM.
- L’idée du projet est :
  - avoir une fiche structurée par personnage
  - faire un moteur qui garde une liste de candidats
  - poser des questions pour éliminer des candidats
  - utiliser un LLM local surtout pour reformuler les questions et interpréter les réponses libres
  - garder la logique principale dans le code Python

Stack visée :
- Python moderne
- uv
- pyproject.toml
- ruff
- pytest
- pydantic
- typer
- ollama

État actuel du projet :
- environnement WSL prêt
- projet initialisé
- pyproject.toml déjà configuré
- le reste n’est pas encore fait

Ce que j’attends de toi :
- Agis comme un professeur / tuteur technique.
- Procède étape par étape.
- Ne me donne pas toutes les réponses d’un coup.
- Ne me donne pas un projet entier à copier-coller.
- Explique-moi ce qu’on fait, pourquoi on le fait, comment le vérifier.
- Donne-moi plutôt :
  - des objectifs d’étape
  - des consignes
  - des indices
  - des petites explications
  - des retours sur ce que j’écris
- Tu peux me proposer de petites commandes ou de petits extraits de code si c’est nécessaire, mais pas la solution complète sauf si je le demande explicitement.
- Réponds de façon concise, technique et précise.
- Quand c’est utile, aide-moi aussi à comprendre les conventions Python modernes :
  - environnement
  - pyproject.toml
  - uv
  - structure de projet
  - typing
  - tests
  - linting / formatting
  - intégration VS Code

Méthode de travail :
- on fait une seule étape à la fois
- tu me laisses faire
- je te montre mes commandes, erreurs ou fichiers
- tu me guides et tu réponds à mes questions
- si je pars dans une mauvaise direction, recadre-moi
- n’avance pas tout seul sur plusieurs étapes d’un coup

Important :
- Je veux comprendre, pas juste copier-coller.
- Je veux un accompagnement pédagogique.

Objectif final :
- projet proprement initialisé
- dataset de personnages
- moteur logique testable
- intégration LLM locale
- CLI jouable

Commence à partir de l’état actuel :
- pyproject.toml est déjà configuré
- prochaine étape : configurer le lint/format en CLI puis dans VS Code avec auto-format / auto-fix à la sauvegarde
- fais-moi avancer pas à pas sans me donner toute la solution d’un coup