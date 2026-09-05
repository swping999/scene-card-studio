# Scene Card Studio 视觉选择指南

[English](VISUAL-GUIDE.md) · [返回中文首页](README.zh-CN.md)

Scene Card Studio 不是把 24 种效果随机套在照片上。它用两个可以组合的选择控制结果：

```text
照片内容与叙事目标 → Narrative System（如何阅读照片）
审美与材质要求     → Expression Profile（最终如何呈现）
```

例如，同一张湖边照片可以被读成 `travel-journal`（旅途中一个停顿），再用 `travel-zine` 做成克制的旅行页面；也可以被读成 `memory-atlas`（地点与空间记忆），再用 `selective-material-relief` 保留真实小船、把山体转成浮雕。

## 最简单的两种用法

### 让系统自动选择

把照片上传到 Codex，然后说：

> 使用 $scene-card-studio 分析这张照片，自动选择最合适的 Narrative System 和 Expression Profile。先用一句话说明选择理由；如果两个方向接近，给我两个候选。保持主体身份和原始场景可辨认。

自动选择不是随机抽风格：

- Codex 先观察主体、空间、动作、光线和情绪，完成 Scene Card；
- 系统根据照片证据和你的 brief 选择 Narrative System；
- 当你明确提出“水彩、国风、3D 微缩、像素、蓝晒”等视觉诉求，或明确说“视觉风格也由你选择”时，Codex 才会选择非默认 Profile；
- 没有明确风格要求时使用 `source-led`，尽量从原图自身的光线、颜色和材质出发；
- 路由置信度过低或两个系统接近时，应先展示候选，不擅自决定；
- 远程图片生成前仍需确认提供商、用途和上传文件清单。

本地命令可以自动准备 Scene Card、Prompt Manifest 和 Workprint：

```bash
scene-card-studio direct photo.jpg \
  --brief "自动选择最适合这张照片的叙事与视觉表达" \
  --output-dir scene-card-output
```

`direct` 是本地准备步骤，不会独自调用图片生成服务。裸 CLI 只能根据 brief 中明确出现的视觉词路由 Profile；由 Codex 自动判断视觉风格时，Codex 会先检查照片，再把选中的 Profile 明确传给 `direct`。完整 After 由安装后的 Skill 在完成语义方向并获得上传同意后生成。

### 自己指定效果

不需要记住所有参数，直接用自然语言说清“系统 + Profile”即可：

> 使用 $scene-card-studio，把这张照片按 Memory Atlas 组织，并使用 chinese-ink-poetry。保留真实主体与真实环境，边缘融入水墨。文字：静观｜窗影入墨，闲看岁长。

本地编译时也可以明确指定：

```bash
scene-card-studio direct photo.jpg \
  --system memory-atlas \
  --expression-profile chinese-ink-poetry \
  --brief "保留真实主体，环境边缘水墨化；标题：静观；诗句：窗影入墨，闲看岁长" \
  --output-dir scene-card-output
```

## 第一步：选择 Narrative System

Narrative System 决定照片如何被理解和组织，不等于滤镜。单张照片在任何系统下都只生成一张独立 After；下表的“多图方式”只说明上传多张照片时的默认组织方式。

