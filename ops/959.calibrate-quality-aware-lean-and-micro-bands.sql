-- =============================================================================
-- Migration: 959.calibrate-quality-aware-lean-and-micro-bands.sql
-- Description: Calibrate AV1 Micro 2160p to 1.0 - 5.0 GB (-10000 hard ban)
--              and AV1 Lean 2160p to 5.0 - 11.0 GB (-2500 score) so high-VMAF
--              Quality Encoders (ChopperHitler at 5.89 GB) score 2700-3000
--              and win over standard 14-25 GB x265, while non-quality lean
--              encodes (Smokindevil etc.) score ~2200 and yield to 14 GB x265.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 95901
-- 1. Update 'AV1 Micro 2160p' window to 1.0 - 5.0 GB
UPDATE condition_sizes
SET min_bytes = 1073741824, max_bytes = 5368709120
WHERE custom_format_name = 'AV1 Micro 2160p' AND condition_name = 'Micro 2160p Size';

-- 2. Update 'AV1 Lean 2160p' window to 5.0 - 11.0 GB
UPDATE condition_sizes
SET min_bytes = 5368709121, max_bytes = 11811160064
WHERE custom_format_name = 'AV1 Lean 2160p' AND condition_name = 'Lean 2160p Size';

-- 3. Set 'AV1 Micro 2160p' score to -10000 in Movies 2160p AV1 HQ
UPDATE quality_profile_custom_formats
SET score = -10000
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'AV1 Micro 2160p';

-- 4. Set 'AV1 Lean 2160p' score to -2500 in Movies 2160p AV1 HQ
UPDATE quality_profile_custom_formats
SET score = -2500
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'AV1 Lean 2160p';
-- --- END op 95901
