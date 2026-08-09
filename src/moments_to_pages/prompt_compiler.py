from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from .model import SceneCard


COMPILER_VERSION = "0.3.0"
SUPPORTED_SYSTEMS = (
    "cinematic-storyboard",
    "minimal-editorial",
    "memory-atlas",
    "family-archive",
)


@dataclass(frozen=True)
class PromptBlocks:
    subject_fidelity: list[str]
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
        "system_distinctiveness": "The result uses the selected Narrative System's mechanism rather than a generic beauty treatment.",
        "artifact_control": "No distorted anatomy, broken geometry, invented metadata, unwanted text, collage seams, or synthetic clutter.",
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
    record = {"path": source}
    if resolved.exists() and resolved.is_file():
        record["sha256"] = sha256(resolved.read_bytes()).hexdigest()
    return record


def _base_fidelity(card: SceneCard) -> list[str]:
    subjects = _joined(card.observation.subjects, "the visible source subjects")
    gesture = card.observation.dominant_gesture or "the visible action and pose"
    return [
        f"Preserve the recognizable identity, count, proportions, position, and defining details of: {subjects}.",
        f"Preserve the observed action or structural gesture: {gesture}.",
        "Treat the source photograph as visual evidence: do not replace the location, redesign the subject, reconstruct hidden content, or invent people.",
    ]


def _base_narrative(card: SceneCard) -> list[str]:
    tone = _joined(card.interpretation.emotional_tone, "quiet")
    return [
        f"Narrative intent: {card.interpretation.narrative_intent}.",
        f"Emotional tone: {tone}. Story role: {card.story_role}.",
        f"Director note: {card.direction.director_note}",
    ]


def _cinematic_blocks(card: SceneCard, aspect_ratio: str) -> PromptBlocks:
    palette = _joined(card.palette[:4], "source-derived colors")
    emphasis = card.direction.layout_emphasis or "the primary subject"
    return PromptBlocks(
        subject_fidelity=_base_fidelity(card),
        narrative_intent=_base_narrative(card),
        composition=[
            f"Create one continuous cinematic photograph with {emphasis} as the visual anchor; no panels or montage.",
            "Use a natural 35–50 mm observational perspective, deliberate crop, and a legible foreground–midground–background relationship.",
            "Suppress accidental clutter through framing, depth, and shadow while keeping the place believable and lived-in.",
        ],
        lighting=[
            "Use motivated practical light with one coherent direction; shape the subject rather than bathing the whole frame evenly.",
            f"Build a restrained color grade from the source palette ({palette}); allow controlled warm–cool contrast without turning the scene neon.",
            "Protect highlight detail, retain dimensional blacks, and use reflections or weather only when supported by the source.",
        ],
        material=[
            "Keep skin, glass, pavement, fabric, vehicles, and architecture photorealistic with restrained fine film grain.",
            "Prefer believable atmospheric depth and tactile surfaces over glossy advertising polish.",
        ],
        spatial_relationships=[
            "Keep subject scale plausible and preserve the source scene's directional movement.",
            "Let negative space and off-center placement create tension; do not center everything by default.",
        ],
        text_strategy=["Generate no titles, subtitles, credits, dialogue, logos, watermarks, or visible typography."],
        exclusions=[
            "No commercial movie poster, trailer key art, split screen, contact sheet, or multi-shot composite.",
            "No excessive teal-and-orange grade, cyberpunk neon, bloom overload, plastic skin, beauty retouching, or fake anamorphic flares.",
            "Do not imitate a named director, cinematographer, photographer, film, or franchise.",
        ],
        output=[f"Return one standalone photorealistic frame at {aspect_ratio}.", "Keep the source subject immediately recognizable at first glance."],
    )


