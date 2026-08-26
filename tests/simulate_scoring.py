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
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_dir = os.environ.get("PCD_SCHEMA_PATH")
    if not schema_dir:
        candidate_deps_ops = os.path.join(repo_root, "deps", "schema", "ops")
        candidate_deps_root = os.path.join(repo_root, "deps", "schema")
        
        # Check standard sibling/parent deployment paths relative to repo root
        parent_dir = os.path.dirname(repo_root)
        candidate_sibling_deps = os.path.join(parent_dir, "deps", "schema", "ops")
        candidate_profilarr_deps = os.path.join(parent_dir, "config", "profilarr", "data", "databases", "707ac052-713c-47dc-a438-a9a8d0fd8c7e", "deps", "schema", "ops")
        
        if os.path.exists(candidate_deps_ops) and os.path.isdir(candidate_deps_ops):
            schema_dir = candidate_deps_ops
        elif os.path.exists(candidate_deps_root) and os.path.isdir(candidate_deps_root) and any(f.endswith(".sql") for f in os.listdir(candidate_deps_root)):
            schema_dir = candidate_deps_root
        elif os.path.exists(candidate_sibling_deps) and os.path.isdir(candidate_sibling_deps):
            schema_dir = candidate_sibling_deps
        elif os.path.exists(candidate_profilarr_deps) and os.path.isdir(candidate_profilarr_deps):
            schema_dir = candidate_profilarr_deps
        else:
            raise FileNotFoundError(
                "Could not automatically locate Dictionarry schema ops directory. "
                "Please set the PCD_SCHEMA_PATH environment variable."
            )

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

    ops_dir = os.path.join(repo_root, "ops")
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

def make_python_re_compatible(pat):
    p = pat.replace('(?i)', '').replace('(?-i)', '')
    # Convert (?<=^|...) and (?<=...|^)
    p = re.sub(r'\(\?<=\^\|([^)]+)\)', r'(?:^|(?<=\1))', p)
    p = re.sub(r'\(\?<=([^)]+)\|\^\)', r'(?:(?<=\1)|^)', p)
    p = p.replace(r'(?<=\b[12]\d{3}\b).*?', r'(?:[12]\d{3}.*?)')
    
    # Specific upstream variable-width lookbehinds
    p = p.replace(r'(?<!e-?)', r'(?:(?<!e)(?<!e-))')
    p = p.replace(r'(?<!NON.?)', r'(?:(?<!NON)(?<!NON.))')
    p = p.replace(r'(?<!HD[._ -]|HD)', r'(?:(?<!HD[._ -])(?<!HD))')
    p = p.replace(r'(?<!DTS[ .-]?HD[ .-]?)(MA|YKW)', r'(?:(?<!DTS-HD )(?<!DTS-HD.)(?<!DTS HD.)(?<!DTS.HD.)(?<!DTSHD.))\b(MA|YKW)')
    p = p.replace(r'(?<=\bS\d+\b).*(\b(AI)\b)', r'\bS\d+\b.*?\bAI\b')
    p = p.replace(r'(?<=\bS\d+\b).*\b(Extra(s)?|Bonus|Deleted[ ._-]Scene(s)?|Extended[ ._-]Clip)\b', r'\bS\d+\b.*?\b(Extra(s)?|Bonus|Deleted[ ._-]Scene(s)?|Extended[ ._-]Clip)\b')
    p = p.replace(r'(?<=\bS\d+(E\d+)?\b).*\bDUB(BED)?\b', r'\bS\d+(?:E\d+)?\b.*?\bDUB(?:BED)?\b')
    p = p.replace(r'(?<=^(?!.*(HDR|HULU|REMUX|BLU[-]?RAY)).*?)\b(DV|Dovi|Dolby[ .]?Vision)\b', r'^(?!.*(HDR|HULU|REMUX|BLU[-]?RAY)).*?\b(DV|Dovi|Dolby[ .]?Vision)\b')
    p = p.replace(r'(?<=^(?!.*\b(HLG|PQ|SDR)(\b|\d)).*?)', r'^(?!.*\b(HLG|PQ|SDR)(\b|\d)).*?')
    return p

