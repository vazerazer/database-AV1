# Evidence-Led Policy Simulation Harness Report (Op 946A)
**Date:** 2026-08-28
**Scope:** Policy Simulation & Impact Modeling of AV1 Group Treatments across 30 Consolidated Verdict Ledger Rows
**Artifacts Generated:**
- Simulation Script: [`../scripts/simulate_av1_policy_946a.py`](../scripts/simulate_av1_policy_946a.py)
- Raw Simulation Metrics: [`av1_policy_simulation_946a_raw.json`](av1_policy_simulation_946a_raw.json)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is an evidence-led policy simulation and impact modeling harness only. It does not modify active profiles, tiers, scores, Custom Formats, Radarr/Profilarr configuration, release restrictions, download rules, media files, or live automation.

---

## 1. Executive Summary & Simulation Scope

* **Purpose:** Model how different hypothetical AV1 group treatments and evidence-basis classifications would influence automated release selection in practice, using the consolidated verdict ledger (`evidence/verdicts.csv` from Op 945A).
* **Corpus Evaluated ($N=30$ Ledger Rows):**
  * `same-master-reference` ($n=12$ rows across 5 groups): Credible multi-scene calibrations against UHD masters.
  * `hallowed-relative` ($n=5$ rows across 5 groups): Descriptive incremental loss comparisons relative to Hallowed.
  * `insufficient-parity` ($n=1$ row): Mismatched transfer remastering.
  * `none` ($n=12$ rows): Historical audit, shadow probe, pending, exception, void, and non-AV1 reference anchor rows.

---

## 2. Scenario Definitions & Decision Logic

```mermaid
graph TD
    Row[Ledger Row Evaluated] --> CodecCheck{Codec == AV1?}
    CodecCheck -- No --> BlockAnchor[Blocked: Non-AV1 Reference Anchor]
    CodecCheck -- Yes --> ParityCheck{evidence_basis == insufficient-parity?}
    ParityCheck -- Yes --> BlockParity[Blocked: Excluded Insufficient-Parity]
    ParityCheck -- No --> UnmeasuredCheck{confidence_state == unmeasured?}
    UnmeasuredCheck -- Yes --> BlockUnmeasured[Blocked: Excluded Unmeasured]
    UnmeasuredCheck -- No --> ScenarioSwitch{Scenario Evaluator}

    ScenarioSwitch -- baseline_current --> S1[Candidate: Preferred | Review: Allowed]
    ScenarioSwitch -- strict_candidate_only --> S2[Candidate: Preferred | Review: Blocked]
    ScenarioSwitch -- relaxed_review_allowed --> S3[Candidate: Preferred | Review: Allowed]
    ScenarioSwitch -- evidence_basis_aware --> S4[Qualifies Reason Code by Same-Master vs Hallowed-Relative]
```

### 1. `baseline_current` (Current Operational Architecture)
* **Candidate Groups (`ChopperHitler`, `CoSMiCSuRFeR`):** `allowed=true`, `preferred=true`.
* **Review Groups (`RandH`, `Smokindevil`, `Rob74K`):** `allowed=true`, `preferred=false` (allowed as secondary alternatives when candidate releases are unavailable).
* **Unmeasured / None / Insufficient-Parity:** `allowed=false`, `preferred=false`.

### 2. `strict_candidate_only` (Zero-Risk Quality Gate)
* **Candidate Groups:** `allowed=true`, `preferred=true`.
* **Review Groups:** `allowed=false`, `preferred=false` (strictly blocked from selection).
* **Unmeasured / None / Insufficient-Parity:** `allowed=false`, `preferred=false`.

### 3. `relaxed_review_allowed` (Maximum Pool Availability)
* **Candidate Groups:** `allowed=true`, `preferred=true`.
* **Review Groups:** `allowed=true`, `preferred=false`.
* **Unmeasured / None / Insufficient-Parity:** `allowed=false`, `preferred=false`.

### 4. `evidence_basis_aware` (Fidelity-Origin Disambiguation)
* Refines release selection reason codes by incorporating empirical origin:
  * `same-master-reference` + `candidate`: `allowed=true`, `preferred=true` (`candidate-same-master-reference-fully-preferred`).
  * `hallowed-relative` + `candidate`: `allowed=true`, `preferred=true` (`candidate-hallowed-relative-only-preferred`).
  * `same-master-reference` + `review`: `allowed=true`, `preferred=false` (`review-same-master-reference-allowed`).
  * `hallowed-relative` + `review`: `allowed=true`, `preferred=false` (`review-hallowed-relative-only-allowed-warning`).
  * `insufficient-parity` / `none` / `unmeasured`: `allowed=false`, `preferred=false`.

