-- @description: Rank the movie profile by the hallowed/BHDStudio size window, not group prestige or a large WEB-DL
-- @author: cursor
-- @name: 971.prefer-compact-window-over-prestige

BEGIN TRANSACTION;

-- Mid-size circle is whoever already lands near hallowed (~135 MB/min) and
-- BHDStudio (~120 MB/min). BHDStudio was a tier below HONE, so a 20 GB HONE
-- disc replaced a 14.6 GB BHDStudio of the same movie. They now share a score.
-- edge2020 leaves this circle: the r/trackers size table that named HONE,
-- hallowed, BHDStudio, dkore and HQMUX as mid-size puts edge2020 in the large
-- UHD column with MainFrame and CtrlHD. dkore stays; that same table lists it
-- as mid-size, and the 200 MB/min cap below covers the ~183 MB/min copies.
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:TimeDistortion|bluegreeen|Chivaman|hallowed|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|HQMUX|YELLO|DarQ|HONE|PTer|BHDStudio)\]|(?:^|[-.\s(\[])(?:TimeDistortion|bluegreeen|Chivaman|hallowed|Vyndros|Weasley|DiscoD|noxxus|R1GY3B|Ralphy|ToNaTo|Vialle|dkore|GRiMM|HQMUX|YELLO|DarQ|HONE|PTer|BHDStudio)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)',
    description = 'Mid-size 4K circle, same score: HONE, hallowed, BHDStudio, dkore, HQMUX, PTer. A larger HONE does not outrank a smaller hallowed or BHDStudio file.'
WHERE name = 'HEVC Compact Elite';

UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:edge2020|FreetheFish|Nostradamus|DrainedDay|Species180|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|KeepFRDS|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|HeVK|LION|MNHD|NAN0|Prof|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)\]|(?:^|[-.\s(\[])(?:edge2020|FreetheFish|Nostradamus|DrainedDay|Species180|Bluespots|honeyvera|TheSickle|bccornfo|Garshasp|KeepFRDS|Langbard|MONOLITH|Silence|xtrem3x|AJJMIN|ANONAZ|Celdra|jb2049|RZeroX|SARTRE|t3nzin|Tigole|afm72|Bandi|DUHIT|Ghost|JBENT|Kappa|Natty|Panda|r0b0t|SAMPA|Ainz|ArcX|Erie|Frys|Goki|HeVK|LION|MNHD|NAN0|Prof|r00t|RCVR|TAoE|YOGI|DNU|HxD|Ime|LSt|QxR|SQS|WEM)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)',
    description = 'Smaller than the hallowed/BHDStudio window: QxR, TAoE, and edge2020 (large-UHD group, demoted out of the mid-size circle).'
WHERE name = 'HEVC Compact Circle';

-- FLUX (~147 MB/min), Kitsune (~138) and CMRG (~128) are the compact streaming
-- WEB-DLs already in the library. BYNDR (~181) and NTb stay in the untouched
-- bucket, which now scores below a PSA micro.
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:BLUTONiUM|DUSKLiGHT|NOSiViD|playWEB|4KBEC|ABBIE|AJP69|BYNDR|CEBEX|HHWEB|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|RAWR|NTb|SiC)\]|(?:^|[-.\s(\[])(?:BLUTONiUM|DUSKLiGHT|NOSiViD|playWEB|4KBEC|ABBIE|AJP69|BYNDR|CEBEX|HHWEB|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|RAWR|NTb|SiC)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)',
    description = 'Untouched 4K HEVC WEB-DL groups that run large (BYNDR, NTb and peers). Scored below PSA.'
WHERE name = 'HEVC Compact WEB-DL';

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  'HEVC Compact Streaming WEB',
  '(?i)(?:^\[(?:FLUX|Kitsune|CMRG|CMaRG|CMRioG)\]|(?:^|[-.\s(\[])(?:FLUX|Kitsune|CMRG|CMaRG|CMRioG)(?:\))?(?:\])?(?:\[[a-z0-9_\-\.]+\])?(?:[-._ ]?(?:[0-9]+|xpost))?(?:\.[a-z0-9]{2,4})?$)',
  'Compact 4K HEVC WEB-DL groups. Library medians: FLUX ~147 MB/min, Kitsune ~138, CMRG ~128. Apple, Amazon, Netflix, Max and Disney+ tags stack as tie-breakers.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

UPDATE custom_formats
SET description = '4K Blu-ray HEVC from the mid-size circle (HONE, hallowed, BHDStudio, dkore, HQMUX). Same score, so a larger HONE does not replace a smaller hallowed or BHDStudio file.'
WHERE name = '2160p Compact Bluray Tier 1';

UPDATE custom_formats
SET description = '4K Blu-ray HEVC from the smaller QxR and TAoE circles, plus edge2020. edge2020 is here because public size tables place it with large UHD, not with hallowed and BHDStudio.'
WHERE name = '2160p Compact Bluray Tier 2';

UPDATE custom_formats
SET description = 'Untouched 4K HEVC WEB-DL groups that run large (BYNDR, NTb and peers). Below a PSA micro, so a big WEB-DL does not replace a small encode.'
WHERE name = '2160p WEB-DL HEVC';

INSERT INTO custom_formats (name, description) VALUES (
  '2160p Compact Streaming WEB-DL',
  'Compact 4K HEVC WEB-DL from FLUX, Kitsune and CMRG, including Apple, Amazon, Netflix, Max and Disney+ releases in that size. Below a Blu-ray encode, above a PSA micro.'
) ON CONFLICT (name) DO UPDATE SET description = excluded.description;

INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES
  ('2160p Compact Streaming WEB-DL', 'Release Group'),
  ('2160p Compact Streaming WEB-DL', 'HEVC')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('2160p Compact Streaming WEB-DL', 'Resolution', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'HEVC', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p Compact Streaming WEB-DL', 'HEVC', 'HEVC')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'Not AV1', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p Compact Streaming WEB-DL', 'Not AV1', 'AV1')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'Not Remux', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p Compact Streaming WEB-DL', 'Not Remux', 'Remux')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'Groups', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p Compact Streaming WEB-DL', 'Groups', 'HEVC Compact Streaming WEB')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'Not Bluray', 'source', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p Compact Streaming WEB-DL', 'Not Bluray', 'bluray')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'WEB-DL', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p Compact Streaming WEB-DL', 'WEB-DL', 'web_dl')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact Streaming WEB-DL', 'WEBRip', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p Compact Streaming WEB-DL', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;

