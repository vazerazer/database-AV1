-- =============================================================================
-- Migration: 910.op-909-followups.sql
-- Description: Ensure ENTROPY regular expression carries case-insensitive (?i) prefix.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 91001
UPDATE regular_expressions
SET pattern = '(?i)(?<![a-zA-Z0-9])ENTROPY\b'
WHERE name = 'ENTROPY';
-- --- END op 91001
