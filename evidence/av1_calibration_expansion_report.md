# AV1 Fidelity Calibration Expansion Report (Op 939)
**Date:** 2026-08-28
**Scope:** Expanded Empirical Quality Corpus (Grain, Dark HDR & Group Diversity)
**Corpus:** 8 Total Titles (4 Op 938 + 4 Op 939) $\times$ 27 Calibrated 4K UHD Scenes (24 Standard Core + 3 Optional Near-Black)
**Release Groups Evaluated:** `CoSMiCSuRFeR`, `RandH`, `Smokindevil`, `ChopperHitler`, `Rob74K`

> [!IMPORTANT]
> **Threshold Status:** All AV1 thresholds in ops 938–939 remain **DRAFT**, unenforced, and are not used to change current tier membership or automated scoring.

---

## 0. Tooling & Environment Audit

* **FFmpeg Engine:** `FFmpeg 9.0.1 (static build with gcc 13.2.1)`
* **VMAF Model:** Netflix `vmaf_4k_v0.6.1.json` (4K UHD calibrated)
* **Pixel Pipeline:** Native `yuv420p10le` HDR10 PQ with bicubic dimension normalization (`3840x1600`) and sub-frame offset synchronization.
* **Metric Classification & Tooling Gaps:**
  * **Primary Metric:** VMAF (`vmaf_4k_v0.6.1.json`) is the primary reference-relative fidelity metric for this study.
  * **Secondary Diagnostics:** SSIMULACRA2 was not available and was not measured. `float_ssim` and `PSNR-Y` are secondary diagnostics produced by libvmaf/FFmpeg; they are not substitutes for SSIMULACRA2 and must not be described as such.

---

## 1. Reproducibility & Sample Accounting

*Reconciliation across all 8 anchors in Ops 938 and 939 (27 total valid scenes: 24 standard 3-scene core + 3 permitted optional near-black scenes).*

| Title | AV1 Group | Planned Scenes | Valid Scenes | Rejected Scenes | Optional Near-Black Scene | Timestamps (Valid Scenes) | Reason for Rejected / Extra Scenes |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **`Fury` (2014)** | `Smokindevil` | 3 | 3 | 0 | None | `00:45:00` (Dark)<br>`01:18:20` (Motion)<br>`00:12:30` (Grain) | Standard 3-scene core. 0 rejected. |
| **`John Wick: Chapter 4` (2023)** | `CoSMiCSuRFeR` | 3 | 3 | 0 | None | `00:28:10` (Dark)<br>`01:42:00` (Motion)<br>`02:05:30` (Texture) | Standard 3-scene core. 0 rejected. |
| **`The Shawshank Redemption` (1994)** | `Smokindevil` | 3 | 3 | 0 | None | `00:15:30` (Dark)<br>`01:52:10` (Motion)<br>`00:38:00` (Grain) | Standard 3-scene core. 0 rejected. |
| **`Interstellar` (2014)** | `RandH` | 3 | 3 | 0 | None | `01:02:10` (Dark)<br>`01:21:40` (Motion)<br>`00:08:20` (Texture) | Standard 3-scene core. 0 rejected. |
| **`John Wick` (2014)** | `Rob74K` | 3 | 4 | 0 | `00:36:00` | `00:48:30` (Dark)<br>`00:52:10` (Motion)<br>`00:18:20` (Grain)<br>`00:36:00` (Near-Black) | Extra scene is the permitted optional near-black/gradient scene for dark HDR titles. 0 rejected. |
| **`X-Men` (2000)** | `ChopperHitler` | 3 | 3 | 0 | None | `00:01:20` (Dark)<br>`01:19:10` (Motion)<br>`00:15:30` (Grain) | Standard 3-scene core for 35mm film-grain catalog material. 0 rejected. |
| **`X-Men: Days of Future Past` (2014)** | `ChopperHitler` | 3 | 4 | 0 | `01:48:10` | `00:03:40` (Dark)<br>`00:06:30` (Motion)<br>`00:48:20` (Grain)<br>`01:48:10` (Near-Black) | Extra scene is the permitted optional near-black/gradient scene for dystopian dark HDR titles. 0 rejected. |
| **`John Wick: Chapter 2` (2017)** | `Rob74K` | 3 | 4 | 0 | `01:05:20` | `00:42:10` (Dark)<br>`00:49:30` (Motion)<br>`01:38:00` (Texture)<br>`01:05:20` (Near-Black) | Extra scene is the permitted optional near-black/gradient scene for NYC subway platform shadow gradients. 0 rejected. |

### Dataset Reconciliations:
* **Op 938 Corpus:** 4 titles $\times$ 3 scenes = **12 valid scenes**.
* **Op 939 Corpus:** 4 titles $\times$ 3 core scenes + 3 permitted optional near-black scenes = **15 valid scenes**.
* **Grand Total Combined Corpus:** **27 valid scenes** across 8 same-master UHD BluRay pairs.
* **Standardization:** All multi-title aggregate means use the standardized 3-scene core (24 scenes) to prevent optional 4th scenes from biasing comparisons, with the 3 optional scenes analyzed specifically for near-black gradient stress.

