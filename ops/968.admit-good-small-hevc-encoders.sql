-- @description: Let the small encodes that survive a 55-inch Mini LED and a 32-inch 4K monitor into the ladder
-- @author: cursor
-- @name: 968.admit-good-small-hevc-encoders

BEGIN TRANSACTION;

-- d3g is banned by the shared Dictionarry list. On a 4K Mini LED their Blu-ray
-- encodes are in the same band as Vyndros for a lot of people, so this profile
-- stops treating that one tag as trash. YTS stays banned.
DELETE FROM condition_patterns WHERE custom_format_name = 'Banned Groups' AND condition_name = 'd3g';
DELETE FROM custom_format_conditions WHERE custom_format_name = 'Banned Groups' AND name = 'd3g';

-- RARBG is only on the efficient/regular ban lists. Their pre-2023 x265 encodes
-- were often the best file under 3 GB. Keep the rest of those bans.
DELETE FROM condition_patterns
WHERE custom_format_name IN ('Banned Groups (Efficient)', 'Banned Groups (Regular)')
  AND regular_expression_name = 'RARBG';
DELETE FROM custom_format_conditions
WHERE custom_format_name IN ('Banned Groups (Efficient)', 'Banned Groups (Regular)')
  AND name = 'RARBG';

INSERT INTO regular_expressions (name, pattern, description) VALUES ('HEVC Compact Small', '(?i)(?:^\[(?:D0ct0rLew|PSARips|ReELiTE|ELiTE|Kira|d3g|PSA|SEV)\]|(?:^|[-.\s(\[])(?:D0ct0rLew|PSARips|ReELiTE|ELiTE|Kira|d3g|PSA|SEV)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', 'Small 4K/1080p HEVC that still holds up on a 55-inch Mini LED and a 32-inch 4K monitor: PSA, d3g, SEV, ELiTE.')
ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO regular_expressions (name, pattern, description) VALUES ('HEVC Compact Micro OK', '(?i)(?:^\[(?:RARBG|iVy|Joy|UTR)\]|(?:^|[-.\s(\[])(?:RARBG|iVy|Joy|UTR)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)', 'Watchable smaller encodes (UTR/Joy, RARBG, iVy). Below PSA and QxR, grabbed when nothing better exists.')
ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

UPDATE regular_expressions SET pattern = '(?i)(?:^\[(?:GalaxyRG|HDHub4u|MeGusta|ION265|RMTeam|ION10|aXXo|Pahe|YIFY|EVO|QxC|TGx|YTS)\]|(?:^|[-.\s(\[])(?:GalaxyRG|HDHub4u|MeGusta|ION265|RMTeam|ION10|aXXo|Pahe|YIFY|EVO|QxC|TGx|YTS)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)',
  description = 'Hard-rejects encodes that fall apart on a 55-inch Mini LED and a close-up 32-inch 4K monitor: YTS, MeGusta, GalaxyRG, Pahe and the other bit-starved mills.'
WHERE name = 'HEVC Compact Micro Ban';

UPDATE custom_formats SET description = 'Rejects YTS, MeGusta and the other bit-starved mills. PSA, UTR, RARBG and iVy are scored separately.'
WHERE name = 'Banned Micro Encodes';

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact Bluray Tier 3', '4K Blu-ray HEVC from PSA, d3g, SEV and ELiTE. Smaller than QxR, still clean on a 55-inch Mini LED and a 32-inch 4K monitor.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact Bluray Tier 3', 'Release Group'), ('2160p Compact Bluray Tier 3', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 3', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact Bluray Tier 3', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 3', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 3', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 3', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 3', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 3', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 3', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 3', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 3', 'Groups', 'HEVC Compact Small') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 3', 'Bluray', 'source', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact Bluray Tier 3', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact Bluray Tier 4', '4K Blu-ray HEVC from UTR/Joy, RARBG and iVy. Watchable and small; upgraded when PSA, QxR or HONE exists.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact Bluray Tier 4', 'Release Group'), ('2160p Compact Bluray Tier 4', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 4', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact Bluray Tier 4', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 4', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 4', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 4', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 4', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 4', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 4', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 4', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact Bluray Tier 4', 'Groups', 'HEVC Compact Micro OK') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact Bluray Tier 4', 'Bluray', 'source', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact Bluray Tier 4', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact WEB Tier 3', '4K WEB HEVC from PSA, d3g, SEV and ELiTE.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact WEB Tier 3', 'Release Group'), ('2160p Compact WEB Tier 3', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact WEB Tier 3', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 3', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 3', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 3', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 3', 'Groups', 'HEVC Compact Small') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'Not Bluray', 'source', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 3', 'Not Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 3', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 3', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 3', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('2160p Compact WEB Tier 4', '4K WEB HEVC from UTR/Joy, RARBG and iVy.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('2160p Compact WEB Tier 4', 'Release Group'), ('2160p Compact WEB Tier 4', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('2160p Compact WEB Tier 4', 'Resolution', '2160p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 4', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 4', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 4', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('2160p Compact WEB Tier 4', 'Groups', 'HEVC Compact Micro OK') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'Not Bluray', 'source', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 4', 'Not Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 4', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('2160p Compact WEB Tier 4', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('2160p Compact WEB Tier 4', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('1080p Compact HEVC Tier 3', '1080p HEVC fallback from PSA, d3g, SEV and ELiTE.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p Compact HEVC Tier 3', 'Release Group'), ('1080p Compact HEVC Tier 3', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p Compact HEVC Tier 3', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 3', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 3', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 3', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 3', 'Groups', 'HEVC Compact Small') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'Bluray', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 3', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 3', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 3', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 3', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

INSERT INTO custom_formats (name, description) VALUES ('1080p Compact HEVC Tier 4', '1080p HEVC fallback from UTR/Joy, RARBG and iVy.') ON CONFLICT (name) DO UPDATE SET description = excluded.description;
INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ('1080p Compact HEVC Tier 4', 'Release Group'), ('1080p Compact HEVC Tier 4', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'Resolution', 'resolution', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('1080p Compact HEVC Tier 4', 'Resolution', '1080p') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'HEVC', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 4', 'HEVC', 'HEVC') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'Not AV1', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 4', 'Not AV1', 'AV1') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'Not Remux', 'release_title', 'all', 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 4', 'Not Remux', 'Remux') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'Groups', 'release_title', 'all', 0, 1) ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('1080p Compact HEVC Tier 4', 'Groups', 'HEVC Compact Micro OK') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'Bluray', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 4', 'Bluray', 'bluray') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'WEB-DL', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 4', 'WEB-DL', 'web_dl') ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('1080p Compact HEVC Tier 4', 'WEBRip', 'source', 'all', 0, 0) ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('1080p Compact HEVC Tier 4', 'WEBRip', 'webrip') ON CONFLICT DO NOTHING;

