# v0.4 gallery · fresh Before / After cases

This gallery contains 13 newly generated Before / After pairs. Each Before was intentionally generated as an unpolished phone-style source. Each After was directed from its matching source with explicit identity, object, evidence, composition, material, and exclusion rules.

The cases do not use third-party photographs, style assets, prompt text, artist names, director names, or publication names. All depicted people, places, and objects are fictional AI-generated examples created for Scene Card Studio.

## Case map

| Visual direction | Type | Narrative System | Expression Profile |
| --- | --- | --- | --- |
| Cinematic Sequence | System | `cinematic-storyboard` | `source-led` |
| Memory Atlas | System | `memory-atlas` | `watercolor-contour` |
| Family Chronicle | System | `family-archive` | `source-led` |
| Quiet Editorial | System | `minimal-editorial` | `source-led` |
| Editorial Rhythm | System | `editorial-sequence` | `source-led` |
| Field Log | System | `field-log` | `source-led` |
| Watercolor Chronicle | Profile | `memory-atlas` | `watercolor-chronicle` |
| Heritage Portrait | Profile | `family-archive` | `heritage-portrait` |
| Museum Catalogue | System | `museum-catalogue` | `source-led` |
| Travel Journal | System | `travel-journal` | `source-led` |
| Street Reportage | System | `street-reportage` | `monochrome-reportage` |
| Fashion Editorial | System | `fashion-editorial` | `source-led` |
| Dream Logic | Profile | `memory-atlas` | `dream-logic` |

The compact direction records are stored in [`case-records.json`](case-records.json). Every case also has a schema-valid [`story.json` and recompilable Prompt Manifest](evidence/index.json), including source and reference-output hashes. Regenerate or verify all 13 evidence bundles with:

```bash
python examples/cases/v0.4-gallery/build_evidence.py --check
```

These are prompt-level benchmark records. They do not claim that a new image model run will reproduce identical pixels, and they do not substitute a reference image for a formally bound candidate output.

## 中文说明

本画廊包含 13 组全新生成的 Before / After。每张 Before 都刻意模拟构图普通、光线平、环境杂乱的手机随手拍；每张 After 都基于对应原图进行独立视觉导演，并明确约束主体身份、物件证据、构图、材质与禁止项。

案例未使用第三方照片、风格资产、提示词、艺术家姓名、导演姓名或刊物名称。画面中的人物、地点与物件均为 Scene Card Studio 专门生成的虚构 AI 示例。每个案例现在都提供符合 Schema 的 `story.json` 与可重新编译的 Prompt Manifest，并记录源图和参考 After 的哈希；参考图不能代替正式绑定的新候选输出。
