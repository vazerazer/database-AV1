-- @description: Replace generic last resorts with curated Dumpstarr and Dictionarry group tiers
-- @author: cursor
-- @name: 982.curated-1080p-x264-and-720p-group-tiers

BEGIN TRANSACTION;

-- The generic last resorts admitted any 1080p or 720p group. Those
-- formats are removed. A movie that is not in a named tier is left for
-- a manual grab.
--
-- 1080p x264 tiers are the union of Dictionarry 1080p Quality Tier 1-6
-- and Dumpstarr stable HD Bluray Tier 01-03 (Radarr). 720p tiers are the
-- union of Dictionarry 720p Quality Tier 1-6 and those same Dumpstarr HD
-- lists. When both sources name a group, it keeps the better (lower-number)
-- tier and is not repeated, so the tiers cannot stack. Dumpstarr UHD tiers
-- and codec-agnostic WEB tiers are not imported. PiRaTeS is not added.
--
-- Each 1080p tier requires 1080p, AVC, not HEVC, not remux, and Blu-ray or
-- WEBRip. HQMUX, Kitsune, and PTer therefore do not add this score to an
-- HEVC release that already matches an existing 1080p HEVC format.
-- Each 720p tier requires 720p, not 1080p, not 2160p, and not remux. It
-- does not ban HEVC. x265 (HD) is not scored.
--
-- Scores sit in 3900, 3720, 3540, 3360, 3180, 3000. Tier 1 is under
-- 1080p HEVC Tier 3 at 4100. 720p uses the same numbers inside the 720p
-- Fallback quality group, which stays below every 1080p quality.

