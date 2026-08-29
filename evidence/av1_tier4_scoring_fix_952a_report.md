# Fix Unmeasured AV1 Tier 4 Scoring Report (Op 952A)
**Date:** 2026-08-28
**Scope:** PCD SQL Migration & Live Radarr4k / Profilarr Alignment for Unified 4-Tier Scoring ($\ge 1001$ Grabbable Threshold)
**Artifacts Generated:**
- PCD Migration SQL: [`../ops/952.add-av1-unmeasured-encoders-tier4-scoring.sql`](../ops/952.add-av1-unmeasured-encoders-tier4-scoring.sql)
- Raw Snapshot & Live Results: [`av1_tier4_scoring_fix_952a_raw.json`](av1_tier4_scoring_fix_952a_raw.json)

> [!IMPORTANT]
> **Operational Confirmation:** This operation updated PCD migration SQL and live Custom Format scoring rules in Radarr4k (`Movies 2160p AV1 HQ`, ID `64`). Zero media files, download clients, indexers, or storage containers were modified.

---

## 1. Problem Statement & Context

During the Op 951A field test evaluation of *The Bourne Ultimatum (2007)* (Movie ID `916`), an unmeasured/unvetted AV1 release from group `Bi0hazard` received **`3600` points** and won release selection over a high-fidelity reference x265 encode from `MainFrame` at **`2200` points**:

```markdown
Before Op 952A:
1. Das.Bourne.Ultimatum.2007...AV1-Bi0hazard  [Score: 3600] -> (Unintended Winner)
2. The.Bourne.Ultimatum.2007...x265-MainFrame  [Score: 2200] -> (Subordinate)
```

### Root Cause:
* The base `AV1` Custom Format assigns `+3500` to any release bearing the `AV1` codec marker.
* The previous quarantine rule (`AV1 Nameless`) only triggered on releases lacking a release group tag entirely. Because `-Bi0hazard` carries a recognized regex group name, it avoided the penalty and received the full `+3500` base score.

---

## 2. Unified 4-Tier Scoring Architecture ($\ge 1001$ Grabbable Threshold)

Op 952A updates PCD schema and live Radarr4k configuration to establish a strict, non-overlapping 4-tier score ladder where **every tier is grabbable ($\ge 1001$)**, but unmeasured groups are strictly quarantined in Tier 4 below Tier 3 x265:

```markdown
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 1: Preferred AV1 (ChopperHitler, CoSMiCSuRFeR, UH)                    │
│  Score Band: ~4,500 – 5,950  [AV1 +3500 + AV1 Quality +1000 + HDR/Audio]    │
│  Role: Top priority selection; wins over all other tiers.                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if absent)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 2: Review AV1 (RandH, Smokindevil, Rob74K, WhiskeyJack)               │
│  Score Band: ~3,800 – 5,300  [AV1 +3500 + AV1 Compact +500 + HDR/Audio]     │
│  Role: Allowed fallback; wins over x265 when Tier 1 is absent.              │
│  Guardrail: AV1 Lean 2160p (-3400) demotes undersized releases below x265.  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if absent or penalized)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 3: x265 Reference Fallback (hallowed, MainFrame, Dumpstarr, HONE)     │
│  Score Band: ~2,000 – 2,800  [2160p Quality +2850 - Not AV1 2000 + DV/HDR]  │
│  Role: High-fidelity baseline; wins over failing Review AV1 & Tier 4.       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if absent)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Tier 4: Last Resort AV1 (Bi0hazard, Waldek, SHADOW, Nameless AV1)          │
│  Score Band: ~1,100 – 1,600  [AV1 +3500 - Unmeasured AV1 2400 + HDR/Audio]  │
│  Role: Grabbable (>1000) as last resort, but strictly below Tier 3 x265.    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (if bad release)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Universal Hygiene Blocklist (CAM, Screener, Upscale, 3D, Banned Groups)   │
│  Score: -10,000  (Hard Rejected)                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. PCD Migration Implementation (`ops/952`)

1. **Tier 1 (`AV1 Quality Encoders`):** Regex aligned to `ChopperHitler`, `CoSMiCSuRFeR`, `UH` (Score `+1000`).
2. **Tier 2 (`AV1 Compact Encoders`):** Regex aligned to `RandH`, `Smokindevil`, `Rob74K`, `WhiskeyJack`, etc. (Score `+500`).
3. **Tier 4 (`AV1 Unmeasured Encoders`):** Created regex matching `Bi0hazard`, `Waldek`, `SHADOW`, and created Custom Format `AV1 Unmeasured Encoders` with score **`-2400`** in `Movies 2160p AV1 HQ`.
4. **`AV1 Nameless` Score Alignment:** Updated score to **`-2400`** to align all nameless/unmeasured AV1 at the same Tier 4 level.

---

## 4. Live Verification Results

Interactive release searches in Radarr4k confirmed the fix:

### Case 1: *The Bourne Ultimatum (2007)* (Movie ID `916`)
* **Winner (Tier 3 x265 Reference):** `The Bourne Ultimatum 2007 2160p BluRay DTS-X 7 1 DV HDR10 x265-MainFrame`
  * Score: **`2200`** (`10-bit Depth`, `2160p Quality Tier 2`, `Dolby Vision`, `DTS-X`, `HDR`, `Not AV1`)
* **Quarantined (Tier 4 Unmeasured AV1):** `Das.Bourne.Ultimatum.2007.German.DUBBED.DL.EAC3.2160p.HDR.BluRay.AV1-Bi0hazard`
  * Score: **`1200`** (`10-bit Depth`, `AV1`, `AV1 Unmeasured Encoders`, `Dolby Digital +`, `Foreign Dub`, `HDR`)
* **Verdict:** **PASS.** MainFrame x265 wins at $2200 > 1200$. Bi0hazard is properly quarantined in Tier 4 while remaining grabbable ($1200 \ge 1001$).

### Case 2: *John Wick: Chapter 2 (2017)* (Movie ID `922`)
* **Winner (Tier 2 Review AV1):** `John.Wick.Chapter.2.2017.UHD.BluRay.2160p.TrueHD.Atmos.7.1.AV1-Rob74K`
  * Score: **`3650`** (`AV1`, `TrueHD`)
* **Alternative (Tier 3 x265 Reference):** `John.Wick.Chapter.2.2017.2160p.BluRay.TrueHD.Atmos.7.1.DV.HDR10.x265-MainFrame`
  * Score: **`2200`**
* **Verdict:** **PASS.** Rob74K Review AV1 wins at $3650 > 2200$.

### Case 3: *X-Men (2000)* (Movie ID `861`)
* **Winner (Tier 1 Candidate AV1):** `X-Men.2000.2160p.BluRay.AV1.10bit.5.1ch.AC3.AV1-ChopperHitler`
  * Score: **`4900`**
* **Verdict:** **PASS.** ChopperHitler Candidate AV1 wins top priority.

---

## 5. Governance & Safety Confirmation

* Live changes are strictly confined to Radarr4k Custom Format conditions (`AV1 Unmeasured Encoders`) and Quality Profile 64 scoring weights.
* All tiers score $\ge 1001$, ensuring grabbability across all tiers while enforcing exact tier precedence (Tier 1 > Tier 2 > Tier 3 > Tier 4).
* Zero media files, download clients, indexers, or running storage containers were modified.
