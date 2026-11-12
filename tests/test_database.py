#!/usr/bin/env python3
"""Compile check, audio and preferred-size checks, and the 45-movie regression."""

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

EXPECTED_NEW = {
    "1282.json": "The.Substance.2024.2160p.BluRay.DTS-HD.MA.5.1.DV.HDR10.x265-MainFrame",
    "1328.json": "The Dark Knight (2008) IMAX (2160p UHD BluRay x265 DV HDR DDP 5.1 English - Weasley HONE).mkv-xpost",
    "1349.json": "The.Odyssey.2026.2160p.UHD.BluRay.DTS-HD.MA.5.1.HDR.x265-TRUNKS",
    "838.json": "Fury.2014.2160p.UHD.BluRay.x265.DV.HDR.DDP.7.1.English.DiscoD-HONE",
    "847.json": "The.Black.Cauldron.1985.2160p.DSNP.WEB-DL.DTS-HD.MA.5.1.DoVi.HDR.HEVC-SiC",
    "871.json": "Cast.Away.2000.2160p.WEB-DL.DTS-HD.MA.5.1.DV.HDR10+.H.265-XEBEC",
    "910.json": "Jack.Reacher.2012.2160p.UHD.BluRay.DTS-HD.MA.7.1.DV.x265-W4NK3R",
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
        self.assertEqual(scores["UHD Bluray Mid-Size Tier"], 4200)
        self.assertEqual(scores["hallowed"], 600)
        self.assertEqual(scores["BHDStudio"], 550)
        self.assertEqual(scores["MA Preferred"], 2000)
        self.assertEqual(scores["UHD Bluray Tier 01"], 1900)
        self.assertEqual(scores["UHD Bluray Tier 02"], 1850)
        self.assertEqual(scores["UHD Bluray Tier 03"], 1800)
        self.assertEqual(scores["HD Bluray Tier 01"], 1700)
        self.assertEqual(scores["HD Bluray Tier 02"], 1650)
        self.assertEqual(scores["HD Bluray Tier 03"], 1600)
        self.assertEqual(scores["WEB Tier 01"], 1500)
        self.assertFalse(any("Name Fallback" in name or name.startswith("Lite ") for name in scores))
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
              AND regular_expression_name = 'TrueHD Trusted Groups'
            """
        ).fetchone()
        self.assertIsNotNone(trusted)
        pattern = self.db.execute(
            "SELECT pattern FROM regular_expressions WHERE name = 'TrueHD Trusted Groups'"
        ).fetchone()["pattern"]
        self.assertNotIn("WiKi", pattern)
        self.assertNotIn("Tigole", pattern)
        self.assertIn("hallowed", pattern)
        self.assertIn("BHDStudio", pattern)
        self.assertIn("HONE", pattern)
        self.assertNotIn("BYNDR", pattern)

    def test_preferred_size_window_and_groups(self):
        bounds = self.db.execute(
            """
            SELECT min_bytes, max_bytes FROM condition_sizes
            WHERE custom_format_name = 'UHD Bluray Mid-Size Tier'
            """
        ).fetchone()
        # Radarr's size floor is exclusive and the ceiling is inclusive.
        self.assertEqual(bounds["min_bytes"], 20 * 1024**3)
        self.assertEqual(bounds["max_bytes"], 60 * 1024**3)
        size_name = self.db.execute(
            """
            SELECT condition_name FROM condition_sizes
            WHERE custom_format_name = 'UHD Bluray Mid-Size Tier'
            """
        ).fetchone()["condition_name"]
        self.assertEqual(size_name, "20-60 GB")
        format_description = self.db.execute(
            "SELECT description FROM custom_formats WHERE name = 'UHD Bluray Mid-Size Tier'"
        ).fetchone()["description"]
        self.assertIn("above 20 GB through 60 GB", format_description)
        self.assertIn("below 20 GB", format_description)
        self.assertIn("ZAX", format_description)
        self.assertNotIn("25 GB", format_description)
        preferred = self.db.execute(
            "SELECT pattern FROM regular_expressions WHERE name = 'UHD Mid-Size Groups'"
        ).fetchone()["pattern"]
        trusted = self.db.execute(
            "SELECT pattern FROM regular_expressions WHERE name = 'TrueHD Trusted Groups'"
        ).fetchone()["pattern"]
        preferred_groups = {part.lower() for part in preferred[2:-2].split("|")}
        trusted_groups = {part.lower() for part in trusted[2:-2].split("|")}
        for group in ("w4nk3r", "sphd", "trunks", "ctrlhd"):
            self.assertIn(group, preferred_groups)
            self.assertIn(group, trusted_groups)
        self.assertIn("zax", preferred_groups)
        self.assertNotIn("z@x", preferred_groups)
        self.assertNotIn("zax", trusted_groups)
        self.assertNotIn("hallowed", preferred_groups)
        self.assertNotIn("bhdstudio", preferred_groups)
        self.assertNotIn("wiki", preferred_groups)

        def sized(group, gib):
            return release(
                f"The.Dark.Knight.2008.2160p.UHD.BluRay.DDP7.1.Atmos.DV.HDR.x265-{group}",
                group,
                "Bluray-2160p",
                "bluray",
                2160,
                gib * 1024**3,
            )

        inside, inside_hits = self.scorer.score(sized("TRUNKS", 30))
        below, below_hits = self.scorer.score(sized("TRUNKS", 19))
        above, above_hits = self.scorer.score(sized("TRUNKS", 70))
        floor, floor_hits = self.scorer.score(sized("W4NK3R", 20))
        opened, opened_hits = self.scorer.score(sized("W4NK3R", 25))
        ceiling, ceiling_hits = self.scorer.score(sized("W4NK3R", 60))
        self.assertIn("UHD Bluray Mid-Size Tier", inside_hits)
        self.assertIn("UHD Bluray Mid-Size Tier", ceiling_hits)
        self.assertIn("UHD Bluray Mid-Size Tier", opened_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", below_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", above_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", floor_hits)
        self.assertGreater(inside, below)
        self.assertGreater(inside, above)
        # Outside the window the file is still allowed. The bonus is withheld.
        self.assertGreater(above, 1000)
        self.assertGreater(below, 1000)

    def test_zax_and_hone_inside_the_lowered_floor(self):
        """ZAX earns the mid-size bonus. The floor is above 20 GB, and ZAX stays untrusted."""
        gib = 1024**3

        def encode(group, size):
            return release(
                f"Deadpool.And.Wolverine.2024.2160p.UHD.BluRay.DDP5.1.Atmos.DV.HDR.x265-{group}",
                group,
                "Bluray-2160p",
                "bluray",
                2160,
                size,
            )

        zax_score, zax_hits = self.scorer.score(encode("ZAX", 27 * gib))
        zax_low_score, zax_low_hits = self.scorer.score(encode("ZAX", 19 * gib))
        self.assertIn("UHD Bluray Mid-Size Tier", zax_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", zax_low_hits)
        self.assertEqual(zax_score - zax_low_score, 4200)
        self.assertNotIn("TrueHD", zax_hits)
        self.assertNotIn("TrueHD Block", zax_hits)

        hone_score, hone_hits = self.scorer.score(encode("HONE", 22 * gib))
        hone_low_score, hone_low_hits = self.scorer.score(encode("HONE", 19 * gib))
        self.assertIn("UHD Bluray Mid-Size Tier", hone_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", hone_low_hits)
        self.assertEqual(hone_score - hone_low_score, 4200)

        remux = release(
            "Deadpool.And.Wolverine.2024.2160p.UHD.BluRay.REMUX.HEVC.DDP5.1.Atmos.DV.HDR-ZAX",
            "ZAX",
            "Remux-2160p",
            "bluray",
            2160,
            27 * gib,
        )
        remux_score, remux_hits = self.scorer.score(remux)
        self.assertNotIn("UHD Bluray Mid-Size Tier", remux_hits)
        self.assertLess(remux_score, zax_score)

        truehd = release(
            "Sinners.2025.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-ZAX",
            "ZAX",
            "Bluray-2160p",
            "bluray",
            2160,
            28 * gib,
        )
        truehd_score, truehd_hits = self.scorer.score(truehd)
        self.assertIn("TrueHD", truehd_hits)
        self.assertNotIn("TrueHD Block", truehd_hits)
        self.assertEqual(self.scorer.scores["TrueHD"], -10000)
        self.assertIn("UHD Bluray Mid-Size Tier", truehd_hits)
        self.assertLess(truehd_score, 1000)
        self.assertIsNone(pick([truehd], self.scorer))

    def test_quality_disc_beats_compact_hallowed(self):
        def disc(group, gib):
            return release(
                f"The.Dark.Knight.2008.2160p.UHD.BluRay.DDP7.1.Atmos.DV.HDR.x265-{group}",
                group,
                "Bluray-2160p",
                "bluray",
                2160,
                gib * 1024**3,
            )

        hallowed = disc("hallowed", 20)
        bhdstudio = disc("BHDStudio", 20)
        w4nk3r = disc("W4NK3R", 37)
        sphd = disc("SPHD", 40)
        trunks = disc("TRUNKS", 43)
        ctrlhd = disc("CtrlHD", 45)
        compact_w4nk3r = disc("W4NK3R", 20)
        hallowed_score, hallowed_hits = self.scorer.score(hallowed)
        bhdstudio_score, bhdstudio_hits = self.scorer.score(bhdstudio)
        w4nk3r_score, w4nk3r_hits = self.scorer.score(w4nk3r)
        sphd_score, sphd_hits = self.scorer.score(sphd)
        trunks_score, trunks_hits = self.scorer.score(trunks)
        ctrlhd_score, ctrlhd_hits = self.scorer.score(ctrlhd)
        compact_score, compact_hits = self.scorer.score(compact_w4nk3r)
        for hits in (w4nk3r_hits, sphd_hits, trunks_hits, ctrlhd_hits):
            self.assertIn("UHD Bluray Mid-Size Tier", hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", hallowed_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", bhdstudio_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", compact_hits)
        self.assertGreater(w4nk3r_score, hallowed_score)
        self.assertGreater(sphd_score, hallowed_score)
        self.assertGreater(trunks_score, hallowed_score)
        self.assertGreater(ctrlhd_score, hallowed_score)
        self.assertGreater(w4nk3r_score, bhdstudio_score)
        self.assertGreater(sphd_score, bhdstudio_score)
        self.assertGreater(trunks_score, bhdstudio_score)
        # Dumpstarr's tier order still applies inside the window.
        self.assertGreater(w4nk3r_score, sphd_score)
        self.assertGreater(sphd_score, trunks_score)
        # A compact tier-1 encode stays under hallowed. The bonus is the size window.
        self.assertGreater(hallowed_score, compact_score)
        self.assertGreater(hallowed_score, 1000)
        self.assertGreater(bhdstudio_score, 1000)
        chosen = pick(
            [hallowed, bhdstudio, compact_w4nk3r, w4nk3r, sphd, trunks, ctrlhd],
            self.scorer,
        )
        self.assertEqual(chosen[0]["releaseGroup"], "CtrlHD")
        fallback = pick([hallowed, bhdstudio, compact_w4nk3r], self.scorer)
        self.assertEqual(fallback[0]["releaseGroup"], "hallowed")

    def test_ma_webdl_loses_to_preferred_disc(self):
        disc = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.DTS-HD.MA.7.1.DV.HDR.x265-TRUNKS",
            "TRUNKS",
            "Bluray-2160p",
            "bluray",
            2160,
            43 * 1024**3,
        )
        ma = release(
            "The.Dark.Knight.2008.2160p.MA.iT.WEB-DL.DDP5.1.Atmos.DV.HDR.HDR10+.H.265-FLUX",
            "FLUX",
            "WEBDL-2160p",
            "webdl",
            2160,
            22 * 1024**3,
        )
        disc_score, disc_hits = self.scorer.score(disc)
        ma_score, ma_hits = self.scorer.score(ma)
        self.assertIn("UHD Bluray Mid-Size Tier", disc_hits)
        self.assertIn("DTS-HD MA", disc_hits)
        self.assertNotIn("TrueHD", disc_hits)
        self.assertIn("MA Preferred", ma_hits)
        self.assertIn("WEB Tier 01", ma_hits)
        self.assertGreater(disc_score, ma_score)
        self.assertGreater(disc_score, 1000)
        chosen = pick([ma, disc], self.scorer)
        self.assertEqual(chosen[0]["releaseGroup"], "TRUNKS")

    def test_trusted_truehd_loses_to_dts_hd_ma_and_hallowed(self):
        """TrueHD from a trusted group must not be approved or outrank DTS-HD MA or hallowed."""
        gib = 1024**3

        def bluray(title, group, size):
            return release(title, group, "Bluray-2160p", "bluray", 2160, size)

        # 40 GB is inside the 20-60 GB window, so the mid-size bonus applies.
        samples = [
            bluray("Fury.2014.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-SPHD", "SPHD", 40 * gib),
            bluray(
                "Thor.Love.and.Thunder.2022.2160p.UHD.BluRay.TrueHD.7.1.Atmos.HDR.x265-DON",
                "DON",
                40 * gib,
            ),
            bluray(
                "Sisu.Road.to.Revenge.2025.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-j3rico",
                "j3rico",
                40 * gib,
            ),
            bluray(
                "Supergirl.2026.2160p.UHD.BluRay.HDR10+.DoVi.TrueHD.7.1.Atmos.x265-SPHD",
                "SPHD",
                40 * gib,
            ),
        ]
        dts = bluray(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.DTS-HD.MA.5.1.DV.HDR.x265-W4NK3R",
            "W4NK3R",
            30 * gib,
        )
        hallowed = bluray(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.DDP5.1.Atmos.DV.HDR.x265-hallowed",
            "hallowed",
            20 * gib,
        )
        dts_score, dts_hits = self.scorer.score(dts)
        hallowed_score, hallowed_hits = self.scorer.score(hallowed)
        self.assertEqual(dts_score, 7605, dts_hits)
        self.assertIn("DTS-HD MA", dts_hits)
        self.assertIn("UHD Bluray Mid-Size Tier", dts_hits)
        self.assertIn("UHD Bluray Tier 01", dts_hits)
        self.assertNotIn("TrueHD", dts_hits)
        self.assertNotIn("TrueHD Block", dts_hits)
        dtsx = bluray(
            "Movie.2020.2160p.UHD.BluRay.DTS-X.7.1.DV.HDR.x265-W4NK3R",
            "W4NK3R",
            30 * gib,
        )
        dtsx_score, dtsx_hits = self.scorer.score(dtsx)
        self.assertEqual(dtsx_score, 7610, dtsx_hits)
        self.assertIn("DTS-X", dtsx_hits)
        self.assertNotIn("TrueHD Block", dtsx_hits)
        self.assertEqual(hallowed_score, 4055, hallowed_hits)
        self.assertIn("hallowed", hallowed_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", hallowed_hits)
        self.assertNotIn("TrueHD Block", hallowed_hits)
        for item in samples:
            score, hits = self.scorer.score(item)
            self.assertIn("TrueHD Block", hits, item["title"])
            self.assertLess(score, 1000, item["title"])
            self.assertLess(score, dts_score, item["title"])
            self.assertLess(score, hallowed_score, item["title"])
            self.assertIsNone(pick([item], self.scorer), item["title"])
            against_dts = pick([item, dts], self.scorer)
            against_hallowed = pick([item, hallowed], self.scorer)
            self.assertEqual(against_dts[0]["releaseGroup"], "W4NK3R", item["title"])
            self.assertEqual(against_hallowed[0]["releaseGroup"], "hallowed", item["title"])
        # The shared TrueHD format still skips trusted groups. The block is a
        # separate format scored only on Movies 2160p, so other profiles that
        # use TrueHD are not rewritten. Untrusted TrueHD stays on the original
        # penalty and does not take a second one.
        profiles = [
            row["quality_profile_name"]
            for row in self.db.execute(
                """
                SELECT quality_profile_name FROM quality_profile_custom_formats
                WHERE custom_format_name = 'TrueHD Block'
                """
            )
        ]
        self.assertEqual(profiles, ["Movies 2160p"])
        block_score = self.db.execute(
            """
            SELECT score FROM quality_profile_custom_formats
            WHERE custom_format_name = 'TrueHD Block' AND quality_profile_name = 'Movies 2160p'
            """
        ).fetchone()["score"]
        self.assertEqual(block_score, -10000)
        trusted_condition = self.db.execute(
            """
            SELECT negate, required FROM custom_format_conditions
            WHERE custom_format_name = 'TrueHD Block' AND name = 'Trusted Group'
            """
        ).fetchone()
        self.assertEqual(tuple(trusted_condition), (0, 1))
        still_exempt = self.db.execute(
            """
            SELECT negate, required FROM custom_format_conditions
            WHERE custom_format_name = 'TrueHD' AND name = 'Not Trusted Group'
            """
        ).fetchone()
        self.assertEqual(tuple(still_exempt), (1, 1))
        missing_exempt = self.db.execute(
            """
            SELECT negate, required FROM custom_format_conditions
            WHERE custom_format_name = 'TrueHD Missing' AND name = 'Not Trusted Group'
            """
        ).fetchone()
        self.assertEqual(tuple(missing_exempt), (1, 1))
        untrusted = bluray(
            "Movie.2020.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-SomeGroup",
            "SomeGroup",
            40 * gib,
        )
        untrusted_score, untrusted_hits = self.scorer.score(untrusted)
        self.assertIn("TrueHD", untrusted_hits)
        self.assertNotIn("TrueHD Block", untrusted_hits)
        self.assertLess(untrusted_score, 1000)
        with_dd = bluray(
            "Movie.2020.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DDP5.1.DV.HDR.x265-SPHD",
            "SPHD",
            40 * gib,
        )
        dd_score, dd_hits = self.scorer.score(with_dd)
        self.assertNotIn("TrueHD", dd_hits)
        self.assertNotIn("TrueHD Block", dd_hits)
        self.assertGreater(dd_score, 1000)

    def test_untrusted_truehd_big_encode_stays_rejected(self):
        blocked = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-SomeGroup",
            "SomeGroup",
            "Bluray-2160p",
            "bluray",
            2160,
            50 * 1024**3,
        )
        trusted = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.x265-W4NK3R",
            "W4NK3R",
            "Bluray-2160p",
            "bluray",
            2160,
            40 * 1024**3,
        )
        blocked_score, blocked_hits = self.scorer.score(blocked)
        trusted_score, trusted_hits = self.scorer.score(trusted)
        self.assertIn("TrueHD", blocked_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", blocked_hits)
        self.assertLess(blocked_score, 1000)
        self.assertIsNone(pick([blocked], self.scorer))
        self.assertNotIn("TrueHD", trusted_hits)
        self.assertIn("TrueHD Block", trusted_hits)
        self.assertIn("UHD Bluray Mid-Size Tier", trusted_hits)
        self.assertLess(trusted_score, 1000)
        self.assertIsNone(pick([trusted], self.scorer))

    def test_remux_and_oversize_lose_to_window_encode(self):
        encode = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.DDP7.1.Atmos.DV.HDR.x265-SPHD",
            "SPHD",
            "Bluray-2160p",
            "bluray",
            2160,
            45 * 1024**3,
        )
        oversize = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.DDP7.1.Atmos.DV.HDR.x265-W4NK3R",
            "W4NK3R",
            "Bluray-2160p",
            "bluray",
            2160,
            75 * 1024**3,
        )
        remux_quality = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.REMUX.HEVC.DV.HDR.DDP7.1.Atmos-SPHD",
            "SPHD",
            "Remux-2160p",
            "bluray",
            2160,
            75 * 1024**3,
        )
        remux_title = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.REMUX.HEVC.DV.HDR.DDP7.1.Atmos-W4NK3R",
            "W4NK3R",
            "Bluray-2160p",
            "bluray",
            2160,
            75 * 1024**3,
        )
        encode_score, encode_hits = self.scorer.score(encode)
        oversize_score, oversize_hits = self.scorer.score(oversize)
        remux_score, remux_hits = self.scorer.score(remux_title)
        self.assertIn("UHD Bluray Mid-Size Tier", encode_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", oversize_hits)
        self.assertNotIn("UHD Bluray Mid-Size Tier", remux_hits)
        self.assertNotIn("UHD Bluray Tier 01", remux_hits)
        self.assertGreater(encode_score, oversize_score)
        self.assertGreater(encode_score, remux_score)
        self.assertIsNone(self.scorer.ranks.get("Remux-2160p"))
        # No penalty: a lone oversize encode is still grabable.
        self.assertGreater(oversize_score, 1000)
        chosen = pick([remux_quality, remux_title, oversize, encode], self.scorer)
        self.assertEqual(chosen[0]["title"], encode["title"])
        self.assertGreater(chosen[1], oversize_score)

    def test_fallback_tiers_when_no_2160p(self):
        bluray_1080 = release(
            "The.Dark.Knight.2008.1080p.BluRay.DDP.5.1.x264-hallowed",
            "hallowed",
            "Bluray-1080p",
            "bluray",
            1080,
            8 * 1024**3,
        )
        bluray_720 = release(
            "The.Dark.Knight.2008.720p.BluRay.DD.5.1.x264-hallowed",
            "hallowed",
            "Bluray-720p",
            "bluray",
            720,
            4 * 1024**3,
        )
        uhd = release(
            "The.Dark.Knight.2008.2160p.UHD.BluRay.DDP7.1.Atmos.DV.HDR.x265-hallowed",
            "hallowed",
            "Bluray-2160p",
            "bluray",
            2160,
            20 * 1024**3,
        )
        score_1080, hits_1080 = self.scorer.score(bluray_1080)
        score_720, hits_720 = self.scorer.score(bluray_720)
        self.assertIn("HD Bluray Tier 03", hits_1080)
        self.assertIn("hallowed", hits_1080)
        self.assertIn("HD Bluray Tier 03", hits_720)
        self.assertNotIn("UHD Bluray Mid-Size Tier", hits_1080)
        self.assertNotIn("UHD Bluray Mid-Size Tier", hits_720)
        self.assertGreaterEqual(score_1080, 1000)
        self.assertGreaterEqual(score_720, 1000)
        only_hd = pick([bluray_720, bluray_1080], self.scorer)
        self.assertEqual(only_hd[0]["quality"]["quality"]["name"], "Bluray-1080p")
        only_720 = pick([bluray_720], self.scorer)
        self.assertEqual(only_720[0]["quality"]["quality"]["name"], "Bluray-720p")
        with_uhd = pick([bluray_720, bluray_1080, uhd], self.scorer)
        self.assertEqual(with_uhd[0]["quality"]["quality"]["name"], "Bluray-2160p")

    def test_group_missing_and_bad_hone_stay_upstream(self):
        dotted = release(
            "Movie.2020.2160p.UHD.BluRay.DDP5.1.DV.HDR.x265.hallowed",
            "",
            "Bluray-2160p",
            "bluray",
            2160,
            18 * 1024**3,
        )
        member = release(
            "Movie.2020.2160p.UHD.BluRay.DV.HDR.DDP.5.1.x265-Weasley-HONE",
            "Weasley-HONE",
            "Bluray-2160p",
            "bluray",
            2160,
            18 * 1024**3,
        )
        for item in (dotted, member):
            base_score, base_hits = self.base_scorer.score(item)
            layer_score, layer_hits = self.scorer.score(item)
            self.assertEqual(layer_score, base_score)
            self.assertEqual(layer_hits, base_hits)
        self.assertIn("Group Missing", self.scorer.score(dotted)[1])
        self.assertIn("HONE (Bad Name)", self.scorer.score(member)[1])
        names = [row["name"] for row in self.db.execute("SELECT name FROM custom_formats")]
        self.assertFalse(any("Name Fallback" in name or name.startswith("Lite ") for name in names))
        self.assertNotIn("Lite Group Missing Offset", names)
        self.assertNotIn("Lite HONE Family Offset", names)
        regexes = [row["name"] for row in self.db.execute("SELECT name FROM regular_expressions")]
        self.assertNotIn("Lite HONE Family", regexes)
        self.assertFalse(any(name.endswith(" Tail") for name in regexes))

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
        self.assertNotIn("TrueHD Block", allowed_hits)
        self.assertNotIn("TrueHD", trusted_hits)
        self.assertIn("TrueHD Block", trusted_hits)
        self.assertLess(trusted_score, 1000)

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
                self.assertTrue(
                    appeared <= {"UHD Bluray Mid-Size Tier", "TrueHD Block"}, item["title"]
                )
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
                self.assertFalse({"TrueHD", "TrueHD Block"} & set(after[2]), after_title)
        self.assertEqual(changes, EXPECTED_NEW)


if __name__ == "__main__":
    unittest.main(verbosity=2)
