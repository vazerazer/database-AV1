# 🛡️ Standard Operational Guardrails & Protocol

This document defines the permanent operational rules and execution guardrails for the `database-AV1` repository. Every operational session and agent MUST adhere to these rules without exception.

---

## 1. Core Operational Guardrails

1. **Production Mutability Boundary:**
   * Production `Radarr4k` Profile `64` is strictly **READ-ONLY** unless an operation explicitly mandates updates.
   * `Sonarr4k` is always untouched unless specified.

2. **Runtime Secret Isolation:**
   * All API keys, tokens, and credentials come from environment variables or local service configurations at runtime only.
   * Never hardcode, never log, and never commit secrets or tokens.

3. **Quarantine Path Pattern (Zero-Leakage Rule):**
   * NEVER stage or commit files matching:
     * `evidence/supply_*`
     * `evidence/supply_av1.csv`
     * `evidence/supply_checkpoint.jsonl`
     * `evidence/checkpoints/`
     * `evidence/census_924.md`
     * `evidence/indexer_map.local`
     * `*.local`
   * Only [`evidence/verdicts.csv`](evidence/verdicts.csv) and [`evidence/census_924_public.md`](evidence/census_924_public.md) are allowed public tracked artifacts.

4. **Mandatory Local Proof Loop:**
   * Full local 8-step proof loop INCLUDING [`tests/test_tripwire_hygiene.py`](tests/test_tripwire_hygiene.py) (path guards, 32-hex regex, absolute `/home/` path scan, indexer brand name check) must pass 100% green before any commit.
   * Paste all test battery counts in the response.

5. **Local Commit & Halt Protocol:**
   * Assemble commits locally and **STOP**.
   * The user reviews and pushes manually, every single time.

6. **Post-Push Verification:**
   * After push, run `git ls-remote` to verify the remote ref.
   * Dispatch CI manually if the webhook is delayed.
   * Verify and report the CI run outcome.

---

## 2. Test Battery Reference

Run the offline proof loop:
```bash
# 1. PCD SQLite Harness Audit
python3 tests/audit_pcd_harness.py .

# 2. Refined AV1 Regex Battery
python3 tests/test_refined_regex_battery.py

# 3. Leading-Bracket Anime Encoder Battery
python3 tests/test_final_anime.py

# 4. Simulation Scoring Battery
python3 tests/simulate_scoring.py

# 5. Library Audit Core Test
python3 tests/test_library_audit.py

# 6. Supply Audit Core Test
python3 tests/test_supply_audit.py

# 7. Divergence Study Core Test
python3 tests/test_divergence_study.py

# 8. Local Security Tripwire & Path Guard
python3 tests/test_tripwire_hygiene.py

# 9. Profile Drift Guard Test
python3 tests/test_profile_drift.py
```
