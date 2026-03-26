from typing import Literal

from mini_akinator.engine import (
    GameState,
    apply_answer,
    pick_best_question,
    should_guess,
)
from mini_akinator.models import AnswerValue, Character


def make_character(
    *,
    name: str,
    is_fictional: bool,
    is_human: bool,
    has_powers: bool,
    wears_mask: bool,
    is_villain: bool,
    gender: Literal["male", "female", "other"] = "male",
) -> Character:
    return Character(
        name=name,
        universe="test",
        is_fictional=is_fictional,
        is_human=is_human,
        has_powers=has_powers,
        wears_mask=wears_mask,
        is_villain=is_villain,
        gender=gender,
    )


def make_state(candidates: list[Character], asked_keys: set[str] | None = None) -> GameState:
    return GameState(candidates=candidates, asked_keys=asked_keys or set())


def candidate_names(state: GameState) -> set[str]:
    return {character.name for character in state.candidates}


def test_apply_answer_yes_keeps_matching_candidates() -> None:
    candidates = [
        make_character(
            name="Harry",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="Batman",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=True,
            is_villain=False,
        ),
        make_character(
            name="Voldemort",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=True,
        ),
    ]
    state = make_state(candidates)

    new_state = apply_answer(state, "has_powers", AnswerValue.YES)

    assert candidate_names(new_state) == {"Harry", "Voldemort"}
    assert new_state.asked_keys == {"has_powers"}

    assert candidate_names(state) == {"Harry", "Batman", "Voldemort"}
    assert state.asked_keys == set()
    assert new_state is not state
    assert new_state.candidates is not state.candidates


def test_apply_answer_no_excludes_matching_candidates() -> None:
    candidates = [
        make_character(
            name="Harry",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="Batman",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=True,
            is_villain=False,
        ),
        make_character(
            name="Voldemort",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=True,
        ),
    ]
    state = make_state(candidates)

    new_state = apply_answer(state, "has_powers", AnswerValue.NO)

    assert candidate_names(new_state) == {"Batman"}
    assert new_state.asked_keys == {"has_powers"}

    assert candidate_names(state) == {"Harry", "Batman", "Voldemort"}
    assert state.asked_keys == set()
    assert new_state is not state
    assert new_state.candidates is not state.candidates


def test_apply_answer_unknown_keeps_candidates_unchanged_and_marks_question_as_asked() -> None:
    candidates = [
        make_character(
            name="Harry",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="Batman",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=True,
            is_villain=False,
        ),
    ]
    state = make_state(candidates, asked_keys={"is_human"})

    new_state = apply_answer(state, "has_powers", AnswerValue.UNKNOWN)

    assert candidate_names(new_state) == {"Harry", "Batman"}
    assert new_state.asked_keys == {"is_human", "has_powers"}

    assert candidate_names(state) == {"Harry", "Batman"}
    assert state.asked_keys == {"is_human"}
    assert new_state is not state
    assert new_state.candidates is not state.candidates


def test_should_guess_true_when_one_candidate_left() -> None:
    state = make_state(
        [
            make_character(
                name="Harry",
                is_fictional=True,
                is_human=True,
                has_powers=True,
                wears_mask=False,
                is_villain=False,
            )
        ]
    )

    assert should_guess(state) is True


def test_should_guess_true_when_two_candidates_left() -> None:
    state = make_state(
        [
            make_character(
                name="Harry",
                is_fictional=True,
                is_human=True,
                has_powers=True,
                wears_mask=False,
                is_villain=False,
            ),
            make_character(
                name="Batman",
                is_fictional=True,
                is_human=True,
                has_powers=False,
                wears_mask=True,
                is_villain=False,
            ),
        ]
    )

    assert should_guess(state) is True


def test_should_guess_false_when_more_than_two_candidates_left() -> None:
    state = make_state(
        [
            make_character(
                name="Harry",
                is_fictional=True,
                is_human=True,
                has_powers=True,
                wears_mask=False,
                is_villain=False,
            ),
            make_character(
                name="Batman",
                is_fictional=True,
                is_human=True,
                has_powers=False,
                wears_mask=True,
                is_villain=False,
            ),
            make_character(
                name="Voldemort",
                is_fictional=True,
                is_human=True,
                has_powers=True,
                wears_mask=False,
                is_villain=True,
            ),
        ]
    )

    assert should_guess(state) is False


def test_pick_best_question_prefers_most_balanced_split() -> None:
    candidates = [
        make_character(
            name="Harry",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="Voldemort",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=True,
        ),
        make_character(
            name="Batman",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=True,
            is_villain=False,
        ),
        make_character(
            name="Thanos",
            is_fictional=True,
            is_human=False,
            has_powers=False,
            wears_mask=False,
            is_villain=True,
        ),
    ]
    state = make_state(candidates)

    question = pick_best_question(state)

    assert question is not None
    assert question.key == "has_powers"


def test_pick_best_question_ignores_already_asked_questions() -> None:
    candidates = [
        make_character(
            name="Harry",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="Voldemort",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=True,
        ),
        make_character(
            name="Batman",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=True,
            is_villain=False,
        ),
        make_character(
            name="Thanos",
            is_fictional=True,
            is_human=False,
            has_powers=False,
            wears_mask=False,
            is_villain=True,
        ),
    ]
    state = make_state(candidates, asked_keys={"has_powers"})

    question = pick_best_question(state)

    assert question is not None
    assert question.key == "is_villain"


def test_pick_best_question_returns_none_when_no_question_can_split_candidates() -> None:
    candidates = [
        make_character(
            name="CloneA",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="CloneB",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=False,
            is_villain=False,
        ),
    ]
    state = make_state(candidates)

    question = pick_best_question(state)

    assert question is None


def test_pick_best_question_returns_none_when_all_questions_were_already_asked() -> None:
    candidates = [
        make_character(
            name="Harry",
            is_fictional=True,
            is_human=True,
            has_powers=True,
            wears_mask=False,
            is_villain=False,
        ),
        make_character(
            name="Batman",
            is_fictional=True,
            is_human=True,
            has_powers=False,
            wears_mask=True,
            is_villain=False,
        ),
    ]
    asked_keys = {
        "is_fictional",
        "is_human",
        "has_powers",
        "wears_mask",
        "is_villain",
    }
    state = make_state(candidates, asked_keys=asked_keys)

    question = pick_best_question(state)

    assert question is None


def test_apply_answer_keeps_asked_keys_unique() -> None:
    state = make_state(
        [
            make_character(
                name="Harry",
                is_fictional=True,
                is_human=True,
                has_powers=True,
                wears_mask=False,
                is_villain=False,
            )
        ],
        asked_keys={"has_powers"},
    )

    new_state = apply_answer(state, "has_powers", AnswerValue.YES)

    assert new_state.asked_keys == {"has_powers"}


def test_pick_best_question_returns_none_when_no_candidates() -> None:
    state = make_state([])

    question = pick_best_question(state)

    assert question is None
