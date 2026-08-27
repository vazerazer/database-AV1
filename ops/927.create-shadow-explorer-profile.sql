-- @operation: export
-- @entity: batch
-- @name: Create Movies SHADOW Explorer Quality Profile
-- @exportedAt: 2026-08-27T13:27:00.000Z
-- @opIds: 28270

-- ============================================================================
-- 1. QUALITY PROFILE
-- ============================================================================

INSERT INTO "quality_profiles" ("name", "description", "upgrades_allowed", "minimum_custom_format_score", "upgrade_until_score", "upgrade_score_increment")
VALUES 
  ('Movies SHADOW Explorer', 'Explorer arm profile with neutralized encoder tier bonuses (AV1 Quality & Compact set to 0) for unbiased discovery of promising untiered AV1 releases.', 1, 1000, 6000, 300)
ON CONFLICT ("name") DO UPDATE SET
  "description" = excluded."description",
  "minimum_custom_format_score" = excluded."minimum_custom_format_score",
  "upgrade_until_score" = excluded."upgrade_until_score",
  "upgrade_score_increment" = excluded."upgrade_score_increment";

-- Profile Tag
INSERT INTO "tags" ("name") VALUES ('AV1') ON CONFLICT ("name") DO NOTHING;
INSERT INTO "quality_profile_tags" ("quality_profile_name", "tag_name")
VALUES ('Movies SHADOW Explorer', 'AV1')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 2. QUALITY GROUPS & MEMBERS
-- ============================================================================

INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Movies SHADOW Explorer', '2160p Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Movies SHADOW Explorer', '1080p Fallback') ON CONFLICT DO NOTHING;

INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('Movies SHADOW Explorer', '2160p Group', 'Bluray-2160p', 0),
  ('Movies SHADOW Explorer', '2160p Group', 'Remux-2160p', 1),
  ('Movies SHADOW Explorer', '2160p Group', 'WEBDL-2160p', 2),
  ('Movies SHADOW Explorer', '2160p Group', 'WEBRip-2160p', 3),
  ('Movies SHADOW Explorer', '1080p Fallback', 'Bluray-1080p', 0),
  ('Movies SHADOW Explorer', '1080p Fallback', 'Remux-1080p', 1),
  ('Movies SHADOW Explorer', '1080p Fallback', 'WEBDL-1080p', 2),
  ('Movies SHADOW Explorer', '1080p Fallback', 'WEBRip-1080p', 3)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 3. QUALITY PROFILE QUALITIES (ORDER & CUTOFF)
-- ============================================================================

INSERT INTO "quality_profile_qualities" ("quality_profile_name", "quality_group_name", "position", "enabled", "upgrade_until")
VALUES
  ('Movies SHADOW Explorer', '2160p Group', 0, 1, 1),
  ('Movies SHADOW Explorer', '1080p Fallback', 1, 1, 0)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 4. CUSTOM FORMAT SCORING RULES
-- ============================================================================

