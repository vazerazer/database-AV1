#!/usr/bin/env python3
"""
tests/test_tripwire_hygiene.py
Ensures strict repository hygiene, secret tripwire safety, absolute path sanitization,
and path guards preventing private catalog/indexer data from entering the public repository.
Replicates remote GitHub Actions CI security tripwire locally before push.
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

    # 1. Path Guard: Tracked files must NEVER match forbidden local patterns
    res_tracked = subprocess.run(
        ['git', 'ls-files'],
        cwd=repo_root, capture_output=True, text=True
    )
    tracked_files = [f.strip() for f in res_tracked.stdout.strip().splitlines() if f.strip()]
    
    for tf in tracked_files:
        for pat in FORBIDDEN_TRACKED_PATTERNS:
            if fnmatch.fnmatch(tf, pat):
                errors.append(f"PATH GUARD VIOLATION: Forbidden private file '{tf}' is tracked by git (matches pattern '{pat}').")

    # 2. Check for 32-hex secret-like patterns across tracked files
    res_hex = subprocess.run(
        ['git', 'grep', '-nEi', r'\b[0-9a-f]{32}\b', '--', ':!.github/last-upstream-sha'],
        cwd=repo_root, capture_output=True, text=True
    )
    if res_hex.stdout.strip():
        lines = res_hex.stdout.strip().splitlines()
        errors.append(f"Found {len(lines)} instances of 32-hex string pattern:\n" + "\n".join(lines[:10]))

    # 3. Check for absolute /home/ paths
    res_home = subprocess.run(
        ['git', 'grep', '-nE', r'/home/[A-Za-z0-9._-]+'],
        cwd=repo_root, capture_output=True, text=True
    )
    if res_home.stdout.strip():
        lines = res_home.stdout.strip().splitlines()
        errors.append(f"Found {len(lines)} instances of absolute /home/ paths:\n" + "\n".join(lines[:10]))

    # 4. Check documentation & data files for unredacted indexer names
    for pat in INDEXER_NAME_PATTERNS:
        res_idx = subprocess.run(
            ['git', 'grep', '-nEi', pat, '--', ':!tests/*', ':!scripts/*'],
            cwd=repo_root, capture_output=True, text=True
        )
        if res_idx.stdout.strip():
            lines = res_idx.stdout.strip().splitlines()
            errors.append(f"Found unredacted indexer names matching '{pat}' in tracked non-script files:\n" + "\n".join(lines[:5]))

    if errors:
        print("\n[FAIL] TRIPWIRE AUDIT FAILED WITH ERRORS:\n", file=sys.stderr)
        for err in errors:
            print(f"[-] {err}\n", file=sys.stderr)
        sys.exit(1)

    print("\n[PASS] 100% CLEAN: Path guards verified, 0 32-hex patterns, 0 absolute paths, 0 indexer leaks.")
    print("================================================================================")

if __name__ == '__main__':
    run_tripwire_checks()
