-- @operation: export
-- @entity: batch
-- @name: Create AV1 Master Quality Profiles and Scoring Rules
-- @exportedAt: 2026-08-24T21:07:00.000Z
-- @opIds: 28201, 28202, 28203, 28204, 28205, 28206, 28207

-- ============================================================================
-- 1. QUALITY PROFILES
-- ============================================================================

INSERT INTO "quality_profiles" ("name", "description", "upgrades_allowed", "minimum_custom_format_score", "upgrade_until_score", "upgrade_score_increment")
VALUES 
  ('Movies 2160p AV1 HQ', 'Premium 4K AV1 movie profile with HDR10+/Dolby Vision, lossless master audio and strict non-AV1 leak isolation.', 1, 1000, 3500, 1),
  ('Movies 1080p AV1 HQ', 'Reference 1080p 10-bit AV1 movie profile with Opus/FLAC audio and Criterion/Remaster scoring.', 1, 500, 2500, 1),
  ('Movies 1080p AV1 Storage', 'Storage-optimized 1080p AV1 movie profile for maximum efficiency and secondary libraries.', 1, 200, 1500, 1),
  ('TV 2160p AV1', '4K UHD AV1 episodic profile for high-efficiency 4K HDR television.', 1, 1000, 3500, 1),
  ('TV 1080p AV1 HQ', 'High-fidelity 1080p 10-bit AV1 episodic profile with multi-channel audio.', 1, 500, 2500, 1),
  ('TV 1080p AV1 Storage', 'Ultra-compact 1080p AV1 episodic profile for complete season archive efficiency.', 1, 200, 1500, 1),
  ('Anime 1080p AV1', 'Curated 1080p 10-bit AV1 anime profile with Dual-Audio, multi-sub fansubs and lossless audio scoring.', 1, 500, 3000, 1)
ON CONFLICT ("name") DO NOTHING;

-- Tags
INSERT INTO "tags" ("name") VALUES ('AV1') ON CONFLICT ("name") DO NOTHING;
INSERT INTO "quality_profile_tags" ("quality_profile_name", "tag_name")
VALUES 
  ('Movies 2160p AV1 HQ', 'AV1'),
  ('Movies 1080p AV1 HQ', 'AV1'),
  ('Movies 1080p AV1 Storage', 'AV1'),
  ('TV 2160p AV1', 'AV1'),
  ('TV 1080p AV1 HQ', 'AV1'),
  ('TV 1080p AV1 Storage', 'AV1'),
  ('Anime 1080p AV1', 'AV1')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 2. QUALITY GROUPS & MEMBERS
-- ============================================================================

-- Movies 2160p AV1 HQ
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Movies 2160p AV1 HQ', '2160p Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Movies 2160p AV1 HQ', '1080p Fallback') ON CONFLICT DO NOTHING;

INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('Movies 2160p AV1 HQ', '2160p Group', 'Bluray-2160p', 0),
  ('Movies 2160p AV1 HQ', '2160p Group', 'Remux-2160p', 1),
  ('Movies 2160p AV1 HQ', '2160p Group', 'WEBDL-2160p', 2),
  ('Movies 2160p AV1 HQ', '2160p Group', 'WEBRip-2160p', 3),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'Bluray-1080p', 0),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'Remux-1080p', 1),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'WEBDL-1080p', 2),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'WEBRip-1080p', 3)
ON CONFLICT DO NOTHING;

-- Movies 1080p AV1 HQ
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Movies 1080p AV1 HQ', '1080p Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('Movies 1080p AV1 HQ', '1080p Group', 'Bluray-1080p', 0),
  ('Movies 1080p AV1 HQ', '1080p Group', 'Remux-1080p', 1),
  ('Movies 1080p AV1 HQ', '1080p Group', 'WEBDL-1080p', 2),
  ('Movies 1080p AV1 HQ', '1080p Group', 'WEBRip-1080p', 3)
ON CONFLICT DO NOTHING;

