-- @description: Make Movies 2160p HEVC Compact hard rejects actually miss cutoff, and close German DDP5.1.DL plus Disney+/Apple TV+ identification holes
-- @author: cursor
-- @name: 974.fix-compact-rejects-dubs-and-storefronts

BEGIN TRANSACTION;

-- Ops 972 restacked movie classes to 12800-38400 and moved TrueHD, DTS-HD,
-- and SDR Blu-ray to -100000, because a -10000 penalty no longer clears a
-- tier that sits above 10000. The other hard rejects were left at -10000.
-- An elite HDR disc that is also CAM, hardcoded, 3D, upscaled, extras,
-- sing-along, audio description, VP9, VVC, or AVC-beside-x265 still scored
-- about 28930 and cleared min 3000. Dumpstarr's -10000 works only because
-- their tier bases are near 1900. Same grab decision here is -100000.
--
-- Not moved:
--   Dolby Vision (Without Fallback) stays -10000. A tiered FLUX/Kitsune/CMRG
--     DV WEB with no HDR token still clears cutoff. Dolby Vision WEB-DL is
--     not banned; an untiered DV WEB still misses min 3000. Fat DV WEB is
--     the 200 MB/min cap.
--   Foreign Dub stays -750. A dubbed elite disc keeps its tier.
--   8-bit stays -800.
--   TV scores are not restacked. TV tiers are under 10000, so -10000 still
--     clears them.
--   Encoder lists, class scores, and the Movies Anywhere +15 tie-break stay.

UPDATE quality_profile_custom_formats
SET score = -100000
WHERE quality_profile_name = 'Movies 2160p HEVC Compact'
  AND custom_format_name IN ('3D', 'AV1', 'Audio Description', 'Banned Groups', 'Banned Groups (Efficient)', 'Banned Groups (Regular)', 'Banned Micro Encodes', 'CAM', 'Extras', 'Full Disc', 'Full Disc (Quality Match)', 'Hardcoded Subtitles', 'Remux', 'Sing Along', 'Upscale', 'VP9', 'VVC', 'x264 (2160p)')
  AND score = -10000;

-- German.DDP5.1.DL, German.AC3.5.1.DL, German.EC3.DL, and German.DD5.1.DL
-- are scene dubs. The codec group stopped at the channel digits, so the DL
-- never matched, and a -GHOST WEB with that shape scored as the QxR encoder
-- Ghost. WEB-DL is still not a dub: the DL has to be the dub tag, not the
-- word WEB. Disc Ghost stays in the circle. The scene-GHOST negation is
-- still only on the WEB tiers.
UPDATE regular_expressions
SET pattern = '(?i)\b(?:(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)|(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)[._ -]+DL|DL[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:(?:DDP|DD\+|DD|E-?AC-?3|EC-?3|AC-?3|DTS)(?:[._ -]*\d{1,2}(?:[._ -]\d{1,2})?)?[._ -]*)?(?:LD|MD|DL))\b',
    description = 'Foreign dub tags, including scene AC3/DDP/EC3/DD channel tags such as DDP5.1.DL, AC3.5.1.DL, and EC3.DL. WEB-DL is not a dub.'
WHERE name = 'Foreign Dub';

UPDATE regular_expressions
SET pattern = '(?i)^(?=.*\bweb(?:rip|[-_. ]?(?:dl|rip))?\b).*\.(?:german|french|italian|spanish|castellano|russian|polish|turkish|hindi|dutch|danish|swedish|norwegian|finnish|czech|hungarian|ger|fre|fra|ita|esp|spa|rus|pol|tur|hin)\.(?:(?:ddp|dd\+|dd|e-?ac-?3|ec-?3|ac-?3|dts)(?:[._ -]*\d{1,2}(?:[._ -]\d{1,2})?)?[._ -]*)?(?:ld|md|dl|dubbed|dub)\b.*-ghost(?:\.[a-z0-9]{2,4})?$',
    description = 'Scene-language WEB release ending in -GHOST, including DDP5.1.DL and AC3.5.1.DL. Does not match the QxR encoder Ghost.'
WHERE name = 'Scene Dub GHOST';

-- Disney+.WEB-DL and Apple.TV+.WEB-DL failed the trailing word boundary:
-- a plus sign and the following dot are both non-word characters, so \b
-- never fired. ATVP and DSNP tokens are unchanged. ATV stays its own +10
-- format and is not pulled back into ATVP.
UPDATE regular_expressions
SET pattern = '\b(ATVP|APTV|Apple[ ._-]?TV\+)(?!\w)',
    description = 'Apple TV+ tokens ATVP, APTV, Apple TV+, and Apple.TV+. A plus sign may sit against the next dot. ATV is a separate format.'
WHERE name = 'Apple TV+';

UPDATE regular_expressions
SET pattern = '\b(DSNP|DSNY(?:P)?|Disney\+)(?!\w)',
    description = 'Disney+ tokens DSNP, DSNY, DSNYP, and Disney+. A plus sign may sit against the next dot.'
