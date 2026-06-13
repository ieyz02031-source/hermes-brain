#!/usr/bin/env python3
"""
Hermes Brain - Auto Research

Analyzes existing knowledge, discovers gaps, generates research suggestions.

Usage:
    python auto_research.py discover [vault_path]  # Discover gaps
    python auto_research.py report [vault_path]    # Evolution report
    python auto_research.py suggest [vault_path]   # Research suggestions
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict


def extract_wikilinks(content: str) -> List[str]:
    """Extract wikilinks"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


def extract_tags(content: str) -> List[str]:
    """Extract tags"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


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


def print_gaps(gaps: Dict):
    """Print knowledge gaps"""
    print(f"\n{'='*60}")
    print("🔍 Knowledge Gap Analysis")
    print(f"{'='*60}")
    
    # Isolated notes
    if gaps['isolated']:
        print(f"\n🏝️ Isolated Notes ({len(gaps['isolated'])}):")
        for item in gaps['isolated'][:5]:
            print(f"  - {item['title']}: {item['reason']}")
        if len(gaps['isolated']) > 5:
            print(f"  - ... and {len(gaps['isolated']) - 5} more")
    
    # Thin notes
    if gaps['thin']:
        print(f"\n📝 Thin Notes ({len(gaps['thin'])}):")
        for item in gaps['thin'][:5]:
            print(f"  - {item['title']}: {item['reason']}")
        if len(gaps['thin']) > 5:
            print(f"  - ... and {len(gaps['thin']) - 5} more")
    
    # Missing concepts
    if gaps['missing_concepts']:
        print(f"\n❓ Missing Concepts ({len(gaps['missing_concepts'])}):")
        for item in gaps['missing_concepts'][:10]:
            print(f"  - {item['name']}: {item['reason']}")
        if len(gaps['missing_concepts']) > 10:
            print(f"  - ... and {len(gaps['missing_concepts']) - 10} more")
    
    # Tag gaps
    if gaps['tag_gaps']:
        print(f"\n🏷️ Tag Gaps ({len(gaps['tag_gaps'])}):")
        for item in gaps['tag_gaps'][:5]:
            print(f"  - {item['tag']}: {item['reason']}")
    
    # Topic gaps
    if gaps['topic_gaps']:
        print(f"\n📚 Topic Gaps ({len(gaps['topic_gaps'])}):")
        for item in gaps['topic_gaps']:
            print(f"  - {item['domain']}: {item['reason']}")
    
    # Summary
    total_gaps = sum(len(v) for v in gaps.values())
    print(f"\n{'='*60}")
    print(f"📊 Total: {total_gaps} knowledge gaps")
    print(f"{'='*60}")


def print_suggestions(suggestions: List[Dict]):
    """Print research suggestions"""
    print(f"\n{'='*60}")
    print("💡 Research Suggestions")
    print(f"{'='*60}")
    
    if not suggestions:
        print("  No topics need research")
        return
    
    # Group by priority
    high = [s for s in suggestions if s['priority'] == 'high']
    medium = [s for s in suggestions if s['priority'] == 'medium']
    low = [s for s in suggestions if s['priority'] == 'low']
    
    if high:
        print(f"\n🔴 High Priority:")
        for s in high:
            print(f"  - {s['topic']}: {s['reason']}")
    
    if medium:
        print(f"\n🟡 Medium Priority:")
        for s in medium:
            print(f"  - {s['topic']}: {s['reason']}")
    
    if low:
        print(f"\n🟢 Low Priority:")
        for s in low[:5]:
            print(f"  - {s['topic']}: {s['reason']}")


def generate_evolution_report(vault_path: Path) -> Dict:
    """Generate evolution report"""
    notes = scan_vault(vault_path)
    gaps = analyze_knowledge_gaps(notes)
    suggestions = suggest_research_topics(gaps)
    
    # Calculate health score
    total_notes = len(notes)
    isolated_count = len(gaps['isolated'])
    thin_count = len(gaps['thin'])
    missing_count = len(gaps['missing_concepts'])
    
    # Health score = 100 - (problems / total notes * 100)
    problem_count = isolated_count + thin_count + missing_count
    health_score = max(0, 100 - (problem_count / max(total_notes, 1) * 100))
    
    return {
        'timestamp': datetime.now().isoformat(),
        'total_notes': total_notes,
        'health_score': round(health_score, 1),
        'gaps': {k: len(v) for k, v in gaps.items()},
        'suggestions': suggestions,
        'top_issues': gaps['isolated'][:3] + gaps['thin'][:3] + gaps['missing_concepts'][:3],
    }


def print_evolution_report(report: Dict):
    """Print evolution report"""
    print(f"\n{'='*60}")
    print("🧠 Hermes Brain Self-Evolution Report")
    print(f"{'='*60}")
    
    print(f"\n📊 Basic Statistics:")
    print(f"  - Total notes: {report['total_notes']}")
    print(f"  - Health score: {report['health_score']}%")
    
    # Health score visualization
    score = report['health_score']
    if score >= 80:
        status = "🟢 Healthy"
    elif score >= 60:
        status = "🟡 Fair"
    else:
        status = "🔴 Needs attention"
    print(f"  - Status: {status}")
    
    print(f"\n🔍 Gap Statistics:")
    for gap_type, count in report['gaps'].items():
        if count > 0:
            print(f"  - {gap_type}: {count}")
    
    if report['suggestions']:
        print(f"\n💡 Research Suggestions:")
        for s in report['suggestions'][:5]:
            print(f"  - [{s['priority']}] {s['topic']}")
    
    print(f"\n{'='*60}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python auto_research.py discover [vault_path]  # Discover gaps")
        print("  python auto_research.py report [vault_path]    # Evolution report")
        print("  python auto_research.py suggest [vault_path]   # Research suggestions")
        return
    
    command = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    if command == 'discover':
        notes = scan_vault(vault_path)
        gaps = analyze_knowledge_gaps(notes)
        print_gaps(gaps)
    
    elif command == 'report':
        report = generate_evolution_report(vault_path)
        print_evolution_report(report)
    
    elif command == 'suggest':
        notes = scan_vault(vault_path)
        gaps = analyze_knowledge_gaps(notes)
        suggestions = suggest_research_topics(gaps)
        print_suggestions(suggestions)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
