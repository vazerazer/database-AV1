-- @description: Let a Movies Anywhere WEB from a circle beat that circle's smaller Blu-ray encode
-- @author: cursor
-- @name: 970.prefer-movies-anywhere-over-compact-disc

BEGIN TRANSACTION;

-- Disc stays 200 points ahead of a plain WEB from the same group, so a small
-- WEB does not replace a disc. 200 is inside the feature stack and well under
-- the 700-point group gap.
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 1', 'all', 7900),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 2', 'all', 7200),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 3', 'all', 6500),
  ('Movies 2160p HEVC Compact', '2160p Compact WEB Tier 4', 'all', 5800)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

-- Movies Anywhere is the storefront master these circles encode from. +250
-- clears the 200-point disc edge, so an HONE [MA] WEB outranks an HONE Blu-ray.
-- A lower circle still cannot pass the circle above: 7200 + 250 + features
-- stays under a bare 8100.
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES
  ('Movies 2160p HEVC Compact', 'MA', 'all', 250)
ON CONFLICT (quality_profile_name, custom_format_name, arr_type) DO UPDATE SET score = excluded.score;

UPDATE quality_profiles
SET description = 'Compact 4K HEVC for a 55-inch Mini LED and a 32-inch 4K monitor. HONE, hallowed, HQMUX and PTer first, then QxR/TAoE/BHDStudio, then PSA/HiQVE/DEFLATE, then UTR/RARBG/iVy. A Movies Anywhere WEB from a circle beats that circle''s Blu-ray. YTS and MeGusta stay rejected.'
WHERE name = 'Movies 2160p HEVC Compact';

-- A two-hour movie can now be about 42 GB. The previous 200 MB/min cap
-- rejected a large Movies Anywhere WEB of a normal-length film.
UPDATE radarr_quality_definitions
SET max_size = 360
WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p');

CREATE TEMP TABLE _pcd_assertions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    condition INTEGER CHECK (condition = 1)
);
INSERT INTO _pcd_assertions (name, condition) VALUES
  ('Movie WEB tier sits just under disc', (SELECT score = 7900 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1')),
  ('Movies Anywhere outranks the disc edge', (SELECT score = 250 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = 'MA')),
  ('Disc tier unchanged', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'Movies 2160p HEVC Compact' AND custom_format_name = '2160p Compact Bluray Tier 1')),
  ('TV WEB tier unchanged', (SELECT score = 8100 FROM quality_profile_custom_formats WHERE quality_profile_name = 'TV 2160p HEVC Compact' AND custom_format_name = '2160p Compact WEB Tier 1'));
DROP TABLE _pcd_assertions;

COMMIT;
