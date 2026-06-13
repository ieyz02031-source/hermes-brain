---
name: hermes-brain
description: "Hermes 大脑系统 — 基于 Karpathy LLM Wiki 模式 + 知识图谱 + 语义检索的 Agent 记忆与知识管理系统"
trigger: "当需要管理知识、检索记忆、整理笔记、构建关联图谱、或进行知识驱动的决策时使用"
version: "1.2.0"
created: 2026-06-13
tags: [knowledge-management, memory, graph, obsidian, RAG, second-brain]
---

# Hermes 大脑系统

> 基于 Karpathy LLM Wiki 模式 + 知识图谱 + 语义检索的 Agent 记忆与知识管理系统

## 核心理念

**Karpathy LLM Wiki 模式**：别每次都去翻原始资料，而是让 LLM 一点点维护一个长期的 wiki。知识像复利一样累积。

**三大支柱**：
1. **记忆层** — 短期（热缓存）+ 中期（会话记忆）+ 长期（持久化知识）
2. **知识图谱** — 实体 + 概念 + 关联关系的网络
3. **检索层** — 语义搜索 + BM25 + 关联图遍历

---

## 架构设计

```
输入层（用户对话、外部资料、工具结果、系统事件）
    ↓
处理层（信息抽取、知识融合、图谱构建、索引更新）
    ↓
存储层（热缓存、索引、图谱、日志、笔记库）
    ↓
检索层（语义搜索、关键词搜索、图谱遍历、元数据过滤）
    ↓
输出层（回答、建议、洞察、行动）
```

---

## 笔记结构规范

### 实体笔记

描述具体的人、工具、项目、组织。

```markdown
---
title: [实体名称]
type: entity
created: YYYY-MM-DD
tags: [entity, 类别]
关联: [[相关笔记1]] | [[相关笔记2]]
---

# [实体名称]

## 概述
简要描述这个实体是什么。

## 属性
- **类型**: 人/工具/项目/组织
- **状态**: 活跃/归档/废弃

## 关联
- [[相关实体1]] — 关系描述
```

### 概念笔记

描述抽象的想法、方法论、设计模式。

```markdown
---
title: [概念名称]
type: concept
created: YYYY-MM-DD
tags: [concept, 领域]
关联: [[相关笔记1]] | [[相关笔记2]]
---

# [概念名称]

## 定义
清晰定义这个概念。

## 核心原则
1. 原则1
2. 原则2

## 相关概念
- [[相关概念1]] — 关系描述
```

### 探索笔记

描述研究过程、发现、分析。

```markdown
---
title: [探索主题]
type: exploration
created: YYYY-MM-DD
tags: [exploration, 主题]
关联: [[相关笔记1]] | [[相关笔记2]]
---

# [探索主题]

## 背景
为什么进行这次探索。

## 发现
详细描述。

## 行动项
- [ ] 行动1
- [ ] 行动2
```

### 日记笔记

记录日常任务、状态、思考。

```markdown
---
title: YYYY-MM-DD
type: daily
created: YYYY-MM-DD
tags: [daily]
---

# YYYY-MM-DD

## 任务
- [x] 完成的任务
- [ ] 未完成的任务
```

---

## 脚本工具

所有脚本位于 `D:\Hermes\skills\hermes-brain\scripts\`

### 1. 热缓存 (`hot_cache.py`)

自动扫描最近修改的笔记，更新 `index.md` 顶部的热缓存区域。

```bash
python scripts/hot_cache.py
```

### 2. 语义索引 (`semantic_index.py`)

用 `all-MiniLM-L6-v2` 模型生成笔记的向量嵌入，存储到 SQLite，支持语义相似度搜索。

```bash
python scripts/semantic_index.py index    # 构建索引
python scripts/semantic_index.py search "查询内容"  # 语义搜索
python scripts/semantic_index.py stats    # 显示统计
```

### 3. 自动研究 (`auto_research.py`)

分析现有知识，发现空白和薄弱点，生成研究建议。

```bash
python scripts/auto_research.py discover  # 发现知识空白
python scripts/auto_research.py report    # 自进化报告
python scripts/auto_research.py suggest   # 研究建议
```

### 4. 知识图谱 (`build_graph.py`)

从 Obsidian Vault 中抽取实体和关系，构建知识图谱。

```bash
python scripts/build_graph.py
```

### 5. 知识检索 (`retrieve.py`)

三层检索（热缓存、索引、图谱），返回相关笔记。

```bash
python scripts/retrieve.py "查询内容"
```

### 6. 知识维护 (`maintain.py`)

孤立检测、关联推荐、过期清理、统计报告、引用验证。

```bash
python scripts/maintain.py validate   # 验证引用
python scripts/maintain.py isolated   # 找出孤立笔记
python scripts/maintain.py stats      # 生成统计
```

### 7. 自进化引擎 (`evolve.py`)

完整的自进化循环：发现空白 → 搜索补充 → 创建笔记 → 更新索引 → 更新热缓存。

```bash
python scripts/evolve.py run      # 运行一次自进化循环
python scripts/evolve.py dry-run  # 干运行（不创建笔记）
python scripts/evolve.py status   # 显示自进化状态
```

### 8. Cron 任务 (`cron.py`)

每天自动运行自进化循环。

```bash
python scripts/cron.py setup    # 设置 cron 任务
python scripts/cron.py remove   # 移除 cron 任务
python scripts/cron.py status   # 查看 cron 状态
python scripts/cron.py run      # 手动运行一次
```

### 9. 自动化 Hook (`brain_hook.py`)

在每次对话结束时自动运行，更新热缓存和索引。

```bash
python scripts/brain_hook.py
```

---

## 自进化循环

```
discover（发现空白）
    ↓
