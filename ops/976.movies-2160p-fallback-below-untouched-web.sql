-- @description: Stop Movies 2160p HEVC Compact from grabbing an untouched 4K WEB-DL, and repeat the compact ladder at 1080p
-- @author: cursor
-- @name: 976.movies-2160p-fallback-below-untouched-web

BEGIN TRANSACTION;

-- Untouched 4K WEB-DL (BYNDR, NTb, XEBEC, HHWEB and the rest of HEVC Compact
-- WEB-DL) was 12800, above min 3000. Radarr then kept that 2160p file, so a
-- later 1080p Ralphy or DarQ encode could not replace it. Score 0 leaves the
-- format on the profile, which overwrites the old 12800 on sync, and the
-- positive extras on this profile sum to less than 3000, so a tagged BYNDR
-- still misses the minimum. Radarr continues to the 1080p Fallback group.
-- A 4K file that is already imported is not replaced by 1080p: Radarr does
-- not downgrade a quality group.
--
-- 4K class scores are unchanged:
--   38400 Blu-ray tier 1   the whole elite list
--   35200 Blu-ray tier 2   QxR, TAoE, edge2020 and the rest of the circle
--   32000 WEB tier 1       elite WEB, including an in-cap HONE WEB
--   28800 streaming / WEB tier 2
--   25600 Blu-ray tier 3   PSA
--   22400 Blu-ray tier 4   micros
--   19200 WEB tier 3
--   16000 WEB tier 4
--   0     untouched WEB-DL
--
-- 1080p repeats that ladder under the lowest accepted 4K class. Tier 1 and
-- tier 2 stay 9600 and 6400. The new streaming step is 5200, PSA is 4100,
-- and the micro is 3000. Each of those three steps is more than Dolby
-- Vision's +1000, and 9600 plus every positive extra on this profile still
-- sits under a bare 4K micro at 16000. Group lists are not edited.

UPDATE custom_formats
SET description = 'Untouched 4K HEVC WEB-DL groups that run large (BYNDR, NTb, XEBEC, HHWEB and peers). Scored 0 on Movies 2160p HEVC Compact, so they do not clear the minimum and Radarr falls through to 1080p. TV still scores this format.'
WHERE name = '2160p WEB-DL HEVC';

INSERT INTO custom_formats (name, description) VALUES (
  '1080p Compact Streaming WEB-DL',
  '1080p HEVC WEB-DL from FLUX, Kitsune and CMRG. Below a 1080p compact encode, above a 1080p PSA. Requires 1080p, so it cannot take the 4K streaming score.'
) ON CONFLICT (name) DO UPDATE SET description = excluded.description;

INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES
  ('1080p Compact Streaming WEB-DL', 'Release Group'),
  ('1080p Compact Streaming WEB-DL', 'HEVC')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('1080p Compact Streaming WEB-DL', 'Resolution', '1080p')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'HEVC', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p Compact Streaming WEB-DL', 'HEVC', 'HEVC')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'Not AV1', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p Compact Streaming WEB-DL', 'Not AV1', 'AV1')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'Not Remux', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p Compact Streaming WEB-DL', 'Not Remux', 'Remux')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'Groups', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p Compact Streaming WEB-DL', 'Groups', 'HEVC Compact Streaming WEB')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'Not Bluray', 'source', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p Compact Streaming WEB-DL', 'Not Bluray', 'bluray')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'WEB-DL', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p Compact Streaming WEB-DL', 'WEB-DL', 'web_dl')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact Streaming WEB-DL', 'WEBRip', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p Compact Streaming WEB-DL', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 0),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 1', 'all', 9600),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 2', 'all', 6400),
  ('Movies 2160p HEVC Compact', '1080p Compact Streaming WEB-DL', 'all', 5200),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 3', 'all', 4100),
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Tier 4', 'all', 3000)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = 'Compact 4K for a 55-inch Mini LED, a 32-inch 4K monitor, and a phone. Preferred Blu-ray encodes share one score (the whole elite list: hallowed, BHDStudio, HONE, DarQ, DiscoD, dkore, HQMUX, PTer, Chivaman, Weasley, Vyndros, Ralphy and the rest), then a smaller disc (QxR, TAoE, edge2020). An in-cap elite WEB such as HONE stays above compact streaming WEB (FLUX, Kitsune, CMRG). Then PSA, then UTR, RARBG and iVy. Untouched 4K WEB-DL (BYNDR, NTb, XEBEC, HHWEB) scores 0 and does not clear the minimum, so the search continues at 1080p: elite HEVC, then the smaller circle, then FLUX/Kitsune/CMRG, then PSA, then a micro. A 4K file already imported is not replaced by 1080p. Inside a class, Dolby Vision is +1000, HDR is +500, and HDR10+ is +600. Dolby Digital + is +125, Dolby Digital is +115, Atmos is +25, and AAC is +10. Special Edition is +125. Storefronts stay at or below +15: Movies Anywhere, then Disney+ and iTunes, then Apple TV+, Max, and HBO Max, then Amazon, Netflix, ATV, and Hulu. 4K Blu-ray without HDR is rejected. Dolby Vision without an HDR fallback is rejected. TrueHD, DTS-HD MA, DTS-HD HRA, and DTS-X are rejected for direct play. Lossy DTS is allowed and not preferred. Cap 200 MB/min. YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Elite disc stays 38400', (SELECT score = 38400 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Circle disc stays 35200', (SELECT score = 35200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 2')),
  ('Elite WEB stays 32000', (SELECT score = 32000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('Streaming WEB stays 28800', (SELECT score = 28800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('Circle WEB stays 28800', (SELECT score = 28800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 2')),
  ('PSA disc stays 25600', (SELECT score = 25600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 3')),
  ('Micro disc stays 22400', (SELECT score = 22400 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 4')),
  ('PSA WEB stays 19200', (SELECT score = 19200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 3')),
  ('Micro WEB stays 16000', (SELECT score = 16000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 4')),
  ('Untouched WEB-DL scores 0', (SELECT score = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p WEB-DL HEVC')),
  ('Extras cannot lift a zero class over the minimum', (SELECT minimum_custom_format_score > (SELECT COALESCE(SUM(score), 0) FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND score > 0 AND score < 3000) FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('1080p elite stays 9600', (SELECT score = 9600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 1')),
  ('1080p circle stays 6400', (SELECT score = 6400 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 2')),
  ('1080p streaming is 5200', (SELECT score = 5200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact Streaming WEB-DL')),
  ('1080p PSA is 4100', (SELECT score = 4100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 3')),
  ('1080p micro is 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 4')),
  ('1080p streaming beats PSA', (SELECT s.score > p.score FROM quality_profile_custom_formats s JOIN quality_profile_custom_formats p ON p.quality_profile_name = s.quality_profile_name WHERE s.quality_profile_name = 'Movies 2160p HEVC Compact' AND s.custom_format_name = '1080p Compact Streaming WEB-DL' AND p.custom_format_name = '1080p Compact HEVC Tier 3')),
  ('1080p PSA beats the micro', (SELECT p.score > m.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats m ON m.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '1080p Compact HEVC Tier 3' AND m.custom_format_name = '1080p Compact HEVC Tier 4')),
  ('1080p circle beats streaming', (SELECT c.score > s.score FROM quality_profile_custom_formats c JOIN quality_profile_custom_formats s ON s.quality_profile_name = c.quality_profile_name WHERE c.quality_profile_name = 'Movies 2160p HEVC Compact' AND c.custom_format_name = '1080p Compact HEVC Tier 2' AND s.custom_format_name = '1080p Compact Streaming WEB-DL')),
  ('1080p steps are wider than Dolby Vision', (SELECT (a.score - b.score) > dv.score AND (b.score - c.score) > dv.score AND (c.score - d.score) > dv.score FROM quality_profile_custom_formats a JOIN quality_profile_custom_formats b ON b.quality_profile_name = a.quality_profile_name JOIN quality_profile_custom_formats c ON c.quality_profile_name = a.quality_profile_name JOIN quality_profile_custom_formats d ON d.quality_profile_name = a.quality_profile_name JOIN quality_profile_custom_formats dv ON dv.quality_profile_name = a.quality_profile_name WHERE a.quality_profile_name = 'Movies 2160p HEVC Compact' AND a.custom_format_name = '1080p Compact HEVC Tier 2' AND b.custom_format_name = '1080p Compact Streaming WEB-DL' AND c.custom_format_name = '1080p Compact HEVC Tier 3' AND d.custom_format_name = '1080p Compact HEVC Tier 4' AND dv.custom_format_name = 'Dolby Vision')),
  ('4K streaming format is 2160p only', (SELECT COUNT(*) = 1 FROM condition_resolutions WHERE custom_format_name = '2160p Compact Streaming WEB-DL' AND resolution = '2160p')),
  ('1080p streaming format is 1080p only', (SELECT COUNT(*) = 1 FROM condition_resolutions WHERE custom_format_name = '1080p Compact Streaming WEB-DL' AND resolution = '1080p')),
  ('Profile gates stay 3000 / 41600', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('Movie qualities stay 2160p and 1080p', (SELECT COUNT(*) = 2 AND SUM(enabled) = 2 FROM quality_profile_qualities WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND enabled = 1 AND quality_group_name IN ('2160p', '1080p Fallback'))),
  ('No other movie quality is enabled', (SELECT COUNT(*) = 0 FROM quality_profile_qualities WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND enabled = 1 AND quality_group_name NOT IN ('2160p', '1080p Fallback'))),
  ('Elite regex still has the mid-size list', (SELECT pattern LIKE '%Ralphy%' AND pattern LIKE '%HONE%' AND pattern LIKE '%DarQ%' AND pattern LIKE '%DiscoD%' AND pattern LIKE '%Weasley%' AND pattern LIKE '%Vyndros%' AND pattern LIKE '%dkore%' AND pattern LIKE '%HQMUX%' AND pattern LIKE '%PTer%' AND pattern LIKE '%Chivaman%' AND pattern LIKE '%TimeDistortion%' AND pattern LIKE '%hallowed%' AND pattern LIKE '%BHDStudio%' AND pattern NOT LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('Circle regex still has QxR TAoE Tigole edge2020', (SELECT pattern LIKE '%QxR%' AND pattern LIKE '%TAoE%' AND pattern LIKE '%Tigole%' AND pattern LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('Streaming regex still has FLUX Kitsune CMRG', (SELECT pattern LIKE '%FLUX%' AND pattern LIKE '%Kitsune%' AND pattern LIKE '%CMRG%' FROM regular_expressions WHERE name = 'HEVC Compact Streaming WEB')),
  ('Untouched regex still has BYNDR NTb XEBEC HHWEB', (SELECT pattern LIKE '%BYNDR%' AND pattern LIKE '%NTb%' AND pattern LIKE '%XEBEC%' AND pattern LIKE '%HHWEB%' FROM regular_expressions WHERE name = 'HEVC Compact WEB-DL')),
  ('TV untouched WEB-DL stays 2500', (SELECT score = 2500 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p WEB-DL HEVC')),
  ('TV streaming stays 5300', (SELECT score = 5300 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('TV 1080p tiers stay put', (SELECT COUNT(*) = 4 AND MIN(score) = 400 AND MAX(score) = 1800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Tier 1', '1080p Compact HEVC Tier 2', '1080p Compact HEVC Tier 3', '1080p Compact HEVC Tier 4'))),
  ('TV does not score 1080p streaming', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '1080p Compact Streaming WEB-DL')),
  ('Dolby Vision stays +1000', (SELECT score = 1000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Vision')),
  ('Movies Anywhere stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA'));
DROP TABLE _pcd_assertions;

COMMIT;
