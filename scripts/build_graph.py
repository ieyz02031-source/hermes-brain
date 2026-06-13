#!/usr/bin/env python3
"""
Hermes Brain - Knowledge Graph Construction

Extracts entities and relationships from notes, builds knowledge graph.

Usage:
    python build_graph.py [vault_path]
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def extract_wikilinks(content: str) -> List[str]:
    """Extract wikilinks from content"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


def extract_tags(content: str) -> List[str]:
    """Extract tags from content"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_title(content: str) -> str:
    """Extract title from content"""
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
    """Scan all notes in Vault"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            relative_path = md_file.relative_to(vault_path)
            
            notes[str(relative_path)] = {
                'path': str(md_file),
                'title': extract_title(content),
                'tags': extract_tags(content),
                'wikilinks': extract_wikilinks(content),
                'content_length': len(content),
            }
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    return notes


def build_graph(notes: Dict[str, Dict]) -> Tuple[Dict, Dict]:
    """Build knowledge graph"""
    nodes = {}
    edges = defaultdict(set)
    
    for note_path, note_data in notes.items():
        nodes[note_path] = {
            'title': note_data['title'],
            'tags': note_data['tags'],
        }
        
        for wikilink in note_data['wikilinks']:
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            target_path = None
            for path in notes.keys():
                if target in path or path.endswith(f'{target}.md'):
                    target_path = path
                    break
            
            if target_path:
                edges[(note_path, target_path)].add('wikilink')
    
    return nodes, edges


def analyze_graph(nodes: Dict, edges: Dict) -> Dict:
    """Analyze graph statistics"""
    type_counts = defaultdict(int)
    for node_data in nodes.values():
        type_counts[node_data.get('type', 'unknown')] += 1
    
    edge_count = len(edges)
    
    degree_counts = defaultdict(int)
    for (source, target) in edges:
        degree_counts[source] += 1
        degree_counts[target] += 1
    
    isolated_nodes = [node for node in nodes if degree_counts[node] == 0]
    high_degree_nodes = sorted(degree_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_nodes': len(nodes),
        'total_edges': edge_count,
        'type_counts': dict(type_counts),
        'isolated_nodes': isolated_nodes,
        'high_degree_nodes': high_degree_nodes,
        'average_degree': sum(degree_counts.values()) / len(degree_counts) if degree_counts else 0,
    }


def print_statistics(stats: Dict):
    """Print statistics"""
    print("\n" + "="*60)
    print("Hermes Brain - Knowledge Graph Statistics")
    print("="*60)
    
    print(f"\n📊 Basic Statistics:")
    print(f"  - Total nodes: {stats['total_nodes']}")
    print(f"  - Total edges: {stats['total_edges']}")
    print(f"  - Average degree: {stats['average_degree']:.2f}")
    
    print(f"\n📁 Node Type Distribution:")
    for type_name, count in stats['type_counts'].items():
        print(f"  - {type_name}: {count}")
    
    print(f"\n🔗 High-Degree Nodes (Top 10):")
    for node, degree in stats['high_degree_nodes']:
        print(f"  - {node}: {degree} connections")
    
    print(f"\n🏝️ Isolated Nodes ({len(stats['isolated_nodes'])}):")
    for node in stats['isolated_nodes'][:10]:
        print(f"  - {node}")
    if len(stats['isolated_nodes']) > 10:
        print(f"  - ... and {len(stats['isolated_nodes']) - 10} more")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    else:
        vault_path = Path(r"D:\ObsidianVault")
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    print(f"🔍 Scanning Vault: {vault_path}")
    
    notes = scan_vault(vault_path)
    print(f"  Found {len(notes)} notes")
    
    print(f"\n🔗 Building knowledge graph...")
    nodes, edges = build_graph(notes)
    
    print(f"\n📊 Analyzing graph...")
    stats = analyze_graph(nodes, edges)
    
    print_statistics(stats)
    
    print("\n" + "="*60)
    print("✅ Knowledge graph construction complete!")
    print("="*60)


if __name__ == '__main__':
    main()
