from __future__ import annotations

from dataclasses import dataclass
import re

from .model import SceneCard


@dataclass(frozen=True)
class Recommendation:
    system: str
    score: float
    reason: str


def recommend_systems(cards: list[SceneCard]) -> list[Recommendation]:
    if not cards:
        return []
    gestures = " ".join(card.observation.dominant_gesture for card in cards).lower()
    intents = " ".join(card.interpretation.narrative_intent for card in cards).lower()
    subjects = " ".join(" ".join(card.observation.subjects) for card in cards).lower()
    tones = " ".join(" ".join(card.interpretation.emotional_tone) for card in cards).lower()
    notes = " ".join(card.direction.director_note for card in cards).lower()
    evidence = " ".join((gestures, intents, subjects, tones, notes))
    tokens = set(re.findall(r"[a-z]+", evidence))
    average_saturation = sum(card.saturation for card in cards) / len(cards)
    cinematic_words = ("waiting", "departure", "night", "rain", "reflection", "window", "vehicle", "movement", "pause", "等待", "离开", "出发", "夜", "雨", "倒影", "窗", "车辆", "移动", "停顿")
    minimal_words = ("object", "material", "linen", "chair", "cup", "mug", "ceramic", "fabric", "surface", "fold", "物件", "材质", "亚麻", "椅子", "杯子", "陶瓷", "织物", "表面", "折叠", "留白", "静物")
    memory_words = ("journey", "route", "departure", "distance", "travel", "place", "road", "railway", "旅途", "旅行", "路线", "离开", "出发", "距离", "地点", "道路", "铁路", "空间", "归来")
    family_words = ("family", "care", "inherit", "home", "shared", "domestic", "sibling", "father", "mother", "家庭", "照料", "照顾", "传承", "共同", "家务", "父亲", "母亲", "兄弟", "姐妹", "代际")
    museum_words = ("artifact", "collection", "object", "archive", "specimen", "exhibition", "repair", "patina", "藏品", "收藏", "物件", "档案", "标本", "展览", "修复", "包浆")
    travel_words = ("journey", "travel", "ticket", "station", "road", "hotel", "luggage", "threshold", "旅途", "旅行", "票据", "车站", "道路", "酒店", "行李", "门槛")
    street_words = ("street", "crowd", "pedestrian", "market", "crossing", "traffic", "sidewalk", "街头", "人群", "行人", "市场", "路口", "交通", "人行道")
    fashion_words = ("fashion", "garment", "outfit", "wardrobe", "pose", "fabric", "silhouette", "服装", "时装", "穿搭", "造型", "姿势", "面料", "轮廓")

    def count_terms(terms: tuple[str, ...]) -> int:
        return sum((term in tokens) if term.isascii() else (term in evidence) for term in terms)

    cinematic_matches = count_terms(cinematic_words)
    minimal_matches = count_terms(minimal_words)
    memory_matches = count_terms(memory_words)
    family_matches = count_terms(family_words)
    museum_matches = count_terms(museum_words)
    travel_matches = count_terms(travel_words)
    street_matches = count_terms(street_words)
    fashion_matches = count_terms(fashion_words)
    cinematic_score = .88 if cinematic_matches >= 2 else .80 if cinematic_matches == 1 else .56
    minimal_score = .86 if average_saturation < .45 and minimal_matches >= 2 else .82 if average_saturation < .45 and minimal_matches == 1 else .54
    results = [
        Recommendation("memory-atlas", .90 if memory_matches >= 2 else .84 if memory_matches else .58,
                       "Spatial movement and transitions can become a visible route through the sequence."),
        Recommendation("field-log", .78 if average_saturation < .35 else .62,
                       "Restrained color and observational detail suit a documentary record."),
        Recommendation("family-archive", .90 if family_matches >= 2 else .86 if family_matches else .52,
                       "Repeated domestic gestures and relationships can be read as a family record."),
        Recommendation("cinematic-storyboard", cinematic_score,
                       "Temporal continuity, motivated light, weather, and shot relationships can carry the sequence."),
        Recommendation("minimal-editorial", minimal_score,
                       "Object hierarchy, negative space, light, and material evidence can direct each frame."),
        Recommendation("editorial-sequence", .74,
                       "Scale, pause, contrast, and source order can create an editorial rhythm across separate frames."),
        Recommendation("museum-catalogue", .88 if museum_matches >= 2 else .78 if museum_matches else .48,
                       "Inspectable object evidence and supplied metadata can form a deterministic catalogue sequence."),
        Recommendation("travel-journal", .90 if travel_matches >= 2 else .80 if travel_matches else .50,
                       "Supplied movement, thresholds, tickets, places, and pauses can form a journey record without invented geography."),
        Recommendation("street-reportage", .88 if street_matches >= 2 else .78 if street_matches else .46,
                       "Observed public gestures and environmental context can become a factual reportage sequence."),
        Recommendation("fashion-editorial", .88 if fashion_matches >= 2 else .78 if fashion_matches else .44,
                       "Pose, garment construction, fabric behavior, and shot-scale contrast can carry an editorial sequence."),
    ]
    return sorted(results, key=lambda item: item.score, reverse=True)
