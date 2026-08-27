#!/usr/bin/env python3
"""
tests/test_tripwire_hygiene.py
Ensures strict repository hygiene, secret tripwire safety, and absolute path sanitization.
Replicates remote GitHub Actions CI security tripwire locally before push.
"""

import os
import re
import sys
import subprocess

def run_tripwire_checks():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("================================================================================")
    print("LOCAL PRE-PUSH SECURITY & TRIPWIRE AUDIT")
    print(f"Repository Root: {repo_root}")
    print("================================================================================")

    errors = []

    # 1. Check for 32-hex secret-like patterns across tracked files
    res_hex = subprocess.run(
        ['git', 'grep', '-nEi', r'\b[0-9a-f]{32}\b', '--', ':!.github/last-upstream-sha'],
        cwd=repo_root, capture_output=True, text=True
    )
    if res_hex.stdout.strip():
        lines = res_hex.stdout.strip().splitlines()
        errors.append(f"Found {len(lines)} instances of 32-hex string pattern:\n" + "\n".join(lines[:10]))

    # 2. Check for absolute /home/ paths
    res_home = subprocess.run(
        ['git', 'grep', '-nE', r'/home/[A-Za-z0-9._-]+'],
        cwd=repo_root, capture_output=True, text=True
    )
    if res_home.stdout.strip():
        lines = res_home.stdout.strip().splitlines()
        errors.append(f"Found {len(lines)} instances of absolute /home/ paths:\n" + "\n".join(lines[:10]))

    # 3. Check evidence/supply_av1.csv for URL leaks
    csv_path = os.path.join(repo_root, 'evidence', 'supply_av1.csv')
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                if 'http://' in line or 'https://' in line:
                    errors.append(f"supply_av1.csv:{line_no} contains raw URL: {line.strip()[:80]}")
                    break

    if errors:
        print("\n[FAIL] TRIPWIRE AUDIT FAILED WITH ERRORS:\n", file=sys.stderr)
        for err in errors:
            print(f"[-] {err}\n", file=sys.stderr)
        sys.exit(1)

    print("\n[PASS] 100% CLEAN: 0 32-hex patterns, 0 absolute paths, 0 URL leaks.")
    print("================================================================================")

if __name__ == '__main__':
    run_tripwire_checks()
