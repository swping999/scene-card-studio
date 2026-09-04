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

MINERAL_INK_MEMORY: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "mineral-ink painting",
    "subject_fidelity": [
        "Preserve identity-bearing faces, architecture, terrain silhouettes, route direction, object count, and the source's foreground-to-distance structure.",
    ],
    "transformation_policy": [
        "Translate the complete visible scene into mineral pigment, ink wash, and absorbent paper; change medium and emphasis, not place, identity, chronology, or geography.",
    ],
    "composition": [
        "Use ink density, mineral-color islands, reserved paper, and receding washes to organize memory without turning the image into a decorative scroll or collage.",
    ],
    "lighting": [
        "Convert source light into layered ink values and restrained mineral accents while keeping the original light direction and atmospheric depth legible.",
    ],
    "material": [
        "Use fibrous paper, pooled ink edges, dry-brush stone texture, granulating mineral blue-green and earth pigments, and sparse opaque accents.",
    ],
    "exclusions": [
        "No calligraphy, seals, copied historical composition, imitation of a named painter, floating decorative motifs, photographic cutouts, or generic fantasy mountains.",
    ],
    "output": ["The result must read as one contemporary mineral-ink memory image derived from the supplied evidence."],
}

IMPASTO_LIGHT_STUDY: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "impasto light study",
    "subject_fidelity": [
        "Preserve the recognizable subject silhouette, face geometry when present, architecture, object relationships, horizon, and camera position.",
    ],
    "transformation_policy": [
        "Translate the complete scene into a materially painted light study; allow brush simplification but do not invent props, costume, weather, or location.",
    ],
    "composition": [
        "Let one source-supported light path control the focal hierarchy; concentrate thick paint around illuminated structure and reduce secondary areas into quieter planes.",
    ],
    "lighting": [
        "Keep the source light direction and temperature relationships; build luminous color through adjacent strokes rather than digital glow or bloom.",
    ],
    "material": [
        "Use visible loaded-brush ridges, palette-knife interruptions, broken color, matte ground, and selective thick highlights with believable paint depth.",
    ],
    "exclusions": [
        "No named-painter imitation, generic starry swirls, uniformly thick texture, plastic 3D paint, photographic islands, frame, canvas mockup, or gallery wall.",
    ],
    "output": ["The result must read as one resolved contemporary painting in which light—not a filter—directs attention."],
}

PIXEL_DIARY: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "pixel diary illustration",
    "subject_fidelity": [
        "Preserve subject identity through stable silhouette, hairstyle, clothing colors, pose, landmark geometry, route direction, and object count.",
    ],
    "transformation_policy": [
        "Rebuild the complete scene on one consistent pixel grid; simplify detail by hierarchy without changing the depicted event, place, or relationships.",
    ],
    "composition": [
        "Use a cinematic pixel-art composition with clear large shapes, readable depth bands, and one calm focal beat rather than a game screenshot or sticker sheet.",
    ],
    "lighting": [
        "Use a restrained source-derived palette, clustered highlights, controlled dithering, and coherent atmospheric perspective.",
    ],
    "material": [
        "Use crisp intentional pixels, selective dithering, compact color ramps, and hand-placed edge clusters; keep one pixel scale throughout the image.",
    ],
    "exclusions": [
        "No UI, HUD, dialogue box, game logo, fake scanlines, mixed pixel sizes, vector-smooth faces, copied game assets, named-game imitation, or photographic fragments.",
    ],
    "output": ["The result must read as one authored pixel diary frame, not a photo passed through a mosaic filter."],
}

