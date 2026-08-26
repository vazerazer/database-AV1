# 💎 Profilarr Compliant Database (PCD) — Session Handoff & Architecture Guide

**Repository:** `vazerazer/database-AV1`  
**Branch:** `v2`  
**Schema Specification:** PCD v2 (Schema `1.1.0`)  
**Status:** **Ops 900–910 Fully Implemented, Tested, Synced & Deployed**

---

## 1. Current State & Verification Evidence

All 6 development phases from architecture extraction through E2E live synchronization and GitHub Actions CI have been fully implemented, tested, and verified against real-world media release datasets and live Arr daemon APIs.

### Test Harnesses & Evidence Artifacts Location
* [`tests/audit_pcd_harness.py`](tests/audit_pcd_harness.py): Standalone Python validation engine verifying SQLite integrity, schema loading, foreign keys, and referential integrity (0 findings, 0 FK violations across 35 tables and 302 ops).
* [`tests/simulate_scoring.py`](tests/simulate_scoring.py): 55-case scoring simulation battery evaluating pure AV1, fallback ladders, max-stacked x265/x264 releases, dotted variations (`H.265`, `x.265`, `H.264`), site-tagged variants (`-UH[TGx]`, `-dAV1nci[rarbg]`), adversarial group checks (`-edge2020HD`), anime encoders, upgrade increments, and universal hygiene (55/55 passed).
* [`tests/test_refined_regex_battery.py`](tests/test_refined_regex_battery.py): 83-case regex pattern suite testing positive site-tags and dictionary false-positive immunity (`Dust`, `Rosy`, `Saon`, `DIN`, `GanG`, `ENTROPY`).
* [`tests/test_final_anime.py`](tests/test_final_anime.py): 17-case anime encoder regex suite with leading bracket verification (`[Trix]`, `[Ironclad]`, `[Valenciano]`) and unbracketed title false-positive rejection.
* [`tests/sync_and_verify_parity.py`](tests/sync_and_verify_parity.py): Live synchronization engine that pulls compiled patterns from Radarr/Sonarr `/api/v3/customformat` via environment variables and verifies **100% byte-for-byte pattern parity** against the underlying PCD SQLite database.
* [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions CI workflow running `audit_pcd_harness.py`, `test_refined_regex_battery.py`, `test_final_anime.py`, and `simulate_scoring.py` against the Dictionarry-Hub schema on all pushes and PRs.

---

## 2. Core Architectural & Design Decisions

### A. 900-Series Isolation & Migration Immutability
* Preserved upstream Dictionarry migration history from `0.rosettarr.sql` through `290.add-arin-to-1080-720p-quality-tier-5.sql` (291 upstream base ops).
* Isolated the custom AV1 layer in the high-range `900` namespace:
  * [`ops/900.create-av1-master-regexes.sql`](ops/900.create-av1-master-regexes.sql): Regular expressions and value-guarded upgrade of canonical `AV1`.
  * [`ops/901.add-av1-master-custom-formats.sql`](ops/901.add-av1-master-custom-formats.sql): Custom Formats, conditions, pattern links, and tags.
  * [`ops/902.create-av1-master-quality-profiles.sql`](ops/902.create-av1-master-quality-profiles.sql): 7 Pure AV1 Quality Profiles, quality groups with schema 1.1.0 `position`, quality order cutoff, and baseline scoring.
  * [`ops/903.add-not-av1-custom-format.sql`](ops/903.add-not-av1-custom-format.sql): `Not AV1` CF (negated release_title condition on canonical AV1 regex).
  * [`ops/904.add-fallback-ladder-scoring.sql`](ops/904.add-fallback-ladder-scoring.sql): Initial fallback ladder migration (published & byte-immutable).
  * [`ops/905.add-new-av1-encoders.sql`](ops/905.add-new-av1-encoders.sql): R&H ampersand fix (`R[-._ ]?(?:and|&)[-._ ]?H`), Smokindevil, UserHEVC, RAV1NE, Ironclad.
  * [`ops/906.recalibrate-fallback-ladder.sql`](ops/906.recalibrate-fallback-ladder.sql): Fallback ladder recalibration (SDR WEB-DL pass, hallowed HDR10+ top of fallback, Dolby Digital + wiring, canonical AV1 elevated to `+3500`, profile `upgrade_until_score` elevated to `6000`/`5000`).
  * [`ops/907.set-profile-upgrade-increment.sql`](ops/907.set-profile-upgrade-increment.sql): Enforced `upgrade_score_increment = 300` across all 7 profiles to eliminate service/audio churn.
  * [`ops/908.add-av1-quality-encoders.sql`](ops/908.add-av1-quality-encoders.sql): Created `AV1 Quality Encoders` (+1000 in HQ / -1000 in Storage) starting with `CoSMiCSuRFeR`, and set `CAM` condition `arr_type = 'all'` for Sonarr sync.
  * [`ops/909.expand-av1-encoder-tiers.sql`](ops/909.expand-av1-encoder-tiers.sql): Expanded all 4 encoder tiers with telemetry data (~500 AV1 entries), hardened `CAM` regex against word boundaries, and added `ENTROPY` to `Banned Groups`.
  * [`ops/910.op-909-followups.sql`](ops/910.op-909-followups.sql): Hardened `ENTROPY` regex with explicit `(?i)` case-insensitivity prefix.

### B. Encoder Tier Evaluations & Decisions
1. **`UH` Placement Evaluation:**
   * `UH` produces both 1080p compact mini-encodes (sub-5GB) and 2160p transparent encodes (15–23 GB).
   * **Decision:** Kept in `AV1 Compact Encoders` (`+500` in HQ). This ensures its 1080p releases are correctly treated as compact (not penalized in storage profiles) while still receiving +500 in 2160p HQ.
2. **`DIN` and `GanG` False-Positive Validation:**
   * Short English dictionary words tested against titles: `The Dinner (2017)`, `Dinosaur (2000)`, `American Gangster (2007)`, `Gang Related (1997)`, `Gangs of New York (2002)`.
   * **Decision:** Strict end-anchored regex `-(DIN|GanG)(?:\[...\])?(?:\.[a-z0-9]{2,4})?$` prevents any false-positive matches on title tokens. Included in `AV1 Compact Encoders`.
3. **`WOTT` Exclusion:**
   * German DL encoder. Excluded from active tiers because user profiles reject German content by language.
4. **Codec-Agnostic Tier Scoring (e.g. `TAoE`):**
   * Upstream tier CFs match release groups codec-agnostically. When `TAoE` releases an AV1 encode, it matches `AV1` (+3500) + `AV1 Quality Encoders` (+1000) + upstream tier rules (+1700/+2850) $\rightarrow$ scores $6100 - 9300$. This strictly outscores any non-AV1 counterpart ($< 3500$) and maintains quality ordering.
5. **Usenet Poster Tags Known-Miss Trade-Off:**
   * Poster tags appended after group names (e.g. `' mkv-[N-Z-B]'` or `'-[Obfuscated]'`) fail strict trailing anchors.
   * **Decision:** Trailing anchors are intentionally preserved to guarantee 100% false-positive immunity against dictionary words (`Dust`, `Rosy`, `Saon`, `DIN`, `GanG`).
6. **Telemetry-Based Trust:**
   * Grab counts measure indexer trust and community adoption, subject to owner eyeball quality passes.

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

3. **Live Sonarr4k CAM & Quality Profile Scoring (`/api/v3/qualityprofile` on `TV 2160p AV1`):**
   * `AV1`: **`3500`**
   * `AV1 Quality Encoders`: **`1000`**
   * `AV1 Compact Encoders`: **`500`**
   * `AV1 Storage Savers`: **`-1000`**
   * `CAM`: **`-10000`**
   * `Not AV1`: **`-2000`**

---

## 4. Known Limitations & Design Trade-offs

1. **CAM Regex Year-Lookbehind:**
   * The hardened `CAM` regex `(?i)(?<=\b[12]\d{3}\b).*?\b(?:(AC3)?(LD|MD)|CAM[ ._-]?(?:Rip)?|DCP(?:RIP)?|DVD[ ._-]?(?:SCR(?:EENER)?)|HD[ ._-]?(?:CAM|SCR|TC|TS)|(?:LINE|MIC)[ ._-]?DUBBED|SCREENER|(?:TC|TS)(?:Rip)?|TELE(?:CINE|SYNC)|WORKPRINT)\b` requires a 4-digit release year `[12]\d{3}` preceding the telecine/CAM token.
   * **Trade-off Implications:**
     * *(a) Yearless Movie Releases:* A movie release naming convention that completely omits the 4-digit release year would evade this CAM regex.
     * *(b) TV Episode Releases:* Episodic TV releases standardly omit release years in favor of season/episode markers (e.g. `S01E01`), meaning episodic TV telecine releases would not match this pattern.
   * **Rationale:** Telecined TV episodic releases are effectively non-existent on modern Usenet indexers and trackers. Requiring the year lookbehind is strictly mandatory to prevent catastrophic false-positive CAM penalties on legitimate release tokens (e.g. `DTS-HD`, `MA`, `LD`, `MD`, `LINE`, `TC`, `TS`).

2. **Usenet Obfuscation / Poster Tags:**
   * Releases with non-standard poster suffixes appended after the group name (e.g. `Movie.Title.1080p.AV1-dAV1nci mkv-[N-Z-B]`) fail strict end-of-string anchors.
   * **Rationale:** Anchors are intentionally maintained to guarantee 100% false-positive immunity against dictionary words (`Dust`, `Rosy`, `Saon`, `DIN`, `GanG`).

---

## 5. Post-Rewrite Upstream Sync Architecture (Patch-Based)

1. **Severed Git Ancestry:**
   * The repository git history was rewritten using `git filter-repo` to eliminate historical credential artifacts. Consequently, this fork shares no commit SHAs with `Dictionarry-Hub/database`, rendering GitHub's native **"Sync fork"** button unusable (git rejects merges of unrelated histories).
2. **Patch-Based Sync Mechanism:**
   * **State Pointer ([`.github/last-upstream-sha`](.github/last-upstream-sha)):** Stores the exact upstream commit SHA of the last successful sync.
   * **Sync Helper ([`scripts/sync_upstream.sh`](scripts/sync_upstream.sh)):** Fetches `upstream/v2`, diffs the commit range `${LAST_SHA}..${UPSTREAM_HEAD}`, applies the diff cleanly to our tree, and updates the pointer.
   * **Automated CI Workflow ([`.github/workflows/upstream-sync.yml`](.github/workflows/upstream-sync.yml)):** Runs on a daily schedule (`0 6 * * *`) and `workflow_dispatch`. When upstream commits are detected, it applies the patch, runs the full PCD test battery (audit harness, regex suites, scoring simulator), and commits/pushes cleanly.

---

## 6. Library Quality Audit & Measured-File Telemetry (Op 911)

1. **Telemetry & Measured Quality Fingerprints:**
   * [`tests/library_audit.py`](tests/library_audit.py): Audits live Radarr4k (`:7879`) and Sonarr4k (`:8990`) instances using read-only GET requests, extracting actual file size, media info (video codec, bit depth, dynamic range, audio codec/channels), runtime, and grab history.
   * Derives per-group fingerprints: median/mean size, bitrate proxy ($\text{MB/min} = \frac{\text{Size}}{\text{Runtime}}$), resolution distribution, % HDR10/DV, % lossless audio (TrueHD/DTS-HD MA/FLAC), % Atmos, and bit depth.
2. **Selection-Bias Caveat:**
   * Active library files only represent what current quality profiles admitted. To mitigate selection bias, grab history (`/api/v3/history`) is ingested to capture releases that were initially grabbed but later upgraded or replaced, compiling head-to-head comparisons for identical titles.
3. **Contradiction Flags as Review Inputs:**
   * Flags (`QUALITY_UNDERSIZED`, `STORAGE_OVERSIZED`, `COMPACT_OVERSIZED_QUALITY_CANDIDATE`, `UNTIERED_TIERING_CANDIDATE`, `METADATA_MISMATCH`) serve as diagnostic evidence for human review, never as automatic tier overrides.
4. **Privacy & CI Tripwires:**
   * Audit markdown reports containing user library titles are written to `telemetry/` (gitignored).
   * CI enforces automated tripwires in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) failing any build containing 32-character hex API keys or `/home/[A-Za-z0-9._-]+` user home directory paths in tracked files.