WHERE name = 'Disney+';

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Movie hard rejects are -100000', (SELECT COUNT(*) = 18 AND MIN(score) = -100000 AND MAX(score) = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('3D', 'AV1', 'Audio Description', 'Banned Groups', 'Banned Groups (Efficient)', 'Banned Groups (Regular)', 'Banned Micro Encodes', 'CAM', 'Extras', 'Full Disc', 'Full Disc (Quality Match)', 'Hardcoded Subtitles', 'Remux', 'Sing Along', 'Upscale', 'VP9', 'VVC', 'x264 (2160p)'))),
  ('DV without fallback stays -10000 on movies', (SELECT score = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Dolby Vision (Without Fallback)')),
  ('TV hard rejects stay -10000', (SELECT COUNT(*) = 19 AND MIN(score) = -10000 AND MAX(score) = -10000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND score = -10000 AND custom_format_name IN ('3D', 'AV1', 'Audio Description', 'Banned Groups', 'Banned Groups (Efficient)', 'Banned Groups (Regular)', 'Banned Micro Encodes', 'CAM', 'Extras', 'Full Disc', 'Full Disc (Quality Match)', 'Hardcoded Subtitles', 'Remux', 'Sing Along', 'Upscale', 'VP9', 'VVC', 'x264 (2160p)', 'Dolby Vision (Without Fallback)'))),
  ('TV WEB tier 1 stays 8100', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('TV disc stays under TV WEB', (SELECT w.score > d.score FROM quality_profile_custom_formats w JOIN quality_profile_custom_formats d ON d.quality_profile_name = w.quality_profile_name WHERE w.quality_profile_name = 'TV 2160p HEVC Compact' AND w.custom_format_name = '2160p Compact WEB Tier 1' AND d.custom_format_name = '2160p Compact Bluray Tier 1')),
  ('TV TrueHD stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'TrueHD')),
  ('Elite disc score stays 38400', (SELECT score = 38400 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Streaming WEB score stays 28800', (SELECT score = 28800 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('PSA disc still leads untouched WEB', (SELECT p.score > w.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats w ON w.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '2160p Compact Bluray Tier 3' AND w.custom_format_name = '2160p WEB-DL HEVC')),
  ('Elite disc still leads streaming', (SELECT d.score > s.score FROM quality_profile_custom_formats d JOIN quality_profile_custom_formats s ON s.quality_profile_name = d.quality_profile_name WHERE d.quality_profile_name = 'Movies 2160p HEVC Compact' AND d.custom_format_name = '2160p Compact Bluray Tier 1' AND s.custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('Movies Anywhere stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA')),
  ('ATV stays +10', (SELECT score = 10 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'ATV')),
  ('ATVP stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'ATVP')),
  ('SDR penalty stays -100000', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p SDR Bluray')),
  ('HD audio penalties stay -100000', (SELECT COUNT(*) = 4 AND MIN(score) = -100000 AND MAX(score) = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('TrueHD', 'DTS-HD MA', 'DTS-HD HRA', 'DTS-X'))),
  ('Foreign dub penalty stays -750', (SELECT score = -750 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'Foreign Dub')),
  ('Foreign dub allows a channel count before DL', (SELECT pattern LIKE '%\d{1,2}%' AND pattern LIKE '%EC-?3%' AND pattern LIKE '%DDP%' FROM regular_expressions WHERE name = 'Foreign Dub')),
  ('Scene GHOST allows a channel count before DL', (SELECT pattern LIKE '%\d{1,2}%' AND pattern LIKE '%-ghost%' FROM regular_expressions WHERE name = 'Scene Dub GHOST')),
  ('Scene GHOST negation is still WEB tiers only', (SELECT COUNT(*) = 2 FROM custom_format_conditions WHERE name = 'Not Scene Dub GHOST' AND custom_format_name IN ('2160p Compact WEB Tier 2', '1080p Compact HEVC Tier 2'))),
  ('Bluray tier 2 still does not negate Ghost', (SELECT COUNT(*) = 0 FROM custom_format_conditions WHERE custom_format_name = '2160p Compact Bluray Tier 2' AND name = 'Not Scene Dub GHOST')),
  ('Apple TV+ survives a plus against a dot and does not include ATV', (SELECT pattern = '\b(ATVP|APTV|Apple[ ._-]?TV\+)(?!\w)' FROM regular_expressions WHERE name = 'Apple TV+')),
  ('Disney+ survives a plus against a dot', (SELECT pattern = '\b(DSNP|DSNY(?:P)?|Disney\+)(?!\w)' FROM regular_expressions WHERE name = 'Disney+')),
  ('Elite regex still contains hallowed and HONE', (SELECT pattern LIKE '%hallowed%' AND pattern LIKE '%HONE%' AND pattern LIKE '%BHDStudio%' AND pattern NOT LIKE '%edge2020%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('Circle regex still contains edge2020 and Ghost', (SELECT pattern LIKE '%edge2020%' AND pattern LIKE '%Ghost%' AND pattern LIKE '%QxR%' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('Streaming regex still contains FLUX Kitsune CMRG', (SELECT pattern LIKE '%FLUX%' AND pattern LIKE '%Kitsune%' AND pattern LIKE '%CMRG%' FROM regular_expressions WHERE name = 'HEVC Compact Streaming WEB')),
  ('4K cap stays 6 / 130 / 200', (SELECT COUNT(*) = 4 AND MIN(min_size) = 6 AND MAX(min_size) = 6 AND MIN(preferred_size) = 130 AND MAX(preferred_size) = 130 AND MIN(max_size) = 200 AND MAX(max_size) = 200 FROM radarr_quality_definitions WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p')));
DROP TABLE _pcd_assertions;

COMMIT;
