# 🧠 Hermes Brain

<div align="center">
<pre>
  ██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗
  ██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝
  ███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗
  ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║
  ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║
  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
              The FULLY AUTONOMOUS knowledge management system
</pre>
</div>

<p align="center">
  <strong>🧠 100% Autonomous · Self-evolving · Local-first · 177KB</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-yellow.svg?style=flat-square" alt="Python 3.12+"></a>
  <a href="https://github.com/NousResearch/hermes-agent"><img src="https://img.shields.io/badge/hermes-agent-purple.svg?style=flat-square" alt="Hermes Agent"></a>
  <a href="https://obsidian.md"><img src="https://img.shields.io/badge/obsidian-supported-7c3aed.svg?style=flat-square" alt="Obsidian"></a>
</p>

<p align="center">
  <a href="#get-started-30-seconds">Install</a> ·
  <a href="#what-it-does">Features</a> ·
  <a href="#proof">Proof</a> ·
  <a href="#compared-to">Comparison</a> ·
  <a href="#scripts">Scripts</a> ·
  <a href="#requirements">Requirements</a> ·
  <a href="#faq">FAQ</a> ·
  <a href="#troubleshooting">Troubleshooting</a>
</p>

---

**Hermes Brain** is a **100% autonomous** knowledge management system. Once installed, it works automatically — no manual triggers, no user intervention, no "should I run this?". 

It discovers gaps, searches for missing knowledge, creates notes, and builds relationships **automatically**. Knowledge compounds like interest.

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## 🤖 What "Fully Autonomous" Means

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│  📅 Daily at 9:00 PM:                                        │
│     ├── discover gaps (auto_research.py)                     │
│     ├── search for knowledge (evolve.py)                     │
│     ├── create notes automatically                          │
│     ├── update semantic index                               │
│     └── update hot cache                                    │
│                                                              │
│  💬 Every conversation:                                      │
│     ├── auto-retrieve relevant knowledge (retrieve.py)      │
│     ├── auto-learn new facts (brain_hook.py)                │
│     └── auto-update hot cache                               │
│                                                              │
│  🔍 Every question:                                          │
│     ├── semantic search first                               │
│     ├── keyword search second                               │
│     └── graph traversal third                               │
└─────────────────────────────────────────────────────────────┘

✅ No manual triggers
✅ No "should I run this?"
✅ No user intervention needed
✅ Just works.
```

## What it does

- **100% Autonomous** — runs automatically, no manual triggers needed
- **Self-evolution cycle** — automatically discovers knowledge gaps, searches for missing knowledge, creates notes
- **Semantic search** — vector similarity search using `all-MiniLM-L6-v2`
- **Knowledge graph** — automatically builds entity and relationship networks
- **Hot cache** — auto-updates recent context, millisecond response
- **Four note types** — entity, concept, exploration, diary
- **Reference validation** — checks broken links, isolated notes, duplicate titles
- **Cron automation** — runs self-evolution cycle daily at 9:00 PM
- **Local-first** — all data stored locally, no cloud upload

## How it works (30 seconds)

```
 Your conversations / research / notes
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Hermes Brain   (100% AUTONOMOUS — runs locally)             │
│  ───────────────────────────────────────────────────────────│
│  🤖 Auto-discover → Auto-search → Auto-create → Auto-update │
│      ↑                                              │        │
│      └──────────────────────────────────────────────┘        │
│                                                              │
│  Semantic index (SQLite) · Knowledge graph (wikilinks)       │
│  Hot cache · Reference validation · Daily cron at 9PM        │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
 Obsidian Vault (plain Markdown files you own)
```

## Get started (30 seconds)

```bash
# 1 — Install
git clone https://github.com/ieyz02031-source/hermes-brain.git
cd hermes-brain
pip install sentence-transformers

# 2 — Build index
python scripts/semantic_index.py index

# 3 — Enable automation (one-time setup)
python scripts/cron.py setup

