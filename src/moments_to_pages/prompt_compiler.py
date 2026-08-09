from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from .expression_profiles import expression_profile_names, resolve_expression_profile
from .model import SceneCard


COMPILER_VERSION = "0.3.1"
SUPPORTED_SYSTEMS = (
    "cinematic-storyboard",
    "minimal-editorial",
    "memory-atlas",
    "family-archive",
)


@dataclass(frozen=True)
class PromptBlocks:
    subject_fidelity: list[str]
    transformation_policy: list[str]
    narrative_intent: list[str]
    composition: list[str]
    lighting: list[str]
    material: list[str]
    spatial_relationships: list[str]
    text_strategy: list[str]
    exclusions: list[str]
    output: list[str]

    def render(self) -> str:
        labels = {
            "subject_fidelity": "SUBJECT FIDELITY",
            "transformation_policy": "TRANSFORMATION POLICY",
            "narrative_intent": "NARRATIVE INTENT",
            "composition": "COMPOSITION",
            "lighting": "LIGHTING AND COLOR",
            "material": "MATERIAL AND SURFACE",
            "spatial_relationships": "SPATIAL RELATIONSHIPS",
            "text_strategy": "TEXT AND LABELS",
            "exclusions": "EXCLUSIONS",
            "output": "OUTPUT",
        }
        sections = []
        for name, label in labels.items():
            values = getattr(self, name)
            sections.append(label + "\n" + "\n".join(f"- {value}" for value in values))
        return "\n\n".join(sections)


REVIEW_POLICY: dict[str, Any] = {
    "scale": "1-5",
    "accept_threshold": 4,
    "hard_gates": ["subject_fidelity", "artifact_control"],
    "dimensions": {
        "subject_fidelity": "Recognizable people, objects, architecture, action, and identity-bearing details remain faithful to the source.",
        "narrative_alignment": "The image expresses the Scene Card intent, emotional tone, story role, and director note.",
        "composition": "The frame has a clear hierarchy, intentional depth, crop safety, and no accidental dead zones.",
        "system_distinctiveness": "The result uses the selected Narrative System's mechanism and chosen expression profile rather than a generic beauty treatment.",
        "artifact_control": "No distorted anatomy, broken geometry, invented metadata, unwanted text, collage seams, or synthetic clutter.",
    },
    "sequence_dimensions": {
        "subject_continuity": "Recurring people, clothing, objects, locations, and identity-bearing details remain consistent across frames.",
        "light_color_continuity": "Light direction, exposure progression, and palette form a coherent sequence rather than unrelated grades.",
        "rhythm": "Shot scale, density, and pauses create intentional pacing without repetitive framing.",
        "narrative_arc": "Opening, development, pause, and closing roles read as one arc without invented events.",
    },
}


def _joined(values: list[str], fallback: str) -> str:
    cleaned = [value.strip() for value in values if value.strip()]
    return ", ".join(cleaned) if cleaned else fallback


def _aspect_ratio(card: SceneCard, requested: str) -> str:
    if requested != "source":
        return requested
    if card.orientation == "portrait":
        return "2:3"
    if card.orientation == "square":
        return "1:1"
    return "3:2"


def _source_record(source: str, source_root: Path | None) -> dict[str, str]:
    path = Path(source).expanduser()
    resolved = path if path.is_absolute() else (source_root / path if source_root else path)
    if not resolved.exists():
        raise FileNotFoundError(f"Referenced file does not exist: {resolved}")
    if not resolved.is_file():
        raise ValueError(f"Referenced path is not a file: {resolved}")
    return {"path": source, "sha256": sha256(resolved.read_bytes()).hexdigest()}


def _policy_values(card: SceneCard) -> tuple[list[str], list[str], list[str]]:
    remove = list(card.transformation.must_remove)
    transform = list(card.transformation.may_transform)
    excluded = {value.casefold() for value in remove + transform}
    preserve = list(card.transformation.must_preserve)
    if not preserve:
        preserve = [value for value in card.observation.subjects if value.casefold() not in excluded]
    return preserve, transform, remove