| 系统 | 什么时候选 | 多图方式 | 案例 |
| --- | --- | --- | --- |
| `cinematic-storyboard` · Cinematic Sequence | 时间感、动作、天气、光线变化、电影镜头关系 | 每张独立，保持连续性 | <img src="examples/cases/v0.4-gallery/after/cinematic-sequence.jpg" width="120" alt="Cinematic Sequence"> |
| `memory-atlas` · Memory Atlas | 地点、距离、方向、路线或空间记忆 | 合成为一个空间叙事 | <img src="examples/cases/v0.4-gallery/after/memory-atlas.jpg" width="120" alt="Memory Atlas"> |
| `family-archive` · Family Chronicle | 重复出现的人、物件、家庭动作或时间痕迹 | 合成为一份档案 | <img src="examples/cases/v0.4-gallery/after/family-chronicle.jpg" width="120" alt="Family Chronicle"> |
| `minimal-editorial` · Quiet Editorial | 单一主体、静物、留白、几何、材质与安静光线 | 每张独立 | <img src="examples/cases/v0.4-gallery/after/quiet-editorial.jpg" width="120" alt="Quiet Editorial"> |
| `editorial-sequence` · Editorial Rhythm | 想用大小、疏密、对比和停顿形成编辑节奏 | 每张独立并形成序列 | <img src="examples/cases/v0.4-gallery/after/editorial-rhythm.jpg" width="120" alt="Editorial Rhythm"> |
| `field-log` · Field Log | 现场观察、工具、自然标本、过程和纪实细节 | 每张独立 | <img src="examples/cases/v0.4-gallery/after/field-log.jpg" width="120" alt="Field Log"> |
| `museum-catalogue` · Museum Catalogue | 一个可仔细观察的物件、藏品或工艺细节 | 每张独立成图录页 | <img src="examples/cases/v0.4-gallery/after/museum-catalogue.jpg" width="120" alt="Museum Catalogue"> |
| `travel-journal` · Travel Journal | 旅途、车站、门槛、停顿、票据与地点信息 | 合成为旅行记录 | <img src="examples/cases/v0.4-gallery/after/travel-journal.jpg" width="120" alt="Travel Journal"> |
| `journey-taxonomy` · Journey Taxonomy | 把旅行画面中的地貌、天气、动植物、物件和移动线索分类 | 合成为一张地点分类图 | <img src="examples/cases/v0.6-gallery/after/journey-taxonomy.png" width="120" alt="Journey Taxonomy"> |
| `street-reportage` · Street Reportage | 街头动作、公共空间、事件上下文和纪实瞬间 | 每张独立并保持事实顺序 | <img src="examples/cases/v0.4-gallery/after/street-reportage.jpg" width="120" alt="Street Reportage"> |
| `fashion-editorial` · Fashion Editorial | 人物姿态、服装结构、面料、裁切和镜头尺度 | 每张独立并形成时尚节奏 | <img src="examples/cases/v0.4-gallery/after/fashion-editorial.jpg" width="120" alt="Fashion Editorial"> |

## 第二步：选择 Expression Profile

下面 24 种 Profile（1 个默认 `source-led` + 23 个非默认 Profile）都有仓库内的实际案例。选择时先看“想得到什么”，再把调用短语放进 brief。兼容组合可运行 `scene-card-studio profiles --system SYSTEM_ID` 检查。

### 摄影、电影与编辑语言

| Profile | 想得到什么 | 可以这样说 | 案例 |
| --- | --- | --- | --- |
| `source-led` | 不套固定材质，依据原图自身的光、色、空间与表面做导演 | “保持 source-led，只优化叙事、构图和光线层级” | <img src="examples/cases/v0.4-gallery/after/editorial-rhythm.jpg" width="150" alt="Source-led"> |
| `rain-nocturne` | 有真实光源依据的雨夜电影感，避免滥用霓虹 | “做成克制的雨夜电影镜头，保留真实路灯与湿地反光” | <img src="examples/cases/v0.4-gallery/after/cinematic-sequence.jpg" width="150" alt="Rain Nocturne"> |
| `quiet-window-light` | 暖窗光、明确阴影几何、低密度留白和细微胶片颗粒 | “做成安静窗光 editorial，让光成为第二主体” | <img src="examples/cases/v0.4-gallery/after/quiet-editorial.jpg" width="150" alt="Quiet Window Light"> |
| `heritage-portrait` | 克制银盐、手工着色与保存良好的传统影像质感 | “做成克制银盐与手工着色的传统影像肖像” | <img src="examples/cases/v0.4-gallery/after/heritage-portrait.jpg" width="150" alt="Heritage Portrait"> |
| `monochrome-reportage` | 细节完整的黑白街头纪实与银盐颗粒 | “做成黑白街头纪实，保留环境证据与阴影细节” | <img src="examples/cases/v0.4-gallery/after/street-reportage.jpg" width="150" alt="Monochrome Reportage"> |
| `autochrome-memory` | 克制的早期彩色印相感，不虚构年代或身份 | “使用早期彩色印相质感，但不要把人物伪装成历史角色” | <img src="examples/cases/v0.6-gallery/after/autochrome-memory.png" width="150" alt="Autochrome Memory"> |
| `chinese-photo-editorial` | 保留真实照片锚点的当代水墨纸张编辑感，不自动添加竹子等符号 | “做成克制的照片水墨 editorial，只使用原图支持的元素” | <img src="examples/cases/v0.7-director-gallery/after/chinese-photo-editorial.png" width="150" alt="Chinese Photo Editorial"> |

