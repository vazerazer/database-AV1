# 📊 Op 929: Radarr4k Full-Library Upgrade Census

**Audit Date:** 2026-08-27  
**Target Profile:** `Movies 2160p AV1 HQ` (Profile 64, Read-Only)  
**Total Movies Audited:** 79  
**Operational Status:** **STRICTLY READ-ONLY CENSUS** — Output represents an empirical review queue, not an automated action.

---

## 1. Classification Summary

| Classification | Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **`HOLD`** | **15** | 19.0% | Current library file is already optimal, top-scoring, or anchored by an empirical `PASS` verdict. |
| **`UPGRADE-CANDIDATE`** | **22** | 27.8% | Qualified candidate materially advances playback quality, codec tier, DV/HDR, or resolves a known FAIL/BORDERLINE. |
| **`MANUAL-REVIEW`** | **23** | 29.1% | Score delta exceeds threshold but requires review of audio tracks, bitrate headroom, or group craft exceptions. |
| **`NO-QUALIFIED-CANDIDATE`** | **19** | 24.1% | No indexed candidate cleared profile minimum cutoff score (1000). |
| **Total** | **79** | **100.0%** | Full active Radarr4k library inventory. |

---

## 2. Ranked Priority Upgrade Queue

The following titles are identified as material upgrade candidates, ranked by score improvement delta:

| Rank | Title | Year | Current File (Group / Codec / Score) | Best Candidate (Group / Codec / Score) | Score Delta | Rationale |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| 1 | **The Black Cauldron** | 1985 | `tokar86a` (HEVC, -500 pts) | `TiZU` (AV1, 4150 pts, 5.94GB) | **+4650** | Material codec upgrade from HEVC to AV1 (TiZU, 5.94GB, +4650 pts). |
| 2 | **Akira** | 1988 | `BHDStudio` (x265, 1500 pts) | `TiZU` (AV1, 5450 pts, 8.14GB) | **+3950** | Material codec upgrade from x265 to AV1 (TiZU, 8.14GB, +3950 pts). |
| 3 | **The Deer Hunter** | 1978 | `R` (AV1, 950 pts) | `H` (AV1, 4850 pts, 12.18GB) | **+3900** | Low-scoring baseline file (950) replaced by high-scoring candidate (H, 4850 pts, +3900 delta). |
| 4 | **Jurassic Park** | 1993 | `Smokindevil` (AV1, 1950 pts) | `Smokindevil` (AV1, 5350 pts, 12.32GB) | **+3400** | Low-scoring baseline file (1950) replaced by high-scoring candidate (Smokindevil, 5350 pts, +3400 delta). |
| 5 | **Sisu** | 2022 | `CMRG` (h265, 1600 pts) | `c0kE` (x265, 4900 pts, 15.73GB) | **+3300** | Low-scoring baseline file (1600) replaced by high-scoring candidate (c0kE, 4900 pts, +3300 delta). |
| 6 | **Die My Love** | 2025 | `hallowed` (x265, 1350 pts) | `REBORN` (x265, 4650 pts, 15.38GB) | **+3300** | Low-scoring baseline file (1350) replaced by high-scoring candidate (REBORN, 4650 pts, +3300 delta). |
| 7 | **Greenland 2: Migration** | 2026 | `hallowed` (x265, 1700 pts) | `WOTT` (AV1, 4800 pts, 5.35GB) | **+3100** | Material codec upgrade from x265 to AV1 (WOTT, 5.35GB, +3100 pts). |
| 8 | **X-Men Origins: Wolverine** | 2009 | `ChopperHitler` (AV1, 1800 pts) | `ChopperHitler` (AV1, 4900 pts, 3.91GB) | **+3100** | Low-scoring baseline file (1800) replaced by high-scoring candidate (ChopperHitler, 4900 pts, +3100 delta). |
| 9 | **Jurassic World: Fallen Kingdom** | 2018 | `BHDStudio` (x265, 1500 pts) | `SA89` (x265, 4550 pts, 24.79GB) | **+3050** | Low-scoring baseline file (1500) replaced by high-scoring candidate (SA89, 4550 pts, +3050 delta). |
| 10 | **John Wick: Chapter 2** | 2017 | `Unknown` (AV1, 1850 pts) | `Rosy` (AV1, 4700 pts, 12.11GB) | **+2850** | Low-scoring baseline file (1850) replaced by high-scoring candidate (Rosy, 4700 pts, +2850 delta). |
| 11 | **The Hunt** | 2012 | `KIMJI` (AV1, 1450 pts) | `KIMJI` (AV1, 4250 pts, 3.59GB) | **+2800** | Low-scoring baseline file (1450) replaced by high-scoring candidate (KIMJI, 4250 pts, +2800 delta). |
| 12 | **Greenland** | 2020 | `hallowed` (x265, 1700 pts) | `onlyfaffs` (AV1, 4250 pts, 0.0GB) | **+2550** | Material codec upgrade from x265 to AV1 (onlyfaffs, 0.0GB, +2550 pts). |
| 13 | **Johnny English** | 2003 | `BLUTONiUM` (HEVC, 2100 pts) | `Saon` (AV1, 4150 pts, 5.31GB) | **+2050** | Material codec upgrade from HEVC to AV1 (Saon, 5.31GB, +2050 pts). |
| 14 | **Batman: Mask of the Phantasm** | 1993 | `BHDStudio` (x265, 2100 pts) | `TiZU` (AV1, 4150 pts, 7.89GB) | **+2050** | Material codec upgrade from x265 to AV1 (TiZU, 7.89GB, +2050 pts). |
| 15 | **The Bourne Supremacy** | 2004 | `MainFrame` (x265, 2200 pts) | `WhiskeyJack` (AV1, 4250 pts, 4.2GB) | **+2050** | Material codec upgrade from x265 to AV1 (WhiskeyJack, 4.2GB, +2050 pts). |
| 16 | **The Drama** | 2026 | `hallowed` (x265, 2300 pts) | `Unknown` (AV1, 4050 pts, 0.73GB) | **+1750** | Material codec upgrade from x265 to AV1 (Unknown, 0.73GB, +1750 pts). |
| 17 | **The Rip** | 2026 | `FLUX` (h265, 2450 pts) | `WOTT` (AV1, 4200 pts, 5.37GB) | **+1750** | Material codec upgrade from h265 to AV1 (WOTT, 5.37GB, +1750 pts). |
| 18 | **Extraction 2** | 2023 | `FLUX` (h265, 2450 pts) | `BTT` (AV1, 3800 pts, 4.33GB) | **+1350** | Material codec upgrade from h265 to AV1 (BTT, 4.33GB, +1350 pts). |
| 19 | **X2** | 2003 | `BHDStudio` (x265, 1500 pts) | `DKong` (AV1, 2800 pts, 0.95GB) | **+1300** | Material codec upgrade from x265 to AV1 (DKong, 0.95GB, +1300 pts). |
| 20 | **X-Men: The Last Stand** | 2006 | `hallowed` (x265, 1550 pts) | `DKong` (AV1, 2800 pts, 0.96GB) | **+1250** | Material codec upgrade from x265 to AV1 (DKong, 0.96GB, +1250 pts). |
| 21 | **The Lost World: Jurassic Park** | 1997 | `BHDStudio` (x265, 2150 pts) | `FELIX12345` (AV1, 2800 pts, 6.57GB) | **+650** | Material codec upgrade from x265 to AV1 (FELIX12345, 6.57GB, +650 pts). |
| 22 | **Magic Mike** | 2012 | `hallowed` (x265, 1550 pts) | `FLUX` (x265, 2150 pts, 24.56GB) | **+600** | Low-scoring baseline file (1550) replaced by high-scoring candidate (FLUX, 2150 pts, +600 delta). |