-- Duplicate all base scoring rules from Movies 2160p AV1 HQ except tier bonuses
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES
  -- Universal Anti-Trash Hygiene (-10000)
  ('Movies SHADOW Explorer', 'CAM', 'all', -10000),
  ('Movies SHADOW Explorer', 'Upscale', 'all', -10000),
  ('Movies SHADOW Explorer', '3D', 'all', -10000),
  ('Movies SHADOW Explorer', 'Extras', 'all', -10000),
  ('Movies SHADOW Explorer', 'Sing Along', 'all', -10000),
  ('Movies SHADOW Explorer', 'Full Disc', 'all', -10000),
  ('Movies SHADOW Explorer', 'Full Disc (Quality Match)', 'all', -10000),
  ('Movies SHADOW Explorer', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('Movies SHADOW Explorer', 'Banned Groups', 'all', -10000),
  ('Movies SHADOW Explorer', 'Banned Groups (Compact)', 'all', -10000),
  ('Movies SHADOW Explorer', 'Banned Groups (Efficient)', 'all', -10000),
  ('Movies SHADOW Explorer', 'Banned Groups (Regular)', 'all', -10000),
  ('Movies SHADOW Explorer', 'Banned Groups (Release Title)', 'all', -10000),
  ('Movies SHADOW Explorer', 'Banned Remux', 'all', -10000),
  ('Movies SHADOW Explorer', 'Legacy x264 Codec', 'all', -5000),
  ('Movies SHADOW Explorer', '8-bit Depth', 'all', -1000),

  -- Canonical AV1 Boost
  ('Movies SHADOW Explorer', 'AV1', 'all', 3500),

  -- Sizing & Anti-Junk Bands (Junk still sinks, exploration only in plausible releases)
  ('Movies SHADOW Explorer', 'AV1 Micro 2160p', 'radarr', -2800),
  ('Movies SHADOW Explorer', 'AV1 Micro 1080p', 'radarr', -2800),
  ('Movies SHADOW Explorer', 'AV1 Lean 2160p', 'radarr', -3400),
  ('Movies SHADOW Explorer', 'AV1 Nameless', 'radarr', -2500),
  ('Movies SHADOW Explorer', 'Foreign Dub', 'radarr', -750),
  ('Movies SHADOW Explorer', 'Heavy 2160p Fallback', 'radarr', -400),
  ('Movies SHADOW Explorer', 'Oversized 2160p Fallback', 'radarr', -1500),
  ('Movies SHADOW Explorer', 'Extreme 2160p', 'radarr', -1500),
  ('Movies SHADOW Explorer', 'AV1 Storage Savers', 'all', -1000),
  ('Movies SHADOW Explorer', 'Not AV1', 'all', -2000),

  -- Video Enhancements
  ('Movies SHADOW Explorer', '10-bit Depth', 'all', 300),
  ('Movies SHADOW Explorer', 'Dolby Vision', 'all', 600),
  ('Movies SHADOW Explorer', 'HDR', 'all', 400),
  ('Movies SHADOW Explorer', 'HDR10+', 'all', 500),

  -- Audio Enhancements
  ('Movies SHADOW Explorer', 'TrueHD', 'all', 150),
  ('Movies SHADOW Explorer', 'Dolby Atmos', 'all', 150),
  ('Movies SHADOW Explorer', 'DTS-X', 'all', 150),
  ('Movies SHADOW Explorer', 'Lossless Audio', 'all', 100),
  ('Movies SHADOW Explorer', 'Dolby Digital +', 'all', 150),
  ('Movies SHADOW Explorer', 'Dolby Digital', 'all', 100),
  ('Movies SHADOW Explorer', 'Opus 5.1 / 7.1', 'all', 250),

  -- Editions & Streaming Services
  ('Movies SHADOW Explorer', 'Theatrical', 'all', 100),
  ('Movies SHADOW Explorer', 'CRIT', 'all', 100),
  ('Movies SHADOW Explorer', 'DSNP', 'all', 50),
  ('Movies SHADOW Explorer', 'AMZN', 'all', 50),
  ('Movies SHADOW Explorer', 'MAX', 'all', 50),
  ('Movies SHADOW Explorer', 'HULU', 'all', 50),

  -- Upstream Fallback Ladder Tiers
  ('Movies SHADOW Explorer', '2160p Quality Tier 1', 'all', 2850),
  ('Movies SHADOW Explorer', '2160p Quality Tier 2', 'all', 2750),
  ('Movies SHADOW Explorer', '2160p Quality Tier 3', 'all', 2700),
  ('Movies SHADOW Explorer', '2160p Quality Tier 4', 'all', 2650),
  ('Movies SHADOW Explorer', '2160p Balanced Tier 3', 'all', 2700),
  ('Movies SHADOW Explorer', 'WEB-DL Tier 1', 'all', 2850),
  ('Movies SHADOW Explorer', 'WEB-DL Tier 2', 'all', 2750),
  ('Movies SHADOW Explorer', 'WEB-DL Tier 3', 'all', 2700),
  ('Movies SHADOW Explorer', '1080p Quality Tier 1', 'all', 2850),
  ('Movies SHADOW Explorer', '1080p Quality Tier 2', 'all', 2750),
  ('Movies SHADOW Explorer', '1080p Quality Tier 3', 'all', 2700),
  ('Movies SHADOW Explorer', '1080p Balanced Tier 1', 'all', 2850),
  ('Movies SHADOW Explorer', '1080p Balanced Tier 2', 'all', 2750),
  ('Movies SHADOW Explorer', 'HONE Bluray', 'all', 2750),
  ('Movies SHADOW Explorer', 'HONE WEB', 'all', 2750),

  -- Neutralized Tier Bonuses for Explorer Arm (0 score)
  ('Movies SHADOW Explorer', 'AV1 Quality Encoders', 'all', 0),
  ('Movies SHADOW Explorer', 'AV1 Compact Encoders', 'all', 0)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET
  "score" = excluded."score";
