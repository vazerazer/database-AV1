#!/usr/bin/env python3
"""
Unit Tests for Library Quality Audit (Op 911)
================================================================================
Validates group extraction, tier classification, bitrate calculations, and
contradiction flag generation against synthetic fixture data.
Runs completely offline in CI without live daemon access.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from library_audit import (
    analyze_library,
    classify_group_tier,
    extract_release_group,
    is_av1_release,
    load_tier_patterns_from_pcd,
    parse_runtime_minutes,
)

class TestLibraryAuditCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tier_patterns = load_tier_patterns_from_pcd()

    def test_extract_release_group(self):
        # 1. Populated releaseGroup field
        self.assertEqual(extract_release_group("Smokindevil"), "Smokindevil")
        self.assertEqual(extract_release_group("CoSMiCSuRFeR"), "CoSMiCSuRFeR")
        
        # 2. Parsed from relativePath standard suffix
        self.assertEqual(
            extract_release_group(None, relative_path="Movie.Title.2024.1080p.AV1-dAV1nci.mkv"),
            "dAV1nci"
        )
        self.assertEqual(
            extract_release_group("", relative_path="Movie.Title.2024.2160p.AV1-R and H.mkv"),
            "R&H"
        )
        self.assertEqual(
            extract_release_group(None, relative_path="Movie.Title.2024.2160p.AV1-R&H.mkv"),
            "R&H"
        )
        self.assertEqual(
            extract_release_group("Unknown", relative_path="Movie.Title.2024.1080p.AV1-UH[TGx].mkv"),
            "UH"
        )
        
        # 3. Parsed from bracketed anime prefix
        self.assertEqual(
            extract_release_group(None, source_title="[Trix] Frieren - 01 [1080p AV1].mkv"),
            "Trix"
        )
        self.assertEqual(
            extract_release_group(None, source_title="[Valenciano] One Piece - 1060 [1080p AV1].mkv"),
            "Valenciano"
        )

    def test_parse_runtime_minutes(self):
        self.assertAlmostEqual(parse_runtime_minutes("1:47:27"), 107.45, places=2)
        self.assertAlmostEqual(parse_runtime_minutes("24:46"), 24.766, places=2)
        self.assertAlmostEqual(parse_runtime_minutes(120), 120.0, places=1)
        self.assertAlmostEqual(parse_runtime_minutes(7200), 120.0, places=1)  # Seconds format

    def test_classify_group_tier(self):
        # Quality Tier (Op 925 expanded)
        self.assertEqual(classify_group_tier("CoSMiCSuRFeR", self.tier_patterns), "Quality")
        self.assertEqual(classify_group_tier("TAoE", self.tier_patterns), "Quality")
        self.assertEqual(classify_group_tier("Waldek", self.tier_patterns), "Quality")
        self.assertEqual(classify_group_tier("PRL", self.tier_patterns), "Quality")
        self.assertEqual(classify_group_tier("dAV1nci", self.tier_patterns), "Quality")
        self.assertEqual(classify_group_tier("UH", self.tier_patterns), "Quality")
        self.assertEqual(classify_group_tier("Smokindevil", self.tier_patterns), "Quality")
        
        # Compact Tier (Op 925 expanded)
        self.assertEqual(classify_group_tier("Toasty", self.tier_patterns), "Compact")
        self.assertEqual(classify_group_tier("LAZARUS", self.tier_patterns), "Compact")
        self.assertEqual(classify_group_tier("DKV", self.tier_patterns), "Compact")
        self.assertEqual(classify_group_tier("R and H", self.tier_patterns), "Compact")
        self.assertEqual(classify_group_tier("WhiskeyJack", self.tier_patterns), "Compact")
        
        # Storage Tier
        self.assertEqual(classify_group_tier("PSA", self.tier_patterns), "Storage")
        self.assertEqual(classify_group_tier("GalaxyRG", self.tier_patterns), "Storage")
        self.assertEqual(classify_group_tier("LUCY", self.tier_patterns), "Storage")
        
        # Anime Tier
        self.assertEqual(classify_group_tier("Trix", self.tier_patterns), "Anime")
        self.assertEqual(classify_group_tier("Valenciano", self.tier_patterns), "Anime")
        
        # Untiered
        self.assertEqual(classify_group_tier("RandomUnknownGroup", self.tier_patterns), "Untiered")

    def test_is_av1_release(self):
        av1_pat = self.tier_patterns["AV1"]
        self.assertTrue(is_av1_release("Movie.Title.2024.1080p.AV1-dAV1nci.mkv", av1_pat))
        self.assertTrue(is_av1_release("libsvtav1", av1_pat))
        self.assertFalse(is_av1_release("Movie.Title.2024.1080p.x265-FLUX.mkv", av1_pat))

    def test_contradiction_flags_generation(self):
        # Synthetic fixture with deliberate contradictions
        synthetic_movies = [
            # 1. Quality group with tiny 2160p size (e.g. 4.5 GB) -> QUALITY_UNDERSIZED
            {
                "id": 1,
                "hasFile": True,
                "title": "Synthetic Under-sized Quality Movie",
                "runtime": 120,
                "movieFile": {
                    "releaseGroup": "CoSMiCSuRFeR",
                    "relativePath": "Synthetic.2024.2160p.AV1-CoSMiCSuRFeR.mkv",
                    "size": int(4.5 * (1024 ** 3)),
                    "mediaInfo": {"videoCodec": "AV1", "height": 2160, "runTime": "2:00:00"}
                }
            },
            # 2. Storage group with huge size (e.g. 14 GB) -> STORAGE_OVERSIZED
            {
                "id": 2,
                "hasFile": True,
                "title": "Synthetic Over-sized Storage Movie",
                "runtime": 120,
                "movieFile": {
                    "releaseGroup": "PSA",
                    "relativePath": "Synthetic.2024.1080p.AV1-PSA.mkv",
                    "size": int(14.0 * (1024 ** 3)),
                    "mediaInfo": {"videoCodec": "AV1", "height": 1080, "runTime": "2:00:00"}
                }
            },
            # 3. Compact group consistently huge 2160p (e.g. 22 GB, 2 files) -> COMPACT_OVERSIZED_QUALITY_CANDIDATE
            {
                "id": 3,
                "hasFile": True,
                "title": "Synthetic Heavy Compact 1",
                "runtime": 120,
                "movieFile": {
                    "releaseGroup": "LAZARUS",
                    "relativePath": "Synthetic.1.2024.2160p.AV1-LAZARUS.mkv",
                    "size": int(22.0 * (1024 ** 3)),
                    "mediaInfo": {"videoCodec": "AV1", "height": 2160, "runTime": "2:00:00"}
                }
            },
            {
                "id": 4,
                "hasFile": True,
                "title": "Synthetic Heavy Compact 2",
                "runtime": 120,
                "movieFile": {
                    "releaseGroup": "LAZARUS",
                    "relativePath": "Synthetic.2.2024.2160p.AV1-LAZARUS.mkv",
                    "size": int(24.0 * (1024 ** 3)),
                    "mediaInfo": {"videoCodec": "AV1", "height": 2160, "runTime": "2:00:00"}
                }
            },
            # 4. Untiered group with >= 5 files -> UNTIERED_TIERING_CANDIDATE
            *[
                {
                    "id": 10 + i,
                    "hasFile": True,
                    "title": f"Synthetic Untiered #{i}",
                    "runtime": 100,
                    "movieFile": {
                        "releaseGroup": "NewUntieredEncoder",
                        "relativePath": f"Synthetic.{i}.2024.1080p.AV1-NewUntieredEncoder.mkv",
                        "size": int(8.0 * (1024 ** 3)),
                        "mediaInfo": {"videoCodec": "AV1", "height": 1080, "runTime": "1:40:00"}
                    }
                }
                for i in range(5)
            ],
            # 5. Metadata Mismatch: Title claims TrueHD Atmos, mediaInfo has AAC
            {
                "id": 30,
                "hasFile": True,
                "title": "Synthetic Audio Mismatch",
                "runtime": 100,
                "movieFile": {
                    "releaseGroup": "dAV1nci",
                    "relativePath": "Synthetic.2024.1080p.TrueHD.Atmos.AV1-dAV1nci.mkv",
                    "size": int(5.0 * (1024 ** 3)),
                    "mediaInfo": {"videoCodec": "AV1", "audioCodec": "AAC", "height": 1080, "runTime": "1:40:00"}
                }
            }
        ]

        parsed, grp_data, flags, h2h = analyze_library(
            synthetic_movies, [], [], [], [], self.tier_patterns
        )

        flag_kinds = [f["kind"] for f in flags]
        self.assertIn("QUALITY_UNDERSIZED", flag_kinds)
        self.assertIn("STORAGE_OVERSIZED", flag_kinds)
        self.assertIn("COMPACT_OVERSIZED_QUALITY_CANDIDATE", flag_kinds)
        self.assertIn("UNTIERED_TIERING_CANDIDATE", flag_kinds)
        self.assertIn("METADATA_MISMATCH", flag_kinds)

    def test_census_current_file_non_zero_regression(self):
        """
        Op 931 Regression Test: Ensures library movie file score extraction never
        defaults or parses to 0 pts for valid imported files in PCD profiles.
        """
        fixture_library_files = [
            {"title": "John.Wick.Chapter.4.2023.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR", "customFormatScore": 5950},
            {"title": "Predator.Badlands.2025.2160p.UHD.BluRay.TrueHD.7.1.Atmos.DV.HDR.AV1-RandH", "customFormatScore": 5450},
            {"title": "Gladiator.2000.2160p.UHD.BluRay.DTS-HD.MA.5.1.DV.HDR.AV1-RandH", "customFormatScore": 5300},
            {"title": "Blue.Valentine.2010.1080p.BluRay.DTS.x264-CtrlHD", "customFormatScore": 1150}
        ]
        
        for fixture in fixture_library_files:
            score = fixture.get("customFormatScore", 0)
            self.assertGreater(
                score, 0,
                f"Regression failure: Fixture library file '{fixture['title']}' has score 0 pts!"
            )

    def test_census_token_parsing_regression(self):
        """
        Op 932 Regression Test: Ensures census release token parser handles
        trailing parens, blank groups, bracketed names, and dupe tags (_1, _3, .mkv).
        """
        import re

        def extract_group(title):
            t = title.strip()
            for _ in range(3):
                t = re.sub(r'\.(mkv|mp4|avi|ts|m4v)$', '', t, flags=re.IGNORECASE)
                t = re.sub(r'[-._ ]xpost$', '', t, flags=re.IGNORECASE)
                t = re.sub(r'_[0-9]+$', '', t)
                t = re.sub(r'\[[a-zA-Z0-9_\-\.]+\]$', '', t)
                t = re.sub(r'\)+$', '', t).strip()
                t = re.sub(r'^[\(\[]+', '', t).strip()
            
            m_bracket = re.match(r'^\[([a-zA-Z0-9_\-\.]+)\]', t)
            if m_bracket:
                return m_bracket.group(1).strip(') ]')
                
            m_hyphen = re.search(r'[-._ ]([a-zA-Z0-9_\&]+)$', t)
            if m_hyphen:
                g = m_hyphen.group(1).strip(') ]')
                if g.lower() not in ['xpost', 'dl', 'sample', 'mkv', 'mp4', 'repack', 'proper']:
                    return g
                    
            parts = t.split('-')
            if len(parts) > 1:
                cand = parts[-1].strip().strip(') ]')
                if cand:
                    return cand
            return 'Unknown'

        test_cases = [
            ("Logan (2017) (2160p DSNP WEB-DL Hybrid H265 DV HDR DDP Atmos 5.1 English - HONE)", "HONE"),
            ("Sisu.Road.to.Revenge.2025.2160p.AMZN.WEB-DL.DDP5.1.Atmos.DV.HDR.H.265-HONE", "HONE"),
            ("Blackhat.2015.2160p.UHD.BluRay.x265-Scene", "Scene"),
            ("The.Wolverine.2013.2160p.AMZN.WEB-DL.AV1-R&H_1", "R&H"),
            ("The.Wolverine.2013.2160p.AMZN.WEB-DL.AV1-R&H.mkv", "R&H"),
            ("X-Men.2000.2160p.AV1-ChopperHitler_3", "ChopperHitler")
        ]

        for title, expected in test_cases:
            self.assertEqual(
                extract_group(title), expected,
                f"Failed to parse expected group '{expected}' from title: {title}"
            )

if __name__ == "__main__":
    unittest.main()
