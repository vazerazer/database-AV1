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
| `title_count` | Integer | Number of distinct titles measured for this release group. |
| `confidence_state` | String | Evidence confidence classification (see definitions below). |
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

## 3. Calibration Reports & Datasets

* **Op 938 Baseline Study:**
  * Report: [`av1_calibration_report.md`](av1_calibration_report.md)
  * Raw Metrics: [`av1_calibration_raw.json`](av1_calibration_raw.json)
* **Op 939 Calibration Expansion (Grain, Dark HDR & Group Diversity):**
  * Report: [`av1_calibration_expansion_report.md`](av1_calibration_expansion_report.md)
  * Raw Metrics: [`av1_calibration_expansion_raw.json`](av1_calibration_expansion_raw.json)
* **Op 940B Targeted Candidate Calibration (CoSMiCSuRFeR JW3):**
  * Report: [`av1_calibration_cosmicsurfer_jw3_report.md`](av1_calibration_cosmicsurfer_jw3_report.md)
  * Raw Metrics: [`av1_calibration_cosmicsurfer_jw3_raw.json`](av1_calibration_cosmicsurfer_jw3_raw.json)

---

## 4. Governance & Human-in-the-Loop Principles

1. **Evidence-Only:** Metrics and confidence states provide structured data to guide future manual decisions. They do not alter active Custom Formats, profile scores, or tier membership automatically.
2. **Fidelity-First:** Promotion evaluations require repeated same-master multi-title fidelity (minimum scene floor and mean VMAF) before any tier changes are considered.