def _transformation_lines(card: SceneCard, label: str | None = None) -> list[str]:
    preserve, transform, remove = _policy_values(card)
    prefix = f"{label}: " if label else ""
    return [
        f"{prefix}MUST PRESERVE — {_joined(preserve, 'the primary visible subject and identity-bearing details')}.",
        f"{prefix}MAY TRANSFORM — {_joined(transform, 'crop, exposure, and presentation only')}.",
        f"{prefix}MUST REMOVE — {_joined(remove, 'nothing not explicitly authorized')}.",
    ]


def _base_fidelity(card: SceneCard) -> list[str]:
    preserve, _, _ = _policy_values(card)
    gesture = card.observation.dominant_gesture or "the visible action and pose"
    return [
        f"Preserve the recognizable identity, count, proportions, position, and defining details of: {_joined(preserve, 'the primary visible subject')}.",
        f"Preserve the observed action or structural gesture: {gesture}.",
        "Treat the source photograph as visual evidence: do not replace the location, reconstruct hidden content, or invent people, objects, or events.",
    ]


def _base_narrative(card: SceneCard) -> list[str]:
    return [
        f"Narrative intent: {card.interpretation.narrative_intent}.",
        f"Emotional tone: {_joined(card.interpretation.emotional_tone, 'quiet')}. Story role: {card.story_role}.",
        f"Director note: {card.direction.director_note}",
        f"Visual emphasis: {card.direction.layout_emphasis}.",
    ]


def _sequence_context(cards: list[SceneCard]) -> str:
    beats = [
        f"{index + 1:02d} {card.story_role}: {card.interpretation.narrative_intent}; tone {_joined(card.interpretation.emotional_tone, 'quiet')}"
        for index, card in enumerate(cards)
    ]
    return " | ".join(beats)


def _multi_card_context(cards: list[SceneCard]) -> list[str]:
    lines = []
    for index, card in enumerate(cards):
        lines.append(
            f"Frame {index + 1:02d} / {card.story_role}: intent {card.interpretation.narrative_intent}; "
            f"tone {_joined(card.interpretation.emotional_tone, 'quiet')}; emphasis {card.direction.layout_emphasis}; "
            f"director note {card.direction.director_note}"
        )
    return lines


def _cinematic_blocks(
    card: SceneCard,
    aspect_ratio: str,
    profile: dict[str, Any],
    sequence_context: str,
) -> PromptBlocks:
    palette = _joined(card.palette[:4], "source-derived colors")
    return PromptBlocks(
        subject_fidelity=_base_fidelity(card),
        transformation_policy=_transformation_lines(card),
        narrative_intent=_base_narrative(card),
        composition=[
            f"Create one continuous cinematic photograph with {card.direction.layout_emphasis} as the visual anchor; no panels or montage.",
            "Suppress only elements listed under MUST REMOVE; keep the place believable and lived-in.",
            *profile["composition"],
        ],
        lighting=[
            f"Build from the source palette ({palette}) and keep exposure physically plausible.",
            *profile["lighting"],
        ],
        material=[*profile["material"], "Prefer believable atmospheric depth and tactile surfaces over glossy advertising polish."],
        spatial_relationships=[
            "Keep subject scale plausible and preserve the source scene's directional movement.",
            f"Sequence contract shared with the other frames: {sequence_context}.",
            "Maintain recurring identity, light direction, color progression, and shot rhythm across the sequence.",
        ],
        text_strategy=["Generate no titles, subtitles, credits, dialogue, logos, watermarks, or visible typography."],
        exclusions=[
            "No commercial movie poster, trailer key art, split screen, contact sheet, or multi-shot composite.",
            "No cyberpunk neon, bloom overload, plastic skin, beauty retouching, or fake anamorphic flares unless explicitly authorized.",
            "Do not imitate a named director, cinematographer, photographer, film, or franchise.",
        ],
        output=[f"Return one standalone photorealistic frame at {aspect_ratio}.", "Keep the source subject immediately recognizable at first glance."],
    )


