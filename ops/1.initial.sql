-- ============================================================================
-- AV1 Master Database - PCD 2.0 Initial Import
-- Curated AV1 Custom Formats & Quality Profiles for Radarr and Sonarr
-- ============================================================================

-- ============================================================================
-- 1. TAGS
-- ============================================================================
INSERT INTO tags (name) VALUES ('AV1');
INSERT INTO tags (name) VALUES ('Codec');
INSERT INTO tags (name) VALUES ('10bit');
INSERT INTO tags (name) VALUES ('HDR');
INSERT INTO tags (name) VALUES ('DV');
INSERT INTO tags (name) VALUES ('Audio');
INSERT INTO tags (name) VALUES ('Opus');
INSERT INTO tags (name) VALUES ('Release Groups');
INSERT INTO tags (name) VALUES ('Quality');
INSERT INTO tags (name) VALUES ('Banned');
INSERT INTO tags (name) VALUES ('Streaming Service');
INSERT INTO tags (name) VALUES ('Radarr');
INSERT INTO tags (name) VALUES ('Sonarr');

-- ============================================================================
-- 2. REGULAR EXPRESSIONS
-- ============================================================================

-- Codecs
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_av1', '(?<![a-z0-9])(AV1|AV01|SVT[-._]?AV1|libsvtav1|rav1e|AOM[-._]?AV1)(?![a-z0-9])', 'Matches AV1 encoded video releases');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_10bit', '(?<![a-z0-9])(10[-._]?bit|10b|Hi10P)(?![a-z0-9])', 'Matches 10-bit color depth releases');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_8bit', '(?<![a-z0-9])(8[-._]?bit|8b)(?![a-z0-9])', 'Matches 8-bit encoded releases');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_x265', '(?<![a-z0-9])(x265|HEVC|H[-._]?265)(?![a-z0-9])', 'Matches HEVC / x265 encoded video');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_x264', '(?<![a-z0-9])(x264|AVC|H[-._]?264)(?![a-z0-9])', 'Matches AVC / x264 encoded video');

-- AV1 Release Groups - Tier 01 (Transparent / Master Encoders)
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_av1_tier01_groups', '-(t3nshi|EDGE2020|ZR-|D-Z0N3|Kitsune|Afm72|Vyndros|samsepi0l|FLUX|CtrlHD|Geek|DeciBelle)\b', 'Tier 1 high-fidelity transparent AV1 release groups');

-- AV1 Release Groups - Tier 02 (Quality Series & Anime Encoders)
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_av1_tier02_groups', '-(AkihitoSubs|Judas|Erai-raws|SubsPlease|NanDesuKa|ASW|Kawa|VARYG|LostYears|Tenrai-Sensei)\b', 'Tier 2 quality AV1 anime and TV series encoders');

-- AV1 Release Groups - Tier 03 (Balanced / Storage Savers)
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_av1_tier03_groups', '-(MeGusta|GalaxyRG|PSA|VXT|d3g|Ghost|rartv|BONE|ELiTE|LAMA)\b', 'Tier 3 compact AV1 release groups for storage efficiency');

-- High Dynamic Range & Color
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_dolby_vision', '(?<![a-z0-9])(DV|DoVi|Dolby[-._]?Vision)(?![a-z0-9])', 'Matches Dolby Vision metadata');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_hdr10plus', '(?<![a-z0-9])(HDR10\+|HDR10Plus)(?![a-z0-9])', 'Matches dynamic HDR10+ metadata');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_hdr', '(?<![a-z0-9])(HDR10|HDR)(?![a-z0-9])', 'Matches standard HDR10 or HDR metadata');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_dv_no_hdr_fallback', '(?<![a-z0-9])(DV|DoVi)\b(?=.*\b(WEB[-._]?DL|WEBRip)\b)(?!.*\b(HDR|HDR10|HDR10\+)\b)', 'Matches Dolby Vision Profile 5 without HDR10 fallback layer');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_sdr', '(?<![a-z0-9])(SDR)(?![a-z0-9])', 'Matches Standard Dynamic Range (SDR)');