def _minimal_blocks(card: SceneCard, aspect_ratio: str) -> PromptBlocks:
    palette = _joined(card.palette[:4], "source-derived neutral colors")
    quiet = _joined(card.observation.quiet_regions, "the cleanest available background")
    return PromptBlocks(
        subject_fidelity=_base_fidelity(card),
        narrative_intent=_base_narrative(card),
        composition=[
            "Create one continuous editorial art photograph devoted to the single source subject; no designed page or collage.",
            f"Use {quiet} as breathing room and build one decisive hierarchy through scale, asymmetry, and crop.",
            "Remove only accidental clutter that does not define the subject; do not add decorative props to signal luxury.",
        ],
        lighting=[
            "Use one believable window or soft directional source with a clear shadow structure and gentle tonal falloff.",
            f"Keep color restrained and source-led ({palette}); separate the subject from the ground through tone, not saturation effects.",
        ],
        material=[
            "Preserve wear, fibers, glaze, scratches, dents, and other identity-bearing material evidence.",
            "Make tactile surface and small imperfections visually important; avoid sterile CGI perfection.",
        ],
        spatial_relationships=[
            "Give the object enough negative space to feel intentional but retain a believable physical surface and gravity.",
            "Use shadow, edge, fold, or repetition as the dominant geometry; do not paste abstract shapes over the photograph.",
        ],
        text_strategy=["Generate no masthead, caption, label, logo, watermark, border, or visible typography."],
        exclusions=[
            "No magazine mockup, product advertisement, catalog cutout, multi-object collage, panel, or split screen.",
            "No generic beige luxury styling, ornamental props, excessive smoothing, floating objects, or abstract overlays.",
        ],
        output=[f"Return one standalone photorealistic editorial still life at {aspect_ratio}.", "The result should feel quiet, materially rich, and specific to this object."],
    )


def _memory_atlas_blocks(cards: list[SceneCard], aspect_ratio: str) -> PromptBlocks:
    subjects = [_joined(card.observation.subjects, Path(card.source).stem) for card in cards]
    intents = [_joined([card.interpretation.narrative_intent], "spatial memory") for card in cards]
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve each photographed place as a recognizable photographic anchor: {'; '.join(subjects)}.",
            "Keep architecture, landmarks, horizon, entrances, and identity-bearing spatial details faithful to their source photographs.",
            "Do not redraw the buildings as generic illustrations and do not invent destinations or geographic facts.",
        ],
        narrative_intent=[f"Connect the places as remembered experience rather than a literal navigation map: {' → '.join(intents)}."],
        composition=[
            "Build one coherent travel/space memory field in which real photographic architecture is embedded into drawn geography.",
            "Create a clear spatial rhythm from departure through distance to return; avoid a row of equal photo cards.",
        ],
        lighting=[
            "Preserve plausible light within each photographic fragment and unify the whole artifact with restrained paper warmth.",
            "Use watercolor terrain and graphite contours to bridge tonal differences without recoloring every photograph identically.",
        ],
        material=[
            "Combine photographic buildings with watercolor terrain, pencil contour marks, torn archival paper, faint coastline or topographic texture, and subtle travel ephemera.",
            "Keep paper seams and drawn marks tactile and irregular; they must carry spatial memory rather than decoration.",
        ],
        spatial_relationships=[
            "Let drawn terrain flow behind and between the photographed places; overlap edges selectively so photography and drawing inhabit one geography.",
            "Use scale changes to suggest remembered distance, not literal cartographic accuracy.",
        ],
        text_strategy=["Use no invented place names, dates, coordinates, map pins, interface labels, or route instructions."],
        exclusions=[
            "No arrows, dotted route lines, flowchart connectors, UI map, scrapbook grid, postcard collage, or equal photo panels.",
            "No fantasy architecture, generic tourism poster, glossy 3D terrain, or named-artist imitation.",
        ],
        output=[f"Return one integrated photographic-and-hand-drawn spatial memory artifact at {aspect_ratio}.", "Actual architecture must remain photographic and recognizable."],
    )


