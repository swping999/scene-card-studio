# Design principles and provenance / 设计原则与来源

## Principles / 原则

1. **Evidence before meaning.** Observation, interpretation, and direction remain separate and editable.
2. **Narrative Systems, not style presets.** Every system must change how a story is read, not merely recolor it.
3. **Human authority.** Input order is preserved by default; automatic reordering requires an explicit `--reorder` choice.
4. **Honest automation.** Heuristic analysis is labeled with its method and confidence. Curated examples identify manual direction.
5. **Local-first privacy.** Source photographs remain local unless the user explicitly chooses otherwise.

1. **先证据，后意义。** 观察、理解与导演决策相互分离，并且都可编辑。
2. **叙事系统，而非风格预设。** 每个系统都必须改变故事的阅读方式，而不只是调色。
3. **人的决定优先。** 默认保留输入顺序；只有明确传入 `--reorder` 才允许自动重排。
4. **诚实描述自动化。** 启发式分析必须标注方法与置信度；策划案例必须标明人工导演。
5. **隐私本地优先。** 除非用户明确选择，否则源照片不离开本地。

## Method

Scene Card Studio was implemented as an independent Scene Card, Visual Director, recommendation, and deterministic rendering workflow. It does not contain prompts, scripts, reference libraries, or visual assets copied from similarly themed source-available repositories.

Scene Card Studio 采用独立实现的 Scene Card、视觉导演、推荐与确定性渲染流程。仓库不包含从同类 source-available 项目复制的提示词、脚本、参考图库或视觉资产。

## Example assets

The three photographs in `examples/photos` and the three fictional documentary photographs in `examples/cases/family-archive/photos` were generated specifically for this repository with OpenAI's built-in image generation tool on 2026-08-09. They do not depict real people and were not derived from user photographs. Their role is to test and demonstrate this repository.

`examples/photos` 中的三张场景照片，以及 `examples/cases/family-archive/photos` 中的三张虚构人物纪实照片，均于 2026-08-09 使用 OpenAI 内置图像生成工具专门为本仓库生成，不涉及真实人物，也不来源于用户照片，仅用于测试和展示本项目。

The coastal memory-map illustration in `src/moments_to_pages/assets/maps` was generated for this repository with the same built-in image generation tool on 2026-08-09. The bundled Noto Sans CJK SC font is distributed under the SIL Open Font License 1.1; its notice is stored beside the font.

`src/moments_to_pages/assets/maps` 中的海岸记忆地图插画同样于 2026-08-09 使用内置图像生成工具为本仓库生成。随包提供的 Noto Sans CJK SC 字体采用 SIL Open Font License 1.1，许可证提示与字体放置在同一目录。

The final mixed-media Before/After synthesis records, including source lists and direction summaries, are documented in [`examples/GENERATIVE_CASES.md`](examples/GENERATIVE_CASES.md). Deterministic renderer outputs are labeled workprints; AI-composited images are labeled presentation synthesis.

最终混合媒介 Before/After 的源图列表与导演摘要记录在 [`examples/GENERATIVE_CASES.md`](examples/GENERATIVE_CASES.md)。确定性渲染结果标记为 Workprint，AI 复合图标记为 Presentation Synthesis。

## Contribution rule

Contributors must document the origin and usage terms of example assets. Narrative Systems must describe an expressive mechanism and may not depend on unauthorized imitation of a living artist, director, or photographer.

贡献者必须说明示例素材的来源和使用条款。Narrative System 必须描述一种表达机制，不得依赖对在世艺术家、导演或摄影师的未授权模仿。
