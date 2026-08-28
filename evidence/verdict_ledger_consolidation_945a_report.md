# Evidence-Led Verdict Ledger Consolidation Report (Op 945A)
**Date:** 2026-08-28
**Scope:** Verdict Ledger Schema Extension (`evidence_basis`), Invariant Formalization, and Consolidation of Historic & Op 944A Evidence into `evidence/verdicts.csv`
**Artifacts Generated:**
- Consolidated Ledger: [`verdicts.csv`](verdicts.csv)
- Raw Consolidation Audit: [`verdict_ledger_consolidation_945a_raw.json`](verdict_ledger_consolidation_945a_raw.json)
- Validation Script: [`../scripts/validate_verdict_ledger_945a.py`](../scripts/validate_verdict_ledger_945a.py)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is data-model and evidence-governance work only. Zero modifications were made to Radarr, Profilarr, Custom Formats, profiles, scores, tier behavior, release restrictions, downloads, media, or live automation. All thresholds remain non-enforcing DRAFT.

---

## 1. Objective, Scope & Governance Guardrails

* **Purpose:**
  1. Extend `evidence/verdicts.csv` with a dedicated `evidence_basis` field to formally differentiate between:
     - Credible same-master UHD reference calibrations;
     - Descriptive Hallowed→AV1-only relative observations;
     - Excluded insufficient-parity transfer mismatches;
     - Unmeasured / historical audit entries.
  2. Ingest the descriptive Hallowed→AV1-only observations from Op 944A into the ledger with strict guardrails (blank `title_count`, no confidence-state promotion).
  3. Enforce programmatic ledger invariants via `scripts/validate_verdict_ledger_945a.py`.

---

## 2. Verdict Ledger Schema Evolution

### Original Schema (24 columns):
```text
date, title, year, group, codec, res, size_gb, runtime_min, mbps, tier_claimed, source, verdict, vmaf_mean, vmaf_min, psnr_y_mean, ssim_mean, bpp, reference_master, scene_count, title_count, confidence_state, measurement_date, evidence_doc, notes
```

### Final Extended Schema (25 columns):
```text
date, title, year, group, codec, res, size_gb, runtime_min, mbps, tier_claimed, source, verdict, vmaf_mean, vmaf_min, psnr_y_mean, ssim_mean, bpp, reference_master, scene_count, title_count, confidence_state, evidence_basis, measurement_date, evidence_doc, notes
```

---

## 3. Definitions of `evidence_basis` Values

1. **`same-master-reference`:**
   * A credible candidate/reference pairing with confirmed same title, edition/cut, source/master parity, runtime, resolution, frame rate, aspect ratio, HDR/DV metadata behavior, and spatial/temporal alignment.
   * Directly supports group-level `title_count` increments and group confidence-state evaluation.
2. **`hallowed-relative`:**
   * A credible Hallowed→AV1 comparison with confirmed parity between Hallowed and AV1, but where no higher-quality reference was available in the selected pair.
   * Provides descriptive evidence regarding incremental loss relative to the user's accepted practical Hallowed baseline.
   * Does not count toward same-master `title_count` and does not independently promote group confidence state.
3. **`insufficient-parity`:**
   * A measurement was attempted or recorded, but transfer remastering, color grading, HDR/DV curves, theatrical cut, or runtime divergence rendered the comparison technically invalid.
   * Preserved for complete auditability with blank `title_count` and `confidence_state=insufficient-parity`.
4. **`none`:**
   * No usable empirical calibration evidence exists (historical audit rows, shadow probes, unmeasured entries, pending, or exception rows).
   * Populated with blank measurement metrics, blank `title_count`, and `confidence_state=unmeasured`.

---

## 4. Group-by-Group Evidence-Basis Mapping & Ledger Separation

### Category A: Same-Master-Reference Evidence ($n=12$ rows)
*Credible candidate/reference pairs supporting same-master `title_count` and confidence state.*

