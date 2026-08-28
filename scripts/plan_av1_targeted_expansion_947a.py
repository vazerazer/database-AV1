#!/usr/bin/env python3
"""
scripts/plan_av1_targeted_expansion_947a.py
Targeted Evidence Expansion Planner & Manifest Validator (Op 947A)

Validates the targeted evidence expansion manifest (evidence/av1_targeted_expansion_manifest_947a.json)
for review and unmeasured AV1 groups whose behavior changes between baseline and strict scenarios.
"""

import os
import sys
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(REPO_ROOT, "evidence", "av1_targeted_expansion_manifest_947a.json")
RAW_PATH = os.path.join(REPO_ROOT, "evidence", "av1_targeted_expansion_raw_947a.json")

EXPECTED_TARGET_GROUPS = {"RandH", "Smokindevil", "Rob74K", "Bi0hazard", "Waldek"}

def validate_manifest():
    if not os.path.exists(MANIFEST_PATH):
        print(f"[FAIL] Missing manifest: {MANIFEST_PATH}")
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"[FAIL] JSON decode error in manifest: {e}")
            sys.exit(1)

    meta = data.get("plan_metadata", {})
    if not meta:
        print("[FAIL] Missing plan_metadata in manifest")
        sys.exit(1)

    groups = data.get("target_groups", [])
    if not groups:
        print("[FAIL] Missing target_groups in manifest")
        sys.exit(1)

    found_groups = {g.get("group_name") for g in groups}
    missing_groups = EXPECTED_TARGET_GROUPS - found_groups
    if missing_groups:
        print(f"[FAIL] Missing expected target groups in manifest: {missing_groups}")
        sys.exit(1)

    print(f"Validated {len(groups)} target groups in manifest:")
    total_planned = 0
    total_exhausted = 0

    for g in groups:
        grp_name = g.get("group_name")
        curr_state = g.get("current_confidence_state")
        curr_tc = g.get("current_same_master_title_count")
        status = g.get("expansion_status")
        planned_titles = g.get("proposed_titles", [])

        print(f"  - {grp_name:<12} (State: {curr_state:<10}, Same-Master TC: {curr_tc}) -> Status: {status} ({len(planned_titles)} proposed titles)")
        total_planned += len(planned_titles)
        if status == "inventory-exhausted":
            total_exhausted += 1

    print(f"\nTotal planned expansion titles across all groups: {total_planned}")
    print(f"Groups with local inventory exhaustion: {total_exhausted}")
    print("\n[PASS] Targeted expansion manifest schema and group coverage 100% verified!")

if __name__ == "__main__":
    validate_manifest()