---

## 2. Combined Corpus Summary Table (Ops 938 + 939)

*All 8 anchor pairs evaluated against transparent 4K UHD BluRay reference masters (`hallowed` / `BHDStudio`).*

| Group | Title | Master Edition | Current AV1 Role / Status | AV1 Bitrate | bpp | Mean VMAF (Std 3-Scene) | Min Scene VMAF | Mean PSNR ($Y$) | Mean SSIM | Observed VMAF/Mbps |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`CoSMiCSuRFeR`** | *John Wick: Chapter 4* (2023) | 2160p UHD BluRay | Quality Tier 1 (Active) | 15.02 Mbps | 0.1014 | **97.06** | 96.79 | 48.43 dB | 0.9980 | 6.46 |
| **`RandH`** | *Interstellar* (2014) | 2160p UHD BluRay | Compact Tier (Active) | 14.05 Mbps | 0.0707 | **95.61** | 93.21 | 47.27 dB | 0.9968 | 6.80 |
| **`ChopperHitler`** | *X-Men: Days of Future Past* (2014) | 2160p UHD BluRay | Candidate (2 Titles) | 13.01 Mbps | 0.0884 | **97.16** | 96.84 | 48.82 dB | 0.9978 | 7.47 |
| **`ChopperHitler`** | *X-Men* (2000) | 2160p UHD BluRay | Candidate (2 Titles) | 17.53 Mbps | 0.1190 | **93.44** | 91.10 | 47.92 dB | 0.9965 | 5.33 |
| **`Smokindevil`** | *The Shawshank Redemption* (1994) | 2160p UHD BluRay | Quality Tier 2 (Active) | 5.07 Mbps | 0.0265 | **93.78** | 92.62 | 48.24 dB | 0.9963 | 18.50 |
| **`Smokindevil`** | *Fury* (2014) | 2160p UHD BluRay | Quality Tier 2 (Active) | 10.52 Mbps | 0.0711 | **76.02** | 66.77 | 40.45 dB | 0.9584 | 7.23 |
| **`Rob74K`** | *John Wick: Chapter 2* (2017) | 2160p UHD BluRay | Review Candidate (2 Titles) | 14.80 Mbps | 0.1005 | **77.38** | 73.55 | 26.95 dB | 0.7847 | 5.23 |
| **`Rob74K`** | *John Wick* (2014) | 2160p UHD BluRay | Review Candidate (2 Titles) | 18.25 Mbps | 0.1239 | **72.42** | 68.61 | 27.55 dB | 0.9082 | 3.97 |

---

## 3. Group Evidence Assessment & Confidence

Evidence confidence requires multiple same-master titles and multi-scene stress coverage under identical master parity:

| Release Group | Sampled Titles | Total Scenes | Mean VMAF | Min Scene Floor | Median PSNR ($Y$) | Group Evidence Assessment & Next Steps |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`ChopperHitler`** | 2 | 7 | **95.30** | **91.10** | 48.37 dB | **High-confidence candidate:** two same-master titles and seven measured scenes. Its measured mean VMAF is strong, but its minimum measured scene is 91.10, below the still-draft Tier 1 minimum-scene floor of 93.0. It requires at least one additional same-master title before any promotion or permanent Tier 1 designation is considered. No tier change in this op. |
| **`CoSMiCSuRFeR`** | 1 | 3 | **97.06** | **96.79** | 48.43 dB | **Single-Title Observation.** Pristine multi-scene reference fidelity on *JW4*, but remains an $n=1$ observation requiring at least one additional same-master title for full confidence. No tier change in this op. |
| **`RandH`** | 1 | 3 | **95.61** | **93.21** | 47.27 dB | **Single-Title Observation.** Strong multi-scene performance on *Interstellar*, but remains an $n=1$ observation requiring another same-master title for full confidence. No tier change in this op. |
| **`Smokindevil`** | 2 | 6 | **84.90** | **66.77** | 44.35 dB | **Content-Sensitive in Sample.** Strong performance on *The Shawshank Redemption* (93.78 mean, 92.62 floor), but weak on *Fury* (76.02 mean, 66.77 floor). Preserved in current tier pending further evidence. No tier change in this op. |
| **`Rob74K`** | 2 | 8 | **74.90** | **68.61** | 27.25 dB | **Review Candidate Only.** Two same-master titles show poor measured fidelity (VMAF 72–77, PSNR ~27 dB) despite high bitrates (15–18 Mbps), exhibiting heavy spatial filtering. Preserved without promotion. No tier change in this op. |

---

## 4. Grain & Dark HDR Stress Analysis

Quantifying encoder resilience by measuring the drop from **Best Scene VMAF** to **Hardest Stress Scene VMAF (Dark / Heavy Grain)**:

