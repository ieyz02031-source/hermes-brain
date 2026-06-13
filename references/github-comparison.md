# GitHub 热榜项目对比分析

> 更新时间: 2026-06-13
> 数据来源: GitHub API 实时查询

## 第一梯队（6k+⭐）— 行业标杆

| 项目 | ⭐ | 🍴 | 核心功能 |
|------|------|------|----------|
| **claude-seo** | 8,799 | 1,276 | 25 子技能 + 18 子 Agent 的 SEO 套件 |
| **claude-obsidian** | 6,657 | 781 | 自组织 AI 第二大脑，15 个技能，混合检索 |
| **claude-ads** | 5,986 | 906 | 250+ 检查的广告审计 |

## 第二梯队（300-1.2k⭐）— 知识库核心

| 项目 | ⭐ | 🍴 | 核心功能 |
|------|------|------|----------|
| **karpathy-llm-wiki** | 1,076 | 145 | Agent Skills 兼容的 LLM Wiki |
| **claude-blog** | 1,053 | 200 | 30 子技能的博客套件 |
| **llm-wiki-skill** | 582 | 102 | Karpathy 风格知识库 Agent Skill |
| **swarmvault** | 556 | 68 | 本地优先 LLM Wiki，RAG 知识库 |
| **second-brain** | 394 | 72 | LLM 维护的 Obsidian 个人知识库 |
| **llm-wiki** (Pratiyush) | 301 | 48 | 多 Agent 会话自动提取知识库 |

## 第三梯队（50-300⭐）— 工具级

| 项目 | ⭐ | 🍴 | 核心功能 |
|------|------|------|----------|
| **llm-wiki-compiler** | 279 | 31 | 编译 Markdown 到主题 wiki |
| **llm-wikid** | 278 | 26 | Obsidian 的 Karpathy 风格知识库 |
| **llm-wiki** (Vietnamese) | 211 | 94 | 越南语版全自动知识库 |
| **claude-canvas** | 106 | 12 | Obsidian Canvas 可视化 |
| **karpathy-wiki** (toolboxmd) | 85 | 20 | Claude Code 技能，持久化知识库 |
| **llm-wiki-starter** | 79 | 14 | 一条命令创建 LLM Wiki |

## 第四梯队（0-10⭐）— 实验级

| 项目 | ⭐ | 核心功能 |
|------|------|----------|
| **Mycel** | 6 | Rust+Tauri 桌面知识库，图谱视图 |
| **memwiki** | 6 | AI 编码 Agent 的持久化记忆协议 |
| **graph-memory-mcp** | 4 | MCP 协议的知识图谱记忆 |
| **MAX** | 2 | 自主工程 Agent，持久记忆 |
| **uthy-agentic-os** | 2 | 终端 Agent OS，25 主题 |
| **karpathy-hub** | 1 | 主题隔离 Agent + 源到 wiki 管道 |

## Hermes Brain 对比

### 我们的优势

| 优势 | 说明 |
|------|------|
| **Hermes 原生集成** | 直接集成 memory、search_files、read_file、write_file |
| **完整工具链** | 6 个脚本：图谱构建+检索+维护+热缓存+语义索引+自动研究 |
| **四种笔记模板** | 实体/概念/探索/日记 |
| **自进化能力** | discover → suggest → search → extract → create → update 循环 |
| **已验证运行** | 42 个笔记、138 条关联、6 个脚本全部测试通过 |

### 功能矩阵

| 功能 | Hermes Brain | claude-obsidian | karpathy-llm-wiki | swarmvault |
|------|-------------|-----------------|-------------------|------------|
| 知识图谱 | ✅ | ✅ | ✅ | ✅ |
| 语义搜索 | ✅ | ✅ | ❌ | ✅ |
| 热缓存 | ✅ | ✅ | ❌ | ❌ |
| 自动研究 | ✅ | ✅ | ❌ | ❌ |
| 自进化循环 | ✅ | ❌ | ❌ | ❌ |
| Cron 任务 | ✅ | ❌ | ❌ | ❌ |
| 引用验证 | ✅ | ✅ | ✅ | ❌ |
| Hermes 原生 | ✅ | ❌ | ❌ | ❌ |

## 结论

Hermes Brain 的独特定位：
1. **Hermes 原生** — 唯一一个为 Hermes Agent 专门设计的知识管理系统
2. **工具链完整** — 8 个脚本，开箱即用
3. **自进化能力** — discover → suggest → search → extract → create → update 循环
4. **轻量可扩展** — 不依赖外部服务，纯 Python + Markdown + SQLite
