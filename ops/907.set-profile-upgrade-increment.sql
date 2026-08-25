-- =============================================================================
-- Migration: 907.set-profile-upgrade-increment.sql
-- Description: Set upgrade_score_increment = 300 on all 7 AV1 quality profiles
--              to eliminate minor service/audio churn while ensuring major
--              tier and AV1 upgrades fire cleanly.
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 90701
UPDATE quality_profiles
SET upgrade_score_increment = 300
WHERE name IN (
  'Movies 2160p AV1 HQ',
  'Movies 1080p AV1 HQ',
  'Movies 1080p AV1 Storage',
  'TV 2160p AV1',
  'TV 1080p AV1 HQ',
  'TV 1080p AV1 Storage',
  'Anime 1080p AV1'
);
-- --- END op 90701
