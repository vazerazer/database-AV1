#!/usr/bin/env python3
"""
tests/test_tripwire_hygiene.py
Ensures strict repository hygiene, secret tripwire safety, absolute path sanitization,
and path guards preventing private catalog/indexer data from entering the public repository.
Scans BOTH tracked files and untracked working-tree files (via `git ls-files -co --exclude-standard`).
"""

import os
import re
import sys
import fnmatch
import subprocess

FORBIDDEN_TRACKED_PATTERNS = [
    "evidence/supply_*",
    "evidence/supply_av1.csv",
    "evidence/supply_checkpoint.jsonl",
    "evidence/checkpoints/*",
    "evidence/census_924.md",
    "evidence/indexer_map.local",
    "*.local",
    "evidence/*.local",
    "*.env",
    ".env",
    "telemetry/*"
]

INDEXER_NAME_PATTERNS = [
    r'\bindexer-a\b',
    r'\bindexer-c\b',
    r'\bindexer-d\b',
    r'\bindexer-e\b',
    r'\bindexer-i\b',
    r'\bnzb\.life\b',
    r'\bindexer-g\b',
    r'\btabula\s+rasa\b'
]

def run_tripwire_checks():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("================================================================================")
    print("LOCAL PRE-PUSH SECURITY & TRIPWIRE AUDIT")
    print(f"Repository Root: {repo_root}")
    print("================================================================================")

    errors = []

    # 1. Enumerate all active workspace files (tracked + untracked non-ignored)
    res_files = subprocess.run(
        ['git', 'ls-files', '-co', '--exclude-standard'],
        cwd=repo_root, capture_output=True, text=True
    )
    active_files = [f.strip() for f in res_files.stdout.strip().splitlines() if f.strip()]

    # 2. Path Guard: Tracked files must NEVER match forbidden local patterns
    res_tracked = subprocess.run(
        ['git', 'ls-files'],
        cwd=repo_root, capture_output=True, text=True
    )
    tracked_files = [f.strip() for f in res_tracked.stdout.strip().splitlines() if f.strip()]
    
    for tf in tracked_files:
        for pat in FORBIDDEN_TRACKED_PATTERNS:
            if fnmatch.fnmatch(tf, pat):
                errors.append(f"PATH GUARD VIOLATION: Forbidden private file '{tf}' is tracked by git (matches pattern '{pat}').")

    # 3. Scan all active files for secrets, absolute paths, and indexer leaks
    hex_pat = re.compile(r'\b[0-9a-f]{32}\b', re.IGNORECASE)
    home_pat = re.compile(r'/home/[A-Za-z0-9._-]+')
    indexer_regexes = [re.compile(p, re.IGNORECASE) for p in INDEXER_NAME_PATTERNS]

    for rel_path in active_files:
        if rel_path == '.github/last-upstream-sha' or rel_path.endswith('.png') or rel_path.endswith('.jpg'):
            continue
            
        full_path = os.path.join(repo_root, rel_path)
        if not os.path.isfile(full_path):
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            continue

        is_test_or_script = rel_path.startswith('tests/') or rel_path.startswith('scripts/')

        for line_num, line in enumerate(lines, start=1):
            # Check 32-hex
            if hex_pat.search(line):
                errors.append(f"Found 32-hex secret string in {rel_path}:{line_num}: {line.strip()[:80]}")
                
            # Check absolute /home/
            if home_pat.search(line):
                errors.append(f"Found absolute /home/ path in {rel_path}:{line_num}: {line.strip()[:80]}")
                
            # Check indexer names in non-test/script files
            if not is_test_or_script:
                for idx_re in indexer_regexes:
                    if idx_re.search(line):
                        errors.append(f"Found unredacted indexer name matching '{idx_re.pattern}' in {rel_path}:{line_num}: {line.strip()[:80]}")

    if errors:
        print("\n[FAIL] TRIPWIRE AUDIT FAILED WITH ERRORS:\n", file=sys.stderr)
        for err in errors:
            print(f"[-] {err}\n", file=sys.stderr)
        sys.exit(1)

    print("\n[PASS] 100% CLEAN: Path guards verified, 0 32-hex patterns, 0 absolute paths, 0 indexer leaks across tracked & untracked files.")
    print("================================================================================")

if __name__ == '__main__':
    run_tripwire_checks()
