# 💎 Pure AV1 Master Database for Profilarr

[![PCD Audit & Simulation Battery](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml)

A dedicated, comprehensive, enterprise-grade **AV1 Custom Formats & Quality Profiles** suite for **Radarr** and **Sonarr**, built to the **PCD (Profilarr Compliant Database) v2** specification (Schema `1.1.0`).

---

## 🎯 Architecture & Core Philosophy

This database is designed exclusively for **authentic, active AV1 video encoders** with an intelligent, multi-tiered **x265 fallback ladder**. It prioritizes high-fidelity AV1 releases, provides curated fallbacks when AV1 is unavailable, and prevents unwanted releases or service-churn from degrading your library.

### 🌟 Key Highlights
* **Elevated Canonical AV1 Codec:** Genuine `AV1` receives **`+3500`**, strictly outscoring any non-AV1 release regardless of accumulated audio/video feature points.
* **`Not AV1` Codec Gate:** Custom format `Not AV1` (`-2000`) acts as the gatekeeper, penalizing non-AV1 releases to create a strict, non-overlapping fallback band ($1000 - 3400$).
* **Curated x265 Fallback Ladder:** When no AV1 release exists, curated high-tier x265 releases (e.g. `hallowed` BluRay at +1650, `FLUX` WEB-DL at +1050) pass the minimum score cutoff (`1000` for 2160p, `500` for 1080p) while remaining well below `upgrade_until_score` (`6000`), enabling instant fallback grabbing and automatic future upgrading to AV1.
* **Anti-Churn Protection:** `upgrade_score_increment = 300` across all 7 profiles eliminates cosmetic service swaps (e.g. HMAX $\rightarrow$ AMZN $+50$) while ensuring major quality tier jumps and AV1 upgrades fire cleanly.
* **Universal Hygiene:** CAM, Telesync, Screener, Upscale, 3D, Extras, Sing Along, Full Disc, Dolby Vision (Without Fallback), Banned Groups, and Banned Remux are strictly penalized at **`-10000`** across all 7 profiles.

---

## 📋 The Pure AV1 Quality Profile Suite

| Profile | Category | Min Cutoff | Upgrade Until | Increment | Target Use Case & Scoring Highlights |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`Movies 2160p AV1 HQ`** | 4K Movies | `1000` | `6000` | `300` | Reference 4K UHD AV1 encodes with Dolby Vision / HDR10+, 10-bit depth, Atmos, TrueHD, DTS-X, Opus 5.1/7.1, Quality Encoders (+1000), and Compact Encoders (+500). Storage savers penalized at `-1000`. |
| **`Movies 1080p AV1 HQ`** | 1080p Movies | `500` | `5000` | `300` | High-fidelity 1080p 10-bit AV1 with Opus/lossless surround audio, Criterion/Remaster scoring. |
| **`Movies 1080p AV1 Storage`** | Low Priority | `200` | `3500` | `300` | Maximum space savings for SIDCA or low-priority requests. Prioritizes storage savers (`PSA`, `GalaxyRG`, `MeGusta`) at `+600`, penalizes 40GB quality encodes at `-1000`. |
| **`TV 2160p AV1`** | 4K TV Series | `1000` | `6000` | `300` | 4K UHD AV1 episodic releases with HDR10/Dolby Vision and surround sound. |
| **`TV 1080p AV1 HQ`** | 1080p TV Series | `500` | `5000` | `300` | High-fidelity 1080p 10-bit AV1 episodes with multi-channel audio. |
| **`TV 1080p AV1 Storage`** | 1080p TV Series | `200` | `3500` | `300` | Ultra-compact episodic AV1 for massive disk space savings across complete seasons. |
| **`Anime 1080p AV1`** | Anime TV & Films | `500` | `5000` | `300` | 1080p 10-bit AV1 with Dual Audio (+500), Multi-Subs, FLAC/Opus audio, and verified AV1 Anime encoders (`Trix`, `Breeze`, `INDEX`, `Sav1or`, `AV1ARY`, `Sokudo`, `RigAV1`, `Ironclad`). |

---

## 🏆 Verified Active AV1 Encoder Tiers

### 🥇 `AV1 Quality Encoders` (`+1000` in HQ / `-1000` in Storage)
High-bitrate, transparent 4K/1080p AV1 encodes (~20–40 GB) prioritizing maximum fidelity and lossless/surround audio:
* `CoSMiCSuRFeR` (e.g. verified 2160p DV/HDR10+ BluRay rips).

### 🥈 `AV1 Compact Encoders` (`+500` in HQ / `0` in Storage)
Curated transparent mini-encodes balancing compression with grain retention:
* `dAV1nci`, `WhiskeyJack`, `UH`, `edge2020`, `UnAV1Chain`, `Smokindevil`, `UserHEVC`, `RAV1NE`, `R&H` / `R and H`.

### 🎌 `AV1 Anime Encoders` (`+1000` in Anime Profile)
Verified active encoders releasing 10-bit AV1 anime with multi-subs and dual audio (anchored prefix `^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1|Ironclad)\]`):
* `Trix`, `Breeze`, `INDEX`, `Sav1or`, `AV1ARY`, `Sokudo`, `RigAV1`, `Ironclad`.

### 📦 `AV1 Storage Savers` (`-1000` in HQ / `+600` in Storage)
Ultra-compressed micro-encodes for maximum disk space savings:
* `PSA`, `GalaxyRG`, `MeGusta`, `VXT`, `d3g`, `Ghost`, `rartv`, `ELiTE`, `LAMA`, `KaKa`, `YAWNTIC`, `BONE`, `GZ`, `CART`.

---

## 🛠️ Development, Testing & Operational Guidelines

### 🧪 Local Test Battery Usage
Before committing any migration or pattern change, run the test suite:
```bash
# 1. PCD SQLite Schema & Foreign Key Audit Harness (0 findings required)
python3 tests/audit_pcd_harness.py .

# 2. Refined Regex & Codec Pattern Battery
python3 tests/test_refined_regex_battery.py

# 3. Final Anime Encoders Regex Suite
python3 tests/test_final_anime.py

# 4. Full Scoring & Boundary Simulation Battery (46 test cases)
python3 tests/simulate_scoring.py
```

### 🔒 Manual Pre-Push Verification Gate
`tests/sync_and_verify_parity.py` stays **out of CI** because it communicates directly with live local Radarr/Sonarr daemons. Run it manually before pushing to verify pattern parity:
```bash
python3 tests/sync_and_verify_parity.py
```

### ⚙️ Regular Expression (.NET) Specification
> [!IMPORTANT]
> All regular expressions in this PCD repository must strictly adhere to the **.NET Regular Expression specification** (`System.Text.RegularExpressions`), matching the runtime behavior of Radarr/Sonarr (`RegexSpecificationBase.cs:17` — compiled case-insensitive) and the Profilarr compiler engine. Use anchored suffix syntax `-(GROUP)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$` for standard release groups and `^\[GROUP\]` for anime groups to eliminate false positives.

### 📜 Migration & Op Conventions
1. **Immutable:** Published ops are immutable and must never be edited.
2. **Sequential & Isolated:** All custom AV1 layer ops reside in the `900-series` namespace (`900`, `901`, ..., `908`) to avoid upstream Dictionarry collisions.
3. **Single-Purpose:** Each migration must have a clear, isolated objective.
4. **Commit Convention:** Use Conventional Commits (`feat(scope): ...`, `fix(scope): ...`, `docs: ...`, `chore: ...`).

---

## 🚀 Adding to Profilarr

1. In your **Profilarr Web UI**, go to **Settings** > **Databases**.
2. Add or sync **Pure AV1 Database**:
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
3. Under **Instances** > **radarr4k** or **sonarr4k**, select the desired AV1 profiles and click **Sync**.
