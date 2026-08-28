#!/usr/bin/env python3
"""
scripts/simulate_av1_policy_946a.py
Evidence-Led AV1 Policy Simulation Harness (Op 946A)

Strictly non-operational simulation harness that models how different AV1 group
treatments would affect release selection in practice using the consolidated
verdict ledger (evidence/verdicts.csv).

Scenarios modeled:
1. baseline_current
2. strict_candidate_only
3. relaxed_review_allowed
4. evidence_basis_aware

Outputs evidence/av1_policy_simulation_946a_raw.json.
"""

import os
import sys
import csv
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(REPO_ROOT, "evidence", "verdicts.csv")
RAW_OUTPUT_PATH = os.path.join(REPO_ROOT, "evidence", "av1_policy_simulation_946a_raw.json")

ALLOWED_EVIDENCE_BASIS = {
    "same-master-reference",
    "hallowed-relative",
    "insufficient-parity",
    "none"
}

SCENARIOS = {
    "baseline_current": {
        "name": "Baseline (Current Operational Logic)",
        "description": "Candidate groups preferred when parity is credible; review groups allowed but non-preferred; unmeasured, insufficient-parity, and uncalibrated rows excluded."
    },
    "strict_candidate_only": {
        "name": "Strict Candidate-Only",
        "description": "Only candidate groups with credible evidence are allowed/preferred; all review, unmeasured, insufficient-parity, and uncalibrated rows are blocked."
    },
    "relaxed_review_allowed": {
        "name": "Relaxed Review-Allowed",
        "description": "Candidate groups preferred; review groups permitted as non-preferred alternatives; unmeasured and uncalibrated rows blocked."
    },
    "evidence_basis_aware": {
        "name": "Evidence-Basis Aware",
        "description": "Refines release selection using evidence_basis: differentiates between true same-master reference calibrations and descriptive Hallowed-relative observations."
    }
}

def evaluate_scenario(scenario_key, row):
    grp = row["group"]
    basis = row["evidence_basis"]
    conf = row["confidence_state"]
    codec = row["codec"].upper()

    # Non-AV1 anchor rows (e.g. hallowed x265, FLUX h264) are reference anchors, not AV1 release candidates
    if codec != "AV1":
        return {
            "allowed": False,
            "preferred": False,
            "reason_code": f"non-av1-anchor-{codec.lower()}"
        }

    if basis == "insufficient-parity":
        return {
            "allowed": False,
            "preferred": False,
            "reason_code": "excluded-insufficient-parity"
        }

    if basis == "none" or conf == "unmeasured":
        return {
            "allowed": False,
            "preferred": False,
            "reason_code": "excluded-unmeasured-no-evidence"
        }

    if scenario_key == "baseline_current":
        if conf == "candidate":
            return {
                "allowed": True,
                "preferred": True,
                "reason_code": f"candidate-{basis}"
            }
        elif conf == "review":
            return {
                "allowed": True,
                "preferred": False,
                "reason_code": f"review-{basis}"
            }
        else:
            return {
                "allowed": False,
                "preferred": False,
                "reason_code": f"excluded-{conf}"
            }

    elif scenario_key == "strict_candidate_only":
        if conf == "candidate":
            return {
                "allowed": True,
                "preferred": True,
                "reason_code": f"candidate-accepted-{basis}"
            }
        else:
            return {
                "allowed": False,
                "preferred": False,
                "reason_code": f"blocked-non-candidate-{conf}"
            }

    elif scenario_key == "relaxed_review_allowed":
        if conf == "candidate":
            return {
                "allowed": True,
                "preferred": True,
                "reason_code": f"candidate-preferred-{basis}"
            }
        elif conf == "review":
            return {
                "allowed": True,
                "preferred": False,
                "reason_code": f"review-allowed-non-preferred-{basis}"
            }
        else:
            return {
                "allowed": False,
                "preferred": False,
                "reason_code": f"blocked-unmeasured-{conf}"
            }

    elif scenario_key == "evidence_basis_aware":
        if conf == "candidate" and basis == "same-master-reference":
            return {
                "allowed": True,
                "preferred": True,
                "reason_code": "candidate-same-master-reference-fully-preferred"
            }
        elif conf == "candidate" and basis == "hallowed-relative":
            return {
                "allowed": True,
                "preferred": True,
                "reason_code": "candidate-hallowed-relative-only-preferred"
            }
        elif conf == "review" and basis == "same-master-reference":
            return {
                "allowed": True,
                "preferred": False,
                "reason_code": "review-same-master-reference-allowed"
            }
        elif conf == "review" and basis == "hallowed-relative":
            return {
                "allowed": True,
                "preferred": False,
                "reason_code": "review-hallowed-relative-only-allowed-warning"
            }
        else:
            return {
                "allowed": False,
                "preferred": False,
                "reason_code": f"excluded-{conf}-{basis}"
            }

    return {"allowed": False, "preferred": False, "reason_code": "unknown-scenario"}