class ScoringContext:
    def __init__(self, conn):
        self.profiles = {}
        # Pre-cache profiles and their rules
        prof_rows = conn.execute("SELECT name, minimum_custom_format_score, upgrade_until_score FROM quality_profiles").fetchall()
        for p_name, min_s, upg_s in prof_rows:
            self.profiles[p_name] = {"min_score": min_s, "upgrade_until": upg_s, "rules": {}}
            
        # Pre-compile regular expressions
        pat_cache = {}
        for r_name, p_str in conn.execute("SELECT name, pattern FROM regular_expressions").fetchall():
            clean_pat = make_python_re_compatible(p_str)
            try:
                pat_cache[r_name] = (re.compile(clean_pat, re.IGNORECASE), None)
            except re.error:
                pat_cache[r_name] = (None, clean_pat)

        # Pre-cache rules per profile and arr_type
        for p_name in self.profiles:
            for arr in ("radarr", "sonarr"):
                rules = conn.execute("""
                    SELECT qpcf.custom_format_name, qpcf.score
                    FROM quality_profile_custom_formats qpcf
                    WHERE qpcf.quality_profile_name = ?
                      AND (qpcf.arr_type = 'all' OR qpcf.arr_type = ?)
                """, (p_name, arr)).fetchall()
                
                compiled_rules = []
                for cf_name, score in rules:
                    cond_rows = conn.execute("""
                        SELECT cfc.name, cfc.type, cfc.negate, cfc.required
                        FROM custom_format_conditions cfc
                        WHERE cfc.custom_format_name = ?
                          AND (cfc.arr_type = 'all' OR cfc.arr_type = ?)
                    """, (cf_name, arr)).fetchall()
                    
                    if not cond_rows:
                        continue
                        
                    optional_types = set(c[1] for c in cond_rows if c[3] == 0)
                    compiled_conds = []
                    
                    for c_name, c_type, negate, required in cond_rows:
                        pats = []
                        if c_type in ("release_title", "release_group"):
                            p_rows = conn.execute("""
                                SELECT cp.regular_expression_name FROM condition_patterns cp
                                WHERE cp.custom_format_name = ? AND cp.condition_name = ?
                            """, (cf_name, c_name)).fetchall()
                            for (rn,) in p_rows:
                                if rn in pat_cache:
                                    pats.append(pat_cache[rn])
                                    
                        sources = set()
                        if c_type == "source":
                            for (s_val,) in conn.execute("SELECT source FROM condition_sources WHERE custom_format_name = ? AND condition_name = ?", (cf_name, c_name)).fetchall():
                                sources.add(s_val.lower().replace("_", "").replace("-", ""))
                                
                        res_set = set()
                        if c_type == "resolution":
                            for (r_val,) in conn.execute("SELECT resolution FROM condition_resolutions WHERE custom_format_name = ? AND condition_name = ?", (cf_name, c_name)).fetchall():
                                res_set.add(r_val.lower().replace("_", "").replace("-", ""))
                                
                        compiled_conds.append({
                            "name": c_name,
                            "type": c_type,
                            "negate": bool(negate),
                            "required": bool(required),
                            "pats": pats,
                            "sources": sources,
                            "res_set": res_set
                        })
                        
                    compiled_rules.append({
                        "cf_name": cf_name,
                        "score": score,
                        "optional_types": optional_types,
                        "conds": compiled_conds
                    })
                    
                self.profiles[p_name]["rules"][arr] = compiled_rules

_GLOBAL_SCORING_CONTEXT = None

def get_scoring_context(conn):
    global _GLOBAL_SCORING_CONTEXT
    if _GLOBAL_SCORING_CONTEXT is None:
        _GLOBAL_SCORING_CONTEXT = ScoringContext(conn)
    return _GLOBAL_SCORING_CONTEXT

