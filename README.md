# 💎 Pure AV1 Master Database for Profilarr

A dedicated, comprehensive, enterprise-grade **AV1 Custom Formats & Quality Profiles** suite for **Radarr** and **Sonarr**, built to the **PCD (Profilarr Compliant Database) v2** specification.

---

## 🎯 Architecture & Methodology

This database is built on **objective tracker and scene encoding benchmarks** (following PTP/HDB/Aither quality standards and TRaSH Guides methodology), adapted 100% to the AV1 ecosystem.

Rather than conflating file size or audio tags with encoding quality, groups are categorized strictly by **encoding standards, transparency, multi-pass grain synthesis, and CRF targets**:

### 🌟 Key Highlights
* **269 Comprehensive Custom Formats:** Complete coverage of audio standards (TrueHD Atmos, DTS-HD MA, Opus 5.1/7.1, FLAC), dynamic range (Dolby Vision Profile 5/7/8, HDR10+, HDR10), streaming provenance (ATVP, AMZN, NF, DSNP, MAX, BCORE), special editions, and anti-trash filters.
* **500 Regular Expressions:** Deep regex parsing matching modern P2P, Scene, Web, and Anime naming schemes.
* **Pure AV1 Quality Profiles (7 Dedicated Profiles):** Zero legacy bloat. Every profile is purpose-built for AV1 media acquisition.
* **Rigorously Segmented Encoder Tiers:** Clean separation between reference transparent master encodes, balanced compact mini-encodes, and low-priority storage savers.

---

## 📋 The Pure AV1 Quality Profile Suite

| Profile | Category | Target Use Case & Scoring Highlights |
| :--- | :--- | :--- |
| **`Movies 2160p AV1 HQ`** | 4K Movies | Reference 4K UHD AV1 encodes with Dolby Vision / HDR10+, high video bitrates, Quality Tier 01/02 reference encoders, and TrueHD/Atmos/Opus 5.1 audio. Compact mini-encodes are neutralized/discouraged. |
| **`Movies 1080p AV1 HQ`** | 1080p Movies | High-fidelity 1080p 10-bit AV1 with Film Grain Synthesis, Quality Tier 01/02 reference encoders, Opus 5.1/Stereo, FLAC, and Criterion/Remaster scoring. |
| **`Movies 1080p AV1 Storage`** | Low Priority | Maximum space savings for SIDCA (Sh*t I Don't Care About) or low-priority requests. Actively prioritizes compact encoders (edge2020, Vyndros, PSA, GalaxyRG). |
| **`TV 2160p AV1`** | 4K TV Series | 4K UHD AV1 episodic releases with HDR10/Dolby Vision and surround sound. |
| **`TV 1080p AV1 HQ`** | 1080p TV Series | High-fidelity 1080p 10-bit AV1 episodes with multi-channel audio and Quality Tier encoders. |
| **`TV 1080p AV1 Storage`** | 1080p TV Series | Ultra-compact episodic AV1 for massive disk space savings across complete seasons. |
| **`Anime 1080p AV1`** | Anime TV & Films | 1080p 10-bit AV1 with Dual Audio (Japanese + English), Multi-Subs, FLAC/Opus audio, and top Anime fansub groups (MTBB, SCY, Judas, SubsPlease). |

---

## 🏆 Rigorous Encoder Tier Classification

### 🥇 `AV1 Quality Tier 01` — Reference Transparent Encoders (`+1000`)
High-bitrate, multi-pass AV1 encodes tuned with SVT-AV1-PSY / AOMenc and Film Grain Synthesis (FGS), matching source Blu-ray transparency:
* `DON`, `CtrlHD`, `D-Z0N3`, `EbP`, `Geek`, `HiFi`, `LoRD`, `TayTO`, `VietHD`, `ZQ`, `c0kE`, `SA89`, `SoLaR`, `TeamSyndicate`, `DeciBelle`, `FraMeSToR`, `FLUX`, `playBD`, `WiHD`, `SMURF`, `NBT`.

### 🥈 `AV1 Quality Tier 02` — High-End Scene & P2P Encoders (`+600`)
Reliable transparent encodes and top web rippers:
* `t3nshi`, `Kitsune`, `Afm72`, `ZR-`, `samsepi0l`, `BHDStudio`, `hallowed`, `MainFrame`, `W4NK3R`, `REBORN`.

### 🥉 `AV1 Compact Tier 01` — Curated Grain-Tuned Mini Encoders (`+800` in Storage / `0` in HQ)
High-efficiency mini-encodes with good visual retention for storage-conscious setups:
* `edge2020`, `Vyndros`, `Ralphy`, `ToNaTo`, `YELLO`, `bluegreeen`, `Chivaman`, `R1GY3B`, `noxxus`, `KONTRAST`, `PHOCiS`, `YAWNiX`, `iVy`.

### 📦 `AV1 Compact Tier 02` — Balanced Storage Encoders (`+600` in Storage / `-200` in HQ)
Balanced micro-encodes prioritizing small file size:
* `dAV1nci`, `WhiskeyJack`, `UH`, `UnAV1Chain`, `R and H`, `QxR`, `TAoE`, `NAN0`, `DarQ`, `HONE`, `Honeyvera`, `LSt`, `MNHD`, `SARTRE`, `Vialle`, `dkore`, `GRiMM`, `TimeDistortion`.

### 🗑️ `AV1 Storage Savers / Trash` (`+400` in Storage / `-1000` in HQ)
Ultra-compressed web rips for maximum compression:
* `MeGusta`, `GalaxyRG`, `PSA`, `VXT`, `d3g`, `Ghost`, `rartv`, `BONE`, `ELiTE`, `LAMA`, `KaKa`, `YAWNTIC`, `GZ`, `CART`.

---

## 🚀 Adding to Profilarr

1. In your **Profilarr Web UI**, go to **Settings** > **Databases**.
2. Add or sync **Pure AV1 Database**:
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
3. Under **Instances** > **radarr4k** or **sonarr4k**, select the desired AV1 profiles and click **Sync**.