def _minimal_blocks(card: SceneCard, aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    palette = _joined(card.palette[:4], "source-derived colors")
    quiet = _joined(card.observation.quiet_regions, "the cleanest available background")
    return PromptBlocks(
        subject_fidelity=_base_fidelity(card),
        transformation_policy=_transformation_lines(card),
        narrative_intent=_base_narrative(card),
        composition=[
            "Create one continuous editorial art photograph devoted to the source subject; no designed page or collage.",
            f"Use {quiet} as breathing room and remove only elements listed under MUST REMOVE.",
            *profile["composition"],
        ],
        lighting=[f"Keep color source-led ({palette}) and separate the subject through tonal structure rather than saturation effects.", *profile["lighting"]],
        material=[*profile["material"], "Avoid sterile CGI perfection and preserve identity-bearing imperfections."],
        spatial_relationships=[
            "Give the object enough negative space to feel intentional while retaining believable physical support and gravity.",
            "Use source-supported shadow, edge, fold, or repetition as geometry; do not paste abstract shapes over the photograph.",
        ],
        text_strategy=["Generate no masthead, caption, label, logo, watermark, border, or visible typography."],
        exclusions=[
            "No magazine mockup, product advertisement, catalog cutout, multi-object collage, panel, or split screen.",
            "No generic luxury styling, ornamental props, excessive smoothing, floating objects, or unauthorized abstract overlays.",
        ],
        output=[f"Return one standalone photorealistic editorial still life at {aspect_ratio}.", "Make the result specific to the supplied object and Scene Card."],
    )


def _memory_atlas_blocks(cards: list[SceneCard], aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    subjects = [_joined(_policy_values(card)[0], Path(card.source).stem) for card in cards]
    palette = _joined([color for card in cards for color in card.palette[:2]], "source-derived colors")
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve each supplied place or subject as a recognizable photographic anchor: {'; '.join(subjects)}.",
            "Keep identity-bearing architecture, horizon, entrances, objects, people, and spatial details faithful to each source.",
            "Do not invent destinations, geographic facts, events, or a return that is absent from the Scene Cards.",
        ],
        transformation_policy=[line for index, card in enumerate(cards) for line in _transformation_lines(card, f"Frame {index + 1:02d}")],
        narrative_intent=[
            "Connect the supplied places as remembered spatial experience rather than literal navigation.",
            *_multi_card_context(cards),
        ],
        composition=[
            "Follow the supplied source order and story roles; do not force a departure–return arc.",
            "Avoid a row of equal photo cards; use spatial hierarchy to express the relationships stated in the Scene Cards.",
            *profile["composition"],
        ],
        lighting=[f"Use the combined source palette ({palette}) without recoloring every photograph identically.", *profile["lighting"]],
        material=[*profile["material"], "Every non-photographic mark must perform a Scene Card-supported spatial function rather than decoration."],
        spatial_relationships=[
            "Connect frames through their stated gestures, roles, quiet regions, and layout emphasis.",
            "Use scale changes only to express Scene Card-supported distance or memory, not assumed cartographic accuracy.",
        ],
        text_strategy=["Use no invented place names, dates, coordinates, map pins, interface labels, or route instructions."],
        exclusions=[
            "No generic UI map, flowchart, scrapbook grid, postcard collage, or equal photo panels.",
            "No fantasy architecture, generic tourism poster, or named-artist imitation.",
        ],
        output=[f"Return one integrated spatial-memory artifact at {aspect_ratio}.", "Every supplied place or subject must remain recognizable."],
    )


def _family_archive_blocks(cards: list[SceneCard], aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    subjects = [_joined(_policy_values(card)[0], Path(card.source).stem) for card in cards]
    gestures = [_joined([card.observation.dominant_gesture], "a visible gesture") for card in cards]
    palette = _joined([color for card in cards for color in card.palette[:2]], "source-derived colors")
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve the supplied documentary subjects and visible actions: {'; '.join(subjects)}.",
            f"Keep faces, hands, clothing, body proportions, object handling, and gestures faithful: {'; '.join(gestures)}.",
            "Do not beautify, de-age, restage, invent kinship, or label the subjects as fictional unless the user supplied that fact.",
        ],
        transformation_policy=[line for index, card in enumerate(cards) for line in _transformation_lines(card, f"Frame {index + 1:02d}")],
        narrative_intent=[
            "Build archival meaning only from the supplied Scene Card interpretations; do not assume care, inheritance, continuity, or family relationships.",
            *_multi_card_context(cards),
        ],
        composition=[
            "Use story roles and layout emphasis to vary scale; keep important faces, hands, and actions uncropped.",
            *profile["composition"],
        ],
        lighting=[f"Use the combined source palette ({palette}) without applying a generic nostalgic filter.", *profile["lighting"]],
        material=[*profile["material"], "Every added archive material must refer to a supplied object, surface, or repeated gesture."],
        spatial_relationships=[
            "Bridge only relationships stated in the Scene Cards; use partial overlaps and breathing room instead of stacked decoration.",
            "Keep documentary subjects visually primary and expression-profile materials secondary.",
        ],
        text_strategy=["Generate no invented names, dates, kinship labels, handwriting, captions, stamps, logos, or watermarks."],
        exclusions=[
            "No greeting card, family-tree diagram, scrapbook kit, equal photo grid, sentimental stock-photo glow, or fake antique filter.",
            "No distorted hands or faces, decorative clutter, fabricated documents, or named-artist imitation.",
        ],
        output=[f"Return one integrated documentary archive artifact at {aspect_ratio}.", "Subjects and gestures must remain photographic, natural, and immediately recognizable."],
    )


