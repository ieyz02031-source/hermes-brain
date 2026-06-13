#!/usr/bin/env python3
"""
Hermes Brain - Hot Cache Update

Automatically scans recently modified notes and updates the hot cache section at the top of index.md.

Usage:
    python hot_cache.py [vault_path] [--recent N]

Parameters:
    vault_path - Path to Obsidian Vault (default: D:\ObsidianVault)
    --recent N - Number of recent notes to include (default: 10)
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List


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
    return None


def extract_tags(content: str) -> List[str]:
    """Extract tags from content"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_summary(content: str, max_sentences: int = 3) -> str:
    """Extract summary (first N sentences)"""
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # Remove title lines
    content = re.sub(r'^#\s+.+\n', '', content, flags=re.MULTILINE)
    # Remove empty lines and quotes
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
    
    # Split by period
    sentences = re.split(r'[。！？\.\!\?]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if not sentences:
        return ""
    
    summary = '。'.join(sentences[:max_sentences])
    if len(summary) > 200:
        summary = summary[:200] + '...'
    return summary


def get_recent_notes(vault_path: Path, limit: int = 10) -> List[Dict]:
    """Get recently modified notes"""
    notes = []
    
    for md_file in vault_path.rglob('*.md'):
        # Skip special files
        if md_file.name in ['index.md', 'SCHEMA.md', 'log.md']:
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            mtime = md_file.stat().st_mtime
            content = md_file.read_text(encoding='utf-8')
            title = extract_title(content)
            tags = extract_tags(content)
            summary = extract_summary(content)
            relative_path = md_file.relative_to(vault_path)
            
            notes.append({
                'path': str(relative_path),
                'title': title or str(relative_path),
                'tags': tags,
                'summary': summary,
                'mtime': mtime,
                'date': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d'),
            })
        except Exception as e:
            pass
    
    # Sort by modification time
    notes.sort(key=lambda x: x['mtime'], reverse=True)
    return notes[:limit]


def generate_hot_cache(notes: List[Dict]) -> str:
    """Generate hot cache content"""
    lines = []
    for note in notes:
        tag_str = ', '.join(note['tags'][:3]) if note['tags'] else ''
        summary_str = note['summary'][:80] + '...' if len(note['summary']) > 80 else note['summary']
        
        if tag_str:
            lines.append(f"- **{note['date']}**: [{note['title']}] — {tag_str}")
        else:
            lines.append(f"- **{note['date']}**: [{note['title']}]")
    
    return '\n'.join(lines)


def update_index_hot_cache(index_path: Path, hot_cache_content: str):
    """Update hot cache section in index.md"""
    content = index_path.read_text(encoding='utf-8')
    
    # Find hot cache section
    pattern = r'(## 热缓存 \(Hot Cache\)\s*\n\n最近上下文，每次会话更新：\s*\n\n)(.*?)(\n\n---)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = content[:match.start(1)] + match.group(1) + hot_cache_content + match.group(3) + content[match.end(3):]
    else:
        # If hot cache section not found, add at the beginning
        new_content = f"## 热缓存 (Hot Cache)\n\n最近上下文，每次会话更新：\n\n{hot_cache_content}\n\n---\n\n" + content
    
    index_path.write_text(new_content, encoding='utf-8')


def main():
    """Main function"""
    # Parse arguments
    vault_path = Path(r"D:\ObsidianVault")
    recent_limit = 10
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Usage: python hot_cache.py [vault_path] [--recent N]")
            print("  vault_path: Path to Obsidian Vault (default: D:\\ObsidianVault)")
            print("  --recent N: Number of recent notes (default: 10)")
            return
        if not sys.argv[1].startswith('--'):
            vault_path = Path(sys.argv[1])
    
    if '--recent' in sys.argv:
        idx = sys.argv.index('--recent')
        if idx + 1 < len(sys.argv):
            recent_limit = int(sys.argv[idx + 1])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    print(f"🔥 Updating hot cache: {vault_path}")
    print(f"  Scanning {recent_limit} most recent notes...")
    
    # Get recent notes
    notes = get_recent_notes(vault_path, recent_limit)
    print(f"  Found {len(notes)} recent notes")
    
    # Generate hot cache
    hot_cache = generate_hot_cache(notes)
    
    # Update index.md
    index_path = vault_path / 'index.md'
    if index_path.exists():
        update_index_hot_cache(index_path, hot_cache)
        print(f"  ✅ Updated {index_path}")
    else:
        print(f"  ⚠️ index.md does not exist, skipping update")
    
    # Output hot cache content
    print(f"\n{'='*50}")
    print("Hot cache content:")
    print(f"{'='*50}")
    print(hot_cache)


if __name__ == '__main__':
    main()
