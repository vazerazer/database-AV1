# database-AV1

[![PCD Audit & Simulation Battery](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/database-AV1/actions/workflows/ci.yml)

A custom format database and quality profile suite for Radarr and Sonarr, built to the Profilarr PCD v2 specification. The movie profile targets compact 4K that is good on a 55-inch Mini LED, a 32-inch 4K monitor, and a phone: the hallowed and BHDStudio size window, not a transparent encode and not a large WEB-DL. Scoring follows Dumpstarr's Movies 2160p direct-play weights (Dolby Vision, HDR, DD+, no HD audio, no SDR disc) without taking that profile's WEB-first ladder or its hallowed-only bonus.

## Upstream

Derived from [Dictionarry-Hub/database](https://github.com/Dictionarry-Hub/database), then widened from tracker and forum notes on middle-size 4K HEVC (r/trackers, r/sonarr, TRaSH group requests). On those screens a soft encode shows and a phone would hide it. The target is what hallowed (~135 MB/min) and BHDStudio (~120 MB/min) already produce. HONE disc encodes in that same window share their score, so a larger HONE does not replace a smaller file from prestige alone. Public size notes put edge2020 with the large UHD groups (MainFrame, CtrlHD), so it sits one step down with QxR and TAoE. dkore stays in the mid-size circle; the same notes list it there. A larger copy from that circle shares the circle's score, so size does not jump a class. There is no bitrate cap and no gigabyte penalty: Return of the King extended hallowed is 35.2 GB and 179 MB/min, and a much larger file of the same score stays too.

Compact streaming WEB-DLs come next. That is FLUX, Kitsune and CMRG, and a compact Apple TV, iTunes, Amazon, Netflix, Max or Disney+ release from a vetted group. A Blu-ray encode still beats those. An elite WEB, such as HONE, stays above that streaming step. PSA, PSARips, d3g and the other small encodes come after the compact WEB-DLs, and PSA is the last 4K fallback that clears the minimum. UTR, RARBG, iVy, Joy, t0paz and POF stay on the Micro OK list and are not banned, but at 4K they score 0 and miss the minimum. An untouched 4K WEB-DL such as BYNDR, NTb, XEBEC or HHWEB scores 0 the same way. Neither is grabbed, so Radarr continues at 1080p instead of importing a 4K micro. A 4K file that is already in the library is not replaced by that 1080p copy, because Radarr does not downgrade a quality group. The 1080p ladder is the same shape: elite HEVC (including Ralphy), then the circle, then FLUX/Kitsune/CMRG, then PSA, then a micro. A HONE Movies Anywhere WEB is not rejected for bitrate. It stays a +15 tie-break and does not outrank the disc. YTS and MeGusta stay rejected. Transparent groups (MainFrame, CtrlHD, W4NK3R, FraMeSToR) stay out, as do NVENC tags such as KONTRAST.

The movie profile takes Dumpstarr's direct-play tie-breakers and not its group ladder. Dolby Vision is +1000 and HDR is +500. HDR10+ is +600, because our HDR format does not also match HDR10+ and Dumpstarr's two scores add up to that. Dolby Digital + is +125, Dolby Digital is +115, Atmos is +25, and AAC is +10. Special Edition is +125. Storefronts stay at or below +15, in Dumpstarr's order: Movies Anywhere, then Disney+ and iTunes, then Apple TV+ / Max / HBO Max, then Amazon, Netflix, ATV, and Hulu. TrueHD, DTS-HD MA, DTS-HD HRA and DTS-X miss the cutoff, because those tracks will not direct-play. LPCM and FLAC are not denied: Dumpstarr treats PCM as audio in the name, and does not score it below zero. A 4K Blu-ray with no HDR, HDR10, HDR10+ or Dolby Vision in the name misses the cutoff. A Dolby Vision WEB with no HDR token misses it too. WEB-DL is exempt from the SDR rule. Dumpstarr's -10000 penalty fits their tier bases near 1500. Our 4K class step is 3200 points, and the direct-play, SDR, and Dolby Vision-without-fallback penalties are -100000 so they still miss a tier base in the tens of thousands. hallowed does not get a private +600, and Movies Anywhere does not get +2000. HONE, BHDStudio, DarQ, DiscoD, dkore, HQMUX, PTer, Chivaman, Weasley, Vyndros, Ralphy and the rest of the elite regex share one score. The Elite, Circle, Small, Micro OK and streaming lists are unchanged, including edge2020 in the circle.

## Profiles

* **Movies 2160p HEVC Compact** — mid-size Blu-ray (one score for the whole elite list), then a smaller disc (QxR, TAoE, edge2020), then compact streaming WEB, then PSA. A 4K micro (UTR, RARBG, iVy, Joy, t0paz, POF) scores 0, and so does untouched 4K WEB-DL. Neither clears 3000, so the next grab is 1080p: elite HEVC 9600, circle 6400, FLUX/Kitsune/CMRG 5200, PSA 4100, micro 3000. Radarr max size stays 0, so a large file is not rejected. Preferred size is 130 MB/min for 2160p encodes and 18 MB/min for 1080p encodes. 18 is the midpoint of the 15–20 MB/min band, about 2.1 GB for a two-hour movie, and it is only a same-score tie-break. Remux stays preferred 1999 and stays off the profile. A 230 MB/min HONE WEB is kept or skipped on score, not on size. There is no gigabyte penalty. Movies Anywhere is a storefront tie-break and does not outrank a Blu-ray. HDR disc encodes are required. HD audio is rejected.
* **TV 2160p HEVC Compact** — the same groups, with WEB ranked above disc. That order was not restacked. BHDStudio shares the top circle. FLUX, Kitsune and CMRG sit above untouched WEB-DL. Sonarr size rows stay as the earlier migrations left them: 2160p encode qualities at min 6, preferred 130, max 200, and 1080p encode qualities at min 2, preferred 10, max 30. TV does not take the movie profile's HD-audio ban or the SDR Blu-ray ban.

AV1, remuxes, 4K x264, a 4K micro, and releases with no vetted group do not clear the minimum score. 4K class gaps between the classes that still clear 3000 are 3200 points, wider than Dolby Vision, HDR10+, Dolby Digital +, Atmos, and a special edition together, so those weights only break ties inside a 4K class. The 1080p steps under the circle are 1200, 1100 and 1100, which is enough that Dolby Vision alone cannot reorder them. Both 1080p PSA and a 1080p micro still clear the minimum of 3000.

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
