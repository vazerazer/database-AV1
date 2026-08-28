# Hallowed x265 Quality-Baseline Calibration Report (Op 943A)
**Date:** 2026-08-28
**Scope:** Quantitative Source-to-Baseline and Incremental Loss Study across Hallowed 2160p x265 and AV1
**Corpus Design:** Three parity-verified UHD remux-reference pairs and one parity-verified higher-bitrate MainFrame x265 reference pair (The Bourne Supremacy).
**Sample Size:** 4 Titles $\times$ 16 Calibrated Scenes (12 Core + 4 Optional Stress Scenes)
**Comparison Directions Measured:**
1. UHD Remux / Higher-Bitrate Reference $\rightarrow$ Hallowed 2160p x265 (Baseline Similarity)
2. Hallowed 2160p x265 $\rightarrow$ AV1 Candidate (Incremental Loss)
3. Higher-Bitrate Reference $\rightarrow$ AV1 Candidate (Direct End-to-End Comparison)

> [!IMPORTANT]
> **Governance & Non-Operational Notice:** This is an evidence-only empirical study. It does not modify active tiers, profile scores, Custom Formats, release restrictions, download policies, or `evidence/verdicts.csv`. All evaluation criteria are descriptive.

---

## 1. Scope, Purpose & Acceptance Premise

* **Purpose:** Establish whether the existing trusted 2160p Hallowed x265 fallback demonstrates strong similarity relative to credible same-master UHD reference material (three parity-verified UHD remux-reference pairs and one parity-verified higher-bitrate MainFrame x265 reference pair), and measure how much additional quality loss AV1 candidates introduce relative to that accepted baseline.
* **The User-Defined Acceptance Standard:**
  * Hallowed 2160p x265 is the accepted practical quality baseline for this library.
  * AV1 candidates are evaluated not against an arbitrary universal VMAF threshold, but by whether they are *materially worse* than the Hallowed baseline in the user's high-risk content conditions:
    * Near-black shadows and smooth dark gradients
    * 35mm film grain, smoke, fog, dust, and textured details
    * High-motion action, particles, and rapid camera movements
    * Fine surface texture, clothing weave, and architecture
    * Contrast/gamma retention and color pipeline fidelity.

---

## 2. Pre-Registered Manifest Summary & Source Parity Audit

