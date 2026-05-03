# Stage 05 – Review（爆点质检）

## 背景
对 Stage 04 生成的口播稿进行五问质检，确保达到出厂标准。

## 前置状态
标签锚定：
```json
{{state.stage_01 | tojson(indent=2)}}
```

深度挖掘：
```json
{{state.stage_02 | tojson(indent=2)}}
```

钩子与节奏：
```json
{{state.stage_03 | tojson(indent=2)}}
```

口播稿：
```json
{{state.stage_04 | tojson(indent=2)}}
```

## 五问质检

### 1. 反差够不够强？
标签与真相之间的差距是否足以让观众"真的吗？"

### 2. 史料可不可靠？
核心论点是否有 A/B 级史料支撑？是否混杂了演义内容？

### 3. 人物立体吗？
文稿是否呈现了一个多维度的人，而不是简单的"好人变坏人"或"坏人变好人"？

### 4. 情绪收获吗？
看完后观众是否会有"原来如此"或"还能这样理解"的感受？

### 5. 值得分享吗？
观众是否愿意在评论区说"我以前也这么觉得"或"去看 XX 书里真的有"？

## 输出格式
请严格按以下 JSON 格式输出：

```json
{
  "figure": "人物姓名",
  "tag": "大众标签",
  "overall_verdict": "PASS / NEEDS_REVISION",
  "dimension_scores": {
    "contrast_strength": 85,
    "source_reliability": 80,
    "persona_dimension": 90,
    "emotional_payoff": 85,
    "shareability": 80
  },
  "issues": [
    "如果有问题，列出具体修改建议"
  ],
  "revision_direction": "如果 NEEDS_REVISION，提供修改方向"
}
```

如果 `overall_verdict` 为 `PASS`，`issues` 和 `revision_direction` 可以留空列表。
