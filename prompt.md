Je construis un projet Python : un mini Akinator hybride combinant un moteur logique déterministe et un LLM local.

Objectif :
Créer un jeu CLI capable de deviner un personnage via des questions oui/non, avec :
- un moteur logique qui filtre progressivement les candidats
- un LLM local (Ollama) utilisé uniquement pour interpréter les réponses utilisateur

Stack technique :
- Python 3.12+
- uv
- pytest, mypy, ruff
- pydantic
- Ollama (LLM local)
- structure en src/

Architecture actuelle :

Dataset :
- fichiers JSON (~15 personnages Harry Potter)
- attributs :
  - booléens (is_human, has_powers, etc.)
  - catégoriels (house, role, etc.)

Moteur logique (terminé, testé) :
- GameState :
  - candidats
  - questions déjà posées

- Question :
  - key
  - expected_value
  - label

- Fonctions :
  - pick_best_question → split optimal
  - apply_answer → filtre immuable
  - should_guess → stop si 1 candidat ou plus de question utile
  - candidate_names

- moteur 100% déterministe (aucune dépendance LLM)

LLM abstraction :

class LLM(Protocol):
    def render_question(self, question: Question) -> str
    def parse_answer(self, user_input: str) -> ParsedAnswer

Implémentations :

BasicLLM :
- rule-based
- match simple (yes, no, idk, etc.)
- score élevé si match exact
- fallback principal

OllamaLLM :
- wrapper autour d’un modèle local (ex: mistral)

render_question :
- désactivé (fallback direct)
- raison : hallucinations + modification du sens

parse_answer :
pipeline :
1. fallback BasicLLM
2. si score faible → appel Ollama
3. prompt strict → sortie attendue: yes / no / unknown
4. validation stricte
5. fallback si invalide

Contraintes importantes :
- moteur logique = déterministe
- le LLM ne doit jamais casser la logique
- validation stricte des sorties LLM
- fallback systématique

Problèmes rencontrés :
- hallucinations (ex: injection de personnages)
- modification du sens des questions
- dérive hors univers
- sorties LLM non conformes

État actuel :
- moteur stable + testé
- dataset enrichi
- boucle CLI fonctionnelle
- LLM intégré uniquement sur parse_answer
- architecture propre avec fallback

Prochaine étape :
- améliorer parse_answer :
  - prompt plus robuste
  - meilleure gestion des réponses ambiguës
  - score de confiance
  - enrichir le fallback rule-based

Objectif final :
Améliorer la compréhension des réponses utilisateur tout en gardant :
- fiabilité
- déterminisme du moteur
- architecture simple et testable

Je peux fournir :
- code actuel
- exemples d’inputs utilisateur
- outputs LLM
- tests existants