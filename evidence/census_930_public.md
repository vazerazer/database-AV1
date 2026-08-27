# 📊 Op 930: Radarr4k Full-Library Upgrade Census v2

**Audit Date:** 2026-08-27  
**Target Profile:** `Movies 2160p AV1 HQ` (Profile 64, Read-Only)  
**Total Movies Audited:** 79  
**Operational Status:** **STRICTLY READ-ONLY CENSUS** — Output represents an empirical review queue, not an automated action.

---

## 1. Classification Summary (Resolution & Size-Floor Calibrated)

| Classification | Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **`HOLD`** | **0** | 0.0% | Current library file is already optimal, top-scoring 2160p, or anchored by empirical PASS verdict. |
| **`UPGRADE-CANDIDATE`** | **71** | 89.9% | Qualified candidate materially advances playback quality (res upgrade to 2160p, AV1 codec advancement, or legacy trusted x264). |
| **`MANUAL-REVIEW`** | **0** | 0.0% | Significant score delta within 2160p requiring manual verification of audio channels/bitrate parity. |
| **`NO-QUALIFIED-CANDIDATE`** | **8** | 10.1% | No candidate cleared the +1000 minimum profile cutoff score. |
| **Total** | **79** | **100.0%** | Full active Radarr4k library inventory. |

---

## 2. Top Ranked Priority Upgrade Queue

