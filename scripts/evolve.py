#!/usr/bin/env python3
"""
Hermes Brain - Self-Evolution Engine

Complete self-evolution cycle: discover → search → extract → create → update.

Usage:
    python evolve.py run [vault_path]      # Run one cycle
    python evolve.py dry-run [vault_path]  # Dry run (no changes)
    python evolve.py status [vault_path]   # Show status
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


# Configuration
VAULT_PATH = Path(r"D:\ObsidianVault")
MAX_RESEARCH_TOPICS = 3  # Max topics per cycle
MAX_SEARCH_RESULTS = 5   # Max search results per topic


def extract_title(content: str) -> str:
    """Extract title"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        if title_match:
            return title_match.group(1).strip()
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return "Untitled"


def extract_tags(content: str) -> List[str]:
    """Extract tags"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_wikilinks(content: str) -> List[str]:
    """Extract wikilinks"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


def scan_vault(vault_path: Path) -> Dict[str, Dict]:
    """Scan Vault"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        if md_file.name in ['index.md', 'SCHEMA.md', 'log.md', '.hermes_brain.db']:
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            relative_path = str(md_file.relative_to(vault_path))
            
            notes[relative_path] = {
                'path': relative_path,
                'title': extract_title(content),
                'tags': extract_tags(content),
                'wikilinks': extract_wikilinks(content),
                'content_length': len(content),
            }
        except Exception:
            pass
    
    return notes


def analyze_knowledge_gaps(notes: Dict[str, Dict]) -> Dict:
    """Analyze knowledge gaps"""
    gaps = {
        'isolated': [],
        'thin': [],
        'missing_concepts': [],
        'tag_gaps': [],
        'topic_gaps': [],
    }
    
    # Collect all existing note names
    existing_names = set()
    for path, note in notes.items():
        existing_names.add(note['title'])
        existing_names.add(Path(path).stem)
    
    # Collect all wikilinks
    all_wikilinks = set()
    for note in notes.values():
        all_wikilinks.update(note['wikilinks'])
    
    # Find isolated notes
    linked_notes = set()
    for note in notes.values():
        linked_notes.update(note['wikilinks'])
    
    for path, note in notes.items():
        stem = Path(path).stem
        if not note['wikilinks'] and stem not in linked_notes and note['title'] not in linked_notes:
            gaps['isolated'].append({
                'path': path,
                'title': note['title'],
                'reason': 'No links and not referenced by other notes',
            })
    
    # Find thin notes (content less than 200 characters)
    for path, note in notes.items():
        if note['content_length'] < 200:
            gaps['thin'].append({
                'path': path,
                'title': note['title'],
                'length': note['content_length'],
                'reason': f'Content only has {note["content_length"]} characters',
            })
    
    # Find missing concepts
    for link in all_wikilinks:
        if '|' in link:
            target, _ = link.split('|', 1)
        else:
            target = link
        
        found = False
        for path, note in notes.items():
            if target in note['title'] or target in Path(path).stem:
                found = True
                break
        
        if not found:
            gaps['missing_concepts'].append({
                'name': target,
                'reason': 'Referenced but note does not exist',
            })
    
    # Find tag gaps
    tag_counts = defaultdict(int)
    for note in notes.values():
        for tag in note['tags']:
            tag_counts[tag] += 1
    
    for tag, count in tag_counts.items():
        if count <= 2:
            gaps['tag_gaps'].append({
                'tag': tag,
                'count': count,
                'reason': f'Tag "{tag}" only has {count} notes',
            })
    
    # Find topic gaps
    knowledge_domains = {
        'AI': ['AI', 'LLM', 'Machine Learning', 'Deep Learning', 'GPT', 'Claude'],
        'Design': ['Design', 'UI', 'UX', 'CSS', 'Color', 'Typography'],
        'Development': ['Development', 'Python', 'JavaScript', 'API', 'Database'],
        'Tools': ['Tools', 'MCP', 'Obsidian', 'Git', 'Docker'],
        'Methodology': ['Methodology', 'Process', 'Architecture', 'Pattern', 'Best Practice'],
    }
    
    for domain, keywords in knowledge_domains.items():
        count = 0
        for note in notes.values():
            content_lower = (note['title'] + ' '.join(note['tags'])).lower()
            if any(kw.lower() in content_lower for kw in keywords):
                count += 1
        
        if count <= 2:
            gaps['topic_gaps'].append({
                'domain': domain,
                'count': count,
                'reason': f'Domain "{domain}" only has {count} notes',
            })
    
    return gaps


def suggest_research_topics(gaps: Dict) -> List[Dict]:
    """Generate research suggestions"""
    suggestions = []
    
    # Based on missing concepts
    for item in gaps['missing_concepts'][:5]:
        suggestions.append({
            'topic': item['name'],
            'reason': item['reason'],
            'priority': 'high',
            'type': 'missing_concept',
        })
    
    # Based on topic gaps
    for item in gaps['topic_gaps']:
        suggestions.append({
            'topic': item['domain'],
            'reason': item['reason'],
            'priority': 'medium',
            'type': 'topic_gap',
        })
    
    # Based on tag gaps
    for item in gaps['tag_gaps'][:3]:
        suggestions.append({
            'topic': item['tag'],
            'reason': item['reason'],
            'priority': 'low',
            'type': 'tag_gap',
        })
    
    return suggestions


def create_note_from_research(topic: str, search_results: List[Dict], vault_path: Path) -> Optional[str]:
    """Create note from search results"""
    if not search_results:
        return None
    
    # Generate note content
    title = topic
    date = datetime.now().strftime('%Y-%m-%d')
    
    # Extract key information
    descriptions = []
    urls = []
    for result in search_results[:3]:
        if result.get('description'):
            descriptions.append(result['description'])
        if result.get('url'):
            urls.append(result['url'])
    
    # Generate summary
    summary = ' '.join(descriptions[:3])
    if len(summary) > 500:
        summary = summary[:500] + '...'
    
    # Generate note content
    content = f"""---