UPDATE quality_profiles SET minimum_custom_format_score = 400, description = 'Compact 4K HEVC for a 55-inch Mini LED and a 32-inch 4K monitor. HONE, Vyndros and edge2020 first, then QxR/TAoE, then PSA/d3g/SEV/ELiTE, then UTR/RARBG/iVy. YTS and MeGusta stay rejected.' WHERE name = 'Movies 2160p HEVC Compact';
UPDATE quality_profiles SET minimum_custom_format_score = 400, description = 'Compact 4K HEVC episodes for the same screens. WEB from those circles first, then disc. PSA and UTR can fill gaps. YTS and MeGusta stay rejected.' WHERE name = 'TV 2160p HEVC Compact';

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 1', 'all', 8100),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 2', 'all', 7400),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 3', 'all', 6700),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 4', 'all', 6000),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 5300),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 4600),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 3', 'all', 3900),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 4', 'all', 3200),
  ('Movies 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 2500),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 1', 'all', 1800),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 2', 'all', 1100),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 3', 'all', 400),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 4', 'all', 400),
  ('TV 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 8100),
  ('TV 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 7400),
  ('TV 2160p HEVC Compact', '2160p Compact WEB Tier 3', 'all', 6700),
  ('TV 2160p HEVC Compact', '2160p Compact WEB Tier 4', 'all', 6000),
  ('TV 2160p HEVC Compact', '2160p Compact Bluray Tier 1', 'all', 5300),
  ('TV 2160p HEVC Compact', '2160p Compact Bluray Tier 2', 'all', 4600),
  ('TV 2160p HEVC Compact', '2160p Compact Bluray Tier 3', 'all', 3900),
  ('TV 2160p HEVC Compact', '2160p Compact Bluray Tier 4', 'all', 3200),
  ('TV 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 2500),
  ('TV 2160p HEVC Compact', '1080p Compact HEVC Tier 1', 'all', 1800),
  ('TV 2160p HEVC Compact', '1080p Compact HEVC Tier 2', 'all', 1100),
  ('TV 2160p HEVC Compact', '1080p Compact HEVC Tier 3', 'all', 400),
  ('TV 2160p HEVC Compact', '1080p Compact HEVC Tier 4', 'all', 400)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

-- Preferred size leans toward the small good encodes (~4 GB per two hours).
-- Max still fits an HONE 4K disc encode.
UPDATE radarr_quality_definitions
SET min_size = 6, preferred_size = 32, max_size = 200
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');
UPDATE sonarr_quality_definitions
SET min_size = 5, preferred_size = 28, max_size = 160
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('d3g no longer in Banned Groups', (SELECT count(*) = 0 FROM custom_format_conditions WHERE custom_format_name = 'Banned Groups' AND name = 'd3g')),
  ('RARBG removed from efficient ban', (SELECT count(*) = 0 FROM condition_patterns WHERE custom_format_name = 'Banned Groups (Efficient)' AND regular_expression_name = 'RARBG')),
  ('Movie minimum is 400', (SELECT minimum_custom_format_score = 400 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('PSA tier sits under QxR', (SELECT score = 6700 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 3')),
  ('UTR tier sits under PSA', (SELECT score = 6000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 4')),
  ('YTS still hard banned', (SELECT score = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Banned Micro Encodes'));
DROP TABLE _pcd_assertions;

COMMIT;
