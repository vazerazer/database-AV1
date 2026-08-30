# OP 964A — Full Library BPP Density Audit (314 Movies)

- **Total Movies Audited:** 314
- **Audit Scope:** `library/altmount/complete/movies4k/`
- **Execution:** Local parallel ffprobe inspection (8 workers)

## 1. Classification & Status Breakdown
| Status Flag | Count | Share | Description |
| :--- | :---: | :---: | :--- |
| **OPTIMAL** | 128 | 40.8% | In target density sweet spot (0.045-0.075 AV1 / 0.080-0.140 HEVC) |
| **REFERENCE/HEAVY** | 50 | 15.9% | Above sweet spot (High bitrate / uncompressed master) |
| **RES-ANOMALY** | 100 | 31.8% | 1080p archival fallback or H264 transfer |
| **STARVED** | 36 | 11.5% | Below minimum density floor |

## 2. Codec & Resolution Distribution
| Codec | Count | Share | 2160p | 1080p |
| :--- | :---: | :---: | :---: | :---: |
| **HEVC** | 139 | 44.3% | 132 | 7 |
| **AV1** | 111 | 35.4% | 82 | 29 |
| **H264** | 64 | 20.4% | 0 | 64 |

## 3. Bits-Per-Pixel (BPP) Statistics by Codec
| Codec | Count | Mean BPP | Median BPP | Min BPP | Max BPP | Sweet Spot Target |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HEVC** | 139 | **0.1412** | 0.1059 | 0.0387 | 0.7092 | 0.080 – 0.140 |
| **H264** | 64 | **0.4038** | 0.4118 | 0.0973 | 0.687 | 0.150+ |
| **AV1** | 111 | **0.0845** | 0.0688 | 0.0325 | 0.2762 | 0.045 – 0.075 |

## 4. Top 20 Lowest BPP Suspects
| # | Movie | Year | Codec | Res | Size (GB) | BPP | Status | Audio |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | Capernaum | 2018 | AV1 | 1080p | 1.43 GB | **0.0325** | `RES-ANOMALY` | EAC3 6ch |
| 2 | Klaus | 2019 | HEVC | 2160p | 5.29 GB | **0.0387** | `STARVED` | EAC3 6ch |
| 3 | The Departed | 2006 | AV1 | 2160p | 6.32 GB | **0.0404** | `STARVED` | EAC3 6ch |
| 4 | Rocky.1976-2160p.BluRay.DV.HDR.1 | 0 | AV1 | 2160p | 7.04 GB | **0.0424** | `STARVED` | DTS 6ch |
| 5 | The Wolverine | 2013 | AV1 | 2160p | 5.55 GB | **0.0428** | `STARVED` | DTS 6ch |
| 6 | A Silent Voice | 2016 | AV1 | 1080p | 1.94 GB | **0.043** | `RES-ANOMALY` | EAC3 6ch |
| 7 | Platoon.1986-2160p.BluRay.HDR10. | 0 | AV1 | 2160p | 7.06 GB | **0.0441** | `STARVED` | EAC3 6ch |
| 8 | Mad.Max.Fury.Road.2015-2160p.Blu | 0 | AV1 | 2160p | 7.47 GB | **0.0447** | `STARVED` | DTS 6ch |
| 9 | The Mandalorian and Grogu | 2026 | AV1 | 2160p | 8.24 GB | **0.0449** | `STARVED` | EAC3 6ch |
| 10 | The Terminator | 1984 | AV1 | 2160p | 6.7 GB | **0.0449** | `STARVED` | DTS 6ch |
| 11 | The Dark Knight | 2008 | AV1 | 2160p | 9.54 GB | **0.0451** | `OPTIMAL` | OPUS 6ch |
| 12 | 3 Idiots | 2009 | AV1 | 1080p | 2.73 GB | **0.0458** | `RES-ANOMALY` | EAC3 6ch |
| 13 | Oppenheimer | 2023 | AV1 | 2160p | 11.71 GB | **0.0467** | `OPTIMAL` | DTS 6ch |
| 14 | The.Usual.Suspects.1995-2160p.Bl | 0 | AV1 | 2160p | 5.13 GB | **0.047** | `OPTIMAL` | EAC3 6ch |
| 15 | Schindlers List | 1993 | AV1 | 2160p | 12.86 GB | **0.0474** | `OPTIMAL` | DTS 6ch |
| 16 | No Country for Old Men | 2007 | AV1 | 2160p | 8.24 GB | **0.0485** | `OPTIMAL` | DTS 6ch |
| 17 | Project Hail Mary | 2026 | AV1 | 2160p | 10.69 GB | **0.0492** | `OPTIMAL` | EAC3 6ch |
| 18 | Green.Book.2018-2160p.BluRay.HDR | 0 | AV1 | 2160p | 8.05 GB | **0.0502** | `OPTIMAL` | DTS 6ch |
| 19 | Grand Theft Auto VI An Extended  | 2026 | HEVC | 2160p | 2.36 GB | **0.0507** | `STARVED` | EAC3 6ch |
| 20 | Amadeus | 1984 | AV1 | 2160p | 11.41 GB | **0.0513** | `OPTIMAL` | DTS 6ch |