-- Audio Formats
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_opus_multi', '(?<![a-z0-9])(Opus|OPUS)[-._ ]?(5\.1|7\.1|6ch|8ch)(?![a-z0-9])', 'Matches Opus 5.1/7.1 multi-channel audio');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_opus_stereo', '(?<![a-z0-9])(Opus|OPUS)(?![-._ ]*(?:5\.1|7\.1|6ch|8ch))(?![a-z0-9])', 'Matches Opus stereo / 2.0 / general audio');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_atmos', '(?<![a-z0-9])(Atmos)(?![a-z0-9])', 'Matches Dolby Atmos object-based audio');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_truehd', '(?<![a-z0-9])(TrueHD|Dolby[-._]?TrueHD)(?![a-z0-9])', 'Matches lossless Dolby TrueHD audio');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_dtshd', '(?<![a-z0-9])(DTS[-._]?HD[-._]?MA|DTS[-._]?X|DTS[-._]?HD)(?![a-z0-9])', 'Matches lossless DTS-HD Master Audio or DTS:X');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_ddp', '(?<![a-z0-9])(DDP|EAC3|E-AC-3|Dolby[-._]?Digital[-._]?Plus)(?![a-z0-9])', 'Matches Dolby Digital Plus / E-AC-3 audio');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_flac', '(?<![a-z0-9])(FLAC)(?![a-z0-9])', 'Matches lossless FLAC audio');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_aac', '(?<![a-z0-9])(AAC)(?![a-z0-9])', 'Matches AAC audio');

-- Features & Streaming Services
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_dual_audio', '(?<![a-z0-9])(Dual[-._]?Audio|Multi[-._]?Audio)(?![a-z0-9])', 'Matches Dual or Multi Audio releases');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_streaming_services', '\b(AMZN|NF|ATVP|DSNP|MAX|HMAX|iT|BCORE)\b', 'Matches major streaming provider tags');

-- Anti-Trash / Hygiene Filters
INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_banned_groups', '-(YTS|YIFY|EVO|STUTTERSHIT|FGT|SPARKS)\b', 'Banned low quality or spam release groups');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_bad_sources', '\b(CAM|CAM-?Rip|TS|TELESYNC|HD-TS|HDCAM|WORKPRINT|DVDSCR|SCREENER)\b', 'Matches low quality recording sources');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_bad_ai_upscales', '\b(AI[-._]?Upscale|Topaz|Upscaled|Fake4K)\b', 'Matches unauthorized AI upscales and filters');

INSERT INTO regular_expressions (name, pattern, description) 
VALUES ('regex_br_disk', '\b(BR-DISK|BDMV|ISO|COMPLETE\.BLURAY)\b', 'Matches raw unparsed disc structures');

-- ============================================================================
-- 3. CUSTOM FORMATS
-- ============================================================================
INSERT INTO custom_formats (name, description) VALUES ('AV1 Codec', 'Matches genuine AV1 video streams.');
INSERT INTO custom_formats (name, description) VALUES ('10-bit Precision', 'Matches 10-bit color depth releases.');
INSERT INTO custom_formats (name, description) VALUES ('8-bit Video', 'Matches 8-bit color depth releases.');
INSERT INTO custom_formats (name, description) VALUES ('x265 / HEVC', 'Matches HEVC / x265 video codec.');
INSERT INTO custom_formats (name, description) VALUES ('x264 / AVC', 'Matches AVC / x264 video codec.');
INSERT INTO custom_formats (name, description) VALUES ('AV1 Tier 01', 'Tier 1 high-fidelity transparent AV1 release groups.');
INSERT INTO custom_formats (name, description) VALUES ('AV1 Tier 02', 'Tier 2 quality AV1 anime and TV series encoders.');
INSERT INTO custom_formats (name, description) VALUES ('AV1 Tier 03', 'Tier 3 compact AV1 release groups for storage efficiency.');
INSERT INTO custom_formats (name, description) VALUES ('Dolby Vision', 'Dolby Vision high dynamic range.');
INSERT INTO custom_formats (name, description) VALUES ('HDR10+', 'HDR10+ dynamic HDR format.');
INSERT INTO custom_formats (name, description) VALUES ('HDR10 / HDR', 'HDR10 high dynamic range format.');
INSERT INTO custom_formats (name, description) VALUES ('DV (No HDR Fallback)', 'Dolby Vision Profile 5 without fallback.');
INSERT INTO custom_formats (name, description) VALUES ('SDR Color', 'Standard dynamic range color.');
INSERT INTO custom_formats (name, description) VALUES ('Opus 5.1 / 7.1', 'Multi-channel Opus surround audio.');
INSERT INTO custom_formats (name, description) VALUES ('Opus Stereo', 'Opus stereo audio.');
INSERT INTO custom_formats (name, description) VALUES ('Dolby Atmos', 'Dolby Atmos immersive audio.');
INSERT INTO custom_formats (name, description) VALUES ('TrueHD Audio', 'Lossless Dolby TrueHD audio.');
INSERT INTO custom_formats (name, description) VALUES ('DTS-HD MA Audio', 'Lossless DTS-HD Master Audio.');
INSERT INTO custom_formats (name, description) VALUES ('Dolby Digital +', 'Dolby Digital Plus / E-AC-3 audio.');
INSERT INTO custom_formats (name, description) VALUES ('FLAC Audio', 'Lossless FLAC audio.');
INSERT INTO custom_formats (name, description) VALUES ('AAC Audio', 'AAC audio stream.');
INSERT INTO custom_formats (name, description) VALUES ('Dual Audio', 'Dual audio track release.');
INSERT INTO custom_formats (name, description) VALUES ('Premium Streaming Service', 'Releases sourced from premium streaming services.');
INSERT INTO custom_formats (name, description) VALUES ('Banned Groups', 'Known low-quality re-encoding groups.');
INSERT INTO custom_formats (name, description) VALUES ('Bad Sources (CAM/TS)', 'Cam, Telesync, Screener recordings.');
INSERT INTO custom_formats (name, description) VALUES ('Bad AI Upscales', 'Low-effort AI upscales.');
INSERT INTO custom_formats (name, description) VALUES ('BR-DISK Structure', 'Raw Blu-ray disc structures.');

