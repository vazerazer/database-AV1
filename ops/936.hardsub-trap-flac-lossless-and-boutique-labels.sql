-- @operation: export
-- @entity: batch
-- @name: Op 936 Hardsub Trap FLAC Lossless and Boutique Labels
-- @exportedAt: 2026-08-28T12:05:00.000Z
-- @opIds: 30945, 30946, 30947

-- ============================================================================
-- 1. ADD FLAC TO LOSSLESS AUDIO (+100 PTS)
-- ============================================================================

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('FLAC', '\b(FLAC)\b', 'Free Lossless Audio Codec')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('Lossless Audio', 'FLAC', 'release_title', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('Lossless Audio', 'FLAC', 'FLAC')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 2. HARDCODED SUBTITLES REJECT (-10000 PTS)
-- ============================================================================

INSERT INTO "custom_formats" ("name", "description")
VALUES ('Hardcoded Subtitles', 'Rejects releases with hardcoded / burned-in foreign subtitles (-10000 pts)')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('HARDSUB_REJECT', '(?i)\b(KORSUB|HARDSUB(BED)?|HC|HDCAM[ ._-]?SUBBED|SUBBED(?=[\W_]+(?:1080p|2160p|720p|WEB|BluRay)))\b', 'Hardcoded or burned-in foreign subtitle tags')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('Hardcoded Subtitles', 'Hardcoded Subtitles', 'release_title', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('Hardcoded Subtitles', 'Hardcoded Subtitles', 'HARDSUB_REJECT')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 3. BOUTIQUE RESTORATION LABELS (+50 PTS)
-- ============================================================================

INSERT INTO "custom_formats" ("name", "description")
VALUES ('Boutique Label', 'Boutique restoration labels (Criterion, Arrow Video, Kino Lorber, Shout Factory, Masters of Cinema) (+50 pts)')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "regular_expressions" ("name", "pattern", "description")
VALUES
  ('BOUTIQUE_LABEL', '\b(Criterion([ ._-]?Collection)?|Arrow[ ._-]?Video|Kino[ ._-]?Lorber|Shout[ ._-]?Factory|Masters[ ._-]?of[ ._-]?Cinema)\b', 'Boutique film restoration labels')
ON CONFLICT ("name") DO NOTHING;

INSERT INTO "custom_format_conditions" ("custom_format_name", "name", "type", "arr_type", "negate", "required")
VALUES
  ('Boutique Label', 'Boutique Label', 'release_title', 'all', 0, 0)
ON CONFLICT DO NOTHING;

INSERT INTO "condition_patterns" ("custom_format_name", "condition_name", "regular_expression_name")
VALUES
  ('Boutique Label', 'Boutique Label', 'BOUTIQUE_LABEL')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 4. QUALITY PROFILE SCORING
-- ============================================================================

INSERT INTO "quality_profile_custom_formats" ("quality_profile_name", "custom_format_name", "arr_type", "score")
VALUES
  ('Movies 2160p AV1 HQ', 'Hardcoded Subtitles', 'radarr', -10000),
  ('Movies 2160p AV1 HQ', 'Boutique Label', 'radarr', 50),
  ('Movies SHADOW Explorer', 'Hardcoded Subtitles', 'radarr', -10000),
  ('Movies SHADOW Explorer', 'Boutique Label', 'radarr', 50)
ON CONFLICT ("quality_profile_name", "custom_format_name", "arr_type")
DO UPDATE SET "score" = excluded."score";
