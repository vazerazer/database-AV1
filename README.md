# database-AV1

[![PCD Audit & Simulation Battery](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml)

A custom format database and quality profile suite for Radarr 4K, built to the Profilarr PCD v2 specification. It implements an AV1-first scoring ladder that prioritizes genuine AV1 releases while maintaining curated fallback bands for x265 and x264 releases when AV1 is unavailable.

## Upstream

Derived from [Dictionarry-Hub/database](https://github.com/Dictionarry-Hub/database). This fork departs from upstream by placing verified AV1 encoders at the top of the quality hierarchy and structuring non-AV1 releases as temporary, upgradeable fallbacks.

## Features

* **AV1-First Prioritization:** Top scoring for verified AV1 disc masters (`CoSMiCSuRFeR`, `RandH`, `TAoE`, `dAV1nci`, `ChopperHitler`, etc.).
* **IMAX Tie-Breaker:** Prioritizes 1.90:1 expanded aspect ratio releases (IMAX / IMAX Enhanced) over standard letterboxed widescreen.
* **ARC-Optimized Bitstream Audio:** Universal Dolby Atmos, Dolby Digital Plus, and full-rate 1509 kbps DTS Core passthrough.
* **Monotonic Fallback Tiers:** Strict score separation preventing tier inversion across 4K disc masters, 4K WEB-DLs, and archival 1080p fallbacks.

## Usage

Import this repository into Profilarr to manage and sync custom formats to your Arr instances:

1. In Profilarr, navigate to **Settings** > **Databases**.
2. Add a new database:
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
3. Select the `Movies 2160p AV1 HQ` profile under your instance configuration and sync.

*Note: Profilarr syncs custom format definitions and scores to the target profile. Root folder mappings, download clients, and indexers remain managed directly in Radarr.*

## Repository Layout

* `ops/` — Versioned SQL migration scripts defining custom formats, regex patterns, and profile scores.
* `tests/` — Automated CI test harnesses verifying schema integrity, regex behavior, scoring boundaries, and profile drift.
* `scripts/` — Upstream synchronization script (`sync_upstream.sh`).

## Running Tests

```bash
python3 tests/audit_pcd_harness.py .
python3 tests/test_refined_regex_battery.py
python3 tests/test_final_anime.py
python3 tests/simulate_scoring.py
python3 tests/test_library_audit.py
python3 tests/test_supply_audit.py
python3 tests/test_divergence_study.py
python3 tests/test_tripwire_hygiene.py
python3 tests/test_profile_drift.py
```

## License

MIT License. See [LICENSE](LICENSE) for details.
