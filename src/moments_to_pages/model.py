from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass
class SceneCard:
    source: str
    width: int
    height: int
    palette: list[str]
    brightness: float
    saturation: float
    orientation: str
    story_role: str = "moment"
    caption: str = "UNTITLED MOMENT"
    subjects: list[str] = field(default_factory=list)
    dominant_gesture: str = "still"
    quiet_regions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "SceneCard":
        return cls(**value)


def save_cards(cards: list[SceneCard], path: Path) -> None:
    path.write_text(json.dumps([card.to_dict() for card in cards], ensure_ascii=False, indent=2) + "\n")


def load_cards(path: Path) -> list[SceneCard]:
    return [SceneCard.from_dict(item) for item in json.loads(path.read_text())]
