-- @description: Score Movies 2160p HEVC Compact like Dumpstarr's direct-play 4K profile, without touching the compact group lists
-- @author: cursor
-- @name: 972.movies-2160p-dumpstarr-direct-play

BEGIN TRANSACTION;

-- Dumpstarr Movies 2160p blocks TrueHD, DTS-HD MA, DTS-HD HRA and DTS-X so a
-- TV can direct-play the file, scores Dolby Vision +1000, HDR and HDR10+ +500,
-- and Dolby Digital + +125, and rejects a 4K Blu-ray with no HDR fallback.
-- Their tier steps are about 50 points, so a -10000 penalty clears a tier.
-- Our class step has to be wider than that feature stack or Dolby Vision would
-- let a PSA micro replace a FLUX WEB, and a -10000 penalty would not clear a
-- tier base that sits above 10000. The penalty below is -100000: the release
-- misses the cutoff, which is the same grab decision Dumpstarr gets from -10000.
--
-- Not copied:
--   Movies Anywhere stays +15. There is no +2000 MA bonus.
--   hallowed, BHDStudio and the rest of HEVC Compact Elite share one score.
--     There is no hallowed +600 / BHDStudio +550 / Baseline +500 split.
--   Dolby Vision WEB-DL is not banned. FLUX, Kitsune, CMRG and an in-cap HONE
--     WEB are DV releases this ladder still wants. A 230 MB/min DV WEB misses
--     the 200 MB/min cap instead.
--   The Elite, Circle, Small, Micro OK, streaming WEB and untouched WEB-DL
--     regexes are not edited. edge2020 stays in Circle. HONE stays in Elite.
-- TV scores are not restacked. The shared regexes are unchanged, so the TV
-- disc-vs-WEB order stays where ops/971 left it.

INSERT INTO custom_formats (name, description) VALUES (
  '2160p SDR Bluray',
  '4K Blu-ray with no HDR, HDR10, HDR10+ or Dolby Vision in the name. Same idea as Dumpstarr SDR (no WEBDL): a disc encode needs an HDR fallback, and a WEB-DL is left alone so compact streaming WEB and untouched WEB can still fill a gap.'
) ON CONFLICT (name) DO UPDATE SET description = excluded.description;

INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES
  ('2160p SDR Bluray', 'HDR')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p SDR Bluray', 'Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('2160p SDR Bluray', 'Resolution', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p SDR Bluray', 'Bluray', 'source', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p SDR Bluray', 'Bluray', 'bluray')
ON CONFLICT DO NOTHING;
-- The shared HDR regex already covers HDR, HDR10, HDR10+, HLG and PQ.
-- The old standalone HDR10 regex was removed in ops/127.
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p SDR Bluray', 'Not HDR', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p SDR Bluray', 'Not HDR', 'HDR')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p SDR Bluray', 'Not Dolby Vision', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p SDR Bluray', 'Not Dolby Vision', 'Dolby Vision')
ON CONFLICT DO NOTHING;

-- 3200-point class step. The positive feature stack (Dolby Vision, both HDR
-- formats, DD+, Atmos, IMAX, storefronts, repacks) has to fit inside it.
--   38400 Blu-ray tier 1   one score for the whole elite list
--   35200 Blu-ray tier 2   QxR, TAoE, edge2020
--   32000 WEB tier 1       elite groups on WEB, including an in-cap HONE MA
--   28800 streaming WEB    FLUX, Kitsune, CMRG, CMaRG, CMRioG
--   28800 WEB tier 2       circle groups on WEB
--   25600 Blu-ray tier 3   PSA, PSARips, d3g and the rest of the small list
--   22400 Blu-ray tier 4
--   19200 WEB tier 3       small groups on WEB, still above untouched WEB
--   16000 WEB tier 4
--   12800 untouched WEB    BYNDR, NTb
--    9600 1080 tier 1
--    6400 1080 tier 2
--    3200 1080 tiers 3 and 4
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 1', 'all', 38400),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 2', 'all', 35200),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 32000),
  ('Movies 2160p HEVC Compact', '2160p Compact Streaming WEB-DL', 'all', 28800),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 28800),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 3', 'all', 25600),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 4', 'all', 22400),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 3', 'all', 19200),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 4', 'all', 16000),
  ('Movies 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 12800),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 1', 'all', 9600),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 2', 'all', 6400),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 3', 'all', 3200),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 4', 'all', 3200),
  ('Movies 2160p HEVC Compact', 'Dolby Vision', 'all', 1000),
  ('Movies 2160p HEVC Compact', 'HDR', 'all', 500),
  ('Movies 2160p HEVC Compact', 'HDR10+', 'all', 500),
  ('Movies 2160p HEVC Compact', 'Dolby Digital +', 'all', 125),
  ('Movies 2160p HEVC Compact', 'TrueHD', 'all', -100000),
  ('Movies 2160p HEVC Compact', 'DTS-HD MA', 'all', -100000),
  ('Movies 2160p HEVC Compact', 'DTS-HD HRA', 'all', -100000),
  ('Movies 2160p HEVC Compact', 'DTS-X', 'all', -100000),
  ('Movies 2160p HEVC Compact', '2160p SDR Bluray', 'all', -100000),
  ('Movies 2160p HEVC Compact', 'MA', 'all', 15)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET minimum_custom_format_score = 3000,
    upgrade_until_score = 41600,
    description = 'Compact 4K for a 55-inch Mini LED, a 32-inch 4K monitor, and a phone. Preferred Blu-ray encodes share one score (the whole elite list: hallowed, BHDStudio, HONE, DarQ, DiscoD, dkore, HQMUX, PTer, Chivaman, Weasley, Vyndros and the rest). Then a smaller disc (QxR, TAoE, edge2020), then compact streaming WEB (FLUX, Kitsune, CMRG), then PSA and the other micros, then BYNDR or NTb. Dolby Vision +1000, HDR and HDR10+ +500, Dolby Digital + +125, inside the class gap. 4K Blu-ray without HDR is rejected. TrueHD, DTS-HD MA, DTS-HD HRA and DTS-X are rejected for direct play. Cap 200 MB/min. Movies Anywhere is a tie-break. YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

