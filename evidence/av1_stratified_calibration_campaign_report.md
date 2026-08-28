# AV1 Multi-Group Stratified Calibration Campaign Report (Op 942)
**Date:** 2026-08-28
**Scope:** Multi-Group Stratified Calibration across CoSMiCSuRFeR, RandH, and ChopperHitler
**Target Depth:** 3 Credible Same-Master Measured Titles per Target Group
**Corpus Expansion:** 3 New Candidate Pairs $\times$ 12 Calibrated Scenes (9 Core + 3 Optional Stress Scenes)

> [!IMPORTANT]
> **Governance Notice:** This is an empirical calibration and evidence-expansion study. It does not alter active tier memberships, Radarr profile scores, Custom Formats, release restrictions, or automated download policies. All thresholds remain provisional/DRAFT.

---

## 1. Scope, Objective & Guardrails

* **Objective:** Expand the empirical same-master evidence corpus for `CoSMiCSuRFeR`, `RandH`, and `ChopperHitler` to assess multi-title performance consistency across varied content strata (near-black shadow detail, high-motion action, 35mm grain/dust, modern digital control, and complex stress conditions).
* **Absolute Guardrails Enforced:**
  1. Evidence-only: Zero modifications to active tiers, profiles, Custom Formats, or scoring.
  2. Metric integrity: VMAF/Mbps and BPP are descriptive metrics only, never automated promotion gates.
  3. Parity rigor: Any title exhibiting source transfer or color grading divergence is classified as `insufficient-parity` and excluded from group promotion aggregates.
  4. No promotion: `high-confidence` is not assigned; draft thresholds remain unenforced.

---

## 2. Pre-Registered Corpus Manifest & Source Parity Audit

| Group | Title (Year) | Cut / Master | AV1 Bitrate | Ref Bitrate | Resolution | Frame Rate | Alignment Offset | Pre-Registration Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CoSMiCSuRFeR** | *LOTR: Fellowship of the Ring* (2001) | Extended Cut UHD BluRay | 19.39 Mbps | 19.13 Mbps | $3840 \times 1608$ | 23.976 fps | $+0\text{ ms}$ | `INSUFFICIENT_PARITY` (Color Transfer Divergence) |
| **RandH** | *John Wick* (2014) | Theatrical UHD BluRay | 8.66 Mbps | 16.80 Mbps | $3840 \times 1600^*$ | 23.976 fps | $+0\text{ ms}$ | `ACCEPTED` (100% Transfer Parity) |
| **ChopperHitler** | *X-Men: Apocalypse* (2016) | Theatrical UHD BluRay | 11.63 Mbps | 18.83 Mbps | $3840 \times 1600$ | 23.976 fps | $+0\text{ ms}$ | `ACCEPTED` (100% Transfer Parity) |

*\*Note: RandH John Wick encodes full 16:9 canvas with letterbox black bars, normalized to $3840 \times 1600$ via crop filter `crop=3840:1600:0:280` yielding exact 46.14 dB baseline PSNR-Y.*

---

## 3. Sample Accounting & Reproducibility Tables

### Title 1: *The Lord of the Rings: The Fellowship of the Ring* (2001) — CoSMiCSuRFeR
*Master: 2160p Extended Cut UHD BluRay | Parity Note: Uniform 26–28 dB PSNR-Y indicates transfer/color grading divergence.*

| Scene # | Scene Name | Category | Timestamp | Duration | Status | Optional Scene |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | Near-Black Shadow Detail | `01:47:30` | 10s | **ACCEPTED (INSUFFICIENT PARITY)** | No |
| **2** | High-Motion | High Motion Action | `01:54:10` | 10s | **ACCEPTED (INSUFFICIENT PARITY)** | No |
| **3** | Texture / Fine-Detail | Texture & 35mm Grain | `00:18:20` | 10s | **ACCEPTED (INSUFFICIENT PARITY)** | No |
| **4** | Nazgûl Water & Fog Stress | High-Risk Water / Fog Stress | `01:05:40` | 10s | **ACCEPTED (INSUFFICIENT PARITY)** | Yes |

* Accepted Scenes: 4 | Rejected Scenes: 0 | Parity Outcome: `insufficient-parity`

---

### Title 2: *John Wick* (2014) — RandH
*Master: 2160p Theatrical UHD BluRay | Parity: Validated (+0ms, 46.14 dB initial alignment).*

| Scene # | Scene Name | Category | Timestamp | Duration | Status | Optional Scene |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | Near-Black Shadow Detail | `00:14:30` | 10s | **ACCEPTED** | No |
| **2** | High-Motion | High Motion Action | `00:52:40` | 10s | **ACCEPTED** | No |
| **3** | Texture / Fine-Detail | Clean Modern Digital & Texture | `00:36:20` | 10s | **ACCEPTED** | No |
| **4** | Red Circle Neon Gradient & Haze | High-Risk Neon Gradient / Smoke | `00:54:30` | 10s | **ACCEPTED** | Yes |

