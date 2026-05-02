# Stage 01 大众传说锚定 / Mystery Chronicles

## 背景

我们要创作一条关于"史料中真实记载的超自然/灵异事件"的短视频口播。
事件名称：{{event.name}}
核心人物/关联人物：{{event.protagonist}}

## 任务

分析大众对这个事件的**普遍认知和传说版本**。不是写口播稿，是做"传说背景调查"。

## 输出要求（JSON）

```json
{
  "event_name": "事件名",
  "protagonist": "核心人物",
  "legend_version": {
    "summary": "大众最熟知的传说/故事版本（用一段300字以内概括）",
    "key_elements": ["传说中的关键素村1", "素村2", "素村3"],
    "emotional_tone": "大众对此传说的情绪基调（比如'神秘感'、'恐惧感'、'崇拜感'、'好奇心'）"
  },
  "mass_perception": {
    "what_people_think_they_know": "大众以为自己知道的核心事实（1-3条）",
    "common_misconception": "最常见的误解或毫无根据的推测（1-2条）",
    "source_of_legend": "这个传说版本最可能的流传渠道（比如《三国演义》、民间口口相传、某部经典影视作品）"
  },
  "suspense_potential": {
    "rating": "A|B|C",
    "reason": "为什么这个传说背后隐藏着强大的悬疑潜力？",
    "untapped_detail": "传说中被忽略、但史料中可能有更诡异记载的细节"
  },
  "platform_fit": {
    "recommended_platform": "推荐主打平台",
    "reason": "为什么适合这个平台"
  }
}
```

## 号令

- 不要在这个阶段就去找正史记载。你只需要**复现大众已有的认知**。
- 如果这个事件有多个传说版本，请选最流行的那个。
- 特别关注传说中**被美化/简化/涉及了另一个事件的元素**的部分，这些是后续反差的重点。
