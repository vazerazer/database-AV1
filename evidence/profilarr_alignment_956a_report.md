# Profilarr 69/69 Alignment & Deprecated Banned Format Clean-up Report (Op 956A)
**Date:** 2026-08-29
**Scope:** Resolution of Profilarr "69/71" Profile Sync Discrepancy & Banned Format Standardization
**Artifacts Generated:**
- Raw Alignment Dataset: [`profilarr_alignment_956a_raw.json`](profilarr_alignment_956a_raw.json)
- PCD SQL Migration: [`../ops/956.remove-deprecated-banned-groups-from-av1-profiles.sql`](../ops/956.remove-deprecated-banned-groups-from-av1-profiles.sql)

> [!IMPORTANT]
> **Summary of Action:** Op 956A cleanly removes defunct scoring references to `Banned Groups (Compact)` and `Banned Groups (Release Title)` from all AV1 profiles. The PCD profile `Movies 2160p AV1 HQ` now contains exactly **69 active, operational Custom Formats**, achieving 100% parity with live Radarr4k (69/69).

---

## 1. Problem & Root Cause Analysis

When synchronizing `Movies 2160p AV1 HQ` to Radarr4k via Profilarr, Profilarr displayed `69/71` synchronized formats.

* **Root Cause:**
  - Upstream Dictionarry migrations (ops 88 & 156) originally introduced `Banned Groups (Compact)` and `Banned Groups (Release Title)`.
  - Upstream migrations (ops 171 & 190) subsequently removed and consolidated these formats into the 4 active standard formats:
    1. `Banned Groups` (`-10000`)
    2. `Banned Groups (Regular)` (`-10000`)
    3. `Banned Groups (Efficient)` (`-10000`)
    4. `Banned Remux` (`-10000`)
  - Early AV1 profile creation (`ops/902`) assigned scores to the two defunct format names. Because Radarr4k correctly runs only active Custom Formats, it contained 69 items while PCD held 71.

---

## 2. Changes Applied in Op 956A

1. **PCD Migration (`ops/956.remove-deprecated-banned-groups-from-av1-profiles.sql`):**
   - Cleanly removed `Banned Groups (Compact)` and `Banned Groups (Release Title)` scoring rules across all 8 AV1/SHADOW quality profiles.
   - Aligned `Movies SHADOW Explorer` profile scores (`AV1 Nameless: -2400` and `AV1 Unmeasured Encoders: -2400`).
2. **Snapshot & Profile Drift Synchronization (`ops/profile_snapshot.json`):**
   - Updated profile definition hashes and score snapshots to match live Radarr4k.

---

## 3. Verification & Parity Assessment

* **PCD Scored Custom Formats in `Movies 2160p AV1 HQ`:** **69**
* **Live Radarr4k Scored Custom Formats:** **69**
* **Profilarr Sync State:** **69 / 69 (100% Parity, 0 Drift)**
* **Full 9-Step Cleanroom Test Battery:** **100% Passed**
* **Security & Tripwire Hygiene:** **100% Clean**