* Accepted Scenes: 4 (3 Core + 1 Optional) | Rejected Scenes: 0 | Parity Outcome: `PASS`

---

### Title 3: *X-Men: Apocalypse* (2016) — ChopperHitler
*Master: 2160p Theatrical UHD BluRay | Parity: Validated (+0ms, 48.33 dB initial alignment).*

| Scene # | Scene Name | Category | Timestamp | Duration | Status | Optional Scene |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | Near-Black / Shadow-Detail | Near-Black Shadow Detail | `00:19:10` | 10s | **ACCEPTED** | No |
| **2** | High-Motion | Extreme Motion & Particles | `01:14:40` | 10s | **ACCEPTED** | No |
| **3** | Texture / Fine-Detail | Modern Digital 6K Fine Detail | `00:31:00` | 10s | **ACCEPTED** | No |
| **4** | Psychic Realm Particle & Glow | High-Risk CGI Particle / Glow | `02:04:10` | 10s | **ACCEPTED** | Yes |

* Accepted Scenes: 4 (3 Core + 1 Optional) | Rejected Scenes: 0 | Parity Outcome: `PASS`

---

## 4. Empirical Per-Scene Measurement Results

*Measured via Netflix 4K VMAF model (`vmaf_4k_v0.6.1.json`) on native `yuv420p10le` HDR10 PQ.*

| Group | Title | Scene Label | Timestamp | VMAF (4K) | PSNR-Y ($dB$) | SSIM | Descriptive Review Band |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **CoSMiCSuRFeR** | *LOTR: Fellowship* | Near-Black / Shadow | `01:47:30` | 79.23 | 26.57 dB | 0.8697 | *Insufficient Parity (Color Grading Divergence)* |
| **CoSMiCSuRFeR** | *LOTR: Fellowship* | High-Motion Balrog | `01:54:10` | 78.72 | 28.69 dB | 0.9513 | *Insufficient Parity (Color Grading Divergence)* |
| **CoSMiCSuRFeR** | *LOTR: Fellowship* | Texture Shire Party | `00:18:20` | 76.71 | 28.59 dB | 0.9462 | *Insufficient Parity (Color Grading Divergence)* |
| **CoSMiCSuRFeR** | *LOTR: Fellowship* | Nazgûl Water/Fog (Opt) | `01:05:40` | 81.31 | 27.12 dB | 0.8723 | *Insufficient Parity (Color Grading Divergence)* |
| **RandH** | *John Wick (2014)* | Near-Black Break-In | `00:14:30` | **86.63** | 40.01 dB | 0.9927 | VMAF < 90.0 (Lean Bitrate Shadow Compression) |
| **RandH** | *John Wick (2014)* | High-Motion Gun-Fu | `00:52:40` | **91.33** | 37.62 dB | 0.9947 | VMAF 90.0 – 93.0 (Solid Action Fidelity) |
| **RandH** | *John Wick (2014)* | Texture Gold Coins | `00:36:20` | **83.52** | 37.19 dB | 0.9918 | VMAF < 90.0 (Ultra-Lean Micro-Texture Smearing) |
| **RandH** | *John Wick (2014)* | Red Circle Neon (Opt) | `00:54:30` | **85.35** | 37.99 dB | 0.9911 | VMAF < 90.0 (Haze / Neon Gradient Banding) |
| **ChopperHitler** | *X-Men: Apocalypse* | Near-Black Cairo Vault | `00:19:10` | **96.93** | 47.56 dB | 0.9986 | VMAF $\ge 93.0$ (Pristine Shadow Detail) |
| **ChopperHitler** | *X-Men: Apocalypse* | High-Motion Quicksilver| `01:14:40` | **98.75** | 53.75 dB | 0.9989 | VMAF $\ge 93.0$ (Flawless Particle Velocity) |
| **ChopperHitler** | *X-Men: Apocalypse* | Texture Xavier Lawn | `00:31:00` | **94.48** | 46.44 dB | 0.9969 | VMAF $\ge 93.0$ (High Foliage Texture Retention) |
| **ChopperHitler** | *X-Men: Apocalypse* | Psychic Particle (Opt) | `02:04:10` | **98.75** | 49.65 dB | 0.9984 | VMAF $\ge 93.0$ (Pristine CGI Energy Glows) |

---

## 5. Title-Level Aggregate Metrics (Op 942 Additions)