DELETE FROM custom_formats WHERE name IN (
  '1080p Compact HEVC Last Resort',
  '1080p Compact AVC Last Resort',
  '720p Compact Last Resort'
);
DELETE FROM regular_expressions WHERE name = '720p Last Resort Codec';

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '1080p x264 Tier 1 Groups',
  '(?i)^(?:ATELiER|BBQ|BMF|c0kE|Chotab|coffee|CRiSC|CtrlHD|D\-Z0N3|Dariush|decibeL|DON|EbP|EDPH|Geek|LolHD|NCmt|PTer|REBORN|SA89|SoLaR|TayTO|TDD|TeamSyndicate|TnP|VietHD|ZoroSenpai|ZQ)$',
  'Named groups for 1080p x264 Tier 1. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('1080p x264 Tier 1', '1080p AVC Blu-ray or WEBRip from named tier 1 groups. Union of Dictionarry 1080p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires AVC and rejects HEVC so it cannot stack on the 1080p HEVC ladder.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p x264 Tier 1', '1080p'), ('1080p x264 Tier 1', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p x264 Tier 1', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p x264 Tier 1', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p x264 Tier 1', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 1', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 1', 'Groups', 'release_group', 'all', 0, 1),
  ('1080p x264 Tier 1', 'Bluray', 'source', 'all', 0, 0),
  ('1080p x264 Tier 1', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p x264 Tier 1', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p x264 Tier 1', 'AVC', 'AVC'),
  ('1080p x264 Tier 1', 'Not HEVC', 'HEVC'),
  ('1080p x264 Tier 1', 'Not Remux', 'Remux'),
  ('1080p x264 Tier 1', 'Groups', '1080p x264 Tier 1 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p x264 Tier 1', 'Bluray', 'bluray'),
  ('1080p x264 Tier 1', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p x264 Tier 1', 'all', 3900)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '1080p x264 Tier 2 Groups',
  '(?i)^(?:0BSiDiAN|EA|HiDt|HiFi|HiSD|iFT|LoRD|NTb|QOQ|sbR)$',
  'Named groups for 1080p x264 Tier 2. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('1080p x264 Tier 2', '1080p AVC Blu-ray or WEBRip from named tier 2 groups. Union of Dictionarry 1080p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires AVC and rejects HEVC so it cannot stack on the 1080p HEVC ladder.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p x264 Tier 2', '1080p'), ('1080p x264 Tier 2', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p x264 Tier 2', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p x264 Tier 2', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p x264 Tier 2', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 2', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 2', 'Groups', 'release_group', 'all', 0, 1),
  ('1080p x264 Tier 2', 'Bluray', 'source', 'all', 0, 0),
  ('1080p x264 Tier 2', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p x264 Tier 2', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p x264 Tier 2', 'AVC', 'AVC'),
  ('1080p x264 Tier 2', 'Not HEVC', 'HEVC'),
  ('1080p x264 Tier 2', 'Not Remux', 'Remux'),
  ('1080p x264 Tier 2', 'Groups', '1080p x264 Tier 2 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p x264 Tier 2', 'Bluray', 'bluray'),
  ('1080p x264 Tier 2', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p x264 Tier 2', 'all', 3720)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '1080p x264 Tier 3 Groups',
  '(?i)^(?:BHDStudio|BV|FoRM|hallowed|HiP|HONE|playHD|Skazhutin|SPHD|W4NK3R|WMING)$',
  'Named groups for 1080p x264 Tier 3. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('1080p x264 Tier 3', '1080p AVC Blu-ray or WEBRip from named tier 3 groups. Union of Dictionarry 1080p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires AVC and rejects HEVC so it cannot stack on the 1080p HEVC ladder.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p x264 Tier 3', '1080p'), ('1080p x264 Tier 3', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p x264 Tier 3', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p x264 Tier 3', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p x264 Tier 3', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 3', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 3', 'Groups', 'release_group', 'all', 0, 1),
  ('1080p x264 Tier 3', 'Bluray', 'source', 'all', 0, 0),
  ('1080p x264 Tier 3', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p x264 Tier 3', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p x264 Tier 3', 'AVC', 'AVC'),
  ('1080p x264 Tier 3', 'Not HEVC', 'HEVC'),
  ('1080p x264 Tier 3', 'Not Remux', 'Remux'),
  ('1080p x264 Tier 3', 'Groups', '1080p x264 Tier 3 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p x264 Tier 3', 'Bluray', 'bluray'),
  ('1080p x264 Tier 3', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p x264 Tier 3', 'all', 3540)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '1080p x264 Tier 4 Groups',
  '(?i)^(?:de\[42\]|eXterminator|HDMaNiAcS|IDE)$',
  'Named groups for 1080p x264 Tier 4. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('1080p x264 Tier 4', '1080p AVC Blu-ray or WEBRip from named tier 4 groups. Union of Dictionarry 1080p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires AVC and rejects HEVC so it cannot stack on the 1080p HEVC ladder.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p x264 Tier 4', '1080p'), ('1080p x264 Tier 4', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p x264 Tier 4', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p x264 Tier 4', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p x264 Tier 4', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 4', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 4', 'Groups', 'release_group', 'all', 0, 1),
  ('1080p x264 Tier 4', 'Bluray', 'source', 'all', 0, 0),
  ('1080p x264 Tier 4', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p x264 Tier 4', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p x264 Tier 4', 'AVC', 'AVC'),
  ('1080p x264 Tier 4', 'Not HEVC', 'HEVC'),
  ('1080p x264 Tier 4', 'Not Remux', 'Remux'),
  ('1080p x264 Tier 4', 'Groups', '1080p x264 Tier 4 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p x264 Tier 4', 'Bluray', 'bluray'),
  ('1080p x264 Tier 4', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p x264 Tier 4', 'all', 3360)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '1080p x264 Tier 5 Groups',
  '(?i)^(?:AFKI|Aio|AJP69|aNDy|ARiN|AZVD|BAT1|BBW|BNL|BSTD|Cache|CALiGARi|CJ|CRiME|CRX|DiRTY|E\.N\.D|E1|E76|EBCP|Eby|ENDSkY|ESiR|EXCiSION|faBR|FANDANGO|Friday|FTO|GALAXY|GL|GR|GrapeHD|GS88|GutS|GZ|H@M|hdalx|HDL|HDmonSK|HDV|HDv0T|HDxT|HQMUX|HR|iLL|iLoveHD|IMNEWHERE|Ivandro|J2G|JewelBox|JKP|JM|KamiKaze|KASHMiR|Kitsune|Krispy|Kururun|LAZY|LiNG|luvBB|MCR|MGs|Narkyy|Natuyuki|NiBuRu|NiP|nmd|NorTV|NoVA|NyHD|O2STK|OB1|OmertaHD|ORiGEN|Otaibi|Palm|pcroland|Penumbra|PerfectionHD|PiPicK|POH|Positive|Prestige|RDK123|REPTiLE|RiCO|RightSIZE|RO|Rose3Thorn|rttr|SaNcTi|ShAnKs|SiMPLE|Softboat|SOP|SPEED|SuBHD|SUPER|TAiCHi|TBB|ThD|ToK|UxO|VD|ViSUM|VLAD|VorteX|WESTSiDE|WiHD|WiLF|xander|ZIMBO|ZiNC)$',
  'Named groups for 1080p x264 Tier 5. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('1080p x264 Tier 5', '1080p AVC Blu-ray or WEBRip from named tier 5 groups. Union of Dictionarry 1080p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires AVC and rejects HEVC so it cannot stack on the 1080p HEVC ladder.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p x264 Tier 5', '1080p'), ('1080p x264 Tier 5', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p x264 Tier 5', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p x264 Tier 5', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p x264 Tier 5', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 5', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 5', 'Groups', 'release_group', 'all', 0, 1),
  ('1080p x264 Tier 5', 'Bluray', 'source', 'all', 0, 0),
  ('1080p x264 Tier 5', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p x264 Tier 5', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p x264 Tier 5', 'AVC', 'AVC'),
  ('1080p x264 Tier 5', 'Not HEVC', 'HEVC'),
  ('1080p x264 Tier 5', 'Not Remux', 'Remux'),
  ('1080p x264 Tier 5', 'Groups', '1080p x264 Tier 5 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p x264 Tier 5', 'Bluray', 'bluray'),
  ('1080p x264 Tier 5', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p x264 Tier 5', 'all', 3180)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '1080p x264 Tier 6 Groups',
  '(?i)^(?:147|aBa|ASD87|Baer|BakedFEL|BRUTE|BTN|CART|cFc|CHD|CONSORTiUM|CREATiVE|eckomega|EuReKA|EwT|FraMeSToR|Funner|G4MBiT|GALVANiZE|GOLIATN|Gyroscope|HaB|HANDJOB|HDC|iON|j3rico|KnG|LEGi0N|Lulz|MaG|MKu|MTeam|MySiLU|ORBiT|P0W4HD|PiG30N|PiMP|PriMeHD|PTP|PuTao|ROCiNANTE|SaL|Seal|Slappy|SpaceHD|Spekt0r|Uld|WiKi|WiLDCAT|XFR|ZAL)$',
  'Named groups for 1080p x264 Tier 6. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('1080p x264 Tier 6', '1080p AVC Blu-ray or WEBRip from named tier 6 groups. Union of Dictionarry 1080p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires AVC and rejects HEVC so it cannot stack on the 1080p HEVC ladder.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p x264 Tier 6', '1080p'), ('1080p x264 Tier 6', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p x264 Tier 6', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p x264 Tier 6', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p x264 Tier 6', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 6', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p x264 Tier 6', 'Groups', 'release_group', 'all', 0, 1),
  ('1080p x264 Tier 6', 'Bluray', 'source', 'all', 0, 0),
  ('1080p x264 Tier 6', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p x264 Tier 6', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p x264 Tier 6', 'AVC', 'AVC'),
  ('1080p x264 Tier 6', 'Not HEVC', 'HEVC'),
  ('1080p x264 Tier 6', 'Not Remux', 'Remux'),
  ('1080p x264 Tier 6', 'Groups', '1080p x264 Tier 6 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p x264 Tier 6', 'Bluray', 'bluray'),
  ('1080p x264 Tier 6', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p x264 Tier 6', 'all', 3000)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Tier 1 Groups',
  '(?i)^(?:ATELiER|BBQ|BMF|c0kE|Chotab|CRiSC|CtrlHD|D\-Z0N3|Dariush|decibeL|DON|EbP|EDPH|Geek|LolHD|NCmt|PTer|REBORN|SoLaR|TayTO|TDD|TeamSyndicate|TnP|VietHD|ZoroSenpai|ZQ)$',
  'Named groups for 720p Tier 1. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('720p Tier 1', '720p Blu-ray or WEBRip from named tier 1 groups. Union of Dictionarry 720p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires 720p and does not match 1080p or 2160p.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('720p Tier 1', '720p'), ('720p Tier 1', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Tier 1', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Tier 1', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Tier 1', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Tier 1', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Tier 1', 'Groups', 'release_group', 'all', 0, 1),
  ('720p Tier 1', 'Bluray', 'source', 'all', 0, 0),
  ('720p Tier 1', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Tier 1', 'Resolution', '720p'),
  ('720p Tier 1', 'Not 1080p', '1080p'),
  ('720p Tier 1', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Tier 1', 'Not Remux', 'Remux'),
  ('720p Tier 1', 'Groups', '720p Tier 1 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Tier 1', 'Bluray', 'bluray'),
  ('720p Tier 1', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Tier 1', 'all', 3900)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Tier 2 Groups',
  '(?i)^(?:0BSiDiAN|EA|HiDt|HiFi|HiSD|IDE|iFT|NTb|QOQ|SA89|SbR)$',
  'Named groups for 720p Tier 2. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('720p Tier 2', '720p Blu-ray or WEBRip from named tier 2 groups. Union of Dictionarry 720p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires 720p and does not match 1080p or 2160p.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('720p Tier 2', '720p'), ('720p Tier 2', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Tier 2', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Tier 2', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Tier 2', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Tier 2', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Tier 2', 'Groups', 'release_group', 'all', 0, 1),
  ('720p Tier 2', 'Bluray', 'source', 'all', 0, 0),
  ('720p Tier 2', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Tier 2', 'Resolution', '720p'),
  ('720p Tier 2', 'Not 1080p', '1080p'),
  ('720p Tier 2', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Tier 2', 'Not Remux', 'Remux'),
  ('720p Tier 2', 'Groups', '720p Tier 2 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Tier 2', 'Bluray', 'bluray'),
  ('720p Tier 2', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Tier 2', 'all', 3720)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Tier 3 Groups',
  '(?i)^(?:BHDStudio|hallowed|HONE|LoRD|playHD|Positive|rightSIZE|SPHD|TBB|W4NK3R)$',
  'Named groups for 720p Tier 3. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('720p Tier 3', '720p Blu-ray or WEBRip from named tier 3 groups. Union of Dictionarry 720p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires 720p and does not match 1080p or 2160p.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('720p Tier 3', '720p'), ('720p Tier 3', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Tier 3', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Tier 3', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Tier 3', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Tier 3', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Tier 3', 'Groups', 'release_group', 'all', 0, 1),
  ('720p Tier 3', 'Bluray', 'source', 'all', 0, 0),
  ('720p Tier 3', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Tier 3', 'Resolution', '720p'),
  ('720p Tier 3', 'Not 1080p', '1080p'),
  ('720p Tier 3', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Tier 3', 'Not Remux', 'Remux'),
  ('720p Tier 3', 'Groups', '720p Tier 3 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Tier 3', 'Bluray', 'bluray'),
  ('720p Tier 3', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Tier 3', 'all', 3540)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Tier 4 Groups',
  '(?i)^(?:D\-ZON3|FoRM|Skazhutin|ThD)$',
  'Named groups for 720p Tier 4. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('720p Tier 4', '720p Blu-ray or WEBRip from named tier 4 groups. Union of Dictionarry 720p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires 720p and does not match 1080p or 2160p.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('720p Tier 4', '720p'), ('720p Tier 4', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Tier 4', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Tier 4', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Tier 4', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Tier 4', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Tier 4', 'Groups', 'release_group', 'all', 0, 1),
  ('720p Tier 4', 'Bluray', 'source', 'all', 0, 0),
  ('720p Tier 4', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Tier 4', 'Resolution', '720p'),
  ('720p Tier 4', 'Not 1080p', '1080p'),
  ('720p Tier 4', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Tier 4', 'Not Remux', 'Remux'),
  ('720p Tier 4', 'Groups', '720p Tier 4 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Tier 4', 'Bluray', 'bluray'),
  ('720p Tier 4', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Tier 4', 'all', 3360)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Tier 5 Groups',
  '(?i)^(?:AFKI|ARiN|AZVD|BAT1|BBW|BV|Cache|CALiGARi|CRiME|de\[42\]|DiRTY|E\.N\.D|E76|Eby|ENDSkY|ESiR|FANDANGO|FraMeSToR|Friday|FTO|GrapeHD|greenHD|GS88|GutS|HDL|HDMaNiAcS|HDV|HDv0T|HDxT|HiP|iLL|IMF|IMNEWHERE|iNFLiKTED|Ivandro|JewelBox|JKP|KamiKaze|KASHMiR|Krispy|Kururun|LAZY|LiNG|MCR|MDR|Moshy|Narkyy|NiP|nmd|NorTV|NoVA|NyHD|O2STK|OB1|OmertaHD|ORiGEN|PerfectionHD|PiPicK|RDK123|REPTiLE|RiCO|RO|rttr|SaNcTi|ShAnKs|SillyBird|SPEED|SuBHD|TAiCHi|ToK|WESTSiDE|WiHD|WiLF|WMING|ZIMBO|ZiNC)$',
  'Named groups for 720p Tier 5. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('720p Tier 5', '720p Blu-ray or WEBRip from named tier 5 groups. Union of Dictionarry 720p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires 720p and does not match 1080p or 2160p.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('720p Tier 5', '720p'), ('720p Tier 5', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Tier 5', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Tier 5', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Tier 5', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Tier 5', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Tier 5', 'Groups', 'release_group', 'all', 0, 1),
  ('720p Tier 5', 'Bluray', 'source', 'all', 0, 0),
  ('720p Tier 5', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Tier 5', 'Resolution', '720p'),
  ('720p Tier 5', 'Not 1080p', '1080p'),
  ('720p Tier 5', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Tier 5', 'Not Remux', 'Remux'),
  ('720p Tier 5', 'Groups', '720p Tier 5 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Tier 5', 'Bluray', 'bluray'),
  ('720p Tier 5', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Tier 5', 'all', 3180)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Tier 6 Groups',
  '(?i)^(?:CONSORTiUM|CREATiVE|eckomega|EuReKA|EwT|Funner|Gyroscope|HANDJOB|KnG|LEGi0N|Lulz|MaG|MKu|MTeam|MySiLU|PiG30N|PTP|PuTao|SaL|Slappy|SpaceHD|Spekt0r|Uld|WiKi|ZAL)$',
  'Named groups for 720p Tier 6. Better tier wins when Dumpstarr and Dictionarry disagree.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('720p Tier 6', '720p Blu-ray or WEBRip from named tier 6 groups. Union of Dictionarry 720p Quality tiers and Dumpstarr HD Blu-ray tiers, keeping the better tier. Requires 720p and does not match 1080p or 2160p.')
ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('720p Tier 6', '720p'), ('720p Tier 6', 'Release Group') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Tier 6', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Tier 6', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Tier 6', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Tier 6', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Tier 6', 'Groups', 'release_group', 'all', 0, 1),
  ('720p Tier 6', 'Bluray', 'source', 'all', 0, 0),
  ('720p Tier 6', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Tier 6', 'Resolution', '720p'),
  ('720p Tier 6', 'Not 1080p', '1080p'),
  ('720p Tier 6', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Tier 6', 'Not Remux', 'Remux'),
  ('720p Tier 6', 'Groups', '720p Tier 6 Groups')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Tier 6', 'Bluray', 'bluray'),
  ('720p Tier 6', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Tier 6', 'all', 3000)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = REPLACE(
  description,
  'A 1080p HEVC Blu-ray, WEB-DL, or WEBRip from a group outside that ladder scores 3000, and so does a 1080p AVC Blu-ray, WEB-DL, or WEBRip. Those two share the micro band and do not add to a tier that already matched. A 720p HEVC or AVC Blu-ray, WEB-DL, or WEBRip scores 3000 in its own quality group below every 1080p quality, so a tagged 720p cannot outrank a 1080p release.',
  'Named 1080p x264 Blu-ray and WEBRip groups, the union of Dictionarry and Dumpstarr with the better tier kept, score 3900, 3720, 3540, 3360, 3180, and 3000, under 1080p HEVC Tier 3. Named 720p groups use that same ladder in a quality group below every 1080p quality, so a tagged 720p cannot outrank a 1080p release. Unlisted groups are not grabbed.'
)
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Generic last resorts are gone', (SELECT COUNT(*) = 0 FROM custom_formats WHERE name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort', '720p Compact Last Resort'))),
  ('720p codec regex is gone', (SELECT COUNT(*) = 0 FROM regular_expressions WHERE name = '720p Last Resort Codec')),
  ('Six 1080p x264 tiers exist', (SELECT COUNT(*) = 6 FROM custom_formats WHERE name LIKE '1080p x264 Tier %')),
  ('Six 720p tiers exist', (SELECT COUNT(*) = 6 FROM custom_formats WHERE name LIKE '720p Tier %')),
  ('Movie scores are 3900 down to 3000', (SELECT COUNT(*) = 12 AND MIN(score) = 3000 AND MAX(score) = 3900 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND (custom_format_name LIKE '1080p x264 Tier %' OR custom_format_name LIKE '720p Tier %'))),
  ('1080p x264 tier 1 is 3900', (SELECT score = 3900 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p x264 Tier 1')),
  ('1080p x264 tier 6 is 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p x264 Tier 6')),
  ('1080p x264 tier 1 is under HEVC tier 3', (SELECT x.score < h.score FROM quality_profile_custom_formats x JOIN quality_profile_custom_formats h ON h.quality_profile_name = x.quality_profile_name WHERE x.quality_profile_name = 'Movies 2160p HEVC Compact' AND x.custom_format_name = '1080p x264 Tier 1' AND h.custom_format_name = '1080p Compact HEVC Tier 3')),
  ('TV scores none of the new tiers', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND (custom_format_name LIKE '1080p x264 Tier %' OR custom_format_name LIKE '720p Tier %'))),
  ('1080p HEVC ladder stays', (SELECT COUNT(*) = 5 AND SUM(CASE custom_format_name WHEN '1080p Compact HEVC Tier 1' THEN score WHEN '1080p Compact HEVC Tier 2' THEN score WHEN '1080p Compact Streaming WEB-DL' THEN score WHEN '1080p Compact HEVC Tier 3' THEN score WHEN '1080p Compact HEVC Tier 4' THEN score END) = 9600 + 6400 + 5200 + 4100 + 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Tier 1', '1080p Compact HEVC Tier 2', '1080p Compact Streaming WEB-DL', '1080p Compact HEVC Tier 3', '1080p Compact HEVC Tier 4'))),
  ('4K scores stay put', (SELECT COUNT(*) = 9 AND SUM(score) = 38400 + 35200 + 32000 + 28800 + 28800 + 25600 + 19200 + 0 + 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('2160p Compact Bluray Tier 1', '2160p Compact Bluray Tier 2', '2160p Compact WEB Tier 1', '2160p Compact Streaming WEB-DL', '2160p Compact WEB Tier 2', '2160p Compact Bluray Tier 3', '2160p Compact WEB Tier 3', '2160p Compact Bluray Tier 4', '2160p Compact WEB Tier 4'))),
  ('Minimum and cutoff stay 3000 / 41600', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('x265 (HD) stays off the movie profile', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'x265 (HD)')),
  ('720p rank stays under 1080p', (SELECT p720.position > p1080.position AND p1080.position > p2160.position AND p720.enabled = 1 AND p2160.upgrade_until = 1 AND p720.upgrade_until = 0 FROM quality_profile_qualities p720 JOIN quality_profile_qualities p1080 ON p1080.quality_profile_name = p720.quality_profile_name JOIN quality_profile_qualities p2160 ON p2160.quality_profile_name = p720.quality_profile_name WHERE p720.quality_profile_name = 'Movies 2160p HEVC Compact' AND p720.quality_group_name = '720p Fallback' AND p1080.quality_group_name = '1080p Fallback' AND p2160.quality_group_name = '2160p')),
  ('TV still has no 720p qualities', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND quality_name LIKE '%720p%')),
  ('DON is 1080p x264 tier 1', (SELECT pattern LIKE '%DON%' AND pattern NOT LIKE '%NAPTiME%' AND pattern NOT LIKE '%POWER%' AND pattern NOT LIKE '%POIASD%' FROM regular_expressions WHERE name = '1080p x264 Tier 1 Groups')),
  ('PTer was promoted to 1080p tier 1', (SELECT pattern LIKE '%PTer%' FROM regular_expressions WHERE name = '1080p x264 Tier 1 Groups')),
  ('PTer is not also tier 5', (SELECT pattern NOT LIKE '%PTer%' FROM regular_expressions WHERE name = '1080p x264 Tier 5 Groups')),
  ('W4NK3R is 1080p tier 3', (SELECT pattern LIKE '%W4NK3R%' FROM regular_expressions WHERE name = '1080p x264 Tier 3 Groups')),
  ('FraMeSToR is 1080p tier 6', (SELECT pattern LIKE '%FraMeSToR%' FROM regular_expressions WHERE name = '1080p x264 Tier 6 Groups')),
  ('P0W4HD is tier 6 and POWER is absent', (SELECT t6.pattern LIKE '%P0W4HD%' AND t6.pattern NOT LIKE '%POWER%' AND t1.pattern NOT LIKE '%POWER%' FROM regular_expressions t6 JOIN regular_expressions t1 ON t1.name = '1080p x264 Tier 1 Groups' WHERE t6.name = '1080p x264 Tier 6 Groups')),
  ('HQMUX stays on 1080p tier 5', (SELECT pattern LIKE '%HQMUX%' AND pattern LIKE '%Kitsune%' FROM regular_expressions WHERE name = '1080p x264 Tier 5 Groups')),
  ('1080p tiers require AVC and negate HEVC', (SELECT COUNT(*) = 6 FROM custom_format_conditions c JOIN condition_patterns p ON p.custom_format_name = c.custom_format_name AND p.condition_name = c.name WHERE c.custom_format_name LIKE '1080p x264 Tier %' AND c.name = 'Not HEVC' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name = 'HEVC')),
  ('720p tiers negate 1080p and 2160p', (SELECT COUNT(*) = 12 FROM condition_resolutions WHERE custom_format_name LIKE '720p Tier %' AND resolution IN ('1080p', '2160p'))),
  ('720p size stays 0 / 1990 / 0', (SELECT COUNT(*) = 3 AND MIN(preferred_size) = 1990 AND MAX(preferred_size) = 1990 AND MIN(max_size) = 0 AND MAX(max_size) = 0 AND MIN(min_size) = 0 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-720p', 'WEBDL-720p', 'WEBRip-720p'))),
  ('Profile text names the curated tiers', (SELECT description LIKE '%Named 1080p x264 Blu-ray and WEBRip groups%' FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact'));
DROP TABLE _pcd_assertions;

COMMIT;
