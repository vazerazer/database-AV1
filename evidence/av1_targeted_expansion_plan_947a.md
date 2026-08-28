# Targeted Evidence Expansion Plan for Review & Transition Groups (Op 947A)
**Date:** 2026-08-28
**Scope:** Planning and Candidate Pairing for Groups Shifting Behavior in Op 946A Simulation (`RandH`, `Smokindevil`, `Rob74K`, `Bi0hazard`, `Waldek`)
**Artifacts Generated:**
- Planner & Validator: [`../scripts/plan_av1_targeted_expansion_947a.py`](../scripts/plan_av1_targeted_expansion_947a.py)
- Pre-Registered Manifest: [`av1_targeted_expansion_manifest_947a.json`](av1_targeted_expansion_manifest_947a.json)
- Raw Expansion Data: [`av1_targeted_expansion_raw_947a.json`](av1_targeted_expansion_raw_947a.json)
- Summary Report: [`av1_targeted_expansion_report_947a.md`](av1_targeted_expansion_report_947a.md)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is a planning and documentation artifact only. It does not alter active profiles, tiers, scores, Custom Formats, Radarr/Profilarr configuration, release restrictions, download rules, media files, or live automation. All thresholds remain non-enforcing DRAFT.

---

## 1. Context & Objectives

In Op 946A, policy simulation revealed that while candidate groups (`ChopperHitler`, `CoSMiCSuRFeR`) remain stable across all policy scenarios, review groups (`RandH`, `Smokindevil`, `Rob74K`) and unmeasured single-title groups (`Bi0hazard`, `Waldek`) experience sharp behavioral shifts between permissive (`baseline_current`, `relaxed_review_allowed`) and strict (`strict_candidate_only`) models.

The purpose of this operation is to establish an objective, pre-registered expansion plan to deepen empirical evidence for these transition groups, identifying credible same-master and Hallowed-relative comparison pairs where available, and documenting inventory exhaustion where no further local media exists.

---

## 2. Current State Summary of Target Groups

| Group | `confidence_state` | Same-Master `title_count` | `evidence_basis` Distribution | Op 946A Scenario Transition Behavior |
| :--- | :---: | :---: | :--- | :--- |
| **`RandH`** | `review` | 3 | 3 same-master, 1 Hallowed-relative, 4 none | Shifts from allowed fallback (4 titles) to completely blocked (0 titles) in `strict_candidate_only`. |
| **`Smokindevil`** | `review` | 2 | 2 same-master, 1 Hallowed-relative, 0 none | Shifts from allowed fallback (3 titles) to completely blocked (0 titles) in `strict_candidate_only`. |
| **`Rob74K`** | `review` | 2 | 2 same-master, 0 Hallowed-relative, 0 none | Shifts from allowed fallback (2 titles) to completely blocked (0 titles) in `strict_candidate_only`. |
| **`Bi0hazard`** | `unmeasured` | 0 | 0 same-master, 1 Hallowed-relative, 1 none | Blocked across all scenarios due to unmeasured single-title status. |
| **`Waldek`** | `unmeasured` | 0 | 0 same-master, 1 Hallowed-relative, 0 none | Blocked across all scenarios due to unmeasured single-title status and low VMAF floor. |

---

## 3. Targeted Candidate Pairing & Parity Analysis

### 1. `RandH` (Expansion Status: *Local Candidates Available*)
* **Proposed Title 1:** *The Bourne Supremacy* (2004)
  * **AV1 Identity:** `The.Bourne.Supremacy.2004-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H` (6.83 GB, 8.63 Mbps)
  * **Reference Counterpart:** `The.Bourne.Supremacy.2004.UHD.BluRay.2160p.DTS-HD.MA.5.1.DV.HDR10.x265-MainFrame` (22.28 GB, 28.17 Mbps)
  * **Hallowed Counterpart:** `The.Bourne.Supremacy.2004.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed` (14.91 GB, 18.85 Mbps)
  * **Target Evidence Basis:** `same-master-reference`
  * **Parity Rationale:** Same-master 2160p UHD BluRay transfer; verified in Op 943A baseline calibration with 95.31 mean VMAF against MainFrame reference.
  * **Stress Categories:** Super 35 heavy optical grain, rapid handheld shaky-cam motion, Munich night shadows.
* **Proposed Title 2:** *Jack Reacher* (2012)
  * **AV1 Identity:** `Jack.Reacher.2012.2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H` (6.74 GB, 7.15 Mbps)
  * **Hallowed Counterpart:** `Jack.Reacher.2012.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed` (15.68 GB, 16.64 Mbps)
  * **Target Evidence Basis:** `hallowed-relative`
  * **Parity Rationale:** Matching 3840x1600 canvas, 23.976 fps, and HDR10 PQ metadata.
  * **Stress Categories:** Low-light bar shadows, high-speed muscle car chase, fine facial 35mm grain.
* **Proposed Title 3:** *Blade Runner* (1982) The Final Cut
  * **AV1 Identity:** `Blade.Runner.The.Final.Cut.1982-2160p.BluRay.HDR10.10.bit.Encode.AV1.TrueHD.Atmos.7.1-R and H` (7.11 GB, 8.23 Mbps)
  * **Hallowed Counterpart:** `Blade.Runner.The.Final.Cut.1982.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.x265-hallowed` (15.69 GB, 18.30 Mbps)
  * **Target Evidence Basis:** `hallowed-relative`
  * **Parity Rationale:** Matching 3840x1600 canvas and 23.976 fps on The Final Cut 4K master.
  * **Stress Categories:** Pitch-black urban shadows, optical film grain, volumetric smoke & mist, neon specular highlights.

