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
                                
                        size_bounds = None
                        if c_type == "size":
                            s_row = conn.execute("SELECT min_bytes, max_bytes FROM condition_sizes WHERE custom_format_name = ? AND condition_name = ?", (cf_name, c_name)).fetchone()
                            if s_row:
                                size_bounds = (s_row[0], s_row[1])
                                
                        compiled_conds.append({
                            "name": c_name,
                            "type": c_type,
                            "negate": bool(negate),
                            "required": bool(required),
                            "pats": pats,
                            "sources": sources,
                            "res_set": res_set,
                            "size_bounds": size_bounds
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

def evaluate_release(conn, release_title, profile_name, arr_type="radarr", size_gb=None):
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
            elif c_type == "size":
                if size_gb is not None and cond.get("size_bounds"):
                    min_b, max_b = cond["size_bounds"]
                    min_gb = (min_b / (1024**3)) if (min_b and min_b > 10000) else (min_b or 0.0)
                    max_gb = (max_b / (1024**3)) if (max_b and max_b > 10000) else (max_b or float('inf'))
                    if min_gb <= size_gb <= max_gb:
                        cond_matched = True
                
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
            "min_band": 5800
        },
        # --- OP 916 SIZE-AWARE SCORING BATTERY ---
        {
            "category": "Size-Aware: City of God Micro-AV1 Untiered (1.4GB Penalized to 700 < 1000 Cutoff)",
            "title": "City.of.God.2002.bluray.sdr.portuguese.1080p.av1.1500mb-UnknownGroup-xpost",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 1.41,
            "expect_pass": False,
            "min_band": 600,
            "max_band": 800
        },
        {
            "category": "Size-Aware: City of God Tier 1 1080p x265 (8.1GB Scores 1700 -> Beats Rosy 700)",
            "title": "City.of.God.2002.1080p.BluRay.x265.DDP.5.1.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 8.1,
            "expect_pass": True,
            "min_band": 1600,
            "max_band": 1800
        },
        {
            "category": "Size-Aware: Easy A onlyfaffs 1080p AV1 (2.8GB Micro Penalized but Passes Cutoff)",
            "title": "Easy.A.2010.1080p.BluRay.AV1.Opus.5.1-onlyfaffs",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 2.83,
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 1500
        },
        {
            "category": "Size-Aware: Normal 2160p AV1 (12.5GB -> Score Unchanged at 5950)",
            "title": "Dune.Part.Two.2024.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-TAoE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.5,
            "expect_pass": True,
            "min_band": 5800,
            "max_band": 6200
        },
        {
            "category": "Size-Aware: Oversized 2160p Fallback (Akira 41.4GB x265 Penalized by -1500)",
            "title": "Akira.1988.REPACK.2160p.UHD.BluRay.Dual.Audio.TrueHD.5.1.HDR.x265-Chotab",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 41.36,
            "expect_pass": False,
            "min_band": -2000,
            "max_band": 300
        },
        {
            "category": "Size-Aware: Micro-AV1 as Only Option (Score 1200 >= 1000 Cutoff -> Grabbed)",
            "title": "Obscure.Indie.Film.2023.1080p.Bluray.AV1.Opus.2.0-Rosy",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 1.4,
            "expect_pass": True,
            "min_band": 1000,
            "max_band": 1250
        },
        # --- OP 917 GRADUATED OVERSIZED SCORING BATTERY ---
        {
            "category": "Op 917: 20GB non-AV1 2160p (Tolerated, 0 Penalty -> Score 2300)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 20.0,
            "expect_pass": True,
            "min_band": 2000,
            "max_band": 2600
        },
        {
            "category": "Op 917: 27GB non-AV1 2160p (Heavy Band: -400 Penalty -> Score 1900)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 27.0,
            "expect_pass": True,
            "min_band": 1800,
            "max_band": 2200
        },
        {
            "category": "Op 917: 33GB non-AV1 2160p (Oversized Band: -1500 Penalty -> Score 800 < 1000 Cutoff)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 33.0,
            "expect_pass": False,
            "min_band": 600,
            "max_band": 999
        },
        {
            "category": "Op 917: 35GB AV1 2160p (AV1 Exempt, Zero Penalty -> Score 5950)",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 35.0,
            "expect_pass": True,
            "min_band": 5800,
            "max_band": 6200
        },
        {
            "category": "Op 917 Boundary: 24.9GB non-AV1 2160p (No Penalty -> Score 2300)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 24.9,
            "expect_pass": True,
            "min_band": 2000,
            "max_band": 2600
        },
        {
            "category": "Op 917 Boundary: 25.1GB non-AV1 2160p (-400 Penalty -> Score 1900)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 25.1,
            "expect_pass": True,
            "min_band": 1800,
            "max_band": 2200
        },
        {
            "category": "Op 917 Boundary: 30.1GB non-AV1 2160p (-1500 Penalty -> Score 800 < 1000 Cutoff)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.x265.TrueHD.Atmos.7.1.DV.HDR-DON",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 30.1,
            "expect_pass": False,
            "min_band": 600,
            "max_band": 999
        },
        # --- OP 918 PROFILE HONE & FLOOR BATTERY ---
        {
            "category": "Op 918 Floor: 5.0GB untiered 2160p AV1 (Penalized to 950 < 1000 Cutoff)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.AV1.Opus.5.1-UnknownGroup",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 5.0,
            "expect_pass": False,
            "min_band": 600,
            "max_band": 999
        },
        {
            "category": "Op 918 Floor: 5.5GB Compact-tier 2160p AV1 (Score 1450 -> Loses to hallowed-class 1550)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.AV1.Opus.5.1-onlyfaffs",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 5.5,
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 1500
        },
        {
            "category": "Op 921 Lean Floor: 6.5GB Quality-tier 2160p AV1 (Lean Band Penalty -> Score 1800, Loses to x265)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.HDR.AV1-CoSMiCSuRFeR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 6.5,
            "expect_pass": True,
            "min_band": 1700,
            "max_band": 1900
        },
        {
            "category": "Op 918 Audio Retune: hallowed-class 13GB 2160p x265 with EAC3 5.1 (Scores 1550)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.HDR.DDP.5.1.x265-hallowed",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 13.0,
            "expect_pass": True,
            "min_band": 1500,
            "max_band": 1700
        },
        {
            "category": "Op 918 Insurance: 41.3GB ROTK AV1 (Size < 45GB -> No Extreme Penalty)",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 41.34,
            "expect_pass": True,
            "min_band": 5800,
            "max_band": 6200
        },
        {
            "category": "Op 918 Insurance: 48GB Extreme Release (Size >= 45GB -> Extreme -1500 Penalty)",
            "title": "The.Outsiders.1983.Directors.Cut.2160p.UHD.BluRay.DTS-HD.MA.5.1.HDR.x265-W4NK3R",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 48.18,
            "expect_pass": False,
            "min_band": -2000,
            "max_band": 500
        },
        # --- 14. OP 920: AV1 NAMELESS TRUST BATTERY ---
        {
            "category": "Op 920: NLsub Bourne 17.7GB (Nameless 2160p AV1 -> -2500 penalty -> Score 1700)",
            "title": "The Bourne Supremacy (2004) - 2160p HDR - AV1 BRRip - NLsub",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 17.71,
            "expect_pass": True,
            "min_band": 1500,
            "max_band": 1900
        },
        {
            "category": "Op 920: R&H Bourne 7.8GB (Named Group in Lean Band -> Score 1300)",
            "title": "The.Bourne.Supremacy.2004-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 7.78,
            "expect_pass": True,
            "min_band": 1200,
            "max_band": 1400
        },
        {
            "category": "Op 920: BYNDR x265 Bourne 24.2GB (Score 2200, Beats NLsub 1700)",
            "title": "The.Bourne.Supremacy.2004.2160p.MA.WEB-DL.DTS-X.7.1.DV.HDR.H.265-BYNDR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 24.21,
            "expect_pass": True,
            "min_band": 2000,
            "max_band": 2400
        },
        {
            "category": "Op 920: Smokindevil Shawshank (Named Group -> No Nameless Penalty -> Op 925 Quality Score 2400)",
            "title": "The.Shawshank.Redemption.1994.2160p.HDR.AV1-Smokindevil.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 5.05,
            "expect_pass": True,
            "min_band": 2200,
            "max_band": 2600
        },
        {
            "category": "Op 920: anomoomin Cast Away 1080p (1080p Unaffected -> Score 4250)",
            "title": "Cast.Away.2000.1080p.BluRay.AV1.Opus.5.1-anomoomin.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 3.89,
            "expect_pass": True,
            "min_band": 4100,
            "max_band": 4400
        },
        # --- 15. OP 921: AV1 LEAN BAND BATTERY (6.0 - 11.0 GB) ---
        {
            "category": "Op 921: Blade Runner 7.11GB R&H (Lean Band -> -3400 Penalty -> Score 1900, Loses to x265)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RandH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 7.11,
            "expect_pass": True,
            "min_band": 1800,
            "max_band": 2000
        },
        {
            "category": "Op 921: The Deer Hunter 10.75GB R (Lean Band -> -3400 Penalty -> Score 950)",
            "title": "The.Deer.Hunter.1978.2160p.UHD.BluRay.EAC3.5.1.HDR.AV1-R",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 10.75,
            "expect_pass": False,
            "min_band": 850,
            "max_band": 1050
        },
        {
            "category": "Op 921: Gladiator 11.88GB R&H (Size > 11GB -> Unpenalized Score 5300)",
            "title": "Gladiator.2000.Extended.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RandH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 11.88,
            "expect_pass": True,
            "min_band": 5100,
            "max_band": 5500
        },
        {
            "category": "Op 921: Apocalypse Now 12.72GB R (Size > 11GB -> Unpenalized Score 4200)",
            "title": "Apocalypse.Now.1979.Final.Cut.2160p.UHD.BluRay.DTS.5.1.HDR.AV1-R",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.72,
            "expect_pass": True,
            "min_band": 4000,
            "max_band": 4400
        },
        {
            "category": "Op 921: Boundary 6.0GB AV1 (Micro/Lean Boundary -> Micro Penalty -> Score 1450)",
            "title": "Movie.Title.2024.2160p.UHD.BluRay.AV1.Opus.5.1-onlyfaffs",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 6.0,
            "expect_pass": True,
            "min_band": 1350,
            "max_band": 1550
        },
        {
            "category": "Op 921: Boundary 11.0GB AV1 (Lean/Free Boundary -> Lean Penalty -> Score 1900)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RandH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 11.0,
            "expect_pass": True,
            "min_band": 1800,
            "max_band": 2000
        },
        {
            "category": "Op 921: Boundary 11.01GB AV1 (Free/Unpenalized -> Score 5300)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RandH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 11.01,
            "expect_pass": True,
            "min_band": 5100,
            "max_band": 5500
        },
        {
            "category": "Op 921 Stacking: 8.0GB Nameless Lean AV1 (Both Penalties -2500 & -3400 -> Score -1700 < 1000 Rejected)",
            "title": "The.Bourne.Supremacy.2004.2160p.HDR.AV1.BRRip-NLsub.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 8.0,
            "expect_pass": False,
            "min_band": -3000,
            "max_band": 500
        },
        # --- 16. OP 922: FOREIGN DUB DEMOTION BATTERY ---
        {
            "category": "Op 922: Das Bourne Ultimatum 18.89GB Bi0hazard German Dub (-750 Dub Penalty -> Score 3600)",
            "title": "Das.Bourne.Ultimatum.2007.German.DUBBED.DL.EAC3.2160p.HDR.BluRay.AV1-Bi0hazard",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 18.89,
            "expect_pass": True,
            "min_band": 3500,
            "max_band": 3700
        },
        {
            "category": "Op 922: The Bourne Ultimatum 18.89GB Non-Dub AV1 (No Dub Penalty -> Score 4350)",
            "title": "The.Bourne.Ultimatum.2007.2160p.HDR.EAC3.5.1.BluRay.AV1-Bi0hazard",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 18.89,
            "expect_pass": True,
            "min_band": 4250,
            "max_band": 4450
        },
        {
            "category": "Op 922: Matrix German Dub 2160p AV1 (-750 Penalty -> Score 3450 Beats x265 2200)",
            "title": "The.Matrix.1999.German.DUBBED.2160p.HDR.AV1-Group",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 16.0,
            "expect_pass": True,
            "min_band": 3350,
            "max_band": 3550
        },
        {
            "category": "Op 922: Matrix MULTi release (No Dub Penalty -> Score 4200)",
            "title": "The.Matrix.1999.MULTi.2160p.HDR.AV1-Group",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 16.0,
            "expect_pass": True,
            "min_band": 4100,
            "max_band": 4300
        },
        # --- 17. OP 925: CENSUS-DRIVEN TIER EXPANSION BATTERY ---
        {
            "category": "Op 925: Fat dAV1nci 2160p (Quality +1000 -> Score 5500 Beats x265 2200)",
            "title": "The.Lord.of.the.Rings.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 14.2,
            "expect_pass": True,
            "min_band": 5400,
            "max_band": 5600
        },
        {
            "category": "Op 925: Fat UH 2160p (Quality +1000 -> Score 6100 Beats x265 2200)",
            "title": "LOTR.The.Return.Of.The.King.2003.PROPER.Bluray.2160p.AV1.HDR10.DV.DDP.Atmos-UH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 13.5,
            "expect_pass": True,
            "min_band": 6000,
            "max_band": 6200
        },
        {
            "category": "Op 925: Fat Smokindevil 2160p (Quality +1000 -> Score 5950 Beats x265 2200)",
            "title": "Fury.2014.2160p.UHD.BluRay.AV1.DV.HDR.TrueHD.Atmos-Smokindevil.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.5,
            "expect_pass": True,
            "min_band": 5850,
            "max_band": 6050
        },
        {
            "category": "Op 925: Lean dAV1nci 2160p (Quality +1000 & Lean -3400 -> Score 1800 in Lean Band)",
            "title": "The.Matrix.1999.2160p.HDR.AV1-dAV1nci",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 8.5,
            "expect_pass": True,
            "min_band": 1700,
            "max_band": 1900
        },
        {
            "category": "Op 925: Fat Toasty 2160p (Compact +500 -> Score 5300)",
            "title": "The.Thing.1982.2160p.UHD.BluRay.DV.HDR.DTS.5.1.AV1-Toasty",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 21.65,
            "expect_pass": True,
            "min_band": 5100,
            "max_band": 5500
        },
        {
            "category": "Op 925: Consolidated R and H bare RH suffix (Compact +500 -> Score 5300)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.0,
            "expect_pass": True,
            "min_band": 5100,
            "max_band": 5500
        },
        # --- 18. OP 927: SHADOW EXPLORER PROFILE BATTERY ---
        {
            "category": "Op 927: SHADOW Explorer Tiered Group (dAV1nci Quality Bonus Neutralized -> Score 4500)",
            "title": "The.Lord.of.the.Rings.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "profile": "Movies SHADOW Explorer",
            "arr_type": "radarr",
            "size_gb": 14.2,
            "expect_pass": True,
            "min_band": 4400,
            "max_band": 4600
        },
        {
            "category": "Op 927: SHADOW Explorer Untiered Candidate (Rob74K Scores on Raw Tags -> Score 4950)",
            "title": "John.Wick.Chapter.4.2023.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-Rob74K",
            "profile": "Movies SHADOW Explorer",
            "arr_type": "radarr",
            "size_gb": 19.1,
            "expect_pass": True,
            "min_band": 4850,
            "max_band": 5050
        },
        {
            "category": "Op 927: SHADOW Explorer Anti-Junk Bands Active (Lean -3400 Penalty Fires -> Score 1400)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RandH",
            "profile": "Movies SHADOW Explorer",
            "arr_type": "radarr",
            "size_gb": 7.11,
            "expect_pass": True,
            "min_band": 1300,
            "max_band": 1500
        },
        # --- 19. OP 930: SIZE FLOOR & LEGACY TRUSTED X264 BATTERY ---
        {
            "category": "Op 930: Legacy Trusted x264 CtrlHD (Score 1150 Clears Cutoff)",
            "title": "Blue.Valentine.2010.1080p.BluRay.DTS.x264-CtrlHD",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.54,
            "expect_pass": True,
            "min_band": 1100,
            "max_band": 1200
        },
        {
            "category": "Op 930: Legacy Trusted x264 PiRaTeS (Score 1150 Clears Cutoff)",
            "title": "Hoosiers.1986.1080p.BluRay.DTS.x264-PiRaTeS",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 11.88,
            "expect_pass": True,
            "min_band": 1100,
            "max_band": 1200
        },
        {
            "category": "Op 930: Untrusted Legacy x264 Sparks (Score -7000 Rejected)",
            "title": "Generic.Movie.1080p.BluRay.x264-SPARKS",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 10.0,
            "expect_pass": False,
            "min_band": -7100,
            "max_band": -6900
        },
        {
            "category": "Op 930: Micro Hard Floor 700KB Feature Film (Score -5300 Rejected)",
            "title": "Greenland.2020.2160p.HDR.AV1-onlyfaffs",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 0.0007,
            "expect_pass": False,
            "min_band": -5400,
            "max_band": -5200
        },
        {
            "category": "Op 930: Micro Hard Floor 979MB HDTV Cap (Score -7500 Rejected)",
            "title": "X-Men.The.Last.Stand.2006.1080p.HDTV.AV1-DKong",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 0.95,
            "expect_pass": False,
            "min_band": -7600,
            "max_band": -7400
        },
        {
            "category": "Op 932: Legacy Trusted 1080p WEB-DL (PiRaTeS Hoosiers Lifts Above Cutoff)",
            "title": "Hoosiers.1986.1080p.AMZN.WEB-DL.DDP.5.1.H.264-PiRaTeS",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 11.88,
            "expect_pass": True,
            "min_band": 1300,
            "max_band": 1400
        },
        {
            "category": "Op 932: Indexer Dupe Tag Tolerance (R&H_1 Suffix Retains Compact Tier)",
            "title": "The.Wolverine.2013.Theatrical.Cut.2160p.AMZN.WEB.DV.HDR10.10.bit.Encode.AV1.DTS.5.1-R&H_1",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 5.89,
            "expect_pass": True,
            "min_band": 2500,
            "max_band": 2600
        },
        {
            "category": "Op 932: Opus 5.1 No-Audio Fix (The Hunt KIMJI Lifts Cleanly)",
            "title": "The.Hunt.2012.1080p.BluRay.Opus.5.1.AV1-KIMJI",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 3.59,
            "expect_pass": True,
            "min_band": 3700,
            "max_band": 4300
        },
        {
            "category": "Op 933: Vetted Union ATELiER 1080p BluRay (Score 1150 Clears Cutoff)",
            "title": "Blade.Runner.1982.1080p.BluRay.DTS.x264-ATELiER",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.5,
            "expect_pass": True,
            "min_band": 1100,
            "max_band": 1200
        },
        {
            "category": "Op 933: Vetted Union c0kE 1080p BluRay (Score 1150 Clears Cutoff)",
            "title": "Drive.2011.1080p.BluRay.DTS.x264-c0kE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 10.2,
            "expect_pass": True,
            "min_band": 1100,
            "max_band": 1200
        },
        {
            "category": "Op 933: Vetted Union SA89 Tier 1 1080p BluRay (Score 1250 Clears Cutoff)",
            "title": "Arrival.2016.1080p.BluRay.DTS.x264-SA89",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 14.1,
            "expect_pass": True,
            "min_band": 1200,
            "max_band": 1300
        },
        {
            "category": "Op 933: Hard-Banned YIFY x264 (Score -17000 Rejected)",
            "title": "Movie.2024.1080p.BluRay.x264-YIFY",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 2.1,
            "expect_pass": False,
            "min_band": -20000,
            "max_band": -10000
        },
        {
            "category": "Op 935: Repack1 Micro-Ladder (Score 4655 Beats Standard 4650)",
            "title": "The.Matrix.1999.2160p.UHD.BluRay.PROPER.TrueHD.Atmos.AV1-Waldek",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 18.5,
            "expect_pass": True,
            "min_band": 4600,
            "max_band": 4700
        },
        {
            "category": "Op 935: 4K Remaster Tag (+25 pts on Fallback Tier)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.4K.Remaster.HDR.x265-BHDStudio",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 16.5,
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 1550
        },
        {
            "category": "Op 935: Audio Description Hard Reject (-10000 Rejection)",
            "title": "Movie.Title.2024.1080p.WEB-DL.DDP5.1.DVS-FLUX",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 4.5,
            "expect_pass": False,
            "min_band": -10000,
            "max_band": -5000
        },
        {
            "category": "Op 935: Line Audio Hard Reject (-10000 Rejection)",
            "title": "Movie.Title.2024.1080p.LINE.Audio.x264-Group",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 3.2,
            "expect_pass": False,
            "min_band": -20000,
            "max_band": -10000
        },
        {
            "category": "Op 935: Vetted WEB-DL Tier 2 Union (SiGMA 2160p Fallback)",
            "title": "Movie.Title.2024.2160p.AMZN.WEB-DL.DDP.5.1.HDR.x265-SiGMA",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.5,
            "expect_pass": True,
            "min_band": 1500,
            "max_band": 1750
        },
        {
            "category": "Op 936: Hardcoded Subtitles Reject (KORSUB -10000 Trap Eliminated)",
            "title": "Gladiator.II.2024.2160p.KORSUB.HDR.AV1-Group",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 14.5,
            "expect_pass": False,
            "min_band": -10000,
            "max_band": -5000
        },
        {
            "category": "Op 936: FLAC Lossless Audio Bonus (+100 pts on 1080p Archival)",
            "title": "Akira.1988.1080p.BluRay.FLAC.x264-CtrlHD",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 12.1,
            "expect_pass": True,
            "min_band": 1200,
            "max_band": 1300
        },
        {
            "category": "Op 936: Boutique Label Criterion Bonus (+50 pts on 4K Master)",
            "title": "Seven.Samurai.1954.2160p.UHD.BluRay.Criterion.Collection.HDR.AV1-Waldek",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "size_gb": 19.5,
            "expect_pass": True,
            "min_band": 5200,
            "max_band": 5300
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
        size_gb = case.get("size_gb")
        
        score, min_score, upgrade_until, passed_cutoff, matched = evaluate_release(conn, title, profile, arr_type, size_gb=size_gb)
        
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
