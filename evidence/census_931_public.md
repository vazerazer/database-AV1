# 📊 Op 931: Radarr4k Full-Library Upgrade Census v2.1

**Audit Date:** 2026-08-27  
**Target Profile:** `Movies 2160p AV1 HQ` (Profile 64, Read-Only)  
**Total Movies Audited:** 79  
**Operational Status:** **STRICTLY READ-ONLY CENSUS** — Output represents an empirical review queue, not an automated action.

---

## 1. Classification Summary (Scoring Repaired & Verdict-Anchored)

| Classification | Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **`HOLD`** | **62** | 78.5% | Current library file is already optimal, top-scoring 2160p, or anchored by empirical PASS verdict. |
| **`UPGRADE-CANDIDATE`** | **6** | 7.6% | Qualified candidate materially advances playback quality (res upgrade to 2160p, AV1 codec advancement, or legacy trusted x264). |
| **`MANUAL-REVIEW`** | **3** | 3.8% | Significant score delta within 2160p requiring manual verification of audio channels/bitrate parity. |
| **`NO-QUALIFIED-CANDIDATE`** | **8** | 10.1% | No candidate cleared the +1000 minimum profile cutoff score. |
| **Total** | **79** | **100.0%** | Full active Radarr4k library inventory. |

---

## 2. Top Ranked Priority Upgrade Queue

| Rank | Title | Year | Current File (Group / Codec / Res / Score) | Best Candidate (Group / Codec / Res / Score) | Delta | Material Advancement Rationale |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| 1 | **The Hunt** | 2012 | `KIMJI` (AV1, 1080p, 1450 pts) | `KIMJI` (AV1, 1080p, 4250 pts, 3.59GB) | **+2800** | 1080p tier upgrade to KIMJI AV1 (4250 pts, +2800 delta). |
| 2 | **X-Men Origins: Wolverine** | 2009 | `ChopperHitler` (AV1, 1080p, 2100 pts) | `ChopperHitler` (AV1, 1080p, 4900 pts, 3.73GB) | **+2800** | 1080p tier upgrade to ChopperHitler AV1 (4900 pts, +2800 delta). |
| 3 | **The Perks of Being a Wallflower** | 2012 | `PiRaTeS` (h264, 1080p, -1400 pts) | `playHD` (x264, 1080p, 1250 pts, 17.11GB) | **+2650** | Legacy trusted x264/1080p upgrade: playHD (1250 pts) lifts archival film above cutoff. |
| 4 | **The Wolverine** | 2013 | `R` (AV1, 2160p, 2050 pts) | `R&H` (AV1, 2160p, 2550 pts, 5.89GB) | **+500** | Higher scoring 2160p candidate (R&H AV1, +500 delta). |
| 5 | **Melancholia** | 2011 | `HONE` (h265, 1080p, 950 pts) | `playHD` (x264, 1080p, 1300 pts, 18.37GB) | **+350** | Legacy trusted x264/1080p upgrade: playHD (1300 pts) lifts archival film above cutoff. |
| 6 | **City of God** | 2002 | `DarQ` (x265, 1080p, 900 pts) | `Z0N3` (x264, 1080p, 1150 pts, 14.79GB) | **+250** | Legacy trusted x264/1080p upgrade: Z0N3 (1150 pts) lifts archival film above cutoff. |

---

## 3. Dedicated Review: Legacy Trusted x264 Titles

| Movie Title | Year | Current Group & Codec | Legacy Trusted Candidate | Score Before $\rightarrow$ After | Status & Operational Impact |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **Blue Valentine** | 2010 | `CtrlHD` (x264) | `CtrlHD` (13.62 GB) | `+1150` $\rightarrow$ `+1150` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **The Right Stuff** | 1983 | `BHDStudio` (x264) | `BHDStudio` (13.12 GB) | `+1250` $\rightarrow$ `+1250` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **Hoosiers** | 1986 | `PiRaTeS` (h264) | `None` (0 GB) | `+-1400` $\rightarrow$ `+-1400` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **The Perks of Being a Wallflower** | 2012 | `PiRaTeS` (h264) | `playHD` (17.11 GB) | `+-1400` $\rightarrow$ `+1250` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **Project X** | 2012 | `CtrlHD` (x264) | `DON` (11.46 GB) | `+1150` $\rightarrow$ `+1350` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **The Ides of March** | 2011 | `D-Z0N3` (x264) | `DON` (17.5 GB) | `+1150` $\rightarrow$ `+1250` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **Locke** | 2014 | `LoRD` (x264) | `LoRD` (11.67 GB) | `+1300` $\rightarrow$ `+1300` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |
| **A Royal Affair** | 2012 | `MrTentsaw` (x265) | `MrTentsaw` (16.06 GB) | `+1000` $\rightarrow$ `+1000` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |

---

## 4. Complete Library Catalog Census Breakdown (v2.1 Repaired)

| Title | Year | Current Summary | Best 2160p Candidate | Best 1080p Candidate | Status | Decision Rationale |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- |
| **Predator: Badlands** | 2025 | RandH (AV1, 2160p, 11.41GB, 5450 pts) | RandH (AV1, 12.38GB, 5450 pts) | WOTT (AV1, 5.67GB, 4200 pts) | **`HOLD`** | Current 2160p file 'RandH' (5450 pts) equals or outperforms all indexed 2160p candidates. |
| **Blade Runner** | 1982 | hallowed (x265, 2160p, 13.82GB, 2150 pts) | hallowed (x265, 15.69GB, 2150 pts) | WhiskeyJack (AV1, 6.71GB, 4250 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **The Shawshank Redemption** | 1994 | Smokindevil (AV1, 2160p, 5.05GB, 3150 pts) | Smokindevil (AV1, 5.75GB, 2550 pts) | SA89 (x265, 28.33GB, 1900 pts) | **`HOLD`** | Current 2160p file 'Smokindevil' (3150 pts) equals or outperforms all indexed 2160p candidates. |
| **Sisu** | 2022 | CMRG (h265, 2160p, 9.95GB, 1900 pts) | CMRG (x265, 11.3GB, 1800 pts) | WOTT (AV1, 4.51GB, 4200 pts) | **`HOLD`** | Current 2160p file 'CMRG' (1900 pts) equals or outperforms all indexed 2160p candidates. |
| **Die My Love** | 2025 | hallowed (x265, 2160p, 15.51GB, 1650 pts) | hallowed (x265, 19.2GB, 1650 pts) | REBORN (x265, 15.38GB, 1800 pts) | **`HOLD`** | Current 2160p file 'hallowed' (1650 pts) equals or outperforms all indexed 2160p candidates. |
| **Sisu: Road to Revenge** | 2025 | HONE (h265, 2160p, 15.82GB, 2450 pts) |  (x265, 17.16GB, 2450 pts) | anomoomin (AV1, 5.56GB, 4250 pts) | **`HOLD`** | Current 2160p file 'HONE' (2450 pts) equals or outperforms all indexed 2160p candidates. |
| **City of God** | 2002 | DarQ (x265, 1080p, 7.47GB, 900 pts) | *None* | Z0N3 (x264, 14.79GB, 1150 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: Z0N3 (1150 pts) lifts archival film above cutoff. |
| **Gladiator** | 2000 | RandH (AV1, 2160p, 11.88GB, 5300 pts) | UH (AV1, 14.1GB, 5450 pts) | REBORN (x265, 24.18GB, 2400 pts) | **`HOLD`** | Best 2160p candidate 'UH' delta (+150) is below the +300 upgrade increment threshold. |
| **Akira** | 1988 | BHDStudio (x265, 2160p, 14.36GB, 1500 pts) | BHDStudio (x265, 14.82GB, 1500 pts) | TiZU (AV1, 8.14GB, 5450 pts) | **`HOLD`** | Current 2160p file 'BHDStudio' (1500 pts) equals or outperforms all indexed 2160p candidates. |
| **2001: A Space Odyssey** | 1968 | hallowed (x265, 2160p, 17.37GB, 2250 pts) | hallowed (x265, 19.68GB, 2250 pts) | dAV1nci (AV1, 4.52GB, 4650 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2250 pts) equals or outperforms all indexed 2160p candidates. |
| **The Sixth Sense** | 1999 | Smokindevil (AV1, 2160p, 13.99GB, 5350 pts) | Smokindevil (AV1, 14.43GB, 5350 pts) | DON (x264, 14.98GB, 1250 pts) | **`HOLD`** | Current 2160p file 'Smokindevil' (5350 pts) equals or outperforms all indexed 2160p candidates. |
| **The Ides of March** | 2011 | D-Z0N3 (x264, 1080p, 13.08GB, 1150 pts) | *None* | DON (x264, 17.5GB, 1250 pts) | **`HOLD`** | Current 1080p file 'D-Z0N3' (1150 pts) equals or outperforms indexed 1080p candidates. |
| **The Place Beyond the Pines** | 2013 | hallowed (x265, 2160p, 18.35GB, 2150 pts) | hallowed (x265, 20.81GB, 2150 pts) | HiDt (x265, 21.43GB, 2300 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **La La Land** | 2016 | hallowed (x265, 2160p, 15.07GB, 2150 pts) | hallowed (x265, 17.06GB, 2150 pts) | Saon (AV1, 3.91GB, 4150 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **Blue Valentine** | 2010 | CtrlHD (x264, 1080p, 12.54GB, 1150 pts) | *None* | CtrlHD (x264, 13.62GB, 1150 pts) | **`HOLD`** | Current 1080p file 'CtrlHD' (1150 pts) equals or outperforms indexed 1080p candidates. |
| **Hoosiers** | 1986 | PiRaTeS (h264, 1080p, 11.88GB, -1400 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Easy A** | 2010 | onlyfaffs (AV1, 1080p, 2.66GB, 1450 pts) | *None* | onlyfaffs (AV1, 3.04GB, 1450 pts) | **`HOLD`** | Current 1080p file 'onlyfaffs' (1450 pts) equals or outperforms indexed 1080p candidates. |
| **The Drama** | 2026 | hallowed (x265, 2160p, 14.09GB, 2300 pts) | BYNDR (x265, 21.43GB, 2350 pts) | playHD (x264, 20.16GB, 1300 pts) | **`HOLD`** | Best 2160p candidate 'BYNDR' delta (+50) is below the +300 upgrade increment threshold. |
| **Johnny English** | 2003 | BLUTONiUM (HEVC, 2160p, 16.32GB, 2100 pts) | BLUTONiUM (x265, 17.7GB, 2000 pts) | Saon (AV1, 5.31GB, 4150 pts) | **`HOLD`** | Current 2160p file 'BLUTONiUM' (2100 pts) equals or outperforms all indexed 2160p candidates. |
| **The Right Stuff** | 1983 | BHDStudio (x264, 1080p, 11.55GB, 1250 pts) | *None* | BHDStudio (x264, 13.12GB, 1250 pts) | **`HOLD`** | Current 1080p file 'BHDStudio' (1250 pts) equals or outperforms indexed 1080p candidates. |
| **Magic Mike** | 2012 | FLUX (h265, 2160p, 21.63GB, 2150 pts) | FLUX (x265, 24.56GB, 2150 pts) | playHD (x264, 13.19GB, 1300 pts) | **`HOLD`** | Current 2160p file 'FLUX' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **The Lord of the Rings: The Fellowship of the Ring** | 2001 | CoSMiCSuRFeR (AV1, 2160p, 30.91GB, 5950 pts) | CoSMiCSuRFeR (AV1, 32.52GB, 5950 pts) | UH (AV1, 10.82GB, 4750 pts) | **`HOLD`** | Current 2160p file 'CoSMiCSuRFeR' (5950 pts) equals or outperforms all indexed 2160p candidates. |
| **Robin Hood** | 2010 | ZAX (x265, 2160p, 27.58GB, -850 pts) | *None* | Z0N3 (x264, 19.96GB, 1150 pts) | **`NO-QUALIFIED-CANDIDATE`** | No 2160p candidate cleared the +1000 minimum profile cutoff score. |
| **Fury** | 2014 | Smokindevil (AV1, 2160p, 9.9GB, 2550 pts) | Smokindevil (AV1, 11.24GB, 5950 pts) | HiDt (x265, 22.71GB, 2300 pts) | **`MANUAL-REVIEW`** | Significant score delta (+3400 pts) within 2160p — verify audio track and bitrate parity (Smokindevil vs Smokindevil). |
| **F1** | 2025 | R (AV1, 2160p, 13.04GB, 5550 pts) | R and H (AV1, 14.78GB, 5550 pts) | onlyfaffs (AV1, 4.54GB, 4250 pts) | **`HOLD`** | Current 2160p file 'R' (5550 pts) equals or outperforms all indexed 2160p candidates. |
| **The Deer Hunter** | 1978 | R (AV1, 2160p, 10.75GB, 1450 pts) | R and H (AV1, 12.18GB, 4850 pts) | LoRD (x264, 30.4GB, 1300 pts) | **`MANUAL-REVIEW`** | Significant score delta (+3400 pts) within 2160p — verify audio track and bitrate parity (R vs R and H). |
| **Batman: Mask of the Phantasm** | 1993 | BHDStudio (x265, 2160p, 8.89GB, 2100 pts) | BHDStudio (x265, 10.1GB, 2100 pts) | TiZU (AV1, 7.89GB, 4150 pts) | **`HOLD`** | Current 2160p file 'BHDStudio' (2100 pts) equals or outperforms all indexed 2160p candidates. |
| **The Black Cauldron** | 1985 | TiZU (AV1, 1080p, 5.23GB, 4150 pts) | *None* | TiZU (AV1, 5.94GB, 4150 pts) | **`HOLD`** | Current 1080p file 'TiZU' (4150 pts) equals or outperforms indexed 1080p candidates. |
| **The Da Vinci Code** | 2006 | hallowed (x265, 2160p, 23.33GB, 2300 pts) | hallowed (x265, 24.48GB, 2300 pts) | HiDt (x265, 26.29GB, 2300 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2300 pts) equals or outperforms all indexed 2160p candidates. |
| **X-Men: First Class** | 2011 | BHDStudio (x265, 2160p, 15.14GB, 1500 pts) | hallowed (x265, 18.66GB, 1550 pts) | Z0N3 (x264, 18.76GB, 1150 pts) | **`HOLD`** | Best 2160p candidate 'hallowed' delta (+50) is below the +300 upgrade increment threshold. |
| **Dark Phoenix** | 2019 | ChopperHitler (AV1, 2160p, 5.89GB, 2500 pts) | ChopperHitler (AV1, 6.38GB, 1900 pts) | SA89 (x265, 16.17GB, 1700 pts) | **`HOLD`** | Current 2160p file 'ChopperHitler' (2500 pts) equals or outperforms all indexed 2160p candidates. |
| **X-Men** | 2000 | ChopperHitler (AV1, 2160p, 12.79GB, 5300 pts) | ChopperHitler (AV1, 14.52GB, 4900 pts) | playHD (x264, 13.32GB, 1300 pts) | **`HOLD`** | Current 2160p file 'ChopperHitler' (5300 pts) equals or outperforms all indexed 2160p candidates. |
| **X-Men: The Last Stand** | 2006 | hallowed (x265, 2160p, 13.62GB, 1550 pts) | hallowed (x265, 15.47GB, 1550 pts) | DON (x264, 18.31GB, 1250 pts) | **`HOLD`** | Current 2160p file 'hallowed' (1550 pts) equals or outperforms all indexed 2160p candidates. |
| **X2** | 2003 | BHDStudio (x265, 2160p, 15.3GB, 1500 pts) | hallowed (x265, 18.96GB, 1550 pts) | DON (x264, 16.16GB, 1250 pts) | **`HOLD`** | Best 2160p candidate 'hallowed' delta (+50) is below the +300 upgrade increment threshold. |
| **X-Men: Apocalypse** | 2016 | ChopperHitler (AV1, 2160p, 11.69GB, 5300 pts) | ChopperHitler (AV1, 12.67GB, 5300 pts) | Unknown (AV1, 8.72GB, 4200 pts) | **`HOLD`** | Current 2160p file 'ChopperHitler' (5300 pts) equals or outperforms all indexed 2160p candidates. |
| **X-Men: Days of Future Past** | 2014 | ChopperHitler (AV1, 2160p, 11.96GB, 5300 pts) | ChopperHitler (AV1, 13.58GB, 5300 pts) | KIMJI (AV1, 5.15GB, 4250 pts) | **`HOLD`** | Current 2160p file 'ChopperHitler' (5300 pts) equals or outperforms all indexed 2160p candidates. |
| **72 HOURS** | 2026 | FLUX (h265, 2160p, 14.38GB, 2450 pts) | FLUX (x265, 16.34GB, 2450 pts) | *None* | **`HOLD`** | Current 2160p file 'FLUX' (2450 pts) equals or outperforms all indexed 2160p candidates. |
| **Yi Yi** | 2000 | BHDStudio (x264, 1080p, 10.16GB, 1250 pts) | *None* | BHDStudio (x264, 14.25GB, 1250 pts) | **`HOLD`** | Current 1080p file 'BHDStudio' (1250 pts) equals or outperforms indexed 1080p candidates. |
| **Spider-Man: Brand New Day** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Cast Away** | 2000 | onlyfaffs (AV1, 1080p, 3.89GB, 4250 pts) | *None* | anomoomin (AV1, 6.76GB, 4250 pts) | **`HOLD`** | Current 1080p file 'onlyfaffs' (4250 pts) equals or outperforms indexed 1080p candidates. |
| **The Grand Budapest Hotel** | 2014 | hallowed (x265, 2160p, 13.1GB, 2150 pts) | hallowed (x265, 14.88GB, 2150 pts) | HiDt (x265, 14.5GB, 2150 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **The Perks of Being a Wallflower** | 2012 | PiRaTeS (h264, 1080p, 10.52GB, -1400 pts) | *None* | playHD (x264, 17.11GB, 1250 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: playHD (1250 pts) lifts archival film above cutoff. |
| **The Outsiders** | 1983 | c0kE (x265, 1080p, 21.26GB, 2200 pts) | *None* | c0kE (x265, 24.15GB, 2200 pts) | **`HOLD`** | Current 1080p file 'c0kE' (2200 pts) equals or outperforms indexed 1080p candidates. |
| **Apocalypse Now** | 1979 | R (AV1, 2160p, 12.72GB, 4700 pts) | R&H (AV1, 13.4GB, 4700 pts) | RAV1NE (AV1, 4.22GB, 4250 pts) | **`HOLD`** | Current 2160p file 'R' (4700 pts) equals or outperforms all indexed 2160p candidates. |
| **The End of Oak Street** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Melancholia** | 2011 | HONE (h265, 1080p, 4.18GB, 950 pts) | *None* | playHD (x264, 18.37GB, 1300 pts) | **`UPGRADE-CANDIDATE`** | Legacy trusted x264/1080p upgrade: playHD (1300 pts) lifts archival film above cutoff. |
| **Locke** | 2014 | LoRD (x264, 1080p, 10.28GB, 1300 pts) | *None* | LoRD (x264, 11.67GB, 1300 pts) | **`HOLD`** | Current 1080p file 'LoRD' (1300 pts) equals or outperforms indexed 1080p candidates. |
| **Ghost in the Shell** | 1995 | hallowed (x265, 2160p, 9.34GB, 2300 pts) | hallowed (x265, 10.61GB, 2300 pts) | *None* | **`HOLD`** | Current 2160p file 'hallowed' (2300 pts) equals or outperforms all indexed 2160p candidates. |
| **Greenland** | 2020 | hallowed (x265, 2160p, 15.93GB, 1700 pts) | hallowed (x265, 19.73GB, 1700 pts) | LoRD (x264, 17.93GB, 1300 pts) | **`HOLD`** | Current 2160p file 'hallowed' (1700 pts) equals or outperforms all indexed 2160p candidates. |
| **Greenland 2: Migration** | 2026 | hallowed (x265, 2160p, 13.05GB, 1700 pts) | hallowed (x265, 16.16GB, 1700 pts) | WOTT (AV1, 5.35GB, 4800 pts) | **`HOLD`** | Current 2160p file 'hallowed' (1700 pts) equals or outperforms all indexed 2160p candidates. |
| **Blackhat** | 2015 | 2160p][DV HDR10][EAC3 5.1] (x265, 2160p, 22.24GB, -550 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p candidate cleared the +1000 minimum profile cutoff score. |
| **Extraction 2** | 2023 | FLUX (h265, 2160p, 17.09GB, 2450 pts) | FLUX (x265, 19.11GB, 2450 pts) | BTT (AV1, 4.33GB, 3800 pts) | **`HOLD`** | Current 2160p file 'FLUX' (2450 pts) equals or outperforms all indexed 2160p candidates. |
| **The Rip** | 2026 | FLUX (h265, 2160p, 15.25GB, 2450 pts) | FLUX (x265, 16.12GB, 2450 pts) | WOTT (AV1, 5.37GB, 4200 pts) | **`HOLD`** | Current 2160p file 'FLUX' (2450 pts) equals or outperforms all indexed 2160p candidates. |
| **The Hunt** | 2012 | KIMJI (AV1, 1080p, 3.37GB, 1450 pts) | *None* | KIMJI (AV1, 3.59GB, 4250 pts) | **`UPGRADE-CANDIDATE`** | 1080p tier upgrade to KIMJI AV1 (4250 pts, +2800 delta). |
| **Riders of Justice** | 2020 | LoRD (x264, 1080p, 10.55GB, 1300 pts) | *None* | LoRD (x264, 11.99GB, 1300 pts) | **`HOLD`** | Current 1080p file 'LoRD' (1300 pts) equals or outperforms indexed 1080p candidates. |
| **Interstellar** | 2014 | RandH (AV1, 2160p, 16.59GB, 5300 pts) | RandH (AV1, 18.81GB, 5300 pts) | onlyfaffs (AV1, 3.82GB, 4250 pts) | **`HOLD`** | Current 2160p file 'RandH' (5300 pts) equals or outperforms all indexed 2160p candidates. |
| **The Wolverine** | 2013 | R (AV1, 2160p, 5.55GB, 2050 pts) | R&H (AV1, 5.89GB, 2550 pts) | ChopperHitler (AV1, 4.73GB, 4900 pts) | **`UPGRADE-CANDIDATE`** | Higher scoring 2160p candidate (R&H AV1, +500 delta). |
| **X-Men Origins: Wolverine** | 2009 | ChopperHitler (AV1, 1080p, 3.44GB, 2100 pts) | *None* | ChopperHitler (AV1, 3.73GB, 4900 pts) | **`UPGRADE-CANDIDATE`** | 1080p tier upgrade to ChopperHitler AV1 (4900 pts, +2800 delta). |
| **Logan** | 2017 | HONE (h265, 2160p, 16.59GB, 2400 pts) | HONE) (x265, 17.97GB, 2400 pts) | DON (x264, 13.53GB, 1350 pts) | **`HOLD`** | Current 2160p file 'HONE' (2400 pts) equals or outperforms all indexed 2160p candidates. |
| **Jack Reacher** | 2012 | RandH (AV1, 2160p, 12.34GB, 5300 pts) | RandH (AV1, 14.01GB, 5300 pts) | WOTT (AV1, 6.46GB, 4200 pts) | **`HOLD`** | Current 2160p file 'RandH' (5300 pts) equals or outperforms all indexed 2160p candidates. |
| **True Grit** | 2010 | WhiskeyJack (AV1, 1080p, 4.45GB, 4250 pts) | *None* | WhiskeyJack (AV1, 5.05GB, 4250 pts) | **`HOLD`** | Current 1080p file 'WhiskeyJack' (4250 pts) equals or outperforms indexed 1080p candidates. |
| **The Bourne Supremacy** | 2004 | MainFrame (x265, 2160p, 21.59GB, 2200 pts) | BYNDR (x265, 24.21GB, 2200 pts) | WhiskeyJack (AV1, 4.2GB, 4250 pts) | **`HOLD`** | Current 2160p file 'MainFrame' (2200 pts) equals or outperforms all indexed 2160p candidates. |
| **The Bourne Ultimatum** | 2007 | Bi0hazard (AV1, 2160p, 17.41GB, 3600 pts) | Bi0hazard (AV1, 18.89GB, 3600 pts) | UH (AV1, 3.74GB, 4750 pts) | **`HOLD`** | Current 2160p file 'Bi0hazard' (3600 pts) equals or outperforms all indexed 2160p candidates. |
| **The Lord of the Rings: The Return of the King** | 2003 | CoSMiCSuRFeR (AV1, 2160p, 41.34GB, 5950 pts) | CoSMiCSuRFeR (AV1, 43.4GB, 5950 pts) | UH (AV1, 16.52GB, 4750 pts) | **`HOLD`** | Current 2160p file 'CoSMiCSuRFeR' (5950 pts) equals or outperforms all indexed 2160p candidates. |
| **The Lord of the Rings: The Two Towers** | 2002 | CoSMiCSuRFeR (AV1, 2160p, 29.93GB, 5950 pts) | dAV1nci (AV1, 11.82GB, 5500 pts) | dAV1nci (AV1, 6.66GB, 4650 pts) | **`HOLD`** | Current 2160p file 'CoSMiCSuRFeR' (5950 pts) equals or outperforms all indexed 2160p candidates. |
| **Moana** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **John Wick** | 2014 | Rob74K (AV1, 2160p, 12.9GB, 4950 pts) | Rob74K (AV1, 14.0GB, 4950 pts) | TiFou (AV1, 6.81GB, 4300 pts) | **`HOLD`** | Current 2160p file 'Rob74K' (4950 pts) equals or outperforms all indexed 2160p candidates. |
| **John Wick: Chapter 3 - Parabellum** | 2019 | AV1-CoSMiCSuRFeR (AV1, 2160p, 34.52GB, 5950 pts) | CoSMiCSuRFeR (AV1, 36.28GB, 5950 pts) | HiDt (x265, 19.56GB, 2300 pts) | **`HOLD`** | Current 2160p file 'AV1-CoSMiCSuRFeR' (5950 pts) equals or outperforms all indexed 2160p candidates. |
| **John Wick: Chapter 2** | 2017 | Rob74K (AV1, 2160p, 12.65GB, 4350 pts) | Rob74K (AV1, 13.73GB, 3650 pts) | CtrlHD (x265, 16.25GB, 1600 pts) | **`HOLD`** | Current 2160p file 'Rob74K' (4350 pts) equals or outperforms all indexed 2160p candidates. |
| **John Wick: Chapter 4** | 2023 | CoSMiCSuRFeR (AV1, 2160p, 17.76GB, 5950 pts) | CoSMiCSuRFeR (AV1, 18.74GB, 5950 pts) | dAV1nci (AV1, 4.61GB, 4500 pts) | **`HOLD`** | Current 2160p file 'CoSMiCSuRFeR' (5950 pts) equals or outperforms all indexed 2160p candidates. |
| **A Royal Affair** | 2012 | MrTentsaw (x265, 1080p, 14.14GB, 1000 pts) | *None* | MrTentsaw (x265, 16.06GB, 1000 pts) | **`HOLD`** | Current 1080p file 'MrTentsaw' (1000 pts) equals or outperforms indexed 1080p candidates. |
| **Mutiny** | 2026 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
| **Jurassic Park** | 1993 | Smokindevil (AV1, 2160p, 10.89GB, 1950 pts) | Smokindevil (AV1, 12.32GB, 5350 pts) | FELIX12345 (AV1, 6.41GB, 2800 pts) | **`MANUAL-REVIEW`** | Significant score delta (+3400 pts) within 2160p — verify audio track and bitrate parity (Smokindevil vs Smokindevil). |
| **The Lost World: Jurassic Park** | 1997 | BHDStudio (x265, 2160p, 15.08GB, 2150 pts) | hallowed (x265, 19.19GB, 2150 pts) | FELIX12345 (AV1, 6.57GB, 2800 pts) | **`HOLD`** | Current 2160p file 'BHDStudio' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **Jurassic World: Fallen Kingdom** | 2018 | HHWEB (HEVC, 2160p, 22.16GB, 2400 pts) | HHWEB (x265, 24.01GB, 2300 pts) | LoRD (x264, 11.0GB, 1300 pts) | **`HOLD`** | Current 2160p file 'HHWEB' (2400 pts) equals or outperforms all indexed 2160p candidates. |
| **Jurassic World** | 2015 | hallowed (x265, 2160p, 16.38GB, 2150 pts) | hallowed (x265, 18.54GB, 2150 pts) | onlyfaffs (AV1, 5.68GB, 4250 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **Jurassic Park III** | 2001 | hallowed (x265, 2160p, 12.13GB, 2150 pts) | hallowed (x265, 13.77GB, 2150 pts) | FELIX12345 (AV1, 4.72GB, 2800 pts) | **`HOLD`** | Current 2160p file 'hallowed' (2150 pts) equals or outperforms all indexed 2160p candidates. |
| **Project X** | 2012 | CtrlHD (x264, 1080p, 10.97GB, 1150 pts) | *None* | DON (x264, 11.46GB, 1350 pts) | **`HOLD`** | Current 1080p file 'CtrlHD' (1150 pts) equals or outperforms indexed 1080p candidates. |
| **Caroline - den sidste rejse** | 2012 | None (None, None, 0.0GB, 0 pts) | *None* | *None* | **`NO-QUALIFIED-CANDIDATE`** | No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts). |
