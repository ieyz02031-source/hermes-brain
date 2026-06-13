# GitHub 知识管理项目汇总

> 更新时间: 2026-06-13

## 核心项目

### 1. claude-obsidian — 自组织 AI 第二大脑

- **GitHub**: https://github.com/AgriciDaniel/claude-obsidian
- **Stars**: 6,657
- **功能**: 
  - 15 个 Claude Code 技能
  - 自动研究循环（`/autoresearch`）
  - 知识图谱可视化
  - 混合检索（BM25 + 余弦重排序）
  - 热缓存（`hot.md`）+ 索引（`index.md`）+ 日志（`log.md`）
  - 方法论模式（LYT/PARA/Zettelkasten）
- **适合 Hermes**: 架构设计可以借鉴
- **安装**: 需要 Claude Code 环境

### 2. swarmvault — 本地优先 LLM Wiki

- **GitHub**: https://github.com/swarmclawai/swarmvault
- **Stars**: 556
- **功能**:
  - 本地优先的知识图谱构建器
  - RAG 知识库
  - Agent 记忆存储
  - 基于 Karpathy 的 LLM Wiki 模式
- **适合 Hermes**: 作为知识库后端

### 3. kajet — Obsidian 语义搜索 MCP 服务器

- **GitHub**: https://github.com/jpalczewski/kajet
- **功能**:
  - 12 个 MCP 工具（语义搜索、笔记编辑、vault 探索）
  - 本地嵌入（AllMiniLM-L6-v2），Metal GPU 加速
  - 增量索引，只重新嵌入变化的文件
  - Web 仪表板，实时 MCP 事件流
  - 单一二进制文件，零运行时依赖
- **适合 Hermes**: 直接作为 MCP 服务器接入
- **安装**: 需要从源码编译（Rust + Deno）

### 4. Karpathy-wiki-graph — 企业级知识图谱 Agent

- **GitHub**: https://github.com/LCccode/Karpathy-wiki-graph
- **功能**:
  - CLI-atomic，可插入的技能
  - 支持 Word/PDF/Excel/PPT
  - 三层 wiki：文章 + 概念 + vis-network 图
  - ~10% RAG token 成本
  - 智能增量训练
- **适合 Hermes**: 作为知识图谱构建工具

### 5. graph-memory-mcp — 语义持久化知识图谱记忆

- **GitHub**: https://github.com/river-ai-lab/graph-memory-mcp
- **功能**:
  - 语义、持久化的知识图谱记忆
  - 基于 MCP 协议
  - 支持多 Agent 系统
- **适合 Hermes**: 作为记忆层 MCP 服务器

## 技术趋势

### 1. 三代记忆系统演进

| 代数 | 技术 | 代表项目 | 特点 |
|------|------|---------|------|
| 第一代 | 向量记忆 | LangChain Memory | 简单、易用 |
| 第二代 | 结构化记忆 | MemGPT/Letta, Graphiti | 结构化、可查询 |
| 第三代 | 知识图谱记忆 | Zep, EverMemOS | 语义、关联、时序 |

### 2. Karpathy LLM Wiki 模式

- **核心思想**: 别每次都去翻原始资料，而是让 LLM 一点点维护一个长期的 wiki
- **实现方式**: 增量更新 + 结构化存储 + 关联网络 + 检索增强
- **代表项目**: claude-obsidian, swarmvault, Karpathy-wiki-graph

### 3. MCP 协议标准化

- **趋势**: 越来越多的工具支持 MCP 协议
- **优势**: 标准化、可互操作、易于集成
- **代表项目**: kajet, graph-memory-mcp

## 选型建议

### 对于 Hermes

1. **短期**: 借鉴 claude-obsidian 的架构设计
2. **中期**: 安装 kajet 作为 MCP 服务器
3. **长期**: 构建完整的知识图谱系统