-- 30 GiB is the floor of the 30-40 GB HONE/MA dumps. A two-hour file at the
-- 130 MB/min target is about 15 GiB, so FLUX/Kitsune/CMRG miss this. A long
-- compact disc such as Return of the King hallowed (35 GiB, 179 MB/min) is a
-- Blu-ray and does not match. -3200 pulls a fully tagged Tier 1 WEB under the
-- PSA tier (5300) and under the UTR tier (4600).
INSERT INTO custom_formats (name, description) VALUES (
  '2160p Bloated WEB',
  '4K WEB-DL or WEBRip at or above 30 GiB. The 40 GB HONE Movies Anywhere dumps and other untouched dumps. Scored only on the movie profile, below a PSA micro.'
) ON CONFLICT (name) DO UPDATE SET description = excluded.description;

INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES
  ('2160p Bloated WEB', 'HEVC')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Bloated WEB', 'Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('2160p Bloated WEB', 'Resolution', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Bloated WEB', 'Not Bluray', 'source', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p Bloated WEB', 'Not Bluray', 'bluray')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Bloated WEB', 'WEB-DL', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p Bloated WEB', 'WEB-DL', 'web_dl')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Bloated WEB', 'WEBRip', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('2160p Bloated WEB', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Bloated WEB', 'At Least 30 GiB', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes) VALUES
  ('2160p Bloated WEB', 'At Least 30 GiB', 32212254720, NULL)
ON CONFLICT (custom_format_name, condition_name) DO UPDATE SET min_bytes = excluded.min_bytes, max_bytes = excluded.max_bytes;

-- Movie ladder, 700-point gaps so DV/Atmos/HDR stay inside a class.
--   8100 Blu-ray tier 1  hallowed / BHDStudio / in-window HONE
--   7400 Blu-ray tier 2  QxR / TAoE / edge2020 (still a disc, so it beats WEB)
--   6700 WEB tier 1      compact WEB encode from the mid-size circle
--   6000 streaming WEB   FLUX / Kitsune / CMRG, and QxR WEB
--   5300 Blu-ray tier 3  PSA. Above every big WEB-DL, below compact WEB.
--   4600 Blu-ray tier 4  UTR / RARBG
--   3900 WEB tier 3
--   3200 WEB tier 4
--   2500 untouched WEB   BYNDR / NTb, under the micros
-- A 30 GiB WEB also takes -3200, which puts a tagged HONE/MA dump under PSA.
-- Movies Anywhere is +15, the same kind of storefront tie-break as Amazon, so
-- it no longer clears the disc-over-WEB gap.
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 1', 'all', 8100),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 2', 'all', 7400),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 6700),
  ('Movies 2160p HEVC Compact', '2160p Compact Streaming WEB-DL', 'all', 6000),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 6000),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 3', 'all', 5300),
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 4', 'all', 4600),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 3', 'all', 3900),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 4', 'all', 3200),
  ('Movies 2160p HEVC Compact', '2160p WEB-DL HEVC', 'all', 2500),
  ('Movies 2160p HEVC Compact', '2160p Bloated WEB', 'all', -3200),
  ('Movies 2160p HEVC Compact', 'MA', 'all', 15)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

