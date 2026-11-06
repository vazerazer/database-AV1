# database-AV1

[![PCD Audit & Simulation Battery](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml)

A custom format database and quality profile suite for Radarr and Sonarr, built to the Profilarr PCD v2 specification. The movie profile targets compact 4K that is good on a 55-inch Mini LED, a 32-inch 4K monitor, and a phone: the hallowed and BHDStudio size window, not a transparent encode and not a large WEB-DL.

## Upstream

Derived from [Dictionarry-Hub/database](https://github.com/Dictionarry-Hub/database), then widened from tracker and forum notes on middle-size 4K HEVC (r/trackers, r/sonarr, TRaSH group requests). On those screens a soft encode shows and a phone would hide it, but a 30–40 GB WEB-DL is the wrong trade. The target is what hallowed (~135 MB/min) and BHDStudio (~120 MB/min) already produce. HONE disc encodes in that same window share their score, so a larger HONE does not replace a smaller file from prestige alone. Public size notes put edge2020 with the large UHD groups (MainFrame, CtrlHD), so it sits one step down with QxR and TAoE. dkore stays in the mid-size circle; the same notes list it there, and the 200 MB/min cap contains the larger copies.

Compact streaming WEB-DLs come next. That is FLUX, Kitsune and CMRG, and a compact Apple TV, iTunes, Amazon, Netflix, Max or Disney+ release from a vetted group. A Blu-ray encode still beats those. PSA and the other micros come after the compact WEB-DLs, and they beat a big untouched WEB-DL such as BYNDR or a 30–40 GB HONE Movies Anywhere dump. UTR, RARBG, iVy, t0paz and POF remain the lowest encodes. YTS and MeGusta stay rejected. Transparent groups (MainFrame, CtrlHD, W4NK3R, FraMeSToR) stay out, as do NVENC tags such as KONTRAST.

## Profiles

* **Movies 2160p HEVC Compact** — mid-size Blu-ray (hallowed, BHDStudio, in-window HONE), then a smaller disc (QxR, TAoE, edge2020), then compact streaming WEB, then PSA, then UTR, then untouched WEB-DL, then 1080p HEVC. 4K qualities are capped at 200 MB/min (preferred 130), which keeps Return of the King hallowed at 179 MB/min and rejects a 230 MB/min dump. A WEB at or above 30 GiB is scored under the micros. Movies Anywhere is a storefront tie-break and does not outrank a Blu-ray.
* **TV 2160p HEVC Compact** — the same groups, with WEB ranked above disc. BHDStudio shares the top circle. FLUX, Kitsune and CMRG sit above untouched WEB-DL. The 30 GiB movie penalty is not applied to episodes.

AV1, remuxes, 4K x264 and releases with no vetted group do not clear the minimum score. Gaps between classes are 700 points, wider than the feature stack, so Dolby Vision, HDR and Atmos only break ties inside a class.

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
