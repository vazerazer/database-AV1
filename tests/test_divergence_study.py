#!/usr/bin/env python3
"""
Unit Tests for Release Group Divergence Study (Op 913)
================================================================================
Validates divergence classification logic, candidate regex generation,
and synthetic recorded parse fixtures offline in CI.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate_scoring import build_compiled_db
from divergence_study import (
    get_candidate_release_group_patterns,
    run_divergence_study,
)

class TestDivergenceStudyCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = build_compiled_db()
        cls.cand_patterns = get_candidate_release_group_patterns()

    def test_candidate_release_group_patterns_structure(self):
        self.assertIn("AV1 Quality Encoders", self.cand_patterns)
        self.assertIn("AV1 Compact Encoders", self.cand_patterns)
        self.assertIn("AV1 Storage Savers", self.cand_patterns)
        self.assertIn("AV1 Anime Encoders", self.cand_patterns)
        
        # Test regex pattern format
        q_re = self.cand_patterns["AV1 Quality Encoders"]["compiled"]
        self.assertTrue(q_re.search("CoSMiCSuRFeR"))
        self.assertTrue(q_re.search("TAoE"))
        self.assertTrue(q_re.search("dAV1nci"))
        self.assertTrue(q_re.search("R and H"))
        self.assertTrue(q_re.search("R&H"))
        
        c_re = self.cand_patterns["AV1 Compact Encoders"]["compiled"]
        self.assertTrue(c_re.search("LAZARUS"))
        self.assertTrue(c_re.search("DKV"))
        self.assertFalse(c_re.search("CoSMiCSuRFeR"))

    def test_divergence_classification_synthetic(self):
        # Synthetic recorded corpus with known parser behaviors
        synthetic_corpus = [
            # 1. Direct Agreement (Both title regex and parsed group match Quality)
            {
                "title": "The.Lord.of.the.Rings.2003.Extended.1080p.AV1.DDP.Atmos-TiZU.mkv",
                "category": "Standard Compact",
                "target_cf": "AV1 Quality Encoders",
                "expected_pass": True,
                "parsed_group": "TiZU",
                "arr_type": "radarr"
            },
            # 2. Compound Group Truncation (Radarr parses 'R' for 'R&H') -> TITLE_ONLY_MATCH
            {
                "title": "The.Shawshank.Redemption.1994.2160p.AV1-R&H.mkv",
                "category": "Compound Ampersand",
                "target_cf": "AV1 Quality Encoders",
                "expected_pass": True,
                "parsed_group": "R",
                "arr_type": "radarr"
            },
            # 3. Compound Group Space Truncation (Radarr parses 'R' for 'R and H') -> TITLE_ONLY_MATCH
            {
                "title": "The.Shawshank.Redemption.1994.2160p.AV1-R and H.mkv",
                "category": "Compound Space",
                "target_cf": "AV1 Quality Encoders",
                "expected_pass": True,
                "parsed_group": "R",
                "arr_type": "radarr"
            },
            # 4. Unseasoned Anime (Sonarr parses None for '[AV1ARY]') -> TITLE_ONLY_MATCH
            {
                "title": "[AV1ARY] Dungeon Meshi [1080p AV1].mkv",
                "category": "Unseasoned Anime",
                "target_cf": "AV1 Anime Encoders",
                "expected_pass": True,
                "parsed_group": None,
                "arr_type": "sonarr"
            },
            # 5. Negative False Positive Check (Movie starting with group name) -> AGREEMENT_FAIL
            {
                "title": "Trix the Girl Who Leapt Through Time 2006 BD 1080p Av1 Fc875ba4.mkv",
                "category": "False Positive Movie Title",
                "target_cf": "AV1 Anime Encoders",
                "expected_pass": False,
                "parsed_group": None,
                "arr_type": "radarr"
            }
        ]

        results, summary = run_divergence_study(
            synthetic_corpus, self.conn, self.cand_patterns
        )

        self.assertEqual(summary["AGREEMENT_PASS"], 1)
        self.assertEqual(summary["AGREEMENT_FAIL"], 1)
        self.assertEqual(summary["TITLE_ONLY_MATCH"], 3)
        self.assertEqual(len(summary["DIV_CLASSES"]["COMPOUND_NAMES"]), 2)
        self.assertEqual(len(summary["DIV_CLASSES"]["UNSEASONED_ANIME"]), 1)

if __name__ == "__main__":
    unittest.main()