suggest（生成建议）
    ↓
web_search（搜索补充）
    ↓
LLM 抽取（实体和概念）
    ↓
创建笔记（write_file）
    ↓
更新索引（semantic_index.py）
    ↓
更新热缓存（hot_cache.py）
    ↓
回到 discover
```

---

## 自动化触发器

### 对话结束时自动运行

在每次对话结束时，Hermes Agent 应该自动运行：

```python
# 在对话结束时自动运行
import subprocess
result = subprocess.run([
    r"C:\Users\20716\AppData\Local\Programs\Python\Python312\python.exe",
    r"D:\Hermes\skills\hermes-brain\scripts\brain_hook.py"
], capture_output=True, text=True, timeout=60)
```

### 检索时自动触发

当用户提问时，Hermes Agent 应该自动检索相关知识：

```bash
# 在回答问题前自动检索
python scripts/retrieve.py "用户的问题"
```

### 学习时自动创建笔记

当 Hermes Agent 学到新知识时，应该自动创建笔记：

```bash
# 在学习新知识后自动创建笔记
python scripts/evolve.py run
```

---

## 自动化工作流

```
用户提问
    ↓
自动检索（retrieve.py）
    ↓
回答问题
    ↓
学习新知识
    ↓
自动创建笔记（evolve.py）
    ↓
更新索引（semantic_index.py）
    ↓
更新热缓存（hot_cache.py）
    ↓
等待下一次提问
```

---

## 完全自动化的关键

1. **不要手动触发** — 所有脚本应该在后台自动运行
2. **不要问用户** — 自动运行，不要问"要我运行吗"
3. **不要分步** — 一次性完成所有操作
4. **不要留 TODO** — 所有功能必须完整实现

---

## 工具集成

### Obsidian 集成

笔记存储位置：`D:\ObsidianVault\`

```
D:\ObsidianVault\
├── index.md              # 主索引
├── SCHEMA.md             # 结构规范
├── log.md                # 操作日志
├── concepts/             # 概念笔记
├── entities/             # 实体笔记
├── raw/                  # 原始笔记
│   ├── exploration/      # 探索笔记
│   ├── research/         # 研究笔记
│   └── heartbeat/        # 心跳笔记
├── daily/                # 日记
└── hermes/               # Hermes 相关
```

### 记忆工具集成

```bash
memory(action='add', target='memory', content='...')
memory(action='replace', target='memory', old_text='...', new_text='...')
memory(action='remove', target='memory', old_text='...')
```

### 检索工具集成

```bash
search_files(pattern='...', target='content', path='D:\\ObsidianVault')
read_file(path='D:\\ObsidianVault\\index.md')
write_file(path='D:\\ObsidianVault\\new-note.md', content='...')
```

---

## 最佳实践

### 笔记命名规范

- **实体笔记**: `tool-name.md`, `person-name.md`, `project-name.md`
- **概念笔记**: `concept-name.md`, `methodology-name.md`
- **探索笔记**: `YYYY-MM-DD-exploration-topic.md`
- **日记**: `YYYY-MM-DD.md`

### 标签使用规范

- 每个笔记最多 3 个标签
- 标签按用途分类，不是按主题
- 新标签必须在 SCHEMA.md 中注册

### 关联维护规范

- 每个笔记至少有 1 个关联
- 关联关系要有描述（不只是链接）
- 定期检查关联的有效性

### 热缓存更新规范

- 每次会话后更新热缓存
- 热缓存只保留最近 500 字
- 热缓存是最近上下文的摘要

---

## ⚠️ 关键 Pitfall

### 0. 一口气做完，不留"下一步"

用户明确拒绝任何形式的"待实现"、"下一步"、"计划中"。必须一次性完成所有功能，不留 TODO。
- ❌ "下一步建议：可以添加 X 功能"
- ❌ "待实现：Y 功能"
- ❌ "计划中：Z 优化"
- ❌ "还有建议或者下一步打算" — 用户说这句话时，意思是"把能做的都做完"

### 1. 不要用 C 盘路径

用户明确拒绝 C 盘存储。所有文件必须放在 D 盘：
- **Skill 目录**: `D:\Hermes\skills\hermes-brain\`
- **笔记库**: `D:\ObsidianVault\`
- **项目目录**: `D:\Hermes\`

### 2. Python 3.12 vs 3.13 环境

语义索引需要 Python 3.12 环境，因为 `sentence-transformers` 装在 Python 3.12 中：

```bash
# 语义索引用 Python 3.12
/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe scripts/semantic_index.py index