| Title (Year) | Edition | UHD Reference Master | Hallowed Baseline | AV1 Candidate | Resolution | Frame Rate | Alignment Offset | Pre-Reg Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Jurassic World** (2015) | Theatrical | 1:1 UHD Remux (64.86 GB, 69.5 Mbps) | Hallowed PROPER x265 (17.59 GB, 18.85 Mbps) | — | $3840 \times 1920^*$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` (100% Parity) |
| **The Bourne Supremacy** (2004) | Theatrical | MainFrame 2160p x265 (23.18 GB, 28.5 Mbps) | Hallowed 2160p x265 (15.34 GB, 18.85 Mbps) | RandH 2160p AV1 (7.34 GB, 9.02 Mbps) | $3840 \times 1632$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` (100% Parity) |
| **Jurassic Park III** (2001) | Theatrical | 1:1 UHD Remux (61.61 GB, 89.1 Mbps) | Hallowed PROPER x265 (13.03 GB, 18.83 Mbps) | — | $3840 \times 2076^*$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` (100% Parity) |
| **The Drama** (2026) | Theatrical | 1:1 UHD Remux (72.35 GB, 91.45 Mbps) | Hallowed 2160p x265 (15.13 GB, 19.13 Mbps) | — | $3840 \times 2076^*$ | 23.976 fps | $+0\text{ ms}$ | `ELIGIBLE` (100% Parity) |

*\*Note: 1:1 Remux sources matching full 16:9 disc canvas were normalized to active image dimensions via exact crop filters, verified by $+0\text{ ms}$ baseline PSNR-Y probes.*

---

## 3. Sample-Accounting & Alignment Audit

* **Accepted Scenes:** 16 total scenes across 4 titles (12 Core + 4 Optional Stress Scenes).
* **Rejected Scenes:** 0 technical rejections.
* **Insufficient-Parity Entries:** 0. All 4 titles confirmed same-master parity with peak alignment at $+0\text{ ms}$ ($>40.9\text{ dB}$ PSNR-Y baseline).

---

## 4. Empirical Per-Scene Measurement Results

*Measured via Netflix 4K VMAF model (`vmaf_4k_v0.6.1.json`) on native `yuv420p10le` HDR10 PQ.*

| Title | Scene Label | Timestamp | Category | Ref $\rightarrow$ Hallowed VMAF | Hallowed $\rightarrow$ AV1 VMAF | Ref $\rightarrow$ AV1 VMAF | Baseline PSNR-Y ($dB$) | Baseline SSIM |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Jurassic World** | Scene 1 (Near-Black) | `00:36:10` | Indominus Night Paddock Flashlight | **92.48** | — | — | 40.84 dB | 0.9880 |
| **Jurassic World** | Scene 2 (High-Motion) | `01:21:40` | Raptor Motorcycle Forest Chase | **95.50** | — | — | 45.83 dB | 0.9883 |
| **Jurassic World** | Scene 3 (Fine Texture)| `00:15:30` | Main Street Visitor Architecture | **95.27** | — | — | 44.03 dB | 0.9937 |
| **Jurassic World** | Scene 4 (Stress Opt) | `01:47:20` | T-Rex Final Battle Rain & Flare | **90.62** | — | — | 43.78 dB | 0.9818 |
| **Bourne Supremacy** | Scene 1 (Near-Black) | `00:07:30` | Goa Beach Night Invasion | **95.46** | **91.59** | **92.78** | 50.71 dB | 0.9978 |
| **Bourne Supremacy** | Scene 2 (High-Motion) | `01:31:00` | Moscow Tunnel Shaky Cam Chase | **99.47** | **97.79** | **98.26** | 50.14 dB | 0.9980 |
| **Bourne Supremacy** | Scene 3 (Fine Texture)| `00:27:10` | Munich Safehouse 35mm Grain | **96.96** | **94.09** | **94.88** | 50.57 dB | 0.9976 |
| **Bourne Supremacy** | Scene 4 (Stress Opt) | `00:58:20` | Berlin Rain & Dark Urban Mist | **97.09** | **94.39** | **95.29** | 49.61 dB | 0.9975 |
| **Jurassic Park III** | Scene 1 (Near-Black) | `00:32:40` | InGen Lab Night Shadow Detail | **95.56** | — | — | 45.27 dB | 0.9897 |
| **Jurassic Park III** | Scene 2 (High-Motion) | `00:19:10` | Spinosaurus Plane Attack | **96.32** | — | — | 47.35 dB | 0.9969 |
| **Jurassic Park III** | Scene 3 (Fine Texture)| `00:14:20` | Isla Sorna Canopy 35mm Foliage | **95.64** | — | — | 45.77 dB | 0.9979 |
| **Jurassic Park III** | Scene 4 (Stress Opt) | `00:54:30` | Aviary Volumetric Fog & Mist | **93.05** | — | — | 43.13 dB | 0.9909 |
| **The Drama** | Scene 1 (Near-Black) | `00:41:10` | Low-Light Interior Shadow Gradation| **93.30** | — | — | 44.92 dB | 0.9947 |
| **The Drama** | Scene 2 (High-Motion) | `00:23:40` | Rapid Urban Transit Tracking | **94.14** | — | — | 45.81 dB | 0.9977 |
| **The Drama** | Scene 3 (Fine Texture)| `00:11:50` | 8K Sensor Digital Wardrobe Texture | **96.55** | — | — | 45.50 dB | 0.9922 |
| **The Drama** | Scene 4 (Stress Opt) | `01:18:20` | Evening Rain & Streetlight Halo | **93.88** | — | — | 46.62 dB | 0.9970 |

---

## 5. Hallowed Baseline Summary: How Good is Hallowed x265?

### Title-Level Summary for Reference $\rightarrow$ Hallowed x265:

| Title | Master Bitrate | Hallowed Bitrate | BPP | Mean VMAF (Core) | Median VMAF (Core) | Min Scene Floor | Mean PSNR-Y | Mean SSIM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| *Jurassic World* (2015) | 69.52 Mbps | 18.85 Mbps | 0.1066 | **94.42** | **95.27** | **90.62** | 43.57 dB | 0.9900 |
| *The Bourne Supremacy* (2004) | 28.48 Mbps | 18.85 Mbps | 0.1254 | **97.30** | **96.96** | **95.46** | 50.47 dB | 0.9978 |
| *Jurassic Park III* (2001) | 89.06 Mbps | 18.83 Mbps | 0.0985 | **95.84** | **95.64** | **93.05** | 46.13 dB | 0.9948 |
| *The Drama* (2026) | 91.45 Mbps | 19.13 Mbps | 0.1001 | **94.66** | **94.14** | **93.30** | 45.41 dB | 0.9949 |

### Overall Hallowed Baseline Aggregate ($n=4$ Titles, 16 Scenes):
* **Arithmetic Mean VMAF (Core):** **`95.56`**
* **Median VMAF (Core):** **`95.51`**
* **Global Minimum Scene Floor:** **`90.62`** (on *Jurassic World* Scene 4 rain/flare stress; 15 of 16 scenes are $\ge 92.4$)
* **Mean PSNR-Y:** **`46.39 dB`**
* **Mean SSIM:** **`0.9944`**

> [!NOTE]
> **Executive Baseline Finding:**
> Within this four-title, 16-scene, parity-verified objective-metric corpus, Hallowed 2160p x265 showed strong similarity to the selected higher-quality references (mean 95.56 VMAF; observed minimum 90.62). This supports its use as the user's practical quality baseline, but does not establish universal reference transparency or replace display-side subjective review.

---

## 6. AV1 Incremental-Loss & Three-Way Comparison (*The Bourne Supremacy*)

*Direct measurement of the complete three-way chain (Higher-bitrate MainFrame x265 reference → Hallowed x265 → RandH AV1) across 4 scenes:*

| Scene Label | Content Type | Ref $\rightarrow$ Hallowed VMAF | Hallowed $\rightarrow$ RandH AV1 VMAF | Ref $\rightarrow$ RandH AV1 VMAF | AV1 Incremental Loss ($\Delta$ vs Hallowed) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Scene 1 (Core) | Near-Black Shadow Detail | 95.46 | 91.59 | 92.78 | **$-3.87$ VMAF** |
| Scene 2 (Core) | High-Motion Shaky Cam | 99.47 | 97.79 | 98.26 | **$-1.68$ VMAF** |
| Scene 3 (Core) | 35mm Film Grain & Texture | 96.96 | 94.09 | 94.88 | **$-2.87$ VMAF** |
| Scene 4 (Opt) | Berlin Rain & Dark Urban Mist | 97.09 | 94.39 | 95.29 | **$-2.70$ VMAF** |
| **Core Summary** | **Mean Metrics** | **`97.30`** | **`94.49`** | **`95.31`** | **`-2.81 VMAF`** |

> [!IMPORTANT]
> **AV1 Scope Limitation:**
> The AV1 incremental-loss finding applies only to the measured RandH / The Bourne Supremacy pair. It is not a cross-group AV1 baseline and does not revise RandH's existing review classification, which remains driven by the valid John Wick (2014) core-texture result (83.52 VMAF minimum).

---

## 7. Worst-Scene Register Across All Baseline & Candidate Comparisons

| Title | Direction | Group / Entity | Timestamp | Category | Measured VMAF | Risk Interpretation |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| *Jurassic World* | Ref $\rightarrow$ Hallowed | Hallowed | `01:47:20` | Rain / Smoke / Flare Gradient Stress | **90.62** | Extreme combined stress (heavy rain, flare haze, dark asphalt) experiences mild high-frequency DCT smoothing. |
| *The Bourne Supremacy* | Hallowed $\rightarrow$ AV1 | RandH | `00:07:30` | Near-Black Low-Light Shadows | **91.59** | Slight micro-texture smoothing in low-light shadows at 9.02 Mbps, but retains 91.59 VMAF without blocking. |
| *Jurassic Park III* | Ref $\rightarrow$ Hallowed | Hallowed | `00:54:30` | Volumetric Aviary Fog & Mist | **93.05** | Dense fog particles experience slight compression; smooth gradient ramp preserved. |
| *The Drama* | Ref $\rightarrow$ Hallowed | Hallowed | `00:41:10` | Low-Light Shadow Gradations | **93.30** | Minor quantization in deepest room shadows. |

---

## 8. Limitations & Display-Side Review Statement

1. **Display-Side Review Notice:** *No display-side subjective human review was performed in this operation. Results are objective metric evidence computed via Netflix libvmaf 4K models and require visual confirmation before any operational policy decisions.*
2. **Corpus Scope Distinction:**
   * **Hallowed baseline finding:** Based on four titles / 16 scenes, objective metrics only.
   * **RandH incremental AV1 finding:** Based on one title / four scenes only.

---

## 9. Recommendations & Governance Statement

1. **Executive Conclusion & Scope:**
   * Within this four-title, 16-scene, parity-verified objective-metric corpus, Hallowed 2160p x265 showed strong similarity to the selected higher-quality references (mean 95.56 VMAF; observed minimum 90.62). This supports its use as the user's practical quality baseline, but does not establish universal reference transparency or replace display-side subjective review.
   * The AV1 incremental-loss finding applies only to the measured RandH / The Bourne Supremacy pair. It is not a cross-group AV1 baseline and does not revise RandH's existing review classification, which remains driven by the valid John Wick (2014) core-texture result (83.52 VMAF minimum).
2. **Recommendation:** No live policy change is recommended.
3. **Governance Confirmation:** Zero active operational policies, tier memberships, Custom Formats, profile scores, `evidence/verdicts.csv` records, or download restrictions were modified.
