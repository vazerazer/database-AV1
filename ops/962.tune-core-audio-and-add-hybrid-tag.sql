-- =============================================================================
-- Migration: 962.tune-core-audio-and-add-hybrid-tag.sql
-- Description: Tune direct-bitstream core audio formats (DD+ to +200, TrueHD/DTS-X
--              to +100) optimized for HDMI ARC playback, and add 'Hybrid' (+50)
--              custom format for disc+streaming dynamic metadata injection.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 96201
-- 1. Create 'Hybrid' regular expression
INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES (
  'Hybrid',
  '(?i)\b(?:Hybrid|HYBRID)\b',
  'Matches hybrid releases combining disc video base with injected Dolby Vision metadata'
)
ON CONFLICT DO NOTHING;

-- 2. Create 'Hybrid' custom format
INSERT INTO "custom_formats" ("name", "description")
VALUES (
  'Hybrid',
  'Matches hybrid master releases combining uncompressed disc base with injected streaming Dolby Vision RPU'
)
ON CONFLICT DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name")
VALUES ('Hybrid', 'Enhancement')
ON CONFLICT DO NOTHING;

-- 3. Define condition for 'Hybrid'
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Hybrid', 'Hybrid Marker', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Hybrid', 'Hybrid Marker', 'Hybrid')
ON CONFLICT DO NOTHING;

-- 4. Assign 'Hybrid' score in Movies 2160p AV1 HQ (+50)
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Hybrid', 50, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 50;

-- 5. Tune ARC-friendly audio scores in Movies 2160p AV1 HQ
UPDATE quality_profile_custom_formats
SET score = 200
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'Dolby Digital +';

UPDATE quality_profile_custom_formats
SET score = 100
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'TrueHD';

UPDATE quality_profile_custom_formats
SET score = 100
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'DTS-X';
-- --- END op 96201
