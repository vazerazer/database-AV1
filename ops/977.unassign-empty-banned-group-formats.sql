-- @description: Unassign empty Banned Groups (Efficient) and Banned Groups (Regular) so Profilarr can sync
-- @author: cursor
-- @name: 977.unassign-empty-banned-group-formats

BEGIN TRANSACTION;

-- Op 191 kept unique bans on Banned Groups (Efficient) and Banned Groups
-- (Regular). Op 968 removed their last condition, RARBG, because RARBG is
-- a wanted Micro OK / Tier 4 encode. Both formats then compiled to
-- { name, specifications: [] }. Radarr rejects that create or update with
-- HTTP 400 "Must contain at least one Condition", so Custom Formats stay
-- 70/72 and Drift shows the two formats Missing. Movies 2160p HEVC Compact
-- also stays Modified, because it cannot attach the two scores.
--
-- An empty assigned format never matches a release. Unassigning it does
-- not change a grab. The shared Banned Groups list (~57 release groups)
-- and Banned Micro Encodes stay scored. RARBG, UTR, iVy, Joy, t0paz, and
-- POF stay on the Micro OK list and are not put back on a ban list.
-- The definitions stay in custom_formats. Unused empty definitions are
-- fine; assigned ones are not, because Profilarr syncs formats used by
-- selected profiles.
--
-- Op 974 counted these two among the hard rejects: 18 at -100000 on
-- Movies 2160p HEVC Compact, and 19 at -10000 on TV 2160p HEVC Compact.
-- Removing the assignments drops those counts by 2. The other rejects,
-- class scores, extras, group regexes, minimum, and cutoff stay put.
-- The same rows are also still assigned on the inherited Dictionarry
-- profiles (1080p/2160p Efficient, and Balanced/Quality/Remux/720p Quality).

DELETE FROM quality_profile_custom_formats
WHERE custom_format_name IN ('Banned Groups (Efficient)', 'Banned Groups (Regular)');

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Empty ban formats are unassigned everywhere', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE custom_format_name IN ('Banned Groups (Efficient)', 'Banned Groups (Regular)'))),
  ('Movie hard rejects drop to 16 at -100000', (SELECT COUNT(*) = 16 AND MIN(score) = -100000 AND MAX(score) = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('3D', 'AV1', 'Audio Description', 'Banned Groups', 'Banned Groups (Efficient)', 'Banned Groups (Regular)', 'Banned Micro Encodes', 'CAM', 'Extras', 'Full Disc', 'Full Disc (Quality Match)', 'Hardcoded Subtitles', 'Remux', 'Sing Along', 'Upscale', 'VP9', 'VVC', 'x264 (2160p)'))),
  ('TV hard rejects drop to 17 at -10000', (SELECT COUNT(*) = 17 AND MIN(score) = -10000 AND MAX(score) = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND score = -10000 AND custom_format_name IN ('3D', 'AV1', 'Audio Description', 'Banned Groups', 'Banned Groups (Efficient)', 'Banned Groups (Regular)', 'Banned Micro Encodes', 'CAM', 'Extras', 'Full Disc', 'Full Disc (Quality Match)', 'Hardcoded Subtitles', 'Remux', 'Sing Along', 'Upscale', 'VP9', 'VVC', 'x264 (2160p)', 'Dolby Vision (Without Fallback)'))),
  ('No profile assigns a custom format with zero conditions', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats qpcf WHERE NOT EXISTS (SELECT 1 FROM custom_format_conditions cfc WHERE cfc.custom_format_name = qpcf.custom_format_name))),
  ('Empty ban definitions are kept', (SELECT COUNT(*) = 2 FROM custom_formats WHERE name IN ('Banned Groups (Efficient)', 'Banned Groups (Regular)'))),
  ('Those definitions still have zero conditions', (SELECT COUNT(*) = 0 FROM custom_format_conditions WHERE custom_format_name IN ('Banned Groups (Efficient)', 'Banned Groups (Regular)'))),
  ('Movies still scores Banned Groups at -100000', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Banned Groups')),
  ('Movies still scores Banned Micro Encodes at -100000', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Banned Micro Encodes')),
  ('TV still scores Banned Groups at -10000', (SELECT score = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'Banned Groups')),
  ('TV still scores Banned Micro Encodes at -10000', (SELECT score = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'Banned Micro Encodes')),
  ('Micro OK groups were not put back on a ban list', (SELECT COUNT(*) = 0 FROM custom_format_conditions WHERE custom_format_name LIKE 'Banned%' AND name IN ('RARBG', 'UTR', 'iVy', 'Joy', 't0paz', 'POF', 'UTRcorp'))),
  ('Micro OK regex still lists RARBG UTR iVy Joy t0paz POF', (SELECT pattern LIKE '%RARBG%' AND pattern LIKE '%UTR%' AND pattern LIKE '%iVy%' AND pattern LIKE '%Joy%' AND pattern LIKE '%t0paz%' AND pattern LIKE '%POF%' FROM regular_expressions WHERE name = 'HEVC Compact Micro OK')),
  ('Untouched WEB-DL stays 0', (SELECT score = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p WEB-DL HEVC')),
  ('1080p streaming stays 5200', (SELECT score = 5200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact Streaming WEB-DL')),
  ('1080p PSA stays 4100', (SELECT score = 4100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 3')),
  ('1080p micro stays 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 4')),
  ('Elite disc stays 38400', (SELECT score = 38400 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Movie gates stay 3000 / 41600', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact'));
DROP TABLE _pcd_assertions;

COMMIT;
