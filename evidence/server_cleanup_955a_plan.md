# Local Server Cleanup & Stack-Only Audit Plan (Op 955A)
**Date:** 2026-08-29
**Scope:** Server Host Clean-up (Media Stack Root) & Repository State Audit
**Status:** **PROPOSED & PENDING APPROVAL**

> [!IMPORTANT]
> **Safety Guarantee:** This cleanup plan strictly targets obsolete scratch files, temporary build checkouts, and historical measurement dumps in the `scratch/` directory. Zero media files, Docker containers, live service configs (`config/`), FUSE mounts (`library/`), or git-tracked source files are affected.

---

## 1. Inventory & Categorization Summary

A thorough filesystem audit of the host environment identified **22 temporary artifacts** (~350 MB) accumulated during calibration, measurement, and CI proof testing across Ops 939–954.

| Artifact Path | Size | Category | Rationale & Proposed Action |
| :--- | :---: | :---: | :--- |
| `scratch/bin/` | ~269 MB | **DELETE** | Standalone ffmpeg/vmaf measurement binaries from Ops 939–948. Empirical measurements are completed and frozen in `verdicts.csv`. |
| `scratch/profilarr-src/` | ~53 MB | **DELETE** | Upstream Profilarr source clone used for code inspection during schema design. |
| `scratch/dictionarry-db-src/` | ~5.7 MB | **DELETE** | Upstream Dictionarry database clone used for schema comparison. |
| `scratch/ci-proof-loop-op*/` | ~21.6 MB | **DELETE** | Ephemeral cleanroom test trees from Ops 925, 938, and 940A. |
| `scratch/vmaf_*.json` | ~0.8 MB | **DELETE** | One-off raw VMAF frame telemetry JSON files. All metrics are consolidated in `verdicts.csv`. |
| `scratch/calibration*/` | ~0.03 MB | **DELETE** | Temporary execution logs and directories from early probe tests. |
| `scratch/replace_indexers.txt` | < 4 KB | **DELETE** | Temporary scratchpad notes from indexer verification. |
| `scratch/models/` | ~48 KB | **DELETE** | Standalone VMAF model files used during measurement runs. |
| `docker-compose.yml`, `*.sh`, `optimize_all_dbs.py` | — | **KEEP** | Essential production media stack lifecycle and database maintenance scripts. |
| `config/`, `library/`, `metadata/` | — | **KEEP** | Active service databases, runtime configurations, FUSE mounts, and media metadata. |
| `database-AV1/ops/*.sql` | — | **KEEP** | Full, authoritative PCD migration history (341 files). |
| `database-AV1/evidence/*` | — | **KEEP & FROZEN** | Complete historical evidence suite, verdict ledgers, and audit reports tracked on GitHub `origin/v2`. |

---

## 2. Proposed Execution Steps

1. Purge all obsolete scratch artifacts in `scratch/*`.
2. Clear local `__pycache__` directories in test and scratch paths.
3. Confirm host disk space recovery (~350 MB).
4. Run full repository hygiene and PCD cleanroom test loop to verify zero regressions.
5. Generate final execution report (`server_cleanup_955a_report.md`).
