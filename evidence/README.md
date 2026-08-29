# AV1 Evidence Ledger & Calibration Reports

This directory stores empirical fidelity measurements, release verdicts, and calibration study reports for AV1 release groups and reference masters.

---

## 1. Verdict Ledger Schema (`verdicts.csv`)

`verdicts.csv` tracks release assessments, empirical metrics, and confidence states. It is strictly evidence-only, backward-compatible, and human-governed.

| Column | Type | Description |
| :--- | :--- | :--- |
| `date` | ISO 8601 Date | Date of initial record creation or manual audit. |
| `title` | String | Film or series title. |
| `year` | Integer | Release year. |
| `group` | String | Release group name (e.g. `CoSMiCSuRFeR`, `ChopperHitler`, `Rob74K`). |
| `codec` | String | Video codec (`AV1`, `x265`, `h264`). |
| `res` | String | Target resolution (`2160p`, `1080p`). |
| `size_gb` | Float | File size in gigabytes. |
| `runtime_min` | Integer | Media runtime in minutes. |
| `mbps` | Float | Average stream bitrate in megabits per second. |
| `tier_claimed` | String | Nominal/active tier classification at time of record. |
| `source` | String | Record source (`prod`, `shadow`). |
| `verdict` | String | Qualitative status (`PASS`, `REVIEW`, `BORDERLINE`, `FAIL`, `PENDING`, `EXCEPTION`, `VOID`). |
| `vmaf_mean` | Float | Mean VMAF score across standardized 3-scene core. |
| `vmaf_min` | Float | Minimum VMAF score across all measured scenes (core + optional). |
| `psnr_y_mean` | Float | Mean PSNR-Y in dB against reference master. |
| `ssim_mean` | Float | Mean SSIM against reference master. |
| `bpp` | Float | Bits per pixel ($\frac{\text{bitrate}}{\text{width} \times \text{height} \times \text{fps}}$). |
| `reference_master` | String | Reference encode/edition used for parity testing (e.g. `hallowed 2160p x265 HDR/DV`). |
| `scene_count` | Integer | Number of measured scenes contributing to metrics for this title. |
| `title_count` | Integer | Number of distinct same-master-reference titles measured for this release group. |
| `confidence_state` | String | Evidence confidence classification (see definitions below). |
| `evidence_basis` | String | Basis of empirical evidence (`same-master-reference`, `hallowed-relative`, `insufficient-parity`, `none`). |
| `measurement_date` | ISO 8601 Date | Date of most recent empirical calibration measurement. |
| `evidence_doc` | String | Path to associated calibration report document. |
| `notes` | String | Operational and content-specific notes (e.g. grain/dark stress observations). |

---

## 2. Confidence State Definitions

Confidence states classify the depth and repeatability of empirical evidence without automating profile changes:

* **`unmeasured`**: Historical record; no calibrated perceptual measurements recorded yet.
* **`single-title`**: Empirical evidence derived from exactly one title (e.g. $n=1$, 3 core scenes).
* **`candidate`**: Multi-title evidence ($\ge 2$ titles or $\ge 6$ scenes) with solid mean performance and no obvious content-specific failure.
* **`high-confidence`**: Robust multi-title evidence ($\ge 2$ titles, $\ge 6$ scenes) where all scene-level metrics meet or exceed draft target floors (e.g., minimum scene VMAF $\ge 93.0$ once adopted).
* **`review`**: Inconsistent performance or content-specific failure (e.g. strong on clean transfers, weak on heavy 35mm grain / low-light scenes); requires manual human review.
* **`insufficient-parity`**: Measured, but parity with reference master is questionable (different color grade, mismatched HDR/DV transfer, or different source master).

---

## 3. Evidence Basis Definitions