| Rank | Title | Year | Current File (Group / Codec / Res / Score) | Best Candidate (Group / Codec / Res / Score) | Delta | Material Advancement Rationale |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| 1 | **The Lord of the Rings: The Fellowship of the Ring** | 2001 | `CoSMiCSuRFeR` (AV1, 2160p, 0 pts) | `CoSMiCSuRFeR` (AV1, 2160p, 5950 pts, 32.52GB) | **+5950** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| 2 | **Fury** | 2014 | `Smokindevil` (AV1, 2160p, 0 pts) | `Smokindevil` (AV1, 2160p, 5950 pts, 11.24GB) | **+5950** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (5950 pts, +5950 delta). |
| 3 | **The Lord of the Rings: The Return of the King** | 2003 | `CoSMiCSuRFeR` (AV1, 2160p, 0 pts) | `CoSMiCSuRFeR` (AV1, 2160p, 5950 pts, 43.4GB) | **+5950** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| 4 | **The Lord of the Rings: The Two Towers** | 2002 | `CoSMiCSuRFeR` (AV1, 2160p, 0 pts) | `CoSMiCSuRFeR` (AV1, 2160p, 5950 pts, 31.48GB) | **+5950** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| 5 | **John Wick: Chapter 3 - Parabellum** | 2019 | `AV1-CoSMiCSuRFeR` (AV1, 2160p, 0 pts) | `CoSMiCSuRFeR` (AV1, 2160p, 5950 pts, 36.28GB) | **+5950** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| 6 | **John Wick: Chapter 4** | 2023 | `CoSMiCSuRFeR` (AV1, 2160p, 0 pts) | `CoSMiCSuRFeR` (AV1, 2160p, 5950 pts, 18.74GB) | **+5950** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| 7 | **F1** | 2025 | `R` (AV1, 2160p, 0 pts) | `Unknown` (AV1, 2160p, 5550 pts, 14.78GB) | **+5550** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (5550 pts, +5550 delta). |
| 8 | **Predator: Badlands** | 2025 | `RandH` (AV1, 2160p, 0 pts) | `RandH` (AV1, 2160p, 5450 pts, 12.38GB) | **+5450** | Material upgrade from low baseline (0 pts) to RandH AV1 2160p (5450 pts, +5450 delta). |
| 9 | **Gladiator** | 2000 | `RandH` (AV1, 2160p, 0 pts) | `UH` (AV1, 2160p, 5450 pts, 14.1GB) | **+5450** | Material upgrade from low baseline (0 pts) to UH AV1 2160p (5450 pts, +5450 delta). |
| 10 | **The Sixth Sense** | 1999 | `Smokindevil` (AV1, 2160p, 0 pts) | `Smokindevil` (AV1, 2160p, 5350 pts, 14.43GB) | **+5350** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (5350 pts, +5350 delta). |
| 11 | **Jurassic Park** | 1993 | `Smokindevil` (AV1, 2160p, 0 pts) | `Smokindevil` (AV1, 2160p, 5350 pts, 12.32GB) | **+5350** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (5350 pts, +5350 delta). |
| 12 | **X-Men: Apocalypse** | 2016 | `ChopperHitler` (AV1, 2160p, 0 pts) | `CHOPPERHITLER` (AV1, 2160p, 5300 pts, 13.28GB) | **+5300** | Material upgrade from low baseline (0 pts) to CHOPPERHITLER AV1 2160p (5300 pts, +5300 delta). |
| 13 | **X-Men: Days of Future Past** | 2014 | `ChopperHitler` (AV1, 2160p, 0 pts) | `ChopperHitler` (AV1, 2160p, 5300 pts, 13.58GB) | **+5300** | Material upgrade from low baseline (0 pts) to ChopperHitler AV1 2160p (5300 pts, +5300 delta). |
| 14 | **Interstellar** | 2014 | `RandH` (AV1, 2160p, 0 pts) | `RandH` (AV1, 2160p, 5300 pts, 18.81GB) | **+5300** | Material upgrade from low baseline (0 pts) to RandH AV1 2160p (5300 pts, +5300 delta). |
| 15 | **Jack Reacher** | 2012 | `RandH` (AV1, 2160p, 0 pts) | `RandH` (AV1, 2160p, 5300 pts, 14.01GB) | **+5300** | Material upgrade from low baseline (0 pts) to RandH AV1 2160p (5300 pts, +5300 delta). |
| 16 | **John Wick** | 2014 | `Rob74K` (AV1, 2160p, 0 pts) | `Rob74K` (AV1, 2160p, 4950 pts, 14.0GB) | **+4950** | Material upgrade from low baseline (0 pts) to Rob74K AV1 2160p (4950 pts, +4950 delta). |
| 17 | **X-Men** | 2000 | `ChopperHitler` (AV1, 2160p, 0 pts) | `ChopperHitler` (AV1, 2160p, 4900 pts, 14.52GB) | **+4900** | Material upgrade from low baseline (0 pts) to ChopperHitler AV1 2160p (4900 pts, +4900 delta). |
| 18 | **X-Men Origins: Wolverine** | 2009 | `ChopperHitler` (AV1, 1080p, 0 pts) | `ChopperHitler` (AV1, 1080p, 4900 pts, 3.91GB) | **+4900** | Legacy trusted x264/1080p upgrade: ChopperHitler (4900 pts) lifts archival film above cutoff. |
| 19 | **The Deer Hunter** | 1978 | `R` (AV1, 2160p, 0 pts) | `Unknown` (AV1, 2160p, 4850 pts, 12.18GB) | **+4850** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (4850 pts, +4850 delta). |
| 20 | **Apocalypse Now** | 1979 | `R` (AV1, 2160p, 0 pts) | `Unknown` (AV1, 2160p, 4700 pts, 13.4GB) | **+4700** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (4700 pts, +4700 delta). |
| 21 | **Blade Runner** | 1982 | `hallowed` (x265, 2160p, 0 pts) | `WhiskeyJack` (AV1, 2160p, 4250 pts, 6.71GB) | **+4250** | Material upgrade from low baseline (0 pts) to WhiskeyJack AV1 2160p (4250 pts, +4250 delta). |
| 22 | **Cast Away** | 2000 | `onlyfaffs` (AV1, 1080p, 0 pts) | `anomoomin` (AV1, 1080p, 4250 pts, 6.76GB) | **+4250** | Legacy trusted x264/1080p upgrade: anomoomin (4250 pts) lifts archival film above cutoff. |
| 23 | **The Hunt** | 2012 | `KIMJI` (AV1, 1080p, 0 pts) | `KIMJI` (AV1, 1080p, 4250 pts, 3.59GB) | **+4250** | Legacy trusted x264/1080p upgrade: KIMJI (4250 pts) lifts archival film above cutoff. |
| 24 | **True Grit** | 2010 | `WhiskeyJack` (AV1, 1080p, 0 pts) | `WhiskeyJack` (AV1, 1080p, 4250 pts, 5.05GB) | **+4250** | Legacy trusted x264/1080p upgrade: WhiskeyJack (4250 pts) lifts archival film above cutoff. |
| 25 | **Sisu** | 2022 | `CMRG` (h265, 2160p, 0 pts) | `WOTT` (AV1, 2160p, 4200 pts, 4.51GB) | **+4200** | Material upgrade from low baseline (0 pts) to WOTT AV1 2160p (4200 pts, +4200 delta). |
| 26 | **Sisu: Road to Revenge** | 2025 | `HONE` (h265, 2160p, 0 pts) | `WOTT` (AV1, 2160p, 4200 pts, 5.03GB) | **+4200** | Material upgrade from low baseline (0 pts) to WOTT AV1 2160p (4200 pts, +4200 delta). |
| 27 | **Greenland 2: Migration** | 2026 | `hallowed` (x265, 2160p, 0 pts) | `WOTT` (AV1, 2160p, 4200 pts, 6.18GB) | **+4200** | Material upgrade from low baseline (0 pts) to WOTT AV1 2160p (4200 pts, +4200 delta). |
| 28 | **The Black Cauldron** | 1985 | `TiZU` (AV1, 1080p, 0 pts) | `TiZU` (AV1, 1080p, 4150 pts, 5.94GB) | **+4150** | Legacy trusted x264/1080p upgrade: TiZU (4150 pts) lifts archival film above cutoff. |
| 29 | **John Wick: Chapter 2** | 2017 | `Rob74K` (AV1, 2160p, 0 pts) | `Rob74K` (AV1, 2160p, 3650 pts, 13.73GB) | **+3650** | Material upgrade from low baseline (0 pts) to Rob74K AV1 2160p (3650 pts, +3650 delta). |
| 30 | **The Bourne Ultimatum** | 2007 | `Bi0hazard` (AV1, 2160p, 0 pts) | `Bi0hazard` (AV1, 2160p, 3600 pts, 18.89GB) | **+3600** | Material upgrade from low baseline (0 pts) to Bi0hazard AV1 2160p (3600 pts, +3600 delta). |
| 31 | **The Shawshank Redemption** | 1994 | `Smokindevil` (AV1, 2160p, 0 pts) | `Smokindevil` (AV1, 2160p, 2550 pts, 5.75GB) | **+2550** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (2550 pts, +2550 delta). |
| 32 | **The Wolverine** | 2013 | `R` (AV1, 2160p, 0 pts) | `Unknown` (AV1, 2160p, 2550 pts, 5.89GB) | **+2550** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (2550 pts, +2550 delta). |
| 33 | **72 HOURS** | 2026 | `FLUX` (h265, 2160p, 0 pts) | `FLUX` (Unknown, 2160p, 2450 pts, 16.34GB) | **+2450** | Material upgrade from low baseline (0 pts) to FLUX Unknown 2160p (2450 pts, +2450 delta). |
| 34 | **Extraction 2** | 2023 | `FLUX` (h265, 2160p, 0 pts) | `FLUX` (x265, 2160p, 2450 pts, 19.11GB) | **+2450** | Material upgrade from low baseline (0 pts) to FLUX x265 2160p (2450 pts, +2450 delta). |
| 35 | **The Rip** | 2026 | `FLUX` (h265, 2160p, 0 pts) | `FLUX` (Unknown, 2160p, 2450 pts, 16.12GB) | **+2450** | Material upgrade from low baseline (0 pts) to FLUX Unknown 2160p (2450 pts, +2450 delta). |
| 36 | **La La Land** | 2016 | `hallowed` (x265, 2160p, 0 pts) | `HiDt` (x265, 2160p, 2400 pts, 20.31GB) | **+2400** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2400 pts, +2400 delta). |
| 37 | **Logan** | 2017 | `HONE` (h265, 2160p, 0 pts) | `Unknown` (x265, 2160p, 2400 pts, 17.97GB) | **+2400** | Material upgrade from low baseline (0 pts) to Unknown x265 2160p (2400 pts, +2400 delta). |
| 38 | **The Drama** | 2026 | `hallowed` (x265, 2160p, 0 pts) | `BYNDR` (Unknown, 2160p, 2350 pts, 21.43GB) | **+2350** | Material upgrade from low baseline (0 pts) to BYNDR Unknown 2160p (2350 pts, +2350 delta). |
| 39 | **The Place Beyond the Pines** | 2013 | `hallowed` (x265, 2160p, 0 pts) | `HiDt` (x265, 2160p, 2300 pts, 21.43GB) | **+2300** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| 40 | **The Da Vinci Code** | 2006 | `hallowed` (x265, 2160p, 0 pts) | `HiDt` (x265, 2160p, 2300 pts, 26.29GB) | **+2300** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| 41 | **Ghost in the Shell** | 1995 | `hallowed` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 2300 pts, 10.61GB) | **+2300** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2300 pts, +2300 delta). |
| 42 | **Jurassic World: Fallen Kingdom** | 2018 | `HHWEB` (HEVC, 2160p, 0 pts) | `HHWEB` (x265, 2160p, 2300 pts, 24.01GB) | **+2300** | Material upgrade from low baseline (0 pts) to HHWEB x265 2160p (2300 pts, +2300 delta). |
| 43 | **Jurassic World** | 2015 | `hallowed` (x265, 2160p, 0 pts) | `HiDt` (x265, 2160p, 2300 pts, 25.74GB) | **+2300** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| 44 | **Jurassic Park III** | 2001 | `hallowed` (x265, 2160p, 0 pts) | `HiDt` (x265, 2160p, 2300 pts, 15.93GB) | **+2300** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| 45 | **2001: A Space Odyssey** | 1968 | `hallowed` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 2250 pts, 19.68GB) | **+2250** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2250 pts, +2250 delta). |
| 46 | **The Outsiders** | 1983 | `c0kE` (x265, 1080p, 0 pts) | `c0kE` (x265, 2160p, 2200 pts, 24.15GB) | **+2200** | Resolution upgrade from 1080p to 2160p c0kE x265 (24.15GB, 2200 pts, +2200 delta). |
| 47 | **The Bourne Supremacy** | 2004 | `MainFrame` (x265, 2160p, 0 pts) | `BYNDR` (Unknown, 2160p, 2200 pts, 24.21GB) | **+2200** | Material upgrade from low baseline (0 pts) to BYNDR Unknown 2160p (2200 pts, +2200 delta). |
| 48 | **Magic Mike** | 2012 | `FLUX` (h265, 2160p, 0 pts) | `FLUX` (Unknown, 2160p, 2150 pts, 24.56GB) | **+2150** | Material upgrade from low baseline (0 pts) to FLUX Unknown 2160p (2150 pts, +2150 delta). |
| 49 | **The Grand Budapest Hotel** | 2014 | `hallowed` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 2150 pts, 14.88GB) | **+2150** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2150 pts, +2150 delta). |
| 50 | **The Lost World: Jurassic Park** | 1997 | `BHDStudio` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 2150 pts, 19.19GB) | **+2150** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2150 pts, +2150 delta). |
| 51 | **Batman: Mask of the Phantasm** | 1993 | `BHDStudio` (x265, 2160p, 0 pts) | `BHDStudio` (x265, 2160p, 2100 pts, 10.1GB) | **+2100** | Material upgrade from low baseline (0 pts) to BHDStudio x265 2160p (2100 pts, +2100 delta). |
| 52 | **Johnny English** | 2003 | `BLUTONiUM` (HEVC, 2160p, 0 pts) | `BLUTONiUM` (x265, 2160p, 2000 pts, 17.7GB) | **+2000** | Material upgrade from low baseline (0 pts) to BLUTONiUM x265 2160p (2000 pts, +2000 delta). |
| 53 | **Dark Phoenix** | 2019 | `ChopperHitler` (AV1, 2160p, 0 pts) | `ChopperHitler` (AV1, 2160p, 1900 pts, 6.38GB) | **+1900** | Material upgrade from low baseline (0 pts) to ChopperHitler AV1 2160p (1900 pts, +1900 delta). |
| 54 | **Die My Love** | 2025 | `hallowed` (x265, 2160p, 0 pts) | `REBORN` (x265, 2160p, 1800 pts, 15.38GB) | **+1800** | Material upgrade from low baseline (0 pts) to REBORN x265 2160p (1800 pts, +1800 delta). |
| 55 | **Akira** | 1988 | `BHDStudio` (x265, 2160p, 0 pts) | `SA89` (x265, 2160p, 1700 pts, 4.1GB) | **+1700** | Material upgrade from low baseline (0 pts) to SA89 x265 2160p (1700 pts, +1700 delta). |
| 56 | **Greenland** | 2020 | `hallowed` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 1700 pts, 19.73GB) | **+1700** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1700 pts, +1700 delta). |
| 57 | **X-Men: First Class** | 2011 | `BHDStudio` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 1550 pts, 18.66GB) | **+1550** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1550 pts, +1550 delta). |
| 58 | **X-Men: The Last Stand** | 2006 | `hallowed` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 1550 pts, 15.47GB) | **+1550** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1550 pts, +1550 delta). |
| 59 | **X2** | 2003 | `BHDStudio` (x265, 2160p, 0 pts) | `hallowed` (x265, 2160p, 1550 pts, 18.96GB) | **+1550** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1550 pts, +1550 delta). |
| 60 | **Easy A** | 2010 | `onlyfaffs` (AV1, 1080p, 0 pts) | `onlyfaffs` (AV1, 1080p, 1450 pts, 3.04GB) | **+1450** | Legacy trusted x264/1080p upgrade: onlyfaffs (1450 pts) lifts archival film above cutoff. |
| 61 | **Project X** | 2012 | `CtrlHD` (x264, 1080p, 0 pts) | `DON` (x264, 1080p, 1350 pts, 11.46GB) | **+1350** | Legacy trusted x264/1080p upgrade: DON (1350 pts) lifts archival film above cutoff. |
| 62 | **Melancholia** | 2011 | `HONE` (h265, 1080p, 0 pts) | `playHD` (x264, 1080p, 1300 pts, 18.37GB) | **+1300** | Legacy trusted x264/1080p upgrade: playHD (1300 pts) lifts archival film above cutoff. |
| 63 | **Locke** | 2014 | `LoRD` (x264, 1080p, 0 pts) | `LoRD` (x264, 1080p, 1300 pts, 11.67GB) | **+1300** | Legacy trusted x264/1080p upgrade: LoRD (1300 pts) lifts archival film above cutoff. |
| 64 | **Riders of Justice** | 2020 | `LoRD` (x264, 1080p, 0 pts) | `LoRD` (x264, 1080p, 1300 pts, 11.99GB) | **+1300** | Legacy trusted x264/1080p upgrade: LoRD (1300 pts) lifts archival film above cutoff. |
| 65 | **The Ides of March** | 2011 | `D-Z0N3` (x264, 1080p, 0 pts) | `DON` (x264, 1080p, 1250 pts, 17.5GB) | **+1250** | Legacy trusted x264/1080p upgrade: DON (1250 pts) lifts archival film above cutoff. |
| 66 | **The Right Stuff** | 1983 | `BHDStudio` (x264, 1080p, 0 pts) | `BHDStudio` (x264, 1080p, 1250 pts, 13.12GB) | **+1250** | Legacy trusted x264/1080p upgrade: BHDStudio (1250 pts) lifts archival film above cutoff. |
| 67 | **Yi Yi** | 2000 | `BHDStudio` (x264, 1080p, 0 pts) | `BHDStudio` (x264, 1080p, 1250 pts, 14.25GB) | **+1250** | Legacy trusted x264/1080p upgrade: BHDStudio (1250 pts) lifts archival film above cutoff. |
| 68 | **The Perks of Being a Wallflower** | 2012 | `PiRaTeS` (h264, 1080p, 0 pts) | `playHD` (x264, 1080p, 1250 pts, 17.11GB) | **+1250** | Legacy trusted x264/1080p upgrade: playHD (1250 pts) lifts archival film above cutoff. |
| 69 | **City of God** | 2002 | `DarQ` (x265, 1080p, 0 pts) | `Z0N3` (x264, 1080p, 1150 pts, 14.79GB) | **+1150** | Legacy trusted x264/1080p upgrade: Z0N3 (1150 pts) lifts archival film above cutoff. |
| 70 | **Blue Valentine** | 2010 | `CtrlHD` (x264, 1080p, 0 pts) | `CtrlHD` (x264, 1080p, 1150 pts, 13.62GB) | **+1150** | Legacy trusted x264/1080p upgrade: CtrlHD (1150 pts) lifts archival film above cutoff. |
| 71 | **A Royal Affair** | 2012 | `MrTentsaw` (x265, 1080p, 0 pts) | `MrTentsaw` (x265, 1080p, 1000 pts, 16.06GB) | **+1000** | Legacy trusted x264/1080p upgrade: MrTentsaw (1000 pts) lifts archival film above cutoff. |

