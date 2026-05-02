# Stage 03 悬疑钩子设计 / Mystery Chronicles

## 背景

事件名称：{{event.name}}
核心人物：{{event.protagonist}}

## 前置状态

Stage 01 大众传说锚定：
```json
{{state.stage_01 | json}}
```

Stage 02 史料深挖：
```json
{{state.stage_02 | json}}
```

## 任务

设计一个**悬念钩子**，在前3秒内把观众"钩住"，让他们**不敢划走**。

mystery-chronicles 的钩子与 history-twist 不同：
- history-twist 的钩子是**认知反转**："你以为 A 其实是 B"
- mystery-chronicles 的钩子是**悬念设定**："正史里记载了一件事，但从来没人敢深想"

## 输出要求（JSON）

```json
{
  "event_name": "事件名",
  "hook_candidates": [
    {
      "type": "悬念型|反常型|细思极恐型|引用型",
      "text": "钩子文案（15-30字，口语化）",
      "why_works": "为什么这个钩子能钩住人？",
      "intended_emotion": "目标情绪（好奇/紧张/不安/震惊）"
    }
  ],
  "selected_hook": {
    "text": "最终选定的钩子",
    "platform_adaptation": {
      "抖音": "抖音版本（更直接、更有冲击力）",
      "视频号": "视频号版本（更温和、更适合转发）",
      "B站": "B站版本（更有信息量、允许更长的钩子）"
    }
  },
  "structure_design": {
    "overall_arc": "整体悬念弧线（比如'谜团抛出→层层剥开→最后一刀→开放余韵'）",
    "pacing_nodes": [
      {
        "timestamp": "0-3s",
        "function": "钩子",
        "content": "具体做什么"
      },
      {
        "timestamp": "3-10s",
        "function": "氛围铺垫",
        "content": ""
      },
      {
        "timestamp": "10-25s",
        "function": "史料层剥第一层",
        "content": ""
      },
      {
        "timestamp": "25-40s",
        "function": "史料层剥第二层（间隶）",
        "content": ""
      },
      {
        "timestamp": "40-55s",
        "function": "细思极恐点",
        "content": ""
      },
      {
        "timestamp": "55-60s",
        "function": "开放性余韵 / callback",
        "content": ""
      }
    ],
    "tension_curve": "悬念强度曲线描述（低→高→低→更高→放开）"
  },
  "atmosphere_notes": {
    "bgm_suggestion": "背景音乐风格建议（低沉/科幻感/古典/空灵）",
    "visual_cue": "画面提示（比如'黑屏白字出现史书名'、'故宫夜景'、'星图滑动'）",
    "tone_of_voice": "口播语气（低声/中速/带疑问语气/偶尔停顿）"
  }
}
```

## 号令

- 钩子的核心是"让观众想知道答案"，不是"让观众知道了一个新事实"。
- 禁止悬疑钩子变成**恐怖视频语录**。我们要的是"细思极恐"，不是"嚎叫橡皮"。
- 结尾的余韵必须是**开放的**——不要在钩子里提前告诉人家答案。
