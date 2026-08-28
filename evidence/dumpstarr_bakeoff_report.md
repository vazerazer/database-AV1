# 📊 OP 934: Dumpstarr 2160p Bake-Off Comparative Simulation Report
**Date of Audit:** 2026-08-28  
**Upstream Target:** Dumpstarr Database (`https://github.com/Dumpstarr/Database`)  
**Upstream Commit:** `96ae7394a52e8671ffbce4620d103b82f08129a5` (2026-08-26T23:58:41Z)  
**PCD Target Profile:** `Movies 2160p AV1 HQ` (Profile 64)  
**Dumpstarr Target Profile:** `Movies 2160p` (Profile ID 5)  
**Scope:** 75 Live Library Titles (Full Simulation, Read-Only, 0 Live Edits)  

---

## 1. Executive Summary & Core Architectural Divergence

### Key Philosophy Delta:
1. **AV1 Codec Stance:**
   * **PCD Profile 64:** Prioritizes next-generation AV1 (`AV1` +3500) with evidence-earned quality/compact tiers (+500 to +1000) and sizing bands (-2800 to -3400).
   * **Dumpstarr 2160p:** Explicitly hard-bans AV1 (`AV1` **-10000**) to protect legacy streaming hardware lacking AV1 HW decoders.
2. **HD Lossless Audio Stance:**
   * **PCD Profile 64:** Encourages lossless audio passthrough (`TrueHD` +150, `DTS-X` +150, `Lossless Audio` +100, `Opus 5.1/7.1` +250).
   * **Dumpstarr 2160p:** Explicitly hard-bans HD audio (`TrueHD` **-10000**, `DTS-HD MA` **-10000**, `DTS-X` **-10000**) to avoid CPU transcoding on low-end clients.
3. **Ladder vs Additive Point Stacking:**
   * **PCD Profile 64:** Strict 6-band discrete quality ladder with +1000 cutoff barrier.
   * **Dumpstarr 2160p:** Additive source tiers (+1400-1900) with extensive micro-tag stacking (repacks +5-7, services +10-75, editions +25-125).

---

## 2. Group Steal List Analysis

| Category | Dumpstarr Groups | PCD Status | Op 935 Action / Recommendation |
| :--- | :--- | :--- | :--- |
| **2160p x265 Fallback** | `CtrlHD`, `MainFrame`, `DON`, `W4NK3R`, `HiDt`, `HQMUX`, `RandomBytes`, `BHDStudio`, `hallowed`, `HONE`, `PTer`, `SPHD`, `WEBDV` | All 12 physical groups in PCD (Tier 1-4 / Balanced). Only `WEBDV` missing. | Maintain. Exclude WEB-only `WEBDV` from BluRay rungs. |
| **Legacy x264 Trust** | 39 HD Bluray Tier 01-03 groups (`CtrlHD`, `DON`, `EbP`, `c0kE`, `SA89`, `ATELiER`, `D-Z0N3`, etc.) | **100% Unioned** in PCD `LEGACY_TRUSTED_X264` (Op 933). `HONE` excluded (x265). | 100% Complete. No missing physical BluRay reference groups. |
| **WEB-DL Tiers** | ~50 groups (`SiGMA`, `JETIX`, `CEBEX`, `RTN`, `SDCC`, `GNOME`, `CRUD`, `DRACULA`, `PHOENiX`, `PSiG`, `DEEP`, `orbitron`, `APEX`, `BLOOM`, `KiNGS`, `ETHiCS`, `Cinefeel`, `ViSUM`, `XEPA`, `MiU`, `PEXA`) | Core groups present (`HONE`, `CMRG`, `BYNDR`, `playWEB`, `Kitsune`, `TEPES`, +11 legacy groups). | Candidate menu for Op 935 WEB-DL tier expansion. |

---

## 3. Custom Format Gap Report (Menu Assessment)

The following Custom Formats are scored in Dumpstarr 2160p but unscored in PCD Profile 64:

1. **Streaming Source Branding:**
   * `MA` (+75), `CRIT` (+50), `DSNP` (+50), `iT` (+50), `ATVP` (+25), `BCORE` (+25), `HMAX` (+25), `MAX` (+25), `AMZN` (+10), `NF` (+10).
   * *Assessment:* In PCD, service tags carry clean +50 bonuses (AMZN, DSNP, MAX, HULU). No ranking inversions observed.
