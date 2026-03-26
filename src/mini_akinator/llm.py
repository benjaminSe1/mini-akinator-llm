import re
from typing import Protocol

import ollama

from mini_akinator.engine import Question
from mini_akinator.models import AnswerValue, ParsedAnswer


class LLM(Protocol):
    def render_question(self, question: Question) -> str: ...
    def parse_answer(self, user_input: str) -> ParsedAnswer: ...


class OllamaLLM(LLM):
    def __init__(self, model_name: str = "llama3"):
        self.fallback: LLM = BasicLLM()
        self.model_name = model_name

    def render_question(self, question: Question) -> str:
        return self.fallback.render_question(question=question)

    def parse_answer(self, user_input: str) -> ParsedAnswer:
        answer = self.fallback.parse_answer(user_input=user_input)
        if answer.score > 0.2:
            return answer

        prompt = (
            "Interpret this answer and reply with exactly one word: "
            "yes, no, or unknown.\n"
            f"{user_input}"
        )

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            rendered = response.response.strip().lower()
            print(f"with ollama '{rendered}'")

            if rendered in {"yes", "no", "unknown"}:
                return ParsedAnswer(value=AnswerValue(rendered), score=1.0)
            else:
                raise ValueError("Value given by ollama is not valid")

        except Exception:
            pass

        print("with Basic")
        return self.fallback.parse_answer(user_input=user_input)


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
