# 💎 Profilarr Compliant Database (PCD) — Session Handoff & Architecture Guide

**Repository:** `vazerazer/database-AV1`  
**Branch:** `v2`  
**Schema Specification:** PCD v2 (Schema `1.1.0`)  
**Status:** **Phases 0–4 Fully Complete & Verified**

---

## 1. Current State & Verification Evidence

All 5 development phases from architecture extraction to live end-to-end Arr synchronization are complete, audited, and verified against real-world media release datasets and live Arr daemon APIs.

### Test Harnesses & Evidence Artifacts Location
All validation scripts have been moved to the repository `tests/` directory:
* [`tests/audit_pcd_harness.py`](file:///home/user/desktop-streamer/database-AV1/tests/audit_pcd_harness.py): Standalone Python validation engine verifying SQLite integrity, schema loading, foreign keys, and referential integrity (0 findings, 0 FK violations across 35 tables and 283 ops).
* [`tests/simulate_scoring.py`](file:///home/user/desktop-streamer/database-AV1/tests/simulate_scoring.py): 22-case scoring simulation battery evaluating pure AV1, max-stacked legacy x265/x264 releases (including dotted variations `H.265`, `x.265`, `H.264`), site-tagged variants (`-UH[TGx]`, `-dAV1nci[rarbg]`), adversarial group checks (`-edge2020HD`), anime encoders, and universal hygiene (22/22 passed).
* [`tests/sync_and_verify_parity.py`](file:///home/user/desktop-streamer/database-AV1/tests/sync_and_verify_parity.py): Live synchronization engine with cooldown handling that pulls compiled patterns from Radarr/Sonarr `/api/v3/customformat` and verifies **100% byte-for-byte pattern parity** against the underlying PCD SQLite database.
* [`tests/test_refined_regex_battery.py`](file:///home/user/desktop-streamer/database-AV1/tests/test_refined_regex_battery.py): 45-case adversarial regex test suite.
* [`tests/test_final_anime.py`](file:///home/user/desktop-streamer/database-AV1/tests/test_final_anime.py): Dedicated regex verification for the 7 verified active AV1 anime release groups.

---

## 2. Core Architectural & Design Decisions

### A. Option A (Fork & Append) Architecture
* Preserved upstream Dictionarry migration history from `0.rosettarr.sql` through `279.add-goliatn-to-1080p-quality-tier-6.sql` (280 base ops).
* Added 3 discrete, append-only migrations:
  * [`ops/280.add-av1-master-regexes.sql`](file:///home/user/desktop-streamer/database-AV1/ops/280.add-av1-master-regexes.sql): Regular expressions and value-guarded upgrade of canonical `AV1`.
  * [`ops/281.add-av1-master-custom-formats.sql`](file:///home/user/desktop-streamer/database-AV1/ops/281.add-av1-master-custom-formats.sql): Custom Formats, conditions, pattern links, and tags.
  * [`ops/282.create-av1-master-quality-profiles.sql`](file:///home/user/desktop-streamer/database-AV1/ops/282.create-av1-master-quality-profiles.sql): 7 Pure AV1 Quality Profiles, quality groups with schema 1.1.0 `position`, quality order cutoff, and the complete scoring matrix.

### B. Final Scoring Matrix & 2160p Leak Prevention
* **Canonical AV1 Codec:** Scored at **`+2000`** across all profiles.
* **2160p Leak Elimination:** Both 2160p profiles (`Movies 2160p AV1 HQ` and `TV 2160p AV1`) enforce a **`1000` minimum cutoff score** and a **`-3500` penalty for `Legacy x265 Codec`**. A max-stacked x265 release with DV (+600), HDR (+400), 10-bit (+300), TrueHD Atmos (+650), and streaming tags (+100) sums to `+2050 - 3500 = -1450`, failing the cutoff by 2,450 points.
* **Universal Hygiene:** CAM, Telesync, Screener, Upscale, 3D, Extras, Sing Along, Full Disc, Full Disc (Quality Match), Dolby Vision (Without Fallback), Banned Groups, Banned Groups (Compact), Banned Groups (Efficient), Banned Groups (Regular), Banned Groups (Release Title), and Banned Remux are scored at **`-10000`** across all 7 profiles.
* **Upstream Tier Ban Removal:** `Banned UHD Bluray` and `Banned WEBRip` were removed from all 7 AV1 profiles because their condition requires membership in legacy x265 tier lists.

### C. Release Group Anchoring Conventions
* Standard release groups must be anchored to the release suffix with optional bracketed site tags:
  `-(GROUP)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$`
* Anime release groups must be anchored to the bracket prefix:
  `^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1)\]`

### D. .NET Regular Expression Compatibility Requirement
All regular expressions in this PCD repository must strictly adhere to the **.NET Regular Expression specification** (`System.Text.RegularExpressions`), matching the runtime behavior of Radarr/Sonarr (`RegexSpecificationBase.cs:17` — compiled case-insensitive) and the Profilarr compiler engine.

### E. Custom Format Deduplication
Upstream Dictionarry op 188 already created Custom Format `AV1` (ID 262). Op 280 upgrades its underlying regex pattern in place using a value guard (`WHERE name = 'AV1' AND pattern = '\bAV1\b'`). Op 281 avoids creating a duplicate `AV1 Codec` CF, eliminating double-matching and database drift.

---

## 3. Deployed-Artifact Bug Postmortem & Fixes

1. **Site-Tag Brackets & Bracket Prefix:**
   * *Issue:* The deployed regex for `AV1 Compact Encoders` had `(?:[a-z0-9_\-\.]+)?` missing brackets, causing `-UH[TGx]` and `-dAV1nci[rarbg]` to fail while allowing false positives like `-edge2020HD`.
   * *Fix:* Updated op 280 with `(?:^\[(?:dAV1nci|UnAV1Chain)\]|-(?:dAV1nci|...)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)` for both Compact and Storage Savers. Verified byte-for-byte against Radarr4k live API.
2. **Dotted Codec Spellings (`H.265`, `x.265`, `H.264`):**
   * *Issue:* `(x265|h265|HEVC)` failed to match dotted variants like `H.265` or `x.265`, allowing dotted x265 releases to evade penalty.
   * *Fix:* Updated op 280 with `(?<![a-z0-9])([xh][-._ ]?265|HEVC)(?![a-z0-9])` and `(?<![a-z0-9])([xh][-._ ]?264|AVC)(?![a-z0-9])`.
3. **Multi-Arr Condition Compatibility:**
   * *Issue:* `AV1 Anime Encoders` condition `arr_type` was set to `sonarr`. When synced to Radarr, it generated an empty specification list resulting in HTTP 400 Bad Request.
   * *Fix:* Updated op 281 to set `arr_type = 'all'` on `AV1 Anime Encoders` condition, enabling flawless sync across both Radarr and Sonarr.

---

## 4. Remaining Tasks for Subsequent Sessions

1. **Git Push Authentication:**
   * `git commit` is complete locally on `v2` (`HEAD -> v2`). Remote push over HTTPS requires configuring a GitHub Personal Access Token (PAT) or adding an SSH deploy key.
2. **Phase 5 CI Workflow:**
   * Create `.github/workflows/ci.yml` to automatically execute `python3 tests/audit_pcd_harness.py .` and `python3 tests/simulate_scoring.py` on pull requests and pushes to `v2` and `main`.
3. **Confirm CAM Custom Format on Sonarr4k:**
   * Confirm that the `CAM` Custom Format is mapped and scored at `-10000` in the Sonarr4k Quality Profiles.
4. **Live Telemetry & Upgrade Loop Monitoring:**
   * Monitor Radarr4k and Sonarr4k logs for 24 hours to ensure no releases enter repetitive download/upgrade loops.
5. **Merge to Main:**
   * Once 24 hours of stable production streaming have elapsed, fast-forward merge `v2` into `main`.
