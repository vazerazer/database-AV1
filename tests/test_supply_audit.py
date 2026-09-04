#!/usr/bin/env python3
"""
Unit Tests for Supply-Side Search Audit (Op 912)
================================================================================
Validates token parsing, candidate release scoring, group fingerprinting,
win-rate calculation, and diagnostic flag generation against synthetic fixtures.
Runs completely offline in CI without live daemon access.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate_scoring import build_compiled_db
from library_audit import load_tier_patterns_from_pcd
from supply_audit import (
    analyze_supply_candidates,
    get_all_tiered_groups_from_db,
    parse_title_tokens,
)

class TestSupplyAuditCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = build_compiled_db()
        cls.tier_patterns = load_tier_patterns_from_pcd()

    def test_parse_title_tokens(self):
        t1 = "Dune.Part.Two.2024.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-TAoE"
        tok1 = parse_title_tokens(t1)
        self.assertTrue(tok1["is_hdr"])
        self.assertTrue(tok1["is_dv"])
        self.assertTrue(tok1["is_atmos"])
        self.assertTrue(tok1["is_truehd"])
        self.assertTrue(tok1["is_lossless"])
        self.assertFalse(tok1["is_x265"])
        
        t2 = "Movie.Title.2024.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX"
        tok2 = parse_title_tokens(t2)
        self.assertFalse(tok2["is_hdr"])
        self.assertFalse(tok2["is_dv"])
        self.assertFalse(tok2["is_truehd"])
        self.assertTrue(tok2["is_x264"])

    def test_get_all_tiered_groups_from_db(self):
        tiered = get_all_tiered_groups_from_db(self.conn)
        self.assertIn("CoSMiCSuRFeR", tiered)
        self.assertEqual(tiered["CoSMiCSuRFeR"], "Quality")
        self.assertIn("dAV1nci", tiered)
        self.assertEqual(tiered["dAV1nci"], "Quality")
        self.assertIn("PSA", tiered)
        self.assertEqual(tiered["PSA"], "Storage")
        self.assertIn("Trix", tiered)
        self.assertEqual(tiered["Trix"], "Anime")

    def test_analyze_supply_candidates_synthetic(self):
        # Synthetic search results for 2 movies
        synthetic_candidates = [
            # Movie 1: Has active x265 file, but high-scoring AV1 candidate exists -> UPGRADE_OPPORTUNITY
            {
                "title_info": {"id": 101, "title": "Synthetic Dune", "type": "Movie"},
                "arr_type": "radarr",
                "primary_profile": "Movies 2160p AV1 HQ",
                "runtime_mins": 150,
                "current_file": {
                    "group": "FLUX",
                    "size_gb": 12.0,
                    "is_av1": False,
                    "score": 1050,
                    "file_name": "Synthetic.Dune.2024.2160p.WEB-DL.x265-FLUX.mkv"
                },
                "releases": [
                    {
                        "title": "Synthetic.Dune.2024.2160p.UHD.BluRay.TrueHD.Atmos.DV.HDR.AV1-TAoE",
                        "releaseGroup": "TAoE",
                        "size": int(22.0 * (1024 ** 3)),
                        "indexer": "TestIndexer"
                    },
                    {
                        "title": "Synthetic.Dune.2024.2160p.WEB-DL.DDP5.1.x265-FLUX",
                        "releaseGroup": "FLUX",
                        "size": int(12.0 * (1024 ** 3)),
                        "indexer": "TestIndexer"
                    },
                    # Absurdity candidate (16MB WEBRip) -> ABSURDITY_BAN_CANDIDATE
                    {
                        "title": "Synthetic.Dune.2024.1080p.WEBRip.AV1-ENTROPY",
                        "releaseGroup": "ENTROPY",
                        "size": 16 * 1024 * 1024,
                        "indexer": "FakeIndexer"
                    }
                ]
            },
            # Movie 2: All candidates for a blind group fall below min cutoff -> PROFILE_BLIND_SPOT
            {
                "title_info": {"id": 102, "title": "Synthetic Low Quality", "type": "Movie"},
                "arr_type": "radarr",
                "primary_profile": "Movies 2160p AV1 HQ",
                "runtime_mins": 100,
                "current_file": {},
                "releases": [
                    # 3 releases from GeneMige that fail min score 1000
                    {
                        "title": "Synthetic.Movie.2024.1080p.BluRay.x264-GeneMige",
                        "releaseGroup": "GeneMige",
                        "size": int(6.0 * (1024 ** 3)),
                        "indexer": "TestIndexer"
                    },
                    {
                        "title": "Synthetic.Movie.2023.1080p.BluRay.x264-GeneMige",
                        "releaseGroup": "GeneMige",
                        "size": int(6.5 * (1024 ** 3)),
                        "indexer": "TestIndexer"
                    },
                    {
                        "title": "Synthetic.Movie.2022.1080p.BluRay.x264-GeneMige",
                        "releaseGroup": "GeneMige",
                        "size": int(5.5 * (1024 ** 3)),
                        "indexer": "TestIndexer"
                    }
                ]
            }
        ]

        group_supply, flags, title_evals, total_evaluated = analyze_supply_candidates(
            synthetic_candidates, self.conn, self.tier_patterns
        )

        self.assertEqual(total_evaluated, 6)
        
        # Verify win count for TAoE
        self.assertIn("TAoE", group_supply)
        self.assertEqual(group_supply["TAoE"]["wins"], 1)

        flag_kinds = [f["kind"] for f in flags]
        self.assertIn("UPGRADE_OPPORTUNITY", flag_kinds)
        self.assertIn("ABSURDITY_BAN_CANDIDATE", flag_kinds)
        self.assertIn("PROFILE_BLIND_SPOT", flag_kinds)
        self.assertIn("TIERED_ZERO_SUPPLY", flag_kinds)

if __name__ == "__main__":
    unittest.main()