RISOGRAPH_ROUTE: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "risograph route print",
    "subject_fidelity": [
        "Preserve the supplied landmark silhouettes, people, objects, movement direction, and spatial order as legible print shapes.",
    ],
    "transformation_policy": [
        "Translate visible evidence into a limited-ink print system; route marks may connect only locations or directions supported by the Scene Cards.",
    ],
    "composition": [
        "Use one asymmetric poster-like field with a dominant place anchor, smaller evidence clusters, and directional rhythm; avoid equal cards and scrapbook stickers.",
    ],
    "lighting": [
        "Express value using two or three source-derived ink layers, overprint mixtures, and unprinted paper rather than gradients or digital glow.",
    ],
    "material": [
        "Use soy-ink grain, halftone density, slight registration drift, paper tooth, and transparent overprint while keeping fine identity cues readable.",
    ],
    "exclusions": [
        "No fabricated map labels, stamps, ticket collage, blue scrapbook board, white sticker outlines, duplicated inset photo, named-designer imitation, or unreadable generated text.",
    ],
    "output": ["The result must read as an original route-led risograph print whose marks remain traceable to supplied evidence."],
}

GOUACHE_PLACE_STUDY: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "gouache place study",
    "subject_fidelity": [
        "Preserve recognizable people, architecture, terrain contours, route direction, object count, and source composition while simplifying small detail.",
    ],
    "transformation_policy": [
        "Repaint every visible element in opaque gouache; allow shape simplification and edge hierarchy but no invented location, season, props, or characters.",
    ],
    "composition": [
        "Build a confident place study from interlocking matte shapes, clear foreground-to-distance layers, and one source-supported focal relationship.",
    ],
    "lighting": [
        "Preserve source light and weather through compact value groups, warm-cool adjacency, and restrained opaque highlights.",
    ],
    "material": [
        "Use matte gouache coverage, dry opaque scumble, visible brush edges, subtle paper tooth, and selective pencil underdrawing without photographic residue.",
    ],
    "exclusions": [
        "No named-illustrator imitation, generic children's-book decoration, outlines around every object, pasted photo, frame, lettering, or fabricated travel ephemera.",
    ],
    "output": ["The result must read as one complete hand-painted place study rather than a border treatment."],
}

CYANOTYPE_ARCHIVE: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "cyanotype archive study",
    "subject_fidelity": [
        "Preserve the subject contour, material damage, joins, tool relationships, gesture, and identifying structure as readable tonal evidence.",
    ],
    "transformation_policy": [
        "Translate the complete visible record into a cyanotype-like contact-print language; do not invent specimen names, provenance, measurements, or scientific claims.",
    ],
    "composition": [
        "Use one inspectable evidence field with deliberate exposure variation and negative-space hierarchy, not a faux antique page or equal specimen grid.",
    ],
    "lighting": [
        "Convert source luminance into deep Prussian-blue density, clear paper highlights, and readable midtone exposure without crushing identity-bearing detail.",
    ],
    "material": [
        "Use sensitized-paper grain, contact shadows, brushed emulsion edges, slight exposure irregularity, and clean uncoated paper where the composition needs air.",
    ],
    "exclusions": [
        "No invented handwriting, measurements, botanical labels, stamps, fake damage, duplicated specimens, named-photographer imitation, or decorative blueprint grid.",
    ],
    "output": ["The result must read as a contemporary evidence-bound cyanotype archive object."],
}

PAPER_RELIEF_LANDSCAPE: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "cut-paper relief landscape",
    "subject_fidelity": [
        "Preserve landmark silhouette, terrain layers, subject identity through profile and color, object count, route direction, and source depth order.",
    ],
    "transformation_policy": [
        "Translate the whole scene into cut and molded paper relief; simplify surfaces by depth plane without adding decorative travel icons or changing geography.",
    ],
    "composition": [
        "Construct one integrated bas-relief image with varied plane depth, selective apertures, and a dominant spatial path; avoid a sticker board or separated cutout collection.",
    ],
    "lighting": [
        "Use one plausible raking light so cast shadows clarify paper depth while respecting the source's overall time and atmosphere.",
    ],
    "material": [
        "Use deckled cotton paper, layered pulp, subtle fibers, embossed terrain, clean cut edges, and restrained shadow gaps at a consistent physical scale.",
    ],
    "exclusions": [
        "No white sticker outlines, floating icons, scrapbook page, duplicated source photo, foam-board look, excessive drop shadows, text, or named-paper-artist imitation.",
    ],
    "output": ["The result must read as one physically coherent paper landscape photographed from a single viewpoint."],
}

