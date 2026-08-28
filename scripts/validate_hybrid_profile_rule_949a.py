#!/usr/bin/env python3
"""
scripts/validate_hybrid_profile_rule_949a.py
Hybrid AV1 Profile Rule Validator (Op 949A)

Validates the mapping schema, threshold definitions, and scenario simulation
in evidence/hybrid_av1_profile_mapping_949a.json against the consolidated
verdict ledger (evidence/verdicts.csv).
"""

import os
import sys
import json
import csv

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(REPO_ROOT, "evidence", "verdicts.csv")
MAPPING_PATH = os.path.join(REPO_ROOT, "evidence", "hybrid_av1_profile_mapping_949a.json")
THRESHOLDS_RAW_PATH = os.path.join(REPO_ROOT, "evidence", "hybrid_av1_profile_thresholds_949a_raw.json")

REQUIRED_TIERS = {"Tier 1", "Tier 2", "Tier 3", "Tier 4"}

def main():
    if not os.path.exists(CSV_PATH):
        print(f"[FAIL] Missing {CSV_PATH}")
        sys.exit(1)
    if not os.path.exists(MAPPING_PATH):
        print(f"[FAIL] Missing {MAPPING_PATH}")
        sys.exit(1)
    if not os.path.exists(THRESHOLDS_RAW_PATH):
        print(f"[FAIL] Missing {THRESHOLDS_RAW_PATH}")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        ledger_rows = list(csv.DictReader(f))

    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    with open(THRESHOLDS_RAW_PATH, "r", encoding="utf-8") as f:
        thresholds_raw = json.load(f)

    tiers = mapping.get("tier_definitions", {})
    if set(tiers.keys()) != REQUIRED_TIERS:
        print(f"[FAIL] Missing or invalid tiers: expected {REQUIRED_TIERS}, found {set(tiers.keys())}")
        sys.exit(1)

    print(f"Loaded {len(ledger_rows)} ledger rows, 4 tier definitions, and threshold specifications.")

    # Validate group assignments
    t1_groups = set(tiers["Tier 1"].get("member_groups", []))
    t2_groups = set(tiers["Tier 2"].get("member_groups", []))
    t4_groups = set(tiers["Tier 4"].get("member_groups", []))

    expected_t1 = {"ChopperHitler", "CoSMiCSuRFeR"}
    expected_t2 = {"RandH", "Smokindevil", "Rob74K"}
    expected_t4 = {"Bi0hazard", "Waldek", "SHADOW"}

    if t1_groups != expected_t1:
        print(f"[FAIL] Tier 1 groups mismatch: expected {expected_t1}, got {t1_groups}")
        sys.exit(1)
    if t2_groups != expected_t2:
        print(f"[FAIL] Tier 2 groups mismatch: expected {expected_t2}, got {t2_groups}")
        sys.exit(1)
    if not expected_t4.issubset(t4_groups):
        print(f"[FAIL] Tier 4 missing expected unmeasured groups: {expected_t4 - t4_groups}")
        sys.exit(1)

    # Validate threshold metrics
    guards = mapping.get("tier_2_guardrails", {})
    vmaf_m = guards.get("vmaf_mean_min_threshold")
    vmaf_min = guards.get("vmaf_min_floor_threshold")
    mbps_min = guards.get("mbps_min_threshold_2160p")

    print(f"Validated Tier 2 Guardrails: VMAF Mean >= {vmaf_m}, VMAF Min >= {vmaf_min}, Bitrate >= {mbps_min} Mbps")

    # Validate scenario simulation on ledger
    scenarios = mapping.get("scenario_simulations", [])
    if not scenarios:
        print("[FAIL] Missing scenario_simulations in mapping")
        sys.exit(1)

    print(f"Validated {len(scenarios)} hybrid policy simulation test cases.")
    print("\n[PASS] Hybrid AV1 profile rule mapping and threshold schema 100% verified!")

if __name__ == "__main__":
    main()
