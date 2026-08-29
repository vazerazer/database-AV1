-- @operation: export
-- @entity: batch
-- @name: Deprecate All Unused Profiles (Streamline to Movies 2160p AV1 HQ)
-- @exportedAt: 2026-08-29T09:56:00.000Z
-- @opIds: 28601, 28602, 28603, 28604, 28605, 28606

-- ============================================================================
-- 1. DELETE CUSTOM FORMAT SCORING RULES FOR DEPRECATED PROFILES
-- ============================================================================

DELETE FROM quality_profile_custom_formats
WHERE quality_profile_name IN (
  'Movies SHADOW Explorer',
  'Anime 1080p AV1',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage'
);

-- ============================================================================
-- 2. DELETE QUALITY PROFILE QUALITIES & QUALITY GROUPS
-- ============================================================================

DELETE FROM quality_profile_qualities
WHERE quality_profile_name IN (
  'Movies SHADOW Explorer',
  'Anime 1080p AV1',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage'
);

DELETE FROM quality_group_members
WHERE quality_profile_name IN (
  'Movies SHADOW Explorer',
  'Anime 1080p AV1',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage'
);

DELETE FROM quality_groups
WHERE quality_profile_name IN (
  'Movies SHADOW Explorer',
  'Anime 1080p AV1',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage'
);

-- ============================================================================
-- 3. DELETE QUALITY PROFILE TAGS
-- ============================================================================

DELETE FROM quality_profile_tags
WHERE quality_profile_name IN (
  'Movies SHADOW Explorer',
  'Anime 1080p AV1',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage'
);

-- ============================================================================
-- 4. DELETE QUALITY PROFILES
-- ============================================================================

DELETE FROM quality_profiles
WHERE name IN (
  'Movies SHADOW Explorer',
  'Anime 1080p AV1',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage'
);
