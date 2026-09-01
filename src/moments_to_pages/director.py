from __future__ import annotations

import re
from dataclasses import dataclass

from .model import SceneCard


@dataclass(frozen=True)
class Recommendation:
    system: str
    score: float
    reason: str


@dataclass(frozen=True)
class ProfileRecommendation:
    profile: str
    reason: str


def _term_is_negated(evidence: str, start: int) -> bool:
    prefix = evidence[max(0, start - 40):start]
    english = re.search(
        r"(?:\bno\b|\bnot\b|\bwithout\b|\bavoid(?:ing)?\b|\bdo not\b|\bdon't\b)[^.!?;,，。；！？\n]{0,28}$",
        prefix,
    )
    chinese = re.search(r"(?:不要|别|避免|不想要|不需要|拒绝|去掉)[^，。；！？!?\n]{0,16}$", prefix)
    return bool(english or chinese)


def _term_counts(evidence: str, term: str) -> tuple[int, int]:
    escaped = re.escape(term.casefold())
    pattern = rf"(?<![a-z]){escaped}(?![a-z])" if term.isascii() else escaped
    positive = 0
    negated = 0
    for match in re.finditer(pattern, evidence):
        if _term_is_negated(evidence, match.start()):
            negated += 1
        else:
            positive += 1
    return positive, negated


def _contains_unnegated(evidence: str, *terms: str) -> bool:
    return any(_term_counts(evidence, term)[0] for term in terms)


def recommend_systems(cards: list[SceneCard], brief: str = "") -> list[Recommendation]:
    if not cards:
        return []
    single = len(cards) == 1
    gestures = " ".join(card.observation.dominant_gesture for card in cards).lower()
    directed_cards = [
        card for card in cards
        if card.interpretation.method != "heuristic" or card.interpretation.confidence > .5
    ]
    intents = " ".join(card.interpretation.narrative_intent for card in directed_cards).lower()
    subjects = " ".join(" ".join(card.observation.subjects) for card in cards).lower()
    tones = " ".join(" ".join(card.interpretation.emotional_tone) for card in directed_cards).lower()
    notes = " ".join(card.direction.director_note for card in cards).lower()
    evidence = " ".join((brief.lower(), gestures, intents, subjects, tones, notes))
    average_saturation = sum(card.saturation for card in cards) / len(cards)
    cinematic_words = ("cinematic", "film", "movie", "storyboard", "shot", "waiting", "departure", "night", "rain", "reflection", "window", "vehicle", "movement", "pause", "电影", "分镜", "镜头", "等待", "离开", "出发", "夜", "雨", "倒影", "窗", "车辆", "移动", "停顿")
    minimal_words = ("minimal", "quiet", "still life", "negative space", "object", "material", "linen", "chair", "cup", "mug", "ceramic", "fabric", "surface", "fold", "极简", "安静", "物件", "材质", "亚麻", "椅子", "杯子", "陶瓷", "织物", "表面", "折叠", "留白", "静物")
    memory_words = ("memory", "atlas", "map", "geography", "spatial", "route", "departure", "distance", "place", "road", "railway", "记忆", "地图", "地理", "路线", "离开", "出发", "距离", "地点", "道路", "铁路", "空间", "归来")
    family_words = ("family", "chronicle", "care", "inherit", "home", "shared", "domestic", "sibling", "father", "mother", "家庭", "纪事", "照料", "照顾", "传承", "共同", "家务", "父亲", "母亲", "兄弟", "姐妹", "代际")
    editorial_words = ("editorial", "rhythm", "sequence", "photo essay", "spread", "layout", "编辑", "节奏", "组照", "跨页", "排版", "图文")
    field_words = ("field log", "field note", "observation", "documentary", "evidence", "repair", "worksite", "现场日志", "田野", "观察", "纪实", "证据", "维修", "工作现场")
    museum_words = ("museum", "catalogue", "artifact", "collection", "object", "archive", "specimen", "exhibition", "repair", "patina", "博物馆", "图录", "藏品", "收藏", "物件", "档案", "标本", "展览", "修复", "包浆")
    travel_words = ("travel journal", "journey", "travel", "ticket", "station", "road", "hotel", "luggage", "threshold", "旅行日志", "旅途", "旅行", "票据", "车站", "道路", "酒店", "行李", "门槛")
    street_words = ("street", "reportage", "crowd", "pedestrian", "market", "crossing", "traffic", "sidewalk", "街头", "纪实报道", "人群", "行人", "市场", "路口", "交通", "人行道")
    fashion_words = ("fashion", "editorial portrait", "garment", "outfit", "wardrobe", "pose", "fabric", "silhouette", "时尚", "服装", "时装", "穿搭", "造型", "姿势", "面料", "轮廓")

    def count_terms(terms: tuple[str, ...]) -> tuple[int, int]:
        counts = [_term_counts(evidence, term) for term in terms]
        return (
            sum(1 for positive, _ in counts if positive),
            sum(1 for positive, negated in counts if negated and not positive),
        )

    cinematic_matches = count_terms(cinematic_words)
    minimal_matches = count_terms(minimal_words)
    memory_matches = count_terms(memory_words)
    family_matches = count_terms(family_words)
    editorial_matches = count_terms(editorial_words)
    field_matches = count_terms(field_words)
    museum_matches = count_terms(museum_words)
    travel_matches = count_terms(travel_words)
    street_matches = count_terms(street_words)
    fashion_matches = count_terms(fashion_words)
    def semantic_score(matches: int, negated: int, baseline: float) -> float:
        if matches >= 2:
            return .92
        if matches == 1:
            return .82
        return min(baseline, .18) if negated else baseline

    cinematic_score = semantic_score(*cinematic_matches, .52)
    minimal_score = semantic_score(*minimal_matches, .58 if average_saturation < .45 else .50)
    results = [
        Recommendation("memory-atlas", semantic_score(*memory_matches, .48),
                       "The source's spatial cues can become one self-contained memory field." if single else "Spatial movement and transitions can become a visible route through the sequence."),
        Recommendation("field-log", semantic_score(*field_matches, .56 if average_saturation < .35 else .46),
                       "Restrained color and observational detail suit a documentary record."),
        Recommendation("family-archive", semantic_score(*family_matches, .46),
                       "The visible domestic gesture can become one restrained archival record." if single else "Repeated domestic gestures and relationships can be read as a family record."),
        Recommendation("cinematic-storyboard", cinematic_score,
                       "Motivated light, weather, and framing can make this one directed cinematic image." if single else "Temporal continuity, motivated light, weather, and shot relationships can carry the sequence."),
        Recommendation("minimal-editorial", minimal_score,
                       "Object hierarchy, negative space, light, and material evidence can direct each frame."),
        Recommendation("editorial-sequence", semantic_score(*editorial_matches, .60),
                       "Scale, pause, contrast, and negative space can direct one editorial image." if single else "Scale, pause, contrast, and source order can create an editorial rhythm across separate frames."),
        Recommendation("museum-catalogue", semantic_score(*museum_matches, .44),
                       "Inspectable object evidence can form one deterministic catalogue plate." if single else "Inspectable object evidence and supplied metadata can form a deterministic catalogue sequence."),
        Recommendation("travel-journal", semantic_score(*travel_matches, .44),
                       "The visible place, threshold, or travel evidence can become one journey moment without invented geography." if single else "Supplied movement, thresholds, tickets, places, and pauses can form a journey record without invented geography."),
        Recommendation("street-reportage", semantic_score(*street_matches, .42),
                       "The observed public gesture and context can become one factual reportage image." if single else "Observed public gestures and environmental context can become a factual reportage sequence."),
        Recommendation("fashion-editorial", semantic_score(*fashion_matches, .40),
                       "Pose, garment construction, fabric behavior, and crop tension can carry one editorial image." if single else "Pose, garment construction, fabric behavior, and shot-scale contrast can carry an editorial sequence."),
    ]
    return sorted(results, key=lambda item: item.score, reverse=True)


