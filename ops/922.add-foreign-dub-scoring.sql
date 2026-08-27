-- @operation: export
-- @entity: batch
-- @name: Add Foreign Dub Scoring
-- @exportedAt: 2026-08-27T09:00:00.000Z
-- @opIds: 28930, 28931, 28932, 28933

-- --- BEGIN op 28930 ( create Foreign Dub regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES (
  'Foreign Dub',
  '(?i)\b(?:(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)|(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)[._ -]+DL|DL[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB))\b',
  'Matches releases with explicit foreign audio dubbed tags'
)
ON CONFLICT DO NOTHING;
-- --- END op 28930

-- --- BEGIN op 28931 ( create Foreign Dub Custom Format )
INSERT INTO "custom_formats" ("name", "description")
VALUES (
  'Foreign Dub',
  'Matches releases with explicit foreign audio dub tags'
)
ON CONFLICT DO NOTHING;

INSERT INTO "custom_format_tags" ("custom_format_name", "tag_name")
VALUES ('Foreign Dub', 'Audio')
ON CONFLICT DO NOTHING;
-- --- END op 28931

-- --- BEGIN op 28932 ( define conditions for Foreign Dub )
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('Foreign Dub', 'Foreign Dub Tag', 'release_title', 'all', 0, 1)
ON CONFLICT DO NOTHING;

INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('Foreign Dub', 'Foreign Dub Tag', 'Foreign Dub')
ON CONFLICT DO NOTHING;
-- --- END op 28932

-- --- BEGIN op 28933 ( assign Foreign Dub score in Movies 2160p AV1 HQ )
INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "score", "arr_type")
VALUES ('Movies 2160p AV1 HQ', 'Foreign Dub', -750, 'radarr')
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type") DO UPDATE SET "score" = -750;
-- --- END op 28933
