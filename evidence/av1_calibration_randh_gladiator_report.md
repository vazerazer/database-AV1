# RandH Targeted Calibration Report: Gladiator (Op 941A)
**Date:** 2026-08-28
**Scope:** Second Same-Master 2160p Calibration Title for RandH
**Title:** *Gladiator* (2000) [Extended Cut]
**AV1 Release:** `Gladiator.2000.Extended.Cut.2160p.BluRay.DV.HDR10.Encode.AV1.DTS.5.1-RandH`
**Reference Release:** `Gladiator.2000.Extended.Cut.REPACK.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed`

> [!IMPORTANT]
> **Governance Notice:** This is an empirical calibration measurement study. It does not alter active tier memberships, Radarr profile scores, Custom Formats, or automated download policies. All thresholds remain provisional/DRAFT.

---

## 0. Transfer & Source Parity Audit

* **Source Master:** 2160p Extended Cut UHD BluRay Master (Dolby Vision / HDR10 PQ, `smpte2084`, `bt2020nc`).
* **Frame Rate & Resolution:** Both streams are native $3840 \times 1600$ at $23.976\text{ fps}$ (`24000/1001`).
* **Duration:** Matched within 0.02s ($10,256.94\text{s}$ vs $10,256.96\text{s}$ / 170.9 minutes).
* **Aspect Ratio:** $2.40:1$ letterbox-normalized.
* **Temporal Alignment:** Verified via PSNR probe; offset $+0\text{ ms}$ (frame-accurate).
* **AV1 Bitrate & Density:** $9.95\text{ Mbps}$ ($0.0675\text{ bpp}$).
* **Reference Master Bitrate:** $18.86\text{ Mbps}$ ($0.1280\text{ bpp}$).

---

## 1. Sample Accounting & Reproducibility

| Scene # | Scene Name | Description | Start Time | Duration | Status | Optional Scene |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | Imperial tent candlelight & low-light shadows | `00:26:00` | 10s | **ACCEPTED** | No |
| **2** | High-Motion | Germania forest battle flaming arrows, cavalry charge & sword clash | `00:10:30` | 10s | **ACCEPTED** | No |
| **3** | Texture / Fine-Detail | Zucchabar desert market rough stone architecture & linen grain | `00:46:00` | 10s | **ACCEPTED** | No |
| **4** | Colosseum Chariot Battle (Dust Stress) | Battle of Carthage arena dust cloud, heavy 35mm grain & rapid chariot motion | `01:25:00` | 10s | **ACCEPTED** | Yes (Permitted 4th) |

* **Accepted Scenes:** 4 (3 Core + 1 Permitted Optional)
* **Rejected Scenes:** 0

---

## 2. Empirical Measurement Results

*Measured via Netflix 4K VMAF model (`vmaf_4k_v0.6.1.json`) on native `yuv420p10le` HDR10 PQ.*

| Scene # | Scene Label | Timestamp | VMAF (4K) | PSNR-Y ($dB$) | SSIM | Observed VMAF/Mbps | Offset |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | `00:26:00` | **90.02** | 45.42 dB | 0.9956 | 9.05 | $+0\text{ ms}$ |
| **2** | High-Motion | `00:10:30` | **92.42** | 44.85 dB | 0.9933 | 9.29 | $+0\text{ ms}$ |
| **3** | Texture / Fine-Detail | `00:46:00` | **91.31** | 42.25 dB | 0.9947 | 9.18 | $+0\text{ ms}$ |
| **4** | Colosseum Chariot Battle (Opt) | `01:25:00` | **97.60** | 46.10 dB | 0.9967 | 9.81 | $+0\text{ ms}$ |

---

## 3. Title & Multi-Title Aggregate Summary

### Title Aggregate (*Gladiator* Extended Cut):
* **Mean Core VMAF (Scenes 1–3):** **`91.25`**
* **Minimum Scene VMAF (All 4 Scenes):** **`90.02`** (Core Scene Min: `90.02`)
* **Mean PSNR-Y (Core Scenes):** **`44.17 dB`**
* **Mean SSIM (Core Scenes):** **`0.9945`**

### Multi-Title Aggregate for `RandH` (Combined *Interstellar* + *Gladiator*):

| Title | Master | AV1 Bitrate | BPP | Mean VMAF (Core) | Min Scene VMAF | Mean PSNR-Y | Mean SSIM |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| *Interstellar* (2014) | 2160p IMAX UHD BluRay | 14.05 Mbps | 0.0707 | 95.61 | 93.21 | 47.27 dB | 0.9968 |
| *Gladiator* (2000) | 2160p Extended UHD BluRay | 9.95 Mbps | 0.0675 | 91.25 | 90.02 | 44.17 dB | 0.9945 |
| **Combined Group Level ($n=2$)** | — | — | — | **93.43** | **90.02** | **45.72 dB** | **0.9957** |

---

## 4. Confidence Assessment & Group Verdict

* **Title Count:** 2 distinct same-master titles measured across 7 calibrated scenes.
* **Fidelity Assessment:** RandH demonstrates solid, highly consistent encoding efficiency across both modern digital/IMAX and complex 35mm catalog material. On *Gladiator*, high-motion battle sequences and sand dust clouds score between $92.4 - 97.6$, while low-light imperial tent candlelight holds a steady minimum of $90.02$.
* **Confidence State:** Transitioned from `single-title` $\rightarrow$ **`candidate`**.
* **Tier Governance:** Preserved in existing operational configuration without score or profile modifications.