| Group | Title (Year) | VMAF Mean | VMAF Min | PSNR-Y ($dB$) | SSIM | BPP | `title_count` | `confidence_state` | `evidence_basis` | Supporting Evidence Doc |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`ChopperHitler`** | *X-Men* (2000) | 93.44 | 91.10 | 47.92 | 0.9965 | 0.1190 | 3 | `candidate` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`ChopperHitler`** | *X-Men: Days of Future Past* (2014) | 97.16 | 96.84 | 48.82 | 0.9978 | 0.0884 | 3 | `candidate` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`ChopperHitler`** | *X-Men: Apocalypse* (2016) | 96.72 | 94.48 | 49.25 | 0.9981 | 0.0789 | 3 | `candidate` | `same-master-reference` | [`av1_stratified_calibration_campaign_report.md`](av1_stratified_calibration_campaign_report.md) |
| **`CoSMiCSuRFeR`** | *John Wick: Chapter 3* (2019) | 92.81 | 88.85 | 41.74 | 0.9957 | 0.2558 | 2 | `candidate` | `same-master-reference` | [`av1_calibration_cosmicsurfer_jw3_report.md`](av1_calibration_cosmicsurfer_jw3_report.md) |
| **`CoSMiCSuRFeR`** | *John Wick: Chapter 4* (2023) | 97.06 | 96.79 | 48.43 | 0.9980 | 0.1014 | 2 | `candidate` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`RandH`** | *John Wick* (2014) | 87.16 | 83.52 | 38.27 | 0.9931 | 0.0588 | 3 | `review` | `same-master-reference` | [`av1_stratified_calibration_campaign_report.md`](av1_stratified_calibration_campaign_report.md) |
| **`RandH`** | *Interstellar* (2014) | 95.61 | 93.21 | 47.27 | 0.9968 | 0.0707 | 3 | `review` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`RandH`** | *Gladiator* (2000) | 91.25 | 90.02 | 44.17 | 0.9945 | 0.0675 | 3 | `review` | `same-master-reference` | [`av1_calibration_randh_gladiator_report.md`](av1_calibration_randh_gladiator_report.md) |
| **`Smokindevil`** | *Fury* (2014) | 76.02 | 66.77 | 40.45 | 0.9584 | 0.0711 | 2 | `review` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`Smokindevil`** | *The Shawshank Redemption* (1994) | 93.78 | 92.62 | 48.24 | 0.9963 | 0.0265 | 2 | `review` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`Rob74K`** | *John Wick* (2014) | 72.42 | 68.61 | 27.55 | 0.9082 | 0.1239 | 2 | `review` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |
| **`Rob74K`** | *John Wick: Chapter 2* (2017) | 77.38 | 73.55 | 26.95 | 0.7847 | 0.1005 | 2 | `review` | `same-master-reference` | [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md) |

### Category B: Hallowed-Relative-Only Evidence ($n=5$ rows)
*Descriptive incremental loss observations relative to Hallowed; blank `title_count`; non-promoting.*