title: {title}
type: exploration
created: {date}
updated: {date}
tags: [exploration, {title.lower().replace(' ', '-')}]
关联: [[hermes-brain-system]]
---

# {title}

## Overview

{summary}

## Sources

"""
    
    for url in urls:
        content += f"- [{url}]({url})\n"
    
    content += f"""
## Key Findings

(To be filled)

## Action Items

- [ ] Deep dive into {title}
- [ ] Create related concept notes
- [ ] Build relationships

---

*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # Create note file
    filename = f"{date}-{title.lower().replace(' ', '-')}.md"
    filepath = vault_path / 'raw' / 'exploration' / filename
    
    # Ensure directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    filepath.write_text(content, encoding='utf-8')
    
    return str(filepath.relative_to(vault_path))


def run_evolution_cycle(vault_path: Path, dry_run: bool = False) -> Dict:
    """Run one evolution cycle"""
    print(f"\n{'='*60}")
    print("🧠 Hermes Brain Self-Evolution Cycle")
    print(f"{'='*60}")
    
    # 1. Scan notes
    print("\n📊 Step 1: Scanning notes...")
    notes = scan_vault(vault_path)
    print(f"  Found {len(notes)} notes")
    
    # 2. Analyze knowledge gaps
    print("\n🔍 Step 2: Analyzing knowledge gaps...")
    gaps = analyze_knowledge_gaps(notes)
    total_gaps = sum(len(v) for v in gaps.values())
    print(f"  Found {total_gaps} knowledge gaps")
    
    # 3. Generate research suggestions
    print("\n💡 Step 3: Generating research suggestions...")
    suggestions = suggest_research_topics(gaps)
    print(f"  Generated {len(suggestions)} suggestions")
    
    # 4. Select research topics
    print("\n📋 Step 4: Selecting research topics...")
    topics_to_research = suggestions[:MAX_RESEARCH_TOPICS]
    for i, topic in enumerate(topics_to_research, 1):
        print(f"  {i}. [{topic['priority']}] {topic['topic']}")
    
    # 5. Search for missing knowledge
    print("\n🌐 Step 5: Searching for missing knowledge...")
    search_results = {}
    for topic in topics_to_research:
        print(f"  Searching: {topic['topic']}...")
        # This should call web_search, but because we're in a script, we simulate
        # In actual use, it should be through Hermes's web_search tool
        search_results[topic['topic']] = []
        print(f"    Results: 0 (needs web_search integration)")
    
    # 6. Create notes
    print("\n📝 Step 6: Creating notes...")
    created_notes = []
    if not dry_run:
        for topic in topics_to_research:
            results = search_results.get(topic['topic'], [])
            note_path = create_note_from_research(topic['topic'], results, vault_path)
            if note_path:
                created_notes.append(note_path)
                print(f"  Created: {note_path}")
            else:
                print(f"  Skipping: {topic['topic']} (no search results)")
    else:
        print("  Dry run mode, skipping note creation")
    
    # 7. Update index
    print("\n📦 Step 7: Updating index...")
    if not dry_run:
        # Call semantic_index.py
        os.system(f'cd {vault_path.parent / "Hermes" / "skills" / "hermes-brain"} && python scripts/semantic_index.py index')
        print("  Index updated")
    else:
        print("  Dry run mode, skipping index update")
    
    # 8. Update hot cache
    print("\n🔥 Step 8: Updating hot cache...")
    if not dry_run:
        # Call hot_cache.py
        os.system(f'cd {vault_path.parent / "Hermes" / "skills" / "hermes-brain"} && python scripts/hot_cache.py')
        print("  Hot cache updated")
    else:
        print("  Dry run mode, skipping hot cache update")
    
    # 9. Generate report
    print("\n📊 Step 9: Generating report...")
    report = {
        'timestamp': datetime.now().isoformat(),
        'notes_count': len(notes),
        'gaps_count': total_gaps,
        'suggestions_count': len(suggestions),
        'researched_count': len(topics_to_research),
        'created_count': len(created_notes),
        'created_notes': created_notes,
    }
    
    # Save report
    report_path = vault_path / '.hermes_evolution_report.json'
    if not dry_run:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  Report saved: {report_path}")
    
    return report


