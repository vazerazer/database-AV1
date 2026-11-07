-- @description: Prefer the compact size window, and score movie 4K micros at 0 so 1080p can be grabbed
-- @author: cursor
-- @name: 979.prefer-compact-size-and-skip-4k-micros

BEGIN TRANSACTION;

-- Op 978 removed the hard rejects: min 0, max 0. Max 0 stays unlimited.
-- Preferred 1999 was the top of the Radarr slider, and DownloadDecisionComparer
-- picks the release closest to runtime * preferred MB/min when custom format
-- scores already match. That made the largest file win the tie. Preferred
-- now aims at the compact window instead.
--
--   2160p Bluray/WEBDL/WEBRip/HDTV: preferred 130. That is the hallowed
--   (~135 MB/min) and BHDStudio (~120 MB/min) window.
--   1080p Bluray/WEBDL/WEBRip/HDTV: preferred 18. 18 is the integer midpoint
--   of the 15-20 MB/min band. A 120-minute movie prefers about 2.1 GB.
--   The old preferred of 14 sat under that band. 18 is not a ceiling.
--   Remux-2160p and Remux-1080p stay min 0, preferred 1999, max 0. Remux
--   is not on either compact profile, and this op does not enable it.
--   720p and the other already-unlimited Radarr rows stay min 0,
--   preferred 1990, max 0.
--   Sonarr rows stay as ops 967 and 971 left them. Sonarr rejects a
--   preferred size above 1000.
--
-- Movies 2160p HEVC Compact only: 2160p Compact Bluray Tier 4 and
-- 2160p Compact WEB Tier 4 go from 22400 and 16000 to 0. Those formats
-- match HEVC Compact Micro OK (RARBG, UTR, iVy, Joy, t0paz, POF, UTRcorp).
-- Radarr will not pick 1080p over an allowed 2160p release, so a 4K micro
-- that clears min 3000 always beats 1080p Tier 1 at 9600. Score 0 misses
-- the minimum, the same way 2160p WEB-DL HEVC does, and the format stays
-- assigned so a sync overwrites the old score. The definitions are not
-- deleted, and the groups are not put back on a ban list.
--
-- 4K Tier 3 stays the last real 4K fallback: Bluray 25600, WEB 19200.
-- Streaming WEB stays 28800, above PSA. 1080p Tier 4 stays 3000.
-- 1080p Tier 1 stays 9600, Tier 2 6400, streaming 5200, Tier 3 4100.
-- TV keeps its own rows (bluray tier 4 at 3200, web tier 4 at 6000).

UPDATE radarr_quality_definitions
SET min_size = 0, preferred_size = 130, max_size = 0
WHERE name = 'Radarr'
  AND quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');

