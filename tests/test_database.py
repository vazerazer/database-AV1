#!/usr/bin/env python3
"""Compile check, name-fix checks, and the 45-movie rescore."""

from __future__ import annotations

import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from pcdlib import DATABASE_NAME, PROFILE_NAME, compile_layers  # noqa: E402
from score import Scorer, pick  # noqa: E402

FIXTURES = os.path.join(ROOT, "tests", "fixtures", "releases")

# Research picks, plus one same-score tie the name fix makes eligible.
EXPECTED_NEW = {
    "1272.json": "Cam.2018.1080p.NF.WEB-DL.DD5.1.H264-CMRG-4u7c",
    "847.json": "The.Black.Cauldron.1985.2160p.DSNP.WEB-DL.DTS-HD.MA.5.1.DoVi.HDR.HEVC-SiC",
    "871.json": "Cast.Away.2000.2160p.WEB-DL.DTS-HD.MA.5.1.DV.HDR10+.H.265-XEBEC",
    "910.json": "Jack.Reacher.2012.2160p.UHD.BluRay.DTS-HD.MA.7.1.DV.x265-W4NK3R",
    "963.json": "Supergirl.2026.2160p.Ykw.WEB-DL.HYBRiD.H265.DV.HDR.DDP.Atmos.5.1.ENGLISH.HONE",
}


def schema_dir() -> str:
    env = os.environ.get("PCD_SCHEMA_PATH")
    if env and os.path.isdir(env):
        return env
    candidate = os.path.join(ROOT, "deps", "schema", "ops")
    if os.path.isdir(candidate):
        return candidate
    raise unittest.SkipTest("set PCD_SCHEMA_PATH to the Dictionarry schema ops directory")


def release(title: str, group: str, quality: str, source: str, resolution: int, size: int) -> dict:
    return {
        "title": title,
        "releaseGroup": group,
        "size": size,
        "quality": {
            "quality": {
                "name": quality,
                "source": source,
                "resolution": resolution,
                "modifier": "none",
            }
        },
        "languages": [{"name": "English"}],
        "indexerFlags": [],
        "rejections": [],
    }


class DatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = schema_dir()
        cls.base = compile_layers(schema, os.path.join(ROOT, "ops"))
        cls.db = compile_layers(schema, os.path.join(ROOT, "ops"), os.path.join(ROOT, "tweaks"))
        cls.base_scorer = Scorer(cls.base)
        cls.scorer = Scorer(cls.db)

    def test_manifest_names_the_database_and_keeps_the_profile(self):
        with open(os.path.join(ROOT, "pcd.json"), encoding="utf-8") as handle:
            manifest = json.load(handle)
        self.assertEqual(manifest["name"], DATABASE_NAME)
        self.assertEqual(manifest["repository"], f"https://github.com/vazerazer/{DATABASE_NAME}")
        self.assertEqual(manifest["arr_types"], ["radarr"])
        self.assertIn("https://github.com/Dictionarry-Hub/schema", manifest["dependencies"])
        profiles = [row["name"] for row in self.db.execute("SELECT name FROM quality_profiles")]
        self.assertEqual(profiles, [PROFILE_NAME])
        row = self.db.execute(
            "SELECT minimum_custom_format_score, upgrade_until_score FROM quality_profiles"
        ).fetchone()
        self.assertEqual(row["minimum_custom_format_score"], 1000)
        self.assertEqual(row["upgrade_until_score"], 10000)
        description = self.db.execute("SELECT description FROM quality_profiles").fetchone()["description"]
        self.assertIn("Local layer:", description)
        self.assertIn("DTS-HD scores 0", description)

    def test_only_referenced_formats_and_regexes_remain(self):
        empty_profiles = self.db.execute(
            """
            SELECT name FROM custom_formats cf
            WHERE NOT EXISTS (
                SELECT 1 FROM quality_profile_custom_formats q
                WHERE q.custom_format_name = cf.name AND q.quality_profile_name = ?
            )
            """,
            (PROFILE_NAME,),
        ).fetchall()
        self.assertEqual(empty_profiles, [])
        unused_regex = self.db.execute(
            """
            SELECT name FROM regular_expressions re
            WHERE NOT EXISTS (
                SELECT 1 FROM condition_patterns cp
                WHERE cp.regular_expression_name = re.name
            )
            """
        ).fetchall()
        self.assertEqual(unused_regex, [])
        empty_formats = self.db.execute(
            """
            SELECT q.custom_format_name
            FROM quality_profile_custom_formats q
            WHERE NOT EXISTS (
                SELECT 1 FROM custom_format_conditions c
                WHERE c.custom_format_name = q.custom_format_name
            )
            """
        ).fetchall()
        self.assertEqual(empty_formats, [])
        self.assertEqual(self.db.execute("PRAGMA foreign_key_check").fetchall(), [])
        self.assertEqual(self.db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        others = self.db.execute(
            "SELECT name FROM quality_profiles WHERE name != ?", (PROFILE_NAME,)
        ).fetchall()
        self.assertEqual(others, [])
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM sonarr_naming").fetchone()[0], 0)

    def test_audio_rule_and_no_size_cap(self):
        scores = {
            row["custom_format_name"]: row["score"]
            for row in self.db.execute(
                """
                SELECT custom_format_name, score FROM quality_profile_custom_formats
                WHERE quality_profile_name = ?
                """,
                (PROFILE_NAME,),
            )
        }
        self.assertEqual(scores["DTS-HD MA"], 0)
        self.assertEqual(scores["DTS-HD HRA"], 0)
        self.assertEqual(scores["DTS-X"], 0)
        self.assertEqual(scores["TrueHD"], -10000)
        self.assertEqual(scores["TrueHD Missing"], -10000)
        self.assertEqual(scores["No Audio"], -10000)
        self.assertEqual(scores["Lite UHD Mid Tier"], 1800)
        for name in ("TrueHD", "TrueHD Missing", "DTS-HD MA", "DTS-HD HRA", "DTS-X"):
            sizes = self.db.execute(
                """
                SELECT COUNT(*) FROM condition_sizes
                WHERE custom_format_name = ?
                """,
                (name,),
            ).fetchone()[0]
            self.assertEqual(sizes, 0, name)
        trusted = self.db.execute(
            """
            SELECT 1 FROM condition_patterns
            WHERE custom_format_name = 'TrueHD'
              AND condition_name = 'Not Trusted Group'
              AND regular_expression_name = 'Lite TrueHD Trusted Groups'
            """
        ).fetchone()
        self.assertIsNotNone(trusted)
        pattern = self.db.execute(
            "SELECT pattern FROM regular_expressions WHERE name = 'Lite TrueHD Trusted Groups'"
        ).fetchone()["pattern"]
        self.assertNotIn("WiKi", pattern)
        self.assertNotIn("Tigole", pattern)
        self.assertIn("hallowed", pattern)
        self.assertIn("BHDStudio", pattern)
        self.assertIn("HONE", pattern)
        self.assertNotIn("BYNDR", pattern)

    def test_mid_tier_window_and_rank(self):
        bounds = self.db.execute(
            """
            SELECT min_bytes, max_bytes FROM condition_sizes
            WHERE custom_format_name = 'Lite UHD Mid Tier'
            """
        ).fetchone()
        self.assertEqual(bounds["min_bytes"], 14 * 1024**3)
        self.assertEqual(bounds["max_bytes"], 40 * 1024**3)
        hallowed = release(
            "Movie.2020.2160p.UHD.BluRay.DDP5.1.Atmos.DV.HDR.x265-hallowed",
            "hallowed",
            "Bluray-2160p",
            "bluray",
            2160,
            20 * 1024**3,
        )
        bhdstudio = release(
            "Movie.2020.2160p.UHD.BluRay.DDP5.1.Atmos.DV.HDR.x265-BHDStudio",
            "BHDStudio",
            "Bluray-2160p",
            "bluray",
            2160,
            20 * 1024**3,
        )
        mid = release(
            "Movie.2020.2160p.UHD.BluRay.DDP5.1.Atmos.DV.HDR.x265-j3rico",
            "j3rico",
            "Bluray-2160p",
            "bluray",
            2160,
            20 * 1024**3,
        )
        too_small = dict(mid, size=10 * 1024**3, title=mid["title"] + ".small")
        too_big = dict(mid, size=50 * 1024**3, title=mid["title"] + ".big")
        hallowed_score, hallowed_hits = self.scorer.score(hallowed)
        bhdstudio_score, _ = self.scorer.score(bhdstudio)
        mid_score, mid_hits = self.scorer.score(mid)
        self.assertIn("Lite UHD Mid Tier", mid_hits)
        self.assertNotIn("Lite UHD Mid Tier", hallowed_hits)
        self.assertGreater(hallowed_score, mid_score)
        self.assertGreater(bhdstudio_score, mid_score)
        self.assertEqual(hallowed_score - mid_score, 600)
        small_score, small_hits = self.scorer.score(too_small)
        big_score, big_hits = self.scorer.score(too_big)
        self.assertNotIn("Lite UHD Mid Tier", small_hits)
        self.assertNotIn("Lite UHD Mid Tier", big_hits)
        self.assertLess(small_score, mid_score)
        self.assertLess(big_score, mid_score)
        # The size window does not ban the file. It only withholds the bonus.
        self.assertGreater(big_score, -10000)

    def test_name_fixes_match_radarr_group_scores(self):
        def hits(title: str, group: str, quality="Bluray-2160p", source="bluray", resolution=2160):
            rel = release(title, group, quality, source, resolution, 18 * 1024**3)
            return self.scorer.score(rel)

        dotted = "Movie.2020.2160p.UHD.BluRay.DDP5.1.DV.HDR.x265.hallowed"
        hyphen = "Movie.2020.2160p.UHD.BluRay.DDP5.1.DV.HDR.x265-hallowed"
        self.assertEqual(hits(dotted, "")[0], hits(hyphen, "hallowed")[0])
        pirates_dot = hits(
            "Movie.2020.2160p.WEB-DL.DDP5.1.DV.HDR.H.265.PiRaTeS",
            "",
            "WEBDL-2160p",
            "webdl",
            2160,
        )
        pirates_ok = hits(
            "Movie.2020.2160p.WEB-DL.DDP5.1.DV.HDR.H.265-PiRaTeS",
            "PiRaTeS",
            "WEBDL-2160p",
            "webdl",
            2160,
        )
        self.assertEqual(pirates_dot[0], pirates_ok[0])
        self.assertIn("Lite Group Missing Offset", pirates_dot[1])
        self.assertIn("Lite Baseline (Name Fallback)", pirates_dot[1])

        hone_member = hits(
            "Movie (2020) (2160p UHD BluRay x265 DV HDR DDP 5.1 English - DarQ HONE)",
            "DarQ",
        )
        self.assertIn("Lite HONE Family Offset", hone_member[1])
        self.assertIn("HONE (Bad Name)", hone_member[1])
        self.assertGreater(hone_member[0], 1000)

        weasley = hits(
            "Movie.2020.2160p.UHD.BluRay.DV.HDR.DDP.5.1.x265-Weasley-HONE",
            "Weasley-HONE",
        )
        self.assertIn("Lite HONE Family Offset", weasley[1])
        self.assertGreater(weasley[0], 1000)

        cmrg = hits(
            "Cam.2018.1080p.NF.WEB-DL.DD5.1.H264-CMRG-4u7c",
            "CMRG-4u7c",
            "WEBDL-1080p",
            "webdl",
            1080,
        )
        self.assertIn("Lite WEB Tier 01 (Name Fallback)", cmrg[1])
        self.assertNotIn("WEB Tier 01", cmrg[1])

        kitsune = hits(
            "Movie.2020.2160p.WEB-DL.DDP5.1.HDR.H.265-Kitsune[TGx]",
            "Kitsune",
            "WEBDL-2160p",
            "webdl",
            2160,
        )
        self.assertIn("WEB Tier 01", kitsune[1])
        self.assertNotIn("Lite WEB Tier 01 (Name Fallback)", kitsune[1])
        self.assertNotIn("Lite Group Missing Offset", kitsune[1])

        hone_ok = hits(
            "Movie.2020.2160p.UHD.BluRay.DDP5.1.DV.HDR.x265-HONE-",
            "HONE",
        )
        self.assertNotIn("HONE (Bad Name)", hone_ok[1])
        self.assertNotIn("Lite HONE Family Offset", hone_ok[1])
        self.assertNotIn("Lite UHD Tier 03 (Name Fallback)", hone_ok[1])
        self.assertIn("UHD Bluray Tier 03", hone_ok[1])

        repost = hits(
            "Movie.2020.UHD.BluRay.2160p.DDP.7.1.HDR.x265-BHDStudio.mp4-nEwZ-xpost",
            "nEwZ",
        )
        self.assertIn("Lite BHDStudio (Name Fallback)", repost[1])
        self.assertIn("Lite UHD Tier 03 (Name Fallback)", repost[1])
        plain = hits(
            "Movie.2020.UHD.BluRay.2160p.DDP.7.1.HDR.x265-BHDStudio",
            "BHDStudio",
        )
        self.assertEqual(repost[0], plain[0])

    def test_untrusted_truehd_without_dd_stays_blocked(self):
        blocked = release(
            "Movie.2020.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-SomeGroup",
            "SomeGroup",
            "Bluray-2160p",
            "bluray",
            2160,
            30 * 1024**3,
        )
        allowed_dd = release(
            "Movie.2020.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DDP5.1.DV.HDR.x265-SomeGroup",
            "SomeGroup",
            "Bluray-2160p",
            "bluray",
            2160,
            30 * 1024**3,
        )
        trusted = release(
            "Movie.2020.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-hallowed",
            "hallowed",
            "Bluray-2160p",
            "bluray",
            2160,
            18 * 1024**3,
        )
        blocked_score, blocked_hits = self.scorer.score(blocked)
        allowed_score, allowed_hits = self.scorer.score(allowed_dd)
        trusted_score, trusted_hits = self.scorer.score(trusted)
        self.assertIn("TrueHD", blocked_hits)
        self.assertLess(blocked_score, 1000)
        self.assertNotIn("TrueHD", allowed_hits)
        self.assertNotIn("TrueHD", trusted_hits)
        self.assertGreater(trusted_score, 1000)

    def test_dumpstarr_scores_match_radarr_until_the_layer_fires(self):
        if not os.path.isdir(FIXTURES):
            self.skipTest("release fixtures are not checked out")
        checked = 0
        for name in os.listdir(FIXTURES):
            with open(os.path.join(FIXTURES, name), encoding="utf-8") as handle:
                releases = json.load(handle)
            for item in releases:
                reasons = " | ".join(item.get("rejections") or [])
                if "Unknown Movie" in reasons or "Unable to parse" in reasons:
                    continue
                base_score, base_hits = self.base_scorer.score(item)
                self.assertEqual(base_score, item["customFormatScore"], item["title"])
                layer_score, layer_hits = self.scorer.score(item)
                base_set = set(base_hits)
                layer_set = set(layer_hits)
                audio = {"DTS-HD MA", "DTS-HD HRA", "DTS-X", "TrueHD", "TrueHD Missing"}
                disappeared = base_set - layer_set
                appeared = layer_set - base_set
                self.assertTrue(disappeared <= {"TrueHD", "TrueHD Missing"}, item["title"])
                self.assertTrue(all(hit.startswith("Lite ") for hit in appeared), item["title"])
                delta = 0
                for hit in audio & base_set & layer_set:
                    if hit.startswith("DTS"):
                        delta += 10000
                for hit in disappeared:
                    delta += 10000
                for hit in appeared:
                    delta += self.scorer.scores[hit]
                self.assertEqual(layer_score, base_score + delta, item["title"])
                checked += 1
        self.assertGreater(checked, 18000)

    def test_sample_picks(self):
        if not os.path.isdir(FIXTURES):
            self.skipTest("release fixtures are not checked out")
        changes = {}
        for name in sorted(os.listdir(FIXTURES)):
            with open(os.path.join(FIXTURES, name), encoding="utf-8") as handle:
                releases = json.load(handle)
            before = pick(releases, self.base_scorer)
            after = pick(releases, self.scorer)
            before_title = before[0]["title"] if before else None
            after_title = after[0]["title"] if after else None
            if before_title != after_title:
                changes[name] = after_title
                quality = after[0]["quality"]["quality"]
                self.assertFalse(quality["name"].startswith("Remux"), after_title)
                self.assertNotEqual(quality.get("modifier"), "remux")
                self.assertNotIn("TrueHD", after[2])
        self.assertEqual(changes, EXPECTED_NEW)
        # Supergirl stays on the same HONE MA/YKW WEB-DL score. The name fix
        # only lets a previously unparsed copy tie, and the larger file wins.
        with open(os.path.join(FIXTURES, "963.json"), encoding="utf-8") as handle:
            supergirl = json.load(handle)
        chosen = pick(supergirl, self.scorer)
        self.assertEqual(chosen[1], 5230)
        self.assertIn("Lite Group Missing Offset", chosen[2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
