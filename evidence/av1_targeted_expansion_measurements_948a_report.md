# Targeted Expansion Measurements Report (Op 948A)
**Date:** 2026-08-28
**Scope:** Execution of Targeted Same-Master & Hallowed-Relative Measurements for Transition Groups (`RandH`, `Smokindevil`, `Bi0hazard`, `Waldek`)
**Artifacts Generated:**
- Measurement Script: [`../scripts/run_av1_targeted_expansion_measurements_948a.py`](../scripts/run_av1_targeted_expansion_measurements_948a.py)
- Raw Measurement Metrics: [`av1_targeted_expansion_measurements_948a_raw.json`](av1_targeted_expansion_measurements_948a_raw.json)
- Updated Ledger: [`verdicts.csv`](verdicts.csv)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is an evidence-only measurement and documentation package. Zero modifications were made to active profiles, tiers, scores, Custom Formats, Radarr/Profilarr configuration, release restrictions, download rules, media files, or live automation. All thresholds remain non-enforcing DRAFT.

---

## 1. Executive Summary & Measurement Scope

Op 948A executes the targeted measurement campaign pre-registered in Op 947A, focusing on groups whose behavior shifts in Op 946A policy simulations:
1. **`RandH` (`review`):**
   * **Measured (Same-Master Reference):** *The Bourne Supremacy* (2004) [RandH AV1 8.63 Mbps vs MainFrame x265 28.17 Mbps UHD Reference] $\rightarrow$ **`95.31` Mean VMAF** | **`93.85` Min VMAF** | **`48.95 dB` PSNR-Y** | **`0.9972` SSIM**.
   * **Measured (Hallowed-Relative):** *Blade Runner: The Final Cut* (1982) [RandH AV1 8.23 Mbps vs Hallowed x265 18.30 Mbps] $\rightarrow$ **`83.96` Mean VMAF** | **`74.55` Min VMAF** | **`39.62 dB` PSNR-Y** | **`0.9817` SSIM**.
2. **`Smokindevil` (`review`), `Bi0hazard` (`unmeasured`), `Waldek` (`unmeasured`):**
   * Hallowed-relative observations were already committed in Ops 944A/945A. 1:1 UHD Remux master acquisitions remain pending to elevate these titles into full same-master reference calibrations.

---

## 2. Detailed Per-Title Measurement Results

### 1. *The Bourne Supremacy* (2004) [RandH] — `same-master-reference`
* **File Identity:** `The.Bourne.Supremacy.2004-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H.mkv` (6.83 GB, 8.63 Mbps, 0.0586 BPP)
* **Reference Master:** `The.Bourne.Supremacy.2004.2160p.BluRay.DTS-X.7.1.DV.HDR10.x265-MainFrame.mkv` (22.28 GB, 28.17 Mbps)
* **Parity Status:** Same-master 2160p UHD transfer, matching 3840x1600 canvas and 23.976 fps. Exact temporal sync (0.0s offset).

| Scene | Timestamp / Description | VMAF Mean | VMAF Min | PSNR-Y ($dB$) | SSIM | Content Stress Mode |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Scene 1** | 00:04:15 — Goa Beach Night Hut | 95.12 | 93.85 | 48.82 | 0.9968 | Low-light shadows & Super 35 grain |
| **Scene 2** | 00:15:30 — Naples Interrogation Room | 95.84 | 94.62 | 49.34 | 0.9976 | Fine facial texture & indoor lighting |
| **Scene 3** | 00:42:00 — Munich Foot Chase | 94.95 | 94.10 | 48.65 | 0.9970 | Extreme handheld camera motion |
| **Scene 4** | 01:38:20 — Moscow Tunnel Car Crash | 95.33 | 94.25 | 48.99 | 0.9974 | Rapid action & smoke particles |
| **Overall** | **4 Standardized Scenes (10s each)** | **`95.31`** | **`93.85`** | **`48.95`** | **`0.9972`** | **PASS** |

---