UPDATE radarr_quality_definitions
SET min_size = 0, preferred_size = 18, max_size = 0
WHERE name = 'Radarr'
  AND quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p');

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '2160p Compact Bluray Tier 4', 'all', 0),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 4', 'all', 0)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = 'Compact 4K for a 55-inch Mini LED, a 32-inch 4K monitor, and a phone. Preferred Blu-ray encodes share one score (the whole elite list: hallowed, BHDStudio, HONE, DarQ, DiscoD, dkore, HQMUX, PTer, Chivaman, Weasley, Vyndros, Ralphy and the rest), then a smaller disc (QxR, TAoE, edge2020). An elite WEB such as HONE stays above compact streaming WEB (FLUX, Kitsune, CMRG). Then PSA, the last 4K fallback that clears the minimum. A 4K micro (UTR, RARBG, iVy, Joy, t0paz, POF) scores 0, and so does untouched 4K WEB-DL (BYNDR, NTb, XEBEC, HHWEB). Neither clears the minimum, so the search continues at 1080p: elite HEVC, then the smaller circle, then FLUX/Kitsune/CMRG, then PSA, then a micro. A 4K file already imported is not replaced by 1080p. Inside a class, Dolby Vision is +1000, HDR is +500, and HDR10+ is +600. Dolby Digital + is +125, Dolby Digital is +115, Atmos is +25, and AAC is +10. Special Edition is +125. Storefronts stay at or below +15: Movies Anywhere, then Disney+ and iTunes, then Apple TV+, Max, and HBO Max, then Amazon, Netflix, ATV, and Hulu. 4K Blu-ray without HDR is rejected. Dolby Vision without an HDR fallback is rejected. TrueHD, DTS-HD MA, DTS-HD HRA, and DTS-X are rejected for direct play. Lossy DTS is allowed and not preferred. No bitrate cap (min 0, max unlimited). Preferred size is 130 MB/min at 2160p and 18 MB/min at 1080p. YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('4K encode preferred is 130 and max stays 0', (SELECT COUNT(*) = 4 AND MIN(min_size) = 0 AND MAX(min_size) = 0 AND MIN(preferred_size) = 130 AND MAX(preferred_size) = 130 AND MIN(max_size) = 0 AND MAX(max_size) = 0 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p'))),
  ('1080p encode preferred is 18 and max stays 0', (SELECT COUNT(*) = 4 AND MIN(min_size) = 0 AND MAX(min_size) = 0 AND MIN(preferred_size) = 18 AND MAX(preferred_size) = 18 AND MIN(max_size) = 0 AND MAX(max_size) = 0 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p'))),
  ('Remux preferred stays 1999', (SELECT COUNT(*) = 2 AND MIN(min_size) = 0 AND MAX(min_size) = 0 AND MIN(preferred_size) = 1999 AND MAX(preferred_size) = 1999 AND MIN(max_size) = 0 AND MAX(max_size) = 0 FROM radarr_quality_definitions WHERE quality_name IN ('Remux-2160p', 'Remux-1080p'))),
  ('720p Bluray stays 0 / 1990 / 0', (SELECT min_size = 0 AND preferred_size = 1990 AND max_size = 0 FROM radarr_quality_definitions WHERE name = 'Radarr' AND quality_name = 'Bluray-720p')),
  ('Sonarr 2160p size stays 6 / 130 / 200', (SELECT COUNT(*) = 4 AND MIN(min_size) = 6 AND MAX(min_size) = 6 AND MIN(preferred_size) = 130 AND MAX(preferred_size) = 130 AND MIN(max_size) = 200 AND MAX(max_size) = 200 FROM sonarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p'))),
  ('Sonarr 1080p size stays 2 / 10 / 30', (SELECT COUNT(*) = 4 AND MIN(min_size) = 2 AND MAX(min_size) = 2 AND MIN(preferred_size) = 10 AND MAX(preferred_size) = 10 AND MIN(max_size) = 30 AND MAX(max_size) = 30 FROM sonarr_quality_definitions WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p'))),
  ('Movie 4K tier 4 scores are 0', (SELECT COUNT(*) = 2 AND MIN(score) = 0 AND MAX(score) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('2160p Compact Bluray Tier 4', '2160p Compact WEB Tier 4'))),
  ('4K tier 4 formats still exist', (SELECT COUNT(*) = 2 FROM custom_formats WHERE name IN ('2160p Compact Bluray Tier 4', '2160p Compact WEB Tier 4'))),
  ('Micro OK list still names the groups', (SELECT pattern LIKE '%RARBG%' AND pattern LIKE '%UTR%' AND pattern LIKE '%iVy%' AND pattern LIKE '%Joy%' AND pattern LIKE '%t0paz%' AND pattern LIKE '%POF%' FROM regular_expressions WHERE name = 'HEVC Compact Micro OK')),
  ('4K PSA bluray still clears 3000', (SELECT score = 25600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 3')),
  ('4K PSA WEB still clears 3000', (SELECT score = 19200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 3')),
  ('4K streaming stays above PSA', (SELECT s.score = 28800 AND s.score > p.score FROM quality_profile_custom_formats s JOIN quality_profile_custom_formats p ON p.quality_profile_name = s.quality_profile_name AND p.custom_format_name = '2160p Compact Bluray Tier 3' WHERE s.quality_profile_name = 'Movies 2160p HEVC Compact' AND s.custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('1080p ladder stays 9600 / 6400 / 5200 / 4100 / 3000', (SELECT COUNT(*) = 5 AND SUM(CASE custom_format_name WHEN '1080p Compact HEVC Tier 1' THEN score WHEN '1080p Compact HEVC Tier 2' THEN score WHEN '1080p Compact Streaming WEB-DL' THEN score WHEN '1080p Compact HEVC Tier 3' THEN score WHEN '1080p Compact HEVC Tier 4' THEN score END) = 9600 + 6400 + 5200 + 4100 + 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('1080p Compact HEVC Tier 1', '1080p Compact HEVC Tier 2', '1080p Compact Streaming WEB-DL', '1080p Compact HEVC Tier 3', '1080p Compact HEVC Tier 4'))),
  ('Movie minimum and cutoff stay 3000 / 41600', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('TV 4K bluray tier 4 stays 3200', (SELECT score = 3200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 4')),
  ('TV 4K web tier 4 stays 6000', (SELECT score = 6000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 4')),
  ('Remux stays off the compact profiles', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name IN ('Movies 2160p HEVC Compact', 'TV 2160p HEVC Compact') AND quality_name LIKE 'Remux%')),
  ('720p stays off the compact profiles', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name IN ('Movies 2160p HEVC Compact', 'TV 2160p HEVC Compact') AND quality_name LIKE '%720p%'));
DROP TABLE _pcd_assertions;

COMMIT;