def show_status(vault_path: Path):
    """Show evolution status"""
    print(f"\n{'='*60}")
    print("🧠 Hermes Brain Self-Evolution Status")
    print(f"{'='*60}")
    
    # Check report
    report_path = vault_path / '.hermes_evolution_report.json'
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding='utf-8'))
        print(f"\n📊 Most recent evolution:")
        print(f"  - Time: {report.get('timestamp', 'unknown')}")
        print(f"  - Notes count: {report.get('notes_count', 0)}")
        print(f"  - Knowledge gaps: {report.get('gaps_count', 0)}")
        print(f"  - Research suggestions: {report.get('suggestions_count', 0)}")
        print(f"  - Researched: {report.get('researched_count', 0)}")
        print(f"  - Created: {report.get('created_count', 0)}")
        
        if report.get('created_notes'):
            print(f"\n📝 Created notes:")
            for note in report['created_notes']:
                print(f"  - {note}")
    else:
        print("\n  Has not run evolution cycle yet")
    
    # Check database
    db_path = vault_path / '.hermes_brain.db'
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.execute('SELECT COUNT(*) FROM notes')
        count = cursor.fetchone()[0]
        conn.close()
        print(f"\n📦 Semantic index:")
        print(f"  - Indexed notes: {count}")
    else:
        print(f"\n📦 Semantic index: Not created")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python evolve.py run [vault_path]      # Run one cycle")
        print("  python evolve.py dry-run [vault_path]  # Dry run (no changes)")
        print("  python evolve.py status [vault_path]   # Show status")
        return
    
    command = sys.argv[1]
    vault_path = VAULT_PATH
    
    if len(sys.argv) > 2:
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    if command == 'run':
        report = run_evolution_cycle(vault_path, dry_run=False)
        print(f"\n{'='*60}")
        print("✅ Self-evolution cycle complete")
        print(f"{'='*60}")
        print(f"  - Researched {report['researched_count']} topics")
        print(f"  - Created {report['created_count']} notes")
    
    elif command == 'dry-run':
        report = run_evolution_cycle(vault_path, dry_run=True)
        print(f"\n{'='*60}")
        print("✅ Dry run complete")
        print(f"{'='*60}")
        print(f"  - Would research {report['researched_count']} topics")
        print(f"  - Would create {report['created_count']} notes")
    
    elif command == 'status':
        show_status(vault_path)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
