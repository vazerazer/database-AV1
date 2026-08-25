-- --- BEGIN op 90401 ( score Not AV1 and fallback tiers across 7 profiles )
-- 1. Remove Legacy x265 Codec penalty from the 7 AV1 profiles so it does not double-punish fallback tier releases
DELETE FROM quality_profile_custom_formats
WHERE custom_format_name = 'Legacy x265 Codec'
  AND quality_profile_name IN (
    'Movies 2160p AV1 HQ',
    'Movies 1080p AV1 HQ',
    'Movies 1080p AV1 Storage',
    'TV 2160p AV1',
    'TV 1080p AV1 HQ',
    'TV 1080p AV1 Storage',
    'Anime 1080p AV1'
  );

-- 2. Add Not AV1 (-2000) codec gate to all 7 profiles
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES
  ('Movies 2160p AV1 HQ', 'Not AV1', 'all', -2000),
  ('Movies 1080p AV1 HQ', 'Not AV1', 'all', -2000),
  ('Movies 1080p AV1 Storage', 'Not AV1', 'all', -2000),
  ('TV 2160p AV1', 'Not AV1', 'all', -2000),
  ('TV 1080p AV1 HQ', 'Not AV1', 'all', -2000),
  ('TV 1080p AV1 Storage', 'Not AV1', 'all', -2000),
  ('Anime 1080p AV1', 'Not AV1', 'all', -2000)
ON CONFLICT DO NOTHING;

-- 3. Add 2160p Fallback Tiers
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES
  ('Movies 2160p AV1 HQ', 'WEB-DL Tier 1', 'all', 1900),
  ('Movies 2160p AV1 HQ', 'WEB-DL Tier 2', 'all', 1800),
  ('Movies 2160p AV1 HQ', 'WEB-DL Tier 3', 'all', 1700),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 1', 'all', 1900),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 2', 'all', 1800),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 3', 'all', 1750),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 4', 'all', 1700),
  ('Movies 2160p AV1 HQ', 'HONE WEB', 'all', 1800),
  ('Movies 2160p AV1 HQ', 'HONE Bluray', 'all', 1800),
  
  ('TV 2160p AV1', 'WEB-DL Tier 1', 'all', 1900),
  ('TV 2160p AV1', 'WEB-DL Tier 2', 'all', 1800),
  ('TV 2160p AV1', 'WEB-DL Tier 3', 'all', 1700),
  ('TV 2160p AV1', '2160p Quality Tier 1', 'all', 1900),
  ('TV 2160p AV1', '2160p Quality Tier 2', 'all', 1800),
  ('TV 2160p AV1', '2160p Quality Tier 3', 'all', 1750),
  ('TV 2160p AV1', '2160p Quality Tier 4', 'all', 1700),
  ('TV 2160p AV1', 'HONE WEB', 'all', 1800),
  ('TV 2160p AV1', 'HONE Bluray', 'all', 1800)
ON CONFLICT DO NOTHING;

-- 4. Add 1080p Fallback Tiers
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES
  ('Movies 1080p AV1 HQ', 'WEB-DL Tier 1', 'all', 2400),
  ('Movies 1080p AV1 HQ', 'WEB-DL Tier 2', 'all', 2300),
  ('Movies 1080p AV1 HQ', 'WEB-DL Tier 3', 'all', 2200),
  ('Movies 1080p AV1 HQ', '1080p Quality Tier 1', 'all', 2400),
  ('Movies 1080p AV1 HQ', '1080p Quality Tier 2', 'all', 2300),
  ('Movies 1080p AV1 HQ', '1080p Quality Tier 3', 'all', 2200),
  ('Movies 1080p AV1 HQ', 'HONE WEB', 'all', 2300),
  ('Movies 1080p AV1 HQ', 'HONE Bluray', 'all', 2300),

  ('Movies 1080p AV1 Storage', 'WEB-DL Tier 1', 'all', 2400),
  ('Movies 1080p AV1 Storage', 'WEB-DL Tier 2', 'all', 2300),
  ('Movies 1080p AV1 Storage', 'WEB-DL Tier 3', 'all', 2200),
  ('Movies 1080p AV1 Storage', '1080p Quality Tier 1', 'all', 2400),
  ('Movies 1080p AV1 Storage', '1080p Quality Tier 2', 'all', 2300),
  ('Movies 1080p AV1 Storage', '1080p Quality Tier 3', 'all', 2200),
  ('Movies 1080p AV1 Storage', 'HONE WEB', 'all', 2300),
  ('Movies 1080p AV1 Storage', 'HONE Bluray', 'all', 2300),

  ('TV 1080p AV1 HQ', 'WEB-DL Tier 1', 'all', 2400),
  ('TV 1080p AV1 HQ', 'WEB-DL Tier 2', 'all', 2300),
  ('TV 1080p AV1 HQ', 'WEB-DL Tier 3', 'all', 2200),
  ('TV 1080p AV1 HQ', '1080p Quality Tier 1', 'all', 2400),
  ('TV 1080p AV1 HQ', '1080p Quality Tier 2', 'all', 2300),
  ('TV 1080p AV1 HQ', '1080p Quality Tier 3', 'all', 2200),
  ('TV 1080p AV1 HQ', 'HONE WEB', 'all', 2300),
  ('TV 1080p AV1 HQ', 'HONE Bluray', 'all', 2300),

  ('TV 1080p AV1 Storage', 'WEB-DL Tier 1', 'all', 2400),
  ('TV 1080p AV1 Storage', 'WEB-DL Tier 2', 'all', 2300),
  ('TV 1080p AV1 Storage', 'WEB-DL Tier 3', 'all', 2200),
  ('TV 1080p AV1 Storage', '1080p Quality Tier 1', 'all', 2400),
  ('TV 1080p AV1 Storage', '1080p Quality Tier 2', 'all', 2300),
  ('TV 1080p AV1 Storage', '1080p Quality Tier 3', 'all', 2200),
  ('TV 1080p AV1 Storage', 'HONE WEB', 'all', 2300),
  ('TV 1080p AV1 Storage', 'HONE Bluray', 'all', 2300),

  ('Anime 1080p AV1', 'WEB-DL Tier 1', 'all', 2400),
  ('Anime 1080p AV1', 'WEB-DL Tier 2', 'all', 2300),
  ('Anime 1080p AV1', 'WEB-DL Tier 3', 'all', 2200),
  ('Anime 1080p AV1', '1080p Quality Tier 1', 'all', 2400),
  ('Anime 1080p AV1', '1080p Quality Tier 2', 'all', 2300),
  ('Anime 1080p AV1', '1080p Quality Tier 3', 'all', 2200),
  ('Anime 1080p AV1', 'HONE WEB', 'all', 2300),
  ('Anime 1080p AV1', 'HONE Bluray', 'all', 2300)
ON CONFLICT DO NOTHING;
-- --- END op 90401
