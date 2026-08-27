-- =============================================================================
-- Migration: 925.census-driven-tier-expansion.sql
-- Description: Census-driven tier expansion and alias consolidation.
--              Promotes dAV1nci, UH, and Smokindevil to AV1 Quality Encoders (+1000).
--              Adds Toasty to AV1 Compact Encoders (+500).
--              Consolidates R&H alias family (R&H, RandH, R and H, RH, extension artifacts).
--              Expands PRL Waldek matching to handle dot and space variants.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 92501
-- 1. Update 'AV1 Quality Encoders' Regex
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil)\]|-(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil|\[(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)'
WHERE name = 'AV1 Quality Encoders';

-- 2. Update 'AV1 Compact Encoders' Regex
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH)\]|-(?:WhiskeyJack|WhiskyJack|edge2020|UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|\[(?:UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)'
WHERE name = 'AV1 Compact Encoders';
-- --- END op 92501