---

## 3. Comparative Scenario Outcomes ($N=30$)

| Scenario Name | Total Evaluated | Allowed Titles | Preferred Titles | Blocked Titles | Primary Policy Effect |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`baseline_current`** | 30 | **15** | **6** | **15** | Balances high-confidence automation with review group fallback. |
| **`strict_candidate_only`** | 30 | **6** | **6** | **24** | Maximizes quality assurance; eliminates risk of shadow/grain dips (e.g. *Fury*, *John Wick 1*). |
| **`relaxed_review_allowed`**| 30 | **15** | **6** | **15** | Identical pool coverage to baseline while retaining secondary ranking for review groups. |
| **`evidence_basis_aware`** | 30 | **15** | **6** | **15** | Transparently tags Hallowed-relative observations with explicit relative warnings. |

---

## 4. Group-by-Group Behavioral Impact Matrix

| Release Group | Total Rows in Ledger | `baseline_current` | `strict_candidate_only` | `relaxed_review_allowed` | `evidence_basis_aware` | Policy Transition Notes |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`ChopperHitler`** | 4 | 4 Allowed (4 Preferred) | 4 Allowed (4 Preferred) | 4 Allowed (4 Preferred) | 4 Allowed (4 Preferred) | Fully preferred across all scenarios ($n=3$ same-master, $n=1$ Hallowed-relative). |
| **`CoSMiCSuRFeR`** | 4 | 2 Allowed (2 Preferred) | 2 Allowed (2 Preferred) | 2 Allowed (2 Preferred) | 2 Allowed (2 Preferred) | JW3/JW4 preferred; LOTR mismatch and Rip shadow probe blocked across all scenarios. |
| **`RandH`** | 8 | 4 Allowed (0 Preferred) | **0 Allowed (0 Preferred)**| 4 Allowed (0 Preferred) | 4 Allowed (0 Preferred) | Blocked entirely in `strict_candidate_only`; allowed non-preferred in others ($n=4$ unmeasured blocked). |
| **`Smokindevil`** | 3 | 3 Allowed (0 Preferred) | **0 Allowed (0 Preferred)**| 3 Allowed (0 Preferred) | 3 Allowed (0 Preferred) | Blocked entirely in `strict_candidate_only`; allowed non-preferred in others. |
| **`Rob74K`** | 2 | 2 Allowed (0 Preferred) | **0 Allowed (0 Preferred)**| 2 Allowed (0 Preferred) | 2 Allowed (0 Preferred) | Blocked entirely in `strict_candidate_only`; allowed non-preferred in others. |
| **`Bi0hazard`** | 2 | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | Blocked across all scenarios (single-title Hallowed-relative observation retains unmeasured state). |
| **`Waldek`** | 1 | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | Blocked across all scenarios (single-title Hallowed-relative observation retains unmeasured state). |
| **`SHADOW` / `FLUX` / Anchors** | 6 | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | 0 Allowed (0 Preferred) | Non-AV1 reference anchors and unmeasured shadow probes blocked from AV1 selection. |

---

## 5. Key Findings & Strategic Insights

1. **Candidate Group Stability:** `ChopperHitler` and `CoSMiCSuRFeR` represent the core reliable AV1 supply, delivering 6 preferred titles across all evaluated scenarios with zero policy friction.
2. **Review Group Trade-Offs:**
   * Moving from `baseline_current` to `strict_candidate_only` reduces the available AV1 title pool from 15 to 6 (a 60% reduction in allowed titles), but completely protects against documented low-end edge cases (e.g. *Fury* 66.77 VMAF, *John Wick 1* 68.61 VMAF).
   * In `evidence_basis_aware`, review titles are admitted with explicit tracking reason codes (e.g. `review-hallowed-relative-only-allowed-warning`), ensuring transparent auditability.
3. **Unmeasured Group Containment:** Discovered unmeasured groups (`Bi0hazard`, `Waldek`, `SHADOW`) are safely quarantined across all scenarios until credible multi-title same-master evidence is established.

---

## 6. Limitations & Non-Operational Declaration

* **Simulation Scope Limitation:** This simulation evaluates static decisions over historical and calibration ledger rows. It does not model dynamic Radarr grab queues, indexer RSS feeds, or real-time score arbitration.
* **Non-Operational Guardrail Confirmation:** Zero active operational configurations, Custom Formats, profile scores, tier assignments, release restrictions, download rules, media files, or running containers were modified.
