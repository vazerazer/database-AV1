-- @description: Enable 720p under 1080p so a niche movie can be grabbed when nothing higher clears 3000
-- @author: cursor
-- @name: 981.enable-720p-last-resort-under-1080p

BEGIN TRANSACTION;

-- 1080p already sits under 2160p as its own quality group. Blu-ray, WEB-DL,
-- and WEBRip share that group, so they are one rank. 720p follows the same
-- shape as a third rank, under every 1080p quality. It is not a member of
-- the 1080p group. Custom format score is compared inside a rank. Both the
-- 1080p last resorts and this 720p format score 3000, and the positive
-- extras on this profile can add more than that gap. A shared group would
-- let a tagged 720p beat a bare 1080p. A lower rank cannot.
--
-- One format covers HEVC and AVC. There is no 720p group ladder to protect,
-- and a required condition cannot OR two codecs. The codec regex is the OR.
-- Resolution 720p, plus negated 1080p and 2160p, keeps it off the higher
-- names. Remux and the banned-micro list (YTS, MeGusta, and the rest of
-- HEVC Compact Micro Ban) are negated, so those releases stay rejected
-- instead of taking +3000 on top of the existing penalty. x265 (HD) is not
-- scored here. Dumpstarr's 720p T01-T06 lists are not copied.
--
-- TV is unchanged. 480p and HDTV-720p stay off. 720p size stays min 0,
-- preferred 1990, max 0. Max 0 does not reject the only file. Preferred
-- 1990 is the existing global row, not a new cap.

INSERT INTO regular_expressions (name, pattern, description) VALUES (
  '720p Last Resort Codec',
  '[xh][ ._-]?26[45]|\b(?:HEVC|AVC)(?:\b|\d)',
  'HEVC/x265 or AVC/x264/H.264. Used by the 720p last resort, which has no separate group ladder.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_formats (name, description) VALUES (
  '720p Compact Last Resort',
  '720p HEVC or AVC Blu-ray, WEB-DL, or WEBRip. Scored 3000 on Movies 2160p HEVC Compact only, in a quality group below every 1080p quality. Does not match 1080p, 2160p, remux, or a banned micro.'
) ON CONFLICT (name) DO UPDATE SET description = excluded.description;

INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES
  ('720p Compact Last Resort', '720p'),
  ('720p Compact Last Resort', 'Codec')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('720p Compact Last Resort', 'Resolution', 'resolution', 'all', 0, 1),
  ('720p Compact Last Resort', 'Not 1080p', 'resolution', 'all', 1, 1),
  ('720p Compact Last Resort', 'Not 2160p', 'resolution', 'all', 1, 1),
  ('720p Compact Last Resort', 'Codec', 'release_title', 'all', 0, 1),
  ('720p Compact Last Resort', 'Not Remux', 'release_title', 'all', 1, 1),
  ('720p Compact Last Resort', 'Not Banned Micro', 'release_title', 'all', 1, 1),
  ('720p Compact Last Resort', 'Not Foreign Dub', 'release_title', 'all', 1, 1),
  ('720p Compact Last Resort', 'Not AV1', 'release_title', 'all', 1, 1),
  ('720p Compact Last Resort', 'Bluray', 'source', 'all', 0, 0),
  ('720p Compact Last Resort', 'WEB-DL', 'source', 'all', 0, 0),
  ('720p Compact Last Resort', 'WEBRip', 'source', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES
  ('720p Compact Last Resort', 'Resolution', '720p'),
  ('720p Compact Last Resort', 'Not 1080p', '1080p'),
  ('720p Compact Last Resort', 'Not 2160p', '2160p')
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('720p Compact Last Resort', 'Codec', '720p Last Resort Codec'),
  ('720p Compact Last Resort', 'Not Remux', 'Remux'),
  ('720p Compact Last Resort', 'Not Banned Micro', 'HEVC Compact Micro Ban'),
  ('720p Compact Last Resort', 'Not Foreign Dub', 'Foreign Dub'),
  ('720p Compact Last Resort', 'Not AV1', 'AV1')
ON CONFLICT DO NOTHING;
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES
  ('720p Compact Last Resort', 'Bluray', 'bluray'),
  ('720p Compact Last Resort', 'WEB-DL', 'web_dl'),
  ('720p Compact Last Resort', 'WEBRip', 'webrip')
ON CONFLICT DO NOTHING;

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '720p Compact Last Resort', 'all', 3000)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

