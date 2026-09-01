from __future__ import annotations

from typing import Any

WATERCOLOR_CHRONICLE: dict[str, Any] = {
    "render_mode": "full-redraw",
    "subject_fidelity": [
        "Preserve face geometry, expression, pose, body proportions, clothing silhouette, architecture, horizon, and identity-bearing details while changing only their visible medium.",
    ],
    "transformation_policy": [
        "Authorize a medium-only transformation of the entire visible image into watercolor; do not change identity, anatomy, object count, location, action, chronology, or spatial evidence.",
    ],
    "composition": [
        "Recompose supplied people, objects, and places as one continuous painting whose transitions are carried by washes, reserved paper, and spatial evidence rather than pasted photographs.",
    ],
    "lighting": [
        "Translate source light into transparent value washes while preserving light direction, facial modeling, depth, and source-derived color relationships.",
    ],
    "material": [
        "Render faces, skin, hair, clothing, objects, architecture, sky, water, and terrain in one coherent watercolor medium using transparent washes, wet-on-wet diffusion, restrained dry-brush accents, pigment blooms, and visible paper tooth.",
        "Keep the sharpest brush information around identity-bearing facial features, hands, and structural landmarks; let secondary edges dissolve naturally.",
    ],
    "exclusions": [
        "Leave no photographic pixels, pasted portrait cutouts, hard extraction halos, synthetic skin, or photo-plus-watercolor-border effect.",
        "Do not imitate a named artist or use an unlicensed artwork as a style reference.",
    ],
    "output": [
        "The finished artifact must read as one continuous hand-painted watercolor work, including every visible person, not as a decorated photograph.",
    ],
}

HERITAGE_PORTRAIT: dict[str, Any] = {
    "render_mode": "heritage-photograph",
    "subject_fidelity": [
        "Keep the subject's present-day age, identity, facial structure, expression, body proportions, clothing construction, and pose; do not fabricate ancestry or historical identity.",
    ],
    "transformation_policy": [
        "Authorize photographic-process treatment and restrained hand coloring only; do not replace clothing, invent period costume, de-age, or change ethnicity, status, or family relationships.",
    ],
    "composition": [
        "Use a formal but human portrait hierarchy with stable posture, quiet background separation, and enough breathing room for an archival mount.",
    ],
    "lighting": [
        "Use broad studio-like modeling derived from the source direction, with controlled highlights and readable shadow detail rather than theatrical glamour light.",
    ],
    "material": [
        "Use restrained silver-gelatin tonal depth, fine paper grain, subtle optical softness, and sparse hand-applied color that follows real material boundaries.",
    ],
    "exclusions": [
        "No fake damage, heavy sepia wash, costume invention, aristocratic props, beauty retouching, false historical documents, or named-photographer imitation.",
    ],
    "output": ["The result must read as a carefully conserved portrait object, not a novelty vintage filter."],
}

DREAM_LOGIC: dict[str, Any] = {
    "render_mode": "identity-locked-surrealism",
    "subject_fidelity": [
        "Lock the recognizable identity, face, anatomy, pose logic, subject count, clothing identity, and defining object geometry before changing scale or spatial relationships.",
    ],
    "transformation_policy": [
        "Permit only the Scene Card-authorized subjects and places to change scale, adjacency, gravity, repetition, or enclosure; keep all unlisted evidence unchanged.",
    ],
    "composition": [
        "Build one coherent impossible spatial rule with a clear focal hierarchy; every displacement must support the narrative intent rather than accumulate dreamlike decoration.",
    ],
    "lighting": [
        "Use one consistent light model across impossible spatial relationships so the scene remains materially convincing.",
    ],
    "material": [
        "Keep people, objects, and environments materially specific and edge-consistent even when their scale or adjacency becomes impossible."],
    "exclusions": [
        "No random floating-object collage, duplicate faces, extra limbs, portal clichés, melting clocks, generic cosmic backgrounds, or named-surrealist imitation.",
    ],
    "output": ["The result must express one legible dream rule while remaining immediately traceable to the supplied subjects."],
}


EXPRESSION_PROFILES: dict[str, dict[str, dict[str, Any]]] = {
    "cinematic-storyboard": {
        "source-led": {
            "composition": ["Respect the source camera position and derive shot scale from the visible scene rather than forcing a lens signature."],
            "lighting": ["Develop only light sources already visible or physically plausible in the source."],
            "material": ["Keep photographic surfaces natural and use only restrained source-compatible grain or atmosphere."],
        },
        "rain-nocturne": {
            "composition": ["Use a natural observational perspective with legible foreground, midground, and background."],
            "lighting": ["Shape the frame with motivated cool ambient and warm practical light; use wet reflections without neon excess."],
            "material": ["Keep rain, glass, pavement, skin, fabric, vehicles, and architecture photorealistic with restrained fine film grain."],
        },
    },
    "minimal-editorial": {
        "source-led": {
            "composition": ["Derive dominant geometry and negative space from the source object and its existing surroundings."],
            "lighting": ["Preserve the source light logic while simplifying competing highlights and shadows."],
            "material": ["Let actual wear, fibers, glaze, scratches, and dents determine the material language."],
        },
        "quiet-window-light": {
            "composition": ["Use asymmetrical art-book framing with one clear hierarchy and generous but believable negative space."],
            "lighting": ["Use one plausible directional window source with a clear shadow structure and gentle tonal falloff."],
            "material": ["Emphasize tactile fibers, glaze, chipped paint, folds, and small imperfections without sterile CGI polish."],
        },
    },
    "editorial-sequence": {
        "source-led": {
            "composition": ["Use source-supported scale and negative space to create a clear editorial rhythm."],
            "lighting": ["Preserve source light while keeping the directed image tonally coherent."],
            "material": ["Keep photographic surfaces specific and avoid a uniform preset across unrelated materials."],
        },
    },
    "field-log": {
        "source-led": {
            "composition": ["Prioritize legible evidence, observed gesture, and environmental context over dramatic cropping."],
            "lighting": ["Retain available light and believable exposure, including imperfect documentary conditions."],
            "material": ["Preserve weather, wear, dust, skin, fabric, tools, and surfaces as observed."],
        },
    },
    "memory-atlas": {
        "source-led": {
            "composition": ["Build a spatial memory field from actual directional and geographic evidence."],
            "lighting": ["Preserve the photographic source light and unify transitions using source-derived tone."],
            "material": ["Use only user-supplied or Scene Card-supported map, paper, terrain, drawing, or environmental materials."],
        },
        "watercolor-contour": {
            "composition": ["Embed real photographic places into one hand-drawn geography with varied scale and selective edge overlap."],
            "lighting": ["Preserve photographic light while unifying the field with restrained paper warmth."],
            "material": ["Use watercolor terrain, pencil contours, torn archival paper, faint coastline texture, and subtle travel ephemera."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
        "full-watercolor-memory": {"alias_for": "watercolor-chronicle", **WATERCOLOR_CHRONICLE},
        "dream-logic": DREAM_LOGIC,
    },
    "family-archive": {
        "source-led": {
            "composition": ["Build an archival relationship from supplied gestures and objects, varying scale by Scene Card emphasis."],
            "lighting": ["Preserve natural documentary light and source-supported tonal differences."],
            "material": ["Use only archival materials supported by supplied objects, surfaces, and repeated gestures."],
        },
        "graphite-paper": {
            "composition": ["Use strong documentary rhythm with partial overlaps and breathing room rather than an equal-cell collage."],
            "lighting": ["Preserve documentary light and use warm paper as a ground without applying sepia to people."],
            "material": ["Use graphite object studies, tracing paper, contact-print edges, fabric fibers, thread, and photo corners."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
        "heritage-portrait": HERITAGE_PORTRAIT,
    },
    "museum-catalogue": {
        "source-led": {
            "composition": ["Isolate the supplied subject as a catalogue plate using its true scale cues and material evidence."],
            "lighting": ["Use neutral, source-compatible conservation light with controlled highlights and readable surface relief."],
            "material": ["Preserve the object's real patina, fibers, glaze, wear, joins, and repairs without simulated luxury polish."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
        "heritage-portrait": HERITAGE_PORTRAIT,
    },
    "travel-journal": {
        "source-led": {
            "composition": ["Build a journey field from supplied routes, thresholds, objects, and pauses without forcing a literal map."],
            "lighting": ["Preserve source time and weather evidence while using palette relationships to shape the journey."],
            "material": ["Use only supplied or explicitly authorized tickets, maps, handwriting, paper, fabric, and environmental traces."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
    },
    "street-reportage": {
        "source-led": {
            "composition": ["Keep decisive observed gestures and environmental context legible; crop for event clarity rather than graphic spectacle."],
            "lighting": ["Preserve available street light, mixed color temperature, and imperfect exposure when they carry evidence."],
            "material": ["Retain pavement, weather, skin, fabric, signage shapes, motion, and camera grain as documentary evidence."],
        },
        "monochrome-reportage": {
            "composition": ["Use direct street framing, controlled high contrast, and enough context to understand the observed event."],
            "lighting": ["Convert source luminance into a detailed black-and-white scale with protected skin and shadow information."],
            "material": ["Use restrained silver-rich grain and crisp local contrast without crushed blacks or artificial damage."],
        },
    },
    "fashion-editorial": {
        "source-led": {
            "composition": ["Use full-bleed presence, assertive but anatomy-safe cropping, and source-supported shot scale."],
            "lighting": ["Build from the source light and wardrobe palette; keep skin tone and fabric color truthful."],
            "material": ["Preserve garment construction, fabric behavior, styling details, skin texture, and location surfaces."],
        },
        "dream-logic": DREAM_LOGIC,
    },
}


def expression_profile_names(system: str) -> tuple[str, ...]:
    return tuple(EXPRESSION_PROFILES.get(system, {}))


def resolve_expression_profile(system: str, name: str) -> dict[str, Any]:
    profiles = EXPRESSION_PROFILES.get(system, {})
    if name not in profiles:
        choices = ", ".join(profiles) or "none"
        raise ValueError(f"Unknown expression profile {name!r} for {system}; choose: {choices}")
    return {"name": name, **profiles[name]}
