-- @operation: export
-- @entity: batch
-- @name: Add Graduated Oversized Fallback Scoring
-- @exportedAt: 2026-08-26T16:50:00.000Z
-- @opIds: 28911, 28912, 28913

-- --- BEGIN op 28911 ( create Heavy 2160p Fallback CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Heavy 2160p Fallback', 'Matches heavy non-AV1 2160p releases between 25 GB and 30 GB')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Heavy 2160p Fallback', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Heavy 2160p Fallback', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('Heavy 2160p Fallback', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Heavy 2160p Fallback', 'Heavy Size', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes)
VALUES ('Heavy 2160p Fallback', 'Heavy Size', 26843545600, 32212254720)
ON CONFLICT DO UPDATE SET "min_bytes" = 26843545600, "max_bytes" = 32212254720;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Heavy 2160p Fallback', 'Not AV1 Marker', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Heavy 2160p Fallback', 'Not AV1 Marker', 'AV1')
ON CONFLICT DO NOTHING;
-- --- END op 28911

-- --- BEGIN op 28912 ( update Oversized 2160p Fallback size window to 30-200 GB )
UPDATE condition_sizes
SET min_bytes = 32212254720, max_bytes = 214748364800
WHERE custom_format_name = 'Oversized 2160p Fallback' AND condition_name = 'Oversized Size';
-- --- END op 28912

-- --- BEGIN op 28913 ( assign Heavy 2160p Fallback score in Movies 2160p AV1 HQ )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Heavy 2160p Fallback', -400, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -400;
-- --- END op 28913
