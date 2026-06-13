#!/usr/bin/env python3
"""
Hermes Brain - Semantic Indexing

Builds vector embeddings for all notes using all-MiniLM-L6-v2 model, stores in SQLite.

Usage:
    python semantic_index.py index [vault_path]    # Build index
    python semantic_index.py search "query"        # Semantic search
    python semantic_index.py stats                 # Show statistics
    python semantic_index.py rebuild               # Force rebuild
"""

import os
import re
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


# Configuration
MODEL_NAME = 'all-MiniLM-L6-v2'
DB_NAME = '.hermes_brain.db'


def get_db_path(vault_path: Path) -> Path:
    """Get database path"""
    return vault_path / DB_NAME


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


def extract_text_for_embedding(content: str) -> str:
    """Extract text for embedding"""
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    content = re.sub(r'```[\s\S]*?```', '', content)
    content = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', content)
    content = re.sub(r'[#*_`\[\]()]', '', content)
    content = re.sub(r'\s+', ' ', content).strip()
    return content[:500]


def compute_hash(content: str) -> str:
    """Compute content hash"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def init_db(db_path: Path) -> sqlite3.Connection:
    """Initialize database"""
    conn = sqlite3.connect(str(db_path))
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            path TEXT PRIMARY KEY,
            title TEXT,
            tags TEXT,
            content_hash TEXT,
            embedding BLOB,
            updated_at TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    return conn


def get_embedding_model():
    """Get embedding model (lazy loading)"""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
        return model
    except ImportError:
        print("Error: sentence-transformers required")
        print("Run: pip install sentence-transformers")
        sys.exit(1)


def scan_vault(vault_path: Path) -> Dict[str, Dict]:
    """Scan Vault"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        if md_file.name == DB_NAME:
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
                'text': extract_text_for_embedding(content),
                'hash': compute_hash(content),
            }
        except Exception:
            pass
    
    return notes


def index_vault(vault_path: Path, force: bool = False):
    """Build semantic index"""
    db_path = get_db_path(vault_path)
    conn = init_db(db_path)
    
    print(f"📦 Building semantic index: {vault_path}")
    
    print("  Scanning notes...")
    notes = scan_vault(vault_path)
    print(f"  Found {len(notes)} notes")
    
    existing = {}
    cursor = conn.execute('SELECT path, content_hash FROM notes')
    for row in cursor:
        existing[row[0]] = row[1]
    
    to_update = []
    for path, note in notes.items():
        if force or path not in existing or existing[path] != note['hash']:
            to_update.append(note)
    
    if not to_update:
        print("  ✅ All notes are up to date, no update needed")
        return
    
    print(f"  Need to update {len(to_update)} notes")
    
    print("  Loading embedding model...")
    model = get_embedding_model()
    
    print("  Generating embeddings...")
    texts = [note['text'] for note in to_update]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    print("  Storing to database...")
    for note, embedding in zip(to_update, embeddings):
        conn.execute('''
            INSERT OR REPLACE INTO notes (path, title, tags, content_hash, embedding, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            note['path'],
            note['title'],
            json.dumps(note['tags'], ensure_ascii=False),
            note['hash'],
            embedding.tobytes(),
            datetime.now().isoformat(),
        ))
    
    conn.execute('''
        INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)
    ''', ('last_indexed', datetime.now().isoformat()))
    conn.execute('''
        INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)
    ''', ('model_name', MODEL_NAME))
    conn.execute('''
        INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)
    ''', ('total_notes', str(len(notes))))
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Index complete, {len(notes)} notes indexed")


def search_vault(query: str, vault_path: Path, top_k: int = 5) -> List[Dict]:
    """Semantic search"""
    db_path = get_db_path(vault_path)
    
    if not db_path.exists():
        print("Error: Index does not exist, run first: python semantic_index.py index")
        sys.exit(1)
    
    conn = sqlite3.connect(str(db_path))
    model = get_embedding_model()
    query_embedding = model.encode([query])[0]
    
    cursor = conn.execute('SELECT path, title, tags, embedding FROM notes')
    results = []
    
    for row in cursor:
        path, title, tags_json, embedding_bytes = row
        
        import numpy as np
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        
        dot_product = np.dot(query_embedding, embedding)
        norm1 = np.linalg.norm(query_embedding)
        norm2 = np.linalg.norm(embedding)
        
        if norm1 > 0 and norm2 > 0:
            similarity = dot_product / (norm1 * norm2)
        else:
            similarity = 0.0
        
        tags = json.loads(tags_json) if tags_json else []
        
        results.append({
            'path': path,
            'title': title,
            'tags': tags,
            'score': float(similarity),
        })
    
    conn.close()
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]


def show_stats(vault_path: Path):
    """Show index statistics"""
    db_path = get_db_path(vault_path)
    
    if not db_path.exists():
        print("Index does not exist")
        return
    
    conn = sqlite3.connect(str(db_path))
    
    cursor = conn.execute('SELECT key, value FROM meta')
    meta = {}
    for row in cursor:
        meta[row[0]] = row[1]
    
    cursor = conn.execute('SELECT COUNT(*) FROM notes')
    count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n📊 Index Statistics:")
    print(f"  - Notes indexed: {count}")
    print(f"  - Embedding model: {meta.get('model_name', 'unknown')}")
    print(f"  - Last indexed: {meta.get('last_indexed', 'unknown')}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python semantic_index.py index [vault_path]    # Build index")
        print("  python semantic_index.py search \"query\"        # Semantic search")
        print("  python semantic_index.py stats                 # Show statistics")
        return
    
    command = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if command == 'index':
        if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
            vault_path = Path(sys.argv[2])
        index_vault(vault_path)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: Please provide search query")
            return
        query = ' '.join(sys.argv[2:])
        results = search_vault(query, vault_path)
        print(f"\n{'='*60}")
        print(f"🔍 Semantic Search: {query}")
        print(f"{'='*60}")
        for i, result in enumerate(results, 1):
            tags_str = ', '.join(result['tags'][:3]) if result['tags'] else ''
            score_bar = '█' * int(result['score'] * 20)
            print(f"\n  {i}. {result['title']}")
            print(f"     Path: {result['path']}")
            print(f"     Similarity: {result['score']:.3f} {score_bar}")
            if tags_str:
                print(f"     Tags: {tags_str}")
    
    elif command == 'stats':
        show_stats(vault_path)
    
    elif command == 'rebuild':
        if len(sys.argv) > 2:
            vault_path = Path(sys.argv[2])
        index_vault(vault_path, force=True)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
