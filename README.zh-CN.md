# Scene Card Studio｜场景卡片工作室

中文 · [English](README.md)

> **这不是一个照片风格转换工具，而是一套基于 Scene Card 的个人照片视觉叙事引擎。**

Scene Card Studio 将照片中可观察的事实转化为可编辑叙事决策、版本化生成提示词、导演成片和确定性版面。它不只问“照片应该变成什么风格”，而是先判断“这段故事应该如何被阅读”。

```text
照片 → Scene Cards → Narrative System → Prompt Compiler → 图像生成 → 审美检查 → 重试 / 接受
```

## Before / After 首页案例

以下原始照片均为本项目专门生成的原创示例。Before 保留原始画面内容，仅在接触表展示时进行居中裁切。除非某个 Narrative System 明确依赖空间蒙太奇，否则默认一张原片只生成一张独立 After。

| Before：原始旅行照片 | After：AI 复合 Memory Atlas |
| --- | --- |
| ![原始照片接触表](examples/outputs/before-source-photos.png) | ![真实建筑摄影与手绘记忆地图融合](examples/outputs/memory-atlas-ai-composite.png) |

[查看三层 Scene Cards](examples/generated-story.json) · [Prompt Manifest](examples/prompt-manifest.json) · [Render Manifest](examples/render-manifest.json) · [通过审核](examples/accepted-review.json)

### 案例 2 · Family Archive｜家庭档案

| Before：虚构人物纪实输入 | After：AI 复合家庭档案 |
| --- | --- |
| ![家庭档案原始接触表](examples/cases/family-archive/outputs/before.png) | ![人物纪实摄影与素描、档案材料融合](examples/cases/family-archive/outputs/family-archive-ai-composite.png) |

第二组案例把晾衣、包饺子、整理旧照片这些重复动作，读成一段跨代传递的照料记录。

[查看 Scene Cards](examples/cases/family-archive/story.json) · [Prompt Manifest](examples/cases/family-archive/prompt-manifest.json) · [Render Manifest](examples/cases/family-archive/render-manifest.json) · [通过审核](examples/cases/family-archive/accepted-review.json)

### 案例 3 · Cinematic Storyboard｜电影分镜

三张平淡的手机随手拍，分别变成三个独立电影镜头。它们通过“等待—停顿—离开”的光线与情绪弧线相连，而不是被拼进同一张版式。

| Before：构图失败的手机随手拍 | After：独立导演镜头 |
| --- | --- |
| ![普通公交站手机随手拍](examples/cases/cinematic-storyboard/photos/raw-bus-stop.png) | ![经过导演的雨夜公交站镜头](examples/cases/cinematic-storyboard/outputs/after-bus-stop.png) |
| ![普通小餐馆手机随手拍](examples/cases/cinematic-storyboard/photos/raw-diner.png) | ![隔着雨水观看餐馆的电影镜头](examples/cases/cinematic-storyboard/outputs/after-diner.png) |
| ![普通出租车手机随手拍](examples/cases/cinematic-storyboard/photos/raw-taxi.png) | ![出租车离开的电影镜头](examples/cases/cinematic-storyboard/outputs/after-taxi.png) |

[查看 Scene Cards](examples/cases/cinematic-storyboard/story.json) · [打开三条编译提示词](examples/cases/cinematic-storyboard/prompt-manifest.json) · [查看真实的失败 → 定向重试 → 通过记录](examples/cases/cinematic-storyboard/retry-example/README.md) · [查看原片接触表](examples/cases/cinematic-storyboard/outputs/before.png)

### 案例 4 · Minimal Editorial｜极简编辑

这个系统不会把三个物件贴到一张“设计稿”上，而是给每个普通物件一个独立摄影舞台，让材质、影子和留白承担叙事。

| Before：杂乱的家庭随手拍 | After：独立艺术书摄影 |
| --- | --- |
| ![普通杯子手机随手拍](examples/cases/minimal-editorial/photos/raw-mug.png) | ![同一杯子的安静编辑摄影](examples/cases/minimal-editorial/outputs/after-mug.png) |
| ![普通旧椅子手机随手拍](examples/cases/minimal-editorial/photos/raw-chair.png) | ![同一椅子的雕塑感编辑摄影](examples/cases/minimal-editorial/outputs/after-chair.png) |
| ![普通亚麻布手机随手拍](examples/cases/minimal-editorial/photos/raw-linen.png) | ![同一亚麻布的材质编辑摄影](examples/cases/minimal-editorial/outputs/after-linen.png) |

[查看 Scene Cards](examples/cases/minimal-editorial/story.json) · [编译提示词](examples/cases/minimal-editorial/prompt-manifest.json) · [Render Manifest](examples/cases/minimal-editorial/render-manifest.json) · [通过审核](examples/cases/minimal-editorial/accepted-review.json) · [查看原片接触表](examples/cases/minimal-editorial/outputs/before.png)

这里发生的不是简单滤镜或重新排版。系统先区分观察事实与解释，再分配故事角色、生成导演备注、推荐 Narrative System，最终既可以输出确定性 Workprint，也可以生成真正发生视觉二次创作的成品。空间与档案系统可以使用混合媒介；电影与极简系统默认“一张原片 → 一个独立镜头”。

### Editorial Sequence｜编辑序列

![编辑序列案例](examples/outputs/editorial-sequence.png)

让照片保持主体地位，通过留白、顺序和角色标签建立可阅读的摄影叙事。

### Memory Atlas｜记忆地图

![摄影与手绘融合的记忆地图案例](examples/outputs/memory-atlas-ai-composite.png)