---

## 7. Supply-Side Search Audit & Prospective Telemetry (Op 912)

1. **Prospective Indexer Supply Telemetry:**
   * [`tests/supply_audit.py`](tests/supply_audit.py): Evaluates candidate release supply across live Usenet indexers by querying Radarr4k (`GET /api/v3/release?movieId={id}`) and Sonarr4k (`GET /api/v3/release?episodeId={id}`) across a stratified sample of movie and TV titles.
   * Scores all candidates locally in-memory using the PCD SQLite simulation harness ([`tests/simulate_scoring.py`](tests/simulate_scoring.py)) without mutating profile assignments or issuing automatic grab commands.
2. **Per-Group Supply Fingerprints & Win-Rates:**
   * Tracks candidate volume, % AV1 vs x265/x264, size distribution, MB/min bitrate proxy, title-claimed feature tokens (HDR/DV/Atmos/TrueHD), median simulated profile scores, win-rate (% of titles where the group produces the top-scoring candidate), and multi-indexer availability.
3. **Title-Claimed-Flags Caveat:**
   * Prospective search data relies on release title tokens (self-reported naming). Ground-truth media verification (actual streams and bitrates) is provided by the retrospective library audit ([`tests/library_audit.py`](tests/library_audit.py)).
4. **Safety & Indexer Quota Protection:**
   * Strictly read-only GET operations. `POST /api/v3/command` (which triggers automatic downloading) is strictly forbidden. Rate limiting and sample size caps (`SAMPLE_SIZE`, `SEARCH_DELAY`) prevent indexer rate-limit exhaustion.
