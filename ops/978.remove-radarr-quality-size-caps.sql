-- @description: Remove Radarr quality size caps. Min 0, preferred 1999, max 0 (unlimited), matching Dumpstarr after op 367
-- @author: cursor
-- @name: 978.remove-radarr-quality-size-caps

BEGIN TRANSACTION;

-- Quality definitions are instance-wide size limits in MB/min. They are
-- not profile scores. A file under min or over max is rejected before
-- custom format score is considered. Preferred size only orders two
-- releases that already share a quality and a custom format score.
--
-- Dumpstarr Database op 365 added minimums. Op 367 rolled those Radarr
-- minimums back because they rejected LQ releases the profile still
-- wanted. After 367 every Radarr quality they touched is min 0, max 0,
-- preferred 1999. Radarr treats max 0 as unlimited. Preferred 1999 is
-- the top of the movie size slider, so an equal-score tie prefers the
-- larger file. It does not change a class score.
--
-- Rows this database still caps, and the ops that wrote them:
--   2160p Bluray/WEBDL/WEBRip/HDTV: 6 / 130 / 200 (ops 971 and 972)
--   1080p Bluray/WEBDL/WEBRip/HDTV: 3 / 14 / 40 (op 967)
--   Remux-2160p: 30 / 100 / 250 and Remux-1080p: 12 / 45 / 120 (op 966)
-- The 1080p max of 40 rejects fallback encodes already in a library
-- (Ralphy, DarQ, HONE, Tigole, TAoE). The 2160p max of 200 rejects a
-- large HONE-style WEB that group score, and 2160p WEB-DL HEVC at 0,
-- already rank. Remux is not on the compact profiles; the cap is still
-- an instance-wide reject, so it goes too.
--
-- 720p and the other Radarr qualities are already min 0, max 0,
-- preferred 1990. They stay there. This does not enable 720p.
-- Sonarr rows stay as ops 967 and 971 left them. Sonarr validates
-- preferred size at 1000 or below, so 1999 is a Radarr value. TV
-- profile scores and enabled qualities are not part of this op.
--
-- Custom format scores are unchanged. 2160p WEB-DL HEVC stays 0.
-- 1080p compact streaming WEB-DL stays 5200, tier 3 stays 4100, and
-- tier 4 stays 3000.

UPDATE radarr_quality_definitions
SET min_size = 0, preferred_size = 1999, max_size = 0
WHERE name = 'Radarr'
  AND quality_name IN (
    'Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p',
    'Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p',
    'Remux-2160p', 'Remux-1080p'
  );

UPDATE quality_profiles
SET description = 'Compact 4K for a 55-inch Mini LED, a 32-inch 4K monitor, and a phone. Preferred Blu-ray encodes share one score (the whole elite list: hallowed, BHDStudio, HONE, DarQ, DiscoD, dkore, HQMUX, PTer, Chivaman, Weasley, Vyndros, Ralphy and the rest), then a smaller disc (QxR, TAoE, edge2020). An elite WEB such as HONE stays above compact streaming WEB (FLUX, Kitsune, CMRG). Then PSA, then UTR, RARBG and iVy. Untouched 4K WEB-DL (BYNDR, NTb, XEBEC, HHWEB) scores 0 and does not clear the minimum, so the search continues at 1080p: elite HEVC, then the smaller circle, then FLUX/Kitsune/CMRG, then PSA, then a micro. A 4K file already imported is not replaced by 1080p. Inside a class, Dolby Vision is +1000, HDR is +500, and HDR10+ is +600. Dolby Digital + is +125, Dolby Digital is +115, Atmos is +25, and AAC is +10. Special Edition is +125. Storefronts stay at or below +15: Movies Anywhere, then Disney+ and iTunes, then Apple TV+, Max, and HBO Max, then Amazon, Netflix, ATV, and Hulu. 4K Blu-ray without HDR is rejected. Dolby Vision without an HDR fallback is rejected. TrueHD, DTS-HD MA, DTS-HD HRA, and DTS-X are rejected for direct play. Lossy DTS is allowed and not preferred. No bitrate cap (min 0, preferred 1999, max unlimited). YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Touched Radarr qualities are 0 / 1999 / 0', (SELECT COUNT(*) = 10 AND MIN(min_size) = 0 AND MAX(min_size) = 0 AND MIN(preferred_size) = 1999 AND MAX(preferred_size) = 1999 AND MIN(max_size) = 0 AND MAX(max_size) = 0 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p', 'Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p', 'Remux-2160p', 'Remux-1080p'))),
  ('No Radarr quality keeps a min or a max', (SELECT COUNT(*) = 0 FROM radarr_quality_definitions WHERE min_size != 0 OR max_size != 0)),
  ('Untouched Radarr qualities stay 0 / 1990 / 0', (SELECT COUNT(*) = 20 AND MIN(min_size) = 0 AND MAX(min_size) = 0 AND MIN(preferred_size) = 1990 AND MAX(preferred_size) = 1990 AND MIN(max_size) = 0 AND MAX(max_size) = 0 FROM radarr_quality_definitions WHERE quality_name NOT IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p', 'Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p', 'Remux-2160p', 'Remux-1080p'))),
  ('720p Bluray stays preferred 1990', (SELECT min_size = 0 AND preferred_size = 1990 AND max_size = 0 FROM radarr_quality_definitions WHERE name = 'Radarr' AND quality_name = 'Bluray-720p')),
  ('Sonarr 2160p size stays 6 / 130 / 200', (SELECT COUNT(*) = 4 AND MIN(min_size) = 6 AND MAX(min_size) = 6 AND MIN(preferred_size) = 130 AND MAX(preferred_size) = 130 AND MIN(max_size) = 200 AND MAX(max_size) = 200 FROM sonarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p'))),
  ('Sonarr 1080p size stays 2 / 10 / 30', (SELECT COUNT(*) = 4 AND MIN(min_size) = 2 AND MAX(min_size) = 2 AND MIN(preferred_size) = 10 AND MAX(preferred_size) = 10 AND MIN(max_size) = 30 AND MAX(max_size) = 30 FROM sonarr_quality_definitions WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p'))),
  ('720p stays off the compact profiles', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name IN ('Movies 2160p HEVC Compact', 'TV 2160p HEVC Compact') AND quality_name LIKE '%720p%')),
  ('Remux stays off the compact profiles', (SELECT COUNT(*) = 0 FROM quality_group_members WHERE quality_profile_name IN ('Movies 2160p HEVC Compact', 'TV 2160p HEVC Compact') AND quality_name LIKE 'Remux%')),
  ('2160p WEB-DL HEVC stays 0', (SELECT score = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p WEB-DL HEVC')),
  ('1080p streaming stays 5200', (SELECT score = 5200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact Streaming WEB-DL')),
  ('1080p tier 3 stays 4100', (SELECT score = 4100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 3')),
  ('1080p tier 4 stays 3000', (SELECT score = 3000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '1080p Compact HEVC Tier 4')),
  ('Movie profile drops the 200 MB/min cap', (SELECT description NOT LIKE '%Cap 200%' AND description LIKE '%preferred 1999%' FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact'));
DROP TABLE _pcd_assertions;

COMMIT;
