-- @operation: export
-- @entity: batch
-- @name: Add AV1 Master Custom Formats
-- @exportedAt: 2026-08-24T21:06:00.000Z
-- @opIds: 28101, 28102, 28103, 28104, 28105, 28106, 28107, 28108, 28109

-- --- BEGIN op 28101 ( create 10-bit Depth CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('10-bit Depth', 'Matches 10-bit color depth and HDR/DV encoded releases')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('10-bit Depth', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('10-bit Depth', '10-bit Depth', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('10-bit Depth', '10-bit Depth', '10-bit Depth')
ON CONFLICT DO NOTHING;
-- --- END op 28101

-- --- BEGIN op 28102 ( create 8-bit Depth CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('8-bit Depth', 'Matches 8-bit color depth releases subject to banding artifacts')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('8-bit Depth', 'Resolution') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('8-bit Depth', '8-bit Depth', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('8-bit Depth', '8-bit Depth', '8-bit Depth')
ON CONFLICT DO NOTHING;
-- --- END op 28102

-- --- BEGIN op 28103 ( create Opus 5.1 / 7.1 CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Opus 5.1 / 7.1', 'Matches multi-channel 5.1 and 7.1 Opus surround audio')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Opus 5.1 / 7.1', 'Audio') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Opus 5.1 / 7.1', 'Opus Multi', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Opus 5.1 / 7.1', 'Opus Multi', 'Opus Multi')
ON CONFLICT DO NOTHING;
-- --- END op 28103

-- --- BEGIN op 28104 ( create Opus Stereo CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Opus Stereo', 'Matches 2.0 / stereo Opus audio tracks')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Opus Stereo', 'Audio') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Opus Stereo', 'Opus Stereo', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Opus Stereo', 'Opus Stereo', 'Opus Stereo')
ON CONFLICT DO NOTHING;
-- --- END op 28104

-- --- BEGIN op 28105 ( create AV1 Anime Encoders CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('AV1 Anime Encoders', 'Matches verified active AV1 anime release groups')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('AV1 Anime Encoders', 'Release Group') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Anime Encoders', 'AV1 Anime Encoders', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Anime Encoders', 'AV1 Anime Encoders', 'AV1 Anime Encoders')
ON CONFLICT DO NOTHING;
-- --- END op 28105

-- --- BEGIN op 28106 ( create AV1 Compact Encoders CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('AV1 Compact Encoders', 'Matches verified high-quality AV1 compact encoders')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('AV1 Compact Encoders', 'Release Group') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Compact Encoders', 'AV1 Compact Encoders', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Compact Encoders', 'AV1 Compact Encoders', 'AV1 Compact Encoders')
ON CONFLICT DO NOTHING;
-- --- END op 28106

-- --- BEGIN op 28107 ( create AV1 Storage Savers CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('AV1 Storage Savers', 'Matches verified AV1 micro-encoders for storage optimization')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('AV1 Storage Savers', 'Release Group') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Storage Savers', 'AV1 Storage Savers', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Storage Savers', 'AV1 Storage Savers', 'AV1 Storage Savers')
ON CONFLICT DO NOTHING;
-- --- END op 28107

-- --- BEGIN op 28108 ( create Legacy x265 Codec CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Legacy x265 Codec', 'Matches non-AV1 x265/HEVC releases for negative scoring and upgrade isolation')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Legacy x265 Codec', 'Codec') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Legacy x265 Codec', 'Legacy x265 Codec', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Legacy x265 Codec', 'Legacy x265 Codec', 'Legacy x265 Codec')
ON CONFLICT DO NOTHING;
-- --- END op 28108

-- --- BEGIN op 28109 ( create Legacy x264 Codec CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Legacy x264 Codec', 'Matches non-AV1 x264/AVC releases for hard rejection scoring')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name") VALUES ('Legacy x264 Codec', 'Codec') ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Legacy x264 Codec', 'Legacy x264 Codec', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Legacy x264 Codec', 'Legacy x264 Codec', 'Legacy x264 Codec')
ON CONFLICT DO NOTHING;
-- --- END op 28109
