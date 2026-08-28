# AV1 Library Group Inventory and Expanded Baseline Campaign Report (Op 944A)
**Date:** 2026-08-28
**Scope:** Comprehensive 2160p AV1 Release Group Inventory & Empirical Baseline Calibration across 5 Groups and 6 Titles (24 Scenes)
**Framework Notice:** The artifact filenames reflect the broader campaign framework; the included results are Hallowed→AV1-only comparisons due to reference availability.
**Artifacts Generated:**
- Inventory: [`av1_library_inventory_944a.json`](av1_library_inventory_944a.json)
- Manifest: [`av1_expanded_three_way_manifest_944a.json`](av1_expanded_three_way_manifest_944a.json)
- Raw Metrics: [`av1_expanded_three_way_campaign_raw_944a.json`](av1_expanded_three_way_campaign_raw_944a.json)
- Runner Script: [`../scripts/run_av1_expanded_three_way_campaign_944a.py`](../scripts/run_av1_expanded_three_way_campaign_944a.py)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is an evidence-only discovery and measurement campaign. It does not modify active tiers, profile scores, Custom Formats, release restrictions, download policies, or `evidence/verdicts.csv`. All evaluations and classifications are descriptive observations.

---

## 1. Objective, Scope & Governance Guardrails

* **Purpose:**
  1. Inventory every unique 2160p AV1 release group represented in the available library and calibration media corpus.
  2. Measure incremental quality loss for candidate, review, and unmeasured AV1 groups against the accepted Hallowed 2160p x265 practical baseline across difficult content conditions (near-black shadows, 35mm grain, high motion, textures, smoke/fog).
* **Acceptance Premise:**
  * Hallowed 2160p x265 serves as the user's practical quality baseline (Op 943A: mean 95.56 VMAF, floor 90.62).
  * AV1 encodes are assessed for incremental quality loss relative to Hallowed in high-risk content conditions. Generic numeric VMAF thresholds are not treated as universal quality gates.
* **Explicit Campaign Scope Limitation:**
  * **All six included Op 944A measurements are Hallowed→AV1-only comparisons. No higher-quality reference was available for these selected pairs, so Op 944A does not add new three-way baseline evidence or establish direct reference→AV1 performance.**

---

## 2. Complete 2160p AV1 Release Group Inventory

| Group Name | 2160p Titles Discovered | Titles in Ledger | Ledger Confidence State | Committed Ledger Evidence Depth | Hallowed Counterpart | Reference Counterpart | Availability Status | Concise Technical Rationale |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **`ChopperHitler`** | 4 | 3 | `candidate` | 3 titles / 11 scenes (mean 95.77, floor 91.10) | Yes | No | `eligible-hallowed-av1-only` | Clean 4K same-master parity on *Dark Phoenix* (46.46 dB PSNR-Y baseline). |
| **`CoSMiCSuRFeR`** | 5 | 3 | `candidate` | 2 candidate / 7 scenes (mean 94.94, floor 88.85); 1 excluded | Yes | No | `insufficient-parity` | Remaining LOTR Extended titles exhibit transfer remaster color divergence (~28 dB PSNR-Y). |
| **`RandH`** | 11 | 3 | `review` | 3 titles / 11 scenes (mean 91.34, floor 83.52 on John Wick) | Yes | Yes | `eligible-hallowed-av1-only` | Verified same-master parity on *The Bourne Ultimatum* (48.05 dB PSNR-Y baseline). |
| **`Smokindevil`** | 4 | 2 | `review` | 2 titles / 6 scenes (*Fury* and *The Shawshank Redemption*) | Yes | No | `eligible-hallowed-av1-only` | Smokindevil ledger evidence remains review, based on two prior measured titles and six scenes (Fury and The Shawshank Redemption). Op 944A adds descriptive Hallowed→AV1-only observations for The Shawshank Redemption and The Sixth Sense; these do not revise the committed ledger classification. |
| **`Bi0hazard`** | 1 | 1 | `unmeasured` | 0 measured titles / 0 scenes | Yes | No | `eligible-hallowed-av1-only` | Discovered 21.63 Mbps encode on *The Bourne Ultimatum* sharing English video (38.05 dB PSNR-Y). |
| **`Waldek`** | 1 | 0 | `unmeasured` | 0 measured titles / 0 scenes (new discovery) | Yes | No | `eligible-hallowed-av1-only` | Discovered unmeasured group on *John Wick 2* (42.98 dB PSNR-Y at -41.7 ms offset). |
| **`Rob74K`** | 2 | 1 | `review` | 1 title / 3 scenes (*John Wick 1*) | Yes | No | `insufficient-parity` | *John Wick 2* exhibits custom SDR/gamma mapping relative to HDR10 baseline (26.7 dB PSNR-Y). |
| **`SHADOW`** | 1 | 1 | `unmeasured` | 0 measured titles / 0 scenes (Op 918 probe) | No | Yes | `missing-hallowed` | Netflix WebRip release; lacks a 4K Hallowed BluRay counterpart. |