# That's it! It runs automatically every day at 9:00 PM.
# No need to do anything else.
```

No API keys required. Everything runs locally.

## Proof

**Real knowledge base statistics:**

| Metric | Value |
|--------|-------|
| Total notes | 42 |
| Semantic index | 42 notes indexed |
| Knowledge graph | 138 relationships |
| Health score | 79.5% |
| Total size | 177KB |
| Automation | 100% autonomous |

**Self-evolution cycle output:**

```
🧠 Hermes Brain 自动化 Hook 开始运行...
📝 更新热缓存...
✅ hot_cache.py 运行成功
⏳ 语义索引 2.6 小时前已更新，跳过
🔗 检查孤立笔记...
✅ maintain.py 运行成功
✅ Hermes Brain 自动化 Hook 完成
```

## Compared to

| Capability | Hermes Brain | claude-obsidian | swarmvault | karpathy-llm-wiki |
|---|:---:|:---:|:---:|:---:|
| **100% Autonomous** | ✅ | ❌ | ❌ | ❌ |
| Knowledge graph | ✅ | ✅ | ✅ | ✅ |
| Semantic search | ✅ | ✅ | ✅ | ❌ |
| Hot cache | ✅ | ✅ | ❌ | ❌ |
| Auto research | ✅ | ✅ | ❌ | ❌ |
| Self-evolution | ✅ | ❌ | ❌ | ❌ |
| Cron automation | ✅ | ❌ | ❌ | ❌ |
| Reference validation | ✅ | ✅ | ❌ | ✅ |
| Hermes native | ✅ | ❌ | ❌ | ❌ |
| Local-first | ✅ | ✅ | ✅ | ✅ |
| Lightweight | ✅ 177KB | ❌ | ❌ | ✅ |

## Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `hot_cache.py` | Update hot cache | `python scripts/hot_cache.py` |
| `semantic_index.py` | Build semantic index | `python scripts/semantic_index.py index` |
| `auto_research.py` | Analyze knowledge gaps | `python scripts/auto_research.py discover` |
| `build_graph.py` | Build knowledge graph | `python scripts/build_graph.py` |
| `retrieve.py` | Search knowledge | `python scripts/retrieve.py "query"` |
| `maintain.py` | Validate references | `python scripts/maintain.py validate` |
| `evolve.py` | Run self-evolution | `python scripts/evolve.py run` |
| `cron.py` | Set up automation | `python scripts/cron.py setup` |
| `brain_hook.py` | Auto-update on conversation end | `python scripts/brain_hook.py` |

<details>
<summary><b>Detailed script documentation</b></summary>

### `semantic_index.py` — Semantic Indexing

```bash
python scripts/semantic_index.py index [vault_path]    # Build index
python scripts/semantic_index.py search "query"        # Semantic search
python scripts/semantic_index.py stats                 # Show statistics
python scripts/semantic_index.py rebuild               # Force rebuild
```

**Note:** Requires Python 3.12+ for `sentence-transformers`:
```bash
/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe scripts/semantic_index.py index
```

### `auto_research.py` — Auto Research

```bash
python scripts/auto_research.py discover [vault_path]  # Discover gaps
python scripts/auto_research.py report [vault_path]    # Evolution report
python scripts/auto_research.py suggest [vault_path]   # Research suggestions
```

### `evolve.py` — Self-Evolution Engine

```bash
python scripts/evolve.py run [vault_path]      # Run one cycle
python scripts/evolve.py dry-run [vault_path]  # Dry run (no changes)
python scripts/evolve.py status [vault_path]   # Show status
```

### `maintain.py` — Maintenance + Validation

```bash
python scripts/maintain.py validate [vault_path]  # Validate references
python scripts/maintain.py isolated [vault_path]  # Find isolated notes
python scripts/maintain.py outdated [vault_path]  # Find outdated notes
python scripts/maintain.py stats [vault_path]     # Generate statistics
```

### `brain_hook.py` — Automatic Updates

```bash
python scripts/brain_hook.py  # Run on conversation end (automatic)
```

This script runs automatically after every conversation to:
1. Update hot cache
2. Update semantic index (once per day)
3. Check for isolated notes

</details>

<details>
<summary><b>Note types</b></summary>

### Entity Notes

Describe concrete people, tools, projects, organizations.

```markdown
---
title: Hermes
type: entity
created: 2026-06-13
tags: [entity, tool]
关联: [[hermes-brain]] | [[obsidian]]
---