### 绘画、版画与纸上媒介

| Profile | 想得到什么 | 可以这样说 | 案例 |
| --- | --- | --- | --- |
| `watercolor-contour` | 真实建筑或地点作为摄影锚点，周围融合水彩地形与铅笔等高线 | “保留真实建筑照片，与水彩地形和铅笔轮廓融合” | <img src="examples/cases/v0.4-gallery/after/memory-atlas.jpg" width="150" alt="Watercolor Contour"> |
| `watercolor-chronicle` | 人物、物件和环境全部进入同一套完整水彩媒介 | “把整张照片统一重绘为水彩，人物也要水彩化” | <img src="examples/cases/v0.4-gallery/after/watercolor-chronicle.jpg" width="150" alt="Watercolor Chronicle"> |
| `graphite-paper` | 纪实照片、石墨研究、描图纸和纤维形成档案层次 | “使用石墨、铅笔和描图纸组织成家庭档案” | <img src="examples/cases/v0.4-gallery/after/family-chronicle.jpg" width="150" alt="Graphite Paper"> |
| `mineral-ink-memory` | 矿物颜料和墨色共同组织空间深度与记忆 | “把地点做成矿物岩彩与墨色共同构成的记忆场” | <img src="examples/cases/v0.6-gallery/after/mineral-ink-memory.png" width="150" alt="Mineral Ink Memory"> |
| `impasto-light-study` | 厚涂油彩沿真实光路堆积，强调实体笔触 | “做成厚涂油画光线研究，让笔触跟随原图光线” | <img src="examples/cases/v0.6-gallery/after/impasto-light-study.png" width="150" alt="Impasto Light Study"> |
| `gouache-place-study` | 不透明水粉、哑光形状与清晰地点结构 | “把这个地点重绘成克制的不透明水粉写生” | <img src="examples/cases/v0.6-gallery/after/gouache-place-study.png" width="150" alt="Gouache Place Study"> |
| `risograph-route` | 少量专色、网点和套印误差表达路线与地点 | “用两到三种专色做孔版印刷旅行路线” | <img src="examples/cases/v0.6-gallery/after/risograph-route.png" width="150" alt="Risograph Route"> |
| `cyanotype-archive` | 普鲁士蓝的蓝晒档案或日光印相语言 | “把可见物件做成有证据约束的蓝晒档案” | <img src="examples/cases/v0.6-gallery/after/cyanotype-archive.png" width="150" alt="Cyanotype Archive"> |
| `chinese-ink-poetry` | 真实主体和真实环境仍可辨认，边缘融入宣纸与水墨，并准确排入用户诗句 | “做成国风水墨诗意照片；文字：静观｜窗影入墨，闲看岁长” | <img src="examples/cases/v0.7-director-gallery/after/chinese-ink-poetry-final.png" width="150" alt="Chinese Ink Poetry"> |

### 立体、纤维与材料转换

| Profile | 想得到什么 | 可以这样说 | 案例 |
| --- | --- | --- | --- |
| `paper-relief-landscape` | 整个地点变成有前后景深度的连续纸雕地景 | “把完整风景做成层叠纸张与切纸构成的连续浮雕” | <img src="examples/cases/v0.6-gallery/after/paper-relief-landscape.png" width="150" alt="Paper Relief Landscape"> |
| `sculpted-place-diorama` | 具有真实体积、实体光照和地理层次的 3D 微缩模型 | “把这个地点重建成实体 3D 微缩地景，不做玩具贴纸” | <img src="examples/cases/v0.6-gallery/after/sculpted-place-diorama.png" width="150" alt="Sculpted Place Diorama"> |
| `threaded-landscape` | 整幅画面统一为编织、刺绣、毛线与局部簇绒的纤维浮雕 | “把整张风景重绘成连续的编织刺绣纤维浮雕” | <img src="examples/cases/v0.6-gallery/after/threaded-landscape.png" width="150" alt="Threaded Landscape"> |
| `selective-material-relief` | 主体保持真实摄影，只有授权的环境变成连续浅浮雕 | “船保持真实照片，山体和环境变成连续浅浮雕” | <img src="examples/cases/v0.7-director-gallery/after/selective-material-relief.png" width="150" alt="Selective Material Relief"> |

