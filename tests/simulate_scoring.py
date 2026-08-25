#!/usr/bin/env python3
"""
Phase 4 + Fallback Ladder Unified Scoring Simulation Battery
Evaluates:
- Band 1: Pure AV1 Releases (>= 2300) -> Highest priority within quality group
- Band 2: Tiered x265 Fallbacks (1000 - 1400) -> Accepted above min cutoff, auto-upgrades to AV1
- Band 3: Random Untiered x265 / Codec-less Releases (< 1000 for 2160p, < 500 for 1080p) -> Rejected
- Band 4: Codec-less AV1-unnamed Releases -> Rejected (documented trade-off)
- Band 5: Legacy x264 Releases (< 0) -> Hard rejected
- Band 6: Universal Hygiene (CAM, Screener, Upscale, 3D, Full Disc, Banned Groups) -> Hard rejected (-10000)
"""

import sqlite3
import os
import re
import sys
import subprocess

def build_compiled_db():
    schema_dir = "/home/user/desktop-streamer/config/profilarr/data/databases/707ac052-713c-47dc-a438-a9a8d0fd8c7e/deps/schema/ops"
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    
    def get_order(fn):
        m = re.match(r"^(\d+)\.", fn)
        return int(m.group(1)) if m else float("inf")

    conn.create_function("qp", 1, lambda name: 1)
    conn.create_function("cf", 1, lambda name: 1)
    conn.create_function("dp", 1, lambda name: 1)
    conn.create_function("tag", 1, lambda name: 1)

    for f in sorted(os.listdir(schema_dir), key=get_order):
        if f.endswith(".sql"):
            with open(os.path.join(schema_dir, f), "r") as sf:
                conn.executescript(sf.read())

    ops_dir = "/home/user/desktop-streamer/database-AV1/ops"
    for f in sorted(os.listdir(ops_dir), key=get_order):
        if f.endswith(".sql"):
            with open(os.path.join(ops_dir, f), "r") as opf:
                conn.executescript(opf.read())
                
    return conn

def parse_release_tokens(title):
    group = ""
    m_bracket = re.match(r"^\[([a-zA-Z0-9_\-\.]+)\]", title)
    if m_bracket:
        group = m_bracket.group(1)
    else:
        m_hyphen = re.search(r"-([a-zA-Z0-9_\-\.]+?)(?:\[[a-zA-Z0-9_\-\.]+\])?(?:\.[a-zA-Z0-9]{2,4})?$", title)
        if m_hyphen:
            group = m_hyphen.group(1)
            
    is_bluray = bool(re.search(r"\b(Blu[-._]?ray|BD|UHD)\b", title, re.IGNORECASE))
    is_webdl = bool(re.search(r"\b(WEB[-._]?DL|WEBDL)\b", title, re.IGNORECASE))
    is_webrip = bool(re.search(r"\b(WEBRip)\b", title, re.IGNORECASE))
    is_hdtv = bool(re.search(r"\b(HDTV)\b", title, re.IGNORECASE))
    is_2160p = bool(re.search(r"\b(2160p|4K|UHD)\b", title, re.IGNORECASE))
    is_1080p = bool(re.search(r"\b(1080p|1080i)\b", title, re.IGNORECASE))
    
    return {
        "group": group,
        "is_bluray": is_bluray,
        "is_webdl": is_webdl,
        "is_webrip": is_webrip,
        "is_hdtv": is_hdtv,
        "is_2160p": is_2160p,
        "is_1080p": is_1080p
    }

def regex_match(pattern_str, text):
    clean_pat = pattern_str.replace("(?i)", "").replace("(?-i)", "")
    try:
        return bool(re.search(clean_pat, text, re.IGNORECASE))
    except re.error:
        res = subprocess.run(
            ["node", "-e", "const re = new RegExp(process.argv[1], 'i'); process.exit(re.test(process.argv[2]) ? 0 : 1);", clean_pat, text],
            capture_output=True
        )
        return res.returncode == 0

