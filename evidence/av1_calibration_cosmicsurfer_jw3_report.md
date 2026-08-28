# CoSMiCSuRFeR Targeted Calibration Report: John Wick 3 (Op 940B)
**Date:** 2026-08-28
**Scope:** Second Same-Master 2160p Calibration Title for CoSMiCSuRFeR
**Title:** *John Wick: Chapter 3 - Parabellum* (2019)
**AV1 Release:** `John.Wick.Chapter.3.Parabellum.2019.2160p.UHD.BluRay.DV.HDR.TrueHD.7.1.Atmos-AV1-CoSMiCSuRFeR`
**Reference Release:** `John.Wick.Chapter.3.Parabellum.2019.REPACK.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed`

> [!IMPORTANT]
> **Governance Notice:** This is an empirical calibration measurement study. It does not alter active tier memberships, Radarr profile scores, Custom Formats, or automated download policies. All thresholds remain provisional/DRAFT.

---

## 0. Transfer & Source Parity Audit

* **Source Master:** 2160p Theatrical UHD BluRay Master (Dolby Vision / HDR10 PQ, `smpte2084`, `bt2020nc`).
* **Frame Rate & Resolution:** Both streams are native $3840 \times 1600$ at $23.976\text{ fps}$ (`24000/1001`).
* **Aspect Ratio:** $2.40:1$ letterbox-normalized.
* **Temporal Alignment:** Verified via PSNR probe; offset $+0\text{ ms}$ (frame-accurate).
* **AV1 Bitrate & Density:** $37.69\text{ Mbps}$ ($0.2558\text{ bpp}$).
* **Reference Master Bitrate:** $18.86\text{ Mbps}$ ($0.1280\text{ bpp}$).

---

## 1. Sample Accounting & Reproducibility

| Scene # | Scene Name | Description | Start Time | Duration | Status | Optional Scene |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | NYC rainstorm alleyway & Continental near-black shadows | `00:08:30` | 10s | **ACCEPTED** | No |
| **2** | High-Motion | Antique weapon museum knife fight & rapid combat | `00:15:20` | 10s | **ACCEPTED** | No |
| **3** | Texture / Fine-Detail | Casablanca desert hotel mosaic & fine fabric textures | `00:54:10` | 10s | **ACCEPTED** | No |
| **4** | Near-Black Glass Gradient | Glass house final duel neon reflections & deep shadow gradients | `01:46:30` | 10s | **ACCEPTED** | Yes (Permitted 4th) |

* **Accepted Scenes:** 4 (3 Core + 1 Optional)
* **Rejected Scenes:** 0

---

## 2. Empirical Measurement Results

*Measured via Netflix 4K VMAF model (`vmaf_4k_v0.6.1.json`) on native `yuv420p10le` HDR10 PQ.*

| Scene # | Scene Label | Timestamp | VMAF (4K) | PSNR-Y ($dB$) | SSIM | Observed VMAF/Mbps | Offset |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | `00:08:30` | **94.27** | 42.44 dB | 0.9960 | 2.50 | $+0\text{ ms}$ |
| **2** | High-Motion | `00:15:20` | **92.46** | 40.68 dB | 0.9953 | 2.45 | $+0\text{ ms}$ |
| **3** | Texture / Fine-Detail | `00:54:10` | **91.69** | 42.11 dB | 0.9957 | 2.43 | $+0\text{ ms}$ |
| **4** | Near-Black Glass Gradient (Opt) | `01:46:30` | **88.85** | 33.02 dB | 0.9899 | 2.36 | $+0\text{ ms}$ |

---

## 3. Title & Multi-Title Aggregate Summary

### Title Aggregate (*John Wick 3*):
* **Mean Core VMAF (Scenes 1–3):** **`92.81`**
* **Minimum Scene VMAF (All 4 Scenes):** **`88.85`** (Core Scene Min: `91.69`)
* **Mean PSNR-Y (Core Scenes):** **`41.74 dB`**
* **Mean SSIM (Core Scenes):** **`0.9957`**

### Multi-Title Aggregate for `CoSMiCSuRFeR` (Combined *JW4* + *JW3*):

| Title | Master | AV1 Bitrate | BPP | Mean VMAF (Core) | Min Scene VMAF | Mean PSNR-Y | Mean SSIM |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| *John Wick: Chapter 4* (2023) | 2160p UHD BluRay | 15.02 Mbps | 0.1014 | 97.06 | 96.79 | 48.43 dB | 0.9980 |
| *John Wick: Chapter 3* (2019) | 2160p UHD BluRay | 37.69 Mbps | 0.2558 | 92.81 | 88.85 | 41.74 dB | 0.9957 |
| **Combined Group Level ($n=2$)** | — | — | — | **94.94** | **88.85** | **45.09 dB** | **0.9969** |

---

## 4. Confidence Assessment & Group Verdict

* **Title Count:** 2 distinct same-master titles measured across 7 calibrated scenes.
* **Fidelity Assessment:** CoSMiCSuRFeR demonstrates strong high-fidelity encoding across both modern action titles. On *JW3*, shadow detail and knife combat remain very high ($\text{VMAF } 92.5 - 94.3$), while the optional neon glass house stress scene dips to $88.85$.
* **Confidence State:** Transitioned from `single-title` $\rightarrow$ **`candidate`**.
* **Tier Governance:** Remains in active Quality Tier 1 without score or profile changes.
