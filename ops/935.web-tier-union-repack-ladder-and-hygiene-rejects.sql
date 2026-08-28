-- @operation: export
-- @entity: batch
-- @name: Op 935 WEB-Tier Union Repack Ladder and Hygiene Rejects
-- @exportedAt: 2026-08-28T11:45:00.000Z
-- @opIds: 29940, 29941, 29942

-- ============================================================================
-- 1. 4K REMASTER / RESTORATION CUSTOM FORMAT (+25 PTS)
-- ============================================================================

INSERT INTO "custom_formats" ("name", "description")
VALUES ('4K Remaster', '4K Remaster / Restored edition tag (+25 pts)')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('Remastered', '\b(Remaster(ed)?|Restored|4K[ ._-]?Remaster(ed)?|Restoration)\b', 'Remastered or restored edition tag')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('4K Remaster', 'Remastered', 'release_title', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('4K Remaster', 'Remastered', 'Remastered')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 2. HYGIENE REJECTS: DVS / LINE AUDIO / PRORES (-10000 PTS)
-- ============================================================================

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('DVS', '\b(DVS|Descriptive[ ._-]?Audio|Descriptive[ ._-]?Video[ ._-]?Service)\b', 'Descriptive video service audio track')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('Audio Description', 'DVS', 'release_title', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('Audio Description', 'DVS', 'DVS')
ON CONFLICT DO NOTHING;

UPDATE "regular_expressions"
SET "pattern" = '(?i)(?<=\b[12]\d{3}\b).*?\b(?:(AC3)?(LD|MD)|CAM[ ._-]?(?:Rip)?|DCP(?:RIP)?|DVD[ ._-]?(?:SCR(?:EENER)?)|HD[ ._-]?(?:CAM|SCR|TC|TS)|(?:LINE|MIC)[ ._-]?(?:DUBBED|Audio|Audio[ ._-]?DUBBED)|HQ[ ._-]?LINE|SCREENER|(?:TC|TS)(?:Rip)?|TELE(?:CINE|SYNC)|WORKPRINT|ProRes)\b'
WHERE "name" = 'CAM';

-- ============================================================================
-- 3. WEB-DL TIER 2 VETTED GROUP UNION (46 GROUPS)
-- ============================================================================

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('SiGMA', '(?<=^|[\s.-])(SiGMA|SIGMA)\b', 'Vetted WEB group SiGMA'),
  ('JETIX', '(?<=^|[\s.-])JETIX\b', 'Vetted WEB group JETIX'),
  ('CEBEX', '(?<=^|[\s.-])CEBEX\b', 'Vetted WEB group CEBEX'),
  ('RTN', '(?<=^|[\s.-])RTN\b', 'Vetted WEB group RTN'),
  ('SDCC', '(?<=^|[\s.-])SDCC\b', 'Vetted WEB group SDCC'),
  ('GNOME', '(?<=^|[\s.-])GNOME\b', 'Vetted WEB group GNOME'),
  ('SLiGNOME', '(?<=^|[\s.-])SLiGNOME\b', 'Vetted WEB group SLiGNOME'),
  ('CRUD', '(?<=^|[\s.-])CRUD\b', 'Vetted WEB group CRUD'),
  ('DRACULA', '(?<=^|[\s.-])DRACULA\b', 'Vetted WEB group DRACULA'),
  ('PHOENiX', '(?<=^|[\s.-])PHOENiX\b', 'Vetted WEB group PHOENiX'),
  ('PSiG', '(?<=^|[\s.-])PSiG\b', 'Vetted WEB group PSiG'),
  ('DEEP', '(?<=^|[\s.-])DEEP\b', 'Vetted WEB group DEEP'),
  ('orbitron', '(?<=^|[\s.-])orbitron\b', 'Vetted WEB group orbitron'),
  ('APEX', '(?<=^|[\s.-])APEX\b', 'Vetted WEB group APEX'),
  ('BLOOM', '(?<=^|[\s.-])BLOOM\b', 'Vetted WEB group BLOOM'),
  ('ETHiCS', '(?<=^|[\s.-])ETHiCS\b', 'Vetted WEB group ETHiCS'),
  ('ViSUM', '(?<=^|[\s.-])ViSUM\b', 'Vetted WEB group ViSUM'),
  ('XEPA', '(?<=^|[\s.-])XEPA\b', 'Vetted WEB group XEPA'),
  ('MiU', '(?<=^|[\s.-])MiU\b', 'Vetted WEB group MiU'),
  ('PEXA', '(?<=^|[\s.-])PEXA\b', 'Vetted WEB group PEXA'),
  ('Dooky', '(?<=^|[\s.-])Dooky\b', 'Vetted WEB group Dooky'),
  ('iKA', '(?<=^|[\s.-])iKA\b', 'Vetted WEB group iKA'),
  ('KiMCHI', '(?<=^|[\s.-])KiMCHI\b', 'Vetted WEB group KiMCHI'),
  ('NYH', '(?<=^|[\s.-])NYH\b', 'Vetted WEB group NYH'),
  ('ABBIE', '(?<=^|[\s.-])(ABBIE|ABBiE)\b', 'Vetted WEB group ABBIE'),
  ('FC', '(?<=^|[\s.-])FC\b', 'Vetted WEB group FC'),
  ('iJP', '(?<=^|[\s.-])iJP\b', 'Vetted WEB group iJP'),
  ('PAXA', '(?<=^|[\s.-])PAXA\b', 'Vetted WEB group PAXA'),
  ('Flights', '(?<=^|[\s.-])Flights\b', 'Vetted WEB group Flights'),
  ('T6D', '(?<=^|[\s.-])T6D\b', 'Vetted WEB group T6D'),
  ('T4H', '(?<=^|[\s.-])T4H\b', 'Vetted WEB group T4H'),
  ('SiC', '(?<=^|[\s.-])SiC\b', 'Vetted WEB group SiC'),
  ('CiT', '(?<=^|[\s.-])CiT\b', 'Vetted WEB group CiT'),
  ('NINJACENTRAL', '(?<=^|[\s.-])NINJACENTRAL\b', 'Vetted WEB group NINJACENTRAL'),
  ('dB', '(?<=^|[\s.-])dB\b', 'Vetted WEB group dB'),
  ('END', '(?<=^|[\s.-])END\b', 'Vetted WEB group END'),
  ('SwAgLaNdEr', '(?<=^|[\s.-])SwAgLaNdEr\b', 'Vetted WEB group SwAgLaNdEr'),
  ('iT00NZ', '(?<=^|[\s.-])iT00NZ\b', 'Vetted WEB group iT00NZ'),
  ('ROCCaT', '(?<=^|[\s.-])ROCCaT\b', 'Vetted WEB group ROCCaT'),
  ('ViSiON', '(?<=^|[\s.-])ViSiON\b', 'Vetted WEB group ViSiON'),
  ('3cTWeB', '(?<=^|[\s.-])3cTWeB\b', 'Vetted WEB group 3cTWeB'),
  ('RTFM', '(?<=^|[\s.-])RTFM\b', 'Vetted WEB group RTFM'),
  ('SPiRiT', '(?<=^|[\s.-])SPiRiT\b', 'Vetted WEB group SPiRiT'),
  ('4KBEC', '(?<=^|[\s.-])4KBEC\b', 'Vetted WEB group 4KBEC'),
  ('Coo7', '(?<=^|[\s.-])Coo7\b', 'Vetted WEB group Coo7'),
  ('WEBDV', '(?<=^|[\s.-])WEBDV\b', 'Vetted WEB group WEBDV')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('WEB-DL Tier 2', 'SiGMA', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'JETIX', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'CEBEX', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'RTN', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SDCC', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'GNOME', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SLiGNOME', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'CRUD', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'DRACULA', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'PHOENiX', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'PSiG', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'DEEP', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'orbitron', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'APEX', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'BLOOM', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'ETHiCS', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'ViSUM', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'XEPA', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'MiU', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'PEXA', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'Dooky', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'iKA', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'KiMCHI', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'NYH', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'ABBIE', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'FC', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'iJP', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'PAXA', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'Flights', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'T6D', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'T4H', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SiC', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'CiT', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'NINJACENTRAL', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'dB', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'END', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SwAgLaNdEr', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'iT00NZ', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'ROCCaT', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'ViSiON', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', '3cTWeB', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'RTFM', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SPiRiT', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', '4KBEC', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'Coo7', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'WEBDV', 'release_group', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('WEB-DL Tier 2', 'SiGMA', 'SiGMA'),
  ('WEB-DL Tier 2', 'JETIX', 'JETIX'),
  ('WEB-DL Tier 2', 'CEBEX', 'CEBEX'),
  ('WEB-DL Tier 2', 'RTN', 'RTN'),
  ('WEB-DL Tier 2', 'SDCC', 'SDCC'),
  ('WEB-DL Tier 2', 'GNOME', 'GNOME'),
  ('WEB-DL Tier 2', 'SLiGNOME', 'SLiGNOME'),
  ('WEB-DL Tier 2', 'CRUD', 'CRUD'),
  ('WEB-DL Tier 2', 'DRACULA', 'DRACULA'),
  ('WEB-DL Tier 2', 'PHOENiX', 'PHOENiX'),
  ('WEB-DL Tier 2', 'PSiG', 'PSiG'),
  ('WEB-DL Tier 2', 'DEEP', 'DEEP'),
  ('WEB-DL Tier 2', 'orbitron', 'orbitron'),
  ('WEB-DL Tier 2', 'APEX', 'APEX'),
  ('WEB-DL Tier 2', 'BLOOM', 'BLOOM'),
  ('WEB-DL Tier 2', 'ETHiCS', 'ETHiCS'),
  ('WEB-DL Tier 2', 'ViSUM', 'ViSUM'),
  ('WEB-DL Tier 2', 'XEPA', 'XEPA'),
  ('WEB-DL Tier 2', 'MiU', 'MiU'),
  ('WEB-DL Tier 2', 'PEXA', 'PEXA'),
  ('WEB-DL Tier 2', 'Dooky', 'Dooky'),
  ('WEB-DL Tier 2', 'iKA', 'iKA'),
  ('WEB-DL Tier 2', 'KiMCHI', 'KiMCHI'),
  ('WEB-DL Tier 2', 'NYH', 'NYH'),
  ('WEB-DL Tier 2', 'ABBIE', 'ABBIE'),
  ('WEB-DL Tier 2', 'FC', 'FC'),
  ('WEB-DL Tier 2', 'iJP', 'iJP'),
  ('WEB-DL Tier 2', 'PAXA', 'PAXA'),
  ('WEB-DL Tier 2', 'Flights', 'Flights'),
  ('WEB-DL Tier 2', 'T6D', 'T6D'),
  ('WEB-DL Tier 2', 'T4H', 'T4H'),
  ('WEB-DL Tier 2', 'SiC', 'SiC'),
  ('WEB-DL Tier 2', 'CiT', 'CiT'),
  ('WEB-DL Tier 2', 'NINJACENTRAL', 'NINJACENTRAL'),
  ('WEB-DL Tier 2', 'dB', 'dB'),
  ('WEB-DL Tier 2', 'END', 'END'),
  ('WEB-DL Tier 2', 'SwAgLaNdEr', 'SwAgLaNdEr'),
  ('WEB-DL Tier 2', 'iT00NZ', 'iT00NZ'),
  ('WEB-DL Tier 2', 'ROCCaT', 'ROCCaT'),
  ('WEB-DL Tier 2', 'ViSiON', 'ViSiON'),
  ('WEB-DL Tier 2', '3cTWeB', '3cTWeB'),
  ('WEB-DL Tier 2', 'RTFM', 'RTFM'),
  ('WEB-DL Tier 2', 'SPiRiT', 'SPiRiT'),
  ('WEB-DL Tier 2', '4KBEC', '4KBEC'),
  ('WEB-DL Tier 2', 'Coo7', 'Coo7'),
  ('WEB-DL Tier 2', 'WEBDV', 'WEBDV')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 4. QUALITY PROFILE SCORING (PROPER / REPACK LADDER & 4K REMASTER)
-- ============================================================================

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES
  ('Movies 2160p AV1 HQ', 'Repack1', 'radarr', 5),
  ('Movies 2160p AV1 HQ', 'Repack2', 'radarr', 6),
  ('Movies 2160p AV1 HQ', 'Repack3', 'radarr', 7),
  ('Movies 2160p AV1 HQ', '4K Remaster', 'radarr', 25),
  ('Movies 2160p AV1 HQ', 'Audio Description', 'radarr', -10000),
  ('Movies SHADOW Explorer', 'Repack1', 'radarr', 5),
  ('Movies SHADOW Explorer', 'Repack2', 'radarr', 6),
  ('Movies SHADOW Explorer', 'Repack3', 'radarr', 7),
  ('Movies SHADOW Explorer', '4K Remaster', 'radarr', 25),
  ('Movies SHADOW Explorer', 'Audio Description', 'radarr', -10000)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type")
DO UPDATE SET "score" = excluded."score";
