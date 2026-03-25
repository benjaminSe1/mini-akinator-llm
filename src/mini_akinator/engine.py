from dataclasses import dataclass

from mini_akinator.models import AnswerValue, Character


@dataclass
class Question:
    key: str
    label: str


@dataclass
class GameState:
    candidates: list[Character]
    asked_keys: set[str]


QUESTION_BANK = [
    Question(key="is_fictional", label="Est-ce un personnage fictif ?"),
    Question(key="is_human", label="Est-ce un humain ?"),
    Question(key="has_powers", label="Est-ce que ce personnage a des pouvoirs ?"),
    Question(key="wears_mask", label="Est-ce que ce personnage porte souvent un masque ?"),
    Question(key="is_villain", label="Est-ce un antagoniste / méchant ?"),
]


def pick_best_question(state: GameState) -> Question | None:
    best_question: Question | None = None
    best_score = float("inf")
    for question in QUESTION_BANK:
        if question.key in state.asked_keys:
            continue

        yes_count = sum(bool(getattr(c, question.key)) for c in state.candidates)
        no_count = len(state.candidates) - yes_count

        if yes_count == 0 or no_count == 0:
            continue

        score = abs(yes_count - no_count)
        if score < best_score:
            best_score = score
            best_question = question

    return best_question


def apply_answer(state: GameState, key: str, answer: AnswerValue) -> GameState:
    asked_keys = state.asked_keys | {key}

    if answer == AnswerValue.UNKNOWN:
        return GameState(candidates=state.candidates[:], asked_keys=asked_keys)

    expected = answer == AnswerValue.YES
    filtered = [c for c in state.candidates if bool(getattr(c, key)) is expected]

    return GameState(candidates=filtered, asked_keys=asked_keys)


def should_guess(state: GameState) -> bool:
    return len(state.candidates) <= 2
