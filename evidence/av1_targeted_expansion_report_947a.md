# Targeted Evidence Expansion Report (Op 947A)
**Date:** 2026-08-28
**Scope:** Planning Summary for Targeted Evidence Expansion across Review & Transition Groups
**Artifacts Generated:**
- Expansion Plan Document: [`av1_targeted_expansion_plan_947a.md`](av1_targeted_expansion_plan_947a.md)
- Pre-Registered Manifest: [`av1_targeted_expansion_manifest_947a.json`](av1_targeted_expansion_manifest_947a.json)
- Raw Expansion Metadata: [`av1_targeted_expansion_raw_947a.json`](av1_targeted_expansion_raw_947a.json)
- Validation Script: [`../scripts/plan_av1_targeted_expansion_947a.py`](../scripts/plan_av1_targeted_expansion_947a.py)

> [!IMPORTANT]
> **Governance & Non-Operational Guardrail Statement:** This is a planning and documentation artifact only. Zero modifications were made to Radarr, Profilarr, Custom Formats, profiles, scores, tier behavior, release restrictions, downloads, media, or live automation. All thresholds remain non-enforcing DRAFT.

---

## 1. Executive Summary

Op 947A establishes a pre-registered evidence expansion roadmap targeting the 5 release groups whose behavior shifts under different policy scenarios modeled in Op 946A (`RandH`, `Smokindevil`, `Rob74K`, `Bi0hazard`, and `Waldek`).

### Key Expansion Findings:
1. **`RandH` ($n=3$ planned titles):** High local potential. *The Bourne Supremacy (2004)* provides a confirmed same-master calibration pair (Op 943A baseline); *Jack Reacher (2012)* and *Blade Runner (1982)* provide credible Hallowed-relative comparison pairs.
2. **`Smokindevil` ($n=1$ planned title):** Local library corpus is fully cataloged. *The Sixth Sense (1999)* is prioritized for 1:1 UHD Remux master acquisition to upgrade its existing Hallowed-relative observation into a true same-master reference calibration.
3. **`Rob74K` ($n=0$ local titles / Inventory Exhausted):** Both available local releases (*John Wick 1*, *John Wick 2*) are already committed in `verdicts.csv`. Further evidence requires acquiring new 2160p releases from external indexers.
4. **`Bi0hazard` ($n=1$ planned title):** Prioritized for 1:1 UHD Remux acquisition for *The Bourne Ultimatum (2007)* to convert its single-title Hallowed-relative observation into a full same-master calibration.
5. **`Waldek` ($n=1$ planned title):** Prioritized for 1:1 UHD Remux acquisition for *John Wick: Chapter 2 (2017)* to establish ground-truth reference measurements following its severe 63.31 VMAF floor observation in Op 944A.

---

## 2. Target Group Expansion Overview

| Group | `confidence_state` | Same-Master `title_count` | Expansion Status | Proposed Titles | Primary Strategic Objective |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **`RandH`** | `review` | 3 | Candidates Available | 3 | Expand same-master calibration depth & quantify heavy-grain optical stress floor. |
| **`Smokindevil`** | `review` | 2 | Remux Acquisition Needed | 1 | Convert *Sixth Sense* Hallowed-relative observation to same-master reference. |
| **`Rob74K`** | `review` | 2 | **Inventory Exhausted** | 0 | Document exhaustion; roadmap external candidate discovery. |
| **`Bi0hazard`** | `unmeasured` | 0 | Remux Acquisition Needed | 1 | Establish ground-truth calibration for high-bitrate German DL encode. |
| **`Waldek`** | `unmeasured` | 0 | Remux Acquisition Needed | 1 | Verify whether severe textural smoothing (63.31 VMAF) is master- or encode-driven. |

---

## 3. Governance & Non-Operational Declaration

* **Non-Operational Guardrail Confirmation:** Zero active operational configurations, Custom Formats, profile scores, tier assignments, release restrictions, download rules, media files, or running containers were modified.
