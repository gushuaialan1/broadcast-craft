# Stage 02 | Pain Mapping（痛点映射）

## 输入

- 用户画像原始描述：{{target_persona}}
- 书籍锚定结果：stage_01_book_anchor.json

## 任务

**重要提示：**
`target_persona` 是用户自由填写的文本，可能是任何人群。你必须基于这段原始描述**自主推导**痛点，**严禁套用任何预设人群模板**。

1. 从原始描述中提取：
   - 身份标签（他是谁）
   - 生活场景（在什么情况下产生痛点）
   - 核心情绪（他感受到什么）
   - 渴望状态（他希望变成什么样）
2. 找到一个历史人物，其困境与该用户最相似
3. 确认痛点与书籍核心论点的关联度（0-10 分）

## 输出格式（JSON）

```json
{
  "target_persona_raw": "用户原始描述",
  "pain_identity": "身份标签",
  "pain_scenario": "生活场景",
  "pain_emotion": "核心情绪",
  "pain_aspiration": "渴望状态",
  "historical_analog": "历史类比人物",
  "analog_rationale": "为什么这个历史人物的困境与目标用户相似",
  "book_relevance_score": 8
}
```
