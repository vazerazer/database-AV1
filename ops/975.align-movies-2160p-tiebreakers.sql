-- @description: Align Movies 2160p HEVC Compact tie-breakers and Dolby Vision without fallback with Dumpstarr, without moving a class
-- @author: cursor
-- @name: 975.align-movies-2160p-tiebreakers

BEGIN TRANSACTION;

-- Dumpstarr Movies 2160p (stable) picks a winner inside a tier with these
-- extras: Dolby Vision 1000, HDR 500, HDR10+ 100, Dolby Digital + 125,
-- Special Edition 125, Dolby Digital 115, IMF 75, Atmos 25, AAC 10.
-- Their HDR format also matches an HDR10+ title, so HDR10+ lands at 600
-- and plain HDR at 500. Our HDR format excludes HDR10+, so the movie
-- profile scores HDR10+ at 600 directly. The numbers are small enough to
-- stay inside the 3200-point class gap. They are not scaled down further.
--
-- Storefronts keep a 15-point ceiling. Dumpstarr's order, divided by 5:
--   MA 15, DSNP and iTunes 10, ATVP / HMAX / MAX 5, AMZN and NF 2.
-- ATV and HULU are not scored on their Movies 2160p profile. They sit with
-- AMZN and NF so a vaguer Apple or Hulu token cannot outrank ATVP or DSNP.
--
-- Lossy DTS and DTS-ES are not HD-audio denials and are not bonuses there.
-- FLAC is not a format on that profile, so it is no longer a movie bonus.
-- IMAX and IMAX Enhanced are unscored on that profile (they belong to the
-- HQ profile). Scoring them here let IMAX beat Atmos.
--
-- Dolby Vision without an HDR fallback is -10000 there. That misses their
-- tiers, which sit near 1500. Our streaming tier is 28800, so the same
-- grab decision is -100000. TV stays -10000.
--
-- Not copied:
--   MA Preferred +2000, and the hallowed / BHDStudio / Baseline group bonuses.
--   Dumpstarr LQ groups and the PiRaTeS-style extra-bonus lists.
--   The No Audio ban. It matches a release that names no codec at all, and
--     that is how hallowed, BHDStudio, HONE, DarQ, and DiscoD usually write
--     a disc (Movie.2024.2160p.BluRay.HDR.x265-hallowed).
--   TrueHD Missing. It only hits CtrlHD, DON, EPSiLON, JustWatch, NoGroup,
--     PmP, TRiToN, and W4NK3R. Those groups are not in the compact tiers,
--     and an untiered disc already misses min 3000.
--   A PCM / LPCM penalty. Dumpstarr's PCM pattern is only there so a PCM
--     title is not "No Audio". They do not score PCM below zero.
--   7.1 and 5.1. We have no such formats, and their channel regexes are broad.
--   CRIT and BCORE. Their regexes also match release-group tokens.
--   Encoder lists, class scores, min 3000, cutoff 41600, and the 6/130/200 cap.
--   TV scores. TrueHD stays +15.

UPDATE quality_profile_custom_formats
SET score = 600
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name = 'HDR10+';

UPDATE quality_profile_custom_formats
SET score = 115
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name = 'Dolby Digital';

UPDATE quality_profile_custom_formats
SET score = 25
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name = 'Atmos';

UPDATE quality_profile_custom_formats
SET score = 10
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name = 'AAC';

UPDATE quality_profile_custom_formats
SET score = 125
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name = 'Special Edition';

UPDATE quality_profile_custom_formats
SET score = 0
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name IN ('DTS', 'DTS-ES', 'FLAC', 'IMAX', 'IMAX Enhanced');

UPDATE quality_profile_custom_formats
SET score = 10
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name IN ('DSNP', 'iT');

UPDATE quality_profile_custom_formats
SET score = 5
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name IN ('ATVP', 'HMAX', 'MAX');

UPDATE quality_profile_custom_formats
SET score = 2
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name IN ('AMZN', 'NF', 'ATV', 'HULU');