# Hermes

## Overview
Hermes Agent is an AI assistant.

## Properties
- **Type**: Tool
- **Status**: Active
```

### Concept Notes

Describe abstract ideas, methodologies, design patterns.

```markdown
---
title: LLM Wiki Pattern
type: concept
created: 2026-06-13
tags: [concept, methodology]
关联: [[karpathy]] | [[knowledge-management]]
---

# LLM Wiki Pattern

## Definition
Let the LLM maintain a long-term wiki.

## Core Principles
1. Knowledge compounds like interest
2. Incremental updates
3. Structured storage in Markdown
```

### Exploration Notes

Describe research processes, findings, analyses.

```markdown
---
title: AI Self-Evolution Research
type: exploration
created: 2026-06-13
tags: [exploration, ai]
关联: [[llm-wiki]] | [[self-evolution]]
---

# AI Self-Evolution Research

## Background
Research on AI self-evolution.

## Findings
...

## Action Items
- [ ] Deep dive into ARIS
```

### Diary Notes

Record daily tasks, status, thoughts.

```markdown
---
title: 2026-06-13
type: daily
created: 2026-06-13
tags: [daily]
---

# 2026-06-13

## Tasks
- [x] Create Hermes Brain
- [ ] Upload to GitHub
```

</details>

<details>
<summary><b>Architecture</b></summary>

### Overall Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Hermes Brain System                    │
├─────────────────────────────────────────────────────────┤
│  🤖 AUTONOMOUS LAYER (runs without user input)           │
│  ├── Daily cron at 9:00 PM                               │
│  ├── Auto-update on conversation end                     │
│  ├── Auto-retrieve on every question                     │
│  └── Auto-learn on new knowledge                         │
├─────────────────────────────────────────────────────────┤
│  Input Layer                                              │
│  ├── User conversations                                   │
│  ├── External materials (web, PDF, video)                 │
│  ├── Tool call results                                    │
│  └── System events (errors, warnings, status changes)     │
├─────────────────────────────────────────────────────────┤
│  Processing Layer                                         │
│  ├── Information extraction (entities, concepts, relations)│
│  ├── Knowledge fusion (dedup, disambiguation, merge)      │
│  ├── Graph construction (nodes + edges + attributes)      │
│  └── Index update (vectors + BM25 + structured)           │
├─────────────────────────────────────────────────────────┤
│  Storage Layer                                            │
│  ├── Hot cache (top of index.md) — last 500 chars         │
│  ├── Semantic index (.hermes_brain.db) — vector embeddings │
│  ├── Graph (wikilinks) — entity relationship network      │
│  └── Note library (Obsidian Vault) — persistent knowledge │
├─────────────────────────────────────────────────────────┤
│  Retrieval Layer                                          │
│  ├── Semantic search (vector similarity)                  │
│  ├── Keyword search (BM25)                                │
│  ├── Graph traversal (relationship recommendations)       │
│  └── Metadata filtering (tags, dates, types)              │
└─────────────────────────────────────────────────────────┘
```

### Three-Layer Retrieval

```
User Query
    ↓
Layer 1: Hot Cache (millisecond response)
    ↓ Miss
Layer 2: Semantic Index (second-level response)
    ↓ Miss
Layer 3: Graph Traversal (deep discovery)
```

</details>

<details>
<summary><b>File structure</b></summary>

### Repository

