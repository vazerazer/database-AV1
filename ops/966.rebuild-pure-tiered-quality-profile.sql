-- @description: Rebuild Movies 2160p AV1 HQ: AV1-first, Dumpstarr 2160p territory, full canonical rosters, strict monotonic spacing, x265 denied below 2160p
-- @author: Antigravity
-- @name: 966.rebuild-pure-tiered-quality-profile

BEGIN TRANSACTION;

-- 1. Configure Quality Profile Parameters
UPDATE "quality_profiles"
SET "minimum_custom_format_score" = 1000,
    "upgrade_until_score" = 3000,
    "upgrade_score_increment" = 300,
    "description" = 'Flagship 4K Quality profile (AV1-First, Dumpstarr 2160p Territory) targeting transparent 4K AV1 & x265 HDR/Dolby Vision encodes with ARC-optimized bitstream audio and vetted 1080p archival fallback.'
WHERE "name" = 'Movies 2160p AV1 HQ';

-- 2. Hard Quality Guarantee: Structurally remove Remux qualities from profile
DELETE FROM "quality_group_members"
WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ'
  AND "quality_name" IN ('Remux-2160p', 'Remux-1080p');

-- 3. Calibrate Radarr Quality Definitions (proportional runtime MB/min)
UPDATE "radarr_quality_definitions"
SET "min_size" = 30, "preferred_size" = 100, "max_size" = 185
WHERE "quality_name" IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'Remux-2160p', 'HDTV-2160p');

UPDATE "radarr_quality_definitions"
SET "min_size" = 12, "preferred_size" = 45, "max_size" = 120
WHERE "quality_name" IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'Remux-1080p', 'HDTV-1080p');

-- 4. Remove obsolete static size and blanket codec Custom Formats from active profile
DELETE FROM "quality_profile_custom_formats"
WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ'
  AND "custom_format_name" IN (
    'Heavy 2160p Fallback',
    'Oversized 2160p Fallback',
    'Extreme 2160p',
    'Micro Hard Floor',
    'AV1 Lean 2160p',
    'AV1 Micro 1080p',
    'AV1 Micro 2160p',
    'AV1 Storage Savers',
    'AV1 Nameless',
    'AV1 Unmeasured Encoders',
    'Not AV1',
    'AV1',
    'Legacy x264 Codec',
    'Legacy Trusted x264'
  );

-- 5. Create x265 (HD) custom format to deny x265/HEVC below 2160p (Dumpstarr rule)
INSERT INTO "custom_formats" ("name", "description")
VALUES ('x265 (HD)', 'Matches all 720p/1080p HD releases encoded in x265/HEVC to reject sub-4K x265 encodes')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "negate", "required", "arr_type")
VALUES 
  ('x265 (HD)', 'Resolution 1080p', 'resolution', 0, 0, 'all'),
  ('x265 (HD)', 'Resolution 720p', 'resolution', 0, 0, 'all'),
  ('x265 (HD)', 'x265 Codec', 'release_title', 0, 1, 'all')
ON CONFLICT DO NOTHING;

INSERT INTO "condition_resolutions" ("custom_format_name", "condition_name", "resolution")
VALUES 
  ('x265 (HD)', 'Resolution 1080p', '1080p'),
  ('x265 (HD)', 'Resolution 720p', '720p')
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES ('x265 (HD)', 'x265 Codec', 'x265')
ON CONFLICT DO NOTHING;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES ('Movies 2160p AV1 HQ', 'x265 (HD)', 'all', -10000)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = excluded.score;

-- 6. Tier 1 — Elite 4K Encoders (+3000 pts)
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES 
  ('Movies 2160p AV1 HQ', 'AV1 Quality Encoders', 'all', 3000),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 1', 'all', 3000),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 2', 'all', 3000),
  ('Movies 2160p AV1 HQ', '2160p Balanced Tier 1', 'all', 3000),
  ('Movies 2160p AV1 HQ', '2160p Balanced Tier 2', 'all', 3000),
  ('Movies 2160p AV1 HQ', '2160p Balanced Tier 3', 'all', 3000)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 3000;