def _family_archive_blocks(cards: list[SceneCard], aspect_ratio: str) -> PromptBlocks:
    people = [_joined(card.observation.subjects, Path(card.source).stem) for card in cards]
    gestures = [_joined([card.observation.dominant_gesture], "a visible domestic gesture") for card in cards]
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve the fictional documentary subjects and their visible actions: {'; '.join(people)}.",
            f"Keep faces, hands, clothing, body proportions, object handling, and gestures faithful: {'; '.join(gestures)}.",
            "Do not beautify, de-age, restage, or invent family identities and relationships.",
        ],
        narrative_intent=[
            "Read repeated domestic gestures as care, inheritance, and continuity without turning them into sentimental advertising.",
            "Let ordinary work and retained objects carry the emotional meaning.",
        ],
        composition=[
            "Create one coherent archival record with a strong central documentary rhythm, not a tidy equal-cell collage.",
            "Vary scale and edge treatment according to story role; keep important faces and hands uncropped.",
        ],
        lighting=[
            "Preserve natural documentary light and modest tonal differences between sources.",
            "Use warm paper and graphite as a unifying ground without applying a generic sepia filter to the people.",
        ],
        material=[
            "Integrate photographic people with graphite object studies, tracing paper, contact-print edges, fabric fibers, thread, photo corners, and restrained archival wear.",
            "Every non-photographic mark should refer to a supplied object, gesture, or repeated material.",
        ],
        spatial_relationships=[
            "Let archival materials bridge repeated gestures across time; use partial overlaps and breathing room instead of stacked decoration.",
            "Keep photographic subjects visually primary and drawn object studies secondary.",
        ],
        text_strategy=["Generate no invented names, dates, kinship labels, handwriting, captions, stamps, logos, or watermarks."],
        exclusions=[
            "No greeting card, family-tree diagram, scrapbook kit, equal photo grid, sentimental stock-photo glow, or fake antique filter.",
            "No distorted hands or faces, decorative clutter, fabricated documents, or named-artist imitation.",
        ],
        output=[f"Return one integrated documentary-and-archival artifact at {aspect_ratio}.", "People and gestures must remain photographic, natural, and immediately recognizable."],
    )


def compile_manifest(
    cards: list[SceneCard],
    system: str,
    *,
    aspect_ratio: str = "source",
    source_root: Path | None = None,
    story_path: str | None = None,
    reference_outputs: list[str] | None = None,
) -> dict[str, Any]:
    if system not in SUPPORTED_SYSTEMS:
        raise ValueError(f"Unsupported prompt system: {system}")
    if not cards:
        raise ValueError("At least one Scene Card is required")
    references = reference_outputs or []
    prompts: list[dict[str, Any]] = []

    if system in {"cinematic-storyboard", "minimal-editorial"}:
        for index, card in enumerate(cards):
            ratio = _aspect_ratio(card, aspect_ratio)
            blocks = _cinematic_blocks(card, ratio) if system == "cinematic-storyboard" else _minimal_blocks(card, ratio)
            item: dict[str, Any] = {
                "id": f"{system}-{index + 1:02d}",
                "mode": "single-frame",
                "source_indexes": [index],
                "sources": [_source_record(card.source, source_root)],
                "blocks": asdict(blocks),
                "compiled_prompt": blocks.render(),
            }
            if index < len(references):
                item["reference_output"] = _source_record(references[index], source_root)
            prompts.append(item)
    else:
        ratio = aspect_ratio if aspect_ratio != "source" else "4:5"
        blocks = _memory_atlas_blocks(cards, ratio) if system == "memory-atlas" else _family_archive_blocks(cards, ratio)
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

    return {
        "schema_version": "1.0",
        "compiler_version": COMPILER_VERSION,
        "system": system,
        "story": story_path,
        "source_base": "story-directory",
        "prompts": prompts,
        "review_policy": REVIEW_POLICY,
    }