-- Link Custom Format Conditions (Using Multi-Condition Requirement for AV1 Tiers)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES 
  ('AV1 Codec', 'cond_av1', 'release_title', 'all', 0, 1),
  ('10-bit Precision', 'cond_10bit', 'release_title', 'all', 0, 1),
  ('8-bit Video', 'cond_8bit', 'release_title', 'all', 0, 1),
  ('x265 / HEVC', 'cond_x265', 'release_title', 'all', 0, 1),
  ('x264 / AVC', 'cond_x264', 'release_title', 'all', 0, 1),
  ('AV1 Tier 01', 'cond_av1_req_01', 'release_title', 'all', 0, 1),
  ('AV1 Tier 01', 'cond_group_01', 'release_title', 'all', 0, 1),
  ('AV1 Tier 02', 'cond_av1_req_02', 'release_title', 'all', 0, 1),
  ('AV1 Tier 02', 'cond_group_02', 'release_title', 'all', 0, 1),
  ('AV1 Tier 03', 'cond_av1_req_03', 'release_title', 'all', 0, 1),
  ('AV1 Tier 03', 'cond_group_03', 'release_title', 'all', 0, 1),
  ('Dolby Vision', 'cond_dv', 'release_title', 'all', 0, 1),
  ('HDR10+', 'cond_hdr10plus', 'release_title', 'all', 0, 1),
  ('HDR10 / HDR', 'cond_hdr', 'release_title', 'all', 0, 1),
  ('DV (No HDR Fallback)', 'cond_dv_no_fallback', 'release_title', 'all', 0, 1),
  ('SDR Color', 'cond_sdr', 'release_title', 'all', 0, 1),
  ('Opus 5.1 / 7.1', 'cond_opus_multi', 'release_title', 'all', 0, 1),
  ('Opus Stereo', 'cond_opus_stereo', 'release_title', 'all', 0, 1),
  ('Dolby Atmos', 'cond_atmos', 'release_title', 'all', 0, 1),
  ('TrueHD Audio', 'cond_truehd', 'release_title', 'all', 0, 1),
  ('DTS-HD MA Audio', 'cond_dtshd', 'release_title', 'all', 0, 1),
  ('Dolby Digital +', 'cond_ddp', 'release_title', 'all', 0, 1),
  ('FLAC Audio', 'cond_flac', 'release_title', 'all', 0, 1),
  ('AAC Audio', 'cond_aac', 'release_title', 'all', 0, 1),
  ('Dual Audio', 'cond_dual_audio', 'release_title', 'all', 0, 1),
  ('Premium Streaming Service', 'cond_streaming', 'release_title', 'all', 0, 1),
  ('Banned Groups', 'cond_banned', 'release_title', 'all', 0, 1),
  ('Bad Sources (CAM/TS)', 'cond_bad_sources', 'release_title', 'all', 0, 1),
  ('Bad AI Upscales', 'cond_ai_upscales', 'release_title', 'all', 0, 1),
  ('BR-DISK Structure', 'cond_br_disk', 'release_title', 'all', 0, 1);

