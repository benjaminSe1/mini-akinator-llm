from typing import Literal

from mini_akinator.engine import (
    GameState,
    Question,
    apply_answer,
    candidate_names,
    pick_best_question,
    should_guess,
)
from mini_akinator.models import AnswerValue, Character


def make_character(
    *,
    name: str,
    gender: Literal["male", "female", "other"] = "male",
    is_fictional: bool = True,
    is_human: bool = True,
    has_powers: bool = True,
    wears_mask: bool = False,
    is_villain: bool = False,
    house: Literal["gryffindor", "slytherin", "ravenclaw", "hufflepuff", "none"] = "none",
    blood_status: Literal["pure-blood", "half-blood", "muggle-born", "unknown"] = "unknown",
    role: Literal["student", "teacher", "headmaster", "ministry", "other"] = "other",
    species: Literal["human", "half-giant", "ghost", "elf", "other"] = "human",
    alive: bool = True,
    loyal_to_order: bool = False,
    death_eater: bool = False,
    has_wand: bool = True,
    wears_glasses: bool = False,
    hair_color: Literal["black", "brown", "blond", "red", "white", "other"] = "other",
) -> Character:
    return Character(
        name=name,
        universe="Harry Potter",
        is_fictional=is_fictional,
        is_human=is_human,
        has_powers=has_powers,
        wears_mask=wears_mask,
        is_villain=is_villain,
        gender=gender,
        house=house,
        blood_status=blood_status,
        role=role,
        species=species,
        alive=alive,
        loyal_to_order=loyal_to_order,
        death_eater=death_eater,
        has_wand=has_wand,
        wears_glasses=wears_glasses,
        hair_color=hair_color,
    )


def make_state(candidates: list[Character], asked_keys: set[str] | None = None) -> GameState:
    return GameState(candidates=candidates, asked_keys=asked_keys or set())


def qid(question: Question) -> str:
    return f"{question.key}:{question.expected_value}"


def test_apply_answer_yes_keeps_matching_candidates() -> None:
    question = Question(
        key="has_powers",
        label="A des pouvoirs ?",
        expected_value=True,
    )
    state = make_state(
        [
            make_character(name="Harry", has_powers=True),
            make_character(name="Batman", has_powers=False),
            make_character(name="Voldemort", has_powers=True),
        ]
    )

    new_state = apply_answer(state, question, AnswerValue.YES)

    assert candidate_names(new_state) == {"Harry", "Voldemort"}
    assert new_state.asked_keys == {qid(question)}

    assert candidate_names(state) == {"Harry", "Batman", "Voldemort"}
    assert state.asked_keys == set()
    assert new_state is not state
    assert new_state.candidates is not state.candidates


def test_apply_answer_no_excludes_matching_candidates() -> None:
    question = Question(
        key="has_powers",
        label="A des pouvoirs ?",
        expected_value=True,
    )
    state = make_state(
        [
            make_character(name="Harry", has_powers=True),
            make_character(name="Batman", has_powers=False),
            make_character(name="Voldemort", has_powers=True),
        ]
    )

    new_state = apply_answer(state, question, AnswerValue.NO)

    assert candidate_names(new_state) == {"Batman"}
    assert new_state.asked_keys == {qid(question)}


def test_apply_answer_unknown_keeps_candidates_unchanged_and_marks_question_as_asked() -> None:
    question = Question(
        key="has_powers",
        label="A des pouvoirs ?",
        expected_value=True,
    )
    state = make_state(
        [
            make_character(name="Harry", has_powers=True),
            make_character(name="Batman", has_powers=False),
        ],
        asked_keys={"gender:male"},
    )

    new_state = apply_answer(state, question, AnswerValue.UNKNOWN)

    assert candidate_names(new_state) == {"Harry", "Batman"}
    assert new_state.asked_keys == {"gender:male", qid(question)}

    assert candidate_names(state) == {"Harry", "Batman"}
    assert state.asked_keys == {"gender:male"}
    assert new_state is not state
    assert new_state.candidates is not state.candidates


def test_should_guess_true_when_one_candidate_left() -> None:
    state = make_state([make_character(name="Harry")])

    assert should_guess(state) is True


def test_should_guess_true_when_two_candidates_left() -> None:
    state = make_state(
        [
            make_character(name="Harry"),
            make_character(name="Hermione", gender="female"),
        ]
    )

    assert should_guess(state) is True


def test_should_guess_false_when_more_than_two_candidates_left() -> None:
    state = make_state(
        [
            make_character(name="Harry"),
            make_character(name="Hermione", gender="female"),
            make_character(name="Voldemort", is_villain=True),
        ]
    )

    assert should_guess(state) is False


def test_pick_best_question_prefers_most_balanced_split() -> None:
    state = make_state(
        [
            make_character(name="Harry", has_powers=True, is_villain=False),
            make_character(name="Voldemort", has_powers=True, is_villain=True),
            make_character(name="Batman", has_powers=False, is_villain=False),
            make_character(name="Thanos", has_powers=False, is_villain=True, is_human=False),
        ]
    )

    question = pick_best_question(state)

    assert question is not None
    assert question.key in {"has_powers", "is_villain"}


def test_pick_best_question_ignores_already_asked_questions() -> None:
    state = make_state(
        [
            make_character(name="Harry", has_powers=True, is_villain=False),
            make_character(name="Voldemort", has_powers=True, is_villain=True),
            make_character(name="Batman", has_powers=False, is_villain=False),
            make_character(name="Thanos", has_powers=False, is_villain=True, is_human=False),
        ],
        asked_keys={"has_powers:True"},
    )

    question = pick_best_question(state)

    assert question is not None
    assert qid(question) != "has_powers:True"


def test_pick_best_question_returns_none_when_no_question_can_split_candidates() -> None:
    state = make_state(
        [
            make_character(name="CloneA"),
            make_character(name="CloneB"),
        ]
    )

    question = pick_best_question(state)

    assert question is None


def test_pick_best_question_returns_none_when_no_candidates() -> None:
    state = make_state([])

    question = pick_best_question(state)

    assert question is None


def test_apply_answer_keeps_asked_keys_unique() -> None:
    question = Question(
        key="has_powers",
        label="A des pouvoirs ?",
        expected_value=True,
    )
    state = make_state(
        [make_character(name="Harry", has_powers=True)],
        asked_keys={qid(question)},
    )

    new_state = apply_answer(state, question, AnswerValue.YES)

    assert new_state.asked_keys == {qid(question)}
