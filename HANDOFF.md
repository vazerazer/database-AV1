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

### A. Option A (Fork & Append) Architecture with 900-Series Isolation
* Preserved upstream Dictionarry migration history from `0.rosettarr.sql` through `290.add-arin-to-1080-720p-quality-tier-5.sql` (291 upstream ops).
* Isolated the custom AV1 layer in the high-range `900` namespace to guarantee zero collisions with future upstream releases:
  * [`ops/900.create-av1-master-regexes.sql`](file:///home/user/desktop-streamer/database-AV1/ops/900.create-av1-master-regexes.sql): Regular expressions and value-guarded upgrade of canonical `AV1`.
  * [`ops/901.add-av1-master-custom-formats.sql`](file:///home/user/desktop-streamer/database-AV1/ops/901.add-av1-master-custom-formats.sql): Custom Formats, conditions, pattern links, and tags.
  * [`ops/902.create-av1-master-quality-profiles.sql`](file:///home/user/desktop-streamer/database-AV1/ops/902.create-av1-master-quality-profiles.sql): 7 Pure AV1 Quality Profiles, quality groups with schema 1.1.0 `position`, quality order cutoff, and the baseline scoring matrix.
  * [`ops/903.add-not-av1-custom-format.sql`](file:///home/user/desktop-streamer/database-AV1/ops/903.add-not-av1-custom-format.sql): `Not AV1` CF (negated release_title condition on canonical AV1 regex).
  * [`ops/904.add-fallback-ladder-scoring.sql`](file:///home/user/desktop-streamer/database-AV1/ops/904.add-fallback-ladder-scoring.sql): Fallback ladder scoring (`Not AV1` at `-2000`, removal of `Legacy x265 Codec` profile penalties, and upstream Tier scoring).

### B. Coupled Fallback Ladder & Codec Gate Design (Tasks 2 + 3)
* **The Codec-Less Leak Problem:** Releases without an explicit codec token in their title evade all codec-specific penalties (`Legacy x265 Codec`) and cleared the minimum profile score on accumulated feature points alone (DV + HDR + 10-bit + Atmos $\approx +1650$ vs. min 1000).
* **The Solution — `Not AV1` Codec Gate:** Op 903 adds Custom Format `Not AV1` (`negate=1`, `required=1` on canonical `AV1` regex) scored at **`-2000`** across all 7 profiles.
* **Fallback Ladder Mechanics:**
  1. Radarr/Sonarr evaluate **Quality Groups first**, establishing the resolution hierarchy (2160p group > 1080p group).
  2. Within each Quality Group, CF scores establish the codec preference:
     * **AV1 Band ($\ge 2300$):** Canonical AV1 (`+2000`) + features/encoder scores $\ge 2300$. AV1 never triggers `Not AV1`.
     * **Tiered x265 Fallback Band ($1000 - 1400$):** High-tier x265 encodes (FLUX, HONE, DON, CtrlHD, etc.) trigger `Not AV1` (`-2000`) + feature points (`+1400`..`+1700`) + Upstream Tier score (`+1400`..`+1600`), resulting in net scores of $1000 - 1400$. They pass the minimum cutoff score (`1000` for 2160p, `500` for 1080p) but remain well below `upgrade_until` (`3500` / `2500`), enabling instant fallback grabbing and automatic future upgrading to AV1.
     * **Random Untiered x265 / Codec-Less Band ($< 1000$):** Untiered releases receive no tier bonus. Feature points (`+1400`..`+1950`) minus `Not AV1` (`-2000`) yield net scores $\le -50$, strictly failing the cutoff score.
     * **Codec-Less AV1-Unnamed Releases ($< 500$):** Documented trade-off: AV1 releases lacking an explicit AV1 naming token are rejected.
     * **Legacy x264 Band ($< 0$):** Scored at `-5000` with hard rejection.
* **Universal Hygiene:** CAM, Telesync, Screener, Upscale, 3D, Extras, Sing Along, Full Disc, Full Disc (Quality Match), Dolby Vision (Without Fallback), Banned Groups, Banned Groups (Compact), Banned Groups (Efficient), Banned Groups (Regular), and Banned Remux are scored at **`-10000`** across all 7 profiles.

### C. Release Group Anchoring Conventions
* Standard release groups must be anchored to the release suffix with optional bracketed site tags:
  `-(GROUP)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$`
* Anime release groups must be anchored to the bracket prefix:
  `^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1)\]`

### D. .NET Regular Expression Compatibility Requirement
All regular expressions in this PCD repository must strictly adhere to the **.NET Regular Expression specification** (`System.Text.RegularExpressions`), matching the runtime behavior of Radarr/Sonarr (`RegexSpecificationBase.cs:17` — compiled case-insensitive) and the Profilarr compiler engine.

---

## 3. Deployed-Artifact Bug Postmortem & Fixes

1. **Site-Tag Brackets & Bracket Prefix:**
   * *Issue:* The deployed regex for `AV1 Compact Encoders` had `(?:[a-z0-9_\-\.]+)?` missing brackets, causing `-UH[TGx]` and `-dAV1nci[rarbg]` to fail while allowing false positives like `-edge2020HD`.
   * *Fix:* Updated op 900 with `(?:^\[(?:dAV1nci|UnAV1Chain)\]|-(?:dAV1nci|...)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)` for both Compact and Storage Savers. Verified byte-for-byte against Radarr4k live API.
2. **Dotted Codec Spellings (`H.265`, `x.265`, `H.264`):**
   * *Issue:* `(x265|h265|HEVC)` failed to match dotted variants like `H.265` or `x.265`, allowing dotted x265 releases to evade penalty.
   * *Fix:* Updated op 900 with `(?<![a-z0-9])([xh][-._ ]?265|HEVC)(?![a-z0-9])` and `(?<![a-z0-9])([xh][-._ ]?264|AVC)(?![a-z0-9])`.
3. **Multi-Arr Condition Compatibility:**
   * *Issue:* `AV1 Anime Encoders` condition `arr_type` was set to `sonarr`. When synced to Radarr, it generated an empty specification list resulting in HTTP 400 Bad Request.
   * *Fix:* Updated op 901 to set `arr_type = 'all'` on `AV1 Anime Encoders` condition, enabling flawless sync across both Radarr and Sonarr.
4. **Codec-Less Release Leak (Task 2 Postmortem):**
   * *Issue:* Codec-less releases bypassed codec penalties and cleared profile cutoffs.
   * *Fix:* Created `Not AV1` Custom Format (op 903) and scored at `-2000` (op 904).

---

## 4. Remaining Tasks

1. **Task 4 (New Release Groups):** Add `Ironclad` to Anime tier (`nyaa.si/view/2107564`). Research and verify URLs for `RAV1NE` and `UserHEVC` before adding in op 905.
2. **Task 5 (Phase 5 CI Workflow):** Add `.github/workflows/ci.yml` running `audit_pcd_harness.py` and `simulate_scoring.py` on push/PR.
3. **Task 6 (Cleanup):** Verify `CAM` CF on Sonarr4k; audit Radarr for orphaned `AV1 Codec` CF and delete if unscored.
4. **Git Push Authentication:** Configure PAT or SSH key for remote push.
5. **Merge to Main:** Merge `v2` to `main` after 24 hours of stable production operation.
