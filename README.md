# AV1 Master Database for Profilarr

A comprehensive, curated collection of **AV1 Custom Formats & Quality Profiles** for **Radarr** and **Sonarr**, built to the **PCD (Profilarr Compliant Database) v2** specification.

---

## 🎯 What This Database Does

This database bridges the gap between next-generation **AV1 video compression** and the automated media management in the Arr stack. It brings the full sophistication of **TRaSH Guides** and **Dumpstarr** (tier scoring, audio ranking, HDR/DV handling, and anti-trash filters) specifically adapted and weighted for AV1 media.

### Key Highlights:
* **AV1 Codec Prioritization:** Heavily scores genuine AV1 encodes (`AV1`, `AV01`, `SVT-AV1`, `libsvtav1`) over legacy x265 and x264.
* **10-bit Depth Filtering:** Ensures 10-bit color precision is prioritized to eliminate compression color-banding and grain distortion.
* **AV1 Release Group Tiers:** Granular ranking of reputable transparent encoders, series encoders, and storage savers.
* **HDR10+ & Dolby Vision Handshake:** Seamlessly grabs 4K Dolby Vision & HDR10+ AV1 releases with safe fallback validation.
* **Modern Audio Standards:** Native support and scoring for multi-channel **Opus 5.1/7.1**, **E-AC-3 (Dolby Digital Plus with Atmos)**, **FLAC**, and passthrough **TrueHD / DTS-HD MA**.
* **Hygiene & Anti-Trash:** Blocks fake AV1 re-tags, bad AI upscales, CAM/Telesync sources, and known spammers.

---

## 📋 Included Quality Profiles

| Profile | Application | Focus & Optimization |
| :--- | :--- | :--- |
| **`Movies 2160p AV1 HQ`** | Radarr (4K Movies) | Premium 4K AV1 with HDR10/Dolby Vision, high video bitrates, and transparent audio / Opus 5.1. |
| **`Movies 1080p AV1 HQ`** | Radarr (1080p Movies) | High-fidelity 1080p 10-bit AV1 with top-tier transparent encodes and pristine audio. |
| **`TV 2160p AV1`** | Sonarr (4K TV Shows) | 4K UHD AV1 episodic releases with HDR and multi-channel audio. |
| **`TV 1080p AV1`** | Sonarr (1080p TV Shows) | High-efficiency 1080p 10-bit AV1 episodic releases (drastically reduced storage with zero perceptible loss). |
| **`Anime 1080p AV1`** | Sonarr / Radarr (Anime) | 10-bit AV1 anime releases with Dual Audio (Japanese + English) prioritization. |

---

## 🏆 AV1 Release Group Tiers

* **Tier 01 (Transparent / Master Encoders):** `t3nshi`, `EDGE2020`, `ZR-`, `D-Z0N3`, `Kitsune`, `Afm72`, `Vyndros`, `samsepi0l`, `FLUX`, `CtrlHD`, `Geek`, `DeciBelle`.
* **Tier 02 (Quality Series & Anime Encoders):** `AkihitoSubs`, `Judas`, `Erai-raws`, `SubsPlease`, `NanDesuKa`, `ASW`, `Kawa`, `VARYG`, `LostYears`, `Tenrai-Sensei`.
* **Tier 03 (Balanced / Storage Savers):** `MeGusta`, `GalaxyRG`, `PSA`, `VXT`, `d3g`, `Ghost`, `rartv`, `BONE`, `ELiTE`, `LAMA`.

---

## 🚀 Installation into Profilarr

1. Open your **Profilarr Web UI**.
2. Navigate to **Settings** > **Databases**.
3. Click **Add Database**.
4. Enter the repository URL: `https://github.com/<your-username>/av1-profilarr-database`
5. Branch: `main` | Sync Interval: `60` min.
6. Under **Instances**, select your Radarr/Sonarr instance and assign the desired AV1 profiles.