适合旅程、距离、地点与空间记忆。真实建筑保持摄影质感，地点之间的地理空间则转化为手绘记忆；系统不会假设每段旅程都包含“归来”。

### Field Log｜现场日志

![现场日志案例](examples/outputs/field-log.png)

适合人物纪实、旅行观察、现场证据和克制的注释系统。

[查看原创样片](examples/photos) · [查看 Scene Cards](examples/generated-story.json) · [查看设计原则](DESIGN_PRINCIPLES.md)

## AI 视觉导演层

Scene Card 将信息明确分成三层：

- **Observation / 观察层**：记录照片中实际可见的主体、方向、色彩和安静区域。
- **Interpretation / 理解层**：记录暂定主题、情绪和置信度。
- **Direction / 导演层**：记录可编辑的故事角色、导演备注和版面重点。

这种拆分避免把 AI 的推测伪装成照片事实，也允许用户在编译 Prompt 前修改任何导演判断。自动分析保持克制，所有 Scene Card 决策都可以编辑。

## v0.3.2 · 可复核的生成合同

Prompt Compiler 将 Scene Card 证据、一个 Narrative System 与一个可替换的 Expression Profile 编译成版本化 JSON 生成合约。目前支持四个核心系统：`cinematic-storyboard`、`minimal-editorial`、`memory-atlas` 和 `family-archive`。System 决定故事如何被阅读，Profile 决定这种机制如何被视觉表达；默认使用 `source-led`。

每条编译提示词都固定包含十个模块：

1. 主体保真；
2. 明确的 `must_preserve` / `may_transform` / `must_remove`；
3. 叙事意图；
4. 构图；
5. 光线与色彩；
6. 材质与表面；
7. 空间关系；
8. 文字与标签策略；
9. 禁止项；
10. 输出比例与格式。

每条 Prompt 现在都带结构化 `output_contract`，明确 MIME、宽度、高度和比例。`bind-outputs` 会真实解码候选图片，格式或尺寸不符时在审核前直接失败。可选 `reference_output` 仅用于 Benchmark 对照；正式审核必须针对含有 `candidate_output` 的 Render Manifest。

序列系统还会检查人物一致性、光色连续性、节奏和整体叙事弧线。Retry 来源是一条完整哈希链：Prompt Manifest → 失败 Render Manifest → 失败审核 → Retry Manifest → 重试后 Render Manifest → 通过审核。每一段都记录父哈希和时间顺序。

## 不是风格菜单

项目通过“记录方式 / 表达机制”扩展，而不是堆叠复古、电影感、水彩等效果。适合扩展的方向包括：

- `family-archive`：家庭时间档案；
- `contact-sheet`：摄影选片与淘汰逻辑；
- `journey-sequence`：旅程与空间推进；
- `memory-atlas`：地点、物件和记忆连接；
- `field-log`：现场观察记录；
- `exhibition-label`：策展顺序和作品说明。

每个 Narrative System 都必须说明它承担了什么叙事工作，只有视觉关键词不算一个系统。

## 快速开始

需要 Python 3.10 及以上。自动分析和 PNG 输出需要 Pillow。

```bash
python -m pip install -e '.[images]'
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio recommend story.json
scene-card-studio compile story.json --system cinematic-storyboard --expression-profile source-led --output prompt-manifest.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
scene-card-studio bind-outputs prompt-manifest.json --result cinematic-storyboard-01=after-01.png --output render-manifest.json
scene-card-studio retry render-manifest.json assessment.json --output retry-manifest.json
scene-card-studio bind-outputs retry-manifest.json --result cinematic-storyboard-01=after-01-retry.png --output post-retry-render-manifest.json
scene-card-studio consent prompt-manifest.json --provider PROVIDER --purpose "presentation synthesis" --confirm --output upload-consent.json
```

电影与极简系统会为每张源图编译一条独立 Prompt；空间与档案系统会编译一条多源合成 Prompt。云端合成前必须记录 provider、用途和精确上传列表，并由用户明确确认；未同意时 Skill 只生成本地 Workprint 与 Prompt Manifest。正式审核拒绝未经绑定的 Prompt Manifest。SVG 安全嵌入会完整解码并重新编码图片、清除尾随数据与元数据，并限制源文件字节数和像素数。版面默认使用 `presentation`；需要查看观察、理解、角色和导演备注时使用 `--mode workprint`。

## Codex Skill

将 `skills/scene-card-studio` 复制到 Codex Skills 目录并重启，然后输入：

```text
使用 $scene-card-studio 把这些照片编排成一组安静的家庭视觉档案。
```

## 原创与隐私

- 不捆绑第三方风格参考资产；
- 不复制其他同类仓库的提示词；
- 示例图片均为项目新生成的原创演示素材；
- 核心创新是 Scene Card、Visual Director 与叙事渲染工作流；
- 除非用户明确选择，否则原始照片只在本地处理。

版本化来源记录见 [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)，逐资产使用条款见 [examples/ASSET_LICENSE.md](examples/ASSET_LICENSE.md)。

## 路线图

- 可由用户修改的视觉导演判断；
- `contact-sheet`、`journey-sequence`；
- 主体感知裁切；
- 图像模型适配器与生成队列；
- 可打印 PDF 与社交媒体卡片；
- 浏览器预览和拖拽排序；
- 社区 Narrative System 插件。

## 许可证

代码与本仓库专用演示素材采用 Apache-2.0；随包字体仍采用 SIL OFL 1.1。详见 [示例资产条款](examples/ASSET_LICENSE.md)。