-- Link Conditions to Regular Expressions
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES 
  ('AV1 Codec', 'cond_av1', 'regex_av1'),
  ('10-bit Precision', 'cond_10bit', 'regex_10bit'),
  ('8-bit Video', 'cond_8bit', 'regex_8bit'),
  ('x265 / HEVC', 'cond_x265', 'regex_x265'),
  ('x264 / AVC', 'cond_x264', 'regex_x264'),
  ('AV1 Tier 01', 'cond_av1_req_01', 'regex_av1'),
  ('AV1 Tier 01', 'cond_group_01', 'regex_av1_tier01_groups'),
  ('AV1 Tier 02', 'cond_av1_req_02', 'regex_av1'),
  ('AV1 Tier 02', 'cond_group_02', 'regex_av1_tier02_groups'),
  ('AV1 Tier 03', 'cond_av1_req_03', 'regex_av1'),
  ('AV1 Tier 03', 'cond_group_03', 'regex_av1_tier03_groups'),
  ('Dolby Vision', 'cond_dv', 'regex_dolby_vision'),
  ('HDR10+', 'cond_hdr10plus', 'regex_hdr10plus'),
  ('HDR10 / HDR', 'cond_hdr', 'regex_hdr'),
  ('DV (No HDR Fallback)', 'cond_dv_no_fallback', 'regex_dv_no_hdr_fallback'),
  ('SDR Color', 'cond_sdr', 'regex_sdr'),
  ('Opus 5.1 / 7.1', 'cond_opus_multi', 'regex_opus_multi'),
  ('Opus Stereo', 'cond_opus_stereo', 'regex_opus_stereo'),
  ('Dolby Atmos', 'cond_atmos', 'regex_atmos'),
  ('TrueHD Audio', 'cond_truehd', 'regex_truehd'),
  ('DTS-HD MA Audio', 'cond_dtshd', 'regex_dtshd'),
  ('Dolby Digital +', 'cond_ddp', 'regex_ddp'),
  ('FLAC Audio', 'cond_flac', 'regex_flac'),
  ('AAC Audio', 'cond_aac', 'regex_aac'),
  ('Dual Audio', 'cond_dual_audio', 'regex_dual_audio'),
  ('Premium Streaming Service', 'cond_streaming', 'regex_streaming_services'),
  ('Banned Groups', 'cond_banned', 'regex_banned_groups'),
  ('Bad Sources (CAM/TS)', 'cond_bad_sources', 'regex_bad_sources'),
  ('Bad AI Upscales', 'cond_ai_upscales', 'regex_bad_ai_upscales'),
  ('BR-DISK Structure', 'cond_br_disk', 'regex_br_disk');

-- ============================================================================
-- 4. QUALITY PROFILES
-- ============================================================================
INSERT INTO quality_profiles (name, description, upgrades_allowed, minimum_custom_format_score, upgrade_until_score, upgrade_score_increment)
VALUES 
  ('Movies 2160p AV1 HQ', '4K UHD AV1 Movies with HDR10/Dolby Vision, high video bitrate, and transparent/Opus audio.', 1, 500, 10000, 1),
  ('Movies 1080p AV1 HQ', '1080p FHD AV1 Movies with 10-bit precision, transparent tiering, and high-fidelity audio.', 1, 500, 10000, 1),
  ('TV 2160p AV1', '4K UHD AV1 TV Series episodes with HDR and multi-channel audio.', 1, 500, 10000, 1),
  ('TV 1080p AV1', '1080p FHD 10-bit AV1 TV Series (space-saving high-efficiency profile).', 1, 500, 10000, 1),
  ('Anime 1080p AV1', '1080p 10-bit AV1 Anime with Dual Audio (Japanese + English) prioritization.', 1, 500, 10000, 1);

-- ============================================================================
-- 5. QUALITY GROUPS (Profile-Specific)
-- ============================================================================