---

### 2. `Smokindevil` (Expansion Status: *Partially Exhausted — Remux Acquisition Planned*)
* **Proposed Title 1:** *The Sixth Sense* (1999)
  * **AV1 Identity:** `The.Sixth.Sense.1999.2160p.UHD.BluRay.HDR10.DD+5.1.AV1-Smokindevil` (15.02 GB, 18.65 Mbps)
  * **Reference Counterpart:** *Targeting 1:1 UHD BluRay Remux master acquisition*
  * **Hallowed Counterpart:** `The.Sixth.Sense.1999.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed` (15.12 GB, 18.77 Mbps)
  * **Target Evidence Basis:** `same-master-reference` (upon Remux acquisition)
  * **Parity Rationale:** Measured in Op 944A as Hallowed-relative (86.25 mean / 83.92 floor). Acquiring a 1:1 Remux will convert this into a same-master reference calibration.
* **Local Inventory Status:** Exhausted ($n=4$ titles in local library: *Fury* and *Shawshank* measured same-master; *Sixth Sense* measured Hallowed-relative; *Jurassic Park* excluded due to 2018 25th Ann. vs 2023 30th Ann. master mismatch).

---

### 3. `Rob74K` (Expansion Status: *Local Inventory Exhausted*)
* **Local Inventory Status:** Exhausted. Both available local 2160p releases (*John Wick 1* and *John Wick 2*) are already measured and committed in `verdicts.csv`.
* **Expansion Requirement:** External candidate discovery and acquisition of new 2160p Rob74K releases.

---

### 4. `Bi0hazard` (Expansion Status: *Remux Acquisition & Discovery Planned*)
* **Proposed Title 1:** *The Bourne Ultimatum* (2007)
  * **AV1 Identity:** `Das.Bourne.Ultimatum.2007.German.DUBBED.DL.EAC3.2160p.HDR.BluRay.AV1-Bi0hazard` (18.70 GB, 21.63 Mbps)
  * **Reference Counterpart:** *Targeting 1:1 UHD BluRay Remux master acquisition*
  * **Hallowed Counterpart:** `The.Bourne.Ultimatum.2007.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed` (16.31 GB, 18.86 Mbps)
  * **Target Evidence Basis:** `same-master-reference` (upon Remux acquisition)
  * **Parity Rationale:** Measured in Op 944A as Hallowed-relative (98.55 mean / 97.06 floor). Remux calibration will establish ground-truth fidelity.

---

### 5. `Waldek` (Expansion Status: *Remux Acquisition & Discovery Planned*)
* **Proposed Title 1:** *John Wick: Chapter 2* (2017)
  * **AV1 Identity:** `John.Wick.Chapter.2.2017.BluRay.2160p.UHD.AV1.HDR10.TrueHD.7.1.Atmos.PRL.Waldek` (16.03 GB, 17.46 Mbps)
  * **Reference Counterpart:** *Targeting 1:1 UHD BluRay Remux master acquisition*
  * **Hallowed Counterpart:** `John.Wick.Chapter.2.2017.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed` (15.46 GB, 16.85 Mbps)
  * **Target Evidence Basis:** `same-master-reference` (upon Remux acquisition)
  * **Parity Rationale:** Measured in Op 944A as Hallowed-relative (70.71 mean / 63.31 floor). Remux calibration will establish whether textural degradation originates from encoding parameters or source preprocessing.

---

## 4. Measurement Methodology & Integration Framework

1. **Standardized 4-Scene Stratified Sampling:**
   * **Scene 1 (Low-Light / Near-Black):** Focus on shadow grain retention, macroblocking in step-down luma gradients, and near-black noise.
   * **Scene 2 (Fine Texture / High Spatial Frequency):** Focus on fabric weave, facial pores, foliage, and architectural edges.
   * **Scene 3 (High-Motion / Dynamic Particle Stress):** Focus on fast camera pans, action sequences, water splashes, and particle debris.
   * **Scene 4 (Challenging Content / Optical Stress):** Focus on heavy 35mm optical grain, volumetric smoke, and neon specular highlights.
2. **Alignment & Metric Pipeline:**
   * Temporal offset scanning ($\pm 2000\text{ ms}$) using frame hash matching.
   * Native 4K YUV420P10 computation via `libvmaf` (`vmaf_v0.6.1.json`), PSNR-Y, and SSIM.
3. **Future Ledger Integration:**
   * New same-master reference calibrations will increment group `title_count`.
   * Hallowed-relative measurements will populate with blank `title_count` and `evidence_basis=hallowed-relative`.
   * Group confidence state reassessment will follow strict multi-title consensus rules (zero automatic promotions).

---

## 5. Limitations & Exclusions

* **Excluded Local Titles:**
  * *Jurassic Park (1993)* [Smokindevil]: Excluded due to 2018 25th Anniversary vs 2023 30th Anniversary color remaster mismatch.
  * *The Deer Hunter (1978)* [RandH]: Excluded due to StudioCanal vs Shout Factory master transfer mismatch.
  * *The Wolverine (2013)* [RandH]: Excluded due to Extended Cut vs Theatrical Cut runtime divergence.
* **Non-Operational Guardrail Confirmation:** Zero active operational configurations, Custom Formats, profile scores, tier assignments, release restrictions, download rules, media files, or running containers were modified.
