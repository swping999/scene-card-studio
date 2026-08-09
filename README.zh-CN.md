# Scene Card Studio｜场景卡片工作室

中文 · [English](README.md)

> **这不是一个照片风格转换工具，而是一套基于 Scene Card 的个人照片视觉叙事引擎。**

Scene Card Studio 将照片中可观察的事实转化为可编辑的叙事决策和确定性版面。它不只问“照片应该变成什么风格”，而是先判断“这段故事应该如何被阅读”。

```text
照片 → 观察事实 → 理解判断 → 视觉导演 → 叙事排序 → Narrative System → 可编辑输出
```

## Before / After 首页案例

以下原始照片均为本项目专门生成的原创示例。每组对照都保留未经处理的输入。除非某个 Narrative System 明确依赖空间蒙太奇，否则默认一张原片只生成一张独立 After。

| Before：原始旅行照片 | After：AI 复合 Memory Atlas |
| --- | --- |
| ![原始照片接触表](examples/outputs/before-source-photos.png) | ![真实建筑摄影与手绘记忆地图融合](examples/outputs/memory-atlas-ai-composite.png) |

[查看本案例的三层 Scene Cards](examples/generated-story.json)

### 案例 2 · Family Archive｜家庭档案

| Before：虚构人物纪实输入 | After：AI 复合家庭档案 |
| --- | --- |
| ![家庭档案原始接触表](examples/cases/family-archive/outputs/before.png) | ![人物纪实摄影与素描、档案材料融合](examples/cases/family-archive/outputs/family-archive-ai-composite.png) |

第二组案例把晾衣、包饺子、整理旧照片这些重复动作，读成一段跨代传递的照料记录。

[查看 Family Archive Scene Cards](examples/cases/family-archive/story.json)

### 案例 3 · Cinematic Storyboard｜电影分镜

三张平淡的手机随手拍，分别变成三个独立电影镜头。它们通过“等待—停顿—离开”的光线与情绪弧线相连，而不是被拼进同一张版式。

| Before：构图失败的手机随手拍 | After：独立导演镜头 |
| --- | --- |
| ![普通公交站手机随手拍](examples/cases/cinematic-storyboard/photos/raw-bus-stop.png) | ![经过导演的雨夜公交站镜头](examples/cases/cinematic-storyboard/outputs/after-bus-stop.png) |
| ![普通小餐馆手机随手拍](examples/cases/cinematic-storyboard/photos/raw-diner.png) | ![隔着雨水观看餐馆的电影镜头](examples/cases/cinematic-storyboard/outputs/after-diner.png) |
| ![普通出租车手机随手拍](examples/cases/cinematic-storyboard/photos/raw-taxi.png) | ![出租车离开的电影镜头](examples/cases/cinematic-storyboard/outputs/after-taxi.png) |

[查看三层 Scene Cards](examples/cases/cinematic-storyboard/story.json) · [查看未经处理的原片接触表](examples/cases/cinematic-storyboard/outputs/before.png)

### 案例 4 · Minimal Editorial｜极简编辑

这个系统不会把三个物件贴到一张“设计稿”上，而是给每个普通物件一个独立摄影舞台，让材质、影子和留白承担叙事。

| Before：杂乱的家庭随手拍 | After：独立艺术书摄影 |
| --- | --- |
| ![普通杯子手机随手拍](examples/cases/minimal-editorial/photos/raw-mug.png) | ![同一杯子的安静编辑摄影](examples/cases/minimal-editorial/outputs/after-mug.png) |
| ![普通旧椅子手机随手拍](examples/cases/minimal-editorial/photos/raw-chair.png) | ![同一椅子的雕塑感编辑摄影](examples/cases/minimal-editorial/outputs/after-chair.png) |
| ![普通亚麻布手机随手拍](examples/cases/minimal-editorial/photos/raw-linen.png) | ![同一亚麻布的材质编辑摄影](examples/cases/minimal-editorial/outputs/after-linen.png) |

[查看三层 Scene Cards](examples/cases/minimal-editorial/story.json) · [查看未经处理的原片接触表](examples/cases/minimal-editorial/outputs/before.png)

这里发生的不是简单滤镜或重新排版。系统先区分观察事实与解释，再分配故事角色、生成导演备注、推荐 Narrative System，最终既可以输出确定性 Workprint，也可以生成真正发生视觉二次创作的成品。空间与档案系统可以使用混合媒介；电影与极简系统默认“一张原片 → 一个独立镜头”。

### Editorial Sequence｜编辑序列

![编辑序列案例](examples/outputs/editorial-sequence.png)

让照片保持主体地位，通过留白、顺序和角色标签建立可阅读的摄影叙事。

### Memory Atlas｜记忆地图

![摄影与手绘融合的记忆地图案例](examples/outputs/memory-atlas-ai-composite.png)

适合旅程、离开、距离、返回与空间记忆。真实建筑保持摄影质感，地点之间的地理空间则转化为手绘记忆。

### Field Log｜现场日志

![现场日志案例](examples/outputs/field-log.png)

适合人物纪实、旅行观察、现场证据和克制的注释系统。

[查看原创样片](examples/photos) · [查看 Scene Cards](examples/generated-story.json) · [查看设计原则](DESIGN_PRINCIPLES.md)

## AI 视觉导演层

Scene Card 将信息明确分成三层：

- **Observation / 观察层**：记录照片中实际可见的主体、方向、色彩和安静区域。
- **Interpretation / 理解层**：记录暂定主题、情绪和置信度。
- **Direction / 导演层**：记录可编辑的故事角色、导演备注和版面重点。

这种拆分避免把 AI 的推测伪装成照片事实，也允许用户覆盖任何导演判断。首页高级叙事字段明确标记为人工导演示例；当前 analyzer 只提供低置信度启发式判断。

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
scene-card-studio render story.json --style editorial-sequence --format png --output story.png
scene-card-studio render story.json --style field-log --mode workprint --format png --output notes.png
```

默认使用 `presentation`，隐藏内部导演术语；需要查看观察、理解、角色和导演备注时使用 `--mode workprint`。输出高度会随照片数量动态增长，照片路径以 Scene Card JSON 所在目录为基准解析。

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

完整说明见 [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)。

## 路线图

- 可由用户修改的视觉导演判断；
- `contact-sheet`、`journey-sequence`；
- 主体感知裁切；
- 可打印 PDF 与社交媒体卡片；
- 浏览器预览和拖拽排序；
- 社区 Narrative System 插件。

## 许可证

Apache-2.0。贡献的示例素材必须提供清晰的来源和使用条款。