UPDATE quality_profile_custom_formats
SET score = -100000
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name = 'Dolby Vision (Without Fallback)';

INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES ('Movies 2160p HEVC Compact', 'IMF', 'all', 75)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = 'Compact 4K for a 55-inch Mini LED, a 32-inch 4K monitor, and a phone. Preferred Blu-ray encodes share one score (the whole elite list: hallowed, BHDStudio, HONE, DarQ, DiscoD, dkore, HQMUX, PTer, Chivaman, Weasley, Vyndros and the rest). Then a smaller disc (QxR, TAoE, edge2020), then compact streaming WEB (FLUX, Kitsune, CMRG), then PSA and the other micros, then BYNDR or NTb. Inside a class, Dolby Vision is +1000, HDR is +500, and HDR10+ is +600. Dolby Digital + is +125, Dolby Digital is +115, Atmos is +25, and AAC is +10. Special Edition is +125. Storefronts stay at or below +15: Movies Anywhere, then Disney+ and iTunes, then Apple TV+, Max, and HBO Max, then Amazon, Netflix, ATV, and Hulu. 4K Blu-ray without HDR is rejected. Dolby Vision without an HDR fallback is rejected. TrueHD, DTS-HD MA, DTS-HD HRA, and DTS-X are rejected for direct play. Lossy DTS is allowed and not preferred. Cap 200 MB/min. YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Dolby Vision stays +1000', (SELECT score = 1000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Vision')),
  ('HDR stays +500', (SELECT score = 500 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'HDR')),
  ('HDR10+ is the combined Dumpstarr weight', (SELECT score = 600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'HDR10+')),
  ('DD+ stays +125', (SELECT score = 125 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Digital +')),
  ('Dolby Digital is +115', (SELECT score = 115 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Digital')),
  ('Atmos is +25', (SELECT score = 25 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Atmos')),
  ('AAC is +10', (SELECT score = 10 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'AAC')),
  ('Special Edition is +125', (SELECT score = 125 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Special Edition')),
  ('IMF is +75', (SELECT score = 75 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'IMF')),
  ('Lossy DTS, DTS-ES, and FLAC are not movie bonuses', (SELECT COUNT(*) = 3 AND MIN(score) = 0 AND MAX(score) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('DTS', 'DTS-ES', 'FLAC'))),
  ('IMAX adds nothing on the movie profile', (SELECT COUNT(*) = 2 AND MIN(score) = 0 AND MAX(score) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('IMAX', 'IMAX Enhanced'))),
  ('PCM is not scored on the movie profile', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'PCM')),
  ('HD audio stays a hard miss', (SELECT COUNT(*) = 4 AND MIN(score) = -100000 AND MAX(score) = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('TrueHD', 'DTS-HD MA', 'DTS-HD HRA', 'DTS-X'))),
  ('DV without fallback misses a tiered WEB', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Vision (Without Fallback)')),
  ('SDR Blu-ray stays -100000', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p SDR Bluray')),
  ('Foreign dub stays -750', (SELECT score = -750 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Foreign Dub')),
  ('No Audio ban was not added', (SELECT COUNT(*) = 0 FROM custom_formats WHERE name = 'No Audio')),
  ('MA Preferred was not added', (SELECT COUNT(*) = 0 FROM custom_formats WHERE name = 'MA Preferred')),
  ('Movies Anywhere stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA')),
  ('DSNP and iTunes are +10', (SELECT COUNT(*) = 2 AND MIN(score) = 10 AND MAX(score) = 10 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('DSNP', 'iT'))),
  ('ATVP, HMAX, and MAX are +5', (SELECT COUNT(*) = 3 AND MIN(score) = 5 AND MAX(score) = 5 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('ATVP', 'HMAX', 'MAX'))),
  ('AMZN, NF, ATV, and HULU are +2', (SELECT COUNT(*) = 4 AND MIN(score) = 2 AND MAX(score) = 2 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('AMZN', 'NF', 'ATV', 'HULU'))),
  ('Hybrid stays a +15 local tie-break', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Hybrid')),
  ('10-bit stays +30', (SELECT score = 30 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '10-bit Depth')),
  ('8-bit stays -800', (SELECT score = -800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '8-bit Depth')),
  ('Elite disc score stays 38400', (SELECT score = 38400 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Circle disc score stays 35200', (SELECT score = 35200 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 2')),
  ('Elite WEB score stays 32000', (SELECT score = 32000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('Streaming WEB score stays 28800', (SELECT score = 28800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('PSA disc score stays 25600', (SELECT score = 25600 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 3')),
  ('Untouched WEB score stays 12800', (SELECT score = 12800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p WEB-DL HEVC')),
  ('Elite disc still leads streaming', (SELECT d.score > s.score FROM quality_profile_custom_formats d JOIN quality_profile_custom_formats s ON s.quality_profile_name = d.quality_profile_name WHERE d.quality_profile_name = 'Movies 2160p HEVC Compact' AND d.custom_format_name = '2160p Compact Bluray Tier 1' AND s.custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('Streaming still leads PSA', (SELECT s.score > p.score FROM quality_profile_custom_formats s JOIN quality_profile_custom_formats p ON p.quality_profile_name = s.quality_profile_name WHERE s.quality_profile_name = 'Movies 2160p HEVC Compact' AND s.custom_format_name = '2160p Compact Streaming WEB-DL' AND p.custom_format_name = '2160p Compact Bluray Tier 3')),
  ('PSA still leads untouched WEB', (SELECT p.score > w.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats w ON w.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '2160p Compact Bluray Tier 3' AND w.custom_format_name = '2160p WEB-DL HEVC')),
  ('Positive extras stay inside the class gap', (SELECT (a.score - b.score) > feats.total FROM quality_profile_custom_formats a JOIN quality_profile_custom_formats b ON b.quality_profile_name = a.quality_profile_name AND b.custom_format_name = '2160p Compact Bluray Tier 2' JOIN (SELECT COALESCE(SUM(score), 0) AS total FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND score > 0 AND score < 3000) feats WHERE a.quality_profile_name = 'Movies 2160p HEVC Compact' AND a.custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Profile gates stay 3000 / 41600 / 1', (SELECT minimum_custom_format_score = 3000 AND upgrade_until_score = 41600 AND upgrade_score_increment = 1 FROM quality_profiles WHERE name = 'Movies 2160p HEVC Compact')),
  ('4K cap stays 6 / 130 / 200', (SELECT COUNT(*) = 4 AND MIN(min_size) = 6 AND MAX(min_size) = 6 AND MIN(preferred_size) = 130 AND MAX(preferred_size) = 130 AND MIN(max_size) = 200 AND MAX(max_size) = 200 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p'))),
  ('Elite regex still contains hallowed and HONE', (SELECT pattern LIKE '%hallowed%' AND pattern LIKE '%HONE%' AND pattern LIKE '%BHDStudio%' AND pattern NOT LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('TV TrueHD stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'TrueHD')),
  ('TV HDR10+ stays +50', (SELECT score = 50 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'HDR10+')),
  ('TV Atmos stays +80', (SELECT score = 80 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'Atmos')),
  ('TV Dolby Digital stays +20', (SELECT score = 20 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'Dolby Digital')),
  ('TV IMAX stays +40', (SELECT score = 40 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'IMAX')),
  ('TV DV without fallback stays -10000', (SELECT score = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'Dolby Vision (Without Fallback)')),
  ('TV WEB tier 1 stays 8100', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('TV disc stays under TV WEB', (SELECT w.score > d.score FROM quality_profile_custom_formats w JOIN quality_profile_custom_formats d ON d.quality_profile_name = w.quality_profile_name WHERE w.quality_profile_name = 'TV 2160p HEVC Compact' AND w.custom_format_name = '2160p Compact WEB Tier 1' AND d.custom_format_name = '2160p Compact Bluray Tier 1'));
DROP TABLE _pcd_assertions;

COMMIT;