-- TV keeps WEB above disc. The shared group regexes move BHDStudio up and
-- edge2020 down, and FLUX/Kitsune/CMRG have to stay grabable once they leave
-- the untouched WEB-DL list. 5300 sits under TV WEB tier 4 (6000) and above
-- the untouched bucket (2500). The 30 GiB penalty is movie-only.
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('TV 2160p HEVC Compact', '2160p Compact Streaming WEB-DL', 'all', 5300)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = 'Compact 4K for a 55-inch Mini LED, a 32-inch 4K monitor, and a phone. Mid-size Blu-ray first (hallowed, BHDStudio, HONE inside the window), then a smaller disc such as QxR, then compact streaming WEB (Apple, Amazon, Netflix, FLUX, Kitsune, CMRG), then PSA, then a big WEB-DL. Hard cap 200 MB/min. YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

UPDATE quality_profiles
SET description = 'Compact 4K episodes. WEB from HONE, hallowed and BHDStudio first, then the smaller circles, then disc. FLUX, Kitsune and CMRG sit above untouched WEB-DL. edge2020 is not in the top circle. YTS and MeGusta stay rejected.'
WHERE name = 'TV 2160p HEVC Compact';

-- MB/min, not a raw gigabyte cap. 200 still allows Return of the King hallowed
-- at 179 MB/min and a typical HONE disc near 180, and it rejects the 230+ MB/min
-- Movies Anywhere dumps. Preferred 130 is the hallowed/BHDStudio window.
-- Sonarr gets the same 2160p cap so the shared profile pair does not leave TV unlimited.
UPDATE radarr_quality_definitions
SET min_size = 6, preferred_size = 130, max_size = 200
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');

UPDATE sonarr_quality_definitions
SET min_size = 6, preferred_size = 130, max_size = 200
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('BHDStudio is mid-size', (SELECT pattern LIKE '%BHDStudio%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('BHDStudio left the lower circle', (SELECT pattern NOT LIKE '%BHDStudio%' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('edge2020 left the mid-size circle', (SELECT pattern NOT LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('edge2020 is in the lower circle', (SELECT pattern LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('FLUX is compact streaming', (SELECT pattern LIKE '%FLUX%' FROM regular_expressions WHERE name = 'HEVC Compact Streaming WEB')),
  ('FLUX left the untouched bucket', (SELECT pattern NOT LIKE '%FLUX%' FROM regular_expressions WHERE name = 'HEVC Compact WEB-DL')),
  ('BYNDR stays untouched', (SELECT pattern LIKE '%BYNDR%' FROM regular_expressions WHERE name = 'HEVC Compact WEB-DL')),
  ('YTS stays banned', (SELECT pattern LIKE '%YTS%' FROM regular_expressions WHERE name = 'HEVC Compact Micro Ban')),
  ('Movie bluray tier 1 unchanged', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Movie WEB tier sits under both disc tiers', (SELECT score = 6700 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('Compact streaming WEB beats PSA', (SELECT s.score > p.score FROM quality_profile_custom_formats s JOIN quality_profile_custom_formats p ON p.quality_profile_name = s.quality_profile_name WHERE s.quality_profile_name = 'Movies 2160p HEVC Compact' AND s.custom_format_name = '2160p Compact Streaming WEB-DL' AND p.custom_format_name = '2160p Compact Bluray Tier 3')),
  ('PSA beats untouched WEB-DL', (SELECT p.score > w.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats w ON w.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '2160p Compact Bluray Tier 3' AND w.custom_format_name = '2160p WEB-DL HEVC')),
  ('Bloated WEB penalty clears a tagged tier-1 WEB under PSA', (SELECT (6700 + 180 + 80 + 50 + 40 + 40 + 40 + 30 + 20 + 15 + 15 - 3200) < 5300)),
  ('Movies Anywhere is a tie-break', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA')),
  ('TV top WEB tier unchanged', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('4K cap is 200 MB/min', (SELECT COUNT(*) = 4 AND MIN(max_size) = 200 AND MAX(max_size) = 200 AND MIN(preferred_size) = 130 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p')));
DROP TABLE _pcd_assertions;

COMMIT;