SCULPTED_PLACE_DIORAMA: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "sculpted miniature place diorama",
    "subject_fidelity": [
        "Preserve landmark silhouette, terrain topology, water direction, architecture, subject count, route geometry, and the source's near-to-far relationships.",
    ],
    "transformation_policy": [
        "Rebuild the complete scene as one physically plausible miniature diorama; simplify only surface detail and scale, never place identity, geography, weather evidence, or object relationships.",
    ],
    "composition": [
        "Use a single continuous terrain base with convincing elevation, embedded routes, and controlled foreground-to-distance scale; frame it as a collectible spatial portrait rather than a toy display.",
    ],
    "lighting": [
        "Use one studio-like physical light derived from the source direction, with soft cast shadows, contact shadows, and atmospheric depth that reveal volume without glossy spectacle.",
    ],
    "material": [
        "Use hand-sculpted plaster, matte resin, fine scenic fibers, translucent water material, weathered miniature timber or stone, and subtle tool marks at one consistent scale.",
    ],
    "exclusions": [
        "No toy-box border, isometric game tile, floating platform, cute character redesign, plastic CGI gloss, oversized props, UI, labels, branded model kit, or named-studio imitation.",
    ],
    "output": ["The result must read as one refined physical place model photographed in a real studio, not a generic 3D filter."],
}

THREADED_LANDSCAPE: dict[str, Any] = {
    "render_mode": "full-redraw",
    "output_medium": "threaded textile relief",
    "subject_fidelity": [
        "Preserve recognizable faces when present, body proportions, clothing silhouette, landmark geometry, terrain topology, horizon, object count, movement direction, and source depth order.",
    ],
    "transformation_policy": [
        "Rebuild the complete visible scene as one continuous fiber artwork; simplify surface detail by thread scale without changing identity, pose, geography, weather evidence, chronology, or relationships.",
    ],
    "composition": [
        "Use one uninterrupted textile field whose stitch direction follows perspective and form: flatter weave for distance, denser embroidery for focal structure, and restrained raised fiber only where real depth or emphasis requires it.",
    ],
    "lighting": [
        "Translate source light through thread color, fiber sheen, stitch density, and shallow cast shadow while preserving the original light direction and atmosphere.",
    ],
    "material": [
        "Use coherent woven ground, embroidery thread, wool roving, needle-felted transitions, looped highlights, and selective tufted relief at one believable physical scale.",
    ],
    "exclusions": [
        "No photographic pixels, split Before/After layout, framed wall mockup, fringe border, loose yarn props, handwritten slogan, doll-like character redesign, chunky craft-kit look, random patchwork, branded pattern, or named-maker imitation.",
    ],
    "output": [
        "The result must read as one refined contemporary textile relief whose depth and stitch language explain the supplied place or memory, not as a decorated photograph.",
    ],
}

AUTOCHROME_MEMORY: dict[str, Any] = {
    "render_mode": "heritage-photograph",
    "output_medium": "autochrome-inspired memory photograph",
    "subject_fidelity": [
        "Preserve present-day identity, age, pose, clothing, architecture, object placement, and the source moment without converting it into a historical reenactment.",
    ],
    "transformation_policy": [
        "Authorize only an early-color photographic material treatment and restrained tonal direction; do not invent period costume, ancestry, or date.",
    ],
    "composition": [
        "Use quiet observational framing, stable subject separation, and source-supported breathing room rather than theatrical nostalgia.",
    ],
    "lighting": [
        "Preserve source light while using gentle highlight bloom, muted color separation, and low-contrast shadow color characteristic of an early color plate.",
    ],
    "material": [
        "Use fine stochastic color grain, soft optical edges, delicate muted reds and blue-greens, glass-plate luminosity, and restrained surface variation.",
    ],
    "exclusions": [
        "No fake scratches, sepia wash, vignette cliché, costume change, de-aging, fabricated date, named-photographer imitation, or generic mobile vintage preset.",
    ],
    "output": ["The result must read as a carefully directed memory photograph, not a novelty antique filter."],
}

