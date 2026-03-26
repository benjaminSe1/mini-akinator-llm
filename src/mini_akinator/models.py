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

    house: Literal["gryffindor", "slytherin", "ravenclaw", "hufflepuff", "none"]
    blood_status: Literal["pure-blood", "half-blood", "muggle-born", "unknown"]
    role: Literal["student", "teacher", "headmaster", "ministry", "other"]
    species: Literal["human", "half-giant", "ghost", "elf", "other"]
    alive: bool
    loyal_to_order: bool
    death_eater: bool
    has_wand: bool
    wears_glasses: bool
    hair_color: Literal["black", "brown", "blond", "red", "white", "other"]


class AnswerValue(StrEnum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class ParsedAnswer(BaseModel):
    value: AnswerValue
    score: float = Field(ge=0, le=1)