def evaluate_release(conn, release_title, profile_name, arr_type="radarr"):
    prof = conn.execute("SELECT minimum_custom_format_score, upgrade_until_score FROM quality_profiles WHERE name = ?", (profile_name,)).fetchone()
    if not prof: raise ValueError(f"Unknown profile: {profile_name}")
    min_score, upgrade_until = prof
    tokens = parse_release_tokens(release_title)
    
    rules = conn.execute("""
        SELECT qpcf.custom_format_name, qpcf.score
        FROM quality_profile_custom_formats qpcf
        WHERE qpcf.quality_profile_name = ?
          AND (qpcf.arr_type = 'all' OR qpcf.arr_type = ?)
    """, (profile_name, arr_type)).fetchall()
    
    total_score = 0
    matched_cfs = []
    
    for cf_name, score in rules:
        conds = conn.execute("""
            SELECT cfc.name, cfc.type, cfc.negate, cfc.required
            FROM custom_format_conditions cfc
            WHERE cfc.custom_format_name = ?
              AND (cfc.arr_type = 'all' OR cfc.arr_type = ?)
        """, (cf_name, arr_type)).fetchall()
        
        if not conds: continue
            
        has_required_conds = any(c[3] == 1 for c in conds)
        optional_types = set(c[1] for c in conds if c[3] == 0)
        all_required_met = True
        matched_optional_types = set()
        
        for cond_name, cond_type, negate, required in conds:
            cond_matched = False
            if cond_type == "release_title":
                patterns = conn.execute("SELECT re.pattern FROM condition_patterns cp JOIN regular_expressions re ON cp.regular_expression_name = re.name WHERE cp.custom_format_name = ? AND cp.condition_name = ?", (cf_name, cond_name)).fetchall()
                for (pat_str,) in patterns:
                    if regex_match(pat_str, release_title):
                        cond_matched = True
                        break
            elif cond_type == "release_group":
                patterns = conn.execute("SELECT re.pattern FROM condition_patterns cp JOIN regular_expressions re ON cp.regular_expression_name = re.name WHERE cp.custom_format_name = ? AND cp.condition_name = ?", (cf_name, cond_name)).fetchall()
                for (pat_str,) in patterns:
                    # In Radarr, ReleaseGroupSpecification matches group or title
                    if (tokens["group"] and regex_match(pat_str, tokens["group"])) or regex_match(pat_str, release_title):
                        cond_matched = True
                        break
            elif cond_type == "source":
                cond_sources = [r[0].lower().replace("_", "").replace("-", "") for r in conn.execute("SELECT source FROM condition_sources WHERE custom_format_name = ? AND condition_name = ?", (cf_name, cond_name)).fetchall()]
                if "bluray" in cond_sources and tokens["is_bluray"]: cond_matched = True
                if ("webdl" in cond_sources or "web_dl" in cond_sources) and tokens["is_webdl"]: cond_matched = True
                if "webrip" in cond_sources and tokens["is_webrip"]: cond_matched = True
                if "hdtv" in cond_sources and tokens["is_hdtv"]: cond_matched = True
            elif cond_type == "resolution":
                cond_res = [r[0].lower().replace("_", "").replace("-", "") for r in conn.execute("SELECT resolution FROM condition_resolutions WHERE custom_format_name = ? AND condition_name = ?", (cf_name, cond_name)).fetchall()]
                if "2160p" in cond_res and tokens["is_2160p"]: cond_matched = True
                if "1080p" in cond_res and tokens["is_1080p"]: cond_matched = True
                
            if negate: cond_matched = not cond_matched
            if required:
                if not cond_matched: all_required_met = False
            else:
                if cond_matched: matched_optional_types.add(cond_type)
                
        # Radarr requirement: all required specs must match AND every present optional specification type must have at least one match
        if optional_types:
            cf_matched = all_required_met and (matched_optional_types == optional_types)
        else:
            cf_matched = all_required_met
            
        if cf_matched:
            total_score += score
            matched_cfs.append((cf_name, score))
            
    passed_cutoff = total_score >= min_score
    return total_score, min_score, upgrade_until, passed_cutoff, matched_cfs

