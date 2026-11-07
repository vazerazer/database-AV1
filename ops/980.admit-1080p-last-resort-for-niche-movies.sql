-- @description: Score unrecognized 1080p HEVC and any 1080p AVC at 3000 so niche movies clear the minimum
-- @author: cursor
-- @name: 980.admit-1080p-last-resort-for-niche-movies

BEGIN TRANSACTION;

-- Sixteen released movies had a usable 1080p candidate whose only rejection
-- was a custom-format score under the movie minimum of 3000. Nine were
-- 1080p HEVC from groups outside the compact ladder (scores 10-155 from
-- extras alone). Seven were 1080p AVC and have no usable HEVC, so adding
-- those groups to 1080p Compact HEVC Tier 4 would not match them.
--
-- Two formats, both +3000 on Movies 2160p HEVC Compact only. That is the
-- same band as 1080p Compact HEVC Tier 4. T1 9600, T2 6400, streaming
-- 5200, and T3 4100 stay where they are.
--
-- A single format cannot say "(HEVC and not already tiered) or (any AVC)".
-- Required conditions are a conjunction, and each pattern condition holds
-- one regex. The HEVC format therefore negates the five group regexes the
-- 1080p tiers already use (elite, circle, small, micro, streaming). A
-- release that qualifies for one of those formats fails a required
-- negation here, so +3000 does not stack on 9600, 6400, 5200, 4100, or
-- 3000. The AVC format does not list groups. It negates HEVC, so a name
-- that contains both codecs takes the HEVC format only.
--
-- Resolution is the parsed 1080p quality, the same guard the other 1080p
-- formats use, so a 2160p release does not match. Source is Blu-ray,
-- WEB-DL, or WEBRip. Remux, AV1, and an explicit foreign-dub tag are
-- negated. 4K micros and untouched 4K WEB-DL stay at 0. minFormatScore
-- stays 3000, because rejected 4K releases in this set still carry extras
-- up to about 1780.

INSERT INTO custom_formats (name, description) VALUES
  (
    '1080p Compact HEVC Last Resort',
    '1080p HEVC Blu-ray, WEB-DL, or WEBRip from a group that is not already on the 1080p compact ladder. Same 3000 band as 1080p Tier 4. Does not match 2160p, remux, AV1, a foreign dub, or a release that already matches 1080p Tier 1-4 or 1080p streaming.'
  ),
  (
    '1080p Compact AVC Last Resort',
    '1080p AVC Blu-ray, WEB-DL, or WEBRip from any group, for a niche movie that has no HEVC release. Same 3000 band as 1080p Tier 4. Does not match 2160p, remux, HEVC, AV1, or a foreign dub.'
  )
ON CONFLICT (name) DO UPDATE SET description = excluded.description;

INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES
  ('1080p Compact HEVC Last Resort', '1080p'),
  ('1080p Compact HEVC Last Resort', 'HEVC'),
  ('1080p Compact AVC Last Resort', '1080p'),
  ('1080p Compact AVC Last Resort', 'Codec')
ON CONFLICT DO NOTHING;

