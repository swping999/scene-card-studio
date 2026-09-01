from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from math import ceil, gcd
from pathlib import Path
from typing import Any

from .expression_profiles import expression_profile_names, resolve_expression_profile
from .model import SceneCard
from .narrative_systems import SUPPORTED_SYSTEMS, resolve_narrative_system
from .presentation import build_presentation_contract
from .readiness import assess_direction_readiness

COMPILER_VERSION = "0.6.1"
__all__ = ["SUPPORTED_SYSTEMS", "compile_manifest"]


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


def _output_contract(aspect_ratio: str) -> dict[str, Any]:
    try:
        left, right = (int(value) for value in aspect_ratio.split(":", 1))
    except (ValueError, AttributeError) as exc:
        raise ValueError("aspect ratio must use positive integer W:H notation") from exc
    if left <= 0 or right <= 0:
        raise ValueError("aspect ratio values must be positive")
    divisor = gcd(left, right)
    left //= divisor
    right //= divisor
    short_ratio = right if left >= right else left
    scale = ceil(1024 / short_ratio)
    width = left * scale
    height = right * scale
    return {
        "mime_type": "image/png",
        "width": width,
        "height": height,
        "aspect_ratio": f"{left}:{right}",
    }


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


def _profile_subject_lines(profile: dict[str, Any]) -> list[str]:
    return list(profile.get("subject_fidelity", []))


def _profile_policy_lines(profile: dict[str, Any]) -> list[str]:
    return list(profile.get("transformation_policy", []))


def _profile_exclusions(profile: dict[str, Any]) -> list[str]:
    return list(profile.get("exclusions", []))


def _profile_output(profile: dict[str, Any]) -> list[str]:
    return list(profile.get("output", []))


def _render_medium(profile: dict[str, Any]) -> str:
    if profile.get("output_medium"):
        return str(profile["output_medium"])
    mode = profile.get("render_mode")
    if mode == "full-redraw":
        return "fully painted"
    if mode == "identity-locked-surrealism":
        return "materially coherent surreal"
    if mode == "heritage-photograph":
        return "heritage photographic"
    return "photographic"


def _sequence_context(cards: list[SceneCard]) -> str:
    beats = [
        f"{index + 1:02d} {card.story_role}: {card.interpretation.narrative_intent}; tone {_joined(card.interpretation.emotional_tone, 'quiet')}"
        for index, card in enumerate(cards)
    ]
    return " | ".join(beats)


def _source_mode(cards: list[SceneCard], prompt_mode: str) -> str:
    if len(cards) == 1:
        return "single-photo"
    return "multi-photo-per-source" if prompt_mode == "per-source" else "multi-photo-synthesis"


def _multi_card_context(cards: list[SceneCard]) -> list[str]:
    lines = []
    for index, card in enumerate(cards):
        label = "Source" if len(cards) == 1 else f"Frame {index + 1:02d}"
        lines.append(
            f"{label} / {card.story_role}: intent {card.interpretation.narrative_intent}; "
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
    sequence_lines = ([
        f"Sequence contract shared with the other frames: {sequence_context}.",
        "Maintain recurring identity, light direction, color progression, and shot rhythm across the sequence.",
    ] if sequence_context else [
        "Single-photo contract: treat this source as one complete directed frame; do not imply adjacent shots or invented events.",
    ])
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
            *sequence_lines,
        ],
        text_strategy=["Generate no titles, subtitles, credits, dialogue, logos, watermarks, or visible typography."],
        exclusions=[
            "No commercial movie poster, trailer key art, split screen, contact sheet, or multi-shot composite.",
            "No cyberpunk neon, bloom overload, plastic skin, beauty retouching, or fake anamorphic flares unless explicitly authorized.",
            "Do not imitate a named director, cinematographer, photographer, film, or franchise.",
        ],
        output=[f"Return one standalone photorealistic PNG frame at exactly {aspect_ratio}.", "Keep the source subject immediately recognizable at first glance."],
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
        output=[f"Return one standalone photorealistic PNG editorial still life at exactly {aspect_ratio}.", "Make the result specific to the supplied object and Scene Card."],
    )