-- Movies 1080p AV1 Storage
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Movies 1080p AV1 Storage', '1080p Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('Movies 1080p AV1 Storage', '1080p Group', 'Bluray-1080p', 0),
  ('Movies 1080p AV1 Storage', '1080p Group', 'Remux-1080p', 1),
  ('Movies 1080p AV1 Storage', '1080p Group', 'WEBDL-1080p', 2),
  ('Movies 1080p AV1 Storage', '1080p Group', 'WEBRip-1080p', 3)
ON CONFLICT DO NOTHING;

-- TV 2160p AV1
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('TV 2160p AV1', '2160p TV Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('TV 2160p AV1', '1080p TV Fallback') ON CONFLICT DO NOTHING;
INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('TV 2160p AV1', '2160p TV Group', 'WEBDL-2160p', 0),
  ('TV 2160p AV1', '2160p TV Group', 'WEBRip-2160p', 1),
  ('TV 2160p AV1', '2160p TV Group', 'Bluray-2160p', 2),
  ('TV 2160p AV1', '2160p TV Group', 'HDTV-2160p', 3),
  ('TV 2160p AV1', '1080p TV Fallback', 'WEBDL-1080p', 0),
  ('TV 2160p AV1', '1080p TV Fallback', 'WEBRip-1080p', 1),
  ('TV 2160p AV1', '1080p TV Fallback', 'Bluray-1080p', 2),
  ('TV 2160p AV1', '1080p TV Fallback', 'HDTV-1080p', 3)
ON CONFLICT DO NOTHING;

-- TV 1080p AV1 HQ
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('TV 1080p AV1 HQ', '1080p TV Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('TV 1080p AV1 HQ', '1080p TV Group', 'WEBDL-1080p', 0),
  ('TV 1080p AV1 HQ', '1080p TV Group', 'WEBRip-1080p', 1),
  ('TV 1080p AV1 HQ', '1080p TV Group', 'Bluray-1080p', 2),
  ('TV 1080p AV1 HQ', '1080p TV Group', 'HDTV-1080p', 3)
ON CONFLICT DO NOTHING;

-- TV 1080p AV1 Storage
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('TV 1080p AV1 Storage', '1080p TV Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('TV 1080p AV1 Storage', '1080p TV Group', 'WEBDL-1080p', 0),
  ('TV 1080p AV1 Storage', '1080p TV Group', 'WEBRip-1080p', 1),
  ('TV 1080p AV1 Storage', '1080p TV Group', 'Bluray-1080p', 2),
  ('TV 1080p AV1 Storage', '1080p TV Group', 'HDTV-1080p', 3)
ON CONFLICT DO NOTHING;

-- Anime 1080p AV1
INSERT INTO "quality_groups" ("quality_profile_name", "name") VALUES ('Anime 1080p AV1', 'Anime 1080p Group') ON CONFLICT DO NOTHING;
INSERT INTO "quality_group_members" ("quality_profile_name", "quality_group_name", "quality_name", "position")
VALUES
  ('Anime 1080p AV1', 'Anime 1080p Group', 'Bluray-1080p', 0),
  ('Anime 1080p AV1', 'Anime 1080p Group', 'Remux-1080p', 1),
  ('Anime 1080p AV1', 'Anime 1080p Group', 'WEBDL-1080p', 2),
  ('Anime 1080p AV1', 'Anime 1080p Group', 'WEBRip-1080p', 3)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 3. QUALITY PROFILE QUALITIES (ORDER & CUTOFF)
-- ============================================================================

INSERT INTO "quality_profile_qualities" ("quality_profile_name", "quality_group_name", "position", "enabled", "upgrade_until")
VALUES
  ('Movies 2160p AV1 HQ', '2160p Group', 0, 1, 1),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 1, 1, 0),
  ('Movies 1080p AV1 HQ', '1080p Group', 0, 1, 1),
  ('Movies 1080p AV1 Storage', '1080p Group', 0, 1, 1),
  ('TV 2160p AV1', '2160p TV Group', 0, 1, 1),
  ('TV 2160p AV1', '1080p TV Fallback', 1, 1, 0),
  ('TV 1080p AV1 HQ', '1080p TV Group', 0, 1, 1),
  ('TV 1080p AV1 Storage', '1080p TV Group', 0, 1, 1),
  ('Anime 1080p AV1', 'Anime 1080p Group', 0, 1, 1)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 4. CUSTOM FORMAT SCORING RULES
-- ============================================================================

-- Helper procedure for batch profile scoring
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES
  -- -------------------------------------------------------------------------
  -- UNIVERSAL ANTI-TRASH HYGIENE (-10000 across all 7 profiles)
  -- -------------------------------------------------------------------------
  ('Movies 2160p AV1 HQ', 'CAM', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Upscale', 'all', -10000),
  ('Movies 2160p AV1 HQ', '3D', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Extras', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Sing Along', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Full Disc', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Full Disc (Quality Match)', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Groups', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Groups (Compact)', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Groups (Efficient)', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Groups (Regular)', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Groups (Release Title)', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Remux', 'all', -10000),
  ('Movies 2160p AV1 HQ', 'Legacy x264 Codec', 'all', -5000),
  ('Movies 2160p AV1 HQ', '8-bit Depth', 'all', -1000),

  ('Movies 1080p AV1 HQ', 'CAM', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Upscale', 'all', -10000),
  ('Movies 1080p AV1 HQ', '3D', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Extras', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Sing Along', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Full Disc', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Full Disc (Quality Match)', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Banned Groups', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Banned Groups (Compact)', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Banned Groups (Efficient)', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Banned Groups (Regular)', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Banned Groups (Release Title)', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Banned Remux', 'all', -10000),
  ('Movies 1080p AV1 HQ', 'Legacy x264 Codec', 'all', -5000),
  ('Movies 1080p AV1 HQ', '8-bit Depth', 'all', -1000),

  ('Movies 1080p AV1 Storage', 'CAM', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Upscale', 'all', -10000),
  ('Movies 1080p AV1 Storage', '3D', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Extras', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Sing Along', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Full Disc', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Full Disc (Quality Match)', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Banned Groups', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Banned Groups (Compact)', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Banned Groups (Efficient)', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Banned Groups (Regular)', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Banned Groups (Release Title)', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Banned Remux', 'all', -10000),
  ('Movies 1080p AV1 Storage', 'Legacy x264 Codec', 'all', -5000),
  ('Movies 1080p AV1 Storage', '8-bit Depth', 'all', -1000),

  ('TV 2160p AV1', 'CAM', 'all', -10000),
  ('TV 2160p AV1', 'Upscale', 'all', -10000),
  ('TV 2160p AV1', '3D', 'all', -10000),
  ('TV 2160p AV1', 'Extras', 'all', -10000),
  ('TV 2160p AV1', 'Sing Along', 'all', -10000),
  ('TV 2160p AV1', 'Full Disc', 'all', -10000),
  ('TV 2160p AV1', 'Full Disc (Quality Match)', 'all', -10000),
  ('TV 2160p AV1', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('TV 2160p AV1', 'Banned Groups', 'all', -10000),
  ('TV 2160p AV1', 'Banned Groups (Compact)', 'all', -10000),
  ('TV 2160p AV1', 'Banned Groups (Efficient)', 'all', -10000),
  ('TV 2160p AV1', 'Banned Groups (Regular)', 'all', -10000),
  ('TV 2160p AV1', 'Banned Groups (Release Title)', 'all', -10000),
  ('TV 2160p AV1', 'Banned Remux', 'all', -10000),
  ('TV 2160p AV1', 'Legacy x264 Codec', 'all', -5000),
  ('TV 2160p AV1', '8-bit Depth', 'all', -1000),

  ('TV 1080p AV1 HQ', 'CAM', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Upscale', 'all', -10000),
  ('TV 1080p AV1 HQ', '3D', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Extras', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Sing Along', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Full Disc', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Full Disc (Quality Match)', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Banned Groups', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Banned Groups (Compact)', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Banned Groups (Efficient)', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Banned Groups (Regular)', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Banned Groups (Release Title)', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Banned Remux', 'all', -10000),
  ('TV 1080p AV1 HQ', 'Legacy x264 Codec', 'all', -5000),
  ('TV 1080p AV1 HQ', '8-bit Depth', 'all', -1000),

  ('TV 1080p AV1 Storage', 'CAM', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Upscale', 'all', -10000),
  ('TV 1080p AV1 Storage', '3D', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Extras', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Sing Along', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Full Disc', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Full Disc (Quality Match)', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Banned Groups', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Banned Groups (Compact)', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Banned Groups (Efficient)', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Banned Groups (Regular)', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Banned Groups (Release Title)', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Banned Remux', 'all', -10000),
  ('TV 1080p AV1 Storage', 'Legacy x264 Codec', 'all', -5000),
  ('TV 1080p AV1 Storage', '8-bit Depth', 'all', -1000),

  ('Anime 1080p AV1', 'CAM', 'all', -10000),
  ('Anime 1080p AV1', 'Upscale', 'all', -10000),
  ('Anime 1080p AV1', '3D', 'all', -10000),
  ('Anime 1080p AV1', 'Extras', 'all', -10000),
  ('Anime 1080p AV1', 'Sing Along', 'all', -10000),
  ('Anime 1080p AV1', 'Full Disc', 'all', -10000),
  ('Anime 1080p AV1', 'Full Disc (Quality Match)', 'all', -10000),
  ('Anime 1080p AV1', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('Anime 1080p AV1', 'Banned Groups', 'all', -10000),
  ('Anime 1080p AV1', 'Banned Groups (Compact)', 'all', -10000),
  ('Anime 1080p AV1', 'Banned Groups (Efficient)', 'all', -10000),
  ('Anime 1080p AV1', 'Banned Groups (Regular)', 'all', -10000),
  ('Anime 1080p AV1', 'Banned Groups (Release Title)', 'all', -10000),
  ('Anime 1080p AV1', 'Banned Remux', 'all', -10000),
  ('Anime 1080p AV1', 'Legacy x264 Codec', 'all', -5000),
  ('Anime 1080p AV1', '8-bit Depth', 'all', -1000),

  -- -------------------------------------------------------------------------
  -- MOVIES 2160p AV1 HQ SCORING
  -- -------------------------------------------------------------------------
  ('Movies 2160p AV1 HQ', 'AV1', 'all', 2000),
  ('Movies 2160p AV1 HQ', 'Legacy x265 Codec', 'all', -3500),
  ('Movies 2160p AV1 HQ', 'Dolby Vision', 'all', 600),
  ('Movies 2160p AV1 HQ', 'HDR10+', 'all', 500),
  ('Movies 2160p AV1 HQ', 'HDR', 'all', 400),
  ('Movies 2160p AV1 HQ', '10-bit Depth', 'all', 300),
  ('Movies 2160p AV1 HQ', 'Dolby Atmos', 'all', 350),
  ('Movies 2160p AV1 HQ', 'TrueHD', 'all', 300),
  ('Movies 2160p AV1 HQ', 'DTS-X', 'all', 300),
  ('Movies 2160p AV1 HQ', 'Opus 5.1 / 7.1', 'all', 250),
  ('Movies 2160p AV1 HQ', 'Lossless Audio', 'all', 250),
  ('Movies 2160p AV1 HQ', 'Dolby Digital', 'all', 150),
  ('Movies 2160p AV1 HQ', 'AV1 Compact Encoders', 'all', 500),
  ('Movies 2160p AV1 HQ', 'AV1 Storage Savers', 'all', -1000),
  ('Movies 2160p AV1 HQ', 'AMZN', 'all', 50),
  ('Movies 2160p AV1 HQ', 'DSNP', 'all', 50),
  ('Movies 2160p AV1 HQ', 'MAX', 'all', 50),
  ('Movies 2160p AV1 HQ', 'HULU', 'all', 50),
  ('Movies 2160p AV1 HQ', 'CRIT', 'all', 100),
  ('Movies 2160p AV1 HQ', 'Theatrical', 'all', 100),

  -- -------------------------------------------------------------------------
  -- MOVIES 1080p AV1 HQ SCORING
  -- -------------------------------------------------------------------------
  ('Movies 1080p AV1 HQ', 'AV1', 'all', 2000),
  ('Movies 1080p AV1 HQ', 'Legacy x265 Codec', 'all', -2000),
  ('Movies 1080p AV1 HQ', '10-bit Depth', 'all', 300),
  ('Movies 1080p AV1 HQ', 'Dolby Atmos', 'all', 350),
  ('Movies 1080p AV1 HQ', 'TrueHD', 'all', 300),
  ('Movies 1080p AV1 HQ', 'DTS-X', 'all', 300),
  ('Movies 1080p AV1 HQ', 'Opus 5.1 / 7.1', 'all', 250),
  ('Movies 1080p AV1 HQ', 'Lossless Audio', 'all', 250),
  ('Movies 1080p AV1 HQ', 'Opus Stereo', 'all', 200),
  ('Movies 1080p AV1 HQ', 'Dolby Digital', 'all', 150),
  ('Movies 1080p AV1 HQ', 'AV1 Compact Encoders', 'all', 500),
  ('Movies 1080p AV1 HQ', 'AV1 Storage Savers', 'all', -1000),
  ('Movies 1080p AV1 HQ', 'AMZN', 'all', 50),
  ('Movies 1080p AV1 HQ', 'DSNP', 'all', 50),
  ('Movies 1080p AV1 HQ', 'MAX', 'all', 50),
  ('Movies 1080p AV1 HQ', 'HULU', 'all', 50),
  ('Movies 1080p AV1 HQ', 'CRIT', 'all', 100),
  ('Movies 1080p AV1 HQ', 'Theatrical', 'all', 100),

  -- -------------------------------------------------------------------------
  -- MOVIES 1080p AV1 STORAGE SCORING
  -- -------------------------------------------------------------------------
  ('Movies 1080p AV1 Storage', 'AV1', 'all', 2000),
  ('Movies 1080p AV1 Storage', 'Legacy x265 Codec', 'all', -1000),
  ('Movies 1080p AV1 Storage', '10-bit Depth', 'all', 300),
  ('Movies 1080p AV1 Storage', 'Opus 5.1 / 7.1', 'all', 250),
  ('Movies 1080p AV1 Storage', 'Opus Stereo', 'all', 200),
  ('Movies 1080p AV1 Storage', 'Dolby Digital', 'all', 150),
  ('Movies 1080p AV1 Storage', 'AV1 Compact Encoders', 'all', 800),
  ('Movies 1080p AV1 Storage', 'AV1 Storage Savers', 'all', 600),
  ('Movies 1080p AV1 Storage', 'AMZN', 'all', 50),
  ('Movies 1080p AV1 Storage', 'DSNP', 'all', 50),
  ('Movies 1080p AV1 Storage', 'MAX', 'all', 50),
  ('Movies 1080p AV1 Storage', 'HULU', 'all', 50),

  -- -------------------------------------------------------------------------
  -- TV 2160p AV1 SCORING
  -- -------------------------------------------------------------------------
  ('TV 2160p AV1', 'AV1', 'all', 2000),
  ('TV 2160p AV1', 'Legacy x265 Codec', 'all', -3500),
  ('TV 2160p AV1', 'Dolby Vision', 'all', 600),
  ('TV 2160p AV1', 'HDR10+', 'all', 500),
  ('TV 2160p AV1', 'HDR', 'all', 400),
  ('TV 2160p AV1', '10-bit Depth', 'all', 300),
  ('TV 2160p AV1', 'Dolby Atmos', 'all', 350),
  ('TV 2160p AV1', 'TrueHD', 'all', 300),
  ('TV 2160p AV1', 'DTS-X', 'all', 300),
  ('TV 2160p AV1', 'Opus 5.1 / 7.1', 'all', 250),
  ('TV 2160p AV1', 'Dolby Digital', 'all', 150),
  ('TV 2160p AV1', 'AV1 Compact Encoders', 'all', 500),
  ('TV 2160p AV1', 'AV1 Storage Savers', 'all', -1000),
  ('TV 2160p AV1', 'AMZN', 'all', 50),
  ('TV 2160p AV1', 'DSNP', 'all', 50),
  ('TV 2160p AV1', 'MAX', 'all', 50),
  ('TV 2160p AV1', 'HULU', 'all', 50),

  -- -------------------------------------------------------------------------
  -- TV 1080p AV1 HQ SCORING
  -- -------------------------------------------------------------------------
  ('TV 1080p AV1 HQ', 'AV1', 'all', 2000),
  ('TV 1080p AV1 HQ', 'Legacy x265 Codec', 'all', -2000),
  ('TV 1080p AV1 HQ', '10-bit Depth', 'all', 300),
  ('TV 1080p AV1 HQ', 'Dolby Atmos', 'all', 350),
  ('TV 1080p AV1 HQ', 'TrueHD', 'all', 300),
  ('TV 1080p AV1 HQ', 'DTS-X', 'all', 300),
  ('TV 1080p AV1 HQ', 'Opus 5.1 / 7.1', 'all', 250),
  ('TV 1080p AV1 HQ', 'Lossless Audio', 'all', 250),
  ('TV 1080p AV1 HQ', 'Opus Stereo', 'all', 200),
  ('TV 1080p AV1 HQ', 'Dolby Digital', 'all', 150),
  ('TV 1080p AV1 HQ', 'AV1 Compact Encoders', 'all', 500),
  ('TV 1080p AV1 HQ', 'AV1 Storage Savers', 'all', -1000),
  ('TV 1080p AV1 HQ', 'AMZN', 'all', 50),
  ('TV 1080p AV1 HQ', 'DSNP', 'all', 50),
  ('TV 1080p AV1 HQ', 'MAX', 'all', 50),
  ('TV 1080p AV1 HQ', 'HULU', 'all', 50),

  -- -------------------------------------------------------------------------
  -- TV 1080p AV1 STORAGE SCORING
  -- -------------------------------------------------------------------------
  ('TV 1080p AV1 Storage', 'AV1', 'all', 2000),
  ('TV 1080p AV1 Storage', 'Legacy x265 Codec', 'all', -1000),
  ('TV 1080p AV1 Storage', '10-bit Depth', 'all', 300),
  ('TV 1080p AV1 Storage', 'Opus 5.1 / 7.1', 'all', 250),
  ('TV 1080p AV1 Storage', 'Opus Stereo', 'all', 200),
  ('TV 1080p AV1 Storage', 'Dolby Digital', 'all', 150),
  ('TV 1080p AV1 Storage', 'AV1 Compact Encoders', 'all', 800),
  ('TV 1080p AV1 Storage', 'AV1 Storage Savers', 'all', 600),
  ('TV 1080p AV1 Storage', 'AMZN', 'all', 50),
  ('TV 1080p AV1 Storage', 'DSNP', 'all', 50),
  ('TV 1080p AV1 Storage', 'MAX', 'all', 50),
  ('TV 1080p AV1 Storage', 'HULU', 'all', 50),

  -- -------------------------------------------------------------------------
  -- ANIME 1080p AV1 SCORING
  -- -------------------------------------------------------------------------
  ('Anime 1080p AV1', 'AV1', 'all', 2000),
  ('Anime 1080p AV1', 'Legacy x265 Codec', 'all', -2000),
  ('Anime 1080p AV1', '10-bit Depth', 'all', 300),
  ('Anime 1080p AV1', 'Dual Audio', 'all', 500),
  ('Anime 1080p AV1', 'AV1 Anime Encoders', 'sonarr', 1000),
  ('Anime 1080p AV1', 'Opus 5.1 / 7.1', 'all', 250),
  ('Anime 1080p AV1', 'Lossless Audio', 'all', 250),
  ('Anime 1080p AV1', 'Opus Stereo', 'all', 200),
  ('Anime 1080p AV1', 'AV1 Storage Savers', 'all', -1000)
ON CONFLICT DO NOTHING;
