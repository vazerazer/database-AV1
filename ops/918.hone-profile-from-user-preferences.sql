-- @operation: export
-- @entity: batch
-- @name: Hone Profile From User Preference Map
-- @exportedAt: 2026-08-26T17:28:00.000Z
-- @opIds: 28921, 28922, 28923, 28924

-- --- BEGIN op 28921 ( retune audio scores in Movies 2160p AV1 HQ for Yamaha 3.1 chain )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Dolby Atmos', 150, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 150;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'TrueHD', 150, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 150;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'DTS-X', 150, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 150;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Lossless Audio', 100, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 100;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Dolby Digital', 100, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 100;

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Dolby Digital +', 150, 'all')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = 150;
-- --- END op 28921

-- --- BEGIN op 28922 ( update AV1 Micro 2160p window to 1-6 GB )
UPDATE condition_sizes
SET min_bytes = 1073741824, max_bytes = 6442450944
WHERE custom_format_name = 'AV1 Micro 2160p' AND condition_name = 'Micro 2160p Size';
-- --- END op 28922

-- --- BEGIN op 28923 ( create Extreme 2160p CF: 45-200 GB all codecs )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Extreme 2160p', 'Matches extreme oversized 2160p releases over 45 GB across all codecs')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Extreme 2160p', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Extreme 2160p', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('Extreme 2160p', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Extreme 2160p', 'Extreme Size', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes)
VALUES ('Extreme 2160p', 'Extreme Size', 48318382080, 214748364800)
ON CONFLICT DO UPDATE SET "min_bytes" = 48318382080, "max_bytes" = 214748364800;
-- --- END op 28923

-- --- BEGIN op 28924 ( assign Extreme 2160p score in Movies 2160p AV1 HQ )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Extreme 2160p', -1500, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -1500;
-- --- END op 28924