-- 7. Tier 2 — Top 4K Encoders (+2200 pts)
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES 
  ('Movies 2160p AV1 HQ', 'WEB-DL Tier 1', 'all', 2200),
  ('Movies 2160p AV1 HQ', 'WEB-DL Tier 2', 'all', 2200),
  ('Movies 2160p AV1 HQ', 'WEB-DL Tier 3', 'all', 2200),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 3', 'all', 2200),
  ('Movies 2160p AV1 HQ', '2160p Quality Tier 4', 'all', 2200),
  ('Movies 2160p AV1 HQ', 'HONE Bluray', 'all', 2200),
  ('Movies 2160p AV1 HQ', 'HONE WEB', 'all', 2200)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 2200;

-- 8. Tier 3 — Archival 1080p Blu-ray Disc (+1400 pts)
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES 
  ('Movies 2160p AV1 HQ', '1080p Quality Tier 1', 'all', 1400),
  ('Movies 2160p AV1 HQ', '1080p Quality Tier 2', 'all', 1400),
  ('Movies 2160p AV1 HQ', '1080p Quality Tier 3', 'all', 1400),
  ('Movies 2160p AV1 HQ', '1080p Balanced Tier 1', 'all', 1400),
  ('Movies 2160p AV1 HQ', '1080p Balanced Tier 2', 'all', 1400)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 1400;

-- 9. Visual Features (Capped below 800)
UPDATE "quality_profile_custom_formats" SET "score" = 300 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Dolby Vision';
UPDATE "quality_profile_custom_formats" SET "score" = 250 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'HDR10+';
UPDATE "quality_profile_custom_formats" SET "score" = 200 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'HDR';
UPDATE "quality_profile_custom_formats" SET "score" = 150 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = '10-bit Depth';
UPDATE "quality_profile_custom_formats" SET "score" = 50  WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Hybrid';
UPDATE "quality_profile_custom_formats" SET "score" = 25  WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = '4K Remaster';
UPDATE "quality_profile_custom_formats" SET "score" = 50  WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Boutique Label';
UPDATE "quality_profile_custom_formats" SET "score" = 50  WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'CRIT';
UPDATE "quality_profile_custom_formats" SET "score" = 50  WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Theatrical';
UPDATE "quality_profile_custom_formats" SET "score" = 200 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'AV1 Compact Encoders';

-- 10. Direct ARC Audio Features (Capped below 800)
UPDATE "quality_profile_custom_formats" SET "score" = 200 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Dolby Atmos';
UPDATE "quality_profile_custom_formats" SET "score" = 120 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Dolby Digital +';
UPDATE "quality_profile_custom_formats" SET "score" = 100 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'DTS-X';
UPDATE "quality_profile_custom_formats" SET "score" = 100 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'TrueHD';
UPDATE "quality_profile_custom_formats" SET "score" = 100 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Lossless Audio';
UPDATE "quality_profile_custom_formats" SET "score" = 80  WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Dolby Digital';
UPDATE "quality_profile_custom_formats" SET "score" = 150 WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" = 'Opus 5.1 / 7.1';

-- 11. Update AV1 Quality Encoders Regex (Authoritative AV1 Ladder, Trailing-Group Anchored)
UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^\[(?:CHOPPERHITLER|ChopperHitler|CoSMiCSuRFeR|dAV1nci|RandH|KIMJI|TAoE|PRL|CHD|UH|RH|TiZU|R[-._ ]?(?:and|&)[-._ ]?H)\]|-(?:CHOPPERHITLER|ChopperHitler|CoSMiCSuRFeR|dAV1nci|RandH|KIMJI|TAoE|PRL|CHD|UH|RH|TiZU|R[-._ ]?(?:and|&)[-._ ]?H|\[(?:CHOPPERHITLER|ChopperHitler|CoSMiCSuRFeR|dAV1nci|RandH|KIMJI|TAoE|PRL|CHD|UH|RH|TiZU|R[-._ ]?(?:and|&)[-._ ]?H)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE "name" = 'AV1 Quality Encoders';

-- 12. Purge Saon from AV1 Compact Encoders
UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|onlyfaffs|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|Smokindevil|SmokinDevil)\]|-(?:WhiskeyJack|WhiskyJack|edge2020|UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|onlyfaffs|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|Smokindevil|SmokinDevil|\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|onlyfaffs|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|Smokindevil|SmokinDevil)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE "name" = 'AV1 Compact Encoders';