### 图形、旅行与实验语言

| Profile | 想得到什么 | 可以这样说 | 案例 |
| --- | --- | --- | --- |
| `pixel-diary` | 整个场景使用统一像素尺度重建，而不是给照片加像素边框 | “把场景重建成统一像素网格的旅行日记” | <img src="examples/cases/v0.6-gallery/after/pixel-diary.png" width="150" alt="Pixel Diary"> |
| `pixel-ink-memory` · 实验 | 近处为清晰像素，远处为水墨扩散，两种媒介共享构图和光线 | “使用像素与水墨双媒介：近景像素、远景墨色，不能左右拼接” | <img src="examples/cases/v0.6-gallery/after/pixel-ink-memory.png" width="150" alt="Pixel Ink Memory"> |
| `dream-logic` | 保留身份与主体的一条清晰超现实空间规则 | “保持人物身份，只建立一条可读的不可能空间规则” | <img src="examples/cases/v0.4-gallery/after/dream-logic.jpg" width="150" alt="Dream Logic"> |
| `travel-zine` | 一张主图、少量源图细节、克制路线信息和大量不规则留白 | “做成稀疏的旅行 Zine，只突出一个记忆节点” | <img src="examples/cases/v0.7-director-gallery/after/travel-zine.png" width="150" alt="Travel Zine"> |

## 按照片快速选择

| 你的照片 | 推荐组合 | 原因 |
| --- | --- | --- |
| 一张旅行风景 | `travel-journal` + `travel-zine` | 最容易得到清晰、克制、可分享的旅行作品 |
| 多张旅行照片 | `journey-taxonomy` + `travel-zine` | 一边组织地点线索，一边维持统一页面语言 |
| 船、自行车、灯塔等清晰主体与风景 | `memory-atlas` + `selective-material-relief` | 主体真实、环境立体，视觉差异最明显 |
| 宠物、人物或建筑，希望做国风 | `minimal-editorial` 或 `memory-atlas` + `chinese-ink-poetry` | 保留真实照片，水墨负责融合，文字由排版层准确完成 |
| 普通人像 | `family-archive` + `heritage-portrait` | 适合克制的传统影像质感，不虚构人物年代 |
| 静物、房间、窗边主体 | `minimal-editorial` + `quiet-window-light` | 用留白、材质和光线提升高级感 |
| 街拍或雨夜 | `street-reportage` + `monochrome-reportage`，或 `cinematic-storyboard` + `rain-nocturne` | 前者偏事实纪实，后者偏镜头叙事 |
| 山、水、草地等完整风景 | `travel-journal` + `threaded-landscape` / `paper-relief-landscape` / `sculpted-place-diorama` | 分别得到纤维、纸雕或实体 3D 地景 |
| 不确定，希望尽量忠于原图 | 自动 System + `source-led` | 不强行套媒介，让系统从原图证据出发 |

## 三个容易混淆的区别

1. `watercolor-contour` 保留真实摄影锚点；`watercolor-chronicle` 会把整张画面统一水彩化。
2. `paper-relief-landscape` 是全画面纸浮雕；`selective-material-relief` 保留真实摄影主体，只改变环境。
3. `chinese-photo-editorial` 不要求诗句；`chinese-ink-poetry` 专门为国风照片与确定性中文排版设计。

案例展示目标视觉机制，不意味着每张输入都会产生像素完全相同的构图。主体、地点、光线和空间关系应由上传照片决定；Profile 负责稳定约束视觉语言。
