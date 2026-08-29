-- =============================================================================
-- Migration: 952.add-av1-unmeasured-encoders-tier4-scoring.sql
-- Description: Align AV1 Quality Encoders (Tier 1), Compact Encoders (Tier 2),
--              and create AV1 Unmeasured Encoders (Tier 4) with -2400 score
--              in Movies 2160p AV1 HQ to ensure unmeasured AV1 is strictly
--              below Tier 3 x265 while remaining >= 1001 grabbable.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 95201
-- 1. Align 'AV1 Quality Encoders' Regex (ChopperHitler, CoSMiCSuRFeR, UH, dAV1nci, Smokindevil, CHD, TAoE, PRL - excluding Waldek)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:CoSMiCSuRFeR|PRL|CHD|CHOPPERHITLER|ChopperHitler|TAoE|dAV1nci|UH|Smokindevil)\]|-(?:CoSMiCSuRFeR|PRL|CHD|CHOPPERHITLER|ChopperHitler|TAoE|dAV1nci|UH|Smokindevil|\[(?:CoSMiCSuRFeR|PRL|CHD|CHOPPERHITLER|ChopperHitler|TAoE|dAV1nci|UH|Smokindevil)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE name = 'AV1 Quality Encoders';

-- 2. Align 'AV1 Compact Encoders' Regex (RandH, Rob74K, WhiskeyJack, RAV1NE, UserHEVC, etc.)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH)\]|-(?:WhiskeyJack|WhiskyJack|edge2020|UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|\[(?:UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE name = 'AV1 Compact Encoders';

-- 3. Create Regular Expression for 'AV1 Unmeasured Encoders' (Bi0hazard, Waldek, SHADOW)
INSERT INTO regular_expressions (name, pattern, description)
VALUES (
  'AV1 Unmeasured Encoders',
  '(?i)(?:^\[(?:Bi0hazard|Biohazard|Waldek|SHADOW)\]|-(?:Bi0hazard|Biohazard|Waldek|SHADOW|\[(?:Bi0hazard|Biohazard|Waldek|SHADOW)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)',
  'Matches unmeasured and unvetted AV1 release groups for Tier 4 quarantine'
) ON CONFLICT (name) DO UPDATE SET pattern = EXCLUDED.pattern;

-- 4. Create Custom Format 'AV1 Unmeasured Encoders'
INSERT INTO custom_formats (name, description)
VALUES (
  'AV1 Unmeasured Encoders',
  'Matches 2160p AV1 releases from unmeasured/unvetted groups for Tier 4 quarantine scoring'
) ON CONFLICT (name) DO NOTHING;

INSERT INTO custom_format_tags (custom_format_name, tag_name)
VALUES ('AV1 Unmeasured Encoders', 'Resolution')
ON CONFLICT DO NOTHING;

-- 5. Define Conditions for 'AV1 Unmeasured Encoders'
-- Condition 1: 2160p Resolution (required)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Unmeasured Encoders', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('AV1 Unmeasured Encoders', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

-- Condition 2: AV1 Codec Marker (required)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Unmeasured Encoders', 'AV1 Codec', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Unmeasured Encoders', 'AV1 Codec', 'AV1')
ON CONFLICT DO NOTHING;

-- Condition 3: Unmeasured Group Marker (required)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Unmeasured Encoders', 'Unmeasured Group', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Unmeasured Encoders', 'Unmeasured Group', 'AV1 Unmeasured Encoders')
ON CONFLICT DO NOTHING;

-- 6. Score 'AV1 Unmeasured Encoders' in Movies 2160p AV1 HQ (-2400)
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, score, arr_type)
VALUES ('Movies 2160p AV1 HQ', 'AV1 Unmeasured Encoders', -2400, 'radarr')
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = -2400;

-- 7. Update 'AV1 Nameless' score to -2400 in Movies 2160p AV1 HQ
UPDATE quality_profile_custom_formats
SET score = -2400
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'AV1 Nameless';
-- --- END op 95201
