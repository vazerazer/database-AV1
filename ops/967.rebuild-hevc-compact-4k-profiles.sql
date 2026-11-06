-- @description: Replace the AV1 flagship with compact 4K HEVC profiles for Radarr and Sonarr
-- @author: cursor
-- @name: 967.rebuild-hevc-compact-4k-profiles

BEGIN TRANSACTION;

-- Retire the AV1 flagship. Child rows cascade, but clear them explicitly so a partial
-- schema without cascade still ends with a single compact ladder.
DELETE FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p AV1 HQ';
DELETE FROM quality_profile_qualities WHERE quality_profile_name = 'Movies 2160p AV1 HQ';
DELETE FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p AV1 HQ';
DELETE FROM quality_groups WHERE quality_profile_name = 'Movies 2160p AV1 HQ';
DELETE FROM quality_profile_tags WHERE quality_profile_name = 'Movies 2160p AV1 HQ';
DELETE FROM quality_profile_languages WHERE quality_profile_name = 'Movies 2160p AV1 HQ';
DELETE FROM quality_profiles WHERE name = 'Movies 2160p AV1 HQ';

INSERT INTO tags (name) VALUES ('HEVC'), ('2160p'), ('Compact') ON CONFLICT (name) DO NOTHING;

INSERT INTO regular_expressions (name, pattern, description) VALUES ('HEVC Compact Elite', '(?i)(?:^\[(?:TimeDistortion|bluegreeen|Chivaman|edge2020|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|YELLO|DarQ|HONE)\]|(?:^|[-.\s(\[])(?:TimeDistortion|bluegreeen|Chivaman|edge2020|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|YELLO|DarQ|HONE)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', 'Trailing-group match for Dictionarry compact tier-1 circles that also publish careful 4K HEVC: HONE, Vyndros, edge2020, dkore and the compact Blu-ray tier.')
ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO regular_expressions (name, pattern, description) VALUES ('HEVC Compact Circle', '(?i)(?:^\[(?:FreetheFish|Nostradamus|DrainedDay|Species180|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|LION|MNHD|NAN0|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)\]|(?:^|[-.\s(\[])(?:FreetheFish|Nostradamus|DrainedDay|Species180|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|LION|MNHD|NAN0|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', 'Trailing-group match for the QxR and TAoE encoder circles plus the remaining Dictionarry compact movie groups.')
ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO regular_expressions (name, pattern, description) VALUES ('HEVC Compact WEB-DL', '(?i)(?:^\[(?:BLUTONiUM|DUSKLiGHT|Kitsune|NOSiViD|playWEB|CMRioG|4KBEC|ABBIE|AJP69|BYNDR|CEBEX|CMaRG|HHWEB|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|CMRG|FLUX|RAWR|NTb|SiC)\]|(?:^|[-.\s(\[])(?:BLUTONiUM|DUSKLiGHT|Kitsune|NOSiViD|playWEB|CMRioG|4KBEC|ABBIE|AJP69|BYNDR|CEBEX|CMaRG|HHWEB|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|CMRG|FLUX|RAWR|NTb|SiC)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', 'Trailing-group match for untouched 4K HEVC WEB-DL groups used only as a larger fallback when no compact encode exists.')
ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO regular_expressions (name, pattern, description) VALUES ('HEVC Compact Micro Ban', '(?i)(?:^\[(?:GalaxyRG|HDHub4u|MeGusta|PSARips|ION265|RMTeam|ION10|RARBG|aXXo|Pahe|YIFY|EVO|iVy|Joy|PSA|QxC|TGx|UTR|YTS)\]|(?:^|[-.\s(\[])(?:GalaxyRG|HDHub4u|MeGusta|PSARips|ION265|RMTeam|ION10|RARBG|aXXo|Pahe|YIFY|EVO|iVy|Joy|PSA|QxC|TGx|UTR|YTS)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', 'Trailing-group match for micro and low-quality 4K reencode tags (UTR, MeGusta, YTS, RARBG, PSA, iVy) kept out of the compact ladder.')
ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact Bluray Tier 1', '4K Blu-ray HEVC from the careful compact circles (HONE, Vyndros, edge2020, dkore and Dictionarry compact Blu-ray tier 1).') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact Bluray Tier 1', 'Release Group'), ('2160p Compact Bluray Tier 1', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 1', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact Bluray Tier 1', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 1', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 1', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 1', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 1', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 1', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 1', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 1', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 1', 'Groups', 'HEVC Compact Elite') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 1', 'Bluray', 'source', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact Bluray Tier 1', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact Bluray Tier 2', '4K Blu-ray HEVC from the QxR and TAoE circles and the rest of the Dictionarry compact movie groups.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact Bluray Tier 2', 'Release Group'), ('2160p Compact Bluray Tier 2', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 2', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact Bluray Tier 2', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 2', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 2', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 2', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 2', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 2', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 2', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 2', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 2', 'Groups', 'HEVC Compact Circle') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 2', 'Bluray', 'source', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact Bluray Tier 2', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact WEB Tier 1', '4K WEB HEVC from the same careful compact circles. Prefers a small encode over an untouched WEB-DL.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact WEB Tier 1', 'Release Group'), ('2160p Compact WEB Tier 1', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact WEB Tier 1', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 1', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 1', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 1', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 1', 'Groups', 'HEVC Compact Elite') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'Not Bluray', 'source', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 1', 'Not Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 1', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 1', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 1', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact WEB Tier 2', '4K WEB HEVC from the QxR and TAoE circles, including parenthetical member tags such as -Tigole)[TAoE].') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact WEB Tier 2', 'Release Group'), ('2160p Compact WEB Tier 2', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact WEB Tier 2', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 2', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 2', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 2', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 2', 'Groups', 'HEVC Compact Circle') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'Not Bluray', 'source', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 2', 'Not Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 2', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 2', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 2', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p WEB-DL HEVC', 'Untouched 4K HEVC WEB-DL groups (NTb, FLUX, CMRG, TEPES and peers). Larger than a compact encode, grabbed only when no compact group is available.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p WEB-DL HEVC', 'Release Group'), ('2160p WEB-DL HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p WEB-DL HEVC', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p WEB-DL HEVC', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p WEB-DL HEVC', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p WEB-DL HEVC', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p WEB-DL HEVC', 'Groups', 'HEVC Compact WEB-DL') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'Not Bluray', 'source', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p WEB-DL HEVC', 'Not Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p WEB-DL HEVC', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p WEB-DL HEVC', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p WEB-DL HEVC', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('1080p Compact HEVC Tier 1', '1080p HEVC fallback from the careful compact circles when no 4K compact encode exists.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p Compact HEVC Tier 1', 'Release Group'), ('1080p Compact HEVC Tier 1', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p Compact HEVC Tier 1', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 1', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 1', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 1', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 1', 'Groups', 'HEVC Compact Elite') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'Bluray', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 1', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 1', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 1', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 1', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('1080p Compact HEVC Tier 2', '1080p HEVC fallback from the QxR and TAoE circles.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p Compact HEVC Tier 2', 'Release Group'), ('1080p Compact HEVC Tier 2', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p Compact HEVC Tier 2', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 2', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 2', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 2', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 2', 'Groups', 'HEVC Compact Circle') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'Bluray', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 2', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 2', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 2', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 2', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('Banned Micro Encodes', 'Rejects micro and public-tracker 4K reencodes (UTR, MeGusta, YTS, RARBG, PSA, iVy, GalaxyRG) that Dictionarry compact also refuses.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('Banned Micro Encodes', 'Release Group'), ('Banned Micro Encodes', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Banned Micro Encodes', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Banned Micro Encodes', 'Groups', 'HEVC Compact Micro Ban') ON CONFLICT DO NOTHING;

INSERT INTO quality_profiles (name, description, upgrades_allowed, minimum_custom_format_score, upgrade_until_score, upgrade_score_increment)
VALUES
  ('Movies 2160p HEVC Compact', 'Compact 4K HEVC movie profile. Prefers small 2160p x265 encodes from HONE, Vyndros, edge2020, dkore and the QxR/TAoE circles, then untouched 4K WEB-DL, then 1080p HEVC. AV1, remuxes and micro encodes are rejected. HDR, Dolby Vision and Atmos break ties inside a tier.', 1, 700, 10000, 1),
  ('TV 2160p HEVC Compact', 'Compact 4K HEVC episodic profile. Prefers 2160p WEB HEVC from the same compact circles, then disc encodes, then untouched WEB-DL, then 1080p HEVC. AV1, remuxes and micro encodes are rejected.', 1, 700, 10000, 1)
ON CONFLICT (name) DO UPDATE SET
  description = excluded.description,
  upgrades_allowed = excluded.upgrades_allowed,
  minimum_custom_format_score = excluded.minimum_custom_format_score,
  upgrade_until_score = excluded.upgrade_until_score,
  upgrade_score_increment = excluded.upgrade_score_increment;

INSERT INTO quality_profile_tags (quality_profile_name, tag_name) VALUES
  ('Movies 2160p HEVC Compact', 'HEVC'),
  ('Movies 2160p HEVC Compact', '2160p'),
  ('Movies 2160p HEVC Compact', 'Compact'),
  ('TV 2160p HEVC Compact', 'HEVC'),
  ('TV 2160p HEVC Compact', '2160p'),
  ('TV 2160p HEVC Compact', 'Compact')
ON CONFLICT DO NOTHING;

INSERT INTO quality_profile_languages (quality_profile_name, language_name, type) VALUES
  ('Movies 2160p HEVC Compact', 'Any', 'simple'),
  ('TV 2160p HEVC Compact', 'Any', 'simple')
ON CONFLICT DO NOTHING;

INSERT INTO quality_groups (quality_profile_name, name) VALUES ('Movies 2160p HEVC Compact', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('Movies 2160p HEVC Compact', '2160p', 'Bluray-2160p', 0) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('Movies 2160p HEVC Compact', '2160p', 'WEBDL-2160p', 1) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('Movies 2160p HEVC Compact', '2160p', 'WEBRip-2160p', 2) ON CONFLICT DO NOTHING;
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('Movies 2160p HEVC Compact', '1080p Fallback') ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('Movies 2160p HEVC Compact', '1080p Fallback', 'Bluray-1080p', 0) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('Movies 2160p HEVC Compact', '1080p Fallback', 'WEBDL-1080p', 1) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('Movies 2160p HEVC Compact', '1080p Fallback', 'WEBRip-1080p', 2) ON CONFLICT DO NOTHING;

INSERT INTO quality_groups (quality_profile_name, name) VALUES ('TV 2160p HEVC Compact', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '2160p', 'WEBDL-2160p', 0) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '2160p', 'WEBRip-2160p', 1) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '2160p', 'Bluray-2160p', 2) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '2160p', 'HDTV-2160p', 3) ON CONFLICT DO NOTHING;
INSERT INTO quality_groups (quality_profile_name, name) VALUES ('TV 2160p HEVC Compact', '1080p Fallback') ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '1080p Fallback', 'WEBDL-1080p', 0) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '1080p Fallback', 'WEBRip-1080p', 1) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '1080p Fallback', 'Bluray-1080p', 2) ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES ('TV 2160p HEVC Compact', '1080p Fallback', 'HDTV-1080p', 3) ON CONFLICT DO NOTHING;

INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, enabled, upgrade_until) VALUES
  ('Movies 2160p HEVC Compact', '2160p', 0, 1, 1),
  ('Movies 2160p HEVC Compact', '1080p Fallback', 1, 1, 0),
  ('TV 2160p HEVC Compact', '2160p', 0, 1, 1),
  ('TV 2160p HEVC Compact', '1080p Fallback', 1, 1, 0)
ON CONFLICT DO NOTHING;

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', 'Dolby Vision', 'all', 180),
  ('Movies 2160p HEVC Compact', 'Atmos', 'all', 80),
  ('Movies 2160p HEVC Compact', 'HDR10+', 'all', 50),
  ('Movies 2160p HEVC Compact', 'HDR', 'all', 40),
  ('Movies 2160p HEVC Compact', 'IMAX', 'all', 40),
  ('Movies 2160p HEVC Compact', 'IMAX Enhanced', 'all', 40),
  ('Movies 2160p HEVC Compact', 'Dolby Digital +', 'all', 40),
  ('Movies 2160p HEVC Compact', '10-bit Depth', 'all', 30),
  ('Movies 2160p HEVC Compact', 'DTS-HD MA', 'all', 25),
  ('Movies 2160p HEVC Compact', 'DTS-X', 'all', 25),
  ('Movies 2160p HEVC Compact', 'DTS-HD HRA', 'all', 25),
  ('Movies 2160p HEVC Compact', 'DTS-ES', 'all', 25),
  ('Movies 2160p HEVC Compact', 'DTS', 'all', 25),
  ('Movies 2160p HEVC Compact', 'Special Edition', 'all', 20),
  ('Movies 2160p HEVC Compact', 'Dolby Digital', 'all', 20),
  ('Movies 2160p HEVC Compact', 'TrueHD', 'all', 15),
  ('Movies 2160p HEVC Compact', 'Hybrid', 'all', 15),
  ('Movies 2160p HEVC Compact', 'AMZN', 'all', 15),
  ('Movies 2160p HEVC Compact', 'DSNP', 'all', 15),
  ('Movies 2160p HEVC Compact', 'NF', 'all', 15),
  ('Movies 2160p HEVC Compact', 'MAX', 'all', 15),
  ('Movies 2160p HEVC Compact', 'ATVP', 'all', 15),
  ('Movies 2160p HEVC Compact', 'HULU', 'all', 10),
  ('Movies 2160p HEVC Compact', 'iT', 'all', 10),
  ('Movies 2160p HEVC Compact', 'ATV', 'all', 10),
  ('Movies 2160p HEVC Compact', 'FLAC', 'all', 10),
  ('Movies 2160p HEVC Compact', 'Opus 5.1 / 7.1', 'all', 10),
  ('Movies 2160p HEVC Compact', '4K Remaster', 'all', 10),
  ('Movies 2160p HEVC Compact', 'Repack3', 'all', 7),
  ('Movies 2160p HEVC Compact', 'Repack2', 'all', 6),
  ('Movies 2160p HEVC Compact', 'Repack1', 'all', 5),
  ('Movies 2160p HEVC Compact', 'AAC', 'all', 5),
  ('Movies 2160p HEVC Compact', 'Foreign Dub', 'all', -750),
  ('Movies 2160p HEVC Compact', '8-bit Depth', 'all', -800),
  ('Movies 2160p HEVC Compact', 'AV1', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'VP9', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'VVC', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Remux', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'x264 (2160p)', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Banned Micro Encodes', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Banned Groups', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Banned Groups (Efficient)', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Banned Groups (Regular)', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'CAM', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Upscale', 'all', -10000),
  ('Movies 2160p HEVC Compact', '3D', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Extras', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Sing Along', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Full Disc', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Full Disc (Quality Match)', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Audio Description', 'all', -10000),
  ('Movies 2160p HEVC Compact', 'Hardcoded Subtitles', 'all', -10000),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 1', 'all', 4600),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 2', 'all', 3900),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 3200),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 2500),
  ('Movies 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 1800),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 1', 'all', 1100),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 2', 'all', 700),
  ('TV 2160p HEVC Compact', 'Dolby Vision', 'all', 180),
  ('TV 2160p HEVC Compact', 'Atmos', 'all', 80),
  ('TV 2160p HEVC Compact', 'HDR10+', 'all', 50),
  ('TV 2160p HEVC Compact', 'HDR', 'all', 40),
  ('TV 2160p HEVC Compact', 'IMAX', 'all', 40),
  ('TV 2160p HEVC Compact', 'IMAX Enhanced', 'all', 40),
  ('TV 2160p HEVC Compact', 'Dolby Digital +', 'all', 40),
  ('TV 2160p HEVC Compact', '10-bit Depth', 'all', 30),
  ('TV 2160p HEVC Compact', 'DTS-HD MA', 'all', 25),
  ('TV 2160p HEVC Compact', 'DTS-X', 'all', 25),
  ('TV 2160p HEVC Compact', 'DTS-HD HRA', 'all', 25),
  ('TV 2160p HEVC Compact', 'DTS-ES', 'all', 25),
  ('TV 2160p HEVC Compact', 'DTS', 'all', 25),
  ('TV 2160p HEVC Compact', 'Special Edition', 'all', 20),
  ('TV 2160p HEVC Compact', 'Dolby Digital', 'all', 20),
  ('TV 2160p HEVC Compact', 'TrueHD', 'all', 15),
  ('TV 2160p HEVC Compact', 'Hybrid', 'all', 15),
  ('TV 2160p HEVC Compact', 'AMZN', 'all', 15),
  ('TV 2160p HEVC Compact', 'DSNP', 'all', 15),
  ('TV 2160p HEVC Compact', 'NF', 'all', 15),
  ('TV 2160p HEVC Compact', 'MAX', 'all', 15),
  ('TV 2160p HEVC Compact', 'ATVP', 'all', 15),
  ('TV 2160p HEVC Compact', 'HULU', 'all', 10),
  ('TV 2160p HEVC Compact', 'iT', 'all', 10),
  ('TV 2160p HEVC Compact', 'ATV', 'all', 10),
  ('TV 2160p HEVC Compact', 'FLAC', 'all', 10),
  ('TV 2160p HEVC Compact', 'Opus 5.1 / 7.1', 'all', 10),
  ('TV 2160p HEVC Compact', '4K Remaster', 'all', 10),
  ('TV 2160p HEVC Compact', 'Repack3', 'all', 7),
  ('TV 2160p HEVC Compact', 'Repack2', 'all', 6),
  ('TV 2160p HEVC Compact', 'Repack1', 'all', 5),
  ('TV 2160p HEVC Compact', 'AAC', 'all', 5),
  ('TV 2160p HEVC Compact', 'Foreign Dub', 'all', -750),
  ('TV 2160p HEVC Compact', '8-bit Depth', 'all', -800),
  ('TV 2160p HEVC Compact', 'AV1', 'all', -10000),
  ('TV 2160p HEVC Compact', 'VP9', 'all', -10000),
  ('TV 2160p HEVC Compact', 'VVC', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Remux', 'all', -10000),
  ('TV 2160p HEVC Compact', 'x264 (2160p)', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Banned Micro Encodes', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Banned Groups', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Banned Groups (Efficient)', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Banned Groups (Regular)', 'all', -10000),
  ('TV 2160p HEVC Compact', 'CAM', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Upscale', 'all', -10000),
  ('TV 2160p HEVC Compact', '3D', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Extras', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Sing Along', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Full Disc', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Full Disc (Quality Match)', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Dolby Vision (Without Fallback)', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Audio Description', 'all', -10000),
  ('TV 2160p HEVC Compact', 'Hardcoded Subtitles', 'all', -10000),
  ('TV 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 4600),
  ('TV 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 3900),
  ('TV 2160p HEVC Compact', '2160p Compact Bluray Tier 1', 'all', 3200),
  ('TV 2160p HEVC Compact', '2160p Compact Bluray Tier 2', 'all', 2500),
  ('TV 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 1800),
  ('TV 2160p HEVC Compact', '1080p Compact HEVC Tier 1', 'all', 1100),
  ('TV 2160p HEVC Compact', '1080p Compact HEVC Tier 2', 'all', 700),
  ('TV 2160p HEVC Compact', 'Season Pack', 'all', 25)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

-- Compact 4K budgets, in MB/min. A two-hour movie lands around 1-19 GB,
-- which covers QxR/TAoE/HONE and rejects remux-sized encodes.
UPDATE radarr_quality_definitions
SET min_size = 8, preferred_size = 45, max_size = 160
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');
UPDATE radarr_quality_definitions
SET min_size = 3, preferred_size = 14, max_size = 40
WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p');
UPDATE sonarr_quality_definitions
SET min_size = 8, preferred_size = 40, max_size = 140
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');
UPDATE sonarr_quality_definitions
SET min_size = 2, preferred_size = 10, max_size = 30
WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p');

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('AV1 flagship removed', (SELECT count(*) = 0 FROM quality_profiles WHERE name = 'Movies 2160p AV1 HQ')),
  ('Movie profile present', (SELECT count(*) = 1 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact' AND minimum_custom_format_score = 700)),
  ('TV profile present', (SELECT count(*) = 1 FROM quality_profiles WHERE name = 'TV 2160p HEVC Compact' AND upgrade_until_score = 10000)),
  ('No remux qualities', (SELECT count(*) = 0 FROM quality_group_members WHERE quality_profile_name IN ('Movies 2160p HEVC Compact', 'TV 2160p HEVC Compact') AND quality_name LIKE 'Remux%')),
  ('Movie bluray tier leads', (SELECT score = 4600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('TV web tier leads', (SELECT score = 4600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('AV1 hard banned', (SELECT count(*) = 2 FROM quality_profile_custom_formats WHERE custom_format_name = 'AV1' AND score = -10000 AND quality_profile_name LIKE '%HEVC Compact')),
  ('Compact formats require HEVC', (SELECT count(*) = 7 FROM condition_patterns WHERE regular_expression_name = 'HEVC' AND custom_format_name IN ('2160p Compact Bluray Tier 1','2160p Compact Bluray Tier 2','2160p Compact WEB Tier 1','2160p Compact WEB Tier 2','2160p WEB-DL HEVC','1080p Compact HEVC Tier 1','1080p Compact HEVC Tier 2')));
DROP TABLE _pcd_assertions;

COMMIT;

