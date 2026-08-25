# 💎 Profilarr Compliant Database (PCD) — Session Handoff & Architecture Guide

**Repository:** `vazerazer/database-AV1`  
**Branch:** `v2`  
**Schema Specification:** PCD v2 (Schema `1.1.0`)  
**Status:** **Phases 0–5 Fully Complete & Deployed to Production**

---

## 1. Current State & Verification Evidence

All 6 development phases from architecture extraction through E2E live synchronization and GitHub Actions CI have been fully implemented, tested, and verified against real-world media release datasets and live Arr daemon APIs.

### Test Harnesses & Evidence Artifacts Location
All validation scripts live in the repository `tests/` directory:
* [`tests/audit_pcd_harness.py`](file:///home/user/desktop-streamer/database-AV1/tests/audit_pcd_harness.py): Standalone Python validation engine verifying SQLite integrity, schema loading, foreign keys, and referential integrity (0 findings, 0 FK violations across 35 tables and 299 ops).
* [`tests/simulate_scoring.py`](file:///home/user/desktop-streamer/database-AV1/tests/simulate_scoring.py): 42-case scoring simulation battery evaluating pure AV1, fallback ladders, max-stacked x265/x264 releases, dotted variations (`H.265`, `x.265`, `H.264`), site-tagged variants (`-UH[TGx]`, `-dAV1nci[rarbg]`), adversarial group checks (`-edge2020HD`), anime encoders, upgrade increments, and universal hygiene (42/42 passed).
* [`tests/sync_and_verify_parity.py`](file:///home/user/desktop-streamer/database-AV1/tests/sync_and_verify_parity.py): Live synchronization engine with cooldown handling that pulls compiled patterns from Radarr/Sonarr `/api/v3/customformat` and verifies **100% byte-for-byte pattern parity** against the underlying PCD SQLite database.
* [`.github/workflows/ci.yml`](file:///home/user/desktop-streamer/database-AV1/.github/workflows/ci.yml): GitHub Actions CI workflow running `audit_pcd_harness.py` and `simulate_scoring.py` against the Dictionarry-Hub schema on all pushes and PRs.

---

## 2. Core Architectural & Design Decisions

### A. 900-Series Isolation & Migration Immutability
* Preserved upstream Dictionarry migration history from `0.rosettarr.sql` through `290.add-arin-to-1080-720p-quality-tier-5.sql` (291 upstream base ops).
* Isolated the custom AV1 layer in the high-range `900` namespace:
  * [`ops/900.create-av1-master-regexes.sql`](file:///home/user/desktop-streamer/database-AV1/ops/900.create-av1-master-regexes.sql): Regular expressions and value-guarded upgrade of canonical `AV1`.
  * [`ops/901.add-av1-master-custom-formats.sql`](file:///home/user/desktop-streamer/database-AV1/ops/901.add-av1-master-custom-formats.sql): Custom Formats, conditions, pattern links, and tags.
  * [`ops/902.create-av1-master-quality-profiles.sql`](file:///home/user/desktop-streamer/database-AV1/ops/902.create-av1-master-quality-profiles.sql): 7 Pure AV1 Quality Profiles, quality groups with schema 1.1.0 `position`, quality order cutoff, and baseline scoring.
  * [`ops/903.add-not-av1-custom-format.sql`](file:///home/user/desktop-streamer/database-AV1/ops/903.add-not-av1-custom-format.sql): `Not AV1` CF (negated release_title condition on canonical AV1 regex).
  * [`ops/904.add-fallback-ladder-scoring.sql`](file:///home/user/desktop-streamer/database-AV1/ops/904.add-fallback-ladder-scoring.sql): Initial fallback ladder migration (published & byte-immutable).
  * [`ops/905.add-new-av1-encoders.sql`](file:///home/user/desktop-streamer/database-AV1/ops/905.add-new-av1-encoders.sql): R&H ampersand fix (`R[-._ ]?(?:and|&)[-._ ]?H`), Smokindevil, UserHEVC, RAV1NE, Ironclad.
  * [`ops/906.recalibrate-fallback-ladder.sql`](file:///home/user/desktop-streamer/database-AV1/ops/906.recalibrate-fallback-ladder.sql): Fallback ladder recalibration (SDR WEB-DL pass, hallowed HDR10+ top of fallback, Dolby Digital + wiring, canonical AV1 elevated to `+3500`, profile `upgrade_until_score` elevated to `6000`/`5000`).
  * [`ops/907.set-profile-upgrade-increment.sql`](file:///home/user/desktop-streamer/database-AV1/ops/907.set-profile-upgrade-increment.sql): Enforced `upgrade_score_increment = 300` across all 7 profiles to eliminate service/audio churn.

### B. Recalibrated Fallback Ladder & Codec Gate Design
1. **Resolution Hierarchy:** Quality Groups evaluate first (2160p group > 1080p group).
2. **Codec Preference within Quality Groups:**
   * **AV1 Band ($\ge 3500$):** Canonical AV1 (`+3500`) + features/encoders $\rightarrow$ scores $3650 - 5800$.
   * **Tiered x265 Fallback Band ($1000 - 3400$):** High-tier x265 encodes (hallowed, FLUX, HONE, DON, CtrlHD) trigger `Not AV1` (`-2000`) + feature points (`+200`..`+2500`) + Tier score (`+2650`..`+2850`) $\rightarrow$ scores $1050 - 3400$. They pass the minimum cutoff score (`1000` for 2160p, `500` for 1080p) and remain strictly below bare AV1 ($3500$) and `upgrade_until_score` ($6000$), auto-upgrading to AV1 when available.
   * **Random Untiered x265 / Codec-Less Band ($< 1000$):** Untiered releases receive no tier bonus. Features minus `Not AV1` (`-2000`) yield net scores $\le +500 < 1000$, strictly failing the cutoff.
   * **Legacy x264 Band ($< 0$):** Scored at `-5000` with hard rejection.
   * **Remuxes / Full Discs:** Scored at `-10000` with hard rejection.

### C. Production Profile Deployment Scope
Production assignments are intentional and scoped to 4K instances:
* **Radarr4k:** `Movies 2160p AV1 HQ` (ours) + `Movies 2160p` (Dumpstarr).
* **Sonarr4k:** `TV 2160p AV1` (ours) + `TV 2160p` (Dumpstarr).
* The other 5 profiles (`Movies 1080p AV1 HQ/Storage`, `TV 1080p AV1 HQ/Storage`, `Anime 1080p AV1`) remain compiled in PCD catalog.

---

## 3. Telemetry & Live Verification Evidence

1. **The Shawshank Redemption (`movieId=584`):**
   * `The.Shawshank.Redemption.1994-2160p.BluRay.DV.HDR10.10.bit.Encode.AV1.DTS.5.1-R&H`: **Score 3800** (matches `AV1 Compact Encoders` +500 via ampersand fix).
   * `The.Shawshank.Redemption.1994.2160p.UHD.BluRay.DD+5.1.HDR.AV1-Smokindevil`: **Score 3200** (matches `AV1 Compact Encoders` +500).
   * `The.Shawshank.Redemption.1994.2160p.MA.WEB-DL.DTS-HD.MA.5.1.DV.HDR.H.265-TheFarm`: **Score 1000** (clears min cutoff 1000).

2. **Die My Love 2025 (`movieId=633` - No AV1 release):**
   * `Die.My.Love.2025.UHD.BluRay.2160p.DDP.5.1.HDR10+.x265-hallowed` (`Bluray-2160p`): **Score 1650** | **Approved: True** (Top of 2160p fallback band, winner of search).
   * `Die.My.Love.2025.2160p.AMZN.WEB-DL.DD5.1.H.265-FLUX` (`WEBDL-2160p`): **Score 1050** | **Approved: True** (In fallback band).
   * `Die.My.Love.2025.2160p.UHD.BluRay.Remux.HEVC.DV.HDR.Atmos-CiNEPHiLES.mkv`: **Score -350** | **Approved: False** (Rejected).
   * `Die My Love 2025 1080p BluRay x264-GeneMige`: **Score -7000** | **Approved: False** (Hard rejected).

---

## 4. Operational Monitoring & Next Steps

1. **Monitor Live Grab Telemetry:** Confirm continuous clean grabbing of AV1 releases and tiered x265 fallbacks across Radarr4k and Sonarr4k without upgrade loops.
2. **Merge `v2` to `main`:** Merge `v2` branch to `main` after 24 hours of clean production operation.
