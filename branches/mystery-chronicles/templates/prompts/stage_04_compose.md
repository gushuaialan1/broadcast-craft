# Stage 04 悬疑口播成稿 / Mystery Chronicles

## 背景

事件名称：{{event.name}}
核心人物：{{event.protagonist}}
平台：{{audience.platform}}
时长：{{output.duration}}

## 前置状态

Stage 01 大众传说锚定：
```json
{{state.stage_01 | json}}
```

Stage 02 史料深挖：
```json
{{state.stage_02 | json}}
```

Stage 03 悬疑钩子设计：
```json
{{state.stage_03 | json}}
```

## 任务

根据以上三个 stage 的产出，写一篇**完整的短视频口播稿**。

核心特征：
1. **悬疑氛围**——不是反转，是"层层剥开"
2. **史料分层**——每个关键信息都必须含有来源标注
3. **开放结尾**——不给出确定结论
4. **情绪余韵**——看完后"越想越不对"

## 输出要求（JSON）

```json
{
  "event_name": "事件名",
  "script": {
    "total_duration": "总时长（秒）",
    "total_chars": "总字数",
    "lines": [
      {
        "time": "0-3s",
        "text": "口播文案",
        "delivery_note": "语气/停顿/重音标注",
        "emotion": "情绪导向",
        "source_tier": "正史|野史|笔记|传说|演绎|无（如果是过渡句/设定）",
        "source_name": "具体来源书名（如有）"
      }
    ]
  },
  "source_notes": [
    {
      "claim": "文案中做出的某个具体断言",
      "tier": "正史|野史|笔记|传说|演绎",
      "source": "来源书名/篇名",
      "caveat": "备注（如果是推测，写明推测依据；如果是传说，写明传说属性）"
    }
  ],
  "emotional_arc": [
    {"timestamp": "0-10s", "emotion": "好奇", "intensity": 1},
    {"timestamp": "10-25s", "emotion": "紧张", "intensity": 2},
    {"timestamp": "25-40s", "emotion": "震惊", "intensity": 3},
    {"timestamp": "40-50s", "emotion": "不安", "intensity": 4},
    {"timestamp": "50-60s", "emotion": "余韵", "intensity": 3}
  ],
  "suspense_moment": {
    "timestamp": "细思极恐点出现的时间段",
    "text": "细思极恐点的原文",
    "why_it_works": "为什么这一句能让人越想越不对"
  }
}
```

## 写作约束

1. **字数**：总字数300-450字（约60-90秒口播）。如果是2分钟版本，600-800字。
2. **口语化**：每一句都是"在说话"，不是"在写文章"。禁止书面语、连贯的文言文句。
3. **短句为主**：每句不超15字。长句要有停顿。
4. **问句作刀**：每隔15秒左右要有一个问句，提高参与感。
5. **史料不干涉流畅**：史料来源在 `source_notes` 里标注，口播本文不必每句都引书名，但关键信息必须可追溯。
6. **开放结尾**：结尾不能是"所以实际上是这样"。必须是"但如果不是呢？"或者"这个问题，XX一直没有答案"。
7. **callback 设计**：结尾最后一句最好能 callback 开头的钩子，形成记忆闭环。
8. **禁止**：
   - 禁止恐怖片式决绝
   - 禁止科学伪证
   - 禁止详细解释太空洞的宇宙理论
   - 禁止歼读历史人物人格