-- Quality Groups for 'Movies 2160p AV1 HQ'
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('Movies 2160p AV1 HQ', '2160p Group');
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('Movies 2160p AV1 HQ', '1080p Fallback');

-- Quality Groups for 'Movies 1080p AV1 HQ'
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('Movies 1080p AV1 HQ', '1080p Group');

-- Quality Groups for 'TV 2160p AV1'
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('TV 2160p AV1', '2160p TV Group');
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('TV 2160p AV1', '1080p TV Fallback');

-- Quality Groups for 'TV 1080p AV1'
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('TV 1080p AV1', '1080p TV Group');

-- Quality Groups for 'Anime 1080p AV1'
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('Anime 1080p AV1', 'Anime 1080p Group');

-- ============================================================================
-- 6. QUALITY GROUP MEMBERS
-- ============================================================================

-- 'Movies 2160p AV1 HQ' - 2160p Group (WEBDL, WEBRip, Bluray, Remux)
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('Movies 2160p AV1 HQ', '2160p Group', 'WEBDL-2160p'),
  ('Movies 2160p AV1 HQ', '2160p Group', 'WEBRip-2160p'),
  ('Movies 2160p AV1 HQ', '2160p Group', 'Bluray-2160p'),
  ('Movies 2160p AV1 HQ', '2160p Group', 'Remux-2160p');

-- 'Movies 2160p AV1 HQ' - 1080p Fallback
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'WEBDL-1080p'),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'WEBRip-1080p'),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 'Bluray-1080p');

-- 'Movies 1080p AV1 HQ' - 1080p Group
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('Movies 1080p AV1 HQ', '1080p Group', 'WEBDL-1080p'),
  ('Movies 1080p AV1 HQ', '1080p Group', 'WEBRip-1080p'),
  ('Movies 1080p AV1 HQ', '1080p Group', 'Bluray-1080p'),
  ('Movies 1080p AV1 HQ', '1080p Group', 'Remux-1080p');

-- 'TV 2160p AV1' - 2160p TV Group
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('TV 2160p AV1', '2160p TV Group', 'WEBDL-2160p'),
  ('TV 2160p AV1', '2160p TV Group', 'WEBRip-2160p'),
  ('TV 2160p AV1', '2160p TV Group', 'Bluray-2160p'),
  ('TV 2160p AV1', '2160p TV Group', 'HDTV-2160p');

-- 'TV 2160p AV1' - 1080p TV Fallback
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('TV 2160p AV1', '1080p TV Fallback', 'WEBDL-1080p'),
  ('TV 2160p AV1', '1080p TV Fallback', 'WEBRip-1080p'),
  ('TV 2160p AV1', '1080p TV Fallback', 'Bluray-1080p');

-- 'TV 1080p AV1' - 1080p TV Group
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('TV 1080p AV1', '1080p TV Group', 'WEBDL-1080p'),
  ('TV 1080p AV1', '1080p TV Group', 'WEBRip-1080p'),
  ('TV 1080p AV1', '1080p TV Group', 'Bluray-1080p'),
  ('TV 1080p AV1', '1080p TV Group', 'HDTV-1080p');

-- 'Anime 1080p AV1' - Anime 1080p Group
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name)
VALUES 
  ('Anime 1080p AV1', 'Anime 1080p Group', 'WEBDL-1080p'),
  ('Anime 1080p AV1', 'Anime 1080p Group', 'WEBRip-1080p'),
  ('Anime 1080p AV1', 'Anime 1080p Group', 'Bluray-1080p');

-- ============================================================================
-- 7. QUALITY PROFILE QUALITIES (Positions & Upgrade Stops)
-- ============================================================================

-- 'Movies 2160p AV1 HQ'
INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, upgrade_until, enabled)
VALUES 
  ('Movies 2160p AV1 HQ', '2160p Group', 0, 1, 1),
  ('Movies 2160p AV1 HQ', '1080p Fallback', 1, 0, 1);

-- 'Movies 1080p AV1 HQ'
INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, upgrade_until, enabled)
VALUES 
  ('Movies 1080p AV1 HQ', '1080p Group', 0, 1, 1);

-- 'TV 2160p AV1'
INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, upgrade_until, enabled)
VALUES 
  ('TV 2160p AV1', '2160p TV Group', 0, 1, 1),
  ('TV 2160p AV1', '1080p TV Fallback', 1, 0, 1);

