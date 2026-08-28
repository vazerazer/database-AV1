# Hybrid AV1 Profile Rule Report (Op 949A — Finish Line)
**Date:** 2026-08-28
**Scope:** Final Synthesis and Policy Architecture Report for Hybrid AV1→x265 Release Selection
**Artifacts Generated:**
- Full Specification Document: [`hybrid_av1_profile_rule_949a.md`](hybrid_av1_profile_rule_949a.md)
- Mapping Schema JSON: [`hybrid_av1_profile_mapping_949a.json`](hybrid_av1_profile_mapping_949a.json)
- Threshold Derivation Dataset: [`hybrid_av1_profile_thresholds_949a_raw.json`](hybrid_av1_profile_thresholds_949a_raw.json)
- Rule Validation Harness: [`../scripts/validate_hybrid_profile_rule_949a.py`](../scripts/validate_hybrid_profile_rule_949a.py)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is an architectural synthesis and design report only. Zero modifications were made to active profiles, tiers, scores, Custom Formats, Radarr/Profilarr configuration, release restrictions, download rules, media files, or live automation. All thresholds remain non-enforcing DRAFT.

---

## 1. Executive Summary

Op 949A establishes the final **Hybrid AV1→x265 Release-Selection Rule**, completing the empirical calibration and policy design campaign (Ops 938–949A).

### Key Architectural Pillars:
1. **Tier 1 (Preferred AV1):** `ChopperHitler` and `CoSMiCSuRFeR` are scored highest ($\ge 2300$), delivering immediate bandwidth efficiency when pristine candidate AV1 releases are available.
2. **Tier 2 (Guarded Review AV1):** `RandH`, `Smokindevil`, and `Rob74K` are permitted as secondary alternatives ($1500 - 2000$), but are protected by concrete numeric quality guardrails ($\text{VMAF Mean} \ge 90.0$, $\text{VMAF Min} \ge 85.0$, $\text{Bitrate} \ge 8.0\text{ Mbps}$).
3. **Tier 3 (x265 Reference Fallback):** High-quality x265 releases (`hallowed`, `Dumpstarr 4K`, `MainFrame`, `Framestor`, etc.) are scored at $1000 - 1400$, automatically winning release selection over failing review AV1 or unmeasured releases.
4. **Tier 4 (Last-Resort AV1 / Quarantine):** Unmeasured groups (`Bi0hazard`, `Waldek`, `SHADOW`) and sub-threshold releases are scored lowest ($0 - 400$), safely quarantined until same-master parity is proven.

---

## 2. Tier Summary & Group Mapping

| Tier Level | Designation | Eligible Release Groups | Required Evidence & Confidence | Target Score Band | Selection Behavior |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Tier 1** | **Preferred AV1** | `ChopperHitler`, `CoSMiCSuRFeR` | `candidate` (`same-master` or `hallowed-relative`) | **`>= 2300`** | Preferred over all other tiers; transparent AV1 streaming. |
| **Tier 2** | **Review AV1 Fallback** | `RandH`, `Smokindevil`, `Rob74K` | `review` (`same-master` or `hallowed-relative`) | **`1500 - 2000`** | Permitted if $\ge 90.0$ mean, $\ge 85.0$ min, $\ge 8.0$ Mbps; demoted if failed. |
| **Tier 3** | **x265 Reference Fallback**| `hallowed`, `Dumpstarr 4K`, `MainFrame`, `Framestor` | Reference Baseline ($95.56$ mean VMAF) | **`1000 - 1400`** | Preferred over Tier 4 and failing Tier 2 releases; rock-solid quality floor. |
| **Tier 4** | **Last Resort / Quarantine**| `Bi0hazard`, `Waldek`, `SHADOW`, Unmeasured | `unmeasured` | **`0 - 400`** | Strictly quarantined; selected only if no Tier 1–3 releases exist. |

---

## 3. Concrete Numeric Thresholds (Tier 2 Guardrails)

* **VMAF Mean Minimum:** **`90.0`** (derived from 32-row ledger distribution to prevent general low-bitrate textural softening).
* **VMAF Min Floor:** **`85.0`** (specifically prevents localized grain/shadow collapses, as seen on *Fury* at $66.77$ and *Blade Runner* at $74.55$).
* **2160p Bitrate Floor:** **`8.0 Mbps`** ($0.055\text{ BPP}$) (ensures sufficient bit allocation for high-spatial-frequency noise in 4K canvas).

---

## 4. Governance & Non-Operational Declaration

* Zero active operational configurations, Custom Formats, profile scores, tier assignments, release restrictions, download rules, media files, or running containers were modified.
