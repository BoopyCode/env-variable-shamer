#!/usr/bin/env python3
"""
Environment Variable Shamer - Because guessing is for carnival games.
Scans your code for env vars and shames you for not documenting them.
"""

import re
import sys
import os
from pathlib import Path
from collections import defaultdict

# Regex to catch those sneaky env var accesses
# Catches os.getenv, os.environ.get, and os.environ[key]
ENV_PATTERNS = [
    r'os\.getenv\(["\']([^"\']+)["\']',  # os.getenv('KEY')
    r'os\.environ\.get\(["\']([^"\']+)["\']',  # os.environ.get('KEY')
    r'os\.environ\[(["\'])([^"\']+)\1\]',  # os.environ['KEY']
]

def find_env_vars(file_path):
    """Find env vars in a file. Returns empty list if file is too ashamed to exist."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return []
    
    found_vars = set()
    for pattern in ENV_PATTERNS:
        matches = re.findall(pattern, content)
        for match in matches:
            # Handle the different regex group captures
            var = match[1] if isinstance(match, tuple) and len(match) > 1 else match
            found_vars.add(var)
    
    return sorted(found_vars)

def scan_directory(directory='.'):
    """Scan Python files for env vars. Skips virtual environments (they're shy)."""
    env_vars = defaultdict(list)
    
    for py_file in Path(directory).rglob('*.py'):
        # Skip virtual environments - they have enough problems
        if any(part in str(py_file) for part in ['venv', '.venv', 'env', '__pycache__']):
            continue
            
        vars_in_file = find_env_vars(py_file)
        if vars_in_file:
            env_vars[str(py_file)] = vars_in_file
    
    return env_vars

def main():
    """Main function - delivers shame where shame is due."""
    print("\n🔍 Environment Variable Shamer - Starting Investigation...\n")
    
    env_vars = scan_directory()
    
    if not env_vars:
        print("No env vars found! Either you're perfect or your code is boring.")
        return 0
    
    total_vars = sum(len(vars) for vars in env_vars.values())
    print(f"Found {total_vars} undocumented env var{'s' if total_vars != 1 else ''} across {len(env_vars)} file{'s' if len(env_vars) != 1 else ''}. Shame level: {'MILD' if total_vars < 5 else 'MODERATE' if total_vars < 10 else 'SEVERE'}\n")
    
    for file_path, vars_list in env_vars.items():
        print(f"📁 {file_path}:")
        for var in vars_list:
            # Check if it's documented in a .env.example or similar
            env_file_exists = any(Path('.').glob(f'*.env*'))
            status = "❓" if not env_file_exists else "🤷"
            print(f"  {status} {var}")
    
    print("\n💡 Pro tip: Create a .env.example file with these variables!")
    print("   Your teammates will thank you (instead of cursing your name).")
    
    return 1 if total_vars > 0 else 0

if __name__ == '__main__':
    sys.exit(main())