def _memory_atlas_blocks(cards: list[SceneCard], aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    single = len(cards) == 1
    subjects = [_joined(_policy_values(card)[0], Path(card.source).stem) for card in cards]
    palette = _joined([color for card in cards for color in card.palette[:2]], "source-derived colors")
    full_redraw = profile.get("render_mode") == "full-redraw"
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve the supplied place or subject as one recognizable {'painted' if full_redraw else 'photographic'} anchor: {subjects[0]}." if single else f"Preserve each supplied place or subject as a recognizable {'painted' if full_redraw else 'photographic'} anchor: {'; '.join(subjects)}.",
            "Keep identity-bearing architecture, horizon, entrances, objects, people, and spatial details faithful to the source." if single else "Keep identity-bearing architecture, horizon, entrances, objects, people, and spatial details faithful to each source.",
            "Do not invent destinations, geographic facts, events, or a return that is absent from the Scene Cards.",
            *profile.get("subject_fidelity", []),
        ],
        transformation_policy=[
            *[line for index, card in enumerate(cards) for line in _transformation_lines(card, None if single else f"Frame {index + 1:02d}")],
            *profile.get("transformation_policy", []),
        ],
        narrative_intent=[
            "Treat the supplied place as one self-contained spatial memory; do not invent another location or a journey." if single else "Connect the supplied places as remembered spatial experience rather than literal navigation.",
            *_multi_card_context(cards),
        ],
        composition=[
            "Build one continuous image from this source and its Scene Card; do not add panels, a route, or a departure–return arc." if single else "Follow the supplied source order and story roles; do not force a departure–return arc.",
            "Use spatial hierarchy inside the single scene without inventing off-frame geography." if single else "Avoid a row of equal photo cards; use spatial hierarchy to express the relationships stated in the Scene Cards.",
            *profile["composition"],
        ],
        lighting=[
            f"Use the combined source palette ({palette}) without flattening every {'painted passage' if full_redraw else 'photograph'} into one identical color treatment.",
            *profile["lighting"],
        ],
        material=[
            *profile["material"],
            "Every added mark must perform a Scene Card-supported spatial function rather than decoration."
            if full_redraw
            else "Every non-photographic mark must perform a Scene Card-supported spatial function rather than decoration.",
        ],
        spatial_relationships=[
            "Use the source's visible direction, quiet regions, and layout emphasis as the complete spatial relationship." if single else "Connect frames through their stated gestures, roles, quiet regions, and layout emphasis.",
            "Use scale changes only to express Scene Card-supported distance or memory, not assumed cartographic accuracy.",
        ],
        text_strategy=["Use no invented place names, dates, coordinates, map pins, interface labels, or route instructions."],
        exclusions=[
            "No generic UI map, flowchart, scrapbook grid, postcard collage, or equal photo panels.",
            "No fantasy architecture, generic tourism poster, or named-artist imitation.",
            *profile.get("exclusions", []),
        ],
        output=[
            f"Return one integrated PNG spatial-memory artifact at exactly {aspect_ratio}.",
            "The supplied place or subject must remain recognizable." if single else "Every supplied place or subject must remain recognizable.",
            *profile.get("output", []),
        ],
    )