-- HEVC last resort. Group negations reference the live tier regexes, so a
-- later edit to those lists stays excluded here too.
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact HEVC Last Resort', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p Compact HEVC Last Resort', 'HEVC', 'release_title', 'all', 0, 1),
  ('1080p Compact HEVC Last Resort', 'Not AV1', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Foreign Dub', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Elite', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Circle', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Small', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Micro', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Not Streaming', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Last Resort', 'Bluray', 'source', 'all', 0, 0),
  ('1080p Compact HEVC Last Resort', 'WEB-DL', 'source', 'all', 0, 0),
  ('1080p Compact HEVC Last Resort', 'WEBRip', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('1080p Compact HEVC Last Resort', 'Resolution', '1080p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p Compact HEVC Last Resort', 'HEVC', 'HEVC'),
  ('1080p Compact HEVC Last Resort', 'Not AV1', 'AV1'),
  ('1080p Compact HEVC Last Resort', 'Not Remux', 'Remux'),
  ('1080p Compact HEVC Last Resort', 'Not Foreign Dub', 'Foreign Dub'),
  ('1080p Compact HEVC Last Resort', 'Not Elite', 'HEVC Compact Elite'),
  ('1080p Compact HEVC Last Resort', 'Not Circle', 'HEVC Compact Circle'),
  ('1080p Compact HEVC Last Resort', 'Not Small', 'HEVC Compact Small'),
  ('1080p Compact HEVC Last Resort', 'Not Micro', 'HEVC Compact Micro OK'),
  ('1080p Compact HEVC Last Resort', 'Not Streaming', 'HEVC Compact Streaming WEB')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p Compact HEVC Last Resort', 'Bluray', 'bluray'),
  ('1080p Compact HEVC Last Resort', 'WEB-DL', 'web_dl'),
  ('1080p Compact HEVC Last Resort', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;

-- AVC last resort. Any group. HEVC is negated so the two formats cannot stack.
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('1080p Compact AVC Last Resort', 'Resolution', 'resolution', 'all', 0, 1),
  ('1080p Compact AVC Last Resort', 'AVC', 'release_title', 'all', 0, 1),
  ('1080p Compact AVC Last Resort', 'Not HEVC', 'release_title', 'all', 1, 1),
  ('1080p Compact AVC Last Resort', 'Not AV1', 'release_title', 'all', 1, 1),
  ('1080p Compact AVC Last Resort', 'Not Remux', 'release_title', 'all', 1, 1),
  ('1080p Compact AVC Last Resort', 'Not Foreign Dub', 'release_title', 'all', 1, 1),
  ('1080p Compact AVC Last Resort', 'Bluray', 'source', 'all', 0, 0),
  ('1080p Compact AVC Last Resort', 'WEB-DL', 'source', 'all', 0, 0),
  ('1080p Compact AVC Last Resort', 'WEBRip', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('1080p Compact AVC Last Resort', 'Resolution', '1080p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('1080p Compact AVC Last Resort', 'AVC', 'AVC'),
  ('1080p Compact AVC Last Resort', 'Not HEVC', 'HEVC'),
  ('1080p Compact AVC Last Resort', 'Not AV1', 'AV1'),
  ('1080p Compact AVC Last Resort', 'Not Remux', 'Remux'),
  ('1080p Compact AVC Last Resort', 'Not Foreign Dub', 'Foreign Dub')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('1080p Compact AVC Last Resort', 'Bluray', 'bluray'),
  ('1080p Compact AVC Last Resort', 'WEB-DL', 'web_dl'),
  ('1080p Compact AVC Last Resort', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '1080p Compact HEVC Last Resort', 'all', 3000),
  ('Movies 2160p HEVC Compact', '1080p Compact AVC Last Resort', 'all', 3000)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = REPLACE(
  description,
  'so the search continues at 1080p: elite HEVC, then the smaller circle, then FLUX/Kitsune/CMRG, then PSA, then a micro.',
  'so the search continues at 1080p: elite HEVC, then the smaller circle, then FLUX/Kitsune/CMRG, then PSA, then a micro. A 1080p HEVC Blu-ray, WEB-DL, or WEBRip from a group outside that ladder scores 3000, and so does a 1080p AVC Blu-ray, WEB-DL, or WEBRip. Those two share the micro band and do not add to a tier that already matched.'
)
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('HEVC last resort exists', (SELECT COUNT(*) = 1 FROM custom_formats WHERE name = '1080p Compact HEVC Last Resort')),
  ('AVC last resort exists', (SELECT COUNT(*) = 1 FROM custom_formats WHERE name = '1080p Compact AVC Last Resort')),
  ('Movie HEVC last resort is 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Last Resort')),
  ('Movie AVC last resort is 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact AVC Last Resort')),
  ('TV does not score either last resort', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort'))),
  ('No other profile scores either last resort', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name != 'Movies 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort'))),
  ('1080p ladder stays 9600 / 6400 / 5200 / 4100 / 3000', (SELECT COUNT(*) = 5 AND SUM(CASE custom_format_name WHEN '1080p Compact HEVC Tier 1' THEN score WHEN '1080p Compact HEVC Tier 2' THEN score WHEN '1080p Compact Streaming WEB-DL' THEN score WHEN '1080p Compact HEVC Tier 3' THEN score WHEN '1080p Compact HEVC Tier 4' THEN score END) = 9600 + 6400 + 5200 + 4100 + 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Tier 1', '1080p Compact HEVC Tier 2', '1080p Compact Streaming WEB-DL', '1080p Compact HEVC Tier 3', '1080p Compact HEVC Tier 4'))),
  ('4K class scores stay put', (SELECT COUNT(*) = 9 AND SUM(score) = 38400 + 35200 + 32000 + 28800 + 28800 + 25600 + 19200 + 0 + 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('2160p Compact Bluray Tier 1', '2160p Compact Bluray Tier 2', '2160p Compact WEB Tier 1', '2160p Compact Streaming WEB-DL', '2160p Compact WEB Tier 2', '2160p Compact Bluray Tier 3', '2160p Compact WEB Tier 3', '2160p Compact Bluray Tier 4', '2160p Compact WEB Tier 4'))),
  ('Untouched 4K WEB-DL stays 0', (SELECT score = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p WEB-DL HEVC')),
  ('Movie minimum and cutoff stay 3000 / 41600', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('Extras still cannot lift a zero 4K class over the minimum', (SELECT minimum_custom_format_score > (SELECT COALESCE(SUM(score), 0) FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND score > 0 AND score < 3000) FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('Last resort resolutions are 1080p only', (SELECT COUNT(*) = 2 AND SUM(resolution = '1080p') = 2 FROM condition_resolutions WHERE custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort'))),
  ('Neither last resort lists 2160p or 720p', (SELECT COUNT(*) = 0 FROM condition_resolutions WHERE custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort') AND resolution IN ('2160p', '720p'))),
  ('HEVC last resort requires HEVC and negates AV1, remux, and foreign dub', (SELECT COUNT(*) = 4 FROM custom_format_conditions c JOIN condition_patterns p ON p.custom_format_name = c.custom_format_name AND p.condition_name = c.name WHERE c.custom_format_name = '1080p Compact HEVC Last Resort' AND ((c.name = 'HEVC' AND c.negate = 0 AND c.required = 1 AND p.regular_expression_name = 'HEVC') OR (c.name = 'Not AV1' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name = 'AV1') OR (c.name = 'Not Remux' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name = 'Remux') OR (c.name = 'Not Foreign Dub' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name = 'Foreign Dub')))),
  ('HEVC last resort excludes all five 1080p group lists', (SELECT COUNT(*) = 5 FROM custom_format_conditions c JOIN condition_patterns p ON p.custom_format_name = c.custom_format_name AND p.condition_name = c.name WHERE c.custom_format_name = '1080p Compact HEVC Last Resort' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name IN ('HEVC Compact Elite', 'HEVC Compact Circle', 'HEVC Compact Small', 'HEVC Compact Micro OK', 'HEVC Compact Streaming WEB'))),
  ('AVC last resort is generic AVC and not HEVC', (SELECT COUNT(*) = 2 FROM custom_format_conditions c JOIN condition_patterns p ON p.custom_format_name = c.custom_format_name AND p.condition_name = c.name WHERE c.custom_format_name = '1080p Compact AVC Last Resort' AND ((c.name = 'AVC' AND c.negate = 0 AND c.required = 1 AND p.regular_expression_name = 'AVC') OR (c.name = 'Not HEVC' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name = 'HEVC')))),
  ('AVC last resort does not list compact groups', (SELECT COUNT(*) = 0 FROM condition_patterns WHERE custom_format_name = '1080p Compact AVC Last Resort' AND regular_expression_name LIKE 'HEVC Compact%')),
  ('AVC last resort negates remux, AV1, and foreign dub', (SELECT COUNT(*) = 3 FROM custom_format_conditions c JOIN condition_patterns p ON p.custom_format_name = c.custom_format_name AND p.condition_name = c.name WHERE c.custom_format_name = '1080p Compact AVC Last Resort' AND c.negate = 1 AND c.required = 1 AND p.regular_expression_name IN ('Remux', 'AV1', 'Foreign Dub'))),
  ('Both last resorts allow bluray, web_dl, and webrip', (SELECT COUNT(*) = 6 AND SUM(source = 'bluray') = 2 AND SUM(source = 'web_dl') = 2 AND SUM(source = 'webrip') = 2 FROM condition_sources WHERE custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort'))),
  ('Neither last resort allows HDTV', (SELECT COUNT(*) = 0 FROM condition_sources WHERE custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort') AND source = 'hdtv')),
  ('Source guards are optional', (SELECT COUNT(*) = 6 AND SUM(required) = 0 FROM custom_format_conditions WHERE custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort') AND type = 'source')),
  ('720p stays off the movie profile', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND quality_name LIKE '%720p%')),
  ('Profile text names the 1080p last resort', (SELECT description LIKE '%1080p HEVC Blu-ray, WEB-DL, or WEBRip from a group outside that ladder scores 3000%' FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact'));
DROP TABLE _pcd_assertions;

COMMIT;
