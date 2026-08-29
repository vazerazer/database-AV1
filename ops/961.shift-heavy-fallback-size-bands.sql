-- =============================================================================
-- Migration: 961.shift-heavy-fallback-size-bands.sql
-- Description: Shift Heavy 2160p Fallback window to 30.0 - 38.0 GB (-400 penalty),
--              Oversized 2160p Fallback window to 38.0 - 50.0 GB (-1500 penalty),
--              and Extreme 2160p window to 50.0 - 200.0 GB (-1500 penalty).
--              This provides a 0 - 30.0 GB penalty-free sweet spot for transparent
--              4K x265 Blu-ray encodes while preserving the full AV1 ladder.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 96101
-- 1. Update 'Heavy 2160p Fallback' size window to 30.0 - 38.0 GB
UPDATE condition_sizes
SET min_bytes = 32212254720, max_bytes = 40802189312
WHERE custom_format_name = 'Heavy 2160p Fallback' AND condition_name = 'Heavy Size';

-- 2. Update 'Oversized 2160p Fallback' size window to 38.0 - 50.0 GB
UPDATE condition_sizes
SET min_bytes = 40802189313, max_bytes = 53687091200
WHERE custom_format_name = 'Oversized 2160p Fallback' AND condition_name = 'Oversized Size';

-- 3. Update 'Extreme 2160p' size window to 50.0 - 200.0 GB
UPDATE condition_sizes
SET min_bytes = 53687091201, max_bytes = 214748364800
WHERE custom_format_name = 'Extreme 2160p' AND condition_name = 'Extreme Size';
-- --- END op 96101