def compile_manifest(
    cards: list[SceneCard],
    system: str,
    *,
    aspect_ratio: str = "source",
    expression_profile: str = "source-led",
    source_root: Path | None = None,
    story_path: str | None = None,
    reference_outputs: list[str] | None = None,
) -> dict[str, Any]:
    if system not in SUPPORTED_SYSTEMS:
        raise ValueError(f"Unsupported prompt system: {system}")
    if not cards:
        raise ValueError("At least one Scene Card is required")
    for card in cards:
        card.validate()
    profile = resolve_expression_profile(system, expression_profile)
    references = reference_outputs or []
    if system in {"cinematic-storyboard", "minimal-editorial"} and len(references) not in {0, len(cards)}:
        raise ValueError(f"{system} requires either zero reference outputs or one per Scene Card")
    if system in {"memory-atlas", "family-archive"} and len(references) > 1:
        raise ValueError(f"{system} accepts at most one reference output")
    prompts: list[dict[str, Any]] = []
    sequence_context = _sequence_context(cards)

    if system in {"cinematic-storyboard", "minimal-editorial"}:
        for index, card in enumerate(cards):
            ratio = _aspect_ratio(card, aspect_ratio)
            blocks = (
                _cinematic_blocks(card, ratio, profile, sequence_context)
                if system == "cinematic-storyboard"
                else _minimal_blocks(card, ratio, profile)
            )
            item: dict[str, Any] = {
                "id": f"{system}-{index + 1:02d}",
                "mode": "single-frame",
                "source_indexes": [index],
                "sources": [_source_record(card.source, source_root)],
                "blocks": asdict(blocks),
                "compiled_prompt": blocks.render(),
            }
            if references:
                item["reference_output"] = _source_record(references[index], source_root)
            prompts.append(item)
    else:
        ratio = aspect_ratio if aspect_ratio != "source" else "4:5"
        blocks = (
            _memory_atlas_blocks(cards, ratio, profile)
            if system == "memory-atlas"
            else _family_archive_blocks(cards, ratio, profile)
        )
        item = {
            "id": f"{system}-01",
            "mode": "spatial-synthesis" if system == "memory-atlas" else "archival-synthesis",
            "source_indexes": list(range(len(cards))),
            "sources": [_source_record(card.source, source_root) for card in cards],
            "blocks": asdict(blocks),
            "compiled_prompt": blocks.render(),
        }
        if references:
            item["reference_output"] = _source_record(references[0], source_root)
        prompts.append(item)

    upload_files = [record for prompt in prompts for record in prompt["sources"]]
    manifest: dict[str, Any] = {
        "schema_version": "1.1",
        "compiler_version": COMPILER_VERSION,
        "system": system,
        "expression_profile": profile["name"],
        "available_expression_profiles": list(expression_profile_names(system)),
        "story": story_path,
        "source_base": "story-directory",
        "prompts": prompts,
        "review_policy": REVIEW_POLICY,
        "privacy": {
            "upload_requires_explicit_consent": True,
            "consent_status": "not-recorded",
            "provider": None,
            "purpose": "presentation synthesis",
            "files": upload_files,
        },
    }
    if system == "cinematic-storyboard" and len(cards) > 1:
        manifest["sequence_context"] = sequence_context
    return manifest