-- 'TV 1080p AV1'
INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, upgrade_until, enabled)
VALUES 
  ('TV 1080p AV1', '1080p TV Group', 0, 1, 1);

-- 'Anime 1080p AV1'
INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, upgrade_until, enabled)
VALUES 
  ('Anime 1080p AV1', 'Anime 1080p Group', 0, 1, 1);

-- ============================================================================
-- 8. QUALITY PROFILE CUSTOM FORMAT SCORING
-- ============================================================================

-- Scores for 'Movies 2160p AV1 HQ' (Radarr)
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES 
  ('Movies 2160p AV1 HQ', 'AV1 Codec', 'radarr', 1500),
  ('Movies 2160p AV1 HQ', '10-bit Precision', 'radarr', 250),
  ('Movies 2160p AV1 HQ', 'AV1 Tier 01', 'radarr', 800),
  ('Movies 2160p AV1 HQ', 'AV1 Tier 02', 'radarr', 400),
  ('Movies 2160p AV1 HQ', 'AV1 Tier 03', 'radarr', 200),
  ('Movies 2160p AV1 HQ', 'Dolby Vision', 'radarr', 500),
  ('Movies 2160p AV1 HQ', 'HDR10+', 'radarr', 400),
  ('Movies 2160p AV1 HQ', 'HDR10 / HDR', 'radarr', 300),
  ('Movies 2160p AV1 HQ', 'Dolby Atmos', 'radarr', 300),
  ('Movies 2160p AV1 HQ', 'TrueHD Audio', 'radarr', 250),
  ('Movies 2160p AV1 HQ', 'DTS-HD MA Audio', 'radarr', 250),
  ('Movies 2160p AV1 HQ', 'Opus 5.1 / 7.1', 'radarr', 200),
  ('Movies 2160p AV1 HQ', 'Dolby Digital +', 'radarr', 150),
  ('Movies 2160p AV1 HQ', 'Premium Streaming Service', 'radarr', 100),
  ('Movies 2160p AV1 HQ', '8-bit Video', 'radarr', -500),
  ('Movies 2160p AV1 HQ', 'DV (No HDR Fallback)', 'radarr', -10000),
  ('Movies 2160p AV1 HQ', 'Banned Groups', 'radarr', -10000),
  ('Movies 2160p AV1 HQ', 'Bad Sources (CAM/TS)', 'radarr', -10000),
  ('Movies 2160p AV1 HQ', 'Bad AI Upscales', 'radarr', -10000),
  ('Movies 2160p AV1 HQ', 'BR-DISK Structure', 'radarr', -10000);

-- Scores for 'Movies 1080p AV1 HQ' (Radarr)
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES 
  ('Movies 1080p AV1 HQ', 'AV1 Codec', 'radarr', 1500),
  ('Movies 1080p AV1 HQ', '10-bit Precision', 'radarr', 250),
  ('Movies 1080p AV1 HQ', 'AV1 Tier 01', 'radarr', 800),
  ('Movies 1080p AV1 HQ', 'AV1 Tier 02', 'radarr', 400),
  ('Movies 1080p AV1 HQ', 'AV1 Tier 03', 'radarr', 200),
  ('Movies 1080p AV1 HQ', 'Opus 5.1 / 7.1', 'radarr', 250),
  ('Movies 1080p AV1 HQ', 'Opus Stereo', 'radarr', 150),
  ('Movies 1080p AV1 HQ', 'Dolby Digital +', 'radarr', 150),
  ('Movies 1080p AV1 HQ', 'FLAC Audio', 'radarr', 200),
  ('Movies 1080p AV1 HQ', 'Premium Streaming Service', 'radarr', 100),
  ('Movies 1080p AV1 HQ', '8-bit Video', 'radarr', -500),
  ('Movies 1080p AV1 HQ', 'Banned Groups', 'radarr', -10000),
  ('Movies 1080p AV1 HQ', 'Bad Sources (CAM/TS)', 'radarr', -10000),
  ('Movies 1080p AV1 HQ', 'Bad AI Upscales', 'radarr', -10000),
  ('Movies 1080p AV1 HQ', 'BR-DISK Structure', 'radarr', -10000);

