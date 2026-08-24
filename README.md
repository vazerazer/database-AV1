# 💎 Pure AV1 Master Database for Profilarr

A dedicated, comprehensive, enterprise-grade **AV1 Custom Formats & Quality Profiles** suite for **Radarr** and **Sonarr**, built to the **PCD (Profilarr Compliant Database) v2** specification (Schema `1.1.0`).

---

## 🎯 Architecture & Core Philosophy

This database is designed exclusively for **authentic, active AV1 video encoders** and **uncompromising codec isolation**. Legacy x264/x265 release groups have been purged from the active tiers, and strict codec penalties prevent x265/x264 releases from ever outscoring an AV1 release.

### 🌟 Key Highlights
* **Absolute Codec Enforcement:** Genuine `AV1` receives **`+2000`**, while `Legacy x265 Codec` receives **`-3500`** (on 2160p) / **`-2000`** (on 1080p) and `Legacy x264 Codec` receives **`-5000`**. Minimum score cutoffs are set to `1000` on 2160p profiles and `500` on 1080p profiles, mathematically preventing max-stacked x265 releases from leaking.
* **Verified Active AV1 Encoders:** Every group in the AV1 tiers is a verified, active encoder with verifiable public releases on public/private trackers.
* **Universal Hygiene:** CAM, Telesync, Screener, Upscale, 3D, Extras, Sing Along, Full Disc, Dolby Vision (Without Fallback), Banned Groups, and Banned Remux are strictly penalized at **`-10000`** across all 7 profiles.
* **7 Dedicated Pure AV1 Quality Profiles:** Purpose-built for 4K Movies, 1080p Movies, TV Series, Storage Savers, and Anime.

---

## ⚙️ Engine & Regex Compatibility Specification

> [!IMPORTANT]
> **.NET Regex Compatibility Requirement:**
> All regular expressions in this PCD repository must strictly adhere to the **.NET Regular Expression specification** (`System.Text.RegularExpressions`), matching the runtime behavior of Radarr/Sonarr (`RegexSpecificationBase.cs:17` — compiled case-insensitive) and the Profilarr compiler engine. Patterns utilize anchored release group positions (`-(GROUP)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$` for standard releases and `^\[GROUP\]` for anime releases) to prevent substring false-positives.

---

## 📋 The Pure AV1 Quality Profile Suite

| Profile | Category | Min Cutoff | Upgrade Until | Target Use Case & Scoring Highlights |
| :--- | :--- | :--- | :--- | :--- |
| **`Movies 2160p AV1 HQ`** | 4K Movies | `1000` | `3500` | Reference 4K UHD AV1 encodes with Dolby Vision / HDR10+, 10-bit depth, Atmos, TrueHD, DTS-X, Opus 5.1/7.1, and verified AV1 Compact Encoders. Storage savers penalized at `-1000`. |
| **`Movies 1080p AV1 HQ`** | 1080p Movies | `500` | `2500` | High-fidelity 1080p 10-bit AV1 with Opus/lossless surround audio, Criterion/Remaster scoring. |
| **`Movies 1080p AV1 Storage`** | Low Priority | `200` | `1500` | Maximum space savings for SIDCA or low-priority requests. Prioritizes storage savers (`PSA`, `GalaxyRG`, `MeGusta`). |
| **`TV 2160p AV1`** | 4K TV Series | `1000` | `3500` | 4K UHD AV1 episodic releases with HDR10/Dolby Vision and surround sound. |
| **`TV 1080p AV1 HQ`** | 1080p TV Series | `500` | `2500` | High-fidelity 1080p 10-bit AV1 episodes with multi-channel audio. |
| **`TV 1080p AV1 Storage`** | 1080p TV Series | `200` | `1500` | Ultra-compact episodic AV1 for massive disk space savings across complete seasons. |
| **`Anime 1080p AV1`** | Anime TV & Films | `500` | `3000` | 1080p 10-bit AV1 with Dual Audio (+500), Multi-Subs, FLAC/Opus audio, and verified AV1 Anime encoders (`Trix`, `Breeze`, `INDEX`, `Sav1or`, `AV1ARY`, `Sokudo`, `RigAV1`). |

---

## 🏆 Verified Active AV1 Encoder Tiers

### 🎌 `AV1 Anime Encoders` (`+1000` in Anime Profile)
Verified active encoders releasing 10-bit AV1 anime with multi-subs and dual audio (anchored prefix `^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1)\]`):
* `Trix`, `Breeze`, `INDEX`, `Sav1or`, `AV1ARY`, `Sokudo`, `RigAV1`.

### 🥈 `AV1 Compact Encoders` (`+500` in HQ / `+500` in Storage)
Curated transparent mini-encodes balancing compression with grain retention (anchored `-(dAV1nci|WhiskeyJack|UH|edge2020|Vyndros|UnAV1Chain|R and H)`):
* `dAV1nci`, `WhiskeyJack`, `UH`, `edge2020`, `Vyndros`, `UnAV1Chain`, `R and H`.

### 📦 `AV1 Storage Savers` (`-1000` in HQ / `+600` in Storage)
Ultra-compressed micro-encodes for maximum disk space savings:
* `PSA`, `GalaxyRG`, `MeGusta`.

---

## 🚀 Adding to Profilarr

1. In your **Profilarr Web UI**, go to **Settings** > **Databases**.
2. Add or sync **Pure AV1 Database**:
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
3. Under **Instances** > **radarr4k** or **sonarr4k**, select the desired AV1 profiles and click **Sync**.