def main():
    if not os.path.exists(CSV_PATH):
        print(f"[FAIL] Missing {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded {len(rows)} ledger rows from verdicts.csv")

    # Verify evidence_basis
    for i, r in enumerate(rows, 1):
        basis = r.get("evidence_basis")
        if basis not in ALLOWED_EVIDENCE_BASIS:
            print(f"[FAIL] Row {i} ({r.get('title')}) has invalid evidence_basis: '{basis}'")
            sys.exit(1)

    simulation_results = []
    scenario_aggregates = {k: {"total_evaluated": len(rows), "allowed_count": 0, "preferred_count": 0, "blocked_count": 0, "by_group": {}, "by_basis": {}} for k in SCENARIOS}

    for row in rows:
        title = row["title"]
        yr = row["year"]
        grp = row["group"]
        codec = row["codec"]
        basis = row["evidence_basis"]
        conf = row["confidence_state"]

        row_eval = {
            "title": title,
            "year": yr,
            "group": grp,
            "codec": codec,
            "evidence_basis": basis,
            "confidence_state": conf,
            "vmaf_mean": row.get("vmaf_mean", ""),
            "vmaf_min": row.get("vmaf_min", ""),
            "scenarios": {}
        }

        for sc_key in SCENARIOS:
            res = evaluate_scenario(sc_key, row)
            row_eval["scenarios"][sc_key] = res

            agg = scenario_aggregates[sc_key]
            if res["allowed"]:
                agg["allowed_count"] += 1
            else:
                agg["blocked_count"] += 1

            if res["preferred"]:
                agg["preferred_count"] += 1

            # Aggregate by group
            if grp not in agg["by_group"]:
                agg["by_group"][grp] = {"allowed": 0, "preferred": 0, "blocked": 0}
            if res["allowed"]:
                agg["by_group"][grp]["allowed"] += 1
            else:
                agg["by_group"][grp]["blocked"] += 1
            if res["preferred"]:
                agg["by_group"][grp]["preferred"] += 1

            # Aggregate by basis
            if basis not in agg["by_basis"]:
                agg["by_basis"][basis] = {"allowed": 0, "preferred": 0, "blocked": 0}
            if res["allowed"]:
                agg["by_basis"][basis]["allowed"] += 1
            else:
                agg["by_basis"][basis]["blocked"] += 1
            if res["preferred"]:
                agg["by_basis"][basis]["preferred"] += 1

        simulation_results.append(row_eval)

    raw_payload = {
        "simulation_metadata": {
            "operation": "OP 946A",
            "campaign_name": "Evidence-Led Policy Simulation Harness",
            "date": "2026-08-28",
            "scope": "Simulation of hypothetical release-selection policies across 30 consolidated verdict ledger rows",
            "governance_notice": "Non-operational simulation only. Zero modifications to Radarr, Profilarr, Custom Formats, profile scores, tier assignments, release restrictions, media, or live automation."
        },
        "scenarios": SCENARIOS,
        "scenario_aggregates": scenario_aggregates,
        "row_evaluations": simulation_results
    }

    with open(RAW_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_payload, f, indent=2)

    print(f"[OK] Simulation raw JSON saved to {RAW_OUTPUT_PATH}")

    # Print summary table
    print("\n================================================================================")
    print("SCENARIO OUTCOME SUMMARY (N = 30 Ledger Rows)")
    print("================================================================================")
    print(f"{'Scenario Name':<30} | {'Allowed':<8} | {'Preferred':<10} | {'Blocked':<8}")
    print("-" * 65)
    for sc_key, agg in scenario_aggregates.items():
        name = SCENARIOS[sc_key]["name"]
        print(f"{name:<30} | {agg['allowed_count']:<8} | {agg['preferred_count']:<10} | {agg['blocked_count']:<8}")
    print("================================================================================\n")

if __name__ == "__main__":
    main()
