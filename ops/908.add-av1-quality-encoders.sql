-- =============================================================================
-- Migration: 908.add-av1-quality-encoders.sql
-- Description: Create 'AV1 Quality Encoders' custom format for high-bitrate/40GB
--              AV1 releases (starting with CoSMiCSuRFeR), score +1000 in HQ profiles,
--              penalize -1000 in Storage profiles, and set CAM condition arr_type='all'.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 90801
-- 1. Create Regular Expression for AV1 Quality Encoders
INSERT INTO regular_expressions (name, pattern, description)
VALUES (
  'AV1 Quality Encoders',
  '(?i)(?:^\[(?:CoSMiCSuRFeR)\]|-(?:CoSMiCSuRFeR|\[CoSMiCSuRFeR\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)',
  'Matches high-bitrate quality-first AV1 encode groups'
) ON CONFLICT DO NOTHING;

-- 2. Create Custom Format 'AV1 Quality Encoders'
INSERT INTO custom_formats (name, description)
VALUES (
  'AV1 Quality Encoders',
  'Matches quality-first, high-bitrate AV1 encoding groups (e.g. CoSMiCSuRFeR)'
) ON CONFLICT DO NOTHING;

-- 3. Create Condition for 'AV1 Quality Encoders'
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES (
  'AV1 Quality Encoders',
  'Quality Encoder',
  'release_title',
  'all',
  0,
  1
) ON CONFLICT DO NOTHING;

-- 4. Link Condition to Regular Expression
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES (
  'AV1 Quality Encoders',
  'Quality Encoder',
  'AV1 Quality Encoders'
) ON CONFLICT DO NOTHING;

-- 5. Score 'AV1 Quality Encoders' in Quality Profiles
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES
  ('Movies 2160p AV1 HQ', 'AV1 Quality Encoders', 'all', 1000),
  ('Movies 1080p AV1 HQ', 'AV1 Quality Encoders', 'all', 1000),
  ('TV 2160p AV1', 'AV1 Quality Encoders', 'all', 1000),
  ('TV 1080p AV1 HQ', 'AV1 Quality Encoders', 'all', 1000),
  ('Anime 1080p AV1', 'AV1 Quality Encoders', 'all', 1000),
  ('Movies 1080p AV1 Storage', 'AV1 Quality Encoders', 'all', -1000),
  ('TV 1080p AV1 Storage', 'AV1 Quality Encoders', 'all', -1000)
ON CONFLICT DO NOTHING;

-- 6. Update CAM Condition arr_type to 'all' for Sonarr Sync
UPDATE custom_format_conditions
SET arr_type = 'all'
WHERE custom_format_name = 'CAM';
-- --- END op 90801