5. **Supply Diagnostic Flags:**
   * Flags `TIERED_ZERO_SUPPLY` (rewarded groups absent from indexers), `PROFILE_BLIND_SPOT` (releases consistently scoring below cutoff), `ABSURDITY_BAN_CANDIDATE` (fake/corrupt stubs <50MB claiming HD/UHD), and `UPGRADE_OPPORTUNITY` (candidate AV1 release outscoring current non-AV1 library file by $\ge 300$).

---

## 8. Release_Group Divergence Study & Recommendation (Op 913)

1. **Objective & Hypothesis:**
   * Investigated whether migrating AV1 tier custom formats from end-anchored `release_title` regexes to Dumpstarr-style parsed `release_group` matching (`^(?i)(GroupA|GroupB|...)$`) maintains parity across all test batteries and real-world releases.
2. **Oracle & Empirical Methodology ([`tests/divergence_study.py`](tests/divergence_study.py)):**
   * Queried live Radarr4k (`:7879`) and Sonarr4k (`:8990`) parse endpoints (`GET /api/v3/parse?title=...`) across 88 battery test titles (positives, adversarial negatives, anime, and obfuscated formats).
   * Compared production `release_title` match results against candidate `release_group` regexes applied to the parsed `releaseGroup`.
3. **Key Divergence Findings & Failure Modes:**
   * **Compound Name Truncation (`R&H`, `R and H`):** Radarr's built-in parser standardly truncates on `&` and spaces, emitting `releaseGroup='R'`. Candidate `^(?i)(R&H|R and H)$` fails completely, causing total tier scoring dropouts on R&H releases.
   * **Usenet Poster / Obfuscation Suffixes (`-[N-Z-B]`, `mkv-`):** Appended poster suffixes corrupt the parser's token boundary (e.g. emitting `releaseGroup='Z-B'`), causing candidate regexes to miss legitimate encoders (e.g. `dAV1nci`).
   * **Unseasoned Anime Media (`[AV1ARY]`):** Episode and batch titles lacking standard `SxxExx` numbering return `releaseGroup=None` in Sonarr/Radarr parsers. Title-anchored `^[\[(Group)\]` matches 100% reliably.
   * **Negative Case Parity:** Both mechanisms achieve 100% false-positive rejection on dictionary collisions (e.g., `Trix the Girl Who Leapt Through Time...`).
