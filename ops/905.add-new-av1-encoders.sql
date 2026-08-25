-- =============================================================================
-- Migration: 905.add-new-av1-encoders.sql
-- Description: Update AV1 Compact Encoders (R&H ampersand variant, Smokindevil,
--              UserHEVC, RAV1NE) and AV1 Anime Encoders (Ironclad)
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 90501
-- Update AV1 Compact Encoders regular expression pattern
UPDATE regular_expressions
SET pattern = '(?i)(?:^\[(?:dAV1nci|UnAV1Chain|RAV1NE|UserHEVC)\]|-(?:dAV1nci|WhiskeyJack|WhiskyJack|UH|edge2020|UnAV1Chain|Smokindevil|SmokinDevil|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|\[dAV1nci\]|\[UnAV1Chain\]|\[RAV1NE\]|\[UserHEVC\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)'
WHERE name = 'AV1 Compact Encoders';

-- Update AV1 Anime Encoders regular expression pattern
UPDATE regular_expressions
SET pattern = '(?i)^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1|Ironclad)\]'
WHERE name = 'AV1 Anime Encoders';
-- --- END op 90501