def evaluate_release(conn, release_title, profile_name, arr_type="radarr"):
    ctx = get_scoring_context(conn)
    if profile_name not in ctx.profiles:
        raise ValueError(f"Unknown profile: {profile_name}")
        
    p_data = ctx.profiles[profile_name]
    min_score = p_data["min_score"]
    upgrade_until = p_data["upgrade_until"]
    rules = p_data["rules"].get(arr_type, [])
    
    tokens = parse_release_tokens(release_title)
    total_score = 0
    matched_cfs = []
    
    for rule in rules:
        cf_name = rule["cf_name"]
        score = rule["score"]
        optional_types = rule["optional_types"]
        conds = rule["conds"]
        
        all_required_met = True
        matched_optional_types = set()
        
        for cond in conds:
            c_type = cond["type"]
            negate = cond["negate"]
            required = cond["required"]
            cond_matched = False
            
            if c_type == "release_title":
                for compiled_re, raw_pat in cond["pats"]:
                    if compiled_re:
                        if compiled_re.search(release_title):
                            cond_matched = True
                            break
                    elif raw_pat and regex_match(raw_pat, release_title):
                        cond_matched = True
                        break
            elif c_type == "release_group":
                for compiled_re, raw_pat in cond["pats"]:
                    if compiled_re:
                        if (tokens["group"] and compiled_re.search(tokens["group"])) or compiled_re.search(release_title):
                            cond_matched = True
                            break
                    elif raw_pat and ((tokens["group"] and regex_match(raw_pat, tokens["group"])) or regex_match(raw_pat, release_title)):
                        cond_matched = True
                        break
            elif c_type == "source":
                s_set = cond["sources"]
                if "bluray" in s_set and tokens["is_bluray"]: cond_matched = True
                if ("webdl" in s_set or "web_dl" in s_set) and tokens["is_webdl"]: cond_matched = True
                if "webrip" in s_set and tokens["is_webrip"]: cond_matched = True
                if "hdtv" in s_set and tokens["is_hdtv"]: cond_matched = True
            elif c_type == "resolution":
                r_set = cond["res_set"]
                if "2160p" in r_set and tokens["is_2160p"]: cond_matched = True
                if "1080p" in r_set and tokens["is_1080p"]: cond_matched = True
                
            if negate:
                cond_matched = not cond_matched
                
            if required:
                if not cond_matched:
                    all_required_met = False
            else:
                if cond_matched:
                    matched_optional_types.add(c_type)
                    
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
            "category": "Pure AV1 2160p HQ (R&H ampersand variant - Task 4 Top Priority)",
            "title": "The.Shawshank.Redemption.1994.2160p.BluRay.DV.HDR10.AV1.DTS.5.1-R&H",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 2160p HQ (R and H spaced variant)",
            "title": "The.Shawshank.Redemption.1994.2160p.BluRay.DV.HDR10.AV1.DTS.5.1-R and H",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 2160p HQ (Smokindevil - Task 4 Item 2)",
            "title": "The.Shawshank.Redemption.1994.2160p.UHD.BluRay.DD+5.1.HDR.AV1-Smokindevil",
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
            "category": "Pure AV1 2160p HQ (CoSMiCSuRFeR Quality Encoder - Beats Compact Tier)",
            "title": "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.Extended.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR10+.AV1-CoSMiCSuRFeR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 6000
        },
        {
            "category": "Pure AV1 2160p HQ (CoSMiCSuRFeR site-tagged [rarbg])",
            "title": "Dune.Part.Two.2024.2160p.HDR.AV1-CoSMiCSuRFeR[rarbg]",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 4500
        },
        {
            "category": "Pure AV1 2160p HQ (CoSMiCSuRFeR no extension)",
            "title": "Dune.Part.Two.2024.2160p.HDR.AV1-CoSMiCSuRFeR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 4500
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
            "category": "Pure AV1 1080p HQ (UserHEVC - Task 4 Item 4)",
            "title": "The.Matrix.1999.1080p.AV1.Opus-UserHEVC.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2300
        },
        {
            "category": "Pure AV1 1080p HQ (RAV1NE prefix - Task 4 Item 4)",
            "title": "[RAV1NE] Interstellar 2014 1080p AV1 10bit.mkv",
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
            "category": "Pure AV1 Anime (Ironclad - Task 4 Item 4)",
            "title": "[Ironclad] Sousou no Frieren - 01 [AV1 1080p 10bit Opus].mkv",
            "profile": "Anime 1080p AV1",
            "arr_type": "sonarr",
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

        # --- 3. TIERED X265 FALLBACK RELEASES (BAND 1000 - 3400 for 2160p, 1000 - 3400 for 1080p fallback) ---
        {
            "category": "SDR 2160p WEB-DL Tier 1 (FLUX - Constraint 1 Test)",
            "title": "Die.My.Love.2025.2160p.AMZN.WEB-DL.DDP5.1.H.265-FLUX",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 3400
        },
        {
            "category": "hallowed-class 2160p BluRay HDR10+ (Constraint 2 Test - Top of Fallback)",
            "title": "Die.My.Love.2025.UHD.BluRay.2160p.DDP.5.1.HDR10+.x265-hallowed",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1500,
            "max_band": 3400
        },
        {
            "category": "Stacked Tiered 2160p x265 (Constraint 3 Test - Must be < Bare AV1 3500)",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR.HDR10+.CRIT-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 3400
        },
        {
            "category": "Tiered x265 Fallback (HONE WEB-DL Tier 2)",
            "title": "Dune.Part.Two.2024.2160p.UHD.WEB-DL.DDP5.1.Atmos.DV.HDR.x265-HONE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 3400
        },
        {
            "category": "1080p Tiered Fallback in 2160p Profile (Constraint 7 Test - DON)",
            "title": "Oppenheimer.2023.1080p.BluRay.x265.TrueHD.7.1.CRIT-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 3400
        },
        {
            "category": "Tiered x265 Fallback (DON BluRay 1080p Quality Tier 1 in 1080p Profile)",
            "title": "Oppenheimer.2023.1080p.BluRay.x265.DTS-HD.MA.7.1.CRIT-DON",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 500,
            "max_band": 3400
        },

        # --- 4. RANDOM UNTIERED X265 & CODEC-LESS LEAK REJECTIONS (< 1000 for 2160p, < 500 for 1080p) ---
        {
            "category": "Random Untiered 2160p x265 (Constraint 4 Test - Max Features Untiered Must Fail < 1000)",
            "title": "Gladiator.2000.2160p.UHD.BluRay.x.265.TrueHD.Atmos.7.1.DV.HDR.HDR10+-RandomGroup",
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
        
        # --- 5. BARE AV1 RELEASES (Constraint 5 Test - Minimal features must beat all non-AV1) ---
        {
            "category": "Bare SDR AV1 2160p (Constraint 5 Test - Must Score >= 3500)",
            "title": "Die.My.Love.2025.2160p.AV1.DD5.1-BareGroup.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3500
        },
        {
            "category": "Bare SDR AV1 1080p (Constraint 8 Test - Must Beat Stacked 1080p x265)",
            "title": "Die.My.Love.2025.1080p.AV1.DD5.1-BareGroup.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3500
        },
        
        # --- 6. ADVERSARIAL FALSE-POSITIVE CHECK (-edge2020HD) ---
        {
            "category": "Adversarial Check (-edge2020HD must NOT match compact encoder)",
            "title": "Top.Gun.Maverick.2022.1080p.AV1.10bit.DDP5.1-edge2020HD",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True
        },
        
        # --- 7. X264 & REMUX REJECTIONS (Constraint 6 Test) ---
        {
            "category": "x264 Release (Hard Reject - Constraint 6 Test)",
            "title": "Oppenheimer.2023.1080p.BluRay.H.264.DTS-HD.MA.7.1.CRIT-DON",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Remux Release (Hard Reject - Constraint 6 Test)",
            "title": "Die.My.Love.2025.2160p.UHD.BluRay.Remux.HEVC.DV.HDR.Atmos-CiNEPHiLES.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },

        # --- 8. HYGIENE & ANTI-TRASH REJECTIONS (-10000) ---
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
        {
            "category": "Hygiene Rejection (Banned ENTROPY Fake/Corrupted)",
            "title": "Movie.Title.2024.1080p.WEBRip.AV1-ENTROPY.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Hygiene Rejection (Banned ENTROPY Lowercase -entropy)",
            "title": "Movie.Title.2024.1080p.WEBRip.AV1-entropy.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Junk-Line Separation (R&H Upscale Rejected Despite Bonus)",
            "title": "The.Shawshank.Redemption.1994.1080p.Upscale.AV1-R and H.mkv",
            "profile": "Movies 1080p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Junk-Line Separation (LUCY TC Rejected Despite Bonus)",
            "title": "Deadpool.and.Wolverine.2024.TC.AV1-LUCY.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Junk-Line Separation (LUCY Ts Rejected Despite Bonus)",
            "title": "Deadpool.and.Wolverine.2024.Ts.AV1-LUCY.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Junk-Line Separation (LUCY Telesync Rejected Despite Bonus)",
            "title": "Deadpool.and.Wolverine.2024.Telesync.AV1-LUCY.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Junk-Line Separation (LUCY SCREENER Rejected Despite Bonus)",
            "title": "Deadpool.and.Wolverine.2024.SCREENER.AV1-LUCY.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
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
            "category": "Storage Saver In Storage Profile (-LUCY[TGx])",
            "title": "Fallout.S01E01.1080p.AV1-LUCY[TGx].mkv",
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
        },
        {
            "category": "Quality Encoder in Storage Profile (Penalized -1000, Ranks Below Storage Savers)",
            "title": "Fallout.S01E01.1080p.AV1-CoSMiCSuRFeR.mkv",
            "profile": "TV 1080p AV1 Storage",
            "arr_type": "sonarr",
            "expect_pass": True,
            "max_band": 3000
        },

        # --- 9. CODEC-AGNOSTIC TIER SCORING (TAoE AV1 + Tier 1 Quality) ---
        {
            "category": "Codec-Agnostic Tier Scoring (TAoE AV1 + Tier 1 Quality)",
            "title": "Dune.Part.Two.2024.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-TAoE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 6000
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
        print(f"  Score:   {score} -> Clears Profile Minimum: {passed_cutoff} (Expected: {expect_pass})")
        print(f"  Matched Formats:")
        for cf, s in matched:
            print(f"    - {cf:<30}: {s:>+6}")

    # --- 9. UPGRADE SCORE INCREMENT BATTERY (op 907: increment = 300) ---
    increment_cases = [
        {"name": "Minor service swap (1350 HMAX vs 1400 AMZN)", "existing": 1350, "new": 1400, "expect_upgrade": False},
        {"name": "Major AV1 upgrade (1400 x265 vs 2300 AV1)", "existing": 1400, "new": 2300, "expect_upgrade": True},
        {"name": "Tier upgrade (1400 vs 1700)", "existing": 1400, "new": 1700, "expect_upgrade": True},
    ]
    inc_val = conn.execute("SELECT upgrade_score_increment FROM quality_profiles WHERE name = 'TV 2160p AV1'").fetchone()[0]
    print(f"\n=== UPGRADE SCORE INCREMENT BATTERY (op 907: increment = {inc_val}) ===")
    for c in increment_cases:
        delta = c["new"] - c["existing"]
        fires = delta >= inc_val
        passed = (fires == c["expect_upgrade"])
        print(f"[{'PASS' if passed else 'FAIL'}] {c['name']} (Delta: +{delta}) -> Upgrade: {fires} (Expected: {c['expect_upgrade']})")
        if not passed:
            failed_tests += 1
        else:
            passed_tests += 1
            
    print("\n================================================================================")
    print(f"SIMULATION SUMMARY: {passed_tests} Passed, {failed_tests} Failed (Total: {passed_tests + failed_tests})")
    print("================================================================================")
    
    return failed_tests == 0

if __name__ == "__main__":
    success = run_simulation_battery()
    sys.exit(0 if success else 1)