4. **Architectural Decision & Recommendation:**
   * **RETAIN `release_title` MATCHING:** Migration to pure `release_group` is rejected. Our hardened end-anchored and bracket-prefixed `release_title` regexes provide identical false-positive protection while remaining fully immune to *arr parser truncation and obfuscation corruption bugs.

---

## 9. Local Housekeeping, Resource Audit & Sync Hardening (Op 914)

1. **Host Footprint & Media Stack Priority:**
   * Audited system RAM and process tree: 0 endeavor-attributable background processes or hung scripts remain on the host. Media stack services remain untouched and prioritized.
2. **Artifact & Temporary File Purge:**
   * Purged transient test outputs, proof-loop scratch directories, `__pycache__` artifacts, and early root scratch scripts. The repository operates as a self-contained Git entity with `telemetry/` initialized via `.gitkeep`.
3. **Arr Instance Hygiene:**
   * Audited Radarr4k (`:7879`) and Sonarr4k (`:8990`): 0 duplicate or unreferenced AV1 custom formats exist. Every canonical tier CF is referenced with single-cardinality in the active AV1 quality profile.
4. **Upstream Sync Concurrency Protection:**
   * Enhanced [`scripts/sync_upstream.sh`](scripts/sync_upstream.sh) with non-blocking kernel file locking (`flock -n /tmp/pcd_upstream_sync.lock`) to eliminate potential race conditions or concurrent execution overlaps.

