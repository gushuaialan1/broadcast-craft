# Broadcast Craft / 口播工坊

> **Hero Line**: 用人格化的方法论，生产有温度、有爆点、有记忆点的短视频口播文案。
> 
> Produce short-video broadcast scripts with personality, punch, and memorability.

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/python-3.10%2B-yellow" alt="python">
</p>

---

## Features / 特点

- **人格化口播体系** — 从「数字生命卡兹克」的长文方法论迁移而来，专为短视频重构
- **8 种 Hook 原型** — 反常识、反问、情绪引爆、数据冲击、秘密揭露、对立冲突、场景幻化、零成本好奇
- **5 种内容原型** — 调查实验、产品体验、现象解读、工具分享、方法论分享
- **L1-L4 四层质检** — 从硬性规则到活人感终审，确保每条文案不达 A 级不发布
- **多分支架构** — 支持横向扩展专业领域（历史反差、科普解读、人物揭秘等）
- **零 LLM 依赖** — Skill 本身不调用任何模型 API，只负责生成 prompt 与编排流程

---

## Quick Start / 快速上手

```bash
# 克隆仓库
git clone https://github.com/gushuaialan1/broadcast-craft.git
cd broadcast-craft/branches/history-twist

# 生成单阶段 prompt
python3 scripts/broadcast_craft.py stage 01_anchor \
  --character 项羽 --event 垓下之战 --length 60s --platform 抖音

# 一键生成全部5个阶段 prompt
python3 scripts/broadcast_craft.py pipeline \
  --character 项羽 --event 垓下之战 --platform 抖音
```

### Demo / 演示

执行 pipeline 后，在 `.broadcast-craft/staging/` 目录下会生成5个按阶段组织的 prompt 文件：

```
.broadcast-craft/staging/
├── stage_01_垓下之战_项羽.md   # 大众认知锚定
├── stage_02_垓下之战_项羽.md   # 反常视角挖掘
├── stage_03_垓下之战_项羽.md   # 钩子与节奏设计
├── stage_04_垓下之战_项羽.md   # 成稿
└── stage_05_垓下之战_项羽.md   # 爆点质检
```

将这些 prompt 逐个交给你的 LLM（如 Kimi、Claude、GPT），它们会返回结构化的 JSON 或 Markdown，你的状态会在每个阶段后自动保存，下一阶段可以引用前面的产出。

---

## Architecture / 架构

| 组件 | 语言 | 职责 |
|---|---|---|
| `SKILL.md` | YAML + Markdown | Skill 主文档，定义流程与元数据 |
| `references/` | Markdown | 通用方法论：Hook 、原型、质检、风格 |
| `branches/<name>/methodology.md` | Markdown | 分支专属方法论 |
| `branches/<name>/templates/prompts/` | Markdown | 分阶段 Prompt 模板（{{dot.path}} 占位符） |
| `branches/<name>/templates/schemas/` | JSON | 各阶段输出的 JSON Schema 校验规则 |
| `branches/<name>/scripts/` | Python 3 | CLI 编排器：渲染、状态、校验 |

```
broadcast-craft/
├── SKILL.md                           # 主文档
├── README.md                          # 本文件
├── references/                        # 通用方法论
│   ├── style_guide.md                 # 风格指南
│   ├── hook_patterns.md               # 8 种钩子
│   ├── content_archetypes.md          # 5 种原型
│   └── quality_matrix.md              # 四层质检
└── branches/
    └── history-twist/                 # 分支一：历史反差爆点
        ├── methodology.md             # 分支方法论
        ├── templates/
        │   ├── prompts/               # 5 个阶段 prompt
        │   └── schemas/               # 5 个 JSON schema
        └── scripts/
            ├── broadcast_craft.py     # CLI 入口
            └── lib/
                ├── prompt_builder.py  # 模板渲染
                ├── state.py           # 状态管理
                └── validator.py       # Schema 校验
```

---

## Installation / 安装

无需安装。只需 Python 3.10+，零依赖（`jsonschema` 可选，用于强校验）。

```bash
# 可选：安装 jsonschema 获得完整的 JSON Schema 校验
pip3 install jsonschema
```

---

## Usage / 使用

### 单阶段渲染

```bash
python3 scripts/broadcast_craft.py stage <stage_name> \
  --character <主角> --event <事件> \
  [--length <时长>] [--platform <平台>]
```

`stage_name` 支持以下别名：
- `01`, `01_anchor`, `anchor`, `stage_01`, `stage_01_anchor`
- `02`, `02_twist`, `twist`, `stage_02`, `stage_02_twist`
- `03`, `03_hook`, `hook`, `stage_03`, `stage_03_hook`
- `04`, `04_compose`, `compose`, `stage_04`, `stage_04_compose`
- `05`, `05_review`, `review`, `stage_05`, `stage_05_review`

### 校验 JSON 输出

```bash
python3 scripts/broadcast_craft.py validate <stage_name> --file <output.json>
```

### 一键生成全流程 Prompt

```bash
python3 scripts/broadcast_craft.py pipeline \
  --character <主角> --event <事件> \
  [--platform <平台>]
```

生成的 prompt 文件会写入 `.broadcast-craft/staging/` 目录。

---

## Configuration / 配置

无配置文件。所有参数通过 CLI 传入。

状态存储位置：`.broadcast-craft/state/{event}_{protagonist}.json`

---

## Development / 开发

### 添加新分支

1. 在 `branches/` 下创建新目录，结构仿照 `history-twist/`
2. 编写 `methodology.md` 定义分支方法论
3. 在 `templates/prompts/` 中创建分阶段 prompt 模板
4. 在 `templates/schemas/` 中定义 JSON Schema
5. 实现或复用 Python CLI 编排器
6. 在 `SKILL.md` 中注册新分支

### 扩展 Prompt 模板语法

占位符支持以下语法：
- `{{var}}` — 简单变量
- `{{obj.field}}` — 字典属性
- `{{arr[0]}}` — 数组索引
- `{{expr | json}}` — JSON 序列化
- `{{expr | join}}` — 数组转字符串
- `{{arr[index-1]}}` — 简单算术表达式

---

## Roadmap / 路线图

- [x] 通用口播方法论骨架
- [x] 分支一：history-twist 历史反差爆点
- [ ] 分支二：science-twist 科普反差
- [ ] 分支三：figure-twist 人物揭秘
- [ ] 自动化 LLM 调用插件（可选）
- [ ] Web UI 版本

---

## Documentation / 文档

- [通用风格指南](references/style_guide.md)
- [8 种 Hook 钩子模式](references/hook_patterns.md)
- [5 种内容原型](references/content_archetypes.md)
- [四层质检体系](references/quality_matrix.md)
- [历史反差方法论](branches/history-twist/methodology.md)

---

## License / 授权

MIT License

**致谢**：本项目方法论继承自「数字生命卡兹克」的 khazix-writer 内容人格系统，并将其从公众号长文迁移重构为短视频口播体系。