---

## 3. Dedicated Review: CMRG x265 Releases (Parked from Op 927)

`CMRG` produces widely distributed x265 UHD transparent encodes and remuxes. Analysis of interactive search appearances:

Discovered **199 candidate releases** matching `CMRG` across 8 distinct library titles.

| Movie Title | Year | Candidate Size | Codec | Review & Fallback Calibration Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Sisu** | 2022 | 10.50 GB | `x265` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **Dark Phoenix** | 2019 | 3.60 GB | `x264` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **Extraction 2** | 2023 | 4.38 GB | `x265` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **The Rip** | 2026 | 1.48 GB | `x264` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **John Wick: Chapter 3 - Parabellum** | 2019 | 12.57 GB | `x264` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **John Wick: Chapter 4** | 2023 | 3.08 GB | `x265` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **Jurassic World: Fallen Kingdom** | 2018 | 3.56 GB | `Unknown` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |
| **Jurassic World** | 2015 | 1.51 GB | `x264` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |

---

## 4. Complete Library Catalog Census Breakdown

| Title | Year | Current Summary | Best Candidate Summary | Delta | Status | Decision Rationale |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **Predator: Badlands** | 2025 | RandH (AV1, 11.41GB, 5450 pts) | RandH (AV1, 12.38GB, 5450 pts) | `+0` | **`HOLD`** | Current file 'RandH' (5450 pts) equals or outperforms all indexed candidates (best candidate: 5450 pts). |
| **Blade Runner** | 1982 | hallowed (x265, 13.82GB, 2150 pts) | HiDt (x265, 20.74GB, 4950 pts) | `+2800` | **`MANUAL-REVIEW`** | Score delta (+2800) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Shawshank Redemption** | 1994 | hallowed (x265, 16.7GB, 2150 pts) | SA89 (x265, 28.33GB, 4350 pts) | `+2200` | **`MANUAL-REVIEW`** | Score delta (+2200) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Sisu** | 2022 | CMRG (h265, 9.95GB, 1600 pts) | c0kE (x265, 15.73GB, 4900 pts) | `+3300` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1600) replaced by high-scoring candidate (c0kE, 4900 pts, +3300 delta). |
| **Die My Love** | 2025 | hallowed (x265, 15.51GB, 1350 pts) | REBORN (x265, 15.38GB, 4650 pts) | `+3300` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1350) replaced by high-scoring candidate (REBORN, 4650 pts, +3300 delta). |
| **Sisu: Road to Revenge** | 2025 | hallowed (x265, 11.9GB, 2400 pts) | HiDt (x265, 13.3GB, 5050 pts) | `+2650` | **`MANUAL-REVIEW`** | Score delta (+2650) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **City of God** | 2002 | DarQ (x265, 7.47GB, -1850 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Gladiator** | 2000 | RandH (AV1, 11.88GB, 5300 pts) | UH (AV1, 14.1GB, 5450 pts) | `+150` | **`HOLD`** | Candidate 'UH' has minor score advantage (+150), below the +300 upgrade increment threshold. |
| **Akira** | 1988 | BHDStudio (x265, 14.36GB, 1500 pts) | TiZU (AV1, 8.14GB, 5450 pts) | `+3950` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (TiZU, 8.14GB, +3950 pts). |
| **2001: A Space Odyssey** | 1968 | hallowed (x265, 17.37GB, 2250 pts) | CtrlHD (x265, 24.35GB, 4800 pts) | `+2550` | **`MANUAL-REVIEW`** | Score delta (+2550) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Sixth Sense** | 1999 | Smokindevil (AV1, 13.99GB, 5350 pts) | Smokindevil (AV1, 14.43GB, 5350 pts) | `+0` | **`HOLD`** | Current file 'Smokindevil' (5350 pts) equals or outperforms all indexed candidates (best candidate: 5350 pts). |
| **The Ides of March** | 2011 | Z0N3 (x264, 13.08GB, -4250 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **The Place Beyond the Pines** | 2013 | hallowed (x265, 18.35GB, 2150 pts) | HiDt (x265, 21.43GB, 4950 pts) | `+2800` | **`MANUAL-REVIEW`** | Score delta (+2800) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **La La Land** | 2016 | hallowed (x265, 15.07GB, 2150 pts) | HiDt (x265, 20.31GB, 5050 pts) | `+2900` | **`MANUAL-REVIEW`** | Score delta (+2900) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Blue Valentine** | 2010 | CtrlHD (x264, 12.54GB, -4250 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Hoosiers** | 1986 | PiRaTeS (h264, 11.88GB, -6800 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Easy A** | 2010 | onlyfaffs (AV1, 2.66GB, 1450 pts) | onlyfaffs (AV1, 3.04GB, 1450 pts) | `+0` | **`HOLD`** | Current file 'onlyfaffs' (1450 pts) equals or outperforms all indexed candidates (best candidate: 1450 pts). |
| **The Drama** | 2026 | hallowed (x265, 14.09GB, 2300 pts) | Unknown (AV1, 0.73GB, 4050 pts) | `+1750` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (Unknown, 0.73GB, +1750 pts). |
| **Johnny English** | 2003 | BLUTONiUM (HEVC, 16.32GB, 2100 pts) | Saon (AV1, 5.31GB, 4150 pts) | `+2050` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from HEVC to AV1 (Saon, 5.31GB, +2050 pts). |
| **The Right Stuff** | 1983 | BHDStudio (x264, 11.55GB, -4150 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Magic Mike** | 2012 | hallowed (x265, 12.93GB, 1550 pts) | FLUX (x265, 24.56GB, 2150 pts) | `+600` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1550) replaced by high-scoring candidate (FLUX, 2150 pts, +600 delta). |
| **The Lord of the Rings: The Fellowship of the Ring** | 2001 | CoSMiCSuRFeR (AV1, 30.91GB, 5950 pts) | REBORN (x265, 23.2GB, 7900 pts) | `+1950` | **`MANUAL-REVIEW`** | Score delta (+1950) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Robin Hood** | 2010 | ZAX (x265, 27.58GB, -850 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Fury** | 2014 | Smokindevil (AV1, 9.9GB, 2550 pts) | Smokindevil (AV1, 11.24GB, 5950 pts) | `+3400` | **`MANUAL-REVIEW`** | Score delta (+3400) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **F1** | 2025 | R (AV1, 13.04GB, 4950 pts) | H (AV1, 14.78GB, 5550 pts) | `+600` | **`MANUAL-REVIEW`** | Score delta (+600) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Deer Hunter** | 1978 | R (AV1, 10.75GB, 950 pts) | H (AV1, 12.18GB, 4850 pts) | `+3900` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (950) replaced by high-scoring candidate (H, 4850 pts, +3900 delta). |
| **Batman: Mask of the Phantasm** | 1993 | BHDStudio (x265, 8.89GB, 2100 pts) | TiZU (AV1, 7.89GB, 4150 pts) | `+2050` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (TiZU, 7.89GB, +2050 pts). |
| **The Black Cauldron** | 1985 | tokar86a (HEVC, 12.17GB, -500 pts) | TiZU (AV1, 5.94GB, 4150 pts) | `+4650` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from HEVC to AV1 (TiZU, 5.94GB, +4650 pts). |
| **The Da Vinci Code** | 2006 | hallowed (x265, 23.33GB, 2300 pts) | HiDt (x265, 24.33GB, 4950 pts) | `+2650` | **`MANUAL-REVIEW`** | Score delta (+2650) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **X-Men: First Class** | 2011 | BHDStudio (x265, 15.14GB, 1500 pts) | hallowed (x265, 18.66GB, 1550 pts) | `+50` | **`HOLD`** | Candidate 'hallowed' has minor score advantage (+50), below the +300 upgrade increment threshold. |
| **Dark Phoenix** | 2019 | ChopperHitler (AV1, 5.89GB, 2500 pts) | SA89 (x265, 16.17GB, 4550 pts) | `+2050` | **`MANUAL-REVIEW`** | Score delta (+2050) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **X-Men** | 2000 | ChopperHitler (AV1, 12.79GB, 5300 pts) | ChopperHitler (AV1, 14.52GB, 4900 pts) | `-400` | **`HOLD`** | Current file 'ChopperHitler' (5300 pts) equals or outperforms all indexed candidates (best candidate: 4900 pts). |
| **X-Men: The Last Stand** | 2006 | hallowed (x265, 13.62GB, 1550 pts) | DKong (AV1, 0.96GB, 2800 pts) | `+1250` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (DKong, 0.96GB, +1250 pts). |
| **X2** | 2003 | BHDStudio (x265, 15.3GB, 1500 pts) | DKong (AV1, 0.95GB, 2800 pts) | `+1300` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (DKong, 0.95GB, +1300 pts). |
| **X-Men: Apocalypse** | 2016 | ChopperHitler (AV1, 11.69GB, 5300 pts) | CHOPPERHITLER (AV1, 13.28GB, 5300 pts) | `+0` | **`HOLD`** | Current file 'ChopperHitler' (5300 pts) equals or outperforms all indexed candidates (best candidate: 5300 pts). |
| **X-Men: Days of Future Past** | 2014 | ChopperHitler (AV1, 11.96GB, 5300 pts) | ChopperHitler (AV1, 13.58GB, 5300 pts) | `+0` | **`HOLD`** | Current file 'ChopperHitler' (5300 pts) equals or outperforms all indexed candidates (best candidate: 5300 pts). |
| **72 HOURS** | 2026 | FLUX (h265, 14.38GB, 2450 pts) | FLUX (x265, 16.34GB, 2450 pts) | `+0` | **`HOLD`** | Current file 'FLUX' (2450 pts) equals or outperforms all indexed candidates (best candidate: 2450 pts). |
| **Yi Yi** | 2000 | BHDStudio (x264, 10.16GB, -4150 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Spider-Man: Brand New Day** | 2026 | *None* | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No file present and no viable releases indexed. |
| **Cast Away** | 2000 | onlyfaffs (AV1, 3.89GB, 4250 pts) | anomoomin (AV1, 6.76GB, 4250 pts) | `+0` | **`HOLD`** | Current file 'onlyfaffs' (4250 pts) equals or outperforms all indexed candidates (best candidate: 4250 pts). |
| **The Grand Budapest Hotel** | 2014 | hallowed (x265, 13.1GB, 2150 pts) | HiDt (x265, 14.5GB, 4800 pts) | `+2650` | **`MANUAL-REVIEW`** | Score delta (+2650) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Perks of Being a Wallflower** | 2012 | playHD (x264, 15.12GB, -6900 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **The Outsiders** | 1983 | c0kE (x265, 21.26GB, 2200 pts) | c0kE (x265, 24.15GB, 4900 pts) | `+2700` | **`MANUAL-REVIEW`** | Score delta (+2700) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Apocalypse Now** | 1979 | R (AV1, 12.72GB, 4200 pts) | R&H (AV1, 13.4GB, 4700 pts) | `+500` | **`MANUAL-REVIEW`** | Score delta (+500) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The End of Oak Street** | 2026 | *None* | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No file present and no viable releases indexed. |
| **Melancholia** | 2011 | HONE (h265, 4.18GB, 950 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Locke** | 2014 | LoRD (x264, 10.28GB, -4100 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Ghost in the Shell** | 1995 | hallowed (x265, 9.34GB, 2300 pts) | DON (x265, 16.23GB, 5100 pts) | `+2800` | **`MANUAL-REVIEW`** | Score delta (+2800) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Greenland** | 2020 | hallowed (x265, 15.93GB, 1700 pts) | onlyfaffs (AV1, 0.0GB, 4250 pts) | `+2550` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (onlyfaffs, 0.0GB, +2550 pts). |
| **Greenland 2: Migration** | 2026 | hallowed (x265, 13.05GB, 1700 pts) | WOTT (AV1, 5.35GB, 4800 pts) | `+3100` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (WOTT, 5.35GB, +3100 pts). |
| **Blackhat** | 2015 | Unknown (x265, 22.24GB, -550 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Extraction 2** | 2023 | FLUX (h265, 17.09GB, 2450 pts) | BTT (AV1, 4.33GB, 3800 pts) | `+1350` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from h265 to AV1 (BTT, 4.33GB, +1350 pts). |
| **The Rip** | 2026 | FLUX (h265, 15.25GB, 2450 pts) | WOTT (AV1, 5.37GB, 4200 pts) | `+1750` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from h265 to AV1 (WOTT, 5.37GB, +1750 pts). |
| **The Hunt** | 2012 | KIMJI (AV1, 3.37GB, 1450 pts) | KIMJI (AV1, 3.59GB, 4250 pts) | `+2800` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1450) replaced by high-scoring candidate (KIMJI, 4250 pts, +2800 delta). |
| **Riders of Justice** | 2020 | LoRD (x264, 10.55GB, -4100 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Interstellar** | 2014 | R (AV1, 16.59GB, 4800 pts) | RandH (AV1, 18.81GB, 5300 pts) | `+500` | **`MANUAL-REVIEW`** | Score delta (+500) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Wolverine** | 2013 | R (AV1, 5.55GB, 2050 pts) | ChopperHitler (AV1, 4.73GB, 4900 pts) | `+2850` | **`MANUAL-REVIEW`** | Score delta (+2850) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **X-Men Origins: Wolverine** | 2009 | ChopperHitler (AV1, 3.44GB, 1800 pts) | ChopperHitler (AV1, 3.91GB, 4900 pts) | `+3100` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1800) replaced by high-scoring candidate (ChopperHitler, 4900 pts, +3100 delta). |
| **Logan** | 2017 | HONE (h265, 16.59GB, 2400 pts) | DON (x265, 12.12GB, 4550 pts) | `+2150` | **`MANUAL-REVIEW`** | Score delta (+2150) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Jack Reacher** | 2012 | RandH (AV1, 12.34GB, 5300 pts) | RandH (AV1, 14.01GB, 5300 pts) | `+0` | **`HOLD`** | Current file 'RandH' (5300 pts) equals or outperforms all indexed candidates (best candidate: 5300 pts). |
| **True Grit** | 2010 | WhiskeyJack (AV1, 4.45GB, 4250 pts) | WhiskeyJack (AV1, 5.05GB, 4250 pts) | `+0` | **`HOLD`** | Current file 'WhiskeyJack' (4250 pts) equals or outperforms all indexed candidates (best candidate: 4250 pts). |
| **The Bourne Supremacy** | 2004 | MainFrame (x265, 21.59GB, 2200 pts) | WhiskeyJack (AV1, 4.2GB, 4250 pts) | `+2050` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (WhiskeyJack, 4.2GB, +2050 pts). |
| **The Bourne Ultimatum** | 2007 | Bi0hazard (AV1, 17.41GB, 4350 pts) | UH (AV1, 3.74GB, 4750 pts) | `+400` | **`MANUAL-REVIEW`** | Score delta (+400) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Lord of the Rings: The Return of the King** | 2003 | CoSMiCSuRFeR (AV1, 41.34GB, 5950 pts) | dAV1nci (AV1, 7.8GB, 7400 pts) | `+1450` | **`MANUAL-REVIEW`** | Score delta (+1450) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **The Lord of the Rings: The Two Towers** | 2002 | CoSMiCSuRFeR (AV1, 29.93GB, 5950 pts) | dAV1nci (AV1, 6.66GB, 7400 pts) | `+1450` | **`MANUAL-REVIEW`** | Score delta (+1450) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Moana** | 2026 | *None* | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No file present and no viable releases indexed. |
| **John Wick** | 2014 | Rob74K (AV1, 12.9GB, 4950 pts) | HiDt (x265, 15.87GB, 4950 pts) | `+0` | **`HOLD`** | Current file 'Rob74K' (4950 pts) equals or outperforms all indexed candidates (best candidate: 4950 pts). |
| **John Wick: Chapter 3 - Parabellum** | 2019 | CoSMiCSuRFeR (AV1, 34.52GB, 5950 pts) | CoSMiCSuRFeR (AV1, 36.28GB, 5950 pts) | `+0` | **`HOLD`** | Current file 'CoSMiCSuRFeR' (5950 pts) equals or outperforms all indexed candidates (best candidate: 5950 pts). |
| **John Wick: Chapter 2** | 2017 | Unknown (AV1, 14.93GB, 1850 pts) | Rosy (AV1, 12.11GB, 4700 pts) | `+2850` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1850) replaced by high-scoring candidate (Rosy, 4700 pts, +2850 delta). |
| **John Wick: Chapter 4** | 2023 | CoSMiCSuRFeR (AV1, 17.76GB, 5950 pts) | CoSMiCSuRFeR (AV1, 18.74GB, 5950 pts) | `+0` | **`HOLD`** | Current file group 'CoSMiCSuRFeR' holds an empirical PASS verdict; delta (+0) is below the upgrade threshold. |
| **A Royal Affair** | 2012 | EbP (x264, 7.25GB, -6900 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Mutiny** | 2026 | *None* | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No file present and no viable releases indexed. |
| **Jurassic Park** | 1993 | Smokindevil (AV1, 10.89GB, 1950 pts) | Smokindevil (AV1, 12.32GB, 5350 pts) | `+3400` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1950) replaced by high-scoring candidate (Smokindevil, 5350 pts, +3400 delta). |
| **The Lost World: Jurassic Park** | 1997 | BHDStudio (x265, 15.08GB, 2150 pts) | FELIX12345 (AV1, 6.57GB, 2800 pts) | `+650` | **`UPGRADE-CANDIDATE`** | Material codec upgrade from x265 to AV1 (FELIX12345, 6.57GB, +650 pts). |
| **Jurassic World: Fallen Kingdom** | 2018 | BHDStudio (x265, 14.75GB, 1500 pts) | SA89 (x265, 24.79GB, 4550 pts) | `+3050` | **`UPGRADE-CANDIDATE`** | Low-scoring baseline file (1500) replaced by high-scoring candidate (SA89, 4550 pts, +3050 delta). |
| **Jurassic World** | 2015 | BHDStudio (x265, 14.52GB, 2150 pts) | HiDt (x265, 24.58GB, 4950 pts) | `+2800` | **`MANUAL-REVIEW`** | Score delta (+2800) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Jurassic Park III** | 2001 | hallowed (x265, 12.13GB, 2150 pts) | HiDt (x265, 15.93GB, 4950 pts) | `+2800` | **`MANUAL-REVIEW`** | Score delta (+2800) exceeds threshold, but requires manual check on bitrate/audio parity. |
| **Project X** | 2012 | CtrlHD (x264, 10.97GB, -4250 pts) | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned. |
| **Caroline - den sidste rejse** | 2012 | *None* | *None* | `+0` | **`NO-QUALIFIED-CANDIDATE`** | No file present and no viable releases indexed. |

---

## 5. Architectural Invariant & Standing Rule

> [!IMPORTANT]
> **Standing Protocol:** Census outputs NEVER authorize automated production changes. Every item in the upgrade queue requires an explicit, evidence-backed operational directive before any grab, import, or file replacement is performed.
