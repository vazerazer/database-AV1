# Profile Streamlining & Deprecation Report (Op 957A)
**Date:** 2026-08-29
**Scope:** Removal of 7 Unused/Redundant Profiles & Consolidation on Flagship 4K Movie Profile
**Artifacts Generated:**
- Raw Streamlining Dataset: [`profile_streamlining_957a_raw.json`](profile_streamlining_957a_raw.json)
- PCD SQL Migration: [`../ops/957.deprecate-all-unused-profiles.sql`](../ops/957.deprecate-all-unused-profiles.sql)

> [!IMPORTANT]
> **Summary of Action:** Op 957A permanently deprecates all 7 unused, exploratory, and redundant profiles (`Movies SHADOW Explorer`, `Anime 1080p AV1`, `TV 2160p AV1`, `TV 1080p AV1 HQ`, `TV 1080p AV1 Storage`, `Movies 1080p AV1 HQ`, and `Movies 1080p AV1 Storage`). The repository is now 100% pure and dedicated to the flagship production profile: **`Movies 2160p AV1 HQ`**.

---

## 1. Rationale & Inventory

| Profile Name | Role | Reason for Deprecation |
| :--- | :--- | :--- |
| **`Movies SHADOW Explorer`** | Test / Dev | Exploratory testing completed; unmeasured AV1 is now fully governed in Tier 4 of `Movies 2160p AV1 HQ`. |
| **`Anime 1080p AV1`** | Anime draft | Unused; no active anime instance. |
| **`TV 2160p AV1`** | 4K TV draft | Redundant; live Sonarr4k uses the superior Dumpstarr `TV 2160p` profile for untouched streaming WEB-DLs. |
| **`TV 1080p AV1 HQ`** | 1080p TV draft | Unused; live Sonarr uses Dictionarry `1080p Efficient`. |
| **`TV 1080p AV1 Storage`** | 1080p TV draft | Unused; live Sonarr uses Dictionarry `1080p Efficient`. |
| **`Movies 1080p AV1 HQ`** | 1080p Movie draft | Unused; live Radarr uses Dictionarry `1080p Efficient`. |
| **`Movies 1080p AV1 Storage`** | 1080p Movie draft | Unused; live Radarr uses Dictionarry `1080p Efficient`. |

---

## 2. Changes Applied in Op 957A

1. **PCD Migration (`ops/957.deprecate-all-unused-profiles.sql`):**
   - Cleanly removed scoring rules, qualities, quality group members, quality groups, tags, and profile records for all 7 deprecated profiles.
2. **Flagship Snapshot & Drift Guard:**
   - Updated `ops/profile_snapshot.json` and `tests/test_profile_drift.py` to focus exclusively on `Movies 2160p AV1 HQ`.
3. **Live System Cleanup:**
   - Deleted obsolete `Movies SHADOW Explorer` profile (ID 67) from live Radarr4k daemon via REST API.

---

## 3. Post-Streamlining Verification

* **Retained Custom Profiles in PCD:** Exactly 1 (`Movies 2160p AV1 HQ`)
* **Scored Custom Formats:** 69 (100% matched to Radarr4k Profile ID 64)
* **Drift Status:** 0 drift (69/69)
* **9-Step Cleanroom Proof Battery:** 100% Passed
* **Security & Tripwire Hygiene:** 100% Clean