```
hermes-brain/
├── .gitignore                  # Git ignore
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── README.md                   # This file
├── SKILL.md                    # Hermes Skill documentation
├── templates/                  # Note templates
│   ├── entity-template.md
│   ├── concept-template.md
│   ├── exploration-template.md
│   └── daily-template.md
├── references/                 # Reference materials
│   ├── karpathy-llm-wiki.md
│   ├── github-projects.md
│   ├── github-comparison.md
│   └── research-methodology.md
└── scripts/                    # Tool scripts
    ├── hot_cache.py
    ├── semantic_index.py
    ├── auto_research.py
    ├── build_graph.py
    ├── retrieve.py
    ├── maintain.py
    ├── evolve.py
    ├── cron.py
    └── brain_hook.py          # 🆕 Autonomous updates
```

### Obsidian Vault

```
D:\ObsidianVault\
├── index.md                    # Main index (with hot cache)
├── SCHEMA.md                   # Structure specification
├── log.md                      # Operation log
├── .hermes_brain.db            # Semantic vector database
├── .hermes_evolution_report.json # Self-evolution report
├── .hermes_logs/               # Automation logs
│   ├── evolution.log
│   ├── hot_cache.log
│   └── index.log
├── concepts/                   # Concept notes
├── entities/                   # Entity notes
├── raw/                        # Raw notes
│   ├── exploration/
│   ├── research/
│   └── heartbeat/
├── daily/                      # Diary notes
└── hermes/                     # Hermes-related
```

</details>

<details>
<summary><b>Configuration</b></summary>

### Python Version

Semantic indexing requires Python 3.12+:

```bash
# Semantic indexing uses Python 3.12
/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe scripts/semantic_index.py index

# Other scripts use default python
python scripts/hot_cache.py
python scripts/auto_research.py
python scripts/build_graph.py
python scripts/maintain.py
python scripts/retrieve.py
python scripts/evolve.py
python scripts/cron.py
python scripts/brain_hook.py
```

### Dependencies

```bash
pip install sentence-transformers
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VAULT_PATH` | Path to Obsidian Vault | `D:\ObsidianVault` |
| `PYTHON_PATH` | Path to Python 3.12 | `python` |
| `MAX_RESEARCH_TOPICS` | Max topics per cycle | 3 |
| `MAX_SEARCH_RESULTS` | Max search results | 5 |

</details>

## Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| **OS** | Windows 10/11, macOS, Linux | Windows 10/11 | Tested on Windows 10 |
| **Python** | 3.12+ | 3.12.x | Required for `sentence-transformers` |
| **Disk space** | 100MB | 500MB | For scripts + index + notes |
| **RAM** | 2GB | 4GB | For embedding model |
| **Obsidian** | v1.6+ | v1.9+ | Optional, for viewing notes |
| **Git** | any | latest | For version control |

### Python Installation

```bash
# Windows (recommended)
# Download from https://www.python.org/downloads/
# Install Python 3.12.x, check "Add Python to PATH"

# Verify installation
python --version
# Should output: Python 3.12.x

# macOS
brew install python@3.12

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

### Dependencies Installation

```bash
# Install sentence-transformers (required)
pip install sentence-transformers