def _family_archive_blocks(cards: list[SceneCard], aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    single = len(cards) == 1
    subjects = [_joined(_policy_values(card)[0], Path(card.source).stem) for card in cards]
    gestures = [_joined([card.observation.dominant_gesture], "a visible gesture") for card in cards]
    palette = _joined([color for card in cards for color in card.palette[:2]], "source-derived colors")
    full_redraw = profile.get("render_mode") == "full-redraw"
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve the supplied documentary subject and visible action: {subjects[0]}." if single else f"Preserve the supplied documentary subjects and visible actions: {'; '.join(subjects)}.",
            f"Keep face, hands, clothing, body proportions, object handling, and gesture faithful: {gestures[0]}." if single else f"Keep faces, hands, clothing, body proportions, object handling, and gestures faithful: {'; '.join(gestures)}.",
            "Do not beautify, de-age, restage, invent kinship, or label the subjects as fictional unless the user supplied that fact.",
            *_profile_subject_lines(profile),
        ],
        transformation_policy=[
            *[line for index, card in enumerate(cards) for line in _transformation_lines(card, None if single else f"Frame {index + 1:02d}")],
            *_profile_policy_lines(profile),
        ],
        narrative_intent=[
            "Build one self-contained archival portrait or record only from the supplied Scene Card; do not assume care, inheritance, continuity, or family relationships." if single else "Build archival meaning only from the supplied Scene Card interpretations; do not assume care, inheritance, continuity, or family relationships.",
            *_multi_card_context(cards),
        ],
        composition=[
            "Use this Scene Card's layout emphasis to direct one complete image; keep important face, hands, and action uncropped." if single else "Use story roles and layout emphasis to vary scale; keep important faces, hands, and actions uncropped.",
            *profile["composition"],
        ],
        lighting=[f"Use the combined source palette ({palette}) without applying a generic nostalgic filter.", *profile["lighting"]],
        material=[*profile["material"], "Every added archive material must refer to a supplied object, surface, or repeated gesture."],
        spatial_relationships=[
            "Use only relationships visible or stated within this Scene Card; do not invent relatives, companion images, or archival layers." if single else "Bridge only relationships stated in the Scene Cards; use partial overlaps and breathing room instead of stacked decoration.",
            "Keep documentary subjects visually primary and expression-profile materials secondary.",
        ],
        text_strategy=["Generate no invented names, dates, kinship labels, handwriting, captions, stamps, logos, or watermarks."],
        exclusions=[
            "No greeting card, family-tree diagram, scrapbook kit, equal photo grid, sentimental stock-photo glow, or fake antique filter.",
            "No distorted hands or faces, decorative clutter, fabricated documents, or named-artist imitation.",
            *_profile_exclusions(profile),
        ],
        output=[
            f"Return one integrated PNG documentary archive artifact at exactly {aspect_ratio}.",
            "Subjects and gestures must remain natural and immediately recognizable; render them as painted rather than photographic only when the selected profile explicitly requires full redraw."
            if full_redraw
            else "Subjects and gestures must remain photographic, natural, and immediately recognizable.",
            *_profile_output(profile),
        ],
    )


