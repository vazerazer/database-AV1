-- @operation: export
-- @entity: batch
-- @name: Op 933 Vetted Group Union and Sync Ownership Gate
-- @exportedAt: 2026-08-27T18:32:00.000Z
-- @opIds: 28938, 28939, 28940

-- ============================================================================
-- 1. LEGACY TRUSTED X264 REGEX (Vetted Union of HD Bluray Tier 01-03)
-- ============================================================================

UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^|[\s._-])(?:CtrlHD|GRiM|PiRaTeS|BHDStudio|TAoE|DON|EbP|playHD|Z0N3|LoRD|MrTentsaw|ATELiER|BBQ|BMF|c0kE|Chotab|CRiSC|D-Z0N3|Dariush|decibeL|EDPH|Geek|LolHD|NCmt|PTer|TayTO|TDD|TnP|VietHD|ZQ|ZoroSenpai|NTb|EA|HiDt|HiSD|iFT|QOQ|SA89|sbR|hallowed|HiFi|SPHD|W4NK3R)(?:\[[^\]]*\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$'
WHERE "name" = 'LEGACY_TRUSTED_X264';

-- ============================================================================
-- 2. EXPAND 1080P QUALITY TIER 2 WITH NEWLY UNIONED VETTED GROUPS
-- ============================================================================

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('ATELiER', '(?<=^|[\s.-])ATELiER\b', 'Vetted reference group ATELiER'),
  ('BBQ', '(?<=^|[\s.-])BBQ\b', 'Vetted reference group BBQ'),
  ('BMF', '(?<=^|[\s.-])BMF\b', 'Vetted reference group BMF'),
  ('c0kE', '(?<=^|[\s.-])c0kE\b', 'Vetted reference group c0kE'),
  ('Chotab', '(?<=^|[\s.-])Chotab\b', 'Vetted reference group Chotab'),
  ('CRiSC', '(?<=^|[\s.-])CRiSC\b', 'Vetted reference group CRiSC'),
  ('Dariush', '(?<=^|[\s.-])Dariush\b', 'Vetted reference group Dariush'),
  ('decibeL', '(?<=^|[\s.-])decibeL\b', 'Vetted reference group decibeL'),
  ('Geek', '(?<=^|[\s.-])Geek\b', 'Vetted reference group Geek'),
  ('LolHD', '(?<=^|[\s.-])LolHD\b', 'Vetted reference group LolHD'),
  ('NCmt', '(?<=^|[\s.-])NCmt\b', 'Vetted reference group NCmt'),
  ('PTer', '(?<=^|[\s.-])PTer\b', 'Vetted reference group PTer'),
  ('TayTO', '(?<=^|[\s.-])TayTO\b', 'Vetted reference group TayTO'),
  ('TDD', '(?<=^|[\s.-])TDD\b', 'Vetted reference group TDD'),
  ('TnP', '(?<=^|[\s.-])TnP\b', 'Vetted reference group TnP'),
  ('VietHD', '(?<=^|[\s.-])VietHD\b', 'Vetted reference group VietHD'),
  ('ZQ', '(?<=^|[\s.-])ZQ\b', 'Vetted reference group ZQ'),
  ('ZoroSenpai', '(?<=^|[\s.-])ZoroSenpai\b', 'Vetted reference group ZoroSenpai'),
  ('NTb', '(?<=^|[\s.-])NTb\b', 'Vetted reference group NTb'),
  ('EA', '(?<=^|[\s.-])EA\b', 'Vetted reference group EA'),
  ('HiSD', '(?<=^|[\s.-])HiSD\b', 'Vetted reference group HiSD'),
  ('QOQ', '(?<=^|[\s.-])QOQ\b', 'Vetted reference group QOQ'),
  ('SA89', '(?<=^|[\s.-])SA89\b', 'Vetted reference group SA89'),
  ('sbR', '(?<=^|[\s.-])sbR\b', 'Vetted reference group sbR'),
  ('HiFi', '(?<=^|[\s.-])HiFi\b', 'Vetted reference group HiFi'),
  ('SPHD', '(?<=^|[\s.-])SPHD\b', 'Vetted reference group SPHD'),
  ('W4NK3R', '(?<=^|[\s.-])W4NK3R\b', 'Vetted reference group W4NK3R')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('1080p Quality Tier 2', 'ATELiER', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'BBQ', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'BMF', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'c0kE', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'Chotab', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'CRiSC', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'Dariush', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'decibeL', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'Geek', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'LolHD', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'NCmt', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'PTer', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'TayTO', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'TDD', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'TnP', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'VietHD', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'ZQ', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'NTb', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'EA', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'HiSD', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'QOQ', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'sbR', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'HiFi', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'SPHD', 'release_group', 'all', 0, 0),
  ('1080p Quality Tier 2', 'W4NK3R', 'release_group', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('1080p Quality Tier 2', 'ATELiER', 'ATELiER'),
  ('1080p Quality Tier 2', 'BBQ', 'BBQ'),
  ('1080p Quality Tier 2', 'BMF', 'BMF'),
  ('1080p Quality Tier 2', 'c0kE', 'c0kE'),
  ('1080p Quality Tier 2', 'Chotab', 'Chotab'),
  ('1080p Quality Tier 2', 'CRiSC', 'CRiSC'),
  ('1080p Quality Tier 2', 'Dariush', 'Dariush'),
  ('1080p Quality Tier 2', 'decibeL', 'decibeL'),
  ('1080p Quality Tier 2', 'Geek', 'Geek'),
  ('1080p Quality Tier 2', 'LolHD', 'LolHD'),
  ('1080p Quality Tier 2', 'NCmt', 'NCmt'),
  ('1080p Quality Tier 2', 'PTer', 'PTer'),
  ('1080p Quality Tier 2', 'TayTO', 'TayTO'),
  ('1080p Quality Tier 2', 'TDD', 'TDD'),
  ('1080p Quality Tier 2', 'TnP', 'TnP'),
  ('1080p Quality Tier 2', 'VietHD', 'VietHD'),
  ('1080p Quality Tier 2', 'ZQ', 'ZQ'),
  ('1080p Quality Tier 2', 'NTb', 'NTb'),
  ('1080p Quality Tier 2', 'EA', 'EA'),
  ('1080p Quality Tier 2', 'HiSD', 'HiSD'),
  ('1080p Quality Tier 2', 'QOQ', 'QOQ'),
  ('1080p Quality Tier 2', 'sbR', 'sbR'),
  ('1080p Quality Tier 2', 'HiFi', 'HiFi'),
  ('1080p Quality Tier 2', 'SPHD', 'SPHD'),
  ('1080p Quality Tier 2', 'W4NK3R', 'W4NK3R')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 3. EXPAND WEB-DL TIER 2 WITH NEWLY UNIONED VETTED GROUPS
-- ============================================================================

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('WEB-DL Tier 2', 'ATELiER', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'c0kE', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'Chotab', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'NCmt', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'PTer', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'TDD', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'TnP', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'VietHD', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'NTb', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SA89', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'SPHD', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'W4NK3R', 'release_group', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('WEB-DL Tier 2', 'ATELiER', 'ATELiER'),
  ('WEB-DL Tier 2', 'c0kE', 'c0kE'),
  ('WEB-DL Tier 2', 'Chotab', 'Chotab'),
  ('WEB-DL Tier 2', 'NCmt', 'NCmt'),
  ('WEB-DL Tier 2', 'PTer', 'PTer'),
  ('WEB-DL Tier 2', 'TDD', 'TDD'),
  ('WEB-DL Tier 2', 'TnP', 'TnP'),
  ('WEB-DL Tier 2', 'VietHD', 'VietHD'),
  ('WEB-DL Tier 2', 'NTb', 'NTb'),
  ('WEB-DL Tier 2', 'SA89', 'SA89'),
  ('WEB-DL Tier 2', 'SPHD', 'SPHD'),
  ('WEB-DL Tier 2', 'W4NK3R', 'W4NK3R')
ON CONFLICT DO NOTHING;