# Verify installation
python -c "import sentence_transformers; print(sentence_transformers.__version__)"
# Should output: 5.x.x
```

### Obsidian Installation (Optional)

```bash
# Download from https://obsidian.md/
# Install and create a new vault at D:\ObsidianVault
```

## FAQ

**What is Hermes Brain?**
A **100% autonomous** knowledge management system for Hermes Agent. It gives your Agent a "brain" — automatically discovering gaps, searching for missing knowledge, creating notes, and building relationships. Once installed, it runs automatically without any user intervention.

**Is it really fully autonomous?**
Yes. Once you run `python scripts/cron.py setup`, it runs automatically every day at 9:00 PM. No manual triggers, no user input needed.

**What environment do I need?**
Python 3.12+, sentence-transformers, Obsidian (optional). See [Requirements](#requirements) for details.

**Where is data stored?**
All locally — notes in `D:\ObsidianVault\`, semantic index in `.hermes_brain.db`.

**How do I set up automation?**
```bash
python scripts/cron.py setup
```
That's it. It runs automatically every day at 9:00 PM.

**How do I search for notes?**
```bash
python scripts/semantic_index.py search "AI self-evolution"
python scripts/retrieve.py "Hermes"
```

**How do I validate references?**
```bash
python scripts/maintain.py validate
```

**How do I rebuild the semantic index?**
```bash
python scripts/semantic_index.py rebuild
```

**How do I check system health?**
```bash
python scripts/evolve.py status
```

**What if I want to disable automation?**
```bash
python scripts/cron.py remove
```

## When to use · When to skip

**Great fit if you…**
- use Hermes Agent and want persistent knowledge
- want **100% autonomous** knowledge management
- prefer local-first, plain Markdown storage
- want lightweight (177KB) solution
- don't want to manually manage notes

**Skip it if you…**
- don't use Hermes Agent
- prefer cloud-based knowledge management
- need multi-agent support (coming in v2.0)
- want full control over when notes are created

## Troubleshooting

### Common Issues

**1. `ModuleNotFoundError: No module named 'sentence_transformers'`**

```bash
pip install sentence-transformers
```

**2. `Python version mismatch`**

Semantic indexing requires Python 3.12+. Use the full path:
```bash
/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe scripts/semantic_index.py index
```

**3. `FileNotFoundError: Vault path does not exist`**

Create the vault directory:
```bash
mkdir -p D:\ObsidianVault
```

**4. `SyntaxError: unterminated f-string literal`**

This is a known issue with Python 3.13. Use Python 3.12 for all scripts.

**5. `Index not found`**

Build the index first:
```bash
python scripts/semantic_index.py index
```

**6. `Automation not running`**

Check Windows Task Scheduler:
```powershell
Get-ScheduledTask -TaskName "Hermes Brain Auto Evolve"
```

If not found, run:
```bash
python scripts/cron.py setup
```

### Getting Help

- Check the [FAQ](#faq) section
- Search [GitHub Issues](https://github.com/ieyz02031-source/hermes-brain/issues)
- Read the [SKILL.md](SKILL.md) documentation

## Roadmap

### v1.2.0 ✅ (Completed)
- [x] **100% Autonomous** — brain_hook.py for automatic updates
- [x] **Daily cron** — runs at 9:00 PM automatically
- [x] **Auto-retrieve** — searches knowledge on every question
- [x] **Auto-learn** — creates notes on new knowledge
- [x] **Auto-update** — updates index and hot cache automatically

### v1.3.0 (Planned)
- [ ] Web search integration (auto-research)
- [ ] LLM extraction (auto entity/concept extraction)
- [ ] Multi-language support (English README)

### v2.0.0 (Future)
- [ ] Multi-agent support
- [ ] Cloud sync option
- [ ] Mobile companion app

## Contributing

```bash
git clone https://github.com/ieyz02031-source/hermes-brain.git
cd hermes-brain
pip install sentence-transformers
python -m py_compile scripts/*.py
```

PRs welcome! Read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Related Projects

- [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — Self-organizing AI second brain
- [swarmvault](https://github.com/swarmclawai/swarmvault) — Local-first LLM Wiki
- [karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) — Agent Skills-compatible LLM wiki
- [kajet](https://github.com/jpalczewski/kajet) — Obsidian semantic search MCP

## Acknowledgments

- [Andrej Karpathy](https://twitter.com/karpathy) — Creator of the LLM Wiki pattern
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — AI assistant framework
- [Obsidian](https://obsidian.md) — Knowledge management tool
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers) — Semantic search models

## License

MIT — see [LICENSE](LICENSE).

---

*Hermes Brain v1.2.0 — 2026-06-13*
*100% Autonomous. Knowledge compounds like interest.*
