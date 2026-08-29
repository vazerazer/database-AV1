# AV1 Profile Project Close-Out Report (Op 954A)
**Date:** 2026-08-29
**Scope:** Formal Close-Out and Lifecycle Completion of the AV1→x265 Hybrid Quality Profile Project
**Status:** **PROJECT COMPLETED & EVIDENCE PACKAGE FROZEN**

> [!IMPORTANT]
> **Project Close-Out Declaration:** This document formally certifies the completion of the AV1 Profile Project. All operational milestones, empirical measurements, simulation harnesses, live scoring deployments, field validations, and full-stack audits are complete. The entire evidence directory (`evidence/`) is now frozen.

---

## 1. Project Scope, Objectives & Chronological Timeline

The **AV1 Profile Project** was initiated to architect, empirically validate, and deploy a high-fidelity, automated release arbitration system across self-hosted media streaming infrastructure (Radarr4k, Profilarr, Altmount, Silo, Plex). The core objective was ensuring that transparent, high-bitrate 4K AV1 releases receive automatic grab priority when technical parity with UHD Blu-ray remuxes is verified, while establishing an uncompromising, guaranteed fallback to pristine reference x265 encodes whenever AV1 releases underperform or are unmeasured.

### Chronological Milestone Ledger:
* **Ops 943A–944A (Baseline & Empirical Inventory):** Established the Hallowed reference baseline and completed a comprehensive inventory and quality audit of all measured 4K AV1 encoder groups.
* **Op 945A (Consolidated Verdict Ledger):** Consolidated all VMAF metrics ($N=30$ titles) into a single authoritative verdict ledger (`verdicts.csv`) with strict categorization by `evidence_basis` (`same-master-reference`, `hallowed-relative`, `insufficient-parity`).
* **Op 946A (Policy Simulation Harness):** Built an automated policy simulator and threshold derivation engine (`simulate_hybrid_profile_policy_946a.py`), testing candidate policies across varied quality trade-offs.
* **Ops 947A–948A (Targeted Expansion Measurements):** Executed targeted VMAF measurements (*The Bourne Supremacy* same-master 95.31 / *Blade Runner* Hallowed-relative 83.96), expanding the empirical ledger to $N=32$ rows.
* **Op 949A (Hybrid Profile Rule Design):** Formulated the final 4-tier hybrid release-selection architecture, mapping schema, and validation suite.
* **Ops 950A–950C (Live Deployment & Scope Clarifications):** Deployed Option A group-level scoring live into Radarr4k (Profile `64`) and Profilarr; codified the 2160p-only profile scope and 1080p resolution subordination.
* **Op 951A (25-Title Live Field Test):** Validated live release arbitration across 25 diverse movies in production Radarr4k with 100% resolution compliance.
* **Op 952A (Tier 4 Scoring Fix):** Created `AV1 Unmeasured Encoders` (Score `-2400`), subordinating unmeasured/unvetted AV1 groups (`Bi0hazard`, `Waldek`, `SHADOW`) strictly below Tier 3 x265 while maintaining $\ge 1001$ grabbability.
* **Op 953A (Full Stack & Profile Integrity Audit):** Executed a complete four-pillar audit of all 341 PCD migrations, 68 live Custom Formats, and test harnesses with zero drift.

---

## 2. Final Release Arbitration Architecture Reference

The production media stack is permanently configured with the **Unified 4-Tier Decision Ladder**:

```markdown
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 1: Preferred AV1 (ChopperHitler, CoSMiCSuRFeR, UH)                    │
│  Score Band: ~4,500 – 5,950  [AV1 +3500 + AV1 Quality +1000 + HDR/Audio]    │
│  Role: Top priority selection; wins automatically over all other tiers.     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if absent)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 2: Review AV1 (RandH, Smokindevil, Rob74K, WhiskeyJack, RAV1NE)       │
│  Score Band: ~3,800 – 5,300  [AV1 +3500 + AV1 Compact +500 + HDR/Audio]     │
│  Role: Allowed fallback; wins over x265 when Tier 1 is absent.              │
│  Guardrail: AV1 Lean 2160p (-3400) demotes undersized releases below x265.  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if absent or penalized)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 3: x265 Reference Fallback (hallowed, MainFrame, Dumpstarr, HONE)     │
│  Score Band: ~2,000 – 2,800  [2160p Quality +2850 - Not AV1 2000 + DV/HDR]  │
│  Role: High-fidelity baseline; wins over failing Review AV1 & Tier 4.       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if absent)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 4: Last Resort AV1 (Bi0hazard, Waldek, SHADOW, Nameless AV1)          │
│  Score Band: ~1,100 – 1,600  [AV1 +3500 - Unmeasured AV1 2400 + HDR/Audio]  │
│  Role: Grabbable (>1000) as last resort, but strictly below Tier 3 x265.    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if bad release)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Universal Hygiene Blocklist (CAM, Screener, Upscale, 3D, Banned Groups)   │
│  Score: -10,000  (Hard Rejected)                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Resolution Scope:** All custom format rules operate within the 2160p UHD quality domain (`Movies 2160p AV1 HQ`, ID `64`). In accordance with Radarr's quality hierarchy, 1080p releases are subordinate and will not win release selection when a qualifying 2160p release is present.

---

## 3. Operational Integrity & Verification Summary

1. **Live Production State:**
   - Radarr4k Quality Profile `Movies 2160p AV1 HQ` (ID `64`) is actively enforcing the rule.
   - Profilarr is synchronized and managing the PCD repository with 0 schema drift.
2. **Field Validation:**
   - 25-title multi-franchise field test (Op 951A) and 8-title full-stack audit (Op 953A) confirmed 100% adherence to the intended arbitration logic.
3. **Repository Cleanliness:**
   - 341 migrations in `ops/` with 0 foreign key or table schema errors.
   - 121 / 121 simulation tests passing in `tests/simulate_scoring.py`.
   - 100% clean tripwire hygiene (0 secrets, 0 absolute local paths).

---

## 4. Formal Evidence Freeze

Effective as of **2026-08-29 (Op 954A)**, the entire evidence suite within the `evidence/` directory is **FROZEN**.

* No new VMAF measurements, policy rule adjustments, or profile scoring modifications are planned.
* The repository at `origin/v2` represents the permanent, authoritative source of truth.
* Any future maintenance operations (e.g. routine database optimizations, minor group regex expansions) will be executed under standard stack maintenance procedures rather than profile experimentation.