PIXEL_INK_MEMORY: dict[str, Any] = {
    "experimental": True,
    "render_mode": "full-redraw",
    "output_medium": "pixel-and-ink memory illustration",
    "subject_fidelity": [
        "Preserve identity, silhouette, architecture, terrain, object count, movement direction, and source depth through a stable shared shape map.",
    ],
    "transformation_policy": [
        "Fuse only two material systems—intentional pixel clusters for near evidence and mineral-ink diffusion for memory distance—without changing the depicted event or place.",
    ],
    "composition": [
        "Assign crisp pixel structure to identity-bearing anchors and let ink washes carry atmosphere and distance; transitions must follow depth, not arbitrary collage masks.",
    ],
    "lighting": [
        "Use one source-derived palette and one light direction across both media so the fusion reads as a single image.",
    ],
    "material": [
        "Use deliberate pixel clusters, restrained dithering, absorbent ink blooms, paper tooth, and a narrow transitional band where the two media interlock.",
    ],
    "exclusions": [
        "No split-screen, half-and-half effect, glitch overlay, game UI, pasted photograph, random ink splash, named-artist or named-game imitation, or mixed lighting models.",
    ],
    "output": ["Experimental profile: accept only when the two media share one composition, palette, and depth logic."],
}


TRAVEL_ZINE: dict[str, Any] = {
    "render_mode": "source-bound-editorial",
    "output_medium": "travel zine editorial",
    "design_tokens": {
        "palette": {"base": "warm-ivory", "accent": "muted-olive", "ink": "soft-charcoal"},
        "composition": {"density": "low", "asymmetry": "high", "primary_image_ratio": 0.62},
        "texture": {"paper": "aged-uncoated", "grain": "subtle", "torn_edges": "source-supported-only"},
        "typography": {"hierarchy": "editorial", "orientation": ["horizontal", "vertical"], "caption_density": "low"},
    },
    "subject_fidelity": [
        "Keep the supplied photograph as the primary evidence; preserve people, architecture, terrain, horizon, and camera perspective.",
    ],
    "transformation_policy": [
        "Use only source-supported route, date, location, ticket, map, paper, or handwriting cues; never fabricate travel facts or souvenirs.",
    ],
    "composition": [
        "Build one quiet travel-zine page around a single memory node: one dominant image, at most two source-derived detail studies, and generous irregular whitespace.",
        "Use route marks only when they correspond to visible or user-supplied geography; avoid a dense scrapbook board.",
    ],
    "lighting": ["Preserve source time, weather, and light direction; paper warmth must not wash out the photograph."],
    "material": ["Use restrained uncoated paper, tape, folds, or torn edges only when supported by the brief or source evidence; keep edges tactile but not sticker-like."],
    "exclusions": ["No fabricated tickets, dates, coordinates, map labels, handwriting, logos, or decorative sticker pile; no copied travel-zine layout."],
    "output": ["The result must read as an authored travel memory page, not a generic collage template."],
}

