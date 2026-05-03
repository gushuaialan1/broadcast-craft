# Stage 03 | Story Bridge（故事搭桥）

## 输入

- 书籍锚定：stage_01_book_anchor.json
- 痛点映射：stage_02_pain_mapping.json

## 任务

1. 选定一个具体历史场景（必须有情节、有冲突）
2. 设计情绪曲线：钩子 → 发展 → 高潮 → 与现代对照 → 书籍桥梁
3. 确保故事同时承担：3 秒抓住注意力 + 让观众觉得"我也是" + 自然过渡到书籍
4. 在故事结尾预留一个"未解之谜"或"遗憾"，让书籍成为解决方案的自然出口

## 输出格式（JSON）

```json
{
  "story_title": "故事标题",
  "historical_scene": "选定的具体历史场景",
  "emotion_curve": [
    {"time": "0-3s", "emotion": "好奇", "technique": "反常开场"},
    {"time": "3-20s", "emotion": "沉浸", "technique": "细节展开"},
    {"time": "20-30s", "emotion": "扎心", "technique": "现代对照"},
    {"time": "30-45s", "emotion": "希望", "technique": "书籍登场"}
  ],
  "open_question": "故事结尾预留的未解之谜或遗憾",
  "modern_mirror": "现代用户的对照场景"
}
```
