# OP 965A — Suspect Titles Artifact Screening Summary

- **Total Titles Screened:** 47
- **Artifact-Positive (Confirmed Upgrades):** 1 (2.1%)
- **Starved-But-Clean (Efficient / Clean Banding):** 46 (97.9%)
- **HDR/DoVi Profiles Screened:** 44 (93.6%)

## 1. Objective Screening Methodology
- **CAMBI (Contrast Aware Multiscale Banding Index):** Evaluated on the darkest 10s window discovered via luma analysis (`CAMBI <= 5.0` indicates clean gradient, `> 5.0` indicates visible color banding).
- **Blockdetect & Blurdetect:** Evaluated on 10s high-motion sequences (`block_mean > 0.05` triggers blockiness alert).
- **SEI Parameters:** Extracted via MediaInfo for encoder psycho-visual flags.

## 2. Complete Scorecard & Classification
| # | Movie | Year | Codec | Res | Size | BPP | Dynamic Range | CAMBI (Dark) | Block | Verdict | Settings |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | A Silent Voice | 2016 | AV1 | 1080p | 1.94 GB | **0.043** | `SDR` | 0.02 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 2 | Amadeus | 1984 | AV1 | 2160p | 11.41 GB | **0.0513** | `DV/HDR10` | 0.038 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 3 | Avengers-Endgame-2019-IMA | 0 | HEVC | 2160p | 17.34 GB | **0.0689** | `DV/HDR10` | 0.026 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 4 | Bu Liu Huo Kou | 2026 | HEVC | 2160p | 5.22 GB | **0.0549** | `HDR10` | 1.765 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 5 | Capernaum | 2018 | AV1 | 1080p | 1.43 GB | **0.0325** | `SDR` | 0.096 | 1.31 | **`ARTIFACT-POSITIVE`** | None |
| 6 | Casino | 1995 | HEVC | 2160p | 19.2 GB | **0.0776** | `HDR10` | 0.104 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=4.00 rc=abr bitrate=1 |
| 7 | Chinatown | 1974 | HEVC | 2160p | 13.17 GB | **0.0727** | `DV/HDR10` | 0.028 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 8 | Finding Nemo | 2003 | HEVC | 2160p | 9.66 GB | **0.069** | `DV/HDR10` | 1.778 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 9 | Grand Theft Auto VI An Ex | 2026 | HEVC | 2160p | 2.36 GB | **0.0507** | `SDR` | 0.477 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 10 | Green.Book.2018-2160p.Blu | 0 | AV1 | 2160p | 8.05 GB | **0.0502** | `HDR10` | 0.721 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 11 | How to Train Your Dragon | 2010 | HEVC | 2160p | 10.56 GB | **0.0774** | `HDR10` | 0.329 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=4.00 rc=abr bitrate=1 |
| 12 | Inside Out | 2015 | HEVC | 2160p | 9.55 GB | **0.0726** | `DV/HDR10` | 0.544 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 13 | Jaws | 1975 | HEVC | 2160p | 13.76 GB | **0.079** | `DV/HDR10` | 0.104 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=4.00 rc=abr bitrate=1 |
| 14 | Jurassic World | 2015 | HEVC | 2160p | 13.67 GB | **0.0791** | `DV/HDR10` | 0.077 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=4.00 rc=abr bitrate=1 |
| 15 | Jurassic World Fallen Kin | 2018 | HEVC | 2160p | 14.06 GB | **0.0789** | `DV/HDR10` | 0.096 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=4.00 rc=abr bitrate=1 |
| 16 | Kill Bill The Whole Blood | 2004 | HEVC | 2160p | 27.17 GB | **0.0773** | `DV/HDR10` | 0.808 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=2.00 rc=abr bitrate=1 |
| 17 | Kill Bill Vol 1 | 2003 | HEVC | 2160p | 11.85 GB | **0.0767** | `DV/HDR10` | 0.019 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=2.00 rc=abr bitrate=1 |
| 18 | Klaus | 2019 | HEVC | 2160p | 5.29 GB | **0.0387** | `DV/HDR10` | 0.794 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 19 | Mad.Max.Fury.Road.2015-21 | 0 | AV1 | 2160p | 7.47 GB | **0.0447** | `DV/HDR10` | 0.541 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 20 | No Country for Old Men | 2007 | AV1 | 2160p | 8.24 GB | **0.0485** | `DV/HDR10` | 0.21 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 21 | Oppenheimer | 2023 | AV1 | 2160p | 11.71 GB | **0.0467** | `DV/HDR10` | 2.669 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 22 | Platoon.1986-2160p.BluRay | 0 | AV1 | 2160p | 7.06 GB | **0.0441** | `HDR10` | 0.917 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 23 | Project Hail Mary | 2026 | AV1 | 2160p | 10.69 GB | **0.0492** | `DV/HDR10` | 0.186 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 24 | Rocky.1976-2160p.BluRay.D | 0 | AV1 | 2160p | 7.04 GB | **0.0424** | `DV/HDR10` | 0.065 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 25 | Schindlers List | 1993 | AV1 | 2160p | 12.86 GB | **0.0474** | `DV/HDR10` | 0.133 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 26 | Star Wars Episode II Atta | 2002 | HEVC | 2160p | 12.37 GB | **0.0625** | `DV/HDR10` | 0.538 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 27 | Star Wars Episode III Rev | 2005 | HEVC | 2160p | 14.98 GB | **0.077** | `DV/HDR10` | 0.109 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 28 | Star Wars Episode IV A Ne | 1977 | HEVC | 2160p | 12.78 GB | **0.0738** | `DV/HDR10` | 0.008 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 29 | Star Wars Episode IX The  | 2019 | HEVC | 2160p | 15.09 GB | **0.0766** | `DV/HDR10` | 0.098 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 30 | Star Wars Episode V The E | 1980 | HEVC | 2160p | 12.57 GB | **0.071** | `DV/HDR10` | 0.002 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 31 | Star Wars Episode VI Retu | 1983 | HEVC | 2160p | 13.55 GB | **0.0724** | `DV/HDR10` | 0.008 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 32 | Star Wars Episode VII The | 2015 | HEVC | 2160p | 14.57 GB | **0.076** | `DV/HDR10` | 0.01 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 33 | Star Wars Episode VIII Th | 2017 | HEVC | 2160p | 16.67 GB | **0.079** | `DV/HDR10` | 0.005 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 34 | The Dark Knight | 2008 | AV1 | 2160p | 9.54 GB | **0.0451** | `HDR10` | 0.0 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 35 | The Departed | 2006 | AV1 | 2160p | 6.32 GB | **0.0404** | `HDR10` | 1.139 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 36 | The Mandalorian and Grogu | 2026 | AV1 | 2160p | 8.24 GB | **0.0449** | `DV/HDR10` | 0.741 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 37 | The Shawshank Redemption | 1994 | HEVC | 2160p | 15.39 GB | **0.0777** | `DV/HDR10` | 0.02 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=4.00 rc=abr bitrate=1 |
| 38 | The Sound of Music | 1965 | HEVC | 2160p | 19.38 GB | **0.0799** | `DV/HDR10` | 0.1 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 39 | The Terminator | 1984 | AV1 | 2160p | 6.7 GB | **0.0449** | `HDR10` | 0.0 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 40 | The Truman Show | 1998 | HEVC | 2160p | 10.63 GB | **0.0743** | `DV/HDR10` | 0.069 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 41 | The Wolf of Wall Street | 2013 | HEVC | 2160p | 17.43 GB | **0.0698** | `DV/HDR10` | 1.182 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 42 | The Wolverine | 2013 | AV1 | 2160p | 5.55 GB | **0.0428** | `DV/HDR10` | 0.631 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 43 | The.Usual.Suspects.1995-2 | 0 | AV1 | 2160p | 5.13 GB | **0.047** | `HDR10` | 1.511 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 44 | Toy Story | 1995 | HEVC | 2160p | 8.3 GB | **0.0737** | `DV/HDR10` | 0.285 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 45 | Toy Story 3 | 2010 | HEVC | 2160p | 10.42 GB | **0.0732** | `DV/HDR10` | 0.617 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 46 | V.for.Vendetta.2005-2160p | 0 | AV1 | 2160p | 9.48 GB | **0.0515** | `DV/HDR10` | 0.174 | 0.0 | `STARVED-BUT-CLEAN` | None |
| 47 | Your Name | 2016 | HEVC | 2160p | 9.96 GB | **0.0672** | `HDR10` | 0.02 | 0.0 | `STARVED-BUT-CLEAN` | psy-rd=0.40 rc=abr bitrate=1 |