CHINESE_PHOTO_EDITORIAL: dict[str, Any] = {
    "render_mode": "restrained-ink-editorial",
    "output_medium": "contemporary ink-and-paper photo editorial",
    "design_tokens": {
        "palette": ["warm-paper", "ink-black", "diluted-gray", "seal-red-optional"],
        "composition": {"vertical_whitespace": "high", "asymmetry": "high", "motif_density": "low"},
        "texture": {"paper": "xuan-inspired-uncoated", "ink_bleed": "subtle", "brush_marks": "source-supported-only"},
        "typography": {"orientation": ["horizontal", "vertical"], "caption_density": "low"},
    },
    "subject_fidelity": ["Keep the supplied photograph and its identity-bearing subject readable; transform medium and framing, not the person's identity, place, or event."],
    "transformation_policy": ["Use ink wash, dry brush, and paper grain as a restrained editorial layer; bamboo, seals, mountains, calligraphy, and other motifs are optional and may appear only when source-supported or explicitly requested."],
    "composition": ["Use an asymmetric editorial field with large quiet paper areas, one photographic anchor, and a small number of source-derived ink passages; keep the image contemporary rather than costume-like."],
    "lighting": ["Preserve the source light direction and facial/structural modeling while translating values into ink density."],
    "material": ["Use warm uncoated paper, transparent washes, dry-brush edges, and controlled bleed; keep the subject's photographic evidence from dissolving into a generic painting."],
    "exclusions": ["No invented bamboo forest, mountains, seals, historical costume, gold ornament, dragon/cloud motifs, generated calligraphy, or named-artist imitation."],
    "output": ["Keep all Chinese titles, dates, and captions for the deterministic presentation layer; do not render text inside the image model output."],
}