def run_simulation_battery():
    conn = build_compiled_db()
    
    test_corpus = [
        # --- 1. PURE AV1 2160p RELEASES (BAND >= 2300) ---
        {
            "category": "Pure AV1 2160p HQ (standard suffix)",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 2160p HQ (site-tagged [rarbg])",
            "title": "The.Matrix.1999.2160p.HDR.UHD.BluRay.AV1.DDP5.1-dAV1nci[rarbg]",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 2160p HQ (site-tagged [TGx])",
            "title": "LOTR.The.Return.Of.The.King.2003.PROPER.Bluray.2160p.AV1.HDR10.OPUS.7.1-UH[TGx]",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 2160p HQ (bracketed -[dAV1nci])",
            "title": "Dune.Part.Two.2024.2160p.HDR.AV1-[dAV1nci].mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 2160p TV (WEB-DL edge2020)",
            "title": "House.of.the.Dragon.S02E01.2160p.UHD.WEB-DL.AV1.DDP5.1.Atmos.DV.HDR.AMZN.DSNP-edge2020",
            "profile": "TV 2160p AV1",
            "arr_type": "sonarr",
            "expect_pass": True,
            "min_band": 2300
        },
        
        # --- 2. PURE AV1 1080p HQ & ANIME RELEASES (BAND >= 2300) ---
        {
            "category": "Pure AV1 1080p HQ",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.1080p.Bluray.OPUS.7.1.AV1-WhiskeyJack",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 1080p HQ (edge2020 valid)",
            "title": "Top.Gun.Maverick.2022.1080p.AV1.10bit.DDP5.1-edge2020",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 Anime (Trix)",
            "title": "[Trix] Frieren - Beyond Journey's End (01-28) [AV1 10bit 1080p Opus].mkv",
            "profile": "Anime 1080p AV1",
            "arr_type": "sonarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 Anime (Breeze)",
            "title": "[Breeze] Jujutsu Kaisen - S02 [1080p AV1 10bit Opus].mkv",
            "profile": "Anime 1080p AV1",
            "arr_type": "sonarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 Anime (AV1ARY)",
            "title": "[AV1ARY] Dungeon Meshi [1080p AV1 10bit Dual-Audio].mkv",
            "profile": "Anime 1080p AV1",
            "arr_type": "sonarr",
            "expect_pass": True,
            "min_band": 2300
        },

        # --- 3. TIERED X265 FALLBACK RELEASES (BAND 1000 - 1400 for 2160p, 500 - 1400 for 1080p) ---
        {
            "category": "Tiered x265 Fallback (FLUX WEB-DL Tier 1)",
            "title": "House.of.the.Dragon.S02E01.2160p.UHD.WEB-DL.DDP5.1.Atmos.DV.HDR.H.265-FLUX",
            "profile": "TV 2160p AV1",
            "arr_type": "sonarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 1400
        },
        {
            "category": "Tiered x265 Fallback (HONE WEB-DL Tier 2)",
            "title": "Dune.Part.Two.2024.2160p.UHD.WEB-DL.DDP5.1.Atmos.DV.HDR.x265-HONE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 1400
        },
        {
            "category": "Tiered x265 Fallback (DON BluRay 2160p Quality Tier 1)",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR.CRIT-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 1400
        },
        {
            "category": "Tiered x265 Fallback (DON BluRay 1080p Quality Tier 1)",
            "title": "Oppenheimer.2023.1080p.BluRay.x265.DTS-HD.MA.7.1.CRIT-DON",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 500,
            "max_band": 1400
        },

        # --- 4. RANDOM UNTIERED X265 & CODEC-LESS LEAK REJECTIONS (< 1000 for 2160p, < 500 for 1080p) ---
        {
            "category": "Random Untiered 2160p x265 (Rejected)",
            "title": "Gladiator.2000.2160p.UHD.BluRay.x.265.TrueHD.Atmos.7.1.DV.HDR-RandomGroup",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 999
        },
        {
            "category": "Random Untiered 1080p x265 (Point 2 Test - Must Fail < 500)",
            "title": "Gladiator.2000.1080p.BluRay.x265.TrueHD.Atmos.7.1-RandomGroup",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 499
        },
        {
            "category": "Codec-less Release (No Codec Token -> Rejected)",
            "title": "Gladiator.2000.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR-UntieredGroup",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 999
        },
        {
            "category": "Codec-less AV1-unnamed Release (Documented Trade-off -> Rejected)",
            "title": "Top.Gun.Maverick.2022.1080p.10bit.DDP5.1-edge2020",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 499
        },
        
        # --- 5. ADVERSARIAL FALSE-POSITIVE CHECK (-edge2020HD) ---
        {
            "category": "Adversarial Check (-edge2020HD must NOT match compact encoder)",
            "title": "Top.Gun.Maverick.2022.1080p.AV1.10bit.DDP5.1-edge2020HD",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True
        },
        
        # --- 6. X264 ANYTHING (HARD REJECT < 0) ---
        {
            "category": "x264 Release (Hard Reject)",
            "title": "Oppenheimer.2023.1080p.BluRay.H.264.DTS-HD.MA.7.1.CRIT-DON",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },

        # --- 7. HYGIENE & ANTI-TRASH REJECTIONS (-10000) ---
        {
            "category": "Hygiene Rejection (CAM)",
            "title": "Dune.Part.Two.2024.CAM.AV1-TestGroup.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False
        },
        {
            "category": "Hygiene Rejection (Upscale)",
            "title": "Gladiator.II.2024.1080p.Upscale.AV1-Test.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False
        },
        {
            "category": "Hygiene Rejection (3D)",
            "title": "Avatar.The.Way.of.Water.2022.3D.1080p.AV1.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False
        },
        {
            "category": "Hygiene Rejection (Full Disc)",
            "title": "Gladiator.2000.2160p.UHD.COMPLETE.BLURAY.AV1.iso",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False
        },
        {
            "category": "Hygiene Rejection (Banned YTS)",
            "title": "Top.Gun.2022.1080p.AV1-YTS.mp4",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False
        },
        
        # --- 8. STORAGE SAVER PROFILE TESTS ---
        {
            "category": "Storage Saver In Storage Profile (-PSA[ettv])",
            "title": "Fallout.S01E01.1080p.AV1-PSA[ettv].mkv",
            "profile": "TV 1080p AV1 Storage",
            "arr_type": "sonarr",
            "expect_pass": True
        },
        {
            "category": "Storage Saver In Storage Profile (-GalaxyRG[TGx])",
            "title": "Fallout.S01E01.1080p.AV1-GalaxyRG[TGx].mkv",
            "profile": "TV 1080p AV1 Storage",
            "arr_type": "sonarr",
            "expect_pass": True
        },
        {
            "category": "Storage Saver In HQ Profile (Penalty Test)",
            "title": "Fallout.S01E01.1080p.AV1-MeGusta.mkv",
            "profile": "TV 1080p AV1 HQ",
            "arr_type": "sonarr",
            "expect_pass": True
        }
    ]
    
    print("================================================================================")
    print("UNIFIED PHASE 4 & FALLBACK LADDER SIMULATION BATTERY REPORT")
    print("================================================================================")
    
    passed_tests = 0
    failed_tests = 0
    
    for case in test_corpus:
        title = case["title"]
        profile = case["profile"]
        arr_type = case["arr_type"]
        expect_pass = case["expect_pass"]
        category = case["category"]
        
        score, min_score, upgrade_until, passed_cutoff, matched = evaluate_release(conn, title, profile, arr_type)
        
        test_success = (passed_cutoff == expect_pass)
        if "min_band" in case and score < case["min_band"]:
            test_success = False
        if "max_band" in case and score > case["max_band"]:
            test_success = False
            
        # Extra assertion for adversarial edge2020HD
        if "edge2020HD" in title:
            matched_cf_names = [m[0] for m in matched]
            if "AV1 Compact Encoders" in matched_cf_names:
                test_success = False
                
        if test_success:
            status_str = "[PASS]"
            passed_tests += 1
        else:
            status_str = "[FAIL]"
            failed_tests += 1
            
        print(f"\n{status_str} Category: {category}")
        print(f"  Title:   {title}")
        print(f"  Profile: {profile} (Min Cutoff: {min_score}, Upgrade Until: {upgrade_until})")
        print(f"  Score:   {score} -> Accepted: {passed_cutoff} (Expected: {expect_pass})")
        print(f"  Matched Formats:")
        for cf, s in matched:
            print(f"    - {cf:<30}: {s:>+6}")
            
    print("\n================================================================================")
    print(f"SIMULATION SUMMARY: {passed_tests} Passed, {failed_tests} Failed (Total: {passed_tests + failed_tests})")
    print("================================================================================")
    
    return failed_tests == 0

if __name__ == "__main__":
    success = run_simulation_battery()
    sys.exit(0 if success else 1)