| Group & Title | Best Scene (VMAF) | Dark / Grain Stress Scene (VMAF) | Fidelity Drop ($\Delta\text{VMAF}$) | Observed Failure Vector |
| :--- | :---: | :---: | :---: | :--- |
| **`CoSMiCSuRFeR`** (*JW4*) | 97.50 (Dark) | 96.79 (Texture) | **$-0.71$ (0.7%)** | None observed |
| **`ChopperHitler`** (*Days of Future Past*) | 97.69 (Grain) | 96.84 (Dark) | **$-0.85$ (0.9%)** | None observed |
| **`RandH`** (*Interstellar*) | 97.34 (Texture) | 93.21 (Motion) | **$-4.13$ (4.2%)** | Mild temporal motion artifacting |
| **`ChopperHitler`** (*X-Men 2000*) | 94.71 (Grain) | 91.10 (Motion) | **$-3.61$ (3.8%)** | Mild high-motion quantization |
| **`Smokindevil`** (*Shawshank*) | 95.45 (Grain) | 92.62 (Dark) | **$-2.83$ (3.0%)** | Slight near-black shadow smoothing |
| **`Smokindevil`** (*Fury*) | 80.77 (Grain) | 66.77 (Dark) | **$-14.00$ (17.3%)** | Severe low-light 35mm grain collapse |
| **`Rob74K`** (*JW2*) | 83.07 (Dark) | 73.55 (Texture) | **$-9.52$ (11.5%)** | Spatial grain smoothing / detail loss |
| **`Rob74K`** (*JW1*) | 76.65 (Motion) | 68.61 (Dark) | **$-8.04$ (10.5%)** | Shadow noise smearing & gamma drift |

---

## 5. Analysis: Content-Specific vs Group-Specific Factors in *Fury*

The expanded corpus contextualizes the *Fury* outcome:
1. **Grain Preservation Feasibility:** *X-Men (2000)* is also a heavy 35mm film catalog scan. On *X-Men (2000)*, `ChopperHitler` preserved 35mm grain with **`VMAF 94.71`** in grain and **`94.52`** in dark scenes, demonstrating that AV1 is not inherently incapable of preserving film grain.
2. **Bitrate Allocation:** `Smokindevil` encoded *Fury* at **10.52 Mbps** ($0.0711\text{ bpp}$). On heavy 35mm low-light film grain, 10.5 Mbps appears insufficient for that encoder's parameter tuning to retain high-frequency grain synthesis without temporal pooling collapse.
3. **Conclusion:** The *Fury* result is **consistent with release-specific encoder bitrate/tuning failure under dark, high-entropy 35mm grain**, rather than an inherent architectural limitation of AV1.

---

## 6. Review & Calibration of Op 938 Draft Thresholds

> [!NOTE]
> **VMAF/Mbps Policy:** VMAF/Mbps is retained as a descriptive efficiency metric only. It is not an eligibility or promotion criterion. AV1 promotion evidence must establish repeated same-master fidelity first: a minimum-scene floor, a mean-fidelity result, and sufficient independent title coverage. Efficiency may be used only as a secondary tie-breaker once fidelity has been established.

| Proposed Threshold | Draft Target | Op 939 Evidence Status | Status & Provisional Rationale |
| :--- | :---: | :--- | :--- |
| **`Tier 1 Mean VMAF`** | $\ge 95.0$ | **DRAFT — retain for validation.** Current measurements demonstrate that individual releases can meet this range; no release group has yet satisfied the complete multi-title evidence standard. | Retained for ongoing multi-title validation. |
| **`Tier 1 Min Scene Floor`** | $\ge 93.0$ | **DRAFT — retain for validation.** Current measurements demonstrate that individual releases can meet this range; no release group has yet satisfied the complete multi-title evidence standard. | Retained for ongoing multi-title validation. |
| **`Tier 1 PSNR ($Y$) Floor`** | $\ge 45.0\text{ dB}$ | **DRAFT — retain for validation.** Distinguishes transparent encodes from filtered releases like *Rob74K* ($27\text{ dB}$). | Retained for ongoing multi-title validation. |
| **`Tier 2 Mean VMAF`** | $\ge 85.0$ | **DRAFT — retain for validation.** Accommodates balanced encodes while rejecting heavily degraded releases. | Retained for ongoing multi-title validation. |
| **`Tier 2 Grain Floor`** | $\ge 80.0$ | **DRAFT — provisional proposal.** Provisional proposal: minimum-scene VMAF $\ge 80.0$ for grain-heavy 4K material, pending validation on at least two additional grain-heavy same-master reference pairs across at least two independent AV1 release groups. | Provisional proposal pending broader grain validation. |
| **`Compact Tier Fidelity`** | $\text{Mean VMAF} \ge 90.0$ | **DRAFT — retain for validation.** Validated by *Interstellar* (95.61) and *Shawshank* (93.78). (Efficiency metric retained for descriptive context only). | Retained as fidelity-first standard. |

---

## 7. Threshold Governance & Decision Standard (DRAFT)

Future tier promotions must adhere to this empirical standard:
1. **Independent Title Requirement:** Minimum **two same-master titles** and **six calibrated scenes** before any promotion is evaluated.
2. **Stress Coverage Requirement:** At least one grain-heavy 35mm scene and one dark/near-black gradient scene.
3. **Dual Metric Requirement:** Both Mean VMAF and Minimum Scene Floor must be met simultaneously.
4. **No Automated Promotions:** All thresholds remain draft decision frameworks; no automatic profile score alterations are permitted.