-- Scores for 'TV 2160p AV1' (Sonarr)
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES 
  ('TV 2160p AV1', 'AV1 Codec', 'sonarr', 1500),
  ('TV 2160p AV1', '10-bit Precision', 'sonarr', 250),
  ('TV 2160p AV1', 'AV1 Tier 01', 'sonarr', 800),
  ('TV 2160p AV1', 'AV1 Tier 02', 'sonarr', 400),
  ('TV 2160p AV1', 'AV1 Tier 03', 'sonarr', 200),
  ('TV 2160p AV1', 'Dolby Vision', 'sonarr', 500),
  ('TV 2160p AV1', 'HDR10+', 'sonarr', 400),
  ('TV 2160p AV1', 'HDR10 / HDR', 'sonarr', 300),
  ('TV 2160p AV1', 'Dolby Atmos', 'sonarr', 300),
  ('TV 2160p AV1', 'Opus 5.1 / 7.1', 'sonarr', 200),
  ('TV 2160p AV1', 'Dolby Digital +', 'sonarr', 150),
  ('TV 2160p AV1', 'Premium Streaming Service', 'sonarr', 100),
  ('TV 2160p AV1', '8-bit Video', 'sonarr', -500),
  ('TV 2160p AV1', 'DV (No HDR Fallback)', 'sonarr', -10000),
  ('TV 2160p AV1', 'Banned Groups', 'sonarr', -10000),
  ('TV 2160p AV1', 'Bad Sources (CAM/TS)', 'sonarr', -10000),
  ('TV 2160p AV1', 'Bad AI Upscales', 'sonarr', -10000),
  ('TV 2160p AV1', 'BR-DISK Structure', 'sonarr', -10000);

-- Scores for 'TV 1080p AV1' (Sonarr)
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES 
  ('TV 1080p AV1', 'AV1 Codec', 'sonarr', 1500),
  ('TV 1080p AV1', '10-bit Precision', 'sonarr', 250),
  ('TV 1080p AV1', 'AV1 Tier 01', 'sonarr', 800),
  ('TV 1080p AV1', 'AV1 Tier 02', 'sonarr', 400),
  ('TV 1080p AV1', 'AV1 Tier 03', 'sonarr', 200),
  ('TV 1080p AV1', 'Opus 5.1 / 7.1', 'sonarr', 250),
  ('TV 1080p AV1', 'Opus Stereo', 'sonarr', 150),
  ('TV 1080p AV1', 'Dolby Digital +', 'sonarr', 150),
  ('TV 1080p AV1', 'Premium Streaming Service', 'sonarr', 100),
  ('TV 1080p AV1', '8-bit Video', 'sonarr', -500),
  ('TV 1080p AV1', 'Banned Groups', 'sonarr', -10000),
  ('TV 1080p AV1', 'Bad Sources (CAM/TS)', 'sonarr', -10000),
  ('TV 1080p AV1', 'Bad AI Upscales', 'sonarr', -10000),
  ('TV 1080p AV1', 'BR-DISK Structure', 'sonarr', -10000);

-- Scores for 'Anime 1080p AV1' (Sonarr & Radarr)
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES 
  ('Anime 1080p AV1', 'AV1 Codec', 'all', 1500),
  ('Anime 1080p AV1', '10-bit Precision', 'all', 300),
  ('Anime 1080p AV1', 'AV1 Tier 02', 'all', 800),
  ('Anime 1080p AV1', 'AV1 Tier 01', 'all', 600),
  ('Anime 1080p AV1', 'AV1 Tier 03', 'all', 200),
  ('Anime 1080p AV1', 'Dual Audio', 'all', 500),
  ('Anime 1080p AV1', 'Opus 5.1 / 7.1', 'all', 200),
  ('Anime 1080p AV1', 'Opus Stereo', 'all', 150),
  ('Anime 1080p AV1', 'FLAC Audio', 'all', 250),
  ('Anime 1080p AV1', 'AAC Audio', 'all', 100),
  ('Anime 1080p AV1', '8-bit Video', 'all', -500),
  ('Anime 1080p AV1', 'Banned Groups', 'all', -10000),
  ('Anime 1080p AV1', 'Bad Sources (CAM/TS)', 'all', -10000),
  ('Anime 1080p AV1', 'Bad AI Upscales', 'all', -10000),
  ('Anime 1080p AV1', 'BR-DISK Structure', 'all', -10000);
