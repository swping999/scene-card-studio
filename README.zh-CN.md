<h1 align="center">Scene Card Studio｜场景卡片工作室</h1>

<p align="center"><strong>把个人照片转化为结构化、可编辑视觉叙事的 AI 视觉导演。</strong></p>

<p align="center">
  <a href="https://github.com/swping999/scene-card-studio/releases/tag/v0.4.2"><img alt="版本 0.4.2" src="https://img.shields.io/badge/version-0.4.2-315c8c?style=flat-square"></a>
  <a href="https://github.com/swping999/scene-card-studio/actions/workflows/ci.yml"><img alt="持续集成" src="https://img.shields.io/github/actions/workflow/status/swping999/scene-card-studio/ci.yml?branch=main&style=flat-square&label=tests"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-315c8c?style=flat-square">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827?style=flat-square">
  <a href="LICENSE"><img alt="Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-315c8c?style=flat-square"></a>
</p>

<p align="center">中文 · <a href="README.md">English</a></p>

[![Scene Card Studio 开场视频](docs/media/scene-card-studio-opening.gif)](docs/media/scene-card-studio-opening.mp4)

▶ [播放 6 秒开场视频](docs/media/scene-card-studio-opening.mp4)

> **这不是一个照片风格转换工具，而是一套基于 Scene Card 的个人照片视觉叙事引擎。**

Scene Card Studio 将照片中可观察的事实转化为可编辑叙事决策、版本化生成提示词、导演成片和确定性版面。它不只问“照片应该变成什么风格”，而是先判断“这段故事应该如何被阅读”。

```text
照片 → Scene Cards → Narrative System → Prompt Compiler → 图像生成 → 审美检查 → 重试 / 接受
```

| 项目速览 | 明确约定 |
| --- | --- |
| 输入 | 单张照片或一组有关联的照片序列 |
| 导演方式 | 可观察事实 → 可编辑解释 → 明确视觉导演决策 |
| 视觉词汇 | 10 个 Narrative Systems + 3 个可替换 Expression Profiles |
| 输出 | 本地 Workprint、版本化 Prompt、经过合同检查的图像、确定性文字层与审核记录 |
| 隐私 | 默认本地分析；上传云端前必须确认服务商、用途和准确文件清单 |