### 2. *Blade Runner: The Final Cut* (1982) [RandH] — `hallowed-relative`
* **File Identity:** `Blade.Runner.1982.The.Final.Cut.BluRay.2160p.DTS.5.1.DV.HDR.AV1-RandH.mkv` (7.11 GB, 8.23 Mbps, 0.0558 BPP)
* **Reference Master:** `Blade.Runner.1982.The.Final.Cut.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv` (13.82 GB, 18.30 Mbps)
* **Parity Status:** Matching 3840x1600 canvas and 23.976 fps. Exact temporal sync (0.0s offset).

| Scene | Timestamp / Description | VMAF Mean | VMAF Min | PSNR-Y ($dB$) | SSIM | Content Stress Mode |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Scene 1** | 00:04:30 — Opening Eye / Interrogation | 81.16 | 75.98 | 37.06 | 0.9786 | Heavy near-black smoke & grain |
| **Scene 2** | 00:06:15 — Voight-Kampff Iris & Face | 81.07 | 74.55 | 37.74 | 0.9794 | Dense 35mm optical grain & skin |
| **Scene 3** | 00:13:45 — Spinner City Flight | 87.14 | 82.04 | 39.20 | 0.9793 | High-motion rainy neon cityscape |
| **Scene 4** | 01:47:30 — Tears in Rain / Dove Release | 86.47 | 77.93 | 44.47 | 0.9896 | Volumetric mist & neon speculars |
| **Overall** | **4 Standardized Scenes (10s each)** | **`83.96`** | **`74.55`** | **`39.62`** | **`0.9817`** | **PASS (Review Risk Floor)** |

---

## 3. Excluded & Deferred Titles Summary

* ***Jack Reacher* (2012) [RandH]:** Hallowed x265 counterpart is not currently present in local library storage; deferred until local media is accessible.
* ***The Sixth Sense* (1999) [Smokindevil]:** 1:1 UHD Remux master acquisition pending. Existing Hallowed-relative observation remains recorded in `verdicts.csv` (86.25 mean / 83.92 floor).
* ***The Bourne Ultimatum* (2007) [Bi0hazard]:** 1:1 UHD Remux master acquisition pending. Existing Hallowed-relative observation remains recorded in `verdicts.csv` (98.55 mean / 97.06 floor).
* ***John Wick: Chapter 2* (2017) [Waldek]:** 1:1 UHD Remux master acquisition pending. Existing Hallowed-relative observation remains recorded in `verdicts.csv` (70.71 mean / 63.31 floor).
* **`Rob74K` (All Titles):** Local library inventory exhausted; all available 2160p local releases (*JW1*, *JW2*) already evaluated in `verdicts.csv`.

---

## 4. Newly Appended Ledger Rows in `evidence/verdicts.csv`

```csv
2026-08-28,The Bourne Supremacy,2004,RandH,AV1,2160p,6.83,108,8.63,Compact Tier,prod,PASS,95.31,93.85,48.95,0.9972,0.0586,MainFrame 2160p x265 HDR10/DV,4,,review,same-master-reference,2026-08-28,evidence/av1_targeted_expansion_measurements_948a_report.md,Same-master 2160p UHD BluRay calibration against MainFrame x265 reference (from Op 943A); solid Super 35 grain & handheld motion fidelity; title_count pending ledger review.
2026-08-28,Blade Runner,1982,RandH,AV1,2160p,7.11,117,8.23,Compact Tier,prod,PASS,83.96,74.55,39.62,0.9817,0.0558,hallowed 2160p x265 HDR/DV,4,,review,hallowed-relative,2026-08-28,evidence/av1_targeted_expansion_measurements_948a_report.md,Hallowed→AV1-only comparison; heavy 35mm optical grain & neon smoke stress; VMAF min 74.55 floor in dense smoke/face; descriptive relative evidence only; excluded from same-master title_count.
```

---

## 5. Governance & Non-Operational Declaration

* **Non-Operational Guardrail Confirmation:** Zero active operational configurations, Custom Formats, profile scores, tier assignments, release restrictions, download rules, media files, or running containers were modified.
* **Confidence State Preservation:** `RandH` remains `review`, `Smokindevil` remains `review`, `Bi0hazard` remains `unmeasured`, `Waldek` remains `unmeasured`. Zero `high-confidence` states exist.
