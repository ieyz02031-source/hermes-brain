#!/usr/bin/env python3
"""
Hermes Brain - Cron Automation

Set up daily self-evolution cycle automation.

Usage:
    python cron.py setup    # Set up cron task
    python cron.py remove   # Remove cron task
    python cron.py status   # Check cron status
    python cron.py run      # Manual run
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


# Configuration
SCRIPT_DIR = Path(r"D:\Hermes\skills\hermes-brain\scripts")
VAULT_PATH = Path(r"D:\ObsidianVault")
LOG_DIR = VAULT_PATH / ".hermes_logs"


def setup_cron():
    """Set up cron task"""
    print("⏰ Setting up cron task...")
    
    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create cron script
    cron_script = SCRIPT_DIR / "cron_task.sh"
    cron_script.write_text(f"""#!/bin/bash
# Hermes Brain - Auto Evolution Task
# Run time: Daily at 2:00 AM

cd {SCRIPT_DIR.parent}
python scripts/evolve.py run >> {LOG_DIR}/evolution.log 2>&1
python scripts/hot_cache.py >> {LOG_DIR}/hot_cache.log 2>&1
python scripts/semantic_index.py index >> {LOG_DIR}/index.log 2>&1
""", encoding='utf-8')
    
    # Make script executable
    os.chmod(str(cron_script), 0o755)
    
    print(f"  ✅ Cron script created: {cron_script}")
    print(f"  📝 Log directory: {LOG_DIR}")
    print(f"\n  Please manually add to crontab:")
    print(f"  0 2 * * * {cron_script}")


def remove_cron():
    """Remove cron task"""
    print("🗑️ Removing cron task...")
    
    cron_script = SCRIPT_DIR / "cron_task.sh"
    if cron_script.exists():
        cron_script.unlink()
        print(f"  ✅ Cron script deleted: {cron_script}")
    else:
        print(f"  ⚠️ Cron script does not exist: {cron_script}")
    
    print(f"\n  Please manually remove from crontab:")
    print(f"  0 2 * * * {cron_script}")


def show_status():
    """Show cron status"""
    print("⏰ Cron Status:")
    
    cron_script = SCRIPT_DIR / "cron_task.sh"
    if cron_script.exists():
        print(f"  ✅ Cron script exists: {cron_script}")
        
        # Check logs
        log_files = list(LOG_DIR.glob("*.log")) if LOG_DIR.exists() else []
        if log_files:
            print(f"\n  📝 Log files:")
            for log_file in log_files:
                size = log_file.stat().st_size
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                print(f"    - {log_file.name}: {size} bytes, last update: {mtime}")
        else:
            print(f"\n  📝 Log files: None")
    else:
        print(f"  ❌ Cron script does not exist")


def run_once():
    """Manual run"""
    print("🚀 Manual run evolution cycle...")
    
    # Run evolution cycle
    os.system(f'cd {SCRIPT_DIR.parent} && python scripts/evolve.py run')
    
    # Update hot cache
    print("\n🔥 Updating hot cache...")
    os.system(f'cd {SCRIPT_DIR.parent} && python scripts/hot_cache.py')
    
    # Update index
    print("\n📦 Updating index...")
    os.system(f'cd {SCRIPT_DIR.parent} && python scripts/semantic_index.py index')
    
    print("\n✅ Manual run complete")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cron.py setup    # Set up cron task")
        print("  python cron.py remove   # Remove cron task")
        print("  python cron.py status   # Check cron status")
        print("  python cron.py run      # Manual run")
        return
    
    command = sys.argv[1]
    
    if command == 'setup':
        setup_cron()
    elif command == 'remove':
        remove_cron()
    elif command == 'status':
        show_status()
    elif command == 'run':
        run_once()
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
