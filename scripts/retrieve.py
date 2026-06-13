#!/usr/bin/env python3
"""
Hermes Brain - Knowledge Retrieval

Three-tier retrieval (hot cache, index, graph), returns relevant notes.

Usage:
    python retrieve.py "query" [vault_path]
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List


def extract_title(content: str) -> str:
    """Extract title"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'title:\s*(.+)', frontmatter)
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


def extract_summary(content: str, max_length: int = 200) -> str:
    """Extract summary"""
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    content = re.sub(r'^#\s+.+\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
    
    if len(content) > max_length:
        content = content[:max_length] + '...'
    return content.strip()


def search_by_keywords(query: str, vault_path: Path) -> List[Dict]:
    """Search by keywords"""
    results = []
    query_lower = query.lower()
    
    for md_file in vault_path.rglob('*.md'):
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            score = 0
            
            title = extract_title(content)
            if query_lower in title.lower():
                score += 10
            
            tags = extract_tags(content)
            for tag in tags:
                if query_lower in tag.lower():
                    score += 5
            
            if query_lower in content_lower:
                count = content_lower.count(query_lower)
                score += min(count, 5)
            
            if score > 0:
                relative_path = md_file.relative_to(vault_path)
                results.append({
                    'path': str(relative_path),
                    'title': title,
                    'score': score,
                    'summary': extract_summary(content),
                    'tags': tags,
                })
        except Exception:
            pass
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def search_by_wikilinks(query: str, vault_path: Path) -> List[Dict]:
    """Search by wikilinks (graph traversal)"""
    results = []
    query_lower = query.lower()
    
    matching_notes = []
    for md_file in vault_path.rglob('*.md'):
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            title = extract_title(content)
            
            if query_lower in title.lower() or query_lower in content.lower():
                matching_notes.append({
                    'path': str(md_file.relative_to(vault_path)),
                    'title': title,
                    'content': content,
                })
        except Exception:
            pass
    
    for note in matching_notes:
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', note['content'])
        
        for wikilink in wikilinks:
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            for md_file in vault_path.rglob('*.md'):
                if any(part.startswith('.') for part in md_file.parts):
                    continue
                
                try:
                    content = md_file.read_text(encoding='utf-8')
                    title = extract_title(content)
                    
                    if target.lower() in title.lower() or target.lower() in str(md_file).lower():
                        relative_path = md_file.relative_to(vault_path)
                        
                        if not any(r['path'] == str(relative_path) for r in results):
                            results.append({
                                'path': str(relative_path),
                                'title': title,
                                'score': 3,
                                'summary': extract_summary(content),
                                'tags': extract_tags(content),
                                'source': note['title'],
                            })
                except Exception:
                    pass
    
    return results


def retrieve(query: str, vault_path: Path, top_k: int = 5) -> List[Dict]:
    """Execute three-tier retrieval"""
    print(f"\n🔍 Search Query: {query}")
    print(f"📁 Vault Path: {vault_path}")
    
    print(f"\n📊 Layer 1: Keyword Search...")
    keyword_results = search_by_keywords(query, vault_path)
    print(f"  Found {len(keyword_results)} results")
    
    print(f"\n🔗 Layer 2: Graph Traversal...")
    graph_results = search_by_wikilinks(query, vault_path)
    print(f"  Found {len(graph_results)} results")
    
    all_results = []
    seen_paths = set()
    
    for result in keyword_results:
        if result['path'] not in seen_paths:
            all_results.append(result)
            seen_paths.add(result['path'])
    
    for result in graph_results:
        if result['path'] not in seen_paths:
            all_results.append(result)
            seen_paths.add(result['path'])
    
    all_results.sort(key=lambda x: x['score'], reverse=True)
    results = all_results[:top_k]
    
    print(f"\n✅ Search complete, returning {len(results)} results")
    return results


def print_results(results: List[Dict], query: str):
    """Print search results"""
    print(f"\n{'='*60}")
    print(f"🔍 Search Results: {query}")
    print(f"{'='*60}")
    
    if not results:
        print("  No relevant notes found")
        return
    
    for i, result in enumerate(results, 1):
        tags_str = ', '.join(result['tags'][:3]) if result['tags'] else ''
        
        print(f"\n  {i}. {result['title']}")
        print(f"     Path: {result['path']}")
        print(f"     Score: {result['score']}")
        if 'source' in result:
            print(f"     Source: {result['source']}")
        if tags_str:
            print(f"     Tags: {tags_str}")
        print(f"\n     Summary:")
        print(f"     {result['summary'][:150]}...")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python retrieve.py \"query\" [vault_path]")
        return
    
    query = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if len(sys.argv) > 2:
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    results = retrieve(query, vault_path)
    print_results(results, query)
    
    print(f"\n{'='*60}")
    print("📋 JSON Format:")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
