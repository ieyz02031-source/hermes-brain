---
name: hermes-brain
description: "Hermes Brain — The knowledge management system for Hermes Agent based on Karpathy's LLM Wiki pattern"
trigger: "When you need to manage knowledge, retrieve memories, organize notes, build relationship graphs, or make knowledge-driven decisions"
version: "1.1.0"
created: 2026-06-13
tags: [knowledge-management, memory, graph, obsidian, RAG, second-brain]
---

# Hermes Brain

> The knowledge management system for Hermes Agent based on Karpathy's LLM Wiki pattern

## Core Philosophy

**Karpathy LLM Wiki Pattern**: Don't go back to raw sources every time. Instead, let the LLM maintain a long-term wiki. Knowledge compounds like interest.

**Three Pillars**:
1. **Memory Layer** — Short-term (hot cache) + Medium-term (session memory) + Long-term (persistent knowledge)
2. **Knowledge Graph** — Entities + Concepts + Relationship network
3. **Retrieval Layer** — Semantic search + BM25 + Graph traversal

---

## Scripts

All scripts are located in `D:\Hermes\skills\hermes-brain\scripts\`

### 1. Hot Cache (`hot_cache.py`)

```bash
python scripts/hot_cache.py
```

### 2. Semantic Index (`semantic_index.py`)

```bash
python scripts/semantic_index.py index    # Build index
python scripts/semantic_index.py search "query"  # Semantic search
python scripts/semantic_index.py stats    # Show statistics
```

### 3. Auto Research (`auto_research.py`)

```bash
python scripts/auto_research.py discover  # Discover gaps
python scripts/auto_research.py report    # Evolution report
python scripts/auto_research.py suggest   # Research suggestions
```

### 4. Knowledge Graph (`build_graph.py`)

```bash
python scripts/build_graph.py
```

### 5. Knowledge Retrieval (`retrieve.py`)

```bash
python scripts/retrieve.py "query"
```

### 6. Knowledge Maintenance (`maintain.py`)

```bash
python scripts/maintain.py validate   # Validate references
python scripts/maintain.py isolated   # Find isolated notes
python scripts/maintain.py stats      # Generate statistics
```

### 7. Self-Evolution Engine (`evolve.py`)

```bash
python scripts/evolve.py run      # Run one cycle
python scripts/evolve.py dry-run  # Dry run
python scripts/evolve.py status   # Show status
```

### 8. Cron Automation (`cron.py`)

```bash
python scripts/cron.py setup    # Set up cron task
python scripts/cron.py remove   # Remove cron task
python scripts/cron.py status   # Check cron status
python scripts/cron.py run      # Manual run
```

---

## Key Pitfalls

### 1. Never use C drive paths

User explicitly rejects C drive storage. All files must be on D drive:
- **Skill directory**: `D:\Hermes\skills\hermes-brain\`
- **Notes library**: `D:\ObsidianVault\`
- **Project directory**: `D:\Hermes\`

### 2. Python 3.12 vs 3.13 environment

Semantic indexing requires Python 3.12 environment because `sentence-transformers` is installed in Python 3.12:

```bash
# Semantic indexing uses Python 3.12
/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe scripts/semantic_index.py index

# Other scripts use default python
python scripts/hot_cache.py
python scripts/auto_research.py
```

### 3. No real newlines in f-strings

Python f-strings cannot have real newlines, must use `\n`:
```python
# ❌ Wrong
print(f"
{text}")

# ✅ Correct
print(f"\n{text}")
```
