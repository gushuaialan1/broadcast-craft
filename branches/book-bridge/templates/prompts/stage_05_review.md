# Stage 05 | Review（软植入质检）

## 输入

- 书籍锚定：stage_01_book_anchor.json
- 痛点映射：stage_02_pain_mapping.json
- 故事搭桥：stage_03_story_bridge.json
- 成稿：stage_04_compose.json

## 五问审查

1. **价值感优先**：前 60% 是否能独立作为历史短视频观看？
2. **不硬广**：书名是否在视频后半段才出现？
3. **人群精准**：如果删除书名，目标用户是否依然觉得"这说的就是我"？
4. **不夸大**：是否有"读完就能改变人生"的过度承诺？
5. **Fallback 合规**：若使用了 fallback_theme，是否明确标注了"基于 XX 主题展开"？

## 输出格式（JSON）

```json
{
  "review_status": "PASS / NEEDS_REVISION",
  "score": 85,
  "dimension_scores": {
    "value_first": 9,
    "soft_placement": 8,
    "audience_fit": 9,
    "no_hype": 8,
    "fallback_compliance": 10
  },
  "revision_notes": "若 NEEDS_REVISION，列出具体修改建议",
  "final_verdict": "总体评价"
}
```
