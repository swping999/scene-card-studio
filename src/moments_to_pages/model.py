from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json
import re


ILLEGAL_XML_CONTROLS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
STORY_ROLES = {"moment", "opening", "development", "pause", "closing"}
ORIENTATIONS = {"portrait", "landscape", "square"}


def _validate_text(value: str, field_name: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    if ILLEGAL_XML_CONTROLS.search(value):
        raise ValueError(f"{field_name} contains an illegal control character")


def _validate_string_list(values: list[str], field_name: str) -> None:
    if not isinstance(values, list):
        raise ValueError(f"{field_name} must be a list")
    for index, value in enumerate(values):
        _validate_text(value, f"{field_name}[{index}]")


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
class TransformationPolicy:
    must_preserve: list[str] = field(default_factory=list)
    may_transform: list[str] = field(default_factory=list)
    must_remove: list[str] = field(default_factory=list)


@dataclass
class SourceMetadata:
    date: str = ""
    location: str = ""
    collection: str = ""
    catalogue_id: str = ""
    source_note: str = ""


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
    transformation: TransformationPolicy = field(default_factory=TransformationPolicy)
    metadata: SourceMetadata = field(default_factory=SourceMetadata)

    @property
    def story_role(self) -> str:
        return self.direction.story_role

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def validate(self) -> None:
        _validate_text(self.source, "source")
        if not self.source.strip():
            raise ValueError("source must not be empty")
        if not isinstance(self.width, int) or isinstance(self.width, bool) or self.width <= 0:
            raise ValueError("width must be a positive integer")
        if not isinstance(self.height, int) or isinstance(self.height, bool) or self.height <= 0:
            raise ValueError("height must be a positive integer")
        if self.orientation not in ORIENTATIONS:
            raise ValueError(f"orientation must be one of: {', '.join(sorted(ORIENTATIONS))}")
        for field_name, value in (("brightness", self.brightness), ("saturation", self.saturation)):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
                raise ValueError(f"{field_name} must be between 0 and 1")
        if not isinstance(self.palette, list):
            raise ValueError("palette must be a list")
        for color in self.palette:
            if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
                raise ValueError(f"Invalid palette color: {color!r}")
        _validate_text(self.caption, "caption")
        _validate_string_list(self.observation.subjects, "observation.subjects")
        _validate_text(self.observation.dominant_gesture, "observation.dominant_gesture")
        _validate_string_list(self.observation.quiet_regions, "observation.quiet_regions")
        _validate_text(self.interpretation.narrative_intent, "interpretation.narrative_intent")
        _validate_string_list(self.interpretation.emotional_tone, "interpretation.emotional_tone")
        if isinstance(self.interpretation.confidence, bool) or not isinstance(self.interpretation.confidence, (int, float)) or not 0 <= self.interpretation.confidence <= 1:
            raise ValueError("interpretation.confidence must be between 0 and 1")
        _validate_text(self.interpretation.method, "interpretation.method")
        if self.direction.story_role not in STORY_ROLES:
            raise ValueError(f"direction.story_role must be one of: {', '.join(sorted(STORY_ROLES))}")
        _validate_text(self.direction.director_note, "direction.director_note")
        _validate_text(self.direction.layout_emphasis, "direction.layout_emphasis")
        _validate_string_list(self.transformation.must_preserve, "transformation.must_preserve")
        _validate_string_list(self.transformation.may_transform, "transformation.may_transform")
        _validate_string_list(self.transformation.must_remove, "transformation.must_remove")
        for field_name in ("date", "location", "collection", "catalogue_id", "source_note"):
            _validate_text(getattr(self.metadata, field_name), f"metadata.{field_name}")
        groups = {
            "must_preserve": {value.casefold() for value in self.transformation.must_preserve},
            "may_transform": {value.casefold() for value in self.transformation.may_transform},
            "must_remove": {value.casefold() for value in self.transformation.must_remove},
        }
        for left, right in (("must_preserve", "may_transform"), ("must_preserve", "must_remove"), ("may_transform", "must_remove")):
            overlap = groups[left] & groups[right]
            if overlap:
                raise ValueError(f"transformation.{left} and transformation.{right} overlap: {', '.join(sorted(overlap))}")

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
        transformation = value.get("transformation", {})
        metadata = value.get("metadata", {})
        if isinstance(direction, dict):
            direction = dict(direction)
            for key in ("narrative_intent", "emotional_tone", "confidence"):
                if key in direction:
                    legacy_value = direction.pop(key)
                    if key not in interpretation:
                        interpretation[key] = legacy_value
        value["observation"] = observation if isinstance(observation, Observation) else Observation(**observation)
        value["interpretation"] = interpretation if isinstance(interpretation, Interpretation) else Interpretation(**interpretation)
        value["direction"] = direction if isinstance(direction, Direction) else Direction(**direction)
        value["transformation"] = transformation if isinstance(transformation, TransformationPolicy) else TransformationPolicy(**transformation)
        value["metadata"] = metadata if isinstance(metadata, SourceMetadata) else SourceMetadata(**metadata)
        card = cls(**value)
        card.validate()
        return card


def save_cards(cards: list[SceneCard], path: Path) -> None:
    for card in cards:
        card.validate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([card.to_dict() for card in cards], ensure_ascii=False, indent=2) + "\n")


def load_cards(path: Path, resolve_sources: bool = True) -> list[SceneCard]:
    cards = [SceneCard.from_dict(item) for item in json.loads(path.read_text())]
    if resolve_sources:
        base = path.resolve().parent
        for card in cards:
            source = Path(card.source).expanduser()
            if not source.is_absolute():
                card.source = str((base / source).resolve())
    return cards
