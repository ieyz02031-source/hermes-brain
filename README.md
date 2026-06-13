# 🧠 Hermes Brain

<div align="center">
<pre>
  ██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗
  ██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝
  ███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗
  ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║
  ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║
  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
              The knowledge management system for AI agents
</pre>
</div>

<p align="center">
  <strong>Self-evolving knowledge graph · semantic search · local-first · 177KB</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-yellow.svg?style=flat-square" alt="Python 3.12+"></a>
  <a href="https://github.com/NousResearch/hermes-agent"><img src="https://img.shields.io/badge/hermes-agent-purple.svg?style=flat-square" alt="Hermes Agent"></a>
  <a href="https://obsidian.md"><img src="https://img.shields.io/badge/obsidian-supported-7c3aed.svg?style=flat-square" alt="Obsidian"></a>
</p>

---

**Hermes Brain** turns your AI agent's conversations, research, and notes into a durable, self-evolving knowledge graph. It discovers gaps, searches for missing knowledge, and fills them automatically — knowledge compounds like interest.

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## What it does

- **Self-evolution cycle** — automatically discovers knowledge gaps, searches for missing knowledge, creates notes
- **Semantic search** — vector similarity search using `all-MiniLM-L6-v2`
- **Knowledge graph** — automatically builds entity and relationship networks
- **Hot cache** — auto-updates recent context, millisecond response
- **Four note types** — entity, concept, exploration, diary
- **Reference validation** — checks broken links, isolated notes, duplicate titles
- **Cron automation** — runs self-evolution cycle daily
- **Local-first** — all data stored locally, no cloud upload

## Get started (30 seconds)

```bash
# 1 — Install
git clone https://github.com/ieyz02031-source/hermes-brain.git
cd hermes-brain
pip install sentence-transformers

# 2 — Build index
python scripts/semantic_index.py index

# 3 — Run self-evolution
python scripts/evolve.py run
```

No API keys required. Everything runs locally.

## Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| **OS** | Windows 10/11, macOS, Linux | Windows 10/11 | Tested on Windows 10 |
| **Python** | 3.12+ | 3.12.x | Required for `sentence-transformers` |
| **Disk space** | 100MB | 500MB | For scripts + index + notes |
| **RAM** | 2GB | 4GB | For embedding model |
| **Obsidian** | v1.6+ | v1.9+ | Optional, for viewing notes |

## License

MIT — see [LICENSE](LICENSE).

---

*Hermes Brain v1.1.0 — 2026-06-13*
*Based on Andrej Karpathy's LLM Wiki pattern. Knowledge compounds like interest.*