* **`same-master-reference`**: A credible candidate/reference pairing with confirmed same title, edition/cut, source/master parity, runtime, resolution, frame rate, aspect ratio, HDR/DV metadata behavior, and spatial/temporal alignment. Directly supports group-level `title_count` increments and group confidence-state evaluation.
* **`hallowed-relative`**: A credible Hallowed→AV1 comparison with confirmed parity between Hallowed and AV1, but where no higher-quality reference was available in the selected pair. Provides descriptive evidence regarding incremental loss relative to the user's accepted practical Hallowed baseline. Does not count toward same-master `title_count` and does not independently promote group confidence state.
* **`insufficient-parity`**: A measurement was attempted or recorded, but transfer remastering, color grading, HDR/DV curves, theatrical cut, or runtime divergence rendered the comparison technically invalid. Preserved for auditability with blank `title_count` and `confidence_state=insufficient-parity`.
* **`none`**: No usable empirical calibration evidence exists (historical audit rows, shadow probes, unmeasured entries, pending, or exception rows). Populated with blank measurement metrics, blank `title_count`, and `confidence_state=unmeasured`.

---

## 4. Calibration Reports & Datasets

* **Op 938 Baseline Study:**
  * Report: [`av1_calibration_report.md`](av1_calibration_report.md)
  * Raw Metrics: [`av1_calibration_raw.json`](av1_calibration_raw.json)
* **Op 939 Calibration Expansion (Grain, Dark HDR & Group Diversity):**
  * Report: [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md)
  * Raw Metrics: [`av1_calibration_expansion_raw.json`](av1_calibration_expansion_raw.json)
* **Op 940B Targeted Candidate Calibration (CoSMiCSuRFeR JW3):**
  * Report: [`av1_calibration_cosmicsurfer_jw3_report.md`](av1_calibration_cosmicsurfer_jw3_report.md)
  * Raw Metrics: [`av1_calibration_cosmicsurfer_jw3_raw.json`](av1_calibration_cosmicsurfer_jw3_raw.json)
* **Op 941A Targeted Candidate Calibration (RandH Gladiator):**
  * Report: [`av1_calibration_randh_gladiator_report.md`](av1_calibration_randh_gladiator_report.md)
  * Raw Metrics: [`av1_calibration_randh_gladiator_raw.json`](av1_calibration_randh_gladiator_raw.json)
* **Op 942 Multi-Group Stratified Calibration Campaign:**
  * Pre-Registered Manifest: [`av1_stratified_calibration_manifest.json`](av1_stratified_calibration_manifest.json)
  * Campaign Report: [`av1_stratified_calibration_campaign_report.md`](av1_stratified_calibration_campaign_report.md)
  * Raw Metrics: [`av1_stratified_calibration_campaign_raw.json`](av1_stratified_calibration_campaign_raw.json)
* **Op 943A Hallowed x265 Quality-Baseline Calibration:**
  * Pre-Registered Manifest: [`hallowed_baseline_calibration_manifest.json`](hallowed_baseline_calibration_manifest.json)
  * Calibration Report: [`hallowed_baseline_calibration_report.md`](hallowed_baseline_calibration_report.md)
  * Raw Metrics: [`hallowed_baseline_calibration_raw.json`](hallowed_baseline_calibration_raw.json)
* **Op 944A AV1 Library Group Inventory & Expanded Baseline Campaign:**
  * Inventory: [`av1_library_inventory_944a.json`](av1_library_inventory_944a.json)
  * Pre-Registered Manifest: [`av1_expanded_three_way_manifest_944a.json`](av1_expanded_three_way_manifest_944a.json)
  * Campaign Report: [`av1_expanded_three_way_campaign_report_944a.md`](av1_expanded_three_way_campaign_report_944a.md)
  * Raw Metrics: [`av1_expanded_three_way_campaign_raw_944a.json`](av1_expanded_three_way_campaign_raw_944a.json)
* **Op 945A Evidence-Led Verdict Ledger Consolidation:**
  * Consolidated Ledger: [`verdicts.csv`](verdicts.csv)
  * Consolidation Report: [`verdict_ledger_consolidation_945a_report.md`](verdict_ledger_consolidation_945a_report.md)
  * Raw Metrics: [`verdict_ledger_consolidation_945a_raw.json`](verdict_ledger_consolidation_945a_raw.json)
  * Validator: [`../scripts/validate_verdict_ledger_945a.py`](../scripts/validate_verdict_ledger_945a.py)
