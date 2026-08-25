-- --- BEGIN op 90301 ( create Not AV1 CF )
INSERT INTO "custom_formats" ("name", "description")
VALUES ('Not AV1', 'Matches releases that do not contain canonical AV1 naming tokens')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name")
VALUES ('Not AV1', 'Codec')
ON CONFLICT DO NOTHING;

INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Not AV1', 'Not AV1', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Not AV1', 'Not AV1', 'AV1')
ON CONFLICT DO NOTHING;
-- --- END op 90301
