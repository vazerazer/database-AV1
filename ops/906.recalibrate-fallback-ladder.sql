-- =============================================================================
-- Migration: 906.recalibrate-fallback-ladder.sql
-- Description: Recalibrate fallback ladder scoring for SDR 2160p WEB-DL,
--              hallowed-class 2160p BluRay HDR10+, 1080p fallbacks in 2160p,
--              wire Dolby Digital +, and elevate canonical AV1 (+3500).
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 90601
-- 1. Elevate Canonical AV1 Codec score to +3500 across all 7 AV1 quality profiles
UPDATE quality_profile_custom_formats
SET score = 3500
WHERE custom_format_name = 'AV1'
  AND quality_profile_name IN (
    'Movies 2160p AV1 HQ',
    'Movies 1080p AV1 HQ',
    'Movies 1080p AV1 Storage',
    'TV 2160p AV1',
    'TV 1080p AV1 HQ',
    'TV 1080p AV1 Storage',
    'Anime 1080p AV1'
  );

-- 2. Adjust Profile Upgrade Until Scores
UPDATE quality_profiles SET upgrade_until_score = 6000 WHERE name IN ('Movies 2160p AV1 HQ', 'TV 2160p AV1');
UPDATE quality_profiles SET upgrade_until_score = 5000 WHERE name IN ('Movies 1080p AV1 HQ', 'TV 1080p AV1 HQ', 'Anime 1080p AV1');
UPDATE quality_profiles SET upgrade_until_score = 3500 WHERE name IN ('Movies 1080p AV1 Storage', 'TV 1080p AV1 Storage');

-- 3. Update existing 2160p fallback tier scores in 2160p profiles
UPDATE quality_profile_custom_formats SET score = 2850 WHERE custom_format_name IN ('WEB-DL Tier 1', '2160p Quality Tier 1') AND quality_profile_name IN ('Movies 2160p AV1 HQ', 'TV 2160p AV1');
UPDATE quality_profile_custom_formats SET score = 2750 WHERE custom_format_name IN ('WEB-DL Tier 2', '2160p Quality Tier 2', 'HONE WEB', 'HONE Bluray') AND quality_profile_name IN ('Movies 2160p AV1 HQ', 'TV 2160p AV1');
UPDATE quality_profile_custom_formats SET score = 2700 WHERE custom_format_name IN ('WEB-DL Tier 3', '2160p Quality Tier 3') AND quality_profile_name IN ('Movies 2160p AV1 HQ', 'TV 2160p AV1');
UPDATE quality_profile_custom_formats SET score = 2650 WHERE custom_format_name = '2160p Quality Tier 4' AND quality_profile_name IN ('Movies 2160p AV1 HQ', 'TV 2160p AV1');

-- 4. Update existing 1080p fallback tier scores in 1080p profiles
UPDATE quality_profile_custom_formats SET score = 2850 WHERE custom_format_name IN ('WEB-DL Tier 1', '1080p Quality Tier 1') AND quality_profile_name IN ('Movies 1080p AV1 HQ', 'Movies 1080p AV1 Storage', 'TV 1080p AV1 HQ', 'TV 1080p AV1 Storage', 'Anime 1080p AV1');
UPDATE quality_profile_custom_formats SET score = 2750 WHERE custom_format_name IN ('WEB-DL Tier 2', '1080p Quality Tier 2', 'HONE WEB', 'HONE Bluray') AND quality_profile_name IN ('Movies 1080p AV1 HQ', 'Movies 1080p AV1 Storage', 'TV 1080p AV1 HQ', 'TV 1080p AV1 Storage', 'Anime 1080p AV1');
UPDATE quality_profile_custom_formats SET score = 2700 WHERE custom_format_name IN ('WEB-DL Tier 3', '1080p Quality Tier 3') AND quality_profile_name IN ('Movies 1080p AV1 HQ', 'Movies 1080p AV1 Storage', 'TV 1080p AV1 HQ', 'TV 1080p AV1 Storage', 'Anime 1080p AV1');

-- 5. Wire Dolby Digital + and Balanced Tier 3 (hallowed) and 1080p fallback tiers in 2160p profiles
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES
  -- Dolby Digital + across all profiles
  ('Movies 2160p AV1 HQ', 'Dolby Digital +', 'all', 150),
  ('Movies 1080p AV1 HQ', 'Dolby Digital +', 'all', 150),
  ('Movies 1080p AV1 Storage', 'Dolby Digital +', 'all', 150),
  ('TV 2160p AV1', 'Dolby Digital +', 'all', 150),
  ('TV 1080p AV1 HQ', 'Dolby Digital +', 'all', 150),
  ('TV 1080p AV1 Storage', 'Dolby Digital +', 'all', 150),
  ('Anime 1080p AV1', 'Dolby Digital +', 'all', 150),

  -- 2160p Balanced Tier 3 (hallowed)
  ('Movies 2160p AV1 HQ', '2160p Balanced Tier 3', 'all', 2700),
  ('TV 2160p AV1', '2160p Balanced Tier 3', 'all', 2700),

  -- 1080p Fallback Tiers wired into 2160p profiles
  ('Movies 2160p AV1 HQ', '1080p Quality Tier 1', 'all', 2850),
  ('Movies 2160p AV1 HQ', '1080p Quality Tier 2', 'all', 2750),
  ('Movies 2160p AV1 HQ', '1080p Quality Tier 3', 'all', 2700),
  ('Movies 2160p AV1 HQ', '1080p Balanced Tier 1', 'all', 2850),
  ('Movies 2160p AV1 HQ', '1080p Balanced Tier 2', 'all', 2750),

  ('TV 2160p AV1', '1080p Quality Tier 1', 'all', 2850),
  ('TV 2160p AV1', '1080p Quality Tier 2', 'all', 2750),
  ('TV 2160p AV1', '1080p Quality Tier 3', 'all', 2700),
  ('TV 2160p AV1', '1080p Balanced Tier 1', 'all', 2850),
  ('TV 2160p AV1', '1080p Balanced Tier 2', 'all', 2750),

  -- 1080p Balanced Tiers wired into 1080p profiles
  ('Movies 1080p AV1 HQ', '1080p Balanced Tier 1', 'all', 2850),
  ('Movies 1080p AV1 HQ', '1080p Balanced Tier 2', 'all', 2750),
  ('Movies 1080p AV1 Storage', '1080p Balanced Tier 1', 'all', 2850),
  ('Movies 1080p AV1 Storage', '1080p Balanced Tier 2', 'all', 2750),
  ('TV 1080p AV1 HQ', '1080p Balanced Tier 1', 'all', 2850),
  ('TV 1080p AV1 HQ', '1080p Balanced Tier 2', 'all', 2750),
  ('TV 1080p AV1 Storage', '1080p Balanced Tier 1', 'all', 2850),
  ('TV 1080p AV1 Storage', '1080p Balanced Tier 2', 'all', 2750),
  ('Anime 1080p AV1', '1080p Balanced Tier 1', 'all', 2850),
  ('Anime 1080p AV1', '1080p Balanced Tier 2', 'all', 2750)
ON CONFLICT DO NOTHING;
-- --- END op 90601
