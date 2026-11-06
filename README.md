# database-AV1

[![PCD Audit & Simulation Battery](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml)

A custom format database and quality profile suite for Radarr and Sonarr, built to the Profilarr PCD v2 specification. The flagship profiles target compact 4K HEVC (x265) encodes: small files from vetted groups, with HDR, Dolby Vision and Atmos used only as tie-breakers inside a tier.

## Upstream

Derived from [Dictionarry-Hub/database](https://github.com/Dictionarry-Hub/database). The compact group ladder follows Dictionarry's 1080p Compact circles (HONE, Vyndros, edge2020, dkore, QxR, TAoE) and applies them to 2160p. Micro encodes that Dictionarry also refuses (YTS, UTR, MeGusta, RARBG, PSA, iVy) stay banned. Untouched WEB-DL groups such as NTb and FLUX are a larger fallback, not the target.

## Profiles

* **Movies 2160p HEVC Compact** — 4K Blu-ray HEVC from the careful circles, then QxR/TAoE, then compact WEB, then untouched WEB-DL, then 1080p HEVC.
* **TV 2160p HEVC Compact** — the same groups, with compact WEB ranked above disc encodes.

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
