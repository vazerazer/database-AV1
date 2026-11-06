# database-AV1

[![PCD Audit & Simulation Battery](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml)

A custom format database and quality profile suite for Radarr and Sonarr, built to the Profilarr PCD v2 specification. The flagship profiles target compact 4K HEVC (x265) encodes: small files from vetted groups, with HDR, Dolby Vision and Atmos used only as tie-breakers inside a tier.

## Upstream

Derived from [Dictionarry-Hub/database](https://github.com/Dictionarry-Hub/database). The ladder is aimed at a 55-inch 4K Mini LED and a 32-inch 4K monitor, where a soft encode shows and a phone would hide it. Dictionarry's compact circles (HONE, Vyndros, edge2020, QxR, TAoE) stay on top. PSA, d3g, SEV and ELiTE are the next step down: smaller, still clean. UTR/Joy, RARBG and iVy are allowed below that and get replaced when a better encode exists. YTS and MeGusta stay rejected because their 4K files break up on those two screens. Untouched WEB-DL groups such as NTb and FLUX are a larger fallback, not the target.

## Profiles

* **Movies 2160p HEVC Compact** — 4K Blu-ray from the careful circles, then QxR/TAoE, then PSA/d3g/SEV/ELiTE, then UTR/RARBG/iVy, then untouched WEB-DL, then 1080p HEVC.
* **TV 2160p HEVC Compact** — the same groups, with WEB ranked above disc encodes.

AV1, remuxes, 4K x264 and releases with no vetted group do not clear the minimum score. Tier gaps are 700 points, wider than the feature stack, so Dolby Vision cannot promote a lower group over a higher one.

## Usage

Import this repository into Profilarr to manage and sync custom formats to your Arr instances:

1. In Profilarr, navigate to **Settings** > **Databases**.
2. Add a new database:
   * **Repository URL:** `https://github.com/vazerazer/database-AV1`
   * **Branch:** `v2`
3. Select `Movies 2160p HEVC Compact` for Radarr and `TV 2160p HEVC Compact` for Sonarr, then sync.

*Note: Profilarr syncs custom format definitions and scores to the target profile. Root folder mappings, download clients, and indexers remain managed directly in the arrs.*

## Repository Layout

* `ops/` — Versioned SQL migration scripts defining custom formats, regex patterns, and profile scores.
* `tests/` — Automated CI test harnesses verifying schema integrity, regex behavior, and scoring boundaries.
* `scripts/` — Upstream synchronization script (`sync_upstream.sh`).

## Running Tests

```bash
python3 tests/audit_pcd_harness.py .
python3 tests/simulate_scoring.py
```

## License

MIT License. See [LICENSE](LICENSE) for details.