# 其他脚本用默认 python
python scripts/hot_cache.py
python scripts/auto_research.py
```

### 3. f-string 中不要有真实换行

Python f-string 不能有真实换行，必须用 `\n`：
```python
# ❌ 错误
print(f"
{text}")

# ✅ 正确
print(f"\n{text}")
```

### 4. 一口气做完，不要分步确认

用户偏好批量处理，不要问"继续吗"、"下一步"、"要我做吗"。一次性完成所有操作，不留"待实现"或"下一步"。

### 5. 不要创建 Web UI / Dashboard

用户明确拒绝 Web UI 仪表板，不要创建 dashboard.py 或类似的可视化工具。

### 6. Skill 自检流程

打包前必须自检：
- 用 `grep "^##"` 检查 SKILL.md 是否有重复章节
- 删除冗余文件（COMPLETION_REPORT.md、README.md 在 skill 目录中不需要）
- `rm -rf scripts/__pycache__` 清理缓存
- 确认所有路径指向 D 盘
- `python -m py_compile scripts/*.py` 语法检查

---

## GitHub 热榜对比

详见 `references/github-comparison.md` — 包含 20+ 个项目的详细对比分析、功能矩阵、优先级路线图。

---

## 参考资源

### GitHub 项目

| 项目 | 描述 | 链接 |
|------|------|------|
| **claude-obsidian** | 自组织 AI 第二大脑 | https://github.com/AgriciDaniel/claude-obsidian |
| **swarmvault** | 本地优先 LLM Wiki | https://github.com/swarmclawai/swarmvault |
| **kajet** | Obsidian 语义搜索 MCP | https://github.com/jpalczewski/kajet |
| **Karpathy-wiki-graph** | 企业级知识图谱 Agent | https://github.com/LCccode/Karpathy-wiki-graph |
| **graph-memory-mcp** | 语义持久化知识图谱记忆 | https://github.com/river-ai-lab/graph-memory-mcp |
| **hermes-cortex** | Hermes 配置、技能、记忆层 | https://github.com/lukemcqueen/hermes-cortex |
| **PRISM** | Agent 无关的编排系统 | https://github.com/racar/PRISM |

### 中文资源

| 资源 | 描述 | 链接 |
|------|------|------|
| **AI Agent 记忆机制综述** | 知乎专栏 | https://zhuanlan.zhihu.com/p/1995813479794353043 |
| **2026年Agent记忆系统方案横评** | 腾讯云 | https://cloud.tencent.com/developer/article/2665379 |
| **AI Agent 记忆技术演进全解析** | CSDN | https://tianqi.csdn.net/69f58bda0a2f6a37c5a756ea.html |
| **Agent Memory 技术演进** | GitHub Blog | https://github.com/kejun/blogpost/blob/main/agent-memory-evolution-2026.md |

### Karpathy LLM Wiki 原文

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## 总结

Hermes 大脑系统是一个**完全自动化**的知识管理系统，它通过：

1. **结构化存储** — 实体、概念、探索、日记四种笔记类型
2. **知识图谱** — 实体 + 关系的网络结构
3. **三层检索** — 热缓存 + 索引 + 图谱的检索架构
4. **自动维护** — 孤立检测、关联推荐、过期清理、引用验证
5. **自进化循环** — discover → suggest → search → extract → create → update
6. **自动化触发** — 对话结束自动更新，提问自动检索，学习自动创建笔记

**不需要手动触发，不需要问用户，不需要分步操作。**
