from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class Character(BaseModel):
    name: str
    universe: str
    is_fictional: bool
    is_human: bool
    has_powers: bool
    wears_mask: bool
    is_villain: bool
    gender: Literal["male", "female", "other"]


class AnswerValue(StrEnum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class ParsedAnswer(BaseModel):
    value: AnswerValue
    score: float = Field(ge=0, le=1)
