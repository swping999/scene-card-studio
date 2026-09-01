<h1 align="center">Scene Card Studio｜场景卡片工作室</h1>

<p align="center"><strong>把个人照片转化为结构化、可编辑视觉叙事的 AI 视觉导演。</strong></p>

<p align="center">
  <a href="https://github.com/swping999/scene-card-studio/releases/tag/v0.5.0"><img alt="版本 0.5.0" src="https://img.shields.io/badge/version-0.5.0-315c8c?style=flat-square"></a>
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

### 一条命令开始

完成安装后，一条本地命令就能把单张照片或一组相关照片整理为草稿 Scene Cards、自动路由后的 Prompt Manifest、明确标注为分析稿的 Workprint，以及运行摘要：

```bash
scene-card-studio direct photos/portrait.jpg \
  --brief "克制银盐与手工着色的传统影像肖像"
```

多张照片可以直接传入多个路径或使用通配符。`direct` 会根据中英文 Brief 推荐 Narrative System；只有 Brief 明确要求某种视觉表达时才会自动选择非默认 Expression Profile。本地分析器只测量尺寸、方向、调色板、亮度和饱和度，**不会假装这些统计已经识别出人物、物件、动作或空间含义**。语义字段和变换规则补齐前，导演包会标记为 `needs-semantic-direction`，并拒绝创建上传同意记录。这个准备步骤不会上传源照片，也不会把 Workprint 冒充生成完成的 After。

| 项目速览 | 明确约定 |
| --- | --- |
| 输入 | 单张照片或一组有关联的照片序列 |
| 导演方式 | 可观察事实 → 可编辑解释 → 明确视觉导演决策 |
| 视觉词汇 | 11 个 Narrative Systems + 18 个可替换 Expression Profiles |
| 输出 | 本地 Workprint、版本化 Prompt、经过合同检查的图像、确定性文字层与审核记录 |
| 隐私 | 默认本地分析；上传云端前必须确认服务商、用途和准确文件清单 |

