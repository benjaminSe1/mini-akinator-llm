import json
from pathlib import Path

from mini_akinator.models import Character


def load_characters(data_dir: Path) -> list[Character]:
    characters: list[Character] = []

    for path in sorted(data_dir.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            payload = json.load(f)
            characters.append(Character.model_validate(payload))

    if not characters:
        raise ValueError(f"No character files found in {data_dir}")

    return characters
