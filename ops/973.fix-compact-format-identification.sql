-- @description: Fix Movies 2160p HEVC Compact identification: HDR10Plus was scored as SDR, German AC3.LD/MD was scored as CAM, scene group GHOST was scored as compact WEB, and HD audio named next to DD+ matched neither format
-- @author: cursor
-- @name: 973.fix-compact-format-identification

BEGIN TRANSACTION;

-- HDR10Plus / HDR10P / HDR10plus never matched the shared HDR regex, because
-- `\b` after HDR10 fails when the next character is a letter. HDR10+ (the
-- symbol) did match, and the HDR10+ format matched every spelling, so the
-- same disc was both HDR10+ (+500) and SDR (-100000). SDR now negates the
-- HDR10+ pattern too. That pattern also gains a bare HDR+ spelling; the HDR
-- format already negates it, so HDR and HDR10+ still cannot both score.
UPDATE regular_expressions
SET pattern = '\b(?:HDR10.?(\+|P(?:lus)?\b)|HDR\+)',
    description = 'HDR10+, HDR10Plus, HDR10P, and HDR+. Plain HDR and HDR10 stay on the HDR format.'
WHERE name = 'HDR10+';

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('2160p SDR Bluray', 'Not HDR10+', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('2160p SDR Bluray', 'Not HDR10+', 'HDR10+')
ON CONFLICT DO NOTHING;

UPDATE custom_formats
SET description = '4K Blu-ray with no HDR, HDR10, HDR10+, HDR10Plus, HDR10P, HLG, PQ, or Dolby Vision in the name. A WEB-DL is left alone.'
WHERE name = '2160p SDR Bluray';

-- 10-bit already treats HDR, HDR10, HDR10+, DV, and DoVi as 10-bit markers.
-- HDR10Plus failed the same word-boundary hole, and HLG/PQ were omitted.
UPDATE regular_expressions
SET pattern = '(?<![a-z0-9])(10[-._]?bit|10b|Hi10P|HDR10.?(\+|P(?:lus)?)|HDR10|HDR|HLG|PQ(?:10)?|DV|DoVi|Dolby[-._]?Vision)(?![a-z0-9])',
    description = '10-bit token, or an HDR/HDR10+/HLG/PQ/Dolby Vision tag that implies 10-bit.'
WHERE name = '10-bit Depth';

-- (AC3)?(LD|MD) treated any LD or MD token after the year as a cam. German
-- scene AC3.LD / AC3.MD is a line dub or mic dub on a retail WEB or Blu-ray.
-- Real CAM, HDCAM, TS, TC, SCREENER, TELESYNC, and TELECINE stay.
UPDATE regular_expressions
SET pattern = '(?i)(?<=\b[12]\d{3}\b).*?\b(?:CAM[ ._-]?(?:Rip)?|DCP(?:RIP)?|DVD[ ._-]?(?:SCR(?:EENER)?)|HD[ ._-]?(?:CAM|SCR|TC|TS)|(?:LINE|MIC)[ ._-]?(?:DUBBED|Audio|Audio[ ._-]?DUBBED)|HQ[ ._-]?LINE|SCREENER|(?:TC|TS)(?:Rip)?|TELE(?:CINE|SYNC)|WORKPRINT|ProRes)\b',
    description = 'Cam, telesync, telecine, and screener tags after the year. German AC3.LD and AC3.MD dubs are not cams.'
WHERE name = 'CAM';

-- German.AC3.LD, German.DL, and FRENCH.DL are scene dub tags. The old regex
-- only matched language glued to DUB/DUBBED/SYNCHRO, so Mutiny's German WEB
-- was not a foreign dub. WEB-DL is not a dub: DL has to follow the language,
-- not the word WEB.
UPDATE regular_expressions
SET pattern = '(?i)\b(?:(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)|(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)[._ -]+DL|DL[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:(?:AC-?3|E-?AC-?3|DDP|DD\+|DTS)[._ -]*)?(?:LD|MD|DL))\b',
    description = 'Foreign dub tags, including German scene AC3.LD, AC3.MD, and language.DL. WEB-DL is not a dub.'
WHERE name = 'Foreign Dub';

-- Ghost in the circle list is the QxR/TAoE encoder (often "Ghost QxR" or
-- "-Ghost"). GHOST the German scene group uses the same letters and was
-- scoring 2160p Compact WEB Tier 2. The circle regex is unchanged, so a
-- compact Ghost disc or an English "-Ghost" WEB still matches. Only a
-- scene-language dub tag plus a WEB token ending in -GHOST is rejected,
-- and only on the WEB tier formats. Blu-ray tier 2 is untouched.
INSERT INTO regular_expressions (name, pattern, description) VALUES (
  'Scene Dub GHOST',
  '(?i)^(?=.*\bweb(?:rip|[-_. ]?(?:dl|rip))?\b).*\.(?:german|french|italian|spanish|castellano|russian|polish|turkish|hindi|dutch|danish|swedish|norwegian|finnish|czech|hungarian|ger|fre|fra|ita|esp|spa|rus|pol|tur|hin)\.(?:(?:ac-?3|e-?ac-?3|ddp|dd\+|dts)[._ -]*)?(?:ld|md|dl|dubbed|dub)\b.*-ghost(?:\.[a-z0-9]{2,4})?$',
  'German-scene (and other scene-language) WEB release ending in -GHOST. Does not match the QxR encoder Ghost.'
) ON CONFLICT (name) DO UPDATE SET pattern = excluded.pattern, description = excluded.description;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES
  ('2160p Compact WEB Tier 2', 'Not Scene Dub GHOST', 'release_title', 'all', 1, 1),
  ('1080p Compact HEVC Tier 2', 'Not Scene Dub GHOST', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES
  ('2160p Compact WEB Tier 2', 'Not Scene Dub GHOST', 'Scene Dub GHOST'),
  ('1080p Compact HEVC Tier 2', 'Not Scene Dub GHOST', 'Scene Dub GHOST')
ON CONFLICT DO NOTHING;

-- E-AC-3 and EAC-3 are Dolby Digital Plus. The old regex required eac3 with
-- no hyphen before the 3, so E-AC-3 scored as no audio format.
UPDATE regular_expressions
SET pattern = '\bDD[P+]|\b(?:e[-_. ]?ac-?3|ec-?3)\b',
    description = 'Dolby Digital Plus: DDP, DD+, EAC3, E-AC-3, EAC-3, EC3.'
WHERE name = 'Dolby Digital +';

-- HD audio formats negated every lossy codec, and the lossy formats negated
-- HD audio. A name that lists TrueHD or DTS-HD MA plus a DD+ compatibility
-- track matched neither, so the -100000 direct-play penalty never fired.
-- The higher format no longer rejects itself because a lower codec is also
-- named. The lower format still rejects itself when the higher one is present,
-- so the two still do not stack.
DELETE FROM condition_patterns
WHERE (custom_format_name, condition_name) IN (
  ('TrueHD', 'Not DTS'),
  ('TrueHD', 'Not Dolby Digital'),
  ('TrueHD', 'Not Dolby Digital +'),
  ('TrueHD', 'Not FLAC'),
  ('DTS-X', 'Not AAC'),
  ('DTS-X', 'Not Dolby Digital'),
  ('DTS-X', 'Not Dolby Digital +'),
  ('DTS-X', 'Not FLAC'),
  ('DTS-X', 'Not PCM'),
  ('DTS-HD MA', 'Not AAC'),
  ('DTS-HD MA', 'Not Dolby Digital'),
  ('DTS-HD MA', 'Not Dolby Digital +'),
  ('DTS-HD MA', 'Not FLAC'),
  ('DTS-HD MA', 'Not PCM'),
  ('DTS-HD HRA', 'Not AAC'),
  ('DTS-HD HRA', 'Not Dolby Digital'),
  ('DTS-HD HRA', 'Not Dolby Digital +'),
  ('DTS-HD HRA', 'Not FLAC'),
  ('DTS-HD HRA', 'Not PCM'),
  ('DTS-ES', 'Not AAC'),
  ('DTS-ES', 'Not Dolby Digital'),
  ('DTS-ES', 'Not Dolby Digital +'),
  ('DTS-ES', 'Not FLAC'),
  ('DTS-ES', 'Not PCM'),
  ('DTS', 'Not AAC'),
  ('DTS', 'Not Dolby Digital'),
  ('DTS', 'Not Dolby Digital +'),
  ('DTS', 'Not FLAC'),
  ('DTS', 'Not PCM'),
  ('Dolby Digital +', 'Not AAC'),
  ('Dolby Digital +', 'Not FLAC'),
  ('Dolby Digital +', 'Not PCM'),
  ('Dolby Digital', 'Not AAC'),
  ('Dolby Digital', 'Not FLAC'),
  ('Dolby Digital', 'Not PCM')
);
DELETE FROM custom_format_conditions
WHERE (custom_format_name, name) IN (
  ('TrueHD', 'Not DTS'),
  ('TrueHD', 'Not Dolby Digital'),
  ('TrueHD', 'Not Dolby Digital +'),
  ('TrueHD', 'Not FLAC'),
  ('DTS-X', 'Not AAC'),
  ('DTS-X', 'Not Dolby Digital'),
  ('DTS-X', 'Not Dolby Digital +'),
  ('DTS-X', 'Not FLAC'),
  ('DTS-X', 'Not PCM'),
  ('DTS-HD MA', 'Not AAC'),
  ('DTS-HD MA', 'Not Dolby Digital'),
  ('DTS-HD MA', 'Not Dolby Digital +'),
  ('DTS-HD MA', 'Not FLAC'),
  ('DTS-HD MA', 'Not PCM'),
  ('DTS-HD HRA', 'Not AAC'),
  ('DTS-HD HRA', 'Not Dolby Digital'),
  ('DTS-HD HRA', 'Not Dolby Digital +'),
  ('DTS-HD HRA', 'Not FLAC'),
  ('DTS-HD HRA', 'Not PCM'),
  ('DTS-ES', 'Not AAC'),
  ('DTS-ES', 'Not Dolby Digital'),
  ('DTS-ES', 'Not Dolby Digital +'),
  ('DTS-ES', 'Not FLAC'),
  ('DTS-ES', 'Not PCM'),
  ('DTS', 'Not AAC'),
  ('DTS', 'Not Dolby Digital'),
  ('DTS', 'Not Dolby Digital +'),
  ('DTS', 'Not FLAC'),
  ('DTS', 'Not PCM'),
  ('Dolby Digital +', 'Not AAC'),
  ('Dolby Digital +', 'Not FLAC'),
  ('Dolby Digital +', 'Not PCM'),
  ('Dolby Digital', 'Not AAC'),
  ('Dolby Digital', 'Not FLAC'),
  ('Dolby Digital', 'Not PCM')
);

-- Full Disc's "not an encode" check only looked for x265/x264. A Blu-ray
-- named HEVC or AVC, which is how some encodes are titled, matched the disc
-- regex and took -10000 on top of a real tier. Complete discs that do not
-- say HEVC/AVC still match. x265 and x264 still match.
UPDATE regular_expressions
SET pattern = '[xh][ ._-]?265|\bHEVC(\b|\d)'
WHERE name = 'HEVC (Full Disc)';
UPDATE regular_expressions
SET pattern = '[xh][ ._-]?264|\bAVC(\b|\d)'
WHERE name = 'AVC (Full Disc)';

-- Saon is banned, but the regex required a hyphen in front of the name.
-- Release-group specs are tested against the parsed group ("Saon"), so the
-- ban never fired.
UPDATE regular_expressions
SET pattern = '(?<=^|[-._\[])Saon(?:\]|\.|\b|$)'
WHERE name = 'Saon';

-- HMAX is the usual Max/HBO Max token. MAX.WEB-DL already scores +15. HMAX
-- did not score on this profile at all. Same tie-break, not the old +2000.
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score)
VALUES ('Movies 2160p HEVC Compact', 'HMAX', 'all', 15)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('SDR negates HDR10+', (SELECT COUNT(*) = 1 FROM condition_patterns WHERE custom_format_name = '2160p SDR Bluray' AND condition_name = 'Not HDR10+' AND regular_expression_name = 'HDR10+')),
  ('HDR10+ pattern covers Plus and P', (SELECT pattern = '\b(?:HDR10.?(\+|P(?:lus)?\b)|HDR\+)' FROM regular_expressions WHERE name = 'HDR10+')),
  ('10-bit pattern covers HDR10Plus, HLG, and PQ', (SELECT pattern LIKE '%HDR10.?(\+|P(?:lus)?)%' AND pattern LIKE '%HLG%' AND pattern LIKE '%PQ(?:10)?%' FROM regular_expressions WHERE name = '10-bit Depth')),
  ('CAM no longer treats LD or MD as a cam', (SELECT pattern NOT LIKE '%(AC3)?(LD|MD)%' AND pattern LIKE '%SCREENER%' AND pattern LIKE '%TELE(?:CINE|SYNC)%' FROM regular_expressions WHERE name = 'CAM')),
  ('Foreign Dub covers scene LD and DL tags', (SELECT pattern LIKE '%LD|MD|DL%' FROM regular_expressions WHERE name = 'Foreign Dub')),
  ('Scene GHOST negation is on WEB tiers only', (SELECT COUNT(*) = 2 FROM custom_format_conditions WHERE name = 'Not Scene Dub GHOST' AND custom_format_name IN ('2160p Compact WEB Tier 2', '1080p Compact HEVC Tier 2'))),
  ('Bluray tier 2 does not negate Ghost', (SELECT COUNT(*) = 0 FROM custom_format_conditions WHERE custom_format_name = '2160p Compact Bluray Tier 2' AND name = 'Not Scene Dub GHOST')),
  ('Circle regex still contains Ghost', (SELECT pattern LIKE '%Ghost%' AND pattern LIKE '%QxR%' AND pattern LIKE '%TAoE%' FROM regular_expressions WHERE name = 'HEVC Compact Circle')),
  ('Elite regex still contains hallowed and HONE', (SELECT pattern LIKE '%hallowed%' AND pattern LIKE '%HONE%' AND pattern LIKE '%BHDStudio%' FROM regular_expressions WHERE name = 'HEVC Compact Elite')),
  ('DD+ covers E-AC-3', (SELECT pattern LIKE '%ac-?3%' FROM regular_expressions WHERE name = 'Dolby Digital +')),
  ('TrueHD no longer rejects itself for DD+', (SELECT COUNT(*) = 0 FROM custom_format_conditions WHERE custom_format_name = 'TrueHD' AND name = 'Not Dolby Digital +')),
  ('DTS-HD MA no longer rejects itself for DD+', (SELECT COUNT(*) = 0 FROM custom_format_conditions WHERE custom_format_name = 'DTS-HD MA' AND name = 'Not Dolby Digital +')),
  ('DTS-HD MA still rejects TrueHD and DTS-X', (SELECT COUNT(*) = 2 FROM custom_format_conditions WHERE custom_format_name = 'DTS-HD MA' AND name IN ('Not TrueHD', 'Not DTS-X'))),
  ('HEVC full-disc negate includes the word HEVC', (SELECT pattern LIKE '%HEVC%' AND pattern LIKE '%265%' FROM regular_expressions WHERE name = 'HEVC (Full Disc)')),
  ('Saon matches a bare group name', (SELECT pattern LIKE '%(?<=^|[-._\[])Saon%' FROM regular_expressions WHERE name = 'Saon')),
  ('HMAX is a +15 tie-break on movies', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'HMAX')),
  ('TV does not gain an HMAX score', (SELECT COUNT(*) = 0 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'HMAX')),
  ('Movies Anywhere stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA')),
  ('SDR penalty stays -100000', (SELECT score = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p SDR Bluray')),
  ('HD audio penalties stay -100000', (SELECT COUNT(*) = 4 AND MIN(score) = -100000 AND MAX(score) = -100000 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name IN ('TrueHD', 'DTS-HD MA', 'DTS-HD HRA', 'DTS-X'))),
  ('TV TrueHD stays +15', (SELECT score = 15 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = 'TrueHD')),
  ('TV WEB tier 1 stays 8100', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('TV disc stays under TV WEB', (SELECT w.score > d.score FROM quality_profile_custom_formats w JOIN quality_profile_custom_formats d ON d.quality_profile_name = w.quality_profile_name WHERE w.quality_profile_name = 'TV 2160p HEVC Compact' AND w.custom_format_name = '2160p Compact WEB Tier 1' AND d.custom_format_name = '2160p Compact Bluray Tier 1')),
  ('Elite disc still leads streaming', (SELECT d.score > s.score FROM quality_profile_custom_formats d JOIN quality_profile_custom_formats s ON s.quality_profile_name = d.quality_profile_name WHERE d.quality_profile_name = 'Movies 2160p HEVC Compact' AND d.custom_format_name = '2160p Compact Bluray Tier 1' AND s.custom_format_name = '2160p Compact Streaming WEB-DL')),
  ('Streaming still leads PSA', (SELECT s.score > p.score FROM quality_profile_custom_formats s JOIN quality_profile_custom_formats p ON p.quality_profile_name = s.quality_profile_name WHERE s.quality_profile_name = 'Movies 2160p HEVC Compact' AND s.custom_format_name = '2160p Compact Streaming WEB-DL' AND p.custom_format_name = '2160p Compact Bluray Tier 3')),
  ('PSA still leads untouched WEB', (SELECT p.score > w.score FROM quality_profile_custom_formats p JOIN quality_profile_custom_formats w ON w.quality_profile_name = p.quality_profile_name WHERE p.quality_profile_name = 'Movies 2160p HEVC Compact' AND p.custom_format_name = '2160p Compact Bluray Tier 3' AND w.custom_format_name = '2160p WEB-DL HEVC'));
DROP TABLE _pcd_assertions;

COMMIT;
