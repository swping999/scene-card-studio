# Moments to Pages｜片刻成册

中文 · [English](README.md)

> **这不是一个照片风格转换工具，而是一套基于 Scene Card 的个人照片视觉叙事引擎。**

Moments to Pages 将照片中可观察的事实转化为可编辑的叙事决策和确定性版面。它不只问“照片应该变成什么风格”，而是先判断“这段故事应该如何被阅读”。

```text
照片 → 观察事实 → 视觉导演 → 叙事排序 → Narrative System → 可编辑输出
```

## 首页案例

以下原始照片均为本项目专门生成的原创示例。三张版面使用同一组 Scene Cards，但采用不同的记录机制。

### Editorial Sequence｜编辑序列

![编辑序列案例](examples/outputs/editorial-sequence.png)

让照片保持主体地位，通过留白、顺序和角色标签建立可阅读的摄影叙事。

### Memory Atlas｜记忆地图

![记忆地图案例](examples/outputs/memory-atlas.png)

适合旅程、离开、距离、返回与空间记忆。

### Field Log｜现场日志

![现场日志案例](examples/outputs/field-log.png)

适合人物纪实、旅行观察、现场证据和克制的注释系统。

[查看原创样片](examples/photos) · [查看 Scene Cards](examples/generated-story.json) · [查看原创性声明](ORIGINALITY.md)

## AI 视觉导演层

Scene Card 将信息明确分成两层：

- **Observation / 观察层**：记录照片中实际可见的主体、方向、色彩和安静区域。
- **Direction / 导演层**：记录可编辑的叙事意图、情绪、故事角色和导演备注。

这种拆分避免把 AI 的推测伪装成照片事实，也允许用户覆盖任何导演判断。

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
moments-to-pages analyze photos/*.jpg --output story.json
moments-to-pages recommend story.json
moments-to-pages render story.json --style editorial-sequence --format png --output story.png
```

## Codex Skill

将 `skills/moments-to-pages` 复制到 Codex Skills 目录并重启，然后输入：

```text
使用 $moments-to-pages 把这些照片编排成一组安静的家庭视觉档案。
```

## 原创与隐私

- 不捆绑第三方风格参考资产；
- 不复制其他同类仓库的提示词；
- 示例图片均为项目新生成的原创演示素材；
- 核心创新是 Scene Card、Visual Director 与叙事渲染工作流；
- 除非用户明确选择，否则原始照片只在本地处理。

完整说明见 [ORIGINALITY.md](ORIGINALITY.md)。

## 路线图

- 可由用户修改的视觉导演判断；
- `family-archive`、`contact-sheet`、`journey-sequence`；
- 主体感知裁切；
- 可打印 PDF 与社交媒体卡片；
- 浏览器预览和拖拽排序；
- 社区 Narrative System 插件。

## 许可证

Apache-2.0。贡献的示例素材必须提供清晰的来源和使用条款。