def _single_extended_blocks(
    card: SceneCard,
    aspect_ratio: str,
    profile: dict[str, Any],
    sequence_context: str,
    system: str,
) -> PromptBlocks:
    palette = _joined(card.palette[:4], "source-derived colors")
    quiet = _joined(card.observation.quiet_regions, "the least distracting source region")
    templates: dict[str, dict[str, list[str]]] = {
        "editorial-sequence": {
            "narrative": ["Let sequencing, scale, pause, and contrast carry the reading; do not invent an event between frames."],
            "composition": ["Create one standalone continuous image for this beat, not a designed page, border, or multi-photo collage."],
            "spatial": ["Use the Scene Card role and layout emphasis to make this frame distinct while preserving continuity with adjacent beats."],
            "exclusions": ["No equal-grid montage, fake magazine page, generic moodboard, ornamental typography, or unrelated props."],
        },
        "field-log": {
            "narrative": ["Treat observed subjects, gesture, material condition, and environment as field evidence; interpretation must remain visibly secondary."],
            "composition": ["Keep context around the subject and make the observed gesture legible without staging or cinematic exaggeration."],
            "spatial": ["Retain source scale cues, physical support, and environmental relationships so the record remains inspectable."],
            "exclusions": ["No dramatized reenactment, hero lighting, false scientific labels, specimen fiction, or beautification."],
        },
        "museum-catalogue": {
            "narrative": ["Present the supplied subject as an inspectable catalogue plate; do not claim provenance, period, maker, value, or collection history absent from metadata."],
            "composition": ["Create one clean continuous plate with controlled margins inside the image and a complete, uncropped view of identity-bearing details."],
            "spatial": ["Preserve scale cues, support, joins, repairs, wear, and material relief; use a neutral ground only when it does not alter evidence."],
            "exclusions": ["No fake museum room, pedestal spectacle, auction luxury styling, invented accession label, certificate, frame, or wall text."],
        },
        "street-reportage": {
            "narrative": ["Make the supplied observed event and its context readable as one reportage beat; do not fabricate urgency, conflict, or chronology."],
            "composition": ["Prioritize the decisive visible gesture while retaining enough street context to understand where bodies and objects stand."],
            "spatial": ["Preserve crowd count, body position, gaze, signage geometry, vehicle placement, and the source event's directional movement."],
            "exclusions": ["No staged crisis, poverty aesthetic, voyeuristic crop, crushed faces, fake press caption, or sensational news treatment."],
        },
        "fashion-editorial": {
            "narrative": ["Use pose, garment construction, movement, and shot-scale contrast to create an editorial beat without inventing a brand campaign."],
            "composition": ["Use assertive full-bleed framing and intentional crop tension while keeping face, hands, joints, and garment construction anatomically credible."],
            "spatial": ["Preserve the relationship between body, clothing, accessories, floor, furniture, and location; vary shot scale across the sequence."],
            "exclusions": ["No fake brand, logo, masthead, product claim, impossible garment seams, beauty-filter skin, extra fingers, or celebrity imitation."],
        },
    }
    template = templates[system]
    sequence_systems = {"editorial-sequence", "street-reportage", "fashion-editorial"}
    if sequence_context and system in sequence_systems:
        sequence_line = [f"Sequence contract shared with the other frames: {sequence_context}."]
    elif system in sequence_systems:
        sequence_line = [
            "Single-photo contract: make this source a complete standalone image and do not imply adjacent frames."
        ]
    else:
        sequence_line = []
    narrative = list(template["narrative"])
    spatial = list(template["spatial"])
    if not sequence_context and system == "editorial-sequence":
        narrative = ["Let scale, pause, and contrast carry this standalone image; do not imply events outside it."]
        spatial = ["Use the Scene Card role and layout emphasis to complete this frame without implying adjacent beats."]
    elif not sequence_context and system == "fashion-editorial":
        narrative = [
            "Use pose, garment construction, movement, and crop tension to create one editorial image without inventing a brand campaign."
        ]
        spatial = [
            "Preserve the relationship between body, clothing, accessories, floor, furniture, and location inside this one frame."
        ]
    return PromptBlocks(
        subject_fidelity=[*_base_fidelity(card), *_profile_subject_lines(profile)],
        transformation_policy=[*_transformation_lines(card), *_profile_policy_lines(profile)],
        narrative_intent=[*_base_narrative(card), *narrative],
        composition=[
            *template["composition"],
            f"Use {quiet} as controlled breathing room where compatible with the observed scene.",
            *profile["composition"],
        ],
        lighting=[f"Build from the source palette ({palette}) and preserve truthful skin, object, and environment relationships.", *profile["lighting"]],
        material=[*profile["material"], "Keep identity-bearing surface evidence specific; avoid a generic preset finish."],
        spatial_relationships=[*spatial, *sequence_line],
        text_strategy=[
            "Generate no visible typography, captions, dates, locations, catalogue numbers, logos, watermarks, or interface labels inside the image.",
            "Reserve all supplied metadata for the deterministic presentation layer defined by presentation_contract.",
        ],
        exclusions=[*template["exclusions"], "Do not imitate a named artist, photographer, publication, brand, or campaign.", *_profile_exclusions(profile)],
        output=[
            f"Return one standalone {_render_medium(profile)} PNG frame at exactly {aspect_ratio}.",
            "Keep the supplied subject immediately recognizable and leave typography to the deterministic renderer.",
            *_profile_output(profile),
        ],
    )


