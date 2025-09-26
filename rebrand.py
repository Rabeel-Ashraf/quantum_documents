#!/usr/bin/env python3
"""
Rebranding script: Replace h2oGPT / h2ogpt references with Quantum Documents / quantum_docs
"""

import os
import re
import argparse
from pathlib import Path

# Patterns to replace (case-insensitive where appropriate)
REPLACEMENTS = [
    # Full brand name (user-facing)
    (re.compile(r'h2oGPT', re.IGNORECASE), 'Quantum Documents'),
    # Python package name (internal, word-boundary safe)
    (re.compile(r'\bh2ogpt\b'), 'quantum_docs'),
    # File paths in strings or configs (e.g., 'h2ogpt/gradio_runner.py')
    (re.compile(r'h2ogpt/'), 'quantum_docs/'),
    # Docker image tags, Helm chart names (hyphenated, case-insensitive)
    (re.compile(r'\bh2ogpt\b', re.IGNORECASE), 'quantum-documents'),
]

# File extensions to process
EXTENSIONS = {'.py', '.md', '.yaml', '.yml', '.json', '.txt', '.sh', '.dockerfile', '.env', '.cfg'}

def should_process_file(path: Path) -> bool:
    """Skip binary files, .git, __pycache__, etc."""
    if any(part.startswith('.') for part in path.parts):
        return False
    if '__pycache__' in path.parts:
        return False
    if path.name == "rebrand.py":
        return False
    return path.suffix.lower() in EXTENSIONS

def replace_in_file(file_path: Path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for pattern, replacement in REPLACEMENTS:
            content = pattern.sub(replacement, content)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
    except Exception as e:
        print(f"⚠️  Skipped {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rebrand h2oGPT → Quantum Documents")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed")
    args = parser.parse_args()

    root = Path(".")
    files_to_process = [f for f in root.rglob("*") if f.is_file() and should_process_file(f)]

    print(f"Found {len(files_to_process)} files to process...\n")

    for file_path in files_to_process:
        if not args.dry_run:
            replace_in_file(file_path)
        else:
            print(f"[DRY-RUN] Would update: {file_path}")

    if not args.dry_run:
        print("\n🎉 Rebranding complete! Remember to:")
        print("  - Rename 'h2ogpt/' → 'quantum_docs/'")
        print("  - Update setup.py: name='quantum-documents', packages=['quantum_docs']")
        print("  - Test: python3 -c 'import quantum_docs'")

if __name__ == "__main__":
    main()
