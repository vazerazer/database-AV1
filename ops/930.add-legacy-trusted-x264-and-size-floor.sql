-- @operation: export
-- @entity: batch
-- @name: Add Legacy Trusted x264 and Micro Hard Floor Custom Formats
-- @exportedAt: 2026-08-27T15:47:00.000Z
-- @opIds: 28930, 28931, 28932, 28933

-- ============================================================================
-- 1. REGULAR EXPRESSIONS
-- ============================================================================

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES 
  ('LEGACY_TRUSTED_X264', '(?i)(?:^|[\s._-])(?:CtrlHD|GRiM|PiRaTeS|BHDStudio|TAoE|DON|EbP|playHD|Z0N3|LoRD|MrTentsaw)(?:\[[^\]]*\])?(?:\.[a-z0-9]{2,4})?$', 'Matches trusted reference legacy x264 release groups'),
  ('PiRaTeS', '(?i)\bPiRaTeS\b', 'PiRaTeS release group'),
  ('Z0N3', '(?i)\bZ0N3\b', 'Z0N3 release group'),
  ('playHD', '(?i)\bplayHD\b', 'playHD release group'),
  ('GRiM', '(?i)\bGRiM\b', 'GRiM release group'),
  ('MrTentsaw', '(?i)\bMrTentsaw\b', 'MrTentsaw release group')
ON CONFLICT ("name") DO UPDATE SET
  "pattern" = excluded."pattern",
  "description" = excluded."description";

-- ============================================================================
-- 2. EXPAND 1080P QUALITY TIER 2 WITH LEGACY GROUPS
-- ============================================================================

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES 
  ('1080p Quality Tier 2', 'PiRaTeS', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'Z0N3', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'playHD', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'GRiM', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'MrTentsaw', 'release_group', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES 
  ('1080p Quality Tier 2', 'PiRaTeS', 'PiRaTeS'),
  ('1080p Quality Tier 2', 'Z0N3', 'Z0N3'),
  ('1080p Quality Tier 2', 'playHD', 'playHD'),
  ('1080p Quality Tier 2', 'GRiM', 'GRiM'),
  ('1080p Quality Tier 2', 'MrTentsaw', 'MrTentsaw')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 3. CUSTOM FORMATS & CONDITIONS
-- ============================================================================

-- A. Micro Hard Floor (Rejects sub-1GB feature film releases across all profiles)
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Micro Hard Floor', 'Matches sub-1GB feature film releases (< 1.0 GB) for hard rejection')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Micro Hard Floor', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES ('Micro Hard Floor', 'Sub-1GB Hard Floor Size', 'size', 'radarr', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_sizes" ("custom_format_name", "condition_name", "min_bytes", "max_bytes")
VALUES ('Micro Hard Floor', 'Sub-1GB Hard Floor Size', 0, 1073741824)
ON CONFLICT DO NOTHING;

-- B. Legacy Trusted x264
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Legacy Trusted x264', 'Lifts reference x264 encodes from trusted archival groups above profile cutoff score')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Legacy Trusted x264', 'Codec') ON CONFLICT DO NOTHING;

-- Condition 1: Must match Legacy x264 Codec
INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES ('Legacy Trusted x264', 'x264 Codec Condition', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES ('Legacy Trusted x264', 'x264 Codec Condition', 'Legacy x264 Codec')
ON CONFLICT DO NOTHING;

-- Condition 2: Must match trusted legacy groups
INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES ('Legacy Trusted x264', 'Trusted Legacy Group Condition', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES ('Legacy Trusted x264', 'Trusted Legacy Group Condition', 'LEGACY_TRUSTED_X264')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 4. PROFILE SCORING RULES
-- ============================================================================

-- Profile 64 (Movies 2160p AV1 HQ)
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES 
  ('Movies 2160p AV1 HQ', 'Micro Hard Floor', 'radarr', -10000),
  ('Movies 2160p AV1 HQ', 'Legacy Trusted x264', 'radarr', 5400)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET
  "score" = excluded."score";

-- Profile 67 (Movies SHADOW Explorer)
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES 
  ('Movies SHADOW Explorer', 'Micro Hard Floor', 'radarr', -10000),
  ('Movies SHADOW Explorer', 'Legacy Trusted x264', 'radarr', 5400)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET
  "score" = excluded."score";
