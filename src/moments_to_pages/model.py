from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass
class Observation:
    subjects: list[str] = field(default_factory=list)
    dominant_gesture: str = "still"
    quiet_regions: list[str] = field(default_factory=list)


@dataclass
class Interpretation:
    narrative_intent: str = "observation"
    emotional_tone: list[str] = field(default_factory=lambda: ["quiet"])
    confidence: float = 0.5
    method: str = "heuristic"


@dataclass
class Direction:
    story_role: str = "moment"
    director_note: str = "Preserve the observed scene and let sequencing carry the meaning."
    layout_emphasis: str = "photograph"


@dataclass
class SceneCard:
    source: str
    width: int
    height: int
    palette: list[str]
    brightness: float
    saturation: float
    orientation: str
    caption: str = "UNTITLED MOMENT"
    observation: Observation = field(default_factory=Observation)
    interpretation: Interpretation = field(default_factory=Interpretation)
    direction: Direction = field(default_factory=Direction)

    @property
    def story_role(self) -> str:
        return self.direction.story_role

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "SceneCard":
        value = dict(value)
        legacy_observation = {
            key: value.pop(key) for key in ("subjects", "dominant_gesture", "quiet_regions") if key in value
        }
        legacy_direction = {}
        if "story_role" in value:
            legacy_direction["story_role"] = value.pop("story_role")
        observation = value.get("observation", legacy_observation)
        direction = value.get("direction", legacy_direction)
        interpretation = value.get("interpretation", {})
        if isinstance(direction, dict):
            direction = dict(direction)
            for key in ("narrative_intent", "emotional_tone", "confidence"):
                if key in direction and key not in interpretation:
                    interpretation[key] = direction.pop(key)
        value["observation"] = observation if isinstance(observation, Observation) else Observation(**observation)
        value["interpretation"] = interpretation if isinstance(interpretation, Interpretation) else Interpretation(**interpretation)
        value["direction"] = direction if isinstance(direction, Direction) else Direction(**direction)
        return cls(**value)


def save_cards(cards: list[SceneCard], path: Path) -> None:
    path.write_text(json.dumps([card.to_dict() for card in cards], ensure_ascii=False, indent=2) + "\n")


def load_cards(path: Path) -> list[SceneCard]:
    return [SceneCard.from_dict(item) for item in json.loads(path.read_text())]
