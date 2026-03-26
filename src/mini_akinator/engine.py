from dataclasses import dataclass

from mini_akinator.models import AnswerValue, Character


@dataclass(frozen=True)
class Question:
    key: str
    label: str
    expected_value: object


@dataclass(frozen=True)
class GameState:
    candidates: list[Character]
    asked_keys: set[str]


QUESTION_BANK = [
    Question(key="gender", label="Est-ce un homme ?", expected_value="male"),
    Question(key="gender", label="Est-ce une femme ?", expected_value="female"),
    Question(
        key="has_powers", label="Est-ce que ce personnage a des pouvoirs ?", expected_value=True
    ),
    Question(key="is_villain", label="Est-ce un antagoniste / méchant ?", expected_value=True),
    Question(key="is_human", label="Est-ce un humain ?", expected_value=True),
    Question(
        key="alive",
        label="Est-ce que ce personnage est vivant à la fin de la saga ?",
        expected_value=True,
    ),
    Question(
        key="has_wand", label="Est-ce que ce personnage utilise une baguette ?", expected_value=True
    ),
    Question(
        key="wears_glasses",
        label="Est-ce que ce personnage porte des lunettes ?",
        expected_value=True,
    ),
    Question(
        key="wears_mask",
        label="Est-ce que ce personnage porte souvent un masque ?",
        expected_value=True,
    ),
    Question(
        key="loyal_to_order",
        label="Est-ce que ce personnage est lié à l’Ordre du Phénix ?",
        expected_value=True,
    ),
    Question(key="death_eater", label="Est-ce un Mangemort ?", expected_value=True),
    Question(key="house", label="Est-ce à Gryffondor ?", expected_value="gryffindor"),
    Question(key="house", label="Est-ce à Serpentard ?", expected_value="slytherin"),
    Question(key="house", label="Est-ce à Serdaigle ?", expected_value="ravenclaw"),
    Question(key="house", label="Est-ce à Poufsouffle ?", expected_value="hufflepuff"),
    Question(key="blood_status", label="Est-ce un sang-pur ?", expected_value="pure-blood"),
    Question(key="blood_status", label="Est-ce un sang-mêlé ?", expected_value="half-blood"),
    Question(key="blood_status", label="Est-ce un né-moldu ?", expected_value="muggle-born"),
    Question(key="role", label="Est-ce un élève ?", expected_value="student"),
    Question(key="role", label="Est-ce un professeur ?", expected_value="teacher"),
    Question(key="role", label="Est-ce le directeur de Poudlard ?", expected_value="headmaster"),
    Question(key="species", label="Est-ce un humain classique ?", expected_value="human"),
    Question(key="species", label="Est-ce un demi-géant ?", expected_value="half-giant"),
    Question(key="hair_color", label="A-t-il les cheveux noirs ?", expected_value="black"),
    Question(key="hair_color", label="A-t-il les cheveux roux ?", expected_value="red"),
    Question(key="hair_color", label="A-t-il les cheveux blonds ?", expected_value="blond"),
    Question(key="hair_color", label="A-t-il les cheveux blancs ?", expected_value="white"),
]


def pick_best_question(state: GameState) -> Question | None:
    best_question: Question | None = None
    best_score = float("inf")

    for question in QUESTION_BANK:
        question_id = f"{question.key}:{question.expected_value}"
        if question_id in state.asked_keys:
            continue

        yes_count = sum(matches_question(c, question) for c in state.candidates)
        no_count = len(state.candidates) - yes_count

        if yes_count == 0 or no_count == 0:
            continue

        score = abs(yes_count - no_count)
        if score < best_score:
            best_score = score
            best_question = question

    return best_question


def apply_answer(state: GameState, question: Question, answer: AnswerValue) -> GameState:
    question_id = f"{question.key}:{question.expected_value}"
    asked_keys = state.asked_keys | {question_id}

    if answer == AnswerValue.UNKNOWN:
        return GameState(candidates=state.candidates[:], asked_keys=asked_keys)

    if answer == AnswerValue.YES:
        filtered = [c for c in state.candidates if matches_question(c, question)]
    else:
        filtered = [c for c in state.candidates if not matches_question(c, question)]

    return GameState(candidates=filtered, asked_keys=asked_keys)


def should_guess(state: GameState) -> bool:
    return len(state.candidates) <= 1


def candidate_names(state: GameState) -> set[str]:
    return {character.name for character in state.candidates}


def matches_question(character: Character, question: Question) -> bool:
    return getattr(character, question.key) == question.expected_value