2. **Edition & Remaster Tags:**
   * `Special Edition` (+125), `4K Remaster` (+25), `Remaster` (+25).
   * *Assessment:* PCD scores `Theatrical` (+100) and `CRIT` (+100). Harmless micro-bonuses.
3. **Repack & Proper Integrity:**
   * `Repack3` (+7), `Repack2` (+6), `Repack1` (+5), `Proper` (+5).
   * *Assessment:* Recommended adoption in Op 935 to resolve identical-release repack grabs deterministically without disturbing tier point bands.

---

## 4. 81-Title Full Comparative Simulation Table

| Title | Year | Codec | Size (GB) | PCD Profile 64 Score | Dumpstarr Score | Delta | Key Scoring Drivers / Discrepancy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2001: A Space Odyssey** | 1968 | x265 | 17.37 | 2250 | -8270 | +10520 | Source Tier & Tag Stacking |
| **72 HOURS** | 2026 | x265 | 14.38 | 2450 | -8345 | +10795 | Source Tier & Tag Stacking |
| **A Royal Affair** | 2012 | x265 | 14.14 | 1000 | -9995 | +10995 | Source Tier & Tag Stacking |
| **Akira** | 1988 | x265 | 14.36 | 1500 | 620 |   +880 | Source Tier & Tag Stacking |
| **Apocalypse Now** | 1979 | AV1 | 12.72 | 4700 | -19370 | +24070 | Dumpstarr AV1 Ban (-10000) |
| **Batman: Mask of the Phantasm** | 1993 | x265 | 8.89 | 2100 | -8380 | +10480 | Source Tier & Tag Stacking |
| **Blackhat** | 2015 | x265 | 19.28 | -550 | -18500 | +17950 | Source Tier & Tag Stacking |
| **Blade Runner** | 1982 | x265 | 13.82 | 2150 | -8240 | +10390 | Source Tier & Tag Stacking |
| **Blue Valentine** | 2010 | x264 | 12.54 | 1150 | 0 |  +1150 | PCD Legacy Trust (+5400) |
| **Cast Away** | 2000 | AV1 | 3.89 | 4250 | -19995 | +24245 | Dumpstarr AV1 Ban (-10000) |
| **City of God** | 2002 | x264 | 13.09 | 1150 | 0 |  +1150 | PCD Legacy Trust (+5400) |
| **Dark Phoenix** | 2019 | AV1 | 5.89 | 2500 | -9380 | +11880 | Dumpstarr AV1 Ban (-10000) |
| **Die My Love** | 2025 | x265 | 15.51 | 1650 | -9270 | +10920 | Source Tier & Tag Stacking |
| **Easy A** | 2010 | AV1 | 2.66 | 1450 | -19995 | +21445 | Dumpstarr AV1 Ban (-10000) |
| **Extraction 2** | 2023 | x265 | 17.09 | 2450 | -8345 | +10795 | Source Tier & Tag Stacking |
| **F1** | 2025 | AV1 | 13.04 | 5550 | -28365 | +33915 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **Fury** | 2014 | AV1 | 9.9 | 2550 | -28465 | +31015 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **Ghost in the Shell** | 1995 | x265 | 9.34 | 2300 | -8340 | +10640 | Source Tier & Tag Stacking |
| **Gladiator** | 2000 | AV1 | 11.88 | 5300 | -18370 | +23670 | Dumpstarr AV1 Ban (-10000) |
| **Grand Theft Auto VI: An Extended Look** | 2026 | x265 | 2.36 | 1000 | 255 |   +745 | Source Tier & Tag Stacking |
| **Greenland** | 2020 | x265 | 15.93 | 1700 | 655 |  +1045 | Source Tier & Tag Stacking |
| **Greenland 2: Migration** | 2026 | x265 | 13.05 | 1700 | 655 |  +1045 | Source Tier & Tag Stacking |
| **Hoosiers** | 1986 | x264 | 11.88 | 1350 | 130 |  +1220 | PCD Legacy Trust (+5400) |
| **Interstellar** | 2014 | AV1 | 16.59 | 5300 | -28495 | +33795 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **Jack Reacher** | 2012 | AV1 | 12.34 | 5300 | -28490 | +33790 | Dumpstarr AV1 Ban (-10000) |
| **John Wick** | 2014 | AV1 | 12.9 | 4950 | -28465 | +33415 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **John Wick: Chapter 2** | 2017 | AV1 | 12.65 | 4350 | -19965 | +24315 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **John Wick: Chapter 3 - Parabellum** | 2019 | AV1 | 34.52 | 5950 | -28465 | +34415 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **John Wick: Chapter 4** | 2023 | AV1 | 17.76 | 5950 | -28465 | +34415 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **Johnny English** | 2003 | x265 | 16.32 | 2100 | -18445 | +20545 | Source Tier & Tag Stacking |
| **Jurassic Park** | 1993 | AV1 | 10.89 | 1950 | -9370 | +11320 | Dumpstarr AV1 Ban (-10000) |
| **Jurassic Park III** | 2001 | x265 | 12.13 | 2150 | -8360 | +10510 | Source Tier & Tag Stacking |
| **Jurassic World** | 2015 | x265 | 16.38 | 2150 | -8360 | +10510 | Source Tier & Tag Stacking |
| **Jurassic World: Fallen Kingdom** | 2018 | x265 | 22.16 | 2400 | -18295 | +20695 | Source Tier & Tag Stacking |
| **La La Land** | 2016 | x265 | 15.07 | 2150 | -8360 | +10510 | Source Tier & Tag Stacking |
| **Locke** | 2014 | x264 | 10.28 | 1300 | 130 |  +1170 | PCD Legacy Trust (+5400) |
| **Logan** | 2017 | Unknown | 16.59 | 2400 | -18345 | +20745 | Source Tier & Tag Stacking |
| **Magic Mike** | 2012 | Unknown | 21.63 | 2150 | -18420 | +20570 | Dumpstarr HD Audio Ban (-10000) |
| **Melancholia** | 2011 | x264 | 16.21 | 1300 | 130 |  +1170 | PCD Legacy Trust (+5400) |
| **Predator: Badlands** | 2025 | AV1 | 11.41 | 5450 | -28465 | +33915 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **Project X** | 2012 | x264 | 10.97 | 1150 | 0 |  +1150 | PCD Legacy Trust (+5400) |
| **Riders of Justice** | 2020 | x264 | 10.55 | 1300 | 130 |  +1170 | PCD Legacy Trust (+5400) |
| **Robin Hood** | 2010 | x265 | 27.58 | -850 | -8140 |  +7290 | Source Tier & Tag Stacking |
| **Sisu** | 2022 | x265 | 9.95 | 1900 | 655 |  +1245 | Source Tier & Tag Stacking |
| **Sisu: Road to Revenge** | 2025 | Unknown | 15.82 | 2450 | -18195 | +20645 | Source Tier & Tag Stacking |
| **The Black Cauldron** | 1985 | AV1 | 5.23 | 4150 | -19875 | +24025 | Dumpstarr AV1 Ban (-10000) |
| **The Bourne Supremacy** | 2004 | x265 | 21.59 | 2200 | -18490 | +20690 | Dumpstarr HD Audio Ban (-10000) |
| **The Bourne Ultimatum** | 2007 | AV1 | 17.41 | 3600 | -9375 | +12975 | Dumpstarr AV1 Ban (-10000) |
| **The Da Vinci Code** | 2006 | x265 | 23.33 | 2300 | -8220 | +10520 | Source Tier & Tag Stacking |
| **The Deer Hunter** | 1978 | AV1 | 10.75 | 1450 | -9370 | +10820 | Dumpstarr AV1 Ban (-10000) |
| **The Drama** | 2026 | x265 | 14.09 | 2300 | -8345 | +10645 | Source Tier & Tag Stacking |
| **The Grand Budapest Hotel** | 2014 | x265 | 13.1 | 2150 | -8370 | +10520 | Source Tier & Tag Stacking |
| **The Hunt** | 2012 | AV1 | 3.37 | 1450 | -19995 | +21445 | Dumpstarr AV1 Ban (-10000) |
| **The Ides of March** | 2011 | x264 | 13.08 | 1150 | 0 |  +1150 | PCD Legacy Trust (+5400) |
| **The Lord of the Rings: The Fellowship of the Ring** | 2001 | AV1 | 30.91 | 5950 | -28340 | +34290 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **The Lord of the Rings: The Return of the King** | 2003 | AV1 | 41.34 | 5950 | -28340 | +34290 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **The Lord of the Rings: The Two Towers** | 2002 | AV1 | 29.93 | 5950 | -28340 | +34290 | Dumpstarr AV1 Ban (-10000), Dumpstarr HD Audio Ban (-10000) |
| **The Lost World: Jurassic Park** | 1997 | x265 | 15.08 | 2150 | -8365 | +10515 | Source Tier & Tag Stacking |
| **The Outsiders** | 1983 | x265 | 21.26 | 2200 | -8370 | +10570 | Source Tier & Tag Stacking |
| **The Perks of Being a Wallflower** | 2012 | x264 | 15.12 | 1250 | 120 |  +1130 | PCD Legacy Trust (+5400) |
| **The Place Beyond the Pines** | 2013 | x265 | 18.35 | 2150 | -8370 | +10520 | Source Tier & Tag Stacking |
| **The Right Stuff** | 1983 | x264 | 11.55 | 1250 | 120 |  +1130 | PCD Legacy Trust (+5400) |
| **The Rip** | 2026 | Unknown | 15.25 | 2450 | -8345 | +10795 | Source Tier & Tag Stacking |
| **The Shawshank Redemption** | 1994 | AV1 | 5.05 | 3150 | -9370 | +12520 | Dumpstarr AV1 Ban (-10000) |
| **The Sixth Sense** | 1999 | AV1 | 13.99 | 5350 | -9370 | +14720 | Dumpstarr AV1 Ban (-10000) |
| **The Wolverine** | 2013 | AV1 | 5.55 | 2550 | -18495 | +21045 | Dumpstarr AV1 Ban (-10000) |
| **True Grit** | 2010 | AV1 | 4.45 | 4250 | -19995 | +24245 | Dumpstarr AV1 Ban (-10000) |
| **X-Men** | 2000 | AV1 | 12.79 | 5300 | -9885 | +15185 | Dumpstarr AV1 Ban (-10000) |
| **X-Men Origins: Wolverine** | 2009 | AV1 | 3.44 | 2100 | -9880 | +11980 | Dumpstarr AV1 Ban (-10000) |
| **X-Men: Apocalypse** | 2016 | AV1 | 11.69 | 5300 | -9380 | +14680 | Dumpstarr AV1 Ban (-10000) |
| **X-Men: Days of Future Past** | 2014 | AV1 | 11.96 | 5300 | -9385 | +14685 | Dumpstarr AV1 Ban (-10000) |
| **X-Men: First Class** | 2011 | x265 | 15.14 | 1500 | 620 |   +880 | Source Tier & Tag Stacking |
| **X-Men: The Last Stand** | 2006 | x265 | 13.62 | 1550 | 630 |   +920 | Source Tier & Tag Stacking |
| **X2** | 2003 | x265 | 15.3 | 1500 | 620 |   +880 | Source Tier & Tag Stacking |
| **Yi Yi** | 2000 | x264 | 10.16 | 1250 | 115 |  +1135 | PCD Legacy Trust (+5400) |

---

## 5. Recommendations for Op 935

1. **Adopt Repack / Proper Micro-Tiers (+5 to +7 pts):**
   * Integrates `Proper / Repack` micro-tiers (+5 / +6 / +7) to cleanly resolve indexer post-fix collisions without altering cutoff clearance.
2. **Expand WEB-DL Tiers with Vetted Streaming Groups:**
   * Expand `WEB-DL Tier 1-3` with vetted streaming scene/P2P groups (`FLUX`, `SiGMA`, `KiNGS`, `ETHiCS`, `Cinefeel`, `ViSUM`, `DEEP`) to strengthen transparent x265 WEB fallbacks.
3. **Preserve Strict AV1 & HD Audio Invariants:**
   * AV1 and lossless TrueHD/DTS-HD/Opus passthrough remain core pillars of PCD Architecture.