-- 13. Add Saon to Banned Groups
INSERT INTO "regular_expressions" ("name", "pattern")
VALUES ('Saon', '[-._]Saon(\]|\.|\b|$)')
ON CONFLICT ("name") DO UPDATE SET "pattern" = excluded.pattern;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "negate", "required", "arr_type")
VALUES ('Banned Groups', 'Saon', 'release_group', 0, 0, 'all')
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES ('Banned Groups', 'Saon', 'Saon')
ON CONFLICT DO NOTHING;

-- 14. Deduplicate overlapping group patterns across tiers
DELETE FROM "condition_patterns"
WHERE "custom_format_name" = '2160p Balanced Tier 1'
  AND lower("regular_expression_name") = 'hone';

DELETE FROM "condition_patterns"
WHERE "custom_format_name" = '1080p Quality Tier 3'
  AND lower("regular_expression_name") IN ('crisc', 'decibel', 'd-z0n3', 'edph', 'hisd', 'lolhd', 'tdd', 'tnp', 'zq', 'sbr');

DELETE FROM "condition_patterns"
WHERE "custom_format_name" = 'WEB-DL Tier 2'
  AND lower("regular_expression_name") IN ('flux', 'ntb', 'thefarm');

DELETE FROM "condition_patterns"
WHERE "custom_format_name" = 'WEB-DL Tier 3'
  AND lower("regular_expression_name") IN ('flux', 'ntb', 'thefarm', 'byndr', 'cmrg', 'hone', 'kitsune', 'tepes', 'webdv');

