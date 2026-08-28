# Profile 64 (`Movies 2160p AV1 HQ`) Specification & Score Diff (Op 935)
**Date:** 2026-08-28  
**Scope:** `database-AV1` Profile 64 & Profile 67 Score Adjustments + Specification Definitions  

---

## 1. Quality Profile Score Changes

| Custom Format | Previous Score (Op 934) | New Score (Op 935) | Rationale |
| :--- | :---: | :---: | :--- |
| **`Repack1`** | `0` (Unscored) | **`+5`** | Deterministic tie-breaker for identical release PROPER / REPACK / RERIP posts. |
| **`Repack2`** | `0` (Unscored) | **`+6`** | Deterministic tie-breaker for REPACK2 / REAL.REPACK posts. |
| **`Repack3`** | `0` (Unscored) | **`+7`** | Deterministic tie-breaker for REPACK3 / REAL.REAL.REPACK posts. |
| **`4K Remaster`** | `0` (Unscored) | **`+25`** | Restoration & 4K Remaster edition bonus. |
| **`Audio Description`** | `0` (Unscored) | **`-10000`** | Hard-rejection for DVS / Descriptive Video Service / ASL accessibility audio tracks. |

*Profile 64 Minimum Score (`1000`) and Upgrade Until Score (`6000`) remain strictly unchanged.*  
*Profile 67 (`Movies SHADOW Explorer`) mirrors the identical hygiene, repack, and remaster rules.*  
*Sonarr / Sonarr4k profiles remain 100% untouched.*

---

## 2. Custom Format Specification Changes

### A. `WEB-DL Tier 2` (ID 6585) — 46-Group Vetted Fallback Union
Added 46 Dumpstarr-vetted streaming scene/P2P release groups:
`SiGMA`, `JETIX`, `CEBEX`, `RTN`, `SDCC`, `GNOME`, `SLiGNOME`, `CRUD`, `DRACULA`, `PHOENiX`, `PSiG`, `DEEP`, `orbitron`, `APEX`, `BLOOM`, `ETHiCS`, `ViSUM`, `XEPA`, `MiU`, `PEXA`, `Dooky`, `iKA`, `KiMCHI`, `NYH`, `ABBIE`, `FC`, `iJP`, `PAXA`, `Flights`, `T6D`, `T4H`, `SiC`, `CiT`, `NINJACENTRAL`, `dB`, `END`, `SwAgLaNdEr`, `iT00NZ`, `ROCCaT`, `ViSiON`, `3cTWeB`, `RTFM`, `SPiRiT`, `4KBEC`, `Coo7`, `WEBDV`.

### B. `CAM` (ID 6634) — Expanded Source Hygiene Rejects
Updated `CAM` regular expression to include:
* `Line Audio`: `(?i)\b(LINE[ ._-]?Audio|HQ[ ._-]?LINE|LINE(?=[\W_]+(?:AC3|DDP|AAC|5\.1|2\.0)))\b`
* `ProRes`: `\b(ProRes|PRORES)\b`
* `WORKPRINT`, `SCREENER`, `HDCAM`, `HDTS`, `TELESYNC` variants.

### C. `Audio Description` (ID 6620) — DVS Integration
Added condition `DVS` (`\b(DVS|Descriptive[ ._-]?Audio|Descriptive[ ._-]?Video[ ._-]?Service)\b`).

### D. `4K Remaster` (ID 6715) — Local Custom Format Creation
Created custom format with condition `Remastered` (`\b(Remaster(ed)?|Restored|4K[ ._-]?Remaster(ed)?|Restoration)\b`).

---

## 3. Boundary & Invariant Proofs
* **Repack Gap Safety:** Repack bonus ($+5$ to $+7$) is $>14\times$ smaller than the smallest tier difference ($+100$). A Tier 2 Repack ($2750 + 7 = 2757$) will NEVER out-score a Tier 1 release ($2850$).
* **Remaster Gap Safety:** Remaster bonus ($+25$) is $4\times$ smaller than the smallest tier difference ($+100$). A Tier 2 Remaster ($2750 + 25 = 2775$) will NEVER out-score a Tier 1 release ($2850$).
* **AV1 Independence:** AV1 ladder rankings are 100% invariant; only within-band tie-breaks and WEB fallback tier coverage are widened.
