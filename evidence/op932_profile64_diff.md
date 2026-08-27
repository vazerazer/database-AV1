# 🛡️ Op 932 Profile 64 / Profile 67 Diff vs Pre-932 Baseline

**Pre-932 Baseline Commit:** `e853461`  
**Current Commit:** `21b66a1`  
**Verification Invariant:** Production Profile 64 custom format scores strictly unmodified; custom format definitions updated for naming hygiene and WEB-DL Tier 2 parity.

---

### Profile Scoring Diff: 0 Changes (Scores Identical)
```diff
# No score changes to Profile 64 (Movies 2160p AV1 HQ) or Profile 67 (Movies SHADOW Explorer)
```

### Custom Format Definition Updates:
1. **CF 6614 (`LQ Release Title`):** Removed false-positive specifications `\b(R&H)\b` and `PiRaTeS (no WEB-DL)`.
2. **CF 6617 (`No Audio`):** Added `Opus` specification (`(?<![a-zA-Z0-9])(Opus|OPUS)(?![a-zA-Z0-9])`, `Negate: True`, `Required: True`) to eliminate false tagging on Opus surround tracks.
3. **CF 6585 (`WEB-DL Tier 2`):** Expanded with legacy trusted archival groups (`PiRaTeS`, `Z0N3`, `playHD`, `GRiM`, `MrTentsaw`, `CtrlHD`, `BHDStudio`, `DON`, `EbP`, `LoRD`) ensuring 1080p WEB-DL parity.
4. **Group Regexes (`AV1 Compact Encoders`, `AV1 Quality Encoders`, `Legacy Trusted x264`):** Tolerates trailing indexer dupe tags `(?:[-._ ]?(?:[0-9]+|xpost))*$`.
