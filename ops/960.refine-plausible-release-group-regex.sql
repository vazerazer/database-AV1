-- =============================================================================
-- Migration: 960.refine-plausible-release-group-regex.sql
-- Description: Refine 'Plausible Release Group' regex to block technical suffix
--              tokens (-HD, -MA, -bit, -DL, -Rip, -X, etc.) from falsely matching
--              as release groups, restoring the -2400 AV1 Nameless penalty for
--              titles ending in audio/video spec markers (e.g. Star Wars Ep IX).
-- Schema: PCD v2 (Schema 1.1.0)
-- =============================================================================

-- --- START op 96001
UPDATE "regular_expressions"
SET "pattern" = '(?i)(?:^\[[A-Za-z0-9._ -]+\]|-(?:\s*\[(?!(?:NL[- .]?sub|NL|DUTCH|GERMAN|FRENCH|ITA|SPANISH|SWE|DK|NOR|Fi|xpost|AV1|AV01|HEVC|x265|x264|AVC|H\.?264|H\.?265|HDR10\+|HDR10|HDR|DV|DoVi|10[- .]?bit|8[- .]?bit|bit|BRRip|BDRip|WEB[- .]?DL|WEBRip|BluRay|UHD|Remux|HDTV|DL|Rip|2160p|1080p|720p|480p|AAC|DDP|AC3|EAC3|TrueHD|Atmos|DTS[- .]?(?:HD(?:[- .]?MA)?|X|ES)?|HD(?:[- .]?MA)?|MA|HRA|X|Opus|FLAC|MP3|5\.1|7\.1|2\.0|1\.0|PROPER|REPACK(?:[0-9]+)?|RERIP|N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\])[A-Za-z0-9_.-]+\]|(?!\s*(?:NL[- .]?sub|NL|DUTCH|GERMAN|FRENCH|ITA|SPANISH|SWE|DK|NOR|Fi|xpost|AV1|AV01|HEVC|x265|x264|AVC|H\.?264|H\.?265|HDR10\+|HDR10|HDR|DV|DoVi|10[- .]?bit|8[- .]?bit|bit|BRRip|BDRip|WEB[- .]?DL|WEBRip|BluRay|UHD|Remux|HDTV|DL|Rip|2160p|1080p|720p|480p|AAC|DDP|AC3|EAC3|TrueHD|Atmos|DTS[- .]?(?:HD(?:[- .]?MA)?|X|ES)?|HD(?:[- .]?MA)?|MA|HRA|X|Opus|FLAC|MP3|5\.1|7\.1|2\.0|1\.0|PROPER|REPACK(?:[0-9]+)?|RERIP|N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)(?:[\[\].\s-]|$))\s*[A-Za-z0-9_&]+(?:[-. ][A-Za-z0-9_&]+)*(?:\[[a-zA-Z0-9_.-]+\])?)(?:\.[a-zA-Z0-9]{2,4})?$)'
WHERE "name" = 'Plausible Release Group';
-- --- END op 96001