**快速导航：**[Before / After](#before--after-首页案例) · [视觉导演层](#ai-视觉导演层) · [Systems 与 Profiles](#v040--叙事系统表达-profile-与确定性文字) · [快速开始](#快速开始) · [参与贡献](CONTRIBUTING.md)

### 单张或多张都可以

- **一张照片 → 一张经过导演的独立成片。** 为它选择兼容的 Narrative System 和 Expression Profile，输出一组独立 Before/After；不会强迫单张照片变成接触表、序列或装饰拼贴。
- **多张照片 → 一个连贯故事。** 每张都需要独立 After 时使用逐张导演；地点、旅程或重复关系需要进入同一画面时，选择多源合成系统。
- **表达风格可以编辑。** Narrative System 决定照片或故事如何被阅读，Expression Profile 决定画面如何表达。因此单张照片也能使用 `source-led`、`watercolor-chronicle`、`heritage-portrait`、`dream-logic`，或所选系统支持的其他 Profile。

## Before / After 首页案例

下面每一张 Before 都是为本项目重新生成的、刻意保留普通手机随手拍问题的原创输入；每一张 After 都对同一主体进行了实质视觉导演，不是给原图加边框、接触表或装饰拼贴。案例人物均为 AI 生成的虚构人物。

### 1 · Cinematic Sequence｜电影序列

| Before · 平淡的高架桥随手拍 | After · 雨、动机光与镜头空间重新导演 |
| --- | --- |
| ![普通高架桥人物随手拍](examples/cases/v0.4-gallery/before/cinematic-sequence.jpg) | ![电影感雨夜独立镜头](examples/cases/v0.4-gallery/after/cinematic-sequence.jpg) |

### 2 · Memory Atlas｜记忆地图

| Before · 路边真实建筑 | After · 建筑摄影与手绘地形在同一空间融合 |
| --- | --- |
| ![普通路边建筑](examples/cases/v0.4-gallery/before/memory-atlas.jpg) | ![现实建筑与水彩地理融合](examples/cases/v0.4-gallery/after/memory-atlas.jpg) |

### 3 · Family Chronicle｜家庭纪事

| Before · 杂乱的家庭随手拍 | After · 人物摄影、手部素描与动作线索统一成像 |
| --- | --- |
| ![普通叠衣服家庭照片](examples/cases/v0.4-gallery/before/family-chronicle.jpg) | ![经过导演的家庭纪事](examples/cases/v0.4-gallery/after/family-chronicle.jpg) |

### 4 · Quiet Editorial｜安静编辑

| Before · 杂乱的水壶照片 | After · 材质、光线与留白主导的静物 |
| --- | --- |
| ![普通水壶随手拍](examples/cases/v0.4-gallery/before/quiet-editorial.jpg) | ![安静编辑水壶摄影](examples/cases/v0.4-gallery/after/quiet-editorial.jpg) |

### 5 · Editorial Rhythm｜编辑节奏

| Before · 偶然摆放的塑料椅 | After · 色彩、间距、裁切与影子形成节奏 |
| --- | --- |
| ![普通塑料椅照片](examples/cases/v0.4-gallery/before/editorial-rhythm.jpg) | ![经过导演的椅子节奏](examples/cases/v0.4-gallery/after/editorial-rhythm.jpg) |

### 6 · Field Log｜现场日志

| Before · 随手拍的修车现场 | After · 保留事实的克制观察记录 |
| --- | --- |
| ![普通自行车维修照片](examples/cases/v0.4-gallery/before/field-log.jpg) | ![现场日志纪实摄影](examples/cases/v0.4-gallery/after/field-log.jpg) |

### 7 · Watercolor Chronicle｜水彩纪事

| Before · 普通海边人物照 | After · 人物、衣服、物件与环境全部统一水彩化 |
| --- | --- |
| ![普通海边人物照](examples/cases/v0.4-gallery/before/watercolor-chronicle.jpg) | ![全画面水彩纪事](examples/cases/v0.4-gallery/after/watercolor-chronicle.jpg) |

### 8 · Heritage Portrait｜传统影像肖像

| Before · 普通阅读角随手拍 | After · 柔和银盐质感与手工着色肖像 |
| --- | --- |
| ![普通年轻女性肖像](examples/cases/v0.4-gallery/before/heritage-portrait.jpg) | ![传统影像肖像](examples/cases/v0.4-gallery/after/heritage-portrait.jpg) |

### 9 · Museum Catalogue｜博物馆图录

| Before · 杂物间里的旧物 | After · 可检查的藏品记录摄影 |
| --- | --- |
| ![杂乱环境中的旧收音机](examples/cases/v0.4-gallery/before/museum-catalogue.jpg) | ![博物馆图录收音机](examples/cases/v0.4-gallery/after/museum-catalogue.jpg) |

### 10 · Travel Journal｜旅行日志

| Before · 站台等待随手拍 | After · 站台空间转化为有触感的路线场 |
| --- | --- |
| ![普通站台行李箱](examples/cases/v0.4-gallery/before/travel-journal.jpg) | ![连续空间旅行日志](examples/cases/v0.4-gallery/after/travel-journal.jpg) |

### 11 · Street Reportage｜街头纪实

| Before · 松散的雨天路口照片 | After · 决定性黑白公共生活镜头 |
| --- | --- |
| ![普通雨天路口随手拍](examples/cases/v0.4-gallery/before/street-reportage.jpg) | ![黑白街头纪实](examples/cases/v0.4-gallery/after/street-reportage.jpg) |

### 12 · Fashion Editorial｜时装编辑

| Before · 普通商场人物照 | After · 由服装与建筑关系主导的编辑镜头 |
| --- | --- |
| ![普通商场人物照](examples/cases/v0.4-gallery/before/fashion-editorial.jpg) | ![时装编辑摄影](examples/cases/v0.4-gallery/after/fashion-editorial.jpg) |

### 13 · Dream Logic｜梦境逻辑

| Before · 小孩与一只风筝 | After · 只引入一条可信的不可能规则，并锁定人物身份 |
| --- | --- |
| ![普通盐湖风筝照片](examples/cases/v0.4-gallery/before/dream-logic.jpg) | ![单风筝梦境逻辑改造](examples/cases/v0.4-gallery/after/dream-logic.jpg) |

前十项是 Narrative Systems；Watercolor Chronicle、Heritage Portrait 与 Dream Logic 是通过兼容系统使用的可替换 Expression Profiles。这样能把“故事如何被阅读”与“画面表面如何表达”分开。

[查看 13 份 Scene Card 与导演记录](examples/cases/v0.4-gallery/case-records.json) · [阅读案例说明](examples/cases/v0.4-gallery/README.md) · [查看设计原则](DESIGN_PRINCIPLES.md)

## 之前的基准案例

原有案例继续完整保留在仓库中，对应的 Manifest、输出绑定、审核和重试记录均未删除。

### 原始 Memory Atlas 基准案例

| Before：原始旅行照片 | After：AI 复合 Memory Atlas |
| --- | --- |
| ![原始照片接触表](examples/outputs/before-source-photos.png) | ![真实建筑摄影与手绘记忆地图融合](examples/outputs/memory-atlas-ai-composite.png) |

[Scene Cards](examples/generated-story.json) · [Prompt Manifest](examples/prompt-manifest.json) · [Render Manifest](examples/render-manifest.json) · [通过审核](examples/accepted-review.json)

### 原始 Family Archive 基准案例

| Before：虚构人物纪实输入 | After：AI 复合家庭档案 |
| --- | --- |
| ![家庭档案原始接触表](examples/cases/family-archive/outputs/before.png) | ![人物纪实摄影与素描、档案材料融合](examples/cases/family-archive/outputs/family-archive-ai-composite.png) |

[Scene Cards](examples/cases/family-archive/story.json) · [Prompt Manifest](examples/cases/family-archive/prompt-manifest.json) · [Render Manifest](examples/cases/family-archive/render-manifest.json) · [通过审核](examples/cases/family-archive/accepted-review.json)

### 原始 Cinematic Storyboard 基准案例

| Before：构图失败的手机随手拍 | After：独立导演镜头 |
| --- | --- |
| ![普通公交站手机随手拍](examples/cases/cinematic-storyboard/photos/raw-bus-stop.png) | ![经过导演的雨夜公交站镜头](examples/cases/cinematic-storyboard/outputs/after-bus-stop.png) |
| ![普通小餐馆手机随手拍](examples/cases/cinematic-storyboard/photos/raw-diner.png) | ![隔着雨水观看餐馆的电影镜头](examples/cases/cinematic-storyboard/outputs/after-diner.png) |
| ![普通出租车手机随手拍](examples/cases/cinematic-storyboard/photos/raw-taxi.png) | ![出租车离开的电影镜头](examples/cases/cinematic-storyboard/outputs/after-taxi.png) |

[Scene Cards](examples/cases/cinematic-storyboard/story.json) · [编译提示词](examples/cases/cinematic-storyboard/prompt-manifest.json) · [失败 → 定向重试 → 通过记录](examples/cases/cinematic-storyboard/retry-example/README.md) · [原片接触表](examples/cases/cinematic-storyboard/outputs/before.png)

### 原始 Minimal Editorial 基准案例

| Before：杂乱的家庭随手拍 | After：独立艺术书摄影 |
| --- | --- |
| ![普通杯子手机随手拍](examples/cases/minimal-editorial/photos/raw-mug.png) | ![同一杯子的安静编辑摄影](examples/cases/minimal-editorial/outputs/after-mug.png) |
| ![普通旧椅子手机随手拍](examples/cases/minimal-editorial/photos/raw-chair.png) | ![同一椅子的雕塑感编辑摄影](examples/cases/minimal-editorial/outputs/after-chair.png) |
| ![普通亚麻布手机随手拍](examples/cases/minimal-editorial/photos/raw-linen.png) | ![同一亚麻布的材质编辑摄影](examples/cases/minimal-editorial/outputs/after-linen.png) |

[Scene Cards](examples/cases/minimal-editorial/story.json) · [编译提示词](examples/cases/minimal-editorial/prompt-manifest.json) · [Render Manifest](examples/cases/minimal-editorial/render-manifest.json) · [通过审核](examples/cases/minimal-editorial/accepted-review.json) · [原片接触表](examples/cases/minimal-editorial/outputs/before.png)

## AI 视觉导演层

Scene Card 将信息明确分成三层：

- **Observation / 观察层**：记录照片中实际可见的主体、方向、色彩和安静区域。
- **Interpretation / 理解层**：记录暂定主题、情绪和置信度。
- **Direction / 导演层**：记录可编辑的故事角色、导演备注和版面重点。

这种拆分避免把 AI 的推测伪装成照片事实，也允许用户在编译 Prompt 前修改任何导演判断。自动分析保持克制，所有 Scene Card 决策都可以编辑。

## v0.4.0 · 叙事系统、表达 Profile 与确定性文字

Prompt Compiler 将 Scene Card 证据、一个 Narrative System 与一个可替换的 Expression Profile 编译成版本化 JSON 生成合约。目前支持十个 Narrative System。System 决定故事如何被阅读，Profile 决定这种机制如何被视觉表达；默认仍为 `source-led`。

| Narrative System | 展示名称 | 阅读机制 |
| --- | --- | --- |
| `cinematic-storyboard` | Cinematic Sequence | 时间连续、动机光线与镜头关系 |
| `memory-atlas` | Memory Atlas | 地点、距离、方向与空间记忆 |
| `family-archive` | Family Chronicle | 用户提供的人物、物件、动作与时间关系 |
| `minimal-editorial` | Quiet Editorial | 层级、留白、光线与材质节奏 |
| `editorial-sequence` | Editorial Rhythm | 顺序、尺度、对比、密度与停顿 |
| `field-log` | Field Log | 可观察证据与纪实语境 |
| `museum-catalogue` | Museum Catalogue | 可检查的图录画面与用户提供的藏品信息 |
| `travel-journal` | Travel Journal | 移动、停顿、门槛与用户提供的旅行证据 |
| `street-reportage` | Street Reportage | 公共空间中的真实动作与事实序列 |
| `fashion-editorial` | Fashion Editorial | 姿势、服装结构、裁切与镜头尺度节奏 |

可复用 Profile 包括 `watercolor-chronicle`、`heritage-portrait` 和约束更严格、锁定人物身份的 `dream-logic`。v0.3.3 的 `full-watercolor-memory` 在 Memory Atlas 中继续作为 `watercolor-chronicle` 的兼容别名。

所有可见文字现已移出图片生成阶段。Manifest 会提供 `presentation_contract`，`scene-card-studio present` 只把用户提供的标题、日期、地点、收藏名称和藏品编号确定性地排进 SVG；缺失信息直接省略，不进行猜测。

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

项目通过“记录方式 / 表达机制”扩展，而不是堆叠复古、电影感、水彩等效果。水彩、传统影像工艺、黑白处理和 Dream Logic 都属于可替换 Profile。每个 Narrative System 都必须说明它承担了什么叙事工作，只有视觉关键词不算一个系统。

## 快速开始

需要 Python 3.10 及以上。自动分析和 PNG 输出需要 Pillow。

```bash
git clone https://github.com/swping999/scene-card-studio.git
cd scene-card-studio
python -m pip install -e '.[images]'

# 单张照片 → 一张独立导演成片
scene-card-studio analyze photos/portrait.jpg --output portrait-story.json
scene-card-studio compile portrait-story.json --system family-archive --expression-profile heritage-portrait --output portrait-manifest.json

# 多张照片 → 逐张导演或多源叙事合成
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio recommend story.json
scene-card-studio compile story.json --system cinematic-storyboard --expression-profile source-led --output prompt-manifest.json
scene-card-studio compile story.json --system memory-atlas --expression-profile watercolor-chronicle --output watercolor-memory-manifest.json
scene-card-studio compile story.json --system museum-catalogue --expression-profile heritage-portrait --output catalogue-manifest.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
scene-card-studio bind-outputs prompt-manifest.json --result cinematic-storyboard-01=after-01.png --output render-manifest.json
scene-card-studio present render-manifest.json --output presentation.svg
scene-card-studio retry render-manifest.json assessment.json --output retry-manifest.json
scene-card-studio bind-outputs retry-manifest.json --result cinematic-storyboard-01=after-01-retry.png --output post-retry-render-manifest.json
scene-card-studio consent prompt-manifest.json --provider PROVIDER --purpose "presentation synthesis" --confirm --output upload-consent.json
```

电影、Quiet Editorial、Editorial Rhythm、Field Log、Museum、Street 与 Fashion 系统会为每张源图编译独立 Prompt；Memory Atlas、Family Chronicle 和 Travel Journal 使用多源合成。云端合成前必须记录 provider、用途和精确上传列表并由用户明确确认。正式审核拒绝未经绑定的 Prompt Manifest。`present` 会核验候选图片哈希，并让生成图像与确定性文字保持独立来源层。SVG 安全嵌入仍会完整解码和重编码源图、清除尾随数据与元数据，并限制字节数和像素数。

## Codex Skill

克隆仓库后，将内置 Skill 复制到 Codex Skills 目录并重启 Codex：

```bash
mkdir -p ~/.codex/skills
cp -R skills/scene-card-studio ~/.codex/skills/
```

然后输入：

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

## 参与贡献与安全报告

新的 Narrative System 必须提出一种不同的照片序列阅读机制；新的 Expression Profile 必须可以替换，不得模仿具名创作者，也不得复用第三方视觉资产。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果发现路径穿越、照片意外泄露、Manifest 伪造、不安全图像处理、Prompt Injection 或凭证暴露，请通过仓库的私密安全报告渠道提交，详见 [SECURITY.md](SECURITY.md)。

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

版本记录见 [CHANGELOG.md](CHANGELOG.md)。
