#!/usr/bin/env python3
"""
scripts/validate_verdict_ledger_945a.py
Validates evidence/verdicts.csv against Op 945A evidence-basis and schema invariants.
"""

import os
import sys
import csv
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(REPO_ROOT, "evidence", "verdicts.csv")

ALLOWED_EVIDENCE_BASIS = {
    "same-master-reference",
    "hallowed-relative",
    "insufficient-parity",
    "none"
}

ALLOWED_CONFIDENCE_STATES = {
    "candidate",
    "review",
    "unmeasured",
    "insufficient-parity"
}

EXPECTED_HEADER = [
    "date", "title", "year", "group", "codec", "res", "size_gb", "runtime_min",
    "mbps", "tier_claimed", "source", "verdict", "vmaf_mean", "vmaf_min",
    "psnr_y_mean", "ssim_mean", "bpp", "reference_master", "scene_count",
    "title_count", "confidence_state", "evidence_basis", "measurement_date",
    "evidence_doc", "notes"
]

def validate_ledger():
    if not os.path.exists(CSV_PATH):
        print(f"[FAIL] Missing {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        if header != EXPECTED_HEADER:
            print(f"[FAIL] Header mismatch!\nExpected: {EXPECTED_HEADER}\nActual:   {header}")
            sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        dict_reader = csv.DictReader(f)
        rows = list(dict_reader)

    print(f"Total rows in ledger: {len(rows)}")

    group_same_master_counts = {}
    group_confidence_states = {}
    basis_counts = {b: 0 for b in ALLOWED_EVIDENCE_BASIS}

    errors = []

    for i, r in enumerate(rows, 1):
        grp = r["group"]
        basis = r.get("evidence_basis")
        conf = r.get("confidence_state")
        tc = r.get("title_count", "").strip()
        vmaf_m = r.get("vmaf_mean", "").strip()
        doc = r.get("evidence_doc", "").strip()

        # 1. Check evidence_basis
        if basis not in ALLOWED_EVIDENCE_BASIS:
            errors.append(f"Row {i} ({grp} - {r['title']}): Invalid evidence_basis '{basis}'")
        else:
            basis_counts[basis] += 1

        # 2. Check confidence_state
        if conf not in ALLOWED_CONFIDENCE_STATES:
            errors.append(f"Row {i} ({grp} - {r['title']}): Invalid confidence_state '{conf}'")
        if conf == "high-confidence":
            errors.append(f"Row {i} ({grp} - {r['title']}): Forbidden 'high-confidence' state detected!")

        # 3. Check Hallowed not introduced as AV1 group
        if grp.lower() == "hallowed" and r["codec"].upper() == "AV1":
            errors.append(f"Row {i}: Hallowed incorrectly classified as AV1 release group!")

        # 4. Invariants by basis
        if basis == "hallowed-relative":
            if tc != "":
                errors.append(f"Row {i} ({grp} - {r['title']}): hallowed-relative row must have blank title_count, found '{tc}'")
            if "hallowed" not in r["reference_master"].lower():
                errors.append(f"Row {i} ({grp} - {r['title']}): hallowed-relative row must reference hallowed baseline")

        elif basis == "insufficient-parity":
            if tc != "":
                errors.append(f"Row {i} ({grp} - {r['title']}): insufficient-parity row must have blank title_count, found '{tc}'")
            if conf != "insufficient-parity":
                errors.append(f"Row {i} ({grp} - {r['title']}): insufficient-parity row must have confidence_state='insufficient-parity'")

        elif basis == "none":
            if tc != "":
                errors.append(f"Row {i} ({grp} - {r['title']}): unmeasured/none row must have blank title_count, found '{tc}'")
            if vmaf_m != "":
                errors.append(f"Row {i} ({grp} - {r['title']}): unmeasured/none row must have blank vmaf_mean, found '{vmaf_m}'")
            if conf != "unmeasured":
                errors.append(f"Row {i} ({grp} - {r['title']}): unmeasured/none row must have confidence_state='unmeasured'")

        elif basis == "same-master-reference":
            if vmaf_m == "":
                errors.append(f"Row {i} ({grp} - {r['title']}): same-master-reference row must have populated vmaf_mean")
            if doc == "":
                errors.append(f"Row {i} ({grp} - {r['title']}): same-master-reference row must have evidence_doc")
            else:
                doc_path = os.path.join(REPO_ROOT, doc)
                if not os.path.exists(doc_path):
                    errors.append(f"Row {i} ({grp} - {r['title']}): evidence_doc path does not exist: '{doc}'")

            if tc != "":
                if grp not in group_same_master_counts:
                    group_same_master_counts[grp] = tc
                else:
                    if group_same_master_counts[grp] != tc:
                        errors.append(f"Row {i} ({grp} - {r['title']}): Inconsistent title_count '{tc}' vs group '{group_same_master_counts[grp]}'")

            if grp not in group_confidence_states:
                group_confidence_states[grp] = conf
            else:
                if group_confidence_states[grp] != conf:
                    errors.append(f"Row {i} ({grp} - {r['title']}): Inconsistent confidence_state '{conf}' vs group '{group_confidence_states[grp]}'")

        # 5. Check evidence_doc path if populated
        if doc != "":
            doc_path = os.path.join(REPO_ROOT, doc)
            if not os.path.exists(doc_path):
                errors.append(f"Row {i} ({grp} - {r['title']}): evidence_doc path does not exist: '{doc}'")

    print("\n--- Summary by evidence_basis ---")
    for b, count in basis_counts.items():
        print(f"  {b}: {count}")

    print("\n--- Same-Master Group Consistency ---")
    for g, count in group_same_master_counts.items():
        print(f"  {g}: title_count={count}, confidence_state={group_confidence_states.get(g)}")

    if errors:
        print(f"\n[FAIL] Found {len(errors)} validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n[PASS] All Op 945A verdict ledger invariants successfully verified!")

if __name__ == "__main__":
    validate_ledger()