---

## 3. Pre-Registered Selected-Chain Manifest Summary

| Title (Year) | Edition | Group | AV1 Candidate Identity | Hallowed Baseline Identity | Resolution | Frame Rate | Alignment Offset | Pre-Reg Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **X-Men: Dark Phoenix** (2019) | Theatrical | `ChopperHitler` | UHD BluRay AV1 (6.32 GB, 7.40 Mbps) | Hallowed x265 (16.04 GB, 18.78 Mbps) | $3840 \times 1604$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` |
| **The Bourne Ultimatum** (2007) | Theatrical | `RandH` | 2160p AV1 (7.78 GB, 9.00 Mbps) | Hallowed x265 (16.31 GB, 18.86 Mbps) | $3840 \times 1600$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` |
| **The Bourne Ultimatum** (2007) | Theatrical | `Bi0hazard` | 2160p AV1 (18.70 GB, 21.63 Mbps) | Hallowed x265 (16.31 GB, 18.86 Mbps) | $3840 \times 1600$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` |
| **The Shawshank Redemption** (1994)| Theatrical | `Smokindevil` | UHD BluRay AV1 (5.42 GB, 5.07 Mbps) | Hallowed x265 (17.93 GB, 16.77 Mbps) | $3840 \times 2076$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` |
| **The Sixth Sense** (1999) | Theatrical | `Smokindevil` | UHD BluRay AV1 (15.02 GB, 18.65 Mbps)| Hallowed x265 (15.12 GB, 18.77 Mbps) | $3840 \times 2076$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` |
| **John Wick: Chapter 2** (2017) | Theatrical | `Waldek` | UHD BluRay AV1 (16.03 GB, 17.46 Mbps)| Hallowed x265 (15.46 GB, 16.85 Mbps) | $3840 \times 1600$ | 23.976 fps | $-41.7\text{ ms}$ | `ELIGIBLE` |

---

## 4. Excluded & Insufficient-Parity Title Register

| Title | Group | Category | Exclusion Reason | Documented Technical Detail |
| :--- | :--- | :--- | :--- | :--- |
| *LOTR: The Two Towers* (2002) | `CoSMiCSuRFeR` | 4K Catalog | `insufficient-parity` | Remaster color grading transfer divergence resulting in uniform 28.2 dB PSNR-Y baseline. |
| *LOTR: The Return of the King* (2003) | `CoSMiCSuRFeR` | 4K Catalog | `insufficient-parity` | Remaster color grading transfer divergence identical to Fellowship and Two Towers (~28 dB PSNR-Y). |
| *Jurassic Park* (1993) | `Smokindevil` | 4K Catalog | `insufficient-parity` | Encode originates from 2018 25th Ann. master vs Hallowed 2023 30th Ann. master (24.8 dB PSNR-Y). |
| *The Deer Hunter* (1978) | `RandH` | 4K Catalog | `insufficient-parity` | StudioCanal UK 4K restoration vs Shout Factory US 4K restoration transfer divergence (17.9 dB PSNR-Y). |
| *John Wick: Chapter 2* (2017) | `Rob74K` | Modern 4K | `insufficient-parity` | Applies custom SDR/gamma mapping relative to standard UHD BluRay HDR10 pipeline (26.7 dB PSNR-Y). |
| *The Rip* (2026) | `SHADOW` | 4K WebRip | `missing-hallowed` | No 4K Hallowed release exists in library or distribution channels. |

---

## 5. Sample-Accounting & Per-Scene Empirical Results

*Measured via Netflix 4K VMAF model (`vmaf_4k_v0.6.1.json`) on native `yuv420p10le` HDR10 PQ.*

| Title | Group | Scene Label | Timestamp | Category | Hallowed $\rightarrow$ AV1 VMAF | Baseline PSNR-Y ($dB$) | Baseline SSIM | Status |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **X-Men: Dark Phoenix** | `ChopperHitler` | Scene 1 (Near-Black) | `00:09:40` | Space Shuttle Dark Cosmos | **96.90** | 48.36 dB | 0.9981 | ACCEPTED |
| **X-Men: Dark Phoenix** | `ChopperHitler` | Scene 2 (High-Motion) | `01:28:10` | Military Train Battle | **94.22** | 49.11 dB | 0.9978 | ACCEPTED |
| **X-Men: Dark Phoenix** | `ChopperHitler` | Scene 3 (Fine Texture)| `00:37:20` | Genosha Island Forest | **95.24** | 49.83 dB | 0.9979 | ACCEPTED |
| **X-Men: Dark Phoenix** | `ChopperHitler` | Scene 4 (Stress Opt) | `00:11:15` | Cosmic Flare Energy | **95.68** | 49.60 dB | 0.9980 | ACCEPTED |
| **The Bourne Ultimatum** | `RandH` | Scene 1 (Near-Black) | `00:06:20` | Moscow Winter Night Shadows| **96.12** | 50.82 dB | 0.9974 | ACCEPTED |
| **The Bourne Ultimatum** | `RandH` | Scene 2 (High-Motion) | `00:54:10` | Tangier Rooftop Sprint | **98.60** | 48.36 dB | 0.9966 | ACCEPTED |
| **The Bourne Ultimatum** | `RandH` | Scene 3 (35mm Grain) | `00:23:40` | Waterloo Station Crowd | **96.45** | 46.60 dB | 0.9948 | ACCEPTED |
| **The Bourne Ultimatum** | `RandH` | Scene 4 (Stress Opt) | `01:31:30` | New York Tunnel Impact | **97.40** | 49.74 dB | 0.9969 | ACCEPTED |
| **The Bourne Ultimatum** | `Bi0hazard` | Scene 1 (Near-Black) | `00:06:20` | Moscow Winter Night Shadows| **97.06** | 51.61 dB | 0.9984 | ACCEPTED |
| **The Bourne Ultimatum** | `Bi0hazard` | Scene 2 (High-Motion) | `00:54:10` | Tangier Rooftop Sprint | **99.72** | 50.37 dB | 0.9985 | ACCEPTED |
| **The Bourne Ultimatum** | `Bi0hazard` | Scene 3 (35mm Grain) | `00:23:40` | Waterloo Station Crowd | **98.87** | 49.08 dB | 0.9980 | ACCEPTED |
| **The Bourne Ultimatum** | `Bi0hazard` | Scene 4 (Stress Opt) | `01:31:30` | New York Tunnel Impact | **98.47** | 51.15 dB | 0.9982 | ACCEPTED |
| **The Shawshank Redemption**| `Smokindevil` | Scene 1 (Near-Black) | `00:19:10` | Cellblock Night Darkness | **94.18** | 48.53 dB | 0.9978 | ACCEPTED |
| **The Shawshank Redemption**| `Smokindevil` | Scene 2 (High-Motion) | `01:42:30` | Sewage Rainstorm Escape | **90.25** | 47.50 dB | 0.9978 | ACCEPTED |
| **The Shawshank Redemption**| `Smokindevil` | Scene 3 (35mm Grain) | `00:46:10` | Prison Yard Brick Dust | **92.05** | 46.48 dB | 0.9982 | ACCEPTED |
| **The Shawshank Redemption**| `Smokindevil` | Scene 4 (Stress Opt) | `01:44:00` | River Lightning Strike | **89.85** | 47.60 dB | 0.9980 | ACCEPTED |
| **The Sixth Sense** | `Smokindevil` | Scene 1 (Near-Black) | `00:09:10` | Dark Basement Lightbulb | **83.92** | 42.80 dB | 0.9936 | ACCEPTED |
| **The Sixth Sense** | `Smokindevil` | Scene 2 (High-Motion) | `00:58:40` | Panicked Street Traffic | **85.52** | 42.47 dB | 0.9947 | ACCEPTED |
| **The Sixth Sense** | `Smokindevil` | Scene 3 (Fine Texture)| `00:26:30` | Church Sanctuary Interior | **89.31** | 41.28 dB | 0.9960 | ACCEPTED |
| **The Sixth Sense** | `Smokindevil` | Scene 4 (Stress Opt) | `00:41:20` | Tent Breath Vapor Fog | **86.85** | 42.89 dB | 0.9944 | ACCEPTED |
| **John Wick: Chapter 2** | `Waldek` | Scene 1 (Near-Black) | `00:04:10` | Warehouse Night Shadows | **69.24** | 38.32 dB | 0.9623 | ACCEPTED |
| **John Wick: Chapter 2** | `Waldek` | Scene 2 (High-Motion) | `00:57:30` | Catacombs Gunfight | **79.58** | 40.79 dB | 0.9836 | ACCEPTED |
| **John Wick: Chapter 2** | `Waldek` | Scene 3 (Fine Texture)| `00:36:20` | Tailor Shop Suit Weave | **63.31** | 32.76 dB | 0.9364 | ACCEPTED |
| **John Wick: Chapter 2** | `Waldek` | Scene 4 (Stress Opt) | `01:44:10` | Neon Hall of Mirrors | **72.68** | 36.14 dB | 0.9669 | ACCEPTED |

---

## 6. Per-Title & Per-Group Descriptive Summary

### Title-Level Summary:

| Title (Year) | Group | Hallowed Bitrate | AV1 Bitrate | BPP | Mean Core VMAF | Median Core VMAF | Min Scene Floor | Mean PSNR-Y | Mean SSIM |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| *X-Men: Dark Phoenix* (2019) | `ChopperHitler` | 18.78 Mbps | 7.40 Mbps | 0.0501 | **95.45** | **95.24** | **94.22** | 49.10 dB | 0.9979 |
| *The Bourne Ultimatum* (2007) | `RandH` | 18.86 Mbps | 9.00 Mbps | 0.0611 | **97.06** | **96.45** | **96.12** | 48.59 dB | 0.9963 |
| *The Bourne Ultimatum* (2007) | `Bi0hazard` | 18.86 Mbps | 21.63 Mbps | 0.1469 | **98.55** | **98.87** | **97.06** | 50.35 dB | 0.9983 |
| *The Shawshank Redemption* (1994) | `Smokindevil` | 16.77 Mbps | 5.07 Mbps | 0.0265 | **92.16** | **92.05** | **89.85** | 47.50 dB | 0.9979 |
| *The Sixth Sense* (1999) | `Smokindevil` | 18.77 Mbps | 18.65 Mbps | 0.0976 | **86.25** | **85.52** | **83.92** | 42.18 dB | 0.9948 |
| *John Wick: Chapter 2* (2017) | `Waldek` | 16.85 Mbps | 17.46 Mbps | 0.1185 | **70.71** | **69.24** | **63.31** | 37.29 dB | 0.9608 |

### Per-Group Evidence Aggregation:

1. **`ChopperHitler` (Candidate):**
   * *New Op 944A Observation:* *X-Men: Dark Phoenix* (2019) demonstrated high measured similarity (**`95.45`** mean VMAF, **`94.22`** min floor at $7.40\text{ Mbps}$ / $0.0501\text{ BPP}$); no display-side visual review was performed.
   * *Cumulative Corpus ($n=4$ Titles, 15 Scenes):* **`Mean VMAF 95.69`** | **`Median 96.12`** | **`Min Floor 91.10`**. ChopperHitler has additional strong Hallowed-relative evidence but remains candidate until separately reviewed.
2. **`RandH` (Review):**
   * *New Op 944A Observation:* *The Bourne Ultimatum* (2007) demonstrated high measured similarity (**`97.06`** mean VMAF, **`96.12`** min floor at $9.00\text{ Mbps}$ / $0.0611\text{ BPP}$); no display-side visual review was performed.
   * *Group Status:* RandH remains review despite a strong Bourne Ultimatum Hallowed-relative result, as its committed ledger classification remains governed by the valid *John Wick (2014)* fine-texture result ($83.52\text{ VMAF}$).
3. **`Bi0hazard` (Unmeasured):**
   * *New Op 944A Observation:* *The Bourne Ultimatum* (2007) demonstrated high measured similarity (**`98.55`** mean VMAF, **`97.06`** min floor at $21.63\text{ Mbps}$ / $0.1469\text{ BPP}$); no display-side visual review was performed. Bi0hazard is a single-title Hallowed-relative observation only and requires more credible evidence before any group-level conclusion.
4. **`Smokindevil` (Review):**
   * *Committed Ledger & New Observations:* Smokindevil ledger evidence remains review, based on two prior measured titles and six scenes (Fury and The Shawshank Redemption). Op 944A adds descriptive Hallowed→AV1-only observations for The Shawshank Redemption and The Sixth Sense; these do not revise the committed ledger classification.
   * *New Op 944A Observations:* *Shawshank* ($5.07\text{ Mbps}$) maintained `92.16` mean, while *The Sixth Sense* ($18.65\text{ Mbps}$) showed lower measured similarity in dark scenes (**`86.25`** mean / **`83.92`** floor in dark basement shadows); no display-side visual review was performed. Smokindevil remains review.
5. **`Waldek` (Unmeasured):**
   * *New Op 944A Observation:* *John Wick: Chapter 2* (2017) demonstrated low measured similarity (**`70.71`** mean VMAF, dipping to **`63.31`** on fine suit textures and **`69.24`** on near-black shadows at $17.46\text{ Mbps}$). Waldek is a single-title Hallowed-relative observation only and requires more credible evidence before any group-level conclusion.
6. **`CoSMiCSuRFeR` (Candidate):**
   * *Group Status:* CoSMiCSuRFeR remains candidate with no new valid comparison (remaining LOTR titles excluded for transfer remaster color divergence).
7. **`SHADOW` (Unmeasured):**
   * *Group Status:* SHADOW remains unmeasured because no Hallowed comparator was available.

---

## 7. Worst-Scene Register Across All Campaign Comparisons

| Group | Title | Scene Label | Timestamp | Content Category | Measured VMAF | Objective Risk Interpretation | Core / Opt |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :---: |
| **`Waldek`** | *John Wick 2* | Scene 3 (Fine Texture) | `00:36:20` | Tailor Shop Suit Weave | **63.31** | Very low Hallowed→AV1 similarity in this fine-texture scene (63.31 VMAF), indicating a high risk of material spatial-detail loss; no display-side visual review was performed. | Core |
| **`Waldek`** | *John Wick 2* | Scene 1 (Near-Black) | `00:04:10` | Warehouse Night Shadows | **69.24** | Low Hallowed→AV1 similarity in this near-black scene (69.24 VMAF), indicating high risk of shadow-detail and dark-gradient degradation; no display-side visual review was performed. | Core |
| **`Waldek`** | *John Wick 2* | Scene 4 (Stress Opt) | `01:44:10` | Neon Hall of Mirrors | **72.68** | Low Hallowed→AV1 similarity in saturated neon/mirror stress content (72.68 VMAF), indicating high risk of visible degradation in specular and gradient detail; no display-side visual review was performed. | Optional |
| **`Waldek`** | *John Wick 2* | Scene 2 (High-Motion) | `00:57:30` | Catacombs Gunfight | **79.58** | Lower Hallowed→AV1 similarity in high-motion content (79.58 VMAF), indicating elevated risk of motion-detail degradation; no display-side visual review was performed. | Core |
| **`Smokindevil`**| *The Sixth Sense* | Scene 1 (Near-Black) | `00:09:10` | Dark Basement Lightbulb | **83.92** | Measured similarity indicates possible additional loss in this content category (83.92 VMAF); no display-side visual review was performed. | Core |
| **`Smokindevil`**| *The Sixth Sense* | Scene 2 (High-Motion) | `00:58:40` | Panicked Street Traffic | **85.52** | Measured similarity indicates possible additional loss in this content category (85.52 VMAF); no display-side visual review was performed. | Core |
| **`Smokindevil`**| *The Sixth Sense* | Scene 4 (Stress Opt) | `00:41:20` | Tent Breath Vapor Fog | **86.85** | Measured similarity indicates possible additional loss in this content category (86.85 VMAF); no display-side visual review was performed. | Optional |
| **`Smokindevil`**| *Shawshank* | Scene 4 (Stress Opt) | `01:44:00` | River Lightning Strike | **89.85** | Measured similarity indicates possible additional loss in this content category (89.85 VMAF); no display-side visual review was performed. | Optional |
| **`Smokindevil`**| *Shawshank* | Scene 2 (High-Motion) | `01:42:30` | Sewage Rainstorm Escape | **90.25** | Measured similarity indicates possible additional loss in this content category (90.25 VMAF); no display-side visual review was performed. | Core |
| **`Smokindevil`**| *Shawshank* | Scene 3 (35mm Grain) | `00:46:10` | Prison Yard Brick Dust | **92.05** | High measured similarity in this sampled scene (92.05 VMAF); no display-side visual review was performed. | Core |
| **`ChopperHitler`**| *Dark Phoenix*| Scene 2 (High-Motion) | `01:28:10` | Military Train Battle | **94.22** | High measured similarity in this sampled scene (94.22 VMAF); no display-side visual review was performed. | Core |
| **`ChopperHitler`**| *Dark Phoenix*| Scene 3 (Fine Texture)| `00:37:20` | Genosha Island Forest | **95.24** | High measured similarity in this sampled scene (95.24 VMAF); no display-side visual review was performed. | Core |
| **`RandH`** | *Bourne Ultimatum*| Scene 1 (Near-Black) | `00:06:20` | Moscow Winter Night Shadows| **96.12** | High measured similarity in this sampled scene (96.12 VMAF); no display-side visual review was performed. | Core |
| **`Bi0hazard`** | *Bourne Ultimatum*| Scene 1 (Near-Black) | `00:06:20` | Moscow Winter Night Shadows| **97.06** | High measured similarity in this sampled scene (97.06 VMAF); no display-side visual review was performed. | Core |

---

## 8. Limitations & Display-Side Review Notice

1. **Display-Side Subjective Review Notice:** *No display-side subjective human visual review was performed in this operation. All reported metrics are objective measurements computed via Netflix libvmaf 4K models on native HDR10 PQ streams and require visual confirmation.*
2. **Reference Master Availability:** All six included Op 944A measurements are Hallowed→AV1-only comparisons. No higher-quality reference was available for these selected pairs, so Op 944A does not add new three-way baseline evidence or establish direct reference→AV1 performance.
3. **Group Sample Size:** Discovered groups `Bi0hazard` and `Waldek` represent single-title observations and require cautious handling without broad generalization.

---

## 9. Final Recommendations & Governance Statement

1. **Final Recommendation:** **No live policy change is recommended.**
   * **`ChopperHitler`** has additional strong Hallowed-relative evidence but remains candidate until separately reviewed.
   * **`CoSMiCSuRFeR`** remains candidate with no new valid comparison.
   * **`RandH`** remains review despite a strong Bourne Ultimatum Hallowed-relative result.
   * **`Smokindevil`** remains review.
   * **`Bi0hazard`** and **`Waldek`** are single-title Hallowed-relative observations only and require more credible evidence before any group-level conclusion.
   * **`SHADOW`** remains unmeasured because no Hallowed comparator was available.
   * No `evidence/verdicts.csv` change is made.
2. **Governance Confirmation:** Zero active operational policies, tier memberships, Custom Formats, profile scores, `evidence/verdicts.csv` records, or download restrictions were modified.
