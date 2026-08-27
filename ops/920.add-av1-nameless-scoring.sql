-- @operation: export
-- @entity: batch
-- @name: Add AV1 Nameless Trust Scoring
-- @exportedAt: 2026-08-27T08:00:00.000Z
-- @opIds: 28920, 28921, 28922, 28923

-- --- BEGIN op 28920 ( create Plausible Release Group regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES (
  'Plausible Release Group',
  '(?i)(?:^\[[A-Za-z0-9._ -]+\]|-(?:\s*\[(?!(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\])[A-Za-z0-9_.-]+\]|(?!(?:NL[- .]?sub|NL|DUTCH|GERMAN|FRENCH|ITA|SPANISH|SWE|DK|NOR|Fi|xpost|AV1|AV01|HEVC|x265|x264|HDR|DV|10bit|8bit|BRRip|BDRip|WEB[- .]?DL|WEBRip|BluRay|UHD|2160p|1080p|720p|AAC|DDP|AC3|TrueHD|Atmos|DTS|DTS-HD|Opus)(?:[\[\].\s-]|$)|\s*(?:NL[- .]?sub|NL|DUTCH|GERMAN|FRENCH|ITA|SPANISH|SWE|DK|NOR|Fi|xpost|AV1|AV01)(?:[\[\].\s-]|$)|\[(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\])\s*[A-Za-z0-9_&]+(?:[-. ][A-Za-z0-9_&]+)*(?:\[[a-zA-Z0-9_.-]+\])?)(?:\.[a-zA-Z0-9]{2,4})?$)',
  'Matches releases that carry a recognized or plausible release group prefix or suffix'
)
ON CONFLICT DO NOTHING;
-- --- END op 28920

-- --- BEGIN op 28921 ( create AV1 Nameless Custom Format )
INSERT INTO "custom_formats" ("name", "description")
VALUES (
  'AV1 Nameless',
  'Matches 2160p AV1 releases without a recognized or plausible release group suffix'
)
ON CONFLICT DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name")
VALUES ('AV1 Nameless', 'Resolution')
ON CONFLICT DO NOTHING;
-- --- END op 28921

-- --- BEGIN op 28922 ( define conditions for AV1 Nameless )
-- Condition 1: 2160p Resolution (required, not negated)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Nameless', '2160p Resolution', 'resolution', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution)
VALUES ('AV1 Nameless', '2160p Resolution', '2160p')
ON CONFLICT DO NOTHING;

-- Condition 2: AV1 Codec Marker (required, not negated)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Nameless', 'AV1 Codec', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Nameless', 'AV1 Codec', 'AV1')
ON CONFLICT DO NOTHING;

-- Condition 3: Negated Plausible Group (required, negated: fires when title lacks group)
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('AV1 Nameless', 'Has Plausible Group', 'release_title', 'all', 1, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('AV1 Nameless', 'Has Plausible Group', 'Plausible Release Group')
ON CONFLICT DO NOTHING;
-- --- END op 28922

-- --- BEGIN op 28923 ( assign AV1 Nameless score in Movies 2160p AV1 HQ )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'AV1 Nameless', -2500, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -2500;
-- --- END op 28923