-- Bitrate, not gigabytes. Return of the King hallowed at 179 MB/min stays in.
-- The old 30 GiB WEB penalty stays gone. Sonarr's 2160p cap is left as ops/971
-- set it; this migration does not retune TV.
UPDATE radarr_quality_definitions
SET min_size = 6, preferred_size = 130, max_size = 200
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Elite regex untouched', (SELECT pattern = '(?i)(?:^\[(?:TimeDistortion|bluegreeen|Chivaman|hallowed|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|HQMUX|YELLO|DarQ|HONE|PTer|BHDStudio)\]|(?:^|[-.\s(\[])(?:TimeDistortion|bluegreeen|Chivaman|hallowed|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|HQMUX|YELLO|DarQ|HONE|PTer|BHDStudio)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('Circle regex untouched', (SELECT pattern = '(?i)(?:^\[(?:edge2020|FreetheFish|Nostradamus|DrainedDay|Species180|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|KeepFRDS|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|HeVK|LION|MNHD|NAN0|Prof|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)\]|(?:^|[-.\s(\[])(?:edge2020|FreetheFish|Nostradamus|DrainedDay|Species180|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|KeepFRDS|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|HeVK|LION|MNHD|NAN0|Prof|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('Small regex untouched', (SELECT pattern = '(?i)(?:^\[(?:D0ct0rLew|DEFLATE|IAMABLE|POOTLED|PSARips|PSYPHER|ReELiTE|kronox|LEGi0N|yawnix|ELiTE|HiQVE|HODL|Kira|d3g|PSA|SEV|SIQ)\]|(?:^|[-.\s(\[])(?:D0ct0rLew|DEFLATE|IAMABLE|POOTLED|PSARips|PSYPHER|ReELiTE|kronox|LEGi0N|yawnix|ELiTE|HiQVE|HODL|Kira|d3g|PSA|SEV|SIQ)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)' FROM regular_expressions WHERE name = 'HEVC Compact Small')),
  ('Micro OK regex untouched', (SELECT pattern = '(?i)(?:^\[(?:UTRcorp|RARBG|t0paz|iVy|Joy|POF|UTR)\]|(?:^|[-.\s(\[])(?:UTRcorp|RARBG|t0paz|iVy|Joy|POF|UTR)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)' FROM regular_expressions WHERE name = 'HEVC Compact Micro OK')),
  ('Streaming WEB regex untouched', (SELECT pattern = '(?i)(?:^\[(?:FLUX|Kitsune|CMRG|CMaRG|CMRioG)\]|(?:^|[-.\s(\[])(?:FLUX|Kitsune|CMRG|CMaRG|CMRioG)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)' FROM regular_expressions WHERE name = 'HEVC Compact Streaming WEB')),
  ('Untouched WEB-DL regex untouched', (SELECT pattern = '(?i)(?:^\[(?:BLUTONiUM|DUSKLiGHT|NOSiViD|playWEB|4KBEC|ABBIE|AJP69|BYNDR|CEBEX|HHWEB|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|RAWR|NTb|SiC)\]|(?:^|[-.\s(\[])(?:BLUTONiUM|DUSKLiGHT|NOSiViD|playWEB|4KBEC|ABBIE|AJP69|BYNDR|CEBEX|HHWEB|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|RAWR|NTb|SiC)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)' FROM regular_expressions WHERE name = 'HEVC Compact WEB-DL')),
  ('HONE stays elite', (SELECT pattern LIKE '%HONE%' AND pattern LIKE '%BHDStudio%' AND pattern LIKE '%hallowed%' AND pattern NOT LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('No HONE bad-name format', (SELECT COUNT(*) = 0 FROM custom_formats WHERE name LIKE '%Bad Name%' OR name LIKE '%HONE (Bad%')),
  ('YTS stays banned', (SELECT pattern LIKE '%YTS%' AND pattern LIKE '%MeGusta%' FROM regular_expressions WHERE name = 'HEVC Compact Micro Ban')),
  ('Dolby Vision is +1000', (SELECT score = 1000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Vision')),
  ('HDR and HDR10+ are +500', (SELECT COUNT(*) = 2 AND MIN(score) = 500 AND MAX(score) = 500 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('HDR', 'HDR10+'))),
  ('DD+ is +125', (SELECT score = 125 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Digital +')),
  ('HD audio is a hard miss', (SELECT COUNT(*) = 4 AND MIN(score) = -100000 AND MAX(score) = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('TrueHD', 'DTS-HD MA', 'DTS-HD HRA', 'DTS-X'))),
  ('SDR bluray is a hard miss', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p SDR Bluray')),
  ('Movies Anywhere stays a tie-break', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA')),
  ('Preferred disc leads streaming', (SELECT d.score > s.score FROM quality_profile_custom_formats d JOIN quality_profile_custom_formats s ON s.quality_profile_name = d.quality_profile_name WHERE d.quality_profile_name = 'Movies 2160p HEVC Compact' AND d.custom_format_name = '2160p Compact Bluray Tier 1' AND s.custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('Streaming leads PSA', (SELECT s.score > p.score FROM quality_profile_custom_formats s JOIN quality_profile_custom_formats p ON p.quality_profile_name = s.quality_profile_name WHERE s.quality_profile_name = 'Movies 2160p HEVC Compact' AND s.custom_format_name = '2160p Compact Streaming WEB-DL' AND p.custom_format_name = '2160p Compact Bluray Tier 3')),
  ('PSA leads untouched WEB', (SELECT p.score > w.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats w ON w.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '2160p Compact Bluray Tier 3' AND w.custom_format_name = '2160p WEB-DL HEVC')),
  ('PSA WEB leads untouched WEB', (SELECT p.score > w.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats w ON w.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '2160p Compact WEB Tier 3' AND w.custom_format_name = '2160p WEB-DL HEVC')),
  ('Class gap beats the feature stack', (SELECT (a.score - b.score) > feats.total FROM quality_profile_custom_formats a JOIN quality_profile_custom_formats b ON b.quality_profile_name = a.quality_profile_name AND b.custom_format_name = '2160p Compact Bluray Tier 2' JOIN (SELECT COALESCE(SUM(score), 0) AS total FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND score > 0 AND score < 3000) feats WHERE a.quality_profile_name = 'Movies 2160p HEVC Compact' AND a.custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Cutoff beats an unvetted feature stack', (SELECT minimum_custom_format_score > (SELECT COALESCE(SUM(score), 0) FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND score > 0 AND score < 3000) FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('No gigabyte WEB penalty', (SELECT COUNT(*) = 0 FROM custom_formats WHERE name = '2160p Bloated WEB')),
  ('4K cap is 6 / 130 / 200', (SELECT COUNT(*) = 4 AND MIN(min_size) = 6 AND MAX(min_size) = 6 AND MIN(preferred_size) = 130 AND MAX(preferred_size) = 130 AND MIN(max_size) = 200 AND MAX(max_size) = 200 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p'))),
  ('TV top WEB tier unchanged', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('TV disc stays under TV WEB', (SELECT w.score > d.score FROM quality_profile_custom_formats w JOIN quality_profile_custom_formats d ON d.quality_profile_name = w.quality_profile_name WHERE w.quality_profile_name = 'TV 2160p HEVC Compact' AND w.custom_format_name = '2160p Compact WEB Tier 1' AND d.custom_format_name = '2160p Compact Bluray Tier 1')),
  ('TV TrueHD is not banned', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'TrueHD')),
  ('TV does not score the SDR bluray ban', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p SDR Bluray'));
DROP TABLE _pcd_assertions;

COMMIT;