| Group | Title (Year) | VMAF Mean | VMAF Min | PSNR-Y ($dB$) | SSIM | BPP | `title_count` | `confidence_state` | `evidence_basis` | Supporting Evidence Doc |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`ChopperHitler`** | *X-Men: Dark Phoenix* (2019) | 95.45 | 94.22 | 49.10 | 0.9979 | 0.0501 | *(blank)* | `candidate` | `hallowed-relative` | [`av1_expanded_three_way_campaign_report_944a.md`](av1_expanded_three_way_campaign_report_944a.md) |
| **`RandH`** | *The Bourne Ultimatum* (2007) | 97.06 | 96.12 | 48.59 | 0.9963 | 0.0611 | *(blank)* | `review` | `hallowed-relative` | [`av1_expanded_three_way_campaign_report_944a.md`](av1_expanded_three_way_campaign_report_944a.md) |
| **`Smokindevil`** | *The Sixth Sense* (1999) | 86.25 | 83.92 | 42.18 | 0.9948 | 0.0976 | *(blank)* | `review` | `hallowed-relative` | [`av1_expanded_three_way_campaign_report_944a.md`](av1_expanded_three_way_campaign_report_944a.md) |
| **`Bi0hazard`** | *The Bourne Ultimatum* (2007) | 98.55 | 97.06 | 50.35 | 0.9983 | 0.1469 | *(blank)* | `unmeasured` | `hallowed-relative` | [`av1_expanded_three_way_campaign_report_944a.md`](av1_expanded_three_way_campaign_report_944a.md) |
| **`Waldek`** | *John Wick: Chapter 2* (2017) | 70.71 | 63.31 | 37.29 | 0.9608 | 0.1185 | *(blank)* | `unmeasured` | `hallowed-relative` | [`av1_expanded_three_way_campaign_report_944a.md`](av1_expanded_three_way_campaign_report_944a.md) |

### Category C: Insufficient-Parity Exclusions ($n=1$ row)
*Technical transfer/grading mismatches preserved for auditability.*

| Group | Title (Year) | VMAF Mean | VMAF Min | PSNR-Y ($dB$) | SSIM | `title_count` | `confidence_state` | `evidence_basis` | Rationale |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`CoSMiCSuRFeR`** | *LOTR: Fellowship of the Ring* (2001) | 78.22 | 76.71 | 27.95 | 0.9224 | *(blank)* | `insufficient-parity` | `insufficient-parity` | Color grading remaster divergence vs Hallowed. |

### Category D: Historical Audit & Unmeasured Entries ($n=12$ rows)
*Historical audit rows, shadow probes, exceptions, anchors, and pending grabs with no empirical calibration metrics (`evidence_basis=none`, `title_count` blank, `confidence_state=unmeasured`).*

---

## 5. Title-Count & Confidence-State Methodologies

1. **`title_count` Invariant:**
   * Defined exclusively as the number of unique, credible **`same-master-reference`** titles measured for that group.
   * `hallowed-relative`, `insufficient-parity`, and `none` rows leave `title_count` strictly blank (`""`).
   * Every `same-master-reference` row for a given group reflects the exact group-level total (`3` for ChopperHitler, `2` for CoSMiCSuRFeR, `3` for RandH, `2` for Smokindevil, `2` for Rob74K).
2. **`confidence_state` Invariant:**
   * Existing validated group classifications are rigorously preserved:
     - `ChopperHitler`: `candidate`
     - `CoSMiCSuRFeR`: `candidate`
     - `RandH`: `review`
     - `Smokindevil`: `review`
     - `Rob74K`: `review`
     - `SHADOW`: `unmeasured`
   * Newly measured groups from Op 944A (`Bi0hazard` and `Waldek`) remain `confidence_state=unmeasured` because single-title Hallowed-relative observations do not constitute a sufficient sample to promote or broadly convict a group.
   * Zero groups hold `high-confidence`.

---

## 6. Hallowed Baseline Status & Operational Confirmation

1. **Hallowed Status Confirmation:** Hallowed is the user's accepted practical baseline (Op 943A: 95.56 mean VMAF), not an AV1 release group. No AV1 group entry for Hallowed exists in `verdicts.csv`.
2. **Operational Guardrail Confirmation:** Zero active operational policies, tier assignments, Custom Formats, profile scores, Radarr/Profilarr behavior, download rules, or live automations were modified.

---

## 7. Limitations & Recommendations for Future Evidence Work

* **Display-Side Visual Review:** All ledger entries are derived from objective metrics (libvmaf 4K, PSNR-Y, SSIM) without display-side subjective review.
* **Reference Master Acquisition:** Priority for future evidence campaigns should focus on acquiring 1:1 lossless UHD Remux masters for candidate titles to convert `hallowed-relative` observations into full `same-master-reference` calibrations.
