# 💎 Pure AV1 Master Database for Profilarr

A dedicated, comprehensive, enterprise-grade **AV1 Custom Formats & Quality Profiles** suite for **Radarr** and **Sonarr**, built to the **PCD (Profilarr Compliant Database) v2** specification.

---

## 🎯 Architecture & Core Philosophy

This database is designed exclusively for **authentic, active AV1 video encoders** and **uncompromising codec isolation**. Legacy x264/x265 release groups (who do not encode in AV1) have been purged from the active tier lists, and strict codec penalties prevent x265/x264 releases from ever outscoring an AV1 release.

### 🌟 Key Highlights
* **Absolute Codec Enforcement:** Genuine `AV1 Codec` receives **`+5000`**, while `Legacy x265` receives **`-5000`** and `Legacy x264` receives **`-10000`**. A non-AV1 release can never accidentally win.
* **Verified Active AV1 Encoders:** Every group in the AV1 tiers is a verified, active participant in the AV1 encoding ecosystem.
* **270 Comprehensive Custom Formats & 501 Regular Expressions:** Full support for modern audio standards (TrueHD Atmos, DTS-HD MA, Opus 5.1/7.1, FLAC), dynamic range (Dolby Vision Profile 5/7/8, HDR10+, HDR10), streaming provenance (ATVP, AMZN, NF, DSNP, MAX, BCORE), special editions, and anti-trash filters.
* **7 Dedicated Pure AV1 Quality Profiles:** Purpose-built for 4K Movies, 1080p Movies, TV Series, Storage Savers, and Anime.

---

## 📋 The Pure AV1 Quality Profile Suite

| Profile | Category | Target Use Case & Scoring Highlights |
| :--- | :--- | :--- |
| **`Movies 2160p AV1 HQ`** | 4K Movies | Reference 4K UHD AV1 encodes with Dolby Vision / HDR10+, high video bitrates, Quality AV1 encoders (`CoSMiCSuRFeR`, `t3nshi`, `samsepi0l`, `ZR-`, `FLUX`), and TrueHD/Atmos/Opus 5.1 audio. Compact mini-encodes are neutralized. |
| **`Movies 1080p AV1 HQ`** | 1080p Movies | High-fidelity 1080p 10-bit AV1 with Film Grain Synthesis, Quality AV1 encoders, Opus 5.1/Stereo, FLAC, and Criterion/Remaster scoring. |
| **`Movies 1080p AV1 Storage`** | Low Priority | Maximum space savings for SIDCA or low-priority requests. Actively prioritizes compact AV1 encoders (`dAV1nci`, `WhiskeyJack`, `edge2020`, `PSA`, `GalaxyRG`). |
| **`TV 2160p AV1`** | 4K TV Series | 4K UHD AV1 episodic releases with HDR10/Dolby Vision and surround sound. |
| **`TV 1080p AV1 HQ`** | 1080p TV Series | High-fidelity 1080p 10-bit AV1 episodes with multi-channel audio and Quality AV1 encoders. |
| **`TV 1080p AV1 Storage`** | 1080p TV Series | Ultra-compact episodic AV1 for massive disk space savings across complete seasons. |
| **`Anime 1080p AV1`** | Anime TV & Films | 1080p 10-bit AV1 with Dual Audio (Japanese + English), Multi-Subs, FLAC/Opus audio, and verified AV1 Anime encoders (`Judas`, `AkihitoSubs`, `SubsPlease`, `Erai-raws`, `NanDesuKa`, `VARYG`). |

---

## 🏆 Verified Active AV1 Encoder Tiers

### 🥇 `AV1 Quality Encoders` (`+1000` in HQ / `+300` in Storage)
Encoders producing high-bitrate, multi-pass AV1 transparent encodes with film grain synthesis and lossless/surround audio:
* `CoSMiCSuRFeR`, `t3nshi`, `samsepi0l`, `ZR-`, `Kitsune`, `Afm72`, `FLUX`, `DeciBelle`, `Samurai`, `SAMPA`.

### 🎌 `AV1 Anime Encoders` (`+1000` in Anime Profile)
Verified active encoders and fansub groups releasing 10-bit AV1 anime with multi-subs and dual audio:
* `Judas`, `AkihitoSubs`, `SubsPlease`, `Erai-raws`, `NanDesuKa`, `VARYG`, `Tenrai-Sensei`, `CTR`, `Kawa`, `LostYears`, `Kaleido`, `SCY`.

### 🥈 `AV1 Compact Encoders` (`0` in HQ / `+800` in Storage)
Curated mini-encodes balancing high compression efficiency with tuned grain retention:
* `dAV1nci`, `WhiskeyJack`, `UH`, `edge2020`, `Vyndros`, `UnAV1Chain`, `R and H`.

### 📦 `AV1 Storage Savers` (`-1000` in HQ / `+600` in Storage)
Ultra-compressed micro-encodes for maximum disk space savings:
* `PSA`, `GalaxyRG`, `MeGusta`, `VXT`, `d3g`, `Ghost`, `rartv`, `ELiTE`, `LAMA`, `KaKa`, `YAWNTIC`, `BONE`, `GZ`, `CART`.

---

## 🚀 Adding to Profilarr

1. In your **Profilarr Web UI**, go to **Settings** > **Databases**.
2. Add or sync **Pure AV1 Database**:
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
3. Under **Instances** > **radarr4k** or **sonarr4k**, select the desired AV1 profiles and click **Sync**.
