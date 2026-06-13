#!/usr/bin/env python3
"""
Hermes Brain - Knowledge Maintenance

Isolated detection, link recommendation, staleness check, reference validation.

Usage:
    python maintain.py validate [vault_path]  # Validate references
    python maintain.py isolated [vault_path]  # Find isolated notes
    python maintain.py outdated [vault_path]  # Find outdated notes
    python maintain.py stats [vault_path]     # Generate statistics
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
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
    return "Untitled"


def scan_vault(vault_path: Path) -> Dict[str, Dict]:
    """Scan Vault"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        if md_file.name in ['index.md', 'SCHEMA.md', 'log.md']:
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            relative_path = str(md_file.relative_to(vault_path))
            
            notes[relative_path] = {
                'path': str(md_file),
                'title': extract_title(content),
                'tags': extract_tags(content),
                'wikilinks': extract_wikilinks(content),
                'content_length': len(content),
                'mtime': datetime.fromtimestamp(md_file.stat().st_mtime).strftime('%Y-%m-%d'),
            }
        except Exception:
            pass
    
    return notes


def find_isolated_notes(notes: Dict[str, Dict]) -> List[str]:
    """Find isolated notes"""
    linked_notes = set()
    for note in notes.values():
        for wikilink in note['wikilinks']:
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            linked_notes.add(target)
    
    isolated = []
    for path, note in notes.items():
        stem = Path(path).stem
        if not note['wikilinks'] and stem not in linked_notes and note['title'] not in linked_notes:
            isolated.append(path)
    
    return isolated


def validate_references(vault_path: Path) -> Dict:
    """Validate references"""
    notes = scan_vault(vault_path)
    issues = {
        'broken_links': [],
        'orphan_notes': [],
        'duplicate_titles': [],
    }
    
    title_to_paths = defaultdict(list)
    for path, note in notes.items():
        title_to_paths[note['title']].append(path)
    
    for title, paths in title_to_paths.items():
        if len(paths) > 1:
            issues['duplicate_titles'].append({
                'title': title,
                'paths': paths,
                'reason': f'Title "{title}" appears in {len(paths)} files',
            })
    
    for path, note in notes.items():
        for wikilink in note.get('wikilinks', []):
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            found = False
            for other_path, other_note in notes.items():
                if target in other_note['title'] or target in Path(other_path).stem:
                    found = True
                    break
            
            if not found:
                issues['broken_links'].append({
                    'source': path,
                    'target': target,
                    'reason': f'Link [[{target}]] does not exist',
                })
    
    linked_notes = set()
    for note in notes.values():
        for wikilink in note.get('wikilinks', []):
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            linked_notes.add(target)
    
    for path, note in notes.items():
        stem = Path(path).stem
        if not note.get('wikilinks') and stem not in linked_notes and note['title'] not in linked_notes:
            issues['orphan_notes'].append({
                'path': path,
                'title': note['title'],
                'reason': 'No links and not referenced by other notes',
            })
    
    return issues


def print_reference_issues(issues: Dict):
    """Print reference issues"""
    print(f"\n{'='*60}")
    print("🔗 Reference Validation Report")
    print(f"{'='*60}")
    
    if issues['broken_links']:
        print(f"\n❌ Broken Links ({len(issues['broken_links'])}):")
        for item in issues['broken_links'][:10]:
            print(f"  - {item['source']}: {item['reason']}")
        if len(issues['broken_links']) > 10:
            print(f"  - ... and {len(issues['broken_links']) - 10} more")
    else:
        print(f"\n✅ No broken links")
    
    if issues['orphan_notes']:
        print(f"\n🏝️ Orphan Notes ({len(issues['orphan_notes'])}):")
        for item in issues['orphan_notes'][:10]:
            print(f"  - {item['title']}: {item['reason']}")
        if len(issues['orphan_notes']) > 10:
            print(f"  - ... and {len(issues['orphan_notes']) - 10} more")
    else:
        print(f"\n✅ No orphan notes")
    
    if issues['duplicate_titles']:
        print(f"\n⚠️ Duplicate Titles ({len(issues['duplicate_titles'])}):")
        for item in issues['duplicate_titles'][:5]:
            print(f"  - {item['title']}: {item['reason']}")
    else:
        print(f"\n✅ No duplicate titles")
    
    total_issues = sum(len(v) for v in issues.values())
    print(f"\n{'='*60}")
    print(f"📊 Total: {total_issues} reference issues")
    print(f"{'='*60}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python maintain.py validate [vault_path]  # Validate references")
        print("  python maintain.py isolated [vault_path]  # Find isolated notes")
        print("  python maintain.py stats [vault_path]     # Generate statistics")
        return
    
    command = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if len(sys.argv) > 2:
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    if command == 'validate':
        issues = validate_references(vault_path)
        print_reference_issues(issues)
    
    elif command == 'isolated':
        notes = scan_vault(vault_path)
        isolated = find_isolated_notes(notes)
        print(f"Found {len(isolated)} isolated notes")
        for path in isolated[:10]:
            print(f"  - {path}")
    
    elif command == 'stats':
        notes = scan_vault(vault_path)
        print(f"Total notes: {len(notes)}")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
