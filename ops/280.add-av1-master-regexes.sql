-- @operation: export
-- @entity: batch
-- @name: Add AV1 Master Regular Expressions
-- @exportedAt: 2026-08-24T21:05:00.000Z
-- @opIds: 28001, 28002, 28003, 28004, 28005, 28006, 28007, 28008, 28009, 28010

-- --- BEGIN op 28001 ( upgrade canonical AV1 regex )
UPDATE "regular_expressions" 
SET "pattern" = '(?<![a-z0-9])(AV0?1|SVT[-._]?AV1|libsvtav1|rav1e|AOM[-._]?AV1|AOMedia\s*Video\s*1)(?![a-z0-9])',
    "description" = 'Matches all AV1 codec naming variants (AV1, AV01, SVT-AV1, libsvtav1, rav1e, AOM-AV1, AOMedia Video 1)'
WHERE "name" = 'AV1' AND "pattern" = '\bAV1\b';
-- --- END op 28001

-- --- BEGIN op 28002 ( create 10-bit Depth regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('10-bit Depth', '(?<![a-z0-9])(10[-._]?bit|10b|Hi10P|HDR10\+|HDR10|HDR|DV|DoVi|Dolby[-._]?Vision)(?![a-z0-9])', 'Matches 10-bit color depth markers and HDR/DV layers', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "tags" ("name") VALUES ('Resolution') ON CONFLICT ("name") DO NOTHING;
INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('10-bit Depth', 'Resolution') ON CONFLICT DO NOTHING;
-- --- END op 28002

-- --- BEGIN op 28003 ( create 8-bit Depth regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('8-bit Depth', '(?<![a-z0-9])(8[-._]?bit|8b)(?![a-z0-9])', 'Matches 8-bit color depth markers subject to color banding', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('8-bit Depth', 'Resolution') ON CONFLICT DO NOTHING;
-- --- END op 28003

-- --- BEGIN op 28004 ( create Opus Multi regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('Opus Multi', '(?<![a-z0-9])(Opus|OPUS)[-._ ]?(5\.1|7\.1|6ch|8ch)(?![a-z0-9])', 'Matches multi-channel 5.1 and 7.1 Opus surround audio', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "tags" ("name") VALUES ('Audio') ON CONFLICT ("name") DO NOTHING;
INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('Opus Multi', 'Audio') ON CONFLICT DO NOTHING;
-- --- END op 28004

-- --- BEGIN op 28005 ( create Opus Stereo regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('Opus Stereo', '(?<![a-z0-9])(Opus|OPUS)(?![-._ ]*(?:5\.1|7\.1|6ch|8ch))(?![a-z0-9])', 'Matches 2.0 / stereo Opus audio tracks', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('Opus Stereo', 'Audio') ON CONFLICT DO NOTHING;
-- --- END op 28005

-- --- BEGIN op 28006 ( create AV1 Anime Encoders regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('AV1 Anime Encoders', '^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1)\]', 'Matches verified active AV1 anime release groups with bracket prefix', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "tags" ("name") VALUES ('Release Group') ON CONFLICT ("name") DO NOTHING;
INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('AV1 Anime Encoders', 'Release Group') ON CONFLICT DO NOTHING;
-- --- END op 28006

-- --- BEGIN op 28007 ( create AV1 Compact Encoders regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('AV1 Compact Encoders', '(?:^\[(?:dAV1nci|UnAV1Chain)\]|-(?:dAV1nci|WhiskeyJack|WhiskyJack|UH|edge2020|UnAV1Chain|R[-._ ]and[-._ ]H|\[dAV1nci\]|\[UnAV1Chain\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)', 'Matches verified high-quality AV1 compact encoders anchored to release group position with site tag tolerance', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('AV1 Compact Encoders', 'Release Group') ON CONFLICT DO NOTHING;
-- --- END op 28007

-- --- BEGIN op 28008 ( create AV1 Storage Savers regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('AV1 Storage Savers', '(?:^\[(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART)\]|-(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)', 'Matches verified AV1 micro-encoders for maximum storage efficiency', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('AV1 Storage Savers', 'Release Group') ON CONFLICT DO NOTHING;
-- --- END op 28008

-- --- BEGIN op 28009 ( create Legacy x265 Codec regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('Legacy x265 Codec', '(?<![a-z0-9])([xh][-._ ]?265|HEVC)(?![a-z0-9])', 'Matches non-AV1 HEVC / x265 releases for isolation and negative penalty scoring', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "tags" ("name") VALUES ('Codec') ON CONFLICT ("name") DO NOTHING;
INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('Legacy x265 Codec', 'Codec') ON CONFLICT DO NOTHING;
-- --- END op 28009

-- --- BEGIN op 28010 ( create Legacy x264 Codec regex )
INSERT INTO "regular_expressions" ("name", "pattern", "description", "regex101_id")
VALUES ('Legacy x264 Codec', '(?<![a-z0-9])([xh][-._ ]?264|AVC)(?![a-z0-9])', 'Matches non-AV1 AVC / x264 releases for hard rejection penalty scoring', NULL)
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expression_tags" ("regular_expression_name", "tag_name") VALUES ('Legacy x264 Codec', 'Codec') ON CONFLICT DO NOTHING;
-- --- END op 28010
