# Stage 03 – Hook Design（钩子设计）

## 背景
基于前两个阶段的产出，现在设计最能打动人的开场钩子和整体节奏。

## 前置状态
标签锚定：
```json
{{state.stage_01 | tojson(indent=2)}}
```

深度挖掘：
```json
{{state.stage_02 | tojson(indent=2)}}
```

推荐策略：
```json
{{recommended | tojson(indent=2)}}
```

## 任务

### 1. 开场钩子（3秒抢注意力）
设计 3 个备选钩子，要求：
- 直接对冲人物标签
- 用问句、数据、或"你不知道的是"开头
- 不超过 25 字

### 2. 节奏设计
根据人格拼贴叙事结构，设计每个节点的时长分配。

### 3. 情绪曲线
规划整个视频的情绪起伏：好奇 → 震惊 → 深入 → 同情/思考 → 余韵。

### 4. 反差强度评级
- L1（轻微）：补充信息
- L2（中等）：调整认知
- L3（强烈）：彻底颠覆人设
- L4（爆炸）：引发身份认同危机

## 输出格式
请严格按以下 JSON 格式输出：

```json
{
  "figure": "人物姓名",
  "tag": "大众标签",
  "hooks": [
    "钩子1",
    "钩子2",
    "钩子3"
  ],
  "selected_hook": "最推荐钩子",
  "rhythm": {
    "tag_restore_sec": 10,
    "evidence_drop_sec": 15,
    "motive_rebuild_sec": 30,
    "second_evidence_sec": 20,
    "persona_puzzle_sec": 20,
    "modern_mirror_sec": 15,
    "ending_sec": 10
  },
  "emotion_arc": ["好奇", "震惊", "深入", "思考", "余韵"],
  "contrast_level": "L1/L2/L3/L4"
}
```
