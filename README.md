# 💎 Pure AV1 Master Database for Profilarr

A dedicated, comprehensive, enterprise-grade **AV1 Custom Formats & Quality Profiles** suite for **Radarr** and **Sonarr**, built to the **PCD (Profilarr Compliant Database) v2** specification.

---

## 🎯 Architecture & Philosophy

This database is built for users who want a **100% Pure AV1** media automation pipeline. It completely replaces legacy x264/x265 profiles while retaining the full depth, audio refinement, and hygiene standards of **Dictionarry** and **Dumpstarr**.

### 🌟 Key Highlights
* **267 Comprehensive Custom Formats:** Complete coverage of modern audio standards (TrueHD Atmos, DTS-HD MA, Opus 5.1/7.1, FLAC), HDR standards (Dolby Vision Profile 5/7/8, HDR10+, HDR10), streaming service provenance (ATVP, AMZN, NF, DSNP, MAX, BCORE), special editions, and anti-trash filters.
* **498 Regular Expressions:** Deep regex parsing matching modern P2P, Scene, Web, and Anime naming schemes.
* **Pure AV1 Quality Profiles (7 Dedicated Profiles):** Zero legacy bloat. Every profile is purpose-built for AV1 media acquisition.
* **Granular AV1 Encoder Tiers:** Distinct separation between master transparent encodes (CRF 18–22 with Film Grain Synthesis), quality series/anime releases, and compact storage savers.
* **Intelligent Audio & HDR Handshake:** Transparently rewards immersive lossless/Opus surround sound and enforces Dolby Vision fallback safety.

---

## 📋 The Pure AV1 Quality Profile Suite

| Profile | Category | Target Use Case & Scoring Highlights |
| :--- | :--- | :--- |
| **`Movies 2160p AV1 HQ`** | 4K Movies | Premium 4K UHD AV1 encodes with Dolby Vision / HDR10+, transparent video bitrates, Tier 01 encoders, and TrueHD/Atmos/Opus 5.1 audio. |
| **`Movies 1080p AV1 HQ`** | 1080p Movies | High-fidelity 1080p 10-bit AV1 with Film Grain Synthesis, Tier 01 encoders, Opus 5.1/Stereo, FLAC, and Criterion/Remaster scoring. |
| **`Movies 1080p AV1 Storage`** | Low Priority | Maximum space savings for SIDCA (Sh*t I Don't Care About) or low-priority requests. Favors efficient encoders (PSA, GalaxyRG, MeGusta). |
| **`TV 2160p AV1`** | 4K TV Series | 4K UHD AV1 episodic releases with HDR10/Dolby Vision and surround sound. |
| **`TV 1080p AV1 HQ`** | 1080p TV Series | High-fidelity 1080p 10-bit AV1 episodes with multi-channel audio. |
| **`TV 1080p AV1 Storage`** | 1080p TV Series | Ultra-compact episodic AV1 for massive disk space savings across complete seasons. |
| **`Anime 1080p AV1`** | Anime TV & Films | 1080p 10-bit AV1 with Dual Audio (Japanese + English), Multi-Subs, FLAC/Opus audio, and top Anime fansub groups. |

---

## 🏆 AV1 Release Group Tiers

### 🥇 Tier 01 — Master & Transparent Encoders (`+1000`)
High-bitrate, multi-pass AV1 encodes tuned with SVT-AV1-PSY / AOMenc and Film Grain Synthesis (FGS):
* `t3nshi`, `EDGE2020`, `ZR-`, `D-Z0N3`, `Kitsune`, `Afm72`, `Vyndros`, `samsepi0l`, `FLUX`, `CtrlHD`, `DON`, `Geek`, `DeciBelle`, `NBT`, `WiHD`, `playBD`, `TayTO`, `SMURF`, `HiFi`.

### 🥈 Tier 02 — Quality Series & Anime Encoders (`+500` to `+1000`)
Consistent high-quality TV episodic and Anime fansub releases:
* `AkihitoSubs`, `Judas`, `Erai-raws`, `SubsPlease`, `NanDesuKa`, `ASW`, `Kawa`, `VARYG`, `LostYears`, `Tenrai-Sensei`, `Kaleido`, `CTR`, `SCY`.

### 🥉 Tier 03 — Balanced & Storage Savers (`+200` to `+800`)
Efficient micro-encodes designed for maximum compression while maintaining acceptable visual clarity:
* `MeGusta`, `GalaxyRG`, `PSA`, `VXT`, `d3g`, `Ghost`, `rartv`, `BONE`, `ELiTE`, `LAMA`, `KaKa`, `YAWNTIC`, `GZ`, `CART`.

---

## 🔊 Audio & Dynamic Range Scoring Matrix

| Feature | Custom Format | Score Delta | Function |
| :--- | :--- | :--- | :--- |
| **Codec** | `AV1 Codec` | **`+2000`** | Guarantees AV1 always beats legacy x265/x264 |
| **Bit Depth** | `10-bit Depth` | **`+300`** | Prevents color banding and grain artifacting |
| **Grain** | `Film Grain Synthesis` | **`+200`** | Rewards AV1 native grain synthesis |
| **HDR** | `Dolby Vision` | **`+600`** | Dynamic HDR enhancement |
| **HDR** | `HDR10+` | **`+500`** | Dynamic metadata enhancement |
| **HDR** | `HDR` | **`+400`** | Base HDR10 enhancement |
| **Audio** | `Atmos` | **`+350`** | Object-based spatial audio |
| **Audio** | `TrueHD` / `DTS-HD MA` | **`+300`** | Lossless master audio passthrough |
| **Audio** | `Opus 5.1 / 7.1` | **`+250`** | High-efficiency transparent surround sound |
| **Audio** | `FLAC` | **`+250`** | Lossless audio (Anime & Music) |
| **Audio** | `Opus Stereo` | **`+200`** | Clean high-efficiency 2.0 audio |
| **Safety** | `DV (No HDR Fallback)` | **`-10000`** | Blocks unplayable DV Profile 5 on SDR displays |
| **Hygiene** | `Banned Groups` | **`-10000`** | Auto-rejects spam/watermarked re-encodes |
| **Hygiene** | `Upscale` / `Upscaled` | **`-10000`** | Blocks low-effort AI fake upscales |
| **Hygiene** | `BR-DISK Structure` | **`-10000`** | Blocks raw ISO/BDMV unparsed disc dumps |

---

## 🚀 Adding to Profilarr

1. In your **Profilarr Web UI**, go to **Settings** > **Databases**.
2. Click **Add Database**:
   * **Name:** `Pure AV1 Master Database`
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
   * **Sync Interval:** `60`
3. Under **Instances** > **radarr4k** or **sonarr4k**, select the desired AV1 profiles and click **Sync**.