def _travel_journal_blocks(cards: list[SceneCard], aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    single = len(cards) == 1
    subjects = [_joined(_policy_values(card)[0], Path(card.source).stem) for card in cards]
    palette = _joined([color for card in cards for color in card.palette[:2]], "source-derived colors")
    full_redraw = profile.get("render_mode") == "full-redraw"
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve the supplied person, place, object, or threshold as one recognizable {'painted' if full_redraw else 'photographic'} journey anchor: {subjects[0]}."
            if single
            else f"Preserve every supplied person, place, object, and threshold as a recognizable {'painted' if full_redraw else 'photographic'} journey anchor: {'; '.join(subjects)}.",
            "Keep faces, architecture, roads, horizons, vehicles, luggage, tickets, and identity-bearing details faithful to the source."
            if single
            else "Keep faces, architecture, roads, horizons, vehicles, luggage, tickets, and identity-bearing details faithful to their sources.",
            *_profile_subject_lines(profile),
        ],
        transformation_policy=[
            *[
                line
                for index, card in enumerate(cards)
                for line in _transformation_lines(card, None if single else f"Frame {index + 1:02d}")
            ],
            *_profile_policy_lines(profile),
        ],
        narrative_intent=[
            "Treat this source as one self-contained journey moment; do not invent movement, a second stop, destination, return, date, or route."
            if single
            else "Build a journey from supplied movement, pauses, thresholds, and Scene Card roles; do not invent a destination, return, date, or route.",
            *_multi_card_context(cards),
        ],
        composition=[
            "Build one complete image from the source and Scene Card; do not add a postcard grid, itinerary, route, or app map."
            if single
            else "Use varied scale and spatial adjacency to connect the journey; avoid an equal postcard grid or literal app map.",
            "Treat tickets, maps, receipts, and handwriting as usable evidence only when they were supplied or explicitly authorized.",
            *profile["composition"],
        ],
        lighting=[f"Use the combined source palette ({palette}) while retaining distinct weather and time-of-day evidence.", *profile["lighting"]],
        material=[*profile["material"], "Every paper, route, or travel mark must correspond to supplied evidence rather than decorative tourism motifs."],
        spatial_relationships=[
            "Use the source's visible direction, threshold, quiet regions, and layout emphasis without implying an unseen route."
            if single
            else "Follow source order and story roles unless the user explicitly approves reordering.",
            "Keep all spatial claims inside this source; do not invent geography beyond the frame."
            if single
            else "Connect places through visible direction, repeated objects, thresholds, and supplied metadata rather than invented geography.",
        ],
        text_strategy=[
            "Generate no dates, place names, coordinates, tickets, stamps, handwriting, captions, or route labels inside the image.",
            "Place only user-supplied metadata later through the deterministic presentation_contract.",
        ],
        exclusions=[
            "No generic scrapbook kit, tourism poster, passport-stamp collage, airline branding, app map, pins, arrows, or fabricated ephemera.",
            "No named-artist or named-travel-publication imitation.",
            *_profile_exclusions(profile),
        ],
        output=[
            f"Return one integrated {_render_medium(profile)} PNG journey artifact at exactly {aspect_ratio}.",
            "The supplied source must remain a recognizable narrative anchor."
            if single
            else "Every supplied source must contribute a recognizable narrative anchor.",
            *_profile_output(profile),
        ],
    )


