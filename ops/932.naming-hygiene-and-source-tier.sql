-- @operation: export
-- @entity: batch
-- @name: Op 932 Naming Hygiene and Source Tier Policy
-- @exportedAt: 2026-08-27T17:50:00.000Z
-- @opIds: 28935, 28936, 28937

-- ============================================================================
-- 1. REGULAR EXPRESSIONS (Tolerate Trailing Dupe Markers _1, _2, _3, -xpost)
-- ============================================================================

UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^|[\s._-])(?:CtrlHD|GRiM|PiRaTeS|BHDStudio|TAoE|DON|EbP|playHD|Z0N3|LoRD|MrTentsaw)(?:\[[^\]]*\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$'
WHERE "name" = 'LEGACY_TRUSTED_X264';

UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH)\]|-(?:WhiskeyJack|WhiskyJack|edge2020|UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|\[(?:UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE "name" = 'AV1 Compact Encoders';

UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^\[(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil)\]|-(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil|\[(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE "name" = 'AV1 Quality Encoders';

-- ============================================================================
-- 2. EXPAND WEB-DL TIER 2 WITH LEGACY GROUPS
-- ============================================================================

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES 
  ('WEB-DL Tier 2', 'PiRaTeS', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'Z0N3', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'playHD', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'GRiM', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'MrTentsaw', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'CtrlHD', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'BHDStudio', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'DON', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'EbP', 'release_group', 'all', 0, 0),
  ('WEB-DL Tier 2', 'LoRD', 'release_group', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES 
  ('WEB-DL Tier 2', 'PiRaTeS', 'PiRaTeS'),
  ('WEB-DL Tier 2', 'Z0N3', 'Z0N3'),
  ('WEB-DL Tier 2', 'playHD', 'playHD'),
  ('WEB-DL Tier 2', 'GRiM', 'GRiM'),
  ('WEB-DL Tier 2', 'MrTentsaw', 'MrTentsaw'),
  ('WEB-DL Tier 2', 'CtrlHD', 'CtrlHD'),
  ('WEB-DL Tier 2', 'BHDStudio', 'BHDStudio'),
  ('WEB-DL Tier 2', 'DON', 'DON'),
  ('WEB-DL Tier 2', 'EbP', 'EbP'),
  ('WEB-DL Tier 2', 'LoRD', 'LoRD')
ON CONFLICT DO NOTHING;