* **Op 946A Evidence-Led Policy Simulation Harness:**
  * Simulation Script: [`../scripts/simulate_av1_policy_946a.py`](../scripts/simulate_av1_policy_946a.py)
  * Simulation Report: [`av1_policy_simulation_946a_report.md`](av1_policy_simulation_946a_report.md)
  * Raw Simulation Metrics: [`av1_policy_simulation_946a_raw.json`](av1_policy_simulation_946a_raw.json)
* **Op 947A Targeted Evidence Expansion for Review Groups:**
  * Expansion Plan Document: [`av1_targeted_expansion_plan_947a.md`](av1_targeted_expansion_plan_947a.md)
  * Pre-Registered Manifest: [`av1_targeted_expansion_manifest_947a.json`](av1_targeted_expansion_manifest_947a.json)
  * Summary Report: [`av1_targeted_expansion_report_947a.md`](av1_targeted_expansion_report_947a.md)
  * Raw Expansion Data: [`av1_targeted_expansion_raw_947a.json`](av1_targeted_expansion_raw_947a.json)
  * Validator: [`../scripts/plan_av1_targeted_expansion_947a.py`](../scripts/plan_av1_targeted_expansion_947a.py)
* **Op 948A Targeted Expansion Measurements:**
  * Campaign Report: [`av1_targeted_expansion_measurements_948a_report.md`](av1_targeted_expansion_measurements_948a_report.md)
  * Raw Metrics: [`av1_targeted_expansion_measurements_948a_raw.json`](av1_targeted_expansion_measurements_948a_raw.json)
  * Runner: [`../scripts/run_av1_targeted_expansion_measurements_948a.py`](../scripts/run_av1_targeted_expansion_measurements_948a.py)
* **Op 949A Hybrid AV1 Profile Rule (Finish Line):**
  * Full Specification Document: [`hybrid_av1_profile_rule_949a.md`](hybrid_av1_profile_rule_949a.md)
  * Summary Report: [`hybrid_av1_profile_rule_949a_report.md`](hybrid_av1_profile_rule_949a_report.md)
  * Mapping Schema JSON: [`hybrid_av1_profile_mapping_949a.json`](hybrid_av1_profile_mapping_949a.json)
  * Threshold Raw Dataset: [`hybrid_av1_profile_thresholds_949a_raw.json`](hybrid_av1_profile_thresholds_949a_raw.json)
  * Validator: [`../scripts/validate_hybrid_profile_rule_949a.py`](../scripts/validate_hybrid_profile_rule_949a.py)
* **Op 950A Live Hybrid AV1 Profile Rule Application (Option A):**
  * Application Report: [`hybrid_av1_profile_apply_950a_report.md`](hybrid_av1_profile_apply_950a_report.md)
  * Raw Config & Search Results: [`hybrid_av1_profile_apply_950a_raw.json`](hybrid_av1_profile_apply_950a_raw.json)
* **Op 951A Hybrid AV1 Profile Field Test (25 Titles):**
  * Field Test Report: [`hybrid_av1_profile_field_test_951a_report.md`](hybrid_av1_profile_field_test_951a_report.md)
  * Raw Test Results: [`hybrid_av1_profile_field_test_951a_raw.json`](hybrid_av1_profile_field_test_951a_raw.json)
  * Test Runner: [`../scripts/run_hybrid_av1_field_test_951a.py`](../scripts/run_hybrid_av1_field_test_951a.py)
* **Op 952A Fix Unmeasured AV1 Tier 4 Scoring:**
  * Report: [`av1_tier4_scoring_fix_952a_report.md`](av1_tier4_scoring_fix_952a_report.md)
  * Raw Snapshot & Verification: [`av1_tier4_scoring_fix_952a_raw.json`](av1_tier4_scoring_fix_952a_raw.json)
  * PCD SQL Migration: [`../ops/952.add-av1-unmeasured-encoders-tier4-scoring.sql`](../ops/952.add-av1-unmeasured-encoders-tier4-scoring.sql)

---

## 5. Governance & Human-in-the-Loop Principles

1. **Evidence-Only:** Metrics and confidence states provide structured data to guide future manual decisions. They do not alter active Custom Formats, profile scores, or tier membership automatically.
2. **Fidelity-First:** Promotion evaluations require repeated same-master multi-title fidelity (minimum scene floor and mean VMAF) before any tier changes are considered.