def recommend_expression_profile(system: str, cards: list[SceneCard], brief: str = "") -> ProfileRecommendation:
    """Select a non-default Profile only when the user explicitly asks for its visual language."""
    evidence = " ".join([
        brief,
        *(card.interpretation.narrative_intent for card in cards),
        *(card.direction.director_note for card in cards),
    ]).casefold()

    def contains(*terms: str) -> bool:
        return _contains_unnegated(evidence, *terms)

    if system == "cinematic-storyboard" and contains("rain", "rainy", "nocturne", "wet night", "雨", "雨夜", "湿润夜景"):
        return ProfileRecommendation("rain-nocturne", "The brief explicitly requests rain or nocturnal atmosphere.")
    if system == "minimal-editorial" and contains("window light", "quiet window", "窗光", "窗边光", "安静窗光"):
        return ProfileRecommendation("quiet-window-light", "The brief explicitly requests a quiet window-light treatment.")
    if system == "memory-atlas" and contains("watercolor contour", "photographic anchor", "photo and watercolor", "水彩轮廓", "照片锚点", "照片与水彩", "真实照片建筑"):
        return ProfileRecommendation("watercolor-contour", "The brief asks to retain photographic anchors inside drawn watercolor geography.")
    if system in {"memory-atlas", "family-archive", "museum-catalogue", "travel-journal"} and contains("watercolor", "paint everything", "fully painted", "水彩", "全部画成", "全画面绘制", "人物也水彩"):
        return ProfileRecommendation("watercolor-chronicle", "The brief explicitly requests a coherent full-frame watercolor medium.")
    if system == "family-archive" and contains("graphite", "pencil", "tracing paper", "石墨", "铅笔", "描图纸", "素描"):
        return ProfileRecommendation("graphite-paper", "The brief explicitly requests graphite or tracing-paper expression.")
    if system in {"family-archive", "museum-catalogue"} and contains("silver gelatin", "hand-colored", "heritage portrait", "vintage portrait", "银盐", "手工着色", "传统影像", "复古肖像"):
        return ProfileRecommendation("heritage-portrait", "The brief explicitly requests a conserved heritage-photograph treatment.")
    if system == "street-reportage" and contains("black and white", "black-and-white", "monochrome", "黑白", "单色"):
        return ProfileRecommendation("monochrome-reportage", "The brief explicitly requests monochrome reportage.")
    if system in {"memory-atlas", "fashion-editorial"} and contains("dream logic", "surreal", "impossible", "梦境逻辑", "超现实", "不可能空间"):
        return ProfileRecommendation("dream-logic", "The brief explicitly requests identity-locked surreal spatial logic.")
    return ProfileRecommendation("source-led", "No explicit expression treatment was requested, so source-led is the safest default.")
