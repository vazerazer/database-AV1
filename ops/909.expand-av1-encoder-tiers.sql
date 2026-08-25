-- =============================================================================
-- Migration: 909.expand-av1-encoder-tiers.sql
-- Description: Expand AV1 Quality, Compact, Storage, and Anime encoder tiers
--              based on real multi-indexer telemetry (~500 AV1 entries),
--              harden CAM regex to catch all TC/TS/Screener releases, and ban ENTROPY.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 90901
-- 1. Update 'AV1 Quality Encoders' Regex (Waldek, PRL, CHD, CHOPPERHITLER, TAoE, CoSMiCSuRFeR)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:CoSMiCSuRFeR|Waldek|PRL|CHD|CHOPPERHITLER|TAoE)\]|-(?:CoSMiCSuRFeR|Waldek|PRL|CHD|CHOPPERHITLER|TAoE|\[CoSMiCSuRFeR\]|\[Waldek\]|\[PRL\]|\[CHD\]|\[CHOPPERHITLER\]|\[TAoE\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)'
WHERE name = 'AV1 Quality Encoders';

-- 2. Update 'AV1 Compact Encoders' Regex (LAZARUS, DKV, TiZU, Saon, onlyfaffs, KIMJI, heTOrico, Rosy, anomoomin, CMCT, GRiMM, Dust, DIN, GanG)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:dAV1nci|UnAV1Chain|RAV1NE|UserHEVC|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG)\]|-(?:dAV1nci|WhiskeyJack|WhiskyJack|UH|edge2020|UnAV1Chain|Smokindevil|SmokinDevil|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|\[dAV1nci\]|\[UnAV1Chain\]|\[RAV1NE\]|\[UserHEVC\]|\[LAZARUS\]|\[DKV\]|\[TiZU\]|\[Saon\]|\[onlyfaffs\]|\[KIMJI\]|\[heTOrico\]|\[Rosy\]|\[anomoomin\]|\[CMCT\]|\[GRiMM\]|\[Dust\]|\[DIN\]|\[GanG\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)'
WHERE name = 'AV1 Compact Encoders';

-- 3. Update 'AV1 Storage Savers' Regex (LUCY, DKong, Rapta, GubrakZ, Retr0, SWAXXON, FELIX12345)
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART|LUCY|DKong|Rapta|GubrakZ|Retr0|SWAXXON|FELIX12345)\]|-(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART|LUCY|DKong|Rapta|GubrakZ|Retr0|SWAXXON|FELIX12345|\[PSA\]|\[GalaxyRG\]|\[MeGusta\]|\[VXT\]|\[d3g\]|\[Ghost\]|\[rartv\]|\[ELiTE\]|\[LAMA\]|\[KaKa\]|\[YAWNTIC\]|\[BONE\]|\[GZ\]|\[CART\]|\[LUCY\]|\[DKong\]|\[Rapta\]|\[GubrakZ\]|\[Retr0\]|\[SWAXXON\]|\[FELIX12345\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)'
WHERE name = 'AV1 Storage Savers';

-- 4. Update 'AV1 Anime Encoders' Regex (Valenciano)
UPDATE regular_expressions
SET pattern = '(?i)^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1|Ironclad|Valenciano)\]'
WHERE name = 'AV1 Anime Encoders';

-- 5. Harden CAM Regex (catch TC, TS, Telesync, Screener with word boundaries)
UPDATE regular_expressions
SET pattern = '(?i)(?<=\b[12]\d{3}\b).*?\b(?:(AC3)?(LD|MD)|CAM[ ._-]?(?:Rip)?|DCP(?:RIP)?|DVD[ ._-]?(?:SCR(?:EENER)?)|HD[ ._-]?(?:CAM|SCR|TC|TS)|(?:LINE|MIC)[ ._-]?DUBBED|SCREENER|(?:TC|TS)(?:Rip)?|TELE(?:CINE|SYNC)|WORKPRINT)\b'
WHERE name = 'CAM';

-- 6. Ban Fake/Corrupted Group ENTROPY
INSERT INTO regular_expressions (name, pattern, description)
VALUES (
  'ENTROPY',
  '(?<![a-zA-Z0-9])ENTROPY\b',
  'Banned fake/corrupt release group ENTROPY'
) ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES (
  'Banned Groups',
  'ENTROPY',
  'release_group',
  'all',
  0,
  0
) ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES (
  'Banned Groups',
  'ENTROPY',
  'ENTROPY'
) ON CONFLICT DO NOTHING;
-- --- END op 90901
