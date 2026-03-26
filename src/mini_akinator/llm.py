import re
from typing import Protocol

from mini_akinator.engine import Question
from mini_akinator.models import AnswerValue, ParsedAnswer


class LLM(Protocol):
    def render_question(self, question: Question) -> str: ...
    def parse_answer(self, user_input: str) -> ParsedAnswer: ...


class BasicLLM(LLM):
    def render_question(self, question: Question) -> str:
        return question.label

    def parse_answer(self, user_input: str) -> ParsedAnswer:
        tokens = re.sub(r"[^\w\s]", "", user_input.lower().strip()).split()

        yes_inputs = {"yes", "y", "yeah"}
        no_inputs = {"no", "n"}
        unknown_inputs = {"unknown", "idk"}

        if any(token in yes_inputs for token in tokens):
            return ParsedAnswer(value=AnswerValue.YES, score=1.0)

        if any(token in no_inputs for token in tokens):
            return ParsedAnswer(value=AnswerValue.NO, score=1.0)

        if any(token in unknown_inputs for token in tokens):
            return ParsedAnswer(value=AnswerValue.UNKNOWN, score=1.0)

        return ParsedAnswer(value=AnswerValue.UNKNOWN, score=0.2)