---

## 10. Profile-Level Size-Aware Scoring (Op 916)

1. **Motivation & Architecture (Dictionarry Sliders Philosophy):**
   * Avoided hard cutoff limits in `Settings -> Quality` min/max sliders. Instead, implemented dynamic Custom Format scoring using Radarr's `SizeSpecification` condition (absolute GB windows with `min >= 1.0 GB`).
2. **Custom Format Specifications ([`ops/916.add-size-aware-scoring.sql`](ops/916.add-size-aware-scoring.sql)):**
   * **`AV1 Micro 1080p`**: `Resolution: 1080p` AND `AV1 Title Marker` AND `Size: 1.0 - 3.5 GB` (Score: **-2800** in `Movies 2160p AV1 HQ`).
   * **`AV1 Micro 2160p`**: `Resolution: 2160p` AND `AV1 Title Marker` AND `Size: 1.0 - 4.0 GB` (Score: **-2800** in `Movies 2160p AV1 HQ`).
   * **`Oversized 2160p Fallback`**: `Resolution: 2160p` AND `Size: 16.0 - 200.0 GB` AND `NOT AV1 Title Marker` (Score: **-1500** in `Movies 2160p AV1 HQ`).
3. **Core Invariant Guarantees:**
   * **Invariant A (Micro-AV1 vs High-Tier x265):** Micro-AV1 1080p (e.g. Rosy 1.4GB, penalized to 700) loses to standard 1080p/2160p x265 transparent encodes (e.g. DarQ/DON at 1400–1700).
   * **Invariant B (Placeholder Grace):** Micro-AV1 from compact tiers (e.g. onlyfaffs 2.8GB at score 1450) remains grab-able when no better release exists ($\ge 1000$ min cutoff).
   * **Invariant C (2160p AV1 Immunity):** Standard $\ge 4.0\text{GB}$ 2160p AV1 releases experience zero score changes (score intact at 5300–6100).
   * **Invariant D (Non-AV1 Fallback Demotion):** Bloated 20–50GB x265 non-AV1 fallbacks are penalized by -1500, prioritizing transparent 8–14GB x265 encodes.
4. **Scope & Application:**
   * Exclusively applied to `Movies 2160p AV1 HQ` (ID: `64`) in Radarr4k. Sonarr4k remains untouched (where compact/anime 1080p files are intentional).

---

## 11. Graduated Oversized-Fallback Recalibration (Op 917)

1. **Context & Motivation:**
   * Recalibrated the Op 916 binary 16–200 GB oversized cliff into graduated size bands to avoid penalizing legitimate 18–25 GB non-AV1 2160p releases while maintaining protection for long ($\ge 150\text{ min}$) films.
2. **Graduated Size Custom Formats ([`ops/917.add-graduated-oversized-scoring.sql`](ops/917.add-graduated-oversized-scoring.sql)):**
   * **`Tolerated non-AV1 2160p (< 25 GB)`**: **0 penalty** (Clean transparent $1080\text{p}$ and $2160\text{p}$ x265 releases score normally).
   * **`Heavy 2160p Fallback (25 - 30 GB)`**: **`-400` penalty** (Mild nudge preferring leaner options when available).
   * **`Oversized 2160p Fallback (30 - 200 GB)`**: **`-1500` penalty** (Strong demotion for true bloat >250 MB/min).
   * **`AV1 2160p (Any Size)`**: **0 penalty** (Exempt via required negated `(?i)\b(AV1|AV01)\b` title condition).
3. **Long Movie Grace:**
   * Long movies ($\ge 150\text{ min}$) in AV1 (e.g. *LOTR* 30–41 GB) remain 100% immune. Non-AV1 long movies in the heavy/oversized band are penalized, not banned, ensuring they remain grab-able if no alternative exists.








