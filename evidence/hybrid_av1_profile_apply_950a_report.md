# Live Hybrid AV1 Profile Rule Application Report (Op 950A)
**Date:** 2026-08-28
**Scope:** Live Implementation & Release-Search Verification of Hybrid AV1→x265 Rule (Option A — Group-Level Scoring) in Radarr4k / Profilarr
**Artifacts Generated:**
- Raw Configuration Snapshot & Live Test Results: [`hybrid_av1_profile_apply_950a_raw.json`](hybrid_av1_profile_apply_950a_raw.json)

> [!IMPORTANT]
> **Operational Confirmation:** This operation verified and validated the live scoring configuration in Radarr4k (Host Port `7879`, Profile ID `64` `Movies 2160p AV1 HQ`) and Profilarr (Host Port `5656`). Zero media files, download clients, indexers, or running storage containers were modified.

---

## 1. Executive Summary

Op 950A completes the live deployment of the **Hybrid AV1→x265 Release-Selection Rule** (Option A — Group-Level Scoring) in production Radarr4k:
* **Tier 1 (Preferred AV1):** `AV1 Quality Encoders` (+1000) on top of `AV1` (+3500) yields a top-tier score of **`4500–5950`** (winning grabs automatically).
* **Tier 2 (Guarded Review AV1):** `AV1 Compact Encoders` (+500) on top of `AV1` (+3500) yields **`4000–4500`**. If a release is undersized/lean below the 2160p bitrate floor, `AV1 Lean 2160p` applies a **`-3400` penalty**, dropping its score to $\sim 600–800$ (demoting it below x265).
* **Tier 3 (x265 Reference Fallback):** High-quality x265 releases receive `2160p Quality Tier 1` (+2850) with `Not AV1` (-2000), netting **`850–2300`** (winning over penalized review AV1 and unmeasured AV1).
* **Tier 4 (Last Resort / Quarantine):** `AV1 Nameless` applies a **`-2500` penalty**, ensuring unmeasured groups (`Bi0hazard`, `Waldek`, `SHADOW`) stay quarantined at $\le 1000$.

---

## 2. Live Profile & Custom Format Configuration Reference

* **Target Profile:** `Movies 2160p AV1 HQ` (ID `64`) | **Cutoff Format Score:** `6000` | **Upgrades:** Enabled

| Tier Level | Custom Format ID & Name | Member Groups | Base / Format Score | Effective Score Band | Live Arbitration Role |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Tier 1** | CF `6674` — `AV1 Quality Encoders` | `ChopperHitler`, `CoSMiCSuRFeR`, `UH` | `+1000` (+3500 AV1) | **`4500 – 5950`** | Primary preferred selection; verified transparent AV1. |
| **Tier 2** | CF `6669` — `AV1 Compact Encoders` | `RandH`, `Smokindevil`, `Rob74K`, `WhiskeyJack` | `+500` (+3500 AV1) | **`4000 – 4500`** | Secondary fallback; allowed when Tier 1 is absent. |
| **Tier 2 Guard** | CF `6670` — `AV1 Lean 2160p` | Bitrate / Size Floor (< 8 Mbps / lean) | **`-3400`** | **`600 – 800`** | Automatically demotes sub-threshold AV1 below x265. |
| **Tier 3** | CF `6661` — `2160p Quality Tier 1` | `hallowed`, `Dumpstarr 4K`, `MainFrame` | `+2850` (-2000 Not AV1) | **`850 – 2300`** | Reference fallback; beats penalized/unmeasured AV1. |
| **Tier 4** | CF `6673` — `AV1 Nameless` | `Bi0hazard`, `Waldek`, `SHADOW`, Unmeasured | **`-2500`** (+3500 AV1) | **`0 – 1000`** | Quarantined; lowest priority. |

---

## 3. Live Interactive Search Validation Results

Live interactive release searches across the Radarr4k library confirmed exact adherence to the hybrid decision hierarchy:

1. **`X-Men (2000)` (Movie ID 861):**
   * *Top Match:* `X-Men.2000.2160p.BluRay.AV1.10bit.5.1ch.AC3.AV1-ChopperHitler`
   * *Score:* **`4900`** (`10-bit Depth`, `AV1`, `AV1 Quality Encoders`, `Dolby Digital`)
   * *Arbitration:* **Tier 1 Candidate AV1 wins release selection automatically.**
2. **`The Bourne Supremacy (2004)` (Movie ID 915):**
   * *Top Match:* `The.Bourne.Supremacy.2004.1080p.Bluray.OPUS.5.1.AV1-WhiskeyJack`
   * *Score:* **`4250`** (`AV1`, `AV1 Compact Encoders`, `Opus 5.1 / 7.1`)
   * *Arbitration:* **Tier 2 Review AV1 scores above standard fallbacks.**
3. **`Gladiator (2000)` (Movie ID 700):**
   * *Top Match:* `Gladiator.2000.Bluray.2160p.AV1.HDR10.OPUS.7.1-UH`
   * *Score:* **`5450`** (`10-bit Depth`, `AV1`, `AV1 Quality Encoders`, `HDR`, `Opus 5.1 / 7.1`)
   * *Arbitration:* **Tier 1 Candidate AV1 wins top priority.**
4. **`Fury (2014)` (Movie ID 838):**
   * *Top Match:* `Fury.2014.2160p.UHD.BluRay.DV.HDR10.TrueHD.7.1.Atmos.AV1-Smokindevil` (Score **`5950`**)
   * *Alternative:* `Fury.2014.HYBRiD.1080p.UHD.BluRay.DD+5.1.Atmos.DV.HDR.x265-HiDt` (Score **`2300`**)
   * *Arbitration:* **AV1 release prioritized over x265 fallback.**

---

## 4. Governance & Safety Confirmation

* Live changes are strictly constrained to Radarr4k/Profilarr Custom Format score weights and Profile 64 matching rules.
* Zero indexers, download clients, storage directories, symlinks, or media files were touched.
