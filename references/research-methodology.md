# GitHub 研究方法论

> 用于知识管理系统选型和对比分析

## 研究流程

### 1. 搜索阶段

使用 GitHub 搜索相关项目：

```python
# 搜索关键词组合
queries = [
    "LLM wiki knowledge base Karpathy",
    "agent memory knowledge graph second brain",
    "semantic search markdown notes local embedding RAG",
    "AI agent persistent memory system",
]
```

### 2. 数据收集阶段

获取项目信息：

```python
# 获取项目基本信息
for project in projects:
    # Stars, Forks, Description
    curl -s "https://api.github.com/repos/{owner}/{repo}"
    
    # README 内容
    mcp_github_get_file_contents(owner=owner, repo=repo, path="README.md")
```

### 3. 对比分析阶段

创建对比矩阵：

| 维度 | 说明 |
|------|------|
| **Stars** | 项目热度 |
| **Forks** | 社区参与度 |
| **功能矩阵** | 核心功能对比 |
| **技术栈** | 使用的技术 |
| **适用场景** | 适合什么用户 |
| **与目标的关系** | 竞品/互补/参考 |

### 4. 输出阶段

生成结构化报告：

1. **梯队划分** — 按 Stars 分为 4 个梯队
2. **功能矩阵** — 核心功能对比表
3. **优劣势分析** — 我们有什么、缺什么
4. **优先级路线图** — 需要补什么功能

## 输出格式

### 对比表格

| 项目 | ⭐ | 🍴 | 核心功能 | 与目标对比 |
|------|------|------|----------|-----------|
| **项目名** | Stars | Forks | 功能描述 | 优势/劣势 |

### 功能矩阵

| 功能 | 我们 | 竞品A | 竞品B | 竞品C |
|------|------|-------|-------|-------|
| 功能1 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### 优先级路线图

| 优先级 | 功能 | 预计工作量 | 参考实现 |
|--------|------|-----------|---------|
| 🔴 P0 | 功能名 | 时间 | 参考项目 |
| 🟡 P1 | 功能名 | 时间 | 参考项目 |
| 🟢 P2 | 功能名 | 时间 | 参考项目 |
