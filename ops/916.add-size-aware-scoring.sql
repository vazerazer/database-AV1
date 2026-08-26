-- @operation: export
-- @entity: batch
-- @name: Add Size-Aware Scoring Custom Formats
-- @exportedAt: 2026-08-26T16:25:00.000Z
-- @opIds: 28901, 28902, 28903, 28904

-- --- BEGIN op 28901 ( create AV1 Micro 1080p CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('AV1 Micro 1080p', 'Matches low-bitrate micro-AV1 1080p releases between 1 GB and 3.5 GB')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('AV1 Micro 1080p', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Micro 1080p', '1080p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('AV1 Micro 1080p', '1080p Resolution', '1080p')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Micro 1080p', 'AV1 Marker', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Micro 1080p', 'AV1 Marker', 'AV1')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Micro 1080p', 'Micro 1080p Size', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes)
VALUES ('AV1 Micro 1080p', 'Micro 1080p Size', 1073741824, 3758096384)
ON CONFLICT DO NOTHING;
-- --- END op 28901

-- --- BEGIN op 28902 ( create AV1 Micro 2160p CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('AV1 Micro 2160p', 'Matches absurdly small micro-AV1 2160p releases between 1 GB and 4 GB')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('AV1 Micro 2160p', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Micro 2160p', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('AV1 Micro 2160p', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Micro 2160p', 'AV1 Marker', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Micro 2160p', 'AV1 Marker', 'AV1')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Micro 2160p', 'Micro 2160p Size', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes)
VALUES ('AV1 Micro 2160p', 'Micro 2160p Size', 1073741824, 4294967296)
ON CONFLICT DO NOTHING;
-- --- END op 28902

-- --- BEGIN op 28903 ( create Oversized 2160p Fallback CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Oversized 2160p Fallback', 'Matches oversized non-AV1 2160p releases over 16 GB')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Oversized 2160p Fallback', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Oversized 2160p Fallback', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('Oversized 2160p Fallback', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Oversized 2160p Fallback', 'Oversized Size', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes)
VALUES ('Oversized 2160p Fallback', 'Oversized Size', 17179869184, 214748364800)
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Oversized 2160p Fallback', 'Not AV1 Marker', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Oversized 2160p Fallback', 'Not AV1 Marker', 'AV1')
ON CONFLICT DO NOTHING;
-- --- END op 28903

-- --- BEGIN op 28904 ( Assign Size-Aware Scores to Movies 2160p AV1 HQ )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'AV1 Micro 1080p', -2800, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -2800;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'AV1 Micro 2160p', -2800, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -2800;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Oversized 2160p Fallback', -1500, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -1500;
-- --- END op 28904