SELECTIVE_MATERIAL_RELIEF: dict[str, Any] = {
    "render_mode": "selective-material-relief",
    "output_medium": "photographic subject with continuous relief environment",
    "design_tokens": {
        "composition": {"subject_fidelity": "high", "relief_extent": "environment-only", "depth": "shallow-to-moderate"},
        "material": {"surface": "paper-clay-stone", "edge_transition": "soft", "shadow": "source-consistent"},
        "lighting": {"continuity": "source-derived", "specular": "restrained"},
    },
    "subject_fidelity": ["Keep the main person, animal, vehicle, vessel, or object photographic and unmistakably real, including silhouette, texture, scale, and contact shadow."],
    "transformation_policy": ["Transform only the authorized environment into a continuous low-relief material; blend at real boundaries with no halo, cutout, or sticker edge."],
    "composition": ["Make the real subject the focal anchor and let relief depth explain the surrounding place; preserve camera position, horizon, and perspective."],
    "lighting": ["Preserve source light direction, color, and shadow footprint across the photographic subject and relief environment."],
    "material": ["Use believable shallow relief with layered paper, clay, plaster, or carved terrain; surface grain must follow geography and recede with depth."],
    "exclusions": ["No full-scene cartoonization, floating cutout, sticker outline, plastic CGI, unrelated diorama props, duplicated subject, or invented geography."],
    "output": ["At first glance the subject must be a real photograph; the surrounding material transformation should be visible only as a coherent spatial intervention."],
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
            "design_tokens": {
                "palette": ["warm-ivory", "olive-gray", "window-gold", "charcoal"],
                "composition": {"negative_space": "generous", "shadow_geometry": "explicit", "density": "low"},
                "texture": {"film_grain": "fine", "dust": "subtle", "surfaces": "tactile"},
            },
            "composition": ["Use asymmetrical art-book framing with one clear hierarchy and generous but believable negative space."],
            "lighting": ["Use one plausible directional window source with a clear geometric shadow structure, warm side light, protected highlights, and gentle tonal falloff."],
            "material": ["Emphasize tactile fibers, glaze, chipped paint, folds, fine film grain, and small imperfections without sterile CGI polish or dreamy glow."],
            "exclusions": ["No neon, plastic CGI, over-smoothed skin, artificial bokeh, or generic cinematic preset."],
        },
        "impasto-light-study": IMPASTO_LIGHT_STUDY,
        "chinese-photo-editorial": CHINESE_PHOTO_EDITORIAL,
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
        "cyanotype-archive": CYANOTYPE_ARCHIVE,
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
        "mineral-ink-memory": MINERAL_INK_MEMORY,
        "impasto-light-study": IMPASTO_LIGHT_STUDY,
        "pixel-diary": PIXEL_DIARY,
        "risograph-route": RISOGRAPH_ROUTE,
        "gouache-place-study": GOUACHE_PLACE_STUDY,
        "paper-relief-landscape": PAPER_RELIEF_LANDSCAPE,
        "sculpted-place-diorama": SCULPTED_PLACE_DIORAMA,
        "threaded-landscape": THREADED_LANDSCAPE,
        "autochrome-memory": AUTOCHROME_MEMORY,
        "pixel-ink-memory": PIXEL_INK_MEMORY,
        "travel-zine": TRAVEL_ZINE,
        "chinese-photo-editorial": CHINESE_PHOTO_EDITORIAL,
        "selective-material-relief": SELECTIVE_MATERIAL_RELIEF,
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
        "cyanotype-archive": CYANOTYPE_ARCHIVE,
        "autochrome-memory": AUTOCHROME_MEMORY,
        "threaded-landscape": THREADED_LANDSCAPE,
        "travel-zine": TRAVEL_ZINE,
        "chinese-photo-editorial": CHINESE_PHOTO_EDITORIAL,
        "selective-material-relief": SELECTIVE_MATERIAL_RELIEF,
    },
    "museum-catalogue": {
        "source-led": {
            "composition": ["Isolate the supplied subject as a catalogue plate using its true scale cues and material evidence."],
            "lighting": ["Use neutral, source-compatible conservation light with controlled highlights and readable surface relief."],
            "material": ["Preserve the object's real patina, fibers, glaze, wear, joins, and repairs without simulated luxury polish."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
        "heritage-portrait": HERITAGE_PORTRAIT,
        "cyanotype-archive": CYANOTYPE_ARCHIVE,
        "chinese-photo-editorial": CHINESE_PHOTO_EDITORIAL,
    },
    "travel-journal": {
        "source-led": {
            "composition": ["Build a journey field from supplied routes, thresholds, objects, and pauses without forcing a literal map."],
            "lighting": ["Preserve source time and weather evidence while using palette relationships to shape the journey."],
            "material": ["Use only supplied or explicitly authorized tickets, maps, handwriting, paper, fabric, and environmental traces."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
        "mineral-ink-memory": MINERAL_INK_MEMORY,
        "impasto-light-study": IMPASTO_LIGHT_STUDY,
        "pixel-diary": PIXEL_DIARY,
        "risograph-route": RISOGRAPH_ROUTE,
        "gouache-place-study": GOUACHE_PLACE_STUDY,
        "paper-relief-landscape": PAPER_RELIEF_LANDSCAPE,
        "sculpted-place-diorama": SCULPTED_PLACE_DIORAMA,
        "threaded-landscape": THREADED_LANDSCAPE,
        "autochrome-memory": AUTOCHROME_MEMORY,
        "travel-zine": TRAVEL_ZINE,
        "chinese-photo-editorial": CHINESE_PHOTO_EDITORIAL,
        "selective-material-relief": SELECTIVE_MATERIAL_RELIEF,
    },
    "journey-taxonomy": {
        "source-led": {
            "composition": ["Build one semantic place field from visible evidence, grouping observed elements by role rather than by decorative similarity."],
            "lighting": ["Preserve source time, weather, and color relationships across the dominant scene and its material studies."],
            "material": ["Keep every extracted visual cue traceable to a supplied person, place, object, texture, plant, animal, weather condition, or route feature."],
        },
        "watercolor-chronicle": WATERCOLOR_CHRONICLE,
        "mineral-ink-memory": MINERAL_INK_MEMORY,
        "impasto-light-study": IMPASTO_LIGHT_STUDY,
        "pixel-diary": PIXEL_DIARY,
        "risograph-route": RISOGRAPH_ROUTE,
        "gouache-place-study": GOUACHE_PLACE_STUDY,
        "paper-relief-landscape": PAPER_RELIEF_LANDSCAPE,
        "sculpted-place-diorama": SCULPTED_PLACE_DIORAMA,
        "threaded-landscape": THREADED_LANDSCAPE,
        "autochrome-memory": AUTOCHROME_MEMORY,
        "pixel-ink-memory": PIXEL_INK_MEMORY,
        "travel-zine": TRAVEL_ZINE,
        "selective-material-relief": SELECTIVE_MATERIAL_RELIEF,
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
        "cyanotype-archive": CYANOTYPE_ARCHIVE,
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
