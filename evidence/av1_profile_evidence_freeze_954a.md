# AV1 Profile Project Evidence Freeze Manifest (Op 954A)
**Freeze Date:** 2026-08-29
**Status:** **PERMANENT EVIDENCE BASELINE (FROZEN)**
**Source of Truth:** GitHub Repository (`origin/v2`)

> [!IMPORTANT]
> **Evidence Immutability Notice:** All artifacts listed in this manifest represent the empirical, theoretical, and operational foundation of the AV1→x265 Quality Profile Project. These files are formally frozen and must not be altered, deleted, or re-scored, except for critical factual corrections or security/tripwire hygiene remediation.

---

## 1. Frozen Evidence Catalog

### A. Empirical Verdict Ledgers & Inventory
* [`verdicts.csv`](verdicts.csv): Master empirical dataset containing $N=32$ VMAF measurements categorized by `evidence_basis`.
* [`av1_inventory.md`](av1_inventory.md) & [`av1_inventory_raw.json`](av1_inventory_raw.json): Initial census and encoder group categorization.
* [`hallowed_baseline.md`](hallowed_baseline.md) & [`hallowed_baseline_raw.json`](hallowed_baseline_raw.json): High-fidelity x265 baseline reference metrics.
* [`verdict_ledger_945a.md`](verdict_ledger_945a.md) & [`verdict_ledger_945a_report.md`](verdict_ledger_945a_report.md): Consolidated verdict ledger documentation.

### B. Policy Simulation & Derivation Datasets
* [`hybrid_policy_simulation_946a_report.md`](hybrid_policy_simulation_946a_report.md) & [`hybrid_policy_simulation_946a_raw.json`](hybrid_policy_simulation_946a_raw.json): Automated policy simulation across 5 candidate rules.
* [`av1_targeted_expansion_947a_manifest.json`](av1_targeted_expansion_947a_manifest.json) & [`av1_targeted_expansion_947a_report.md`](av1_targeted_expansion_947a_report.md): Targeted sampling plan.
* [`targeted_expansion_measurements_948a_raw.json`](targeted_expansion_measurements_948a_raw.json) & [`targeted_expansion_measurements_948a_report.md`](targeted_expansion_measurements_948a_report.md): Final VMAF measurement records (*Bourne Supremacy* & *Blade Runner*).

### C. Rule Specification & Schemas
* [`hybrid_av1_profile_rule_949a.md`](hybrid_av1_profile_rule_949a.md): Definitive 4-tier decision hierarchy specification and 2160p scope rule.
* [`hybrid_av1_profile_mapping_949a.json`](hybrid_av1_profile_mapping_949a.json): Machine-readable group-to-tier mapping schema.
* [`hybrid_av1_profile_thresholds_949a_raw.json`](hybrid_av1_profile_thresholds_949a_raw.json): Formal quality and bitrate guardrail derivation thresholds.
* [`hybrid_av1_profile_rule_949a_report.md`](hybrid_av1_profile_rule_949a_report.md): Option A scoring summary.

### D. Live Deployment, Validation & Audit Reports
* [`hybrid_av1_profile_apply_950a_report.md`](hybrid_av1_profile_apply_950a_report.md) & [`hybrid_av1_profile_apply_950a_raw.json`](hybrid_av1_profile_apply_950a_raw.json): Live deployment in Radarr4k Profile `64`.
* [`hybrid_av1_profile_field_test_951a_report.md`](hybrid_av1_profile_field_test_951a_report.md) & [`hybrid_av1_profile_field_test_951a_raw.json`](hybrid_av1_profile_field_test_951a_raw.json): 25-title live library field test.
* [`av1_tier4_scoring_fix_952a_report.md`](av1_tier4_scoring_fix_952a_report.md) & [`av1_tier4_scoring_fix_952a_raw.json`](av1_tier4_scoring_fix_952a_raw.json): Unmeasured AV1 Tier 4 quarantine fix.
* [`full_stack_audit_953a_report.md`](full_stack_audit_953a_report.md) & [`full_stack_audit_953a_raw.json`](full_stack_audit_953a_raw.json): Complete system integrity audit.
* [`av1_profile_project_closeout_954a_report.md`](av1_profile_project_closeout_954a_report.md): Formal project close-out summary.

### E. Dedicated Evidence Scripts
* [`../scripts/validate_verdict_ledger_945a.py`](../scripts/validate_verdict_ledger_945a.py)
* [`../scripts/simulate_hybrid_profile_policy_946a.py`](../scripts/simulate_hybrid_profile_policy_946a.py)
* [`../scripts/plan_av1_targeted_expansion_947a.py`](../scripts/plan_av1_targeted_expansion_947a.py)
* [`../scripts/validate_targeted_expansion_948a.py`](../scripts/validate_targeted_expansion_948a.py)
* [`../scripts/validate_hybrid_profile_rule_949a.py`](../scripts/validate_hybrid_profile_rule_949a.py)
* [`../scripts/run_hybrid_av1_field_test_951a.py`](../scripts/run_hybrid_av1_field_test_951a.py)

---

## 2. Maintenance & Governance Guidelines

1. **Immutability:** The above artifacts constitute a historical record of empirical findings and decisions. They must not be modified or re-generated.
2. **Exception Handling:** Modifications to files in this manifest are strictly restricted to:
   - Critical factual errata corrections.
   - Pre-push security and tripwire hygiene fixes (path guards, hex leaks).
3. **Repository Authority:** The remote repository branch `v2` on GitHub (`origin/v2`) is the authoritative source of truth for this evidence suite.
