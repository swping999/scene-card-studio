from __future__ import annotations

from typing import Any


EXPRESSION_PROFILES: dict[str, dict[str, dict[str, list[str]]]] = {
    "cinematic-storyboard": {
        "source-led": {
            "composition": ["Respect the source camera position and derive shot scale from the visible scene rather than forcing a lens signature."],
            "lighting": ["Develop only light sources already visible or physically plausible in the source."],
            "material": ["Keep photographic surfaces natural and use only restrained source-compatible grain or atmosphere."],
        },
        "rain-nocturne": {
            "composition": ["Use a natural 35–50 mm observational perspective with legible foreground, midground, and background."],
            "lighting": ["Shape the frame with motivated mixed cool ambient and warm practical light; use wet reflections without neon excess."],
            "material": ["Keep rain, glass, pavement, skin, fabric, vehicles, and architecture photorealistic with restrained fine film grain."],
        },
    },
    "minimal-editorial": {
        "source-led": {
            "composition": ["Derive the dominant geometry and negative space from the source object and its existing surroundings."],
            "lighting": ["Preserve the source light logic while simplifying competing highlights and shadows."],
            "material": ["Let the object's actual wear, fibers, glaze, scratches, and dents determine the material language."],
        },
        "quiet-window-light": {
            "composition": ["Use asymmetrical art-book framing with one clear object hierarchy and generous but believable negative space."],
            "lighting": ["Use one plausible directional window source with a clear shadow structure and gentle tonal falloff."],
            "material": ["Emphasize tactile fibers, glaze, chipped paint, folds, and small imperfections without sterile CGI polish."],
        },
    },
    "memory-atlas": {
        "source-led": {
            "composition": ["Build a spatial memory field from the Scene Cards' actual directional and geographic evidence."],
            "lighting": ["Preserve each photographic fragment's light and unify transitions using source-derived tone."],
            "material": ["Use only user-supplied or Scene Card-supported map, paper, terrain, drawing, or environmental materials."],
        },
        "watercolor-contour": {
            "composition": ["Embed real photographic places into one hand-drawn geography with varied scale and selective edge overlap."],
            "lighting": ["Preserve photographic light while unifying the field with restrained paper warmth."],
            "material": ["Use watercolor terrain, pencil contours, torn archival paper, faint coastline texture, and subtle travel ephemera."],
        },
    },
    "family-archive": {
        "source-led": {
            "composition": ["Build an archival relationship from repeated supplied gestures and objects, varying scale by story role."],
            "lighting": ["Preserve natural documentary light and the modest tonal differences between sources."],
            "material": ["Use only archival materials supported by supplied objects, surfaces, and repeated gestures."],
        },
        "graphite-paper": {
            "composition": ["Use a strong documentary rhythm with partial overlaps and breathing room rather than an equal-cell collage."],
            "lighting": ["Preserve documentary light and use warm paper as a unifying ground without applying a sepia filter to people."],
            "material": ["Use graphite object studies, tracing paper, contact-print edges, fabric fibers, thread, and photo corners."],
        },
    },
}


def expression_profile_names(system: str) -> tuple[str, ...]:
    if system not in EXPRESSION_PROFILES:
        return ()
    return tuple(EXPRESSION_PROFILES[system])


def resolve_expression_profile(system: str, name: str) -> dict[str, Any]:
    profiles = EXPRESSION_PROFILES.get(system, {})
    if name not in profiles:
        choices = ", ".join(profiles) or "none"
        raise ValueError(f"Unknown expression profile {name!r} for {system}; choose: {choices}")
    return {"name": name, **profiles[name]}
