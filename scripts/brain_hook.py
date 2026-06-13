#!/usr/bin/env python3
"""
Hermes Brain 自动化 Hook
在每次对话结束时自动运行，更新热缓存和索引
"""
import os
import sys
import subprocess
from pathlib import Path

# 配置
SKILL_DIR = Path(r"D:\Hermes\skills\hermes-brain")
SCRIPTS_DIR = SKILL_DIR / "scripts"
VAULT_DIR = Path(r"D:\ObsidianVault")
PYTHON_312 = Path(r"C:\Users\20716\AppData\Local\Programs\Python\Python312\python.exe")

def run_script(script_name, args=None):
    """运行脚本"""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"⚠️ 脚本不存在: {script_path}")
        return False
    
    cmd = [str(PYTHON_312), str(script_path)]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ {script_name} 运行成功")
            return True
        else:
            print(f"❌ {script_name} 运行失败: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_name} 超时")
        return False
    except Exception as e:
        print(f"❌ {script_name} 异常: {e}")
        return False

def main():
    """主函数：自动运行 Hermes Brain 的关键任务"""
    print("🧠 Hermes Brain 自动化 Hook 开始运行...")
    
    # 1. 更新热缓存
    print("\n📝 更新热缓存...")
    run_script("hot_cache.py")
    
    # 2. 更新语义索引（每天只运行一次）
    index_file = VAULT_DIR / ".hermes_brain.db"
    if index_file.exists():
        import time
        last_modified = index_file.stat().st_mtime
        hours_since_update = (time.time() - last_modified) / 3600
        
        if hours_since_update > 24:
            print("\n🔍 更新语义索引...")
            run_script("semantic_index.py", ["index"])
        else:
            print(f"\n⏳ 语义索引 {hours_since_update:.1f} 小时前已更新，跳过")
    else:
        print("\n🔍 首次构建语义索引...")
        run_script("semantic_index.py", ["index"])
    
    # 3. 检查孤立笔记
    print("\n🔗 检查孤立笔记...")
    run_script("maintain.py", ["isolated"])
    
    print("\n✅ Hermes Brain 自动化 Hook 完成")

if __name__ == "__main__":
    main()