INSERT INTO quality_groups (quality_profile_name, name) VALUES
  ('Movies 2160p HEVC Compact', '720p Fallback')
ON CONFLICT DO NOTHING;
INSERT INTO quality_group_members (quality_profile_name, quality_group_name, quality_name, position) VALUES
  ('Movies 2160p HEVC Compact', '720p Fallback', 'Bluray-720p', 0),
  ('Movies 2160p HEVC Compact', '720p Fallback', 'WEBDL-720p', 1),
  ('Movies 2160p HEVC Compact', '720p Fallback', 'WEBRip-720p', 2)
ON CONFLICT DO NOTHING;
INSERT INTO quality_profile_qualities (quality_profile_name, quality_group_name, position, enabled, upgrade_until) VALUES
  ('Movies 2160p HEVC Compact', '720p Fallback', 2, 1, 0);

UPDATE quality_profiles
SET description = REPLACE(
  description,
  'Those two share the micro band and do not add to a tier that already matched.',
  'Those two share the micro band and do not add to a tier that already matched. A 720p HEVC or AVC Blu-ray, WEB-DL, or WEBRip scores 3000 in its own quality group below every 1080p quality, so a tagged 720p cannot outrank a 1080p release.'
)
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('720p last resort exists', (SELECT COUNT(*) = 1 FROM custom_formats WHERE name = '720p Compact Last Resort')),
  ('Movie 720p last resort is 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '720p Compact Last Resort')),
  ('TV does not score the 720p last resort', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '720p Compact Last Resort')),
  ('No other profile scores the 720p last resort', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name != 'Movies 2160p HEVC Compact' AND custom_format_name = '720p Compact Last Resort')),
  ('x265 (HD) stays off the movie profile', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'x265 (HD)')),
  ('1080p last resorts stay 3000', (SELECT COUNT(*) = 2 AND MIN(score) = 3000 AND MAX(score) = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Last Resort', '1080p Compact AVC Last Resort'))),
  ('1080p ladder stays 9600 / 6400 / 5200 / 4100 / 3000', (SELECT COUNT(*) = 5 AND SUM(CASE custom_format_name WHEN '1080p Compact HEVC Tier 1' THEN score WHEN '1080p Compact HEVC Tier 2' THEN score WHEN '1080p Compact Streaming WEB-DL' THEN score WHEN '1080p Compact HEVC Tier 3' THEN score WHEN '1080p Compact HEVC Tier 4' THEN score END) = 9600 + 6400 + 5200 + 4100 + 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Tier 1', '1080p Compact HEVC Tier 2', '1080p Compact Streaming WEB-DL', '1080p Compact HEVC Tier 3', '1080p Compact HEVC Tier 4'))),
  ('4K class scores stay put', (SELECT COUNT(*) = 9 AND SUM(score) = 38400 + 35200 + 32000 + 28800 + 28800 + 25600 + 19200 + 0 + 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('2160p Compact Bluray Tier 1', '2160p Compact Bluray Tier 2', '2160p Compact WEB Tier 1', '2160p Compact Streaming WEB-DL', '2160p Compact WEB Tier 2', '2160p Compact Bluray Tier 3', '2160p Compact WEB Tier 3', '2160p Compact Bluray Tier 4', '2160p Compact WEB Tier 4'))),
  ('Movie minimum and cutoff stay 3000 / 41600', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('720p rank is below the whole 1080p rank', (SELECT p720.position > p1080.position AND p1080.position > p2160.position AND p720.enabled = 1 AND p1080.enabled = 1 AND p2160.enabled = 1 AND p2160.upgrade_until = 1 AND p1080.upgrade_until = 0 AND p720.upgrade_until = 0 FROM quality_profile_qualities p720 JOIN quality_profile_qualities p1080 ON p1080.quality_profile_name = p720.quality_profile_name JOIN quality_profile_qualities p2160 ON p2160.quality_profile_name = p720.quality_profile_name WHERE p720.quality_profile_name = 'Movies 2160p HEVC Compact' AND p720.quality_group_name = '720p Fallback' AND p1080.quality_group_name = '1080p Fallback' AND p2160.quality_group_name = '2160p')),
  ('720p is not in the 1080p group', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND quality_group_name = '1080p Fallback' AND quality_name LIKE '%720p%')),
  ('1080p is not in the 720p group', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND quality_group_name = '720p Fallback' AND quality_name LIKE '%1080p%')),
  ('720p members are bluray, webdl, and webrip', (SELECT COUNT(*) = 3 AND SUM(quality_name = 'Bluray-720p') = 1 AND SUM(quality_name = 'WEBDL-720p') = 1 AND SUM(quality_name = 'WEBRip-720p') = 1 FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND quality_group_name = '720p Fallback')),
  ('HDTV 720p stays off the movie profile', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND quality_name = 'HDTV-720p')),
  ('480p stays off the movie profile', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND quality_name LIKE '%480p%')),
  ('TV gains no 720p qualities', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND quality_name LIKE '%720p%')),
  ('720p format requires 720p and negates 1080p and 2160p', (SELECT COUNT(*) = 3 FROM custom_format_conditions c JOIN condition_resolutions r ON r.custom_format_name = c.custom_format_name AND r.condition_name = c.name WHERE c.custom_format_name = '720p Compact Last Resort' AND ((c.name = 'Resolution' AND c.negate = 0 AND c.required = 1 AND r.resolution = '720p') OR (c.name = 'Not 1080p' AND c.negate = 1 AND c.required = 1 AND r.resolution = '1080p') OR (c.name = 'Not 2160p' AND c.negate = 1 AND c.required = 1 AND r.resolution = '2160p')))),
  ('720p format negates remux and banned micros', (SELECT COUNT(*) = 2 FROM custom_format_conditions c JOIN condition_patterns p ON p.custom_format_name = c.custom_format_name AND p.condition_name = c.name WHERE c.custom_format_name = '720p Compact Last Resort' AND c.negate = 1 AND c.required = 1 AND ((c.name = 'Not Remux' AND p.regular_expression_name = 'Remux') OR (c.name = 'Not Banned Micro' AND p.regular_expression_name = 'HEVC Compact Micro Ban')))),
  ('720p codec regex covers HEVC and AVC', (SELECT pattern LIKE '%26[45]%' AND pattern LIKE '%HEVC%' AND pattern LIKE '%AVC%' FROM regular_expressions WHERE name = '720p Last Resort Codec')),
  ('720p sources are bluray, web_dl, and webrip', (SELECT COUNT(*) = 3 AND SUM(source = 'bluray') = 1 AND SUM(source = 'web_dl') = 1 AND SUM(source = 'webrip') = 1 AND SUM(source = 'hdtv') = 0 FROM condition_sources WHERE custom_format_name = '720p Compact Last Resort')),
  ('720p size stays 0 / 1990 / 0', (SELECT COUNT(*) = 3 AND MIN(min_size) = 0 AND MAX(min_size) = 0 AND MIN(preferred_size) = 1990 AND MAX(preferred_size) = 1990 AND MIN(max_size) = 0 AND MAX(max_size) = 0 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-720p', 'WEBDL-720p', 'WEBRip-720p'))),
  ('Profile text names the 720p rank', (SELECT description LIKE '%720p HEVC or AVC Blu-ray, WEB-DL, or WEBRip scores 3000 in its own quality group below every 1080p quality%' FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact'));
DROP TABLE _pcd_assertions;

COMMIT;
