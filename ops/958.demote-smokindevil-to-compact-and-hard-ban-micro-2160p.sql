-- =============================================================================
-- Migration: 958.demote-smokindevil-to-compact-and-hard-ban-micro-2160p.sql
-- Description: Demote Smokindevil from AV1 Quality Encoders (+1000) to AV1
--              Compact Encoders (+500), hard-ban AV1 Micro 2160p releases
--              (1.0 - 6.0 GB) with -10000 rejection penalty, and calibrate
--              AV1 Lean 2160p (6.0 - 11.0 GB) to -3800 so high-bitrate 14-30 GB
--              x265 releases strictly beat lean micro-encodes.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 95801
-- 1. Update 'AV1 Quality Encoders' Regex (Remove Smokindevil)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:CoSMiCSuRFeR|PRL|CHD|CHOPPERHITLER|ChopperHitler|TAoE|dAV1nci|UH)\]|-(?:CoSMiCSuRFeR|PRL|CHD|CHOPPERHITLER|ChopperHitler|TAoE|dAV1nci|UH|\[(?:CoSMiCSuRFeR|PRL|CHD|CHOPPERHITLER|ChopperHitler|TAoE|dAV1nci|UH)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE name = 'AV1 Quality Encoders';

-- 2. Update 'AV1 Compact Encoders' Regex (Add Smokindevil / SmokinDevil)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|Smokindevil|SmokinDevil)\]|-(?:WhiskeyJack|WhiskyJack|edge2020|UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|Smokindevil|SmokinDevil|\[(?:UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|Smokindevil|SmokinDevil)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)'
WHERE name = 'AV1 Compact Encoders';

-- 3. Hard-ban 'AV1 Micro 2160p' in Movies 2160p AV1 HQ (-10000 rejection penalty)
UPDATE quality_profile_custom_formats
SET score = -10000
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'AV1 Micro 2160p';

-- 4. Set 'AV1 Lean 2160p' penalty to -3800 in Movies 2160p AV1 HQ
UPDATE quality_profile_custom_formats
SET score = -3800
WHERE quality_profile_name = 'Movies 2160p AV1 HQ' AND custom_format_name = 'AV1 Lean 2160p';
-- --- END op 95801
