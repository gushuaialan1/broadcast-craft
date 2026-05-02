# Stage 05 爆点质检 / Mystery Chronicles

## 背景

事件名称：{{event.name}}
核心人物：{{event.protagonist}}

## 前置状态

Stage 01-04 全部产出：
```json
{{state.stage_01 | json}}
```
```json
{{state.stage_02 | json}}
```
```json
{{state.stage_03 | json}}
```
```json
{{state.stage_04 | json}}
```

## 任务

对 Stage 04 的口播稿进行**终端质检**，确保它满足 mystery-chronicles 的所有标准。

## 五问审查（核心）

1. **悬疑足够强吗？** 是否有一个明确的"细思极恐点"，让人看完后"越想越不对"？
2. **史料分层清晰吗？** 每个关键断言都有来源，没有将传说/演绎包装成史料？
3. **节奏紧凑吗？** 每15秒是否都有信息增量或情绪小高峰？有没有拖沓的部分？
4. **情绪收获有余韵吗？** 结尾是否保持了开放性？观众看完是感觉"就算了吧"还是"有点意思"？
5. **值得分享吗？** 你会转发给朋友说"你看到那个XX的视频没"？

## 输出要求（JSON）

```json
{
  "event_name": "事件名",
  "verdict": "PASS|NEEDS_REVISION",
  "five_questions": [
    {
      "question": "悬疑足够强吗？",
      "score": "1-5",
      "analysis": "分析",
      "issue": "如有问题，具体描述"
    },
    {
      "question": "史料分层清晰吗？",
      "score": "1-5",
      "analysis": "",
      "issue": ""
    },
    {
      "question": "节奏紧凑吗？",
      "score": "1-5",
      "analysis": "",
      "issue": ""
    },
    {
      "question": "情绪收获有余韵吗？",
      "score": "1-5",
      "analysis": "",
      "issue": ""
    },
    {
      "question": "值得分享吗？",
      "score": "1-5",
      "analysis": "",
      "issue": ""
    }
  ],
  "overall_score": "总分（25分满分）",
  "revision_notes": [
    "如果 verdict 是 NEEDS_REVISION，这里列出具体修改建议"
  ],
  "suspense_check": {
    "has_clear_unsolved": "是否有明确的未解之谜",
    "open_ending_intact": "结尾是否开放（不是确定结论）",
    "no_pseudoscience": "没有用伪科学作为结论",
    "source_tier_labels": "史料来源是否每句都有标注"
  }
}
```

## 号令

- **PASS 标准**：总分22分以上，且每个维度4分以上，且 `suspense_check` 全部通过。
- **NEEDS_REVISION 标准**：任何一项不满足，都是 NEEDS_REVISION。
- 如果是 NEEDS_REVISION，修改建议必须**具体、可执行**，不能是"这里感觉差了点"。
