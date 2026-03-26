from pathlib import Path

from mini_akinator.engine import (
    GameState,
    apply_answer,
    candidate_names,
    pick_best_question,
    should_guess,
)
from mini_akinator.llm import OllamaLLM
from mini_akinator.repository import load_characters


def play_game() -> None:
    game_state = GameState(
        candidates=load_characters(Path("data/characters")),
        asked_keys=set(),
    )
    llm = OllamaLLM()

    while not should_guess(state=game_state):
        question = pick_best_question(state=game_state)
        if question is None:
            break

        user_input = input(f"{llm.render_question(question)}> ")
        answer = llm.parse_answer(user_input=user_input)
        game_state = apply_answer(state=game_state, question=question, answer=answer.value)

        print(f"Parsed answer: {answer.value} (score={answer.score:.2f})")
        print(f"Remaining candidates: {len(game_state.candidates)}")

    if len(game_state.candidates) == 0:
        print("No candidate found.")
        return

    if len(game_state.candidates) == 1:
        print(f"The answer is: {game_state.candidates[0].name}")
        return

    print("We cannot determine the answer. Possible candidates:")
    for name in sorted(candidate_names(game_state)):
        print(f"- {name}")