---

## 3. Dedicated Review: Legacy Trusted x264 Titles

| Movie Title | Year | Current Group & Codec | Legacy Trusted Candidate | Score Before $\rightarrow$ After | Status & Operational Impact |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **Blue Valentine** | 2010 | `CtrlHD` (x264) | `CtrlHD` (13.62 GB) | `-4250` $\rightarrow$ `+1150` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **The Right Stuff** | 1983 | `BHDStudio` (x264) | `BHDStudio` (13.12 GB) | `-4250` $\rightarrow$ `+1250` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **Hoosiers** | 1986 | `PiRaTeS` (h264) | `None` (0 GB) | `-4250` $\rightarrow$ `+0` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **The Perks of Being a Wallflower** | 2012 | `PiRaTeS` (h264) | `playHD` (17.11 GB) | `-4250` $\rightarrow$ `+1250` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **Project X** | 2012 | `CtrlHD` (x264) | `DON` (11.46 GB) | `-4250` $\rightarrow$ `+1350` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **The Ides of March** | 2011 | `D-Z0N3` (x264) | `DON` (17.5 GB) | `-4250` $\rightarrow$ `+1250` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **Locke** | 2014 | `LoRD` (x264) | `LoRD` (11.67 GB) | `-4250` $\rightarrow$ `+1300` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **A Royal Affair** | 2012 | `MrTentsaw` (x265) | `MrTentsaw` (16.06 GB) | `-4250` $\rightarrow$ `+1000` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |

---

## 4. Complete Library Catalog Census Breakdown (v2 Resolution-Bucketed)

| Title | Year | Current Summary | Best 2160p Candidate | Best 1080p Candidate | Status | Decision Rationale |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- |
| **Predator: Badlands** | 2025 | RandH (AV1, 2160p, 11.41GB, 0 pts) | RandH (AV1, 12.38GB, 5450 pts) | WOTT (AV1, 5.58GB, 4200 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to RandH AV1 2160p (5450 pts, +5450 delta). |
| **Blade Runner** | 1982 | hallowed (x265, 2160p, 13.82GB, 0 pts) | WhiskeyJack (AV1, 6.71GB, 4250 pts) | TiFou (AV1, 6.84GB, 3600 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to WhiskeyJack AV1 2160p (4250 pts, +4250 delta). |
| **The Shawshank Redemption** | 1994 | Smokindevil (AV1, 2160p, 5.05GB, 0 pts) | Smokindevil (AV1, 5.75GB, 2550 pts) | onlyfaffs (AV1, 2.91GB, 1450 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (2550 pts, +2550 delta). |
| **Sisu** | 2022 | CMRG (h265, 2160p, 9.95GB, 0 pts) | WOTT (AV1, 4.51GB, 4200 pts) | playHD (x264, 12.18GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to WOTT AV1 2160p (4200 pts, +4200 delta). |
| **Die My Love** | 2025 | hallowed (x265, 2160p, 15.51GB, 0 pts) | REBORN (x265, 15.38GB, 1800 pts) | playHD (x264, 20.44GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to REBORN x265 2160p (1800 pts, +1800 delta). |
| **Sisu: Road to Revenge** | 2025 | HONE (h265, 2160p, 15.82GB, 0 pts) | WOTT (AV1, 5.03GB, 4200 pts) | anomoomin (AV1, 5.56GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to WOTT AV1 2160p (4200 pts, +4200 delta). |
| **City of God** | 2002 | DarQ (x265, 1080p, 7.47GB, 0 pts) | *None* | Z0N3 (x264, 14.79GB, 1150 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: Z0N3 (1150 pts) lifts archival film above cutoff. |
| **Gladiator** | 2000 | RandH (AV1, 2160p, 11.88GB, 0 pts) | UH (AV1, 14.1GB, 5450 pts) | playHD (x264, 25.4GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to UH AV1 2160p (5450 pts, +5450 delta). |
| **Akira** | 1988 | BHDStudio (x265, 2160p, 14.36GB, 0 pts) | SA89 (x265, 4.1GB, 1700 pts) | TiZU (AV1, 8.14GB, 5450 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to SA89 x265 2160p (1700 pts, +1700 delta). |
| **2001: A Space Odyssey** | 1968 | hallowed (x265, 2160p, 17.37GB, 0 pts) | hallowed (x265, 19.68GB, 2250 pts) | dAV1nci (AV1, 4.52GB, 4650 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2250 pts, +2250 delta). |
| **The Sixth Sense** | 1999 | Smokindevil (AV1, 2160p, 13.99GB, 0 pts) | Smokindevil (AV1, 14.43GB, 5350 pts) | DON (x264, 14.98GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (5350 pts, +5350 delta). |
| **The Ides of March** | 2011 | D-Z0N3 (x264, 1080p, 13.08GB, 0 pts) | *None* | DON (x264, 17.5GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: DON (1250 pts) lifts archival film above cutoff. |
| **The Place Beyond the Pines** | 2013 | hallowed (x265, 2160p, 18.35GB, 0 pts) | HiDt (x265, 21.43GB, 2300 pts) | EbP (x264, 22.21GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| **La La Land** | 2016 | hallowed (x265, 2160p, 15.07GB, 0 pts) | HiDt (x265, 20.31GB, 2400 pts) | Saon (AV1, 3.91GB, 4150 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2400 pts, +2400 delta). |
| **Blue Valentine** | 2010 | CtrlHD (x264, 1080p, 12.54GB, 0 pts) | *None* | CtrlHD (x264, 13.62GB, 1150 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: CtrlHD (1150 pts) lifts archival film above cutoff. |
| **Hoosiers** | 1986 | PiRaTeS (h264, 1080p, 11.88GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Easy A** | 2010 | onlyfaffs (AV1, 1080p, 2.66GB, 0 pts) | *None* | onlyfaffs (AV1, 3.04GB, 1450 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: onlyfaffs (1450 pts) lifts archival film above cutoff. |
| **The Drama** | 2026 | hallowed (x265, 2160p, 14.09GB, 0 pts) | BYNDR (Unknown, 21.43GB, 2350 pts) | playHD (x264, 20.16GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to BYNDR Unknown 2160p (2350 pts, +2350 delta). |
| **Johnny English** | 2003 | BLUTONiUM (HEVC, 2160p, 16.32GB, 0 pts) | BLUTONiUM (x265, 17.7GB, 2000 pts) | Saon (AV1, 5.31GB, 4150 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to BLUTONiUM x265 2160p (2000 pts, +2000 delta). |
| **The Right Stuff** | 1983 | BHDStudio (x264, 1080p, 11.55GB, 0 pts) | *None* | BHDStudio (x264, 13.12GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: BHDStudio (1250 pts) lifts archival film above cutoff. |
| **Magic Mike** | 2012 | FLUX (h265, 2160p, 21.63GB, 0 pts) | FLUX (Unknown, 24.56GB, 2150 pts) | playHD (x264, 13.19GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to FLUX Unknown 2160p (2150 pts, +2150 delta). |
| **The Lord of the Rings: The Fellowship of the Ring** | 2001 | CoSMiCSuRFeR (AV1, 2160p, 30.91GB, 0 pts) | CoSMiCSuRFeR (AV1, 32.52GB, 5950 pts) | UH (AV1, 10.82GB, 4750 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| **Robin Hood** | 2010 | ZAX (x265, 2160p, 27.58GB, 0 pts) | *None* | Z0N3 (x264, 19.96GB, 1150 pts) | **`NO-QUALIFIED-CANDIDATE`** | No 2160p candidate cleared the +1000 minimum profile cutoff score. |
| **Fury** | 2014 | Smokindevil (AV1, 2160p, 9.9GB, 0 pts) | Smokindevil (AV1, 11.24GB, 5950 pts) | 25.ABMJR (x265, 25.0GB, 2200 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (5950 pts, +5950 delta). |
| **F1** | 2025 | R (AV1, 2160p, 13.04GB, 0 pts) | Unknown (AV1, 14.78GB, 5550 pts) | onlyfaffs (AV1, 4.54GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (5550 pts, +5550 delta). |
| **The Deer Hunter** | 1978 | R (AV1, 2160p, 10.75GB, 0 pts) | Unknown (AV1, 12.18GB, 4850 pts) | playHD (x264, 28.59GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (4850 pts, +4850 delta). |
| **Batman: Mask of the Phantasm** | 1993 | BHDStudio (x265, 2160p, 8.89GB, 0 pts) | BHDStudio (x265, 10.1GB, 2100 pts) | TiZU (AV1, 7.89GB, 4150 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to BHDStudio x265 2160p (2100 pts, +2100 delta). |
| **The Black Cauldron** | 1985 | TiZU (AV1, 1080p, 5.23GB, 0 pts) | *None* | TiZU (AV1, 5.94GB, 4150 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: TiZU (4150 pts) lifts archival film above cutoff. |
| **The Da Vinci Code** | 2006 | hallowed (x265, 2160p, 23.33GB, 0 pts) | HiDt (x265, 26.29GB, 2300 pts) | DON (x264, 22.46GB, 1350 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| **X-Men: First Class** | 2011 | BHDStudio (x265, 2160p, 15.14GB, 0 pts) | hallowed (x265, 18.66GB, 1550 pts) | Z0N3 (x264, 18.76GB, 1150 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1550 pts, +1550 delta). |
| **Dark Phoenix** | 2019 | ChopperHitler (AV1, 2160p, 5.89GB, 0 pts) | ChopperHitler (AV1, 6.38GB, 1900 pts) | BHDStudio (x264, 7.3GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to ChopperHitler AV1 2160p (1900 pts, +1900 delta). |
| **X-Men** | 2000 | ChopperHitler (AV1, 2160p, 12.79GB, 0 pts) | ChopperHitler (AV1, 14.52GB, 4900 pts) | playHD (x264, 13.32GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to ChopperHitler AV1 2160p (4900 pts, +4900 delta). |
| **X-Men: The Last Stand** | 2006 | hallowed (x265, 2160p, 13.62GB, 0 pts) | hallowed (x265, 15.47GB, 1550 pts) | DON (x264, 18.31GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1550 pts, +1550 delta). |
| **X2** | 2003 | BHDStudio (x265, 2160p, 15.3GB, 0 pts) | hallowed (x265, 18.96GB, 1550 pts) | DON (x264, 16.16GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1550 pts, +1550 delta). |
| **X-Men: Apocalypse** | 2016 | ChopperHitler (AV1, 2160p, 11.69GB, 0 pts) | CHOPPERHITLER (AV1, 13.28GB, 5300 pts) | playHD (x264, 21.36GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to CHOPPERHITLER AV1 2160p (5300 pts, +5300 delta). |
| **X-Men: Days of Future Past** | 2014 | ChopperHitler (AV1, 2160p, 11.96GB, 0 pts) | ChopperHitler (AV1, 13.58GB, 5300 pts) | KIMJI (AV1, 5.15GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to ChopperHitler AV1 2160p (5300 pts, +5300 delta). |
| **72 HOURS** | 2026 | FLUX (h265, 2160p, 14.38GB, 0 pts) | FLUX (Unknown, 16.34GB, 2450 pts) | *None* | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to FLUX Unknown 2160p (2450 pts, +2450 delta). |
| **Yi Yi** | 2000 | BHDStudio (x264, 1080p, 10.16GB, 0 pts) | *None* | BHDStudio (x264, 14.25GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: BHDStudio (1250 pts) lifts archival film above cutoff. |
| **Spider-Man: Brand New Day** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Cast Away** | 2000 | onlyfaffs (AV1, 1080p, 3.89GB, 0 pts) | *None* | anomoomin (AV1, 6.76GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: anomoomin (4250 pts) lifts archival film above cutoff. |
| **The Grand Budapest Hotel** | 2014 | hallowed (x265, 2160p, 13.1GB, 0 pts) | hallowed (x265, 14.88GB, 2150 pts) | dAV1nci (AV1, 3.05GB, 1850 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2150 pts, +2150 delta). |
| **The Perks of Being a Wallflower** | 2012 | PiRaTeS (h264, 1080p, 10.52GB, 0 pts) | *None* | playHD (x264, 17.11GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: playHD (1250 pts) lifts archival film above cutoff. |
| **The Outsiders** | 1983 | c0kE (x265, 1080p, 21.26GB, 0 pts) | c0kE (x265, 24.15GB, 2200 pts) | *None* | **`UPGRADE-CANDIDATE`** | Resolution upgrade from 1080p to 2160p c0kE x265 (24.15GB, 2200 pts, +2200 delta). |
| **Apocalypse Now** | 1979 | R (AV1, 2160p, 12.72GB, 0 pts) | Unknown (AV1, 13.4GB, 4700 pts) | RAV1NE (AV1, 4.22GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (4700 pts, +4700 delta). |
| **The End of Oak Street** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Melancholia** | 2011 | HONE (h265, 1080p, 4.18GB, 0 pts) | *None* | playHD (x264, 18.37GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: playHD (1300 pts) lifts archival film above cutoff. |
| **Locke** | 2014 | LoRD (x264, 1080p, 10.28GB, 0 pts) | *None* | LoRD (x264, 11.67GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: LoRD (1300 pts) lifts archival film above cutoff. |
| **Ghost in the Shell** | 1995 | hallowed (x265, 2160p, 9.34GB, 0 pts) | hallowed (x265, 10.61GB, 2300 pts) | *None* | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2300 pts, +2300 delta). |
| **Greenland** | 2020 | hallowed (x265, 2160p, 15.93GB, 0 pts) | hallowed (x265, 19.73GB, 1700 pts) | LoRD (x264, 17.93GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (1700 pts, +1700 delta). |
| **Greenland 2: Migration** | 2026 | hallowed (x265, 2160p, 13.05GB, 0 pts) | WOTT (AV1, 6.18GB, 4200 pts) | WOTT (AV1, 5.35GB, 4800 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to WOTT AV1 2160p (4200 pts, +4200 delta). |
| **Blackhat** | 2015 | Unknown (x265, 2160p, 22.24GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p candidate cleared the +1000 minimum profile cutoff score. |
| **Extraction 2** | 2023 | FLUX (h265, 2160p, 17.09GB, 0 pts) | FLUX (x265, 19.11GB, 2450 pts) | BTT (AV1, 4.33GB, 3800 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to FLUX x265 2160p (2450 pts, +2450 delta). |
| **The Rip** | 2026 | FLUX (h265, 2160p, 15.25GB, 0 pts) | FLUX (Unknown, 16.12GB, 2450 pts) | WOTT (AV1, 5.37GB, 4200 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to FLUX Unknown 2160p (2450 pts, +2450 delta). |
| **The Hunt** | 2012 | KIMJI (AV1, 1080p, 3.37GB, 0 pts) | *None* | KIMJI (AV1, 3.59GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: KIMJI (4250 pts) lifts archival film above cutoff. |
| **Riders of Justice** | 2020 | LoRD (x264, 1080p, 10.55GB, 0 pts) | *None* | LoRD (x264, 11.99GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: LoRD (1300 pts) lifts archival film above cutoff. |
| **Interstellar** | 2014 | RandH (AV1, 2160p, 16.59GB, 0 pts) | RandH (AV1, 18.81GB, 5300 pts) | onlyfaffs (AV1, 3.82GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to RandH AV1 2160p (5300 pts, +5300 delta). |
| **The Wolverine** | 2013 | R (AV1, 2160p, 5.55GB, 0 pts) | Unknown (AV1, 5.89GB, 2550 pts) | ChopperHitler (AV1, 4.73GB, 4900 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Unknown AV1 2160p (2550 pts, +2550 delta). |
| **X-Men Origins: Wolverine** | 2009 | ChopperHitler (AV1, 1080p, 3.44GB, 0 pts) | *None* | ChopperHitler (AV1, 3.91GB, 4900 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: ChopperHitler (4900 pts) lifts archival film above cutoff. |
| **Logan** | 2017 | HONE (h265, 2160p, 16.59GB, 0 pts) | Unknown (x265, 17.97GB, 2400 pts) | DON (x264, 13.53GB, 1350 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Unknown x265 2160p (2400 pts, +2400 delta). |
| **Jack Reacher** | 2012 | RandH (AV1, 2160p, 12.34GB, 0 pts) | RandH (AV1, 14.01GB, 5300 pts) | Saon (AV1, 5.67GB, 4150 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to RandH AV1 2160p (5300 pts, +5300 delta). |
| **True Grit** | 2010 | WhiskeyJack (AV1, 1080p, 4.45GB, 0 pts) | *None* | WhiskeyJack (AV1, 5.05GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: WhiskeyJack (4250 pts) lifts archival film above cutoff. |
| **The Bourne Supremacy** | 2004 | MainFrame (x265, 2160p, 21.59GB, 0 pts) | BYNDR (Unknown, 24.21GB, 2200 pts) | WhiskeyJack (AV1, 4.2GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to BYNDR Unknown 2160p (2200 pts, +2200 delta). |
| **The Bourne Ultimatum** | 2007 | Bi0hazard (AV1, 2160p, 17.41GB, 0 pts) | Bi0hazard (AV1, 18.89GB, 3600 pts) | UH.mkv (AV1, 3.74GB, 4750 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Bi0hazard AV1 2160p (3600 pts, +3600 delta). |
| **The Lord of the Rings: The Return of the King** | 2003 | CoSMiCSuRFeR (AV1, 2160p, 41.34GB, 0 pts) | CoSMiCSuRFeR (AV1, 43.4GB, 5950 pts) | UH (AV1, 16.52GB, 4750 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| **The Lord of the Rings: The Two Towers** | 2002 | CoSMiCSuRFeR (AV1, 2160p, 29.93GB, 0 pts) | CoSMiCSuRFeR (AV1, 31.48GB, 5950 pts) | dAV1nci (AV1, 6.66GB, 4650 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| **Moana** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **John Wick** | 2014 | Rob74K (AV1, 2160p, 12.9GB, 0 pts) | Rob74K (AV1, 14.0GB, 4950 pts) | TiFou (AV1, 6.81GB, 4300 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Rob74K AV1 2160p (4950 pts, +4950 delta). |
| **John Wick: Chapter 3 - Parabellum** | 2019 | AV1-CoSMiCSuRFeR (AV1, 2160p, 34.52GB, 0 pts) | CoSMiCSuRFeR (AV1, 36.28GB, 5950 pts) | onlyfaffs (AV1, 3.16GB, 1450 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| **John Wick: Chapter 2** | 2017 | Rob74K (AV1, 2160p, 12.65GB, 0 pts) | Rob74K (AV1, 13.73GB, 3650 pts) | onlyfaffs (AV1, 2.57GB, 1450 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Rob74K AV1 2160p (3650 pts, +3650 delta). |
| **John Wick: Chapter 4** | 2023 | CoSMiCSuRFeR (AV1, 2160p, 17.76GB, 0 pts) | CoSMiCSuRFeR (AV1, 18.74GB, 5950 pts) | dAV1nci (AV1, 4.61GB, 4500 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to CoSMiCSuRFeR AV1 2160p (5950 pts, +5950 delta). |
| **A Royal Affair** | 2012 | MrTentsaw (x265, 1080p, 14.14GB, 0 pts) | *None* | MrTentsaw (x265, 16.06GB, 1000 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: MrTentsaw (1000 pts) lifts archival film above cutoff. |
| **Mutiny** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Jurassic Park** | 1993 | Smokindevil (AV1, 2160p, 10.89GB, 0 pts) | Smokindevil (AV1, 12.32GB, 5350 pts) | FELIX12345 (AV1, 6.41GB, 2800 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to Smokindevil AV1 2160p (5350 pts, +5350 delta). |
| **The Lost World: Jurassic Park** | 1997 | BHDStudio (x265, 2160p, 15.08GB, 0 pts) | hallowed (x265, 19.19GB, 2150 pts) | FELIX12345 (AV1, 6.57GB, 2800 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to hallowed x265 2160p (2150 pts, +2150 delta). |
| **Jurassic World: Fallen Kingdom** | 2018 | HHWEB (HEVC, 2160p, 22.16GB, 0 pts) | HHWEB (x265, 24.01GB, 2300 pts) | playHD (x264, 13.93GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to HHWEB x265 2160p (2300 pts, +2300 delta). |
| **Jurassic World** | 2015 | hallowed (x265, 2160p, 16.38GB, 0 pts) | HiDt (x265, 25.74GB, 2300 pts) | onlyfaffs (AV1, 5.68GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| **Jurassic Park III** | 2001 | hallowed (x265, 2160p, 12.13GB, 0 pts) | HiDt (x265, 15.93GB, 2300 pts) | FELIX12345 (AV1, 4.72GB, 2800 pts) | **`UPGRADE-CANDIDATE`** | Material upgrade from low baseline (0 pts) to HiDt x265 2160p (2300 pts, +2300 delta). |
| **Project X** | 2012 | CtrlHD (x264, 1080p, 10.97GB, 0 pts) | *None* | DON (x264, 11.46GB, 1350 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: DON (1350 pts) lifts archival film above cutoff. |
| **Caroline - den sidste rejse** | 2012 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