def _journey_taxonomy_blocks(cards: list[SceneCard], aspect_ratio: str, profile: dict[str, Any]) -> PromptBlocks:
    single = len(cards) == 1
    subjects = [_joined(_policy_values(card)[0], Path(card.source).stem) for card in cards]
    gestures = [_joined([card.observation.dominant_gesture], "no movement stated") for card in cards]
    quiet_regions = [_joined(card.observation.quiet_regions, "no quiet region stated") for card in cards]
    palette = _joined([color for card in cards for color in card.palette[:2]], "source-derived colors")
    full_redraw = profile.get("render_mode") == "full-redraw"
    evidence_lines = [
        f"Source {index + 1:02d}: visible anchors {subjects[index]}; observed gesture {gestures[index]}; quiet region {quiet_regions[index]}."
        for index in range(len(cards))
    ]
    return PromptBlocks(
        subject_fidelity=[
            f"Preserve the supplied place and all identity-bearing anchors as recognizable {'rendered' if full_redraw else 'photographic'} evidence: {'; '.join(subjects)}.",
            "Keep people, animals, architecture, terrain contours, plants, vehicles, weather, and objects faithful wherever they are actually visible; omit categories absent from the sources.",
            "Do not substitute generic icons, a different landscape, an invented species, or an imagined destination for observed evidence.",
            *_profile_subject_lines(profile),
        ],
        transformation_policy=[
            *[
                line
                for index, card in enumerate(cards)
                for line in _transformation_lines(card, None if single else f"Source {index + 1:02d}")
            ],
            *_profile_policy_lines(profile),
        ],
        narrative_intent=[
            "Read the supplied journey image as a visual taxonomy of one place: distinguish the dominant place anchor from supporting terrain, weather, living subjects, objects, materials, and movement evidence only when those categories are visible.",
            "The mechanism is semantic classification, not decoration: every secondary study must explain what makes this particular place recognizable.",
            *evidence_lines,
            *_multi_card_context(cards),
        ],
        composition=[
            "Create one integrated full-frame image in which visible semantic roles are differentiated inside the original perspective: movement may become a directional print rhythm, landmark a precise structural anchor, water a translucent tonal field, vegetation a tactile painted mass, weather a broad atmospheric wash, and material evidence a close-grained surface passage.",
            "Treat those examples as roles, not mandatory decoration: assign a distinct but compatible visual register only to categories supported by the Scene Cards, and make every register interlock at real scene boundaries.",
            "Organize categories through scale, depth, edge behavior, and shared ground along one clear visual path; do not create subordinate panels, equal cards, a top-and-bottom duplicate, a vertical sticker column, or a repeated source inset.",
            "Let the Scene Card layout emphasis choose the dominant anchor; use only categories that have at least one visible source-backed element.",
            *profile["composition"],
        ],
        lighting=[
            f"Use the source palette ({palette}) and one coherent light model across the dominant scene and every subordinate study.",
            *profile["lighting"],
        ],
        material=[
            *profile["material"],
            "Material transitions must occur at source-backed boundaries, clarify semantic role and depth, and remain part of one continuous place; they may not become detachable stickers, unrelated swatches, or a photographic image with decorative overlays.",
        ],
        spatial_relationships=[
            "Retain source foreground-to-distance order, movement direction, and landmark relationships in the dominant view.",
            "Make classification legible through adjacent material transitions and shared contours inside the place itself, never through connector lines, pins, arrows, detached studies, or labels.",
            "Keep every relationship inside this one source; do not imply an unseen route or companion image."
            if single
            else "Preserve source order unless the Scene Cards explicitly authorize reordering; do not invent a route between unrelated places.",
        ],
        text_strategy=[
            "Generate no captions, category names, coordinates, dates, map labels, handwriting, logos, watermarks, or interface text inside the image.",
            "Apply user-supplied metadata later through the deterministic presentation_contract.",
        ],
        exclusions=[
            "No blue scrapbook board, white sticker outlines, repeated top-and-bottom photo, thumbnail strip, vertical decal stack, boxed grid, specimen UI, or copied caption placement.",
            "No generic travel poster, fabricated souvenirs, fake tickets, invented map, decorative arrows, or named-artist, named-studio, named-publication, or reference-image imitation.",
            *_profile_exclusions(profile),
        ],
        output=[
            f"Return one integrated {_render_medium(profile)} PNG Journey Taxonomy artifact at exactly {aspect_ratio}.",
            "At first glance it must read as one beautiful directed place image; at second glance its visible taxonomy must become legible without text.",
            *_profile_output(profile),
        ],
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
    spec = resolve_narrative_system(system)
    if not cards:
        raise ValueError("At least one Scene Card is required")
    for card in cards:
        card.validate()
    profile = resolve_expression_profile(system, expression_profile)
    references = reference_outputs or []
    if spec["prompt_mode"] == "per-source" and len(references) not in {0, len(cards)}:
        raise ValueError(f"{system} requires either zero reference outputs or one per Scene Card")
    if spec["prompt_mode"] == "synthesis" and len(references) > 1:
        raise ValueError(f"{system} accepts at most one reference output")
    prompts: list[dict[str, Any]] = []
    sequence_context = _sequence_context(cards) if len(cards) > 1 else ""
    source_mode = _source_mode(cards, spec["prompt_mode"])

    if spec["prompt_mode"] == "per-source":
        for index, card in enumerate(cards):
            ratio = _aspect_ratio(card, aspect_ratio)
            if system == "cinematic-storyboard":
                blocks = _cinematic_blocks(card, ratio, profile, sequence_context)
            elif system == "minimal-editorial":
                blocks = _minimal_blocks(card, ratio, profile)
            else:
                blocks = _single_extended_blocks(card, ratio, profile, sequence_context, system)
            item: dict[str, Any] = {
                "id": f"{system}-{index + 1:02d}",
                "mode": spec["artifact_mode"],
                "source_indexes": [index],
                "sources": [_source_record(card.source, source_root)],
                "output_contract": _output_contract(ratio),
                "blocks": asdict(blocks),
                "compiled_prompt": blocks.render(),
            }
            if references:
                item["reference_output"] = _source_record(references[index], source_root)
            prompts.append(item)
    else:
        ratio = (
            _aspect_ratio(cards[0], aspect_ratio)
            if len(cards) == 1
            else (aspect_ratio if aspect_ratio != "source" else "4:5")
        )
        if system == "memory-atlas":
            blocks = _memory_atlas_blocks(cards, ratio, profile)
        elif system == "family-archive":
            blocks = _family_archive_blocks(cards, ratio, profile)
        elif system == "journey-taxonomy":
            blocks = _journey_taxonomy_blocks(cards, ratio, profile)
        else:
            blocks = _travel_journal_blocks(cards, ratio, profile)
        item = {
            "id": f"{system}-01",
            "mode": spec["artifact_mode"],
            "source_indexes": list(range(len(cards))),
            "sources": [_source_record(card.source, source_root) for card in cards],
            "output_contract": _output_contract(ratio),
            "blocks": asdict(blocks),
            "compiled_prompt": blocks.render(),
        }
        if references:
            item["reference_output"] = _source_record(references[0], source_root)
        prompts.append(item)

    upload_files = [record for prompt in prompts for record in prompt["sources"]]
    direction_readiness = assess_direction_readiness(cards)
    sequence_review_required = system in {
        "cinematic-storyboard", "editorial-sequence", "street-reportage", "fashion-editorial"
    } and len(cards) > 1
    manifest: dict[str, Any] = {
        "schema_version": "1.5",
        "compiler_version": COMPILER_VERSION,
        "source_mode": source_mode,
        "system": system,
        "system_display_name": spec["display_name"],
        "expression_profile": profile["name"],
        "available_expression_profiles": list(expression_profile_names(system)),
        "story": story_path,
        "source_base": "story-directory",
        "prompts": prompts,
        "direction_readiness": direction_readiness,
        "generation_ready": direction_readiness["generation_ready"],
        "presentation_contract": build_presentation_contract(cards, system, [prompt["id"] for prompt in prompts]),
        "review_policy": REVIEW_POLICY,
        "sequence_review_required": sequence_review_required,
        "privacy": {
            "upload_requires_explicit_consent": True,
            "consent_status": "not-recorded",
            "provider": None,
            "purpose": "presentation synthesis",
            "files": upload_files,
        },
    }
    if profile.get("alias_for"):
        manifest["expression_profile_alias_for"] = profile["alias_for"]
    if sequence_review_required:
        manifest["sequence_context"] = sequence_context
    return manifest