-- 15. Update Banned Groups Regex (Full Upstream Clean Groups, CHD & TiZU promoted to Tiers)
UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^\[(?:VISIONPLUSHDR|STUTTERSHIT|Feranki1980|ShieldBearer|jennaortega|COLLECTiVE|CREATiVE24|FaNGDiNG0|L0SERNIGHT|TERMiNAL|CrEwSaDe|GalaxyRG|RiffTrax|SUNSCREEN|edge2020HD|iNTENSO|HDHUB4U|KiNGDOM|BAUCKLEY|PATOMiEL|BARC0DE|C1NEM4|HDTime|HDWinG|MySiLU|NhaNc3|PRODJi|TEKNO3D|Tigole|Tofu4U|DEiMOS|EuReKA|MIRCrew|MarkII|MeGusta|RU4HD|SANTi|Scene|aXXo|beAst|iPlanet|mSD|nHD|nSD|nikt0|QxR|TGx|UTR|Judas|Ghost|Saon|41RGB|4K4U|AROMA|AZAZE|CDDHD|CHAOS|CTFOH|EPiC|FZHD|GPTHD|Leffe|LiGaS|Liber8|MTeam|PTNK|WiKi|YIFY|Zeus|24xHD|BdC|BTM|C4K|CiNE|DDR|DNL|DRX|FGT|FMD|FRDS|GHD|HDS|HDT|JFF|KIRA|LAMA|LUCY|Mesc|MuTT|OFT|Pahe|RDN|SHD|TBS|TIKO|WAF|YTS|d3g|iVy|mHD|x0r|AOC|E|KC)\]|-(?:VISIONPLUSHDR|STUTTERSHIT|Feranki1980|ShieldBearer|jennaortega|COLLECTiVE|CREATiVE24|FaNGDiNG0|L0SERNIGHT|TERMiNAL|CrEwSaDe|GalaxyRG|RiffTrax|SUNSCREEN|edge2020HD|iNTENSO|HDHUB4U|KiNGDOM|BAUCKLEY|PATOMiEL|BARC0DE|C1NEM4|HDTime|HDWinG|MySiLU|NhaNc3|PRODJi|TEKNO3D|Tigole|Tofu4U|DEiMOS|EuReKA|MIRCrew|MarkII|MeGusta|RU4HD|SANTi|Scene|aXXo|beAst|iPlanet|mSD|nHD|nSD|nikt0|QxR|TGx|UTR|Judas|Ghost|Saon|41RGB|4K4U|AROMA|AZAZE|CDDHD|CHAOS|CTFOH|EPiC|FZHD|GPTHD|Leffe|LiGaS|Liber8|MTeam|PTNK|WiKi|YIFY|Zeus|24xHD|BdC|BTM|C4K|CiNE|DDR|DNL|DRX|FGT|FMD|FRDS|GHD|HDS|HDT|JFF|KIRA|LAMA|LUCY|Mesc|MuTT|OFT|Pahe|RDN|SHD|TBS|TIKO|WAF|YTS|d3g|iVy|mHD|x0r|AOC|E|KC|\[(?:VISIONPLUSHDR|STUTTERSHIT|Feranki1980|ShieldBearer|jennaortega|COLLECTiVE|CREATiVE24|FaNGDiNG0|L0SERNIGHT|TERMiNAL|CrEwSaDe|GalaxyRG|RiffTrax|SUNSCREEN|edge2020HD|iNTENSO|HDHUB4U|KiNGDOM|BAUCKLEY|PATOMiEL|BARC0DE|C1NEM4|HDTime|HDWinG|MySiLU|NhaNc3|PRODJi|TEKNO3D|Tigole|Tofu4U|DEiMOS|EuReKA|MIRCrew|MarkII|MeGusta|RU4HD|SANTi|Scene|aXXo|beAst|iPlanet|mSD|nHD|nSD|nikt0|QxR|TGx|UTR|Judas|Ghost|Saon|41RGB|4K4U|AROMA|AZAZE|CDDHD|CHAOS|CTFOH|EPiC|FZHD|GPTHD|Leffe|LiGaS|Liber8|MTeam|PTNK|WiKi|YIFY|Zeus|24xHD|BdC|BTM|C4K|CiNE|DDR|DNL|DRX|FGT|FMD|FRDS|GHD|HDS|HDT|JFF|KIRA|LAMA|LUCY|Mesc|MuTT|OFT|Pahe|RDN|SHD|TBS|TIKO|WAF|YTS|d3g|iVy|mHD|x0r|AOC|E|KC)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE "name" = 'TRaSH Banned Groups';

-- 16. Transactional Verification Assertions (Fails transaction if invariants violated)
CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);

INSERT INTO _pcd_assertions (name, condition)
VALUES
  ('Active CF Count == 59', (SELECT count(*) = 59 FROM "quality_profile_custom_formats" WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ')),
  ('Banned Groups CF Count == 3', (SELECT count(*) = 3 FROM "quality_profile_custom_formats" WHERE "quality_profile_name" = 'Movies 2160p AV1 HQ' AND "custom_format_name" LIKE 'Banned Groups%')),
  ('Tier Regex Audio Token Immunity', (SELECT count(*) = 0 FROM "regular_expressions" r WHERE r.name IN ('AV1 Quality Encoders', 'AV1 Compact Encoders', 'Saon') AND (r.pattern LIKE '%(DTS|%' OR r.pattern LIKE '%|DTS|%' OR r.pattern LIKE '%|DTS)%' OR r.pattern LIKE '%(Atmos|%' OR r.pattern LIKE '%|Atmos|%' OR r.pattern LIKE '%|Atmos)%' OR r.pattern LIKE '%(TrueHD|%' OR r.pattern LIKE '%|TrueHD|%' OR r.pattern LIKE '%|TrueHD)%'))),
  ('Zero Tier vs Banned Collisions', (SELECT count(*) = 0 FROM "regular_expressions" r WHERE r.name = 'TRaSH Banned Groups' AND (r.pattern LIKE '%|CHD|%' OR r.pattern LIKE '%|TiZU|%' OR r.pattern LIKE '%|FLUX|%' OR r.pattern LIKE '%|dAV1nci|%')));

DROP TABLE _pcd_assertions;

COMMIT;
