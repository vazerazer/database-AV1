-- @operation: export
-- @entity: batch
-- @name: Add AV1 Lean Band Scoring
-- @exportedAt: 2026-08-27T08:30:00.000Z
-- @opIds: 28925, 28926, 28927, 28928

-- --- BEGIN op 28925 ( create AV1 Lean 2160p Custom Format )
INSERT INTO "custom_formats" ("name", "description")
VALUES (
  'AV1 Lean 2160p',
  'Matches lean 2160p AV1 releases between 6 GB and 11 GB that fall below the perceptual bitrate floor'
)
ON CONFLICT DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name")
VALUES ('AV1 Lean 2160p', 'Resolution')
ON CONFLICT DO NOTHING;
-- --- END op 28925

-- --- BEGIN op 28926 ( define conditions for AV1 Lean 2160p )
-- Condition 1: 2160p Resolution (required, not negated)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Lean 2160p', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('AV1 Lean 2160p', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

-- Condition 2: AV1 Codec Marker (required, not negated)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Lean 2160p', 'AV1 Codec', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Lean 2160p', 'AV1 Codec', 'AV1')
ON CONFLICT DO NOTHING;

-- Condition 3: Lean Size 6.0 - 11.0 GB (required, not negated)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Lean 2160p', 'Lean 2160p Size', 'size', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes)
VALUES ('AV1 Lean 2160p', 'Lean 2160p Size', 6442450945, 11811160064)
ON CONFLICT DO UPDATE SET "min_bytes" = 6442450945, "max_bytes" = 11811160064;
-- --- END op 28926

-- --- BEGIN op 28927 ( assign AV1 Lean 2160p score in Movies 2160p AV1 HQ )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'AV1 Lean 2160p', -3400, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -3400;
-- --- END op 28927