| Title | Group | AV1 Bitrate | BPP | Mean VMAF (Core) | Median VMAF (Core) | Min Scene VMAF | Mean PSNR-Y | Mean SSIM | Parity Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| *LOTR: Fellowship of the Ring* | CoSMiCSuRFeR | 19.39 Mbps | 0.1310 | 78.22 | 78.72 | 76.71 | 27.95 dB | 0.9224 | `insufficient-parity` |
| *John Wick* (2014) | RandH | 8.66 Mbps | 0.0588 | **87.16** | **86.63** | **83.52** | **38.27 dB** | **0.9931** | `PASS` |
| *X-Men: Apocalypse* (2016) | ChopperHitler | 11.63 Mbps | 0.0789 | **96.72** | **96.93** | **94.48** | **49.25 dB** | **0.9981** | `PASS` |

---

## 6. Comprehensive Group Summary & Corpus Register

### Target Group Summary Across All Credible Measured Titles ($n \ge 1$):

| Group | Credible Titles | Total Scenes | Core / Opt | Mean VMAF (Core) | Median VMAF | Min Scene Floor | Mean PSNR-Y | Mean SSIM | Review Bands (<90 / 90-93 / $\ge 93$) | Confidence State |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ChopperHitler** | **3** | 11 | 9 / 2 | **95.77** | **96.93** | **91.10** | **48.66 dB** | **0.9975** | 0 / 1 / 10 | **`candidate`** |
| **RandH** | **3** | 11 | 9 / 2 | **91.34** | **91.33** | **83.52** | **42.72 dB** | **0.9948** | 3 / 4 / 4 | **`review`** |
| **CoSMiCSuRFeR** | **2** | 7 | 6 / 1 | **94.94** | **94.27** | **88.85** | **45.09 dB** | **0.9969** | 1 / 2 / 4 | **`candidate`** |

*Note on CoSMiCSuRFeR:* Fellowship of the Ring is excluded from credible title counts due to transfer color divergence, preserving the verified $n=2$ baseline (*JW4* + *JW3*).

---

## 7. Worst-Scene Register

The lowest measured scenes observed across the complete active calibration corpus:

| Group | Title | Timestamp | Scene Category | Scene VMAF | Observed Artifact & Risk Interpretation |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **ChopperHitler** | *X-Men* (2000) | `00:37:10` | 35mm Heavy Film Grain (Train Station) | **91.10** | Mild high-frequency grain suppression; no blocking or temporal smearing. |
| **CoSMiCSuRFeR** | *John Wick 3* (2019) | `01:46:30` | Near-Black Glass House Neon Gradient | **88.85** | Slight neon gradient compression in dark glass reflection stress test. |
| **RandH** | *John Wick* (2014) | `00:36:20` | Clean Modern Digital Fine Texture | **83.52** | Ultra-lean bitrate ($8.66\text{ Mbps}$, $0.0588\text{ bpp}$) leads to slight spatial smoothing of fine fabric weave. |
| **Smokindevil** | *Fury* (2014) | `00:46:40` | Dark Low-Light 35mm Grain Collapse | **66.77** | Severe grain collapse & macroblocking under dark 35mm tank battle (Review control). |
| **Rob74K** | *John Wick 2* (2017) | `00:15:30` | Spatial Grain De-noising & Gamma Drift | **68.61** | Persistent temporal denoising and gamma offset across scenes (Review control). |

---

## 8. Limitations & Visual Review Statement

1. **Objective Metrics Only:** All reported metrics (VMAF, PSNR-Y, SSIM) were computed programmatically via Netflix 4K libvmaf models without subjective display-side human double-blind panel viewing.
2. **Transfer Parity Constraints:** *LOTR: Fellowship of the Ring* demonstrates that even matching 4K BluRay tags can exhibit color transfer / remaster differences. Rigorous PSNR alignment audits remain mandatory.
3. **Sample Diversity:** While 3 titles per group provide significantly improved depth, ongoing monitoring across additional boutique labels and difficult animation / black-and-white masters is recommended.

---

## 9. Confidence Conclusions & Governance Statement

1. **`ChopperHitler`:** Achieves 3 credible titles ($n=3$, 11 scenes) with exceptional mean fidelity (`95.77`) and a solid minimum floor of `91.10`. Confirmed as **`candidate`**.
2. **`RandH`:** Has three credible titles ($n=3$, 11 scenes) but is classified **`review`** rather than candidate: the John Wick (2014) required fine-texture core scene reached 83.52 VMAF at 8.66 Mbps / 0.0588 BPP with material spatial smoothing.
3. **`CoSMiCSuRFeR`:** Retains 2 verified credible titles ($n=2$, 7 scenes, `94.94` mean) due to *LOTR* transfer divergence. Confirmed as **`candidate`**.
4. **Governance Confirmation:** Zero active operational policies, tier memberships, Custom Formats, profile scores, or download restrictions were modified.