**快速导航：**[Before / After](#before--after-首页案例) · [视觉导演层](#ai-视觉导演层) · [Systems 与 Profiles](#当前叙事系统表达-profile-与确定性文字) · [快速开始](#快速开始) · [参与贡献](CONTRIBUTING.md)

### 单张或多张都可以

- **一张照片 → 一张经过导演的独立成片。** 为它选择兼容的 Narrative System 和 Expression Profile，输出一组独立 Before/After；不会强迫单张照片变成接触表、序列或装饰拼贴。
- **多张照片 → 一个连贯故事。** 每张都需要独立 After 时使用逐张导演；地点、旅程或重复关系需要进入同一画面时，选择多源合成系统。
- **表达风格可以编辑。** Narrative System 决定照片或故事如何被阅读，Expression Profile 决定画面如何表达。因此单张照片也能使用 `source-led`、`watercolor-chronicle`、`heritage-portrait`、`dream-logic`，或所选系统支持的其他 Profile。

运行 `scene-card-studio profiles` 可以查看兼容组合。每份 Manifest 都会明确记录 `single-photo`、`multi-photo-per-source` 或 `multi-photo-synthesis`，防止后续工具悄悄改变用户选择的源图模式。

## Before / After 首页案例

### 风景主导的新扩展

这批案例刻意以风景和物件为主，不再依赖普通人物照。每张 Before 都是新生成的日常输入，每张 After 都通过一种独立的叙事或材质系统，实质重建同一份可见证据。首个 Journey Taxonomy 案例把地点按移动、地标、水体、植物、天气和材质组织在同一空间中；它明确不复制参考图的配色、上下重复照片、贴纸竖排、白色描边、连接线与标题位置。

#### Journey Taxonomy｜旅行地点分类

| Before · 普通盐沼风景 | After · 一个语义地点场，不是贴纸板 |
| --- | --- |
| ![普通盐沼木栈道](examples/cases/v0.6-gallery/before/salt-marsh-boardwalk.png) | ![旅行地点分类景观](examples/cases/v0.6-gallery/after/journey-taxonomy.png) |

#### Mineral Ink Memory｜矿物色水墨记忆

| Before · 杂乱的冬季石桥 | After · 连续的矿物颜料与墨色空间 |
| --- | --- |
| ![普通冬季石桥](examples/cases/v0.6-gallery/before/stone-bridge.png) | ![矿物色水墨石桥记忆](examples/cases/v0.6-gallery/after/mineral-ink-memory.png) |

#### Impasto Light Study｜厚涂光线研究

| Before · 平淡阴天湖面 | After · 用真实颜料厚度组织光线 |
| --- | --- |
| ![普通山湖随手拍](examples/cases/v0.6-gallery/before/mountain-lake.png) | ![厚涂山湖光线研究](examples/cases/v0.6-gallery/after/impasto-light-study.png) |

#### Pixel Diary｜像素日记

| Before · 空荡市场小巷 | After · 统一像素网格与空间层次 |
| --- | --- |
| ![普通空市场小巷](examples/cases/v0.6-gallery/before/empty-market-lane.png) | ![像素日记市场小巷](examples/cases/v0.6-gallery/after/pixel-diary.png) |

#### Risograph Route｜孔版印刷路线

| Before · 盐沼中的真实路线 | After · 限色油墨构成的路线节奏 |
| --- | --- |
| ![普通盐沼路线](examples/cases/v0.6-gallery/before/salt-marsh-boardwalk.png) | ![孔版印刷路线画面](examples/cases/v0.6-gallery/after/risograph-route.png) |

#### Gouache Place Study｜水粉地点研究

| Before · 生硬的高地随手拍 | After · 不透明、哑光的地点绘画 |
| --- | --- |
| ![普通高地天文台](examples/cases/v0.6-gallery/before/highland-observatory.png) | ![水粉天文台地点研究](examples/cases/v0.6-gallery/after/gouache-place-study.png) |

#### Cyanotype Archive｜蓝晒档案

| Before · 杂乱野外工作台 | After · 与真实证据绑定的接触印相 |
| --- | --- |
| ![桌面上的普通野外物件](examples/cases/v0.6-gallery/before/field-desk.png) | ![蓝晒野外物件档案](examples/cases/v0.6-gallery/after/cyanotype-archive.png) |

#### Paper Relief Landscape｜纸艺浮雕景观

| Before · 扁平冬季地形 | After · 物理结构一致的纸艺浮雕 |
| --- | --- |
| ![普通石桥与梯田](examples/cases/v0.6-gallery/before/stone-bridge.png) | ![剪纸浮雕景观](examples/cases/v0.6-gallery/after/paper-relief-landscape.png) |

#### Autochrome Memory｜早期彩色摄影记忆

| Before · 普通湖边停留 | After · 克制的早期彩色材料记忆 |
| --- | --- |
| ![普通山湖与小船](examples/cases/v0.6-gallery/before/mountain-lake.png) | ![早期彩色摄影质感湖面记忆](examples/cases/v0.6-gallery/after/autochrome-memory.png) |

#### Pixel + Ink Memory｜像素与水墨记忆 · 实验

| Before · 单一摄影表面 | After · 近景像素、远景水墨 |
| --- | --- |
| ![普通空市场小巷](examples/cases/v0.6-gallery/before/empty-market-lane.png) | ![像素与水墨市场记忆](examples/cases/v0.6-gallery/after/pixel-ink-memory.png) |

#### Sculpted Place Diorama｜立体地点微缩模型 · 3D

| Before · 扁平风景照片 | After · 真实体积、地形与接触阴影 |
| --- | --- |
| ![普通盐沼木栈道](examples/cases/v0.6-gallery/before/salt-marsh-boardwalk.png) | ![立体盐沼微缩地景](examples/cases/v0.6-gallery/after/sculpted-place-diorama.png) |

[查看 11 份 Scene Card](examples/cases/v0.6-gallery/case-records.json) · [打开可复编译证据索引](examples/cases/v0.6-gallery/evidence/index.json) · [阅读原创性与案例说明](examples/cases/v0.6-gallery/README.md)

## 之前的 v0.4 Before / After

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

[查看 13 份 Scene Card 与导演记录](examples/cases/v0.4-gallery/case-records.json) · [打开可复编译证据索引](examples/cases/v0.4-gallery/evidence/index.json) · [阅读案例说明](examples/cases/v0.4-gallery/README.md) · [查看设计原则](DESIGN_PRINCIPLES.md)

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

## 当前叙事系统、表达 Profile 与确定性文字

Prompt Compiler 将 Scene Card 证据、一个 Narrative System 与一个可替换的 Expression Profile 编译成版本化 JSON 生成合约。目前支持十一个 Narrative System。System 决定故事如何被阅读，Profile 决定这种机制如何被视觉表达；默认仍为 `source-led`。

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
| `journey-taxonomy` | Journey Taxonomy | 把可见地点证据按语义组织为一个完整空间场 |
| `street-reportage` | Street Reportage | 公共空间中的真实动作与事实序列 |
| `fashion-editorial` | Fashion Editorial | 姿势、服装结构、裁切与镜头尺度节奏 |

除默认 `source-led` 外，现在有 18 个可替换 Profile。新增的十种材质语言包括矿物色水墨、厚涂、手工像素、孔版印刷、水粉、蓝晒、纸艺浮雕、早期彩色摄影、像素水墨融合，以及具有真实体积的 3D 微缩地景。`pixel-ink-memory` 明确标为实验功能。v0.3.3 的 `full-watercolor-memory` 在 Memory Atlas 中继续作为 `watercolor-chronicle` 的兼容别名，不重复计数。

| Expression Profile | 兼容的 Narrative Systems |
| --- | --- |
| `source-led` | 全部系统 |
| `rain-nocturne` | Cinematic Sequence |
| `quiet-window-light` | Quiet Editorial |
| `watercolor-contour` | Memory Atlas |
| `watercolor-chronicle` | Memory Atlas、Family Chronicle、Museum Catalogue、Travel Journal |
| `graphite-paper` | Family Chronicle |
| `heritage-portrait` | Family Chronicle、Museum Catalogue |
| `monochrome-reportage` | Street Reportage |
| `dream-logic` | Memory Atlas、Fashion Editorial |
| `mineral-ink-memory` | Memory Atlas、Travel Journal、Journey Taxonomy |
| `impasto-light-study` | Quiet Editorial、Memory Atlas、Travel Journal、Journey Taxonomy |
| `pixel-diary` | Memory Atlas、Travel Journal、Journey Taxonomy |
| `risograph-route` | Memory Atlas、Travel Journal、Journey Taxonomy |
| `gouache-place-study` | Memory Atlas、Travel Journal、Journey Taxonomy |
| `cyanotype-archive` | Field Log、Family Chronicle、Museum Catalogue、Street Reportage |
| `paper-relief-landscape` | Memory Atlas、Travel Journal、Journey Taxonomy |
| `autochrome-memory` | Memory Atlas、Family Chronicle、Travel Journal、Journey Taxonomy |
| `pixel-ink-memory` · 实验 | Memory Atlas、Journey Taxonomy |
| `sculpted-place-diorama` · 3D | Memory Atlas、Travel Journal、Journey Taxonomy |

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

每条 Prompt 现在都带结构化 `output_contract`，明确 MIME、宽度、高度和比例。`bind-outputs` 会真实解码候选图片，格式或尺寸不符时在审核前直接失败。候选图片路径会相对于 Render Manifest 保存，整个目录可以迁移；正式审核还会重新打开并计算当前文件哈希，绑定后替换图片会使审核失败。可选 `reference_output` 仅用于 Benchmark 对照；正式审核必须针对含有 `candidate_output` 的 Render Manifest。

序列系统还会检查人物一致性、光色连续性、节奏和整体叙事弧线。Retry 来源是一条完整哈希链：Prompt Manifest → 失败 Render Manifest → 失败审核 → Retry Manifest → 重试后 Render Manifest → 通过审核。每一段都记录父哈希和时间顺序。

## 不是风格菜单

项目通过“记录方式 / 表达机制”扩展，而不是堆叠复古、电影感、水彩等效果。水彩、传统影像工艺、黑白处理和 Dream Logic 都属于可替换 Profile。每个 Narrative System 都必须说明它承担了什么叙事工作，只有视觉关键词不算一个系统。

## 快速开始

需要 Python 3.10 及以上。自动分析和 PNG 输出需要 Pillow。

```bash
git clone https://github.com/swping999/scene-card-studio.git
cd scene-card-studio
python -m pip install -e .

# 快速路径：单张照片 → 本地 Prompt-ready 导演包
scene-card-studio direct photos/portrait.jpg --brief "安静家庭肖像，使用克制银盐层次"

# 本地分析器会在虚构语义证据之前主动停止
scene-card-studio check scene-card-output/story.json --json

# 由人工或具备视觉能力的 Skill 补全并核验 Scene Cards 后：
scene-card-studio direct photos/portrait.jpg \
  --brief "安静家庭肖像，使用克制银盐层次" \
  --scene-cards scene-card-output/story.json --force

# 快速路径：多张照片 → 自动推荐的叙事导演包
scene-card-studio direct photos/*.jpg --brief "由车站、票据和门槛构成的旅行日志" --output-dir travel-run

# 需要逐步控制时使用以下高级流程
scene-card-studio analyze photos/portrait.jpg --output portrait-story.json
# 必须依据可见证据补齐这里列出的语义字段，再编译生成 Prompt
scene-card-studio check portrait-story.json --json
scene-card-studio profiles --system family-archive
scene-card-studio compile portrait-story.json --system family-archive --expression-profile heritage-portrait --output portrait-manifest.json

# 多张照片 → 逐张导演或多源叙事合成
scene-card-studio analyze photos/*.jpg --output story.json
scene-card-studio check story.json --json
scene-card-studio recommend story.json
scene-card-studio compile story.json --system cinematic-storyboard --expression-profile source-led --output prompt-manifest.json
scene-card-studio compile story.json --system memory-atlas --expression-profile watercolor-chronicle --output watercolor-memory-manifest.json
scene-card-studio compile story.json --system museum-catalogue --expression-profile heritage-portrait --output catalogue-manifest.json
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
scene-card-studio consent prompt-manifest.json --provider PROVIDER --purpose "presentation synthesis" --confirm --output upload-consent.json
scene-card-studio bind-outputs prompt-manifest.json --result cinematic-storyboard-01=after-01.png --output render-manifest.json
scene-card-studio review-template render-manifest.json --reviewer-type human --reviewer-name "你的名字" --reviewer-model "visual inspection" --method "full-resolution comparison" --output assessment.json
# 检查已绑定图片并填写全部 1–5 分，再生成正式审核记录：
scene-card-studio review render-manifest.json assessment.json --output review.json
scene-card-studio present render-manifest.json --output presentation.svg
scene-card-studio retry render-manifest.json review.json --output retry-manifest.json
scene-card-studio bind-outputs retry-manifest.json --result cinematic-storyboard-01=after-01-retry.png --output post-retry-render-manifest.json
```

`direct` 会在独立输出目录中写入 `story.json`、`prompt-manifest.json`、`workprint.svg` 和 `run-summary.json`；除非明确传入 `--force`，否则拒绝覆盖已有运行结果。`check` 会列出尚未补齐的语义字段。准备完成的 Story 可以通过 `--scene-cards` 重新进入同一流程；它的源图列表必须与命令中提供的照片完全一致，低级图像测量值也会根据真实文件重新计算。输入单张照片时，所有系统都只编译一条独立 Prompt，并把 Manifest 标记为 `single-photo`；不会要求序列连续，也不会虚构相邻场景。输入多张照片时，电影、Quiet Editorial、Editorial Rhythm、Field Log、Museum、Street 与 Fashion 会为每张源图编译独立 Prompt；Memory Atlas、Family Chronicle、Travel Journal 和 Journey Taxonomy 则编译一条多源合成 Prompt。

云端合成前必须记录 provider、用途和精确上传列表并由用户明确确认；缺少或未完成的方向就绪证据会默认拒绝。正式审核拒绝未经绑定的 Prompt Manifest，`retry` 也拒绝未完成或已经通过的审核。`present` 会核验候选图片哈希、写入可迁移的相对引用，并让生成图像与确定性文字保持独立来源层。图片分析、输出绑定和 SVG 安全嵌入都会限制字节数与像素数。

仓库同时提供包含正向、否定与歧义表达的[中英文路由矩阵](evals/direct-briefs.json)。CI 会检查全部十一个 Narrative System、全部非默认 Profile、单图合同、多图模式、语义就绪状态、正式审核、Retry 来源链、安全图片嵌入、首页案例可复编译证据，以及每组已发布 Before/After 的像素级视觉差异。

## Codex Skill

Codex Skill 同时包含在源码和 Wheel 安装包中。将它安装到一个新的 Codex Skill 目录，然后重启 Codex：

```bash
scene-card-studio skill-path
scene-card-studio install-skill --target ~/.codex/skills/scene-card-studio
```

安装命令不会覆盖已有 Skill 目录。

然后输入：

```text
使用 $scene-card-studio 把这张照片导演成克制手工着色的传统影像肖像。
```

Skill 会先使用同一套本地 `direct` 流程生成可检查的导演包，通过视觉检查补齐语义 Scene Card 并用 `check` 验证；只有在用户确认服务商、用途与具体文件后，才继续远程图像生成。

## 原创与隐私

- 不捆绑第三方风格参考资产；
- 不复制其他同类仓库的提示词；
- 示例图片均为项目新生成的原创演示素材；
- 核心创新是 Scene Card、Visual Director 与叙事渲染工作流；
- 除非用户明确选择，否则原始照片只在本地处理。

版本化来源记录见 [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)，逐资产使用条款见 [examples/ASSET_LICENSE.md](examples/ASSET_LICENSE.md)。

## 参与贡献与安全报告

新的 Narrative System 必须提出一种不同的单图或照片序列阅读机制；新的 Expression Profile 必须可以替换，不得模仿具名创作者，也不得复用第三方视觉资产。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果发现路径穿越、照片意外泄露、Manifest 伪造、不安全图像处理、Prompt Injection 或凭证暴露，请通过仓库的私密安全报告渠道提交，详见 [SECURITY.md](SECURITY.md)。

## 路线图

- 超越内置 Skill 流程的更多语义图像适配器；
- `contact-sheet`、`journey-sequence`；
- 主体感知裁切；
- 图像模型适配器与生成队列；
- 可打印 PDF 与社交媒体卡片；
- 浏览器预览和拖拽排序；
- 社区 Narrative System 插件。

## 许可证

代码与本仓库专用演示素材采用 Apache-2.0；随包字体仍采用 SIL OFL 1.1。详见 [示例资产条款](examples/ASSET_LICENSE.md)。

版本记录见 [CHANGELOG.md](CHANGELOG.md)。
