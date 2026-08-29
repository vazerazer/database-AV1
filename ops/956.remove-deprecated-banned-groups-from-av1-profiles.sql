-- @operation: export
-- @entity: batch
-- @name: Remove Deprecated Banned Group References From AV1 Profiles
-- @exportedAt: 2026-08-29T09:43:00.000Z
-- @opIds: 28501, 28502, 28503, 28504, 28505, 28506, 28507, 28508

-- ============================================================================
-- 1. CLEAN UP DEPRECATED BANNED GROUPS (COMPACT)
-- ============================================================================

DELETE FROM quality_profile_custom_formats
WHERE custom_format_name = 'Banned Groups (Compact)'
  AND quality_profile_name IN (
    'Movies 2160p AV1 HQ',
    'Movies 1080p AV1 HQ',
    'Movies 1080p AV1 Storage',
    'TV 2160p AV1',
    'TV 1080p AV1 HQ',
    'TV 1080p AV1 Storage',
    'Anime 1080p AV1',
    'Movies SHADOW Explorer'
  );

-- ============================================================================
-- 2. CLEAN UP DEPRECATED BANNED GROUPS (RELEASE TITLE)
-- ============================================================================

DELETE FROM quality_profile_custom_formats
WHERE custom_format_name = 'Banned Groups (Release Title)'
  AND quality_profile_name IN (
    'Movies 2160p AV1 HQ',
    'Movies 1080p AV1 HQ',
    'Movies 1080p AV1 Storage',
    'TV 2160p AV1',
    'TV 1080p AV1 HQ',
    'TV 1080p AV1 Storage',
    'Anime 1080p AV1',
    'Movies SHADOW Explorer'
  );

-- ============================================================================
-- 3. ALIGN MOVIES SHADOW EXPLORER WITH OP 952A TIER 4 SCORING
-- ============================================================================

UPDATE quality_profile_custom_formats
SET score = -2400
WHERE quality_profile_name = 'Movies SHADOW Explorer'
  AND custom_format_name = 'AV1 Nameless';

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES ('Movies SHADOW Explorer', 'AV1 Unmeasured Encoders', 'all', -2400)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = -2400;
