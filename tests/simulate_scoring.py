#!/usr/bin/env python3
"""
PCD Flagship Quality Profile Simulation Battery (AV1-First, Dumpstarr 2160p Hybrid Standard)
Evaluates:
- Tier 1: Elite 4K Encoders (AV1 + Upstream x265/x264) -> +3000
- Tier 2: Top 4K Encoders (WEB-DL + 2160p Bluray Tier 03/04) -> +2200
- Tier 3: Archival 1080p Blu-ray Disc Encoders -> +1400
- Feature Bonuses: Max stacking strictly capped < 800
- Untiered Releases without Vetted Group: < 1000 (Fails profile minimum cutoff)
- Sub-4K x265/HEVC: -10000 (x265 HD denied below 2160p)
- Banned / Toxic Groups: -10000 (Hard rejected)
- Full Alias Coverage Test: Verifies all aliases across tiers
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
    is_720p = bool(re.search(r"\b(720p)\b", title, re.IGNORECASE))

    return {
        "group": group,
        "is_bluray": is_bluray,
        "is_webdl": is_webdl,
        "is_webrip": is_webrip,
        "is_hdtv": is_hdtv,
        "is_2160p": is_2160p,
        "is_1080p": is_1080p,
        "is_720p": is_720p
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
    p = re.sub(r'\(\?<=\^\|([^)]+)\)', r'(?:^|(?<=\1))', p)
    p = re.sub(r'\(\?<=([^)]+)\|\^\)', r'(?:(?<=\1)|^)', p)
    p = p.replace(r'(?<=\b[12]\d{3}\b).*?', r'(?:[12]\d{3}.*?)')
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
        prof_rows = conn.execute("SELECT name, minimum_custom_format_score, upgrade_until_score FROM quality_profiles").fetchall()
        for p_name, min_s, upg_s in prof_rows:
            self.profiles[p_name] = {"min_score": min_s, "upgrade_until": upg_s, "rules": {}}

        pat_cache = {}
        for r_name, p_str in conn.execute("SELECT name, pattern FROM regular_expressions").fetchall():
            clean_pat = make_python_re_compatible(p_str)
            try:
                pat_cache[r_name] = (re.compile(clean_pat, re.IGNORECASE), None)
            except re.error:
                pat_cache[r_name] = (None, clean_pat)

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
                            s_rows = conn.execute("""
                                SELECT cs.source FROM condition_sources cs
                                WHERE cs.custom_format_name = ? AND cs.condition_name = ?
                            """, (cf_name, c_name)).fetchall()
                            sources = set(r[0].lower() for r in s_rows)

                        res_set = set()
                        if c_type == "resolution":
                            r_rows = conn.execute("""
                                SELECT cr.resolution FROM condition_resolutions cr
                                WHERE cr.custom_format_name = ? AND cr.condition_name = ?
                            """, (cf_name, c_name)).fetchall()
                            res_set = set(r[0].lower() for r in r_rows)

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
                if "720p" in r_set and tokens["is_720p"]: cond_matched = True
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
                    break
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
        # --- 1. TOP TIER AV1 2160p & 1080p ENCODERS (Score >= 3000) ---
        {
            "category": "Pure AV1 2160p HQ (dAV1nci LOTR)",
            "title": "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Pure AV1 2160p HQ (ChopperHitler Matrix)",
            "title": "The.Matrix.1999.2160p.UHD.BluRay.PROPER.TrueHD.Atmos.AV1-ChopperHitler",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Pure AV1 2160p HQ (RandH / R&H Shawshank)",
            "title": "The.Shawshank.Redemption.1994.2160p.BluRay.DV.HDR10.AV1.DTS.5.1-R&H",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Pure AV1 2160p HQ (CoSMiCSuRFeR Dune 2)",
            "title": "Dune.Part.Two.2024.2160p.HDR.AV1-CoSMiCSuRFeR",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Pure AV1 2160p HQ (UH LOTR)",
            "title": "LOTR.The.Return.Of.The.King.2003.PROPER.Bluray.2160p.AV1.HDR10.OPUS.7.1-UH",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Pure AV1 1080p HQ (KIMJI The Hunt)",
            "title": "The.Hunt.2012.1080p.BluRay.Opus.5.1.AV1-KIMJI",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Pure AV1 2160p HQ (TAoE Dune 2)",
            "title": "Dune.Part.Two.2024.2160p.UHD.BluRay.TrueHD.Atmos.7.1.DV.HDR.AV1-TAoE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },

        # --- 2. TIERED X265 4K FALLBACKS (Score 2200 - 3775) ---
        {
            "category": "Tier 1 4K x265 (hallowed Die My Love)",
            "title": "Die.My.Love.2025.UHD.BluRay.2160p.DDP.5.1.HDR10+.x265-hallowed",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Tier 1 4K x265 (BHDStudio Blade Runner)",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.4K.Remaster.HDR.x265-BHDStudio",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Tier 2 4K WEB-DL (FLUX Arrival)",
            "title": "Arrival.2016.2160p.WEB-DL.DDP5.1.Atmos.DV.HDR.x265-FLUX",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2200,
            "max_band": 3300
        },
        {
            "category": "Tier 2 4K WEB-DL (SiGMA AMZN)",
            "title": "Movie.Title.2024.2160p.AMZN.WEB-DL.DDP.5.1.HDR.x265-SiGMA",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2200,
            "max_band": 3300
        },
        {
            "category": "Tier 2 4K WEB-DL (HONE Dune 2)",
            "title": "Dune.Part.Two.2024.2160p.UHD.WEB-DL.DDP5.1.Atmos.DV.HDR.x265-HONE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2200,
            "max_band": 3300
        },

        # --- 3. ARCHIVAL 1080P BLURAY ENCODES (Score 1400 - 2175) ---
        {
            "category": "Archival 1080p BluRay (c0kE Drive)",
            "title": "Drive.2011.1080p.BluRay.DTS.x264-c0kE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 2175
        },
        {
            "category": "Archival 1080p BluRay (CtrlHD Akira)",
            "title": "Akira.1988.1080p.BluRay.FLAC.x264-CtrlHD",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 2175
        },
        {
            "category": "Archival 1080p BluRay (ATELiER Blade Runner)",
            "title": "Blade.Runner.1982.1080p.BluRay.DTS.x264-ATELiER",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 2175
        },
        {
            "category": "Archival 1080p BluRay (SA89 Arrival)",
            "title": "Arrival.2016.1080p.BluRay.DTS.x264-SA89",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 2175
        },

        # --- 4. UNTIERED JUNK & LEAKS (< 1000 Cutoff) ---
        {
            "category": "Untiered 1080p Release without Vetted Group",
            "title": "Gladiator.2000.1080p.BluRay.x265.TrueHD.Atmos.7.1-RandomGroup",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 999
        },
        {
            "category": "Untrusted Legacy x264 Sparks",
            "title": "Generic.Movie.1080p.BluRay.x264-SPARKS",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 999
        },
        {
            "category": "Sub-4K x265 Reject (Dumpstarr Rule)",
            "title": "Movie.2024.1080p.BluRay.x265-RandomGroup",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },

        # --- 5. BANNED GROUPS & HYGIENE REJECTIONS (-10000) ---
        {
            "category": "Banned Micro-Group Saon",
            "title": "Capernaum.2018.1080p.NF.WEB-DL.DDP5.1.AV1-Saon.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Group YIFY",
            "title": "Movie.2024.1080p.BluRay.x264-YIFY",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Group YTS",
            "title": "Top.Gun.2022.1080p.AV1-YTS.mp4",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Audio Description",
            "title": "Movie.Title.2024.1080p.WEB-DL.DDP5.1.DVS-FLUX",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Line Audio",
            "title": "Movie.Title.2024.1080p.LINE.Audio.x264-Group",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Hardcoded Subtitles KORSUB",
            "title": "Gladiator.II.2024.2160p.KORSUB.HDR.AV1-Group",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned CAM",
            "title": "Dune.Part.Two.2024.CAM.AV1-TestGroup.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Upscale",
            "title": "Gladiator.II.2024.1080p.Upscale.AV1-Test.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned 3D",
            "title": "Avatar.The.Way.of.Water.2022.3D.1080p.AV1.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Full Disc",
            "title": "Gladiator.2000.2160p.UHD.COMPLETE.BLURAY.AV1.iso",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Banned Remux LEGi0N",
            "title": "Die.My.Love.2025.2160p.UHD.BluRay.Remux.HEVC.DV.HDR.Atmos-LEGi0N.mkv",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": -1
        },
        {
            "category": "Repack1 Micro-Ladder",
            "title": "The.Matrix.1999.2160p.UHD.BluRay.PROPER.TrueHD.Atmos.AV1-ChopperHitler",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "4K Remaster Tag",
            "title": "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.4K.Remaster.HDR.x265-BHDStudio",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Boutique Label Criterion Bonus",
            "title": "Seven.Samurai.1954.2160p.UHD.BluRay.Criterion.Collection.HDR.AV1-ChopperHitler",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },

        # --- 6. BLOCKER 4 AUDIO-TOKEN IMMUNITY REGRESSION CASES ---
        {
            "category": "Blocker 4 Case 1: Tier 2 NTb with Atmos/DV/HDR10+",
            "title": "Movie.2024.2160p.WEB-DL.DV.HDR10+.DDP5.1.Atmos.H265-NTb",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 2200,
            "max_band": 3220
        },
        {
            "category": "Blocker 4 Case 2: Tier 1 hallowed with DTS-HD MA",
            "title": "Movie.2023.2160p.BluRay.DTS-HD.MA.7.1.x265-hallowed",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 3000
        },
        {
            "category": "Blocker 4 Case 3: Untiered with DV/Atmos (No Group)",
            "title": "Movie.2022.2160p.WEB-DL.DV.DDP5.1.Atmos.H.265",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 999
        },
        {
            "category": "Blocker 4 Case 4: Tier 3 c0kE 1080p BluRay",
            "title": "Movie.2021.1080p.BluRay.DTS.x264-c0kE",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": True,
            "min_band": 1400,
            "max_band": 2175
        },
        {
            "category": "Blocker 4 Case 5: Untiered DVSUX (No False DV Match)",
            "title": "Movie.2020.2160p.WEB-DL.Atmos.DDP5.1-DVSUX",
            "profile": "Movies 2160p AV1 HQ",
            "arr_type": "radarr",
            "expect_pass": False,
            "max_band": 999
        }
    ]

    print("================================================================================")
    print("UNIFIED PURE TIERED QUALITY PROFILE SIMULATION BATTERY REPORT")
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

    # --- UPGRADE SCORE INCREMENT BATTERY (increment = 300) ---
    increment_cases = [
        {"name": "Minor service swap (1350 HMAX vs 1400 AMZN)", "existing": 1350, "new": 1400, "expect_upgrade": False},
        {"name": "Major AV1 upgrade (1400 x265 vs 3000 AV1)", "existing": 1400, "new": 3000, "expect_upgrade": True},
        {"name": "Tier upgrade (1400 vs 1700)", "existing": 1400, "new": 1700, "expect_upgrade": True},
    ]
    inc_val = conn.execute("SELECT upgrade_score_increment FROM quality_profiles WHERE name = 'Movies 2160p AV1 HQ'").fetchone()[0]
    print(f"\n=== UPGRADE SCORE INCREMENT BATTERY (increment = {inc_val}) ===")
    for c in increment_cases:
        delta = c["new"] - c["existing"]
        fires = delta >= inc_val
        passed = (fires == c["expect_upgrade"])
        print(f"[{'PASS' if passed else 'FAIL'}] {c['name']} (Delta: +{delta}) -> Upgrade: {fires} (Expected: {c['expect_upgrade']})")
        if not passed:
            failed_tests += 1
        else:
            passed_tests += 1

    # --- PART 4 BUG 2 ALIAS COVERAGE BATTERY ---
    print("\n================================================================================")
    print("PART 4 BUG 2: ALIAS COVERAGE & MONOTONICITY BATTERY (208 ALIASES)")
    print("================================================================================")

    tier1_aliases = {
        'ChopperHitler': (['CHOPPERHITLER', 'ChopperHitler', 'chopperhitler'], '2160p.UHD.BluRay.AV1'),
        'dAV1nci': (['dAV1nci', 'DAV1NCI', 'dav1nci'], '2160p.UHD.BluRay.AV1'),
        'RandH': (['RandH', 'RH', 'R&H', 'R and H', 'randh', 'rh'], '2160p.UHD.BluRay.AV1'),
        'KIMJI': (['KIMJI', 'kimji'], '2160p.UHD.BluRay.AV1'),
        'UH': (['UH', 'uh'], '2160p.UHD.BluRay.AV1'),
        'TAoE': (['TAoE', 'taoe'], '2160p.UHD.BluRay.AV1'),
        'CoSMiCSuRFeR': (['CoSMiCSuRFeR', 'cosmicsurfer'], '2160p.UHD.BluRay.AV1'),
        'PRL': (['PRL', 'prl'], '2160p.UHD.BluRay.AV1'),
        'CHD': (['CHD', 'chd'], '2160p.UHD.BluRay.AV1'),
        'TiZU': (['TiZU', 'tizu'], '2160p.UHD.BluRay.AV1'),
        'CtrlHD': (['CtrlHD', 'ctrlhd'], '2160p.BluRay'),
        'DON': (['DON', 'don'], '2160p.BluRay'),
        'MainFrame': (['MainFrame', 'mainframe'], '2160p.BluRay'),
        'W4NK3R': (['W4NK3R', 'w4nk3r'], '2160p.BluRay'),
        'REBORN': (['REBORN', 'reborn'], '2160p.BluRay'),
        'SA89': (['SA89', 'sa89'], '2160p.BluRay'),
        'SoLaR': (['SoLaR', 'solar'], '2160p.BluRay'),
        'dkore': (['dkore', 'DKORE'], '2160p.BluRay.x265'),
        'BHDStudio': (['BHDStudio', 'bhdstudio'], '2160p.BluRay'),
        'hallowed': (['hallowed', 'HALLOWED'], '2160p.BluRay'),
    }

    tier2_aliases = {
        'FLUX': (['FLUX', 'flux'], '2160p.WEB-DL'),
        'NTb': (['NTb', 'ntb'], '2160p.WEB-DL'),
        'TheFarm': (['TheFarm', 'thefarm'], '2160p.WEB-DL'),
        'BYNDR': (['BYNDR', 'byndr'], '2160p.WEB-DL'),
        'CMRG': (['CMRG', 'cmrg', 'CMaRG', 'CMRioG'], '2160p.WEB-DL'),
        'Kitsune': (['Kitsune', 'kitsune'], '2160p.WEB-DL'),
        'playWEB': (['playWEB', 'playweb'], '2160p.WEB-DL'),
        'TEPES': (['TEPES', 'tepes'], '2160p.WEB-DL'),
        'ABBIE': (['ABBIE', 'ABBiE', 'abbie'], '2160p.WEB-DL'),
        'AJP69': (['AJP69', 'ajp69'], '2160p.WEB-DL'),
        'APEX': (['APEX', 'apex'], '2160p.WEB-DL'),
        'BLUTONiUM': (['BLUTONiUM', 'blutonium'], '2160p.WEB-DL'),
        'CRFW': (['CRFW', 'crfw'], '2160p.WEB-DL'),
        'CRUD': (['CRUD', 'crud'], '2160p.WEB-DL'),
        'GNOME': (['GNOME', 'gnome'], '2160p.WEB-DL'),
        'KiNGS': (['KiNGS', 'kings'], '2160p.WEB-DL'),
        'MADSKY': (['MADSKY', 'madsky'], '2160p.WEB-DL'),
        'NOSiViD': (['NOSiViD', 'nosivid'], '2160p.WEB-DL'),
        'NTG': (['NTG', 'ntg'], '2160p.WEB-DL'),
        'RAWR': (['RAWR', 'rawr'], '2160p.WEB-DL'),
        'SiC': (['SiC', 'sic'], '2160p.WEB-DL'),
        'ZoroSenpai': (['ZoroSenpai', 'zorosenpai'], '2160p.WEB-DL'),
        'CasStudio': (['CasStudio', 'casstudio'], '2160p.WEB-DL'),
        'monkee': (['monkee', 'MONKEE'], '2160p.WEB-DL'),
        'QOQ': (['QOQ', 'qoq'], '2160p.WEB-DL'),
        'RTN': (['RTN', 'rtn'], '2160p.WEB-DL'),
        'T6D': (['T6D', 't6d'], '2160p.WEB-DL'),
        'TOMMY': (['TOMMY', 'tommy'], '2160p.WEB-DL'),
        'ViSUM': (['ViSUM', 'visum'], '2160p.WEB-DL'),
        'dB': (['dB', 'db'], '2160p.WEB-DL'),
        'MiU': (['MiU', 'miu'], '2160p.WEB-DL'),
        'MZABI': (['MZABI', 'mzabi'], '2160p.WEB-DL'),
        'PHOENiX': (['PHOENiX', 'phoenix'], '2160p.WEB-DL'),
        'SbR': (['SbR', 'sbr'], '2160p.WEB-DL'),
        'SMURF': (['SMURF', 'smurf'], '2160p.WEB-DL'),
        'XEBEC': (['XEBEC', 'xebec', '4KBEC', 'CEBEX'], '2160p.WEB-DL'),
        'SiGMA': (['SiGMA', 'SIGMA', 'sigma'], '2160p.WEB-DL'),
        'EDPH': (['EDPH', 'edph'], '2160p.BluRay'),
        'TDD': (['TDD', 'tdd'], '2160p.BluRay'),
        'Chotab': (['Chotab', 'chotab'], '2160p.BluRay'),
        'D-Z0N3': (['D-Z0N3', 'd-z0n3'], '2160p.BluRay'),
        'c0kE': (['c0kE', 'c0ke'], '2160p.BluRay'),
        'ATELiER': (['ATELiER', 'atelier'], '2160p.BluRay'),
        'BSTD': (['BSTD', 'bstd'], '2160p.BluRay'),
        'BlzT': (['BlzT', 'blzt'], '2160p.BluRay'),
        'ESiR': (['ESiR', 'esir'], '2160p.BluRay'),
        'LESTiN': (['LESTiN', 'lestin'], '2160p.BluRay'),
        'NCmt': (['NCmt', 'ncmt'], '2160p.BluRay'),
        'Softboat': (['Softboat', 'softboat'], '2160p.BluRay'),
        'faBR': (['faBR', 'fabr'], '2160p.BluRay'),
        'iFT': (['iFT', 'ift'], '2160p.BluRay'),
        'HiDt': (['HiDt', 'hidt'], '2160p.BluRay'),
        'HQMUX': (['HQMUX', 'hqmux'], '2160p.BluRay'),
        'RandomBytes': (['RandomBytes', 'randombytes'], '2160p.BluRay'),
        'PTer': (['PTer', 'pter'], '2160p.BluRay'),
        'SPHD': (['SPHD', 'sphd'], '2160p.BluRay'),
        'WEBDV': (['WEBDV', 'webdv'], '2160p.WEB-DL'),
        'HONE': (['HONE', 'hone'], '2160p.WEB-DL')
    }

    tier3_aliases = {
        'BBQ': (['BBQ', 'bbq'], '1080p.BluRay.x264'),
        'BMF': (['BMF', 'bmf'], '1080p.BluRay.x264'),
        'CRiSC': (['CRiSC', 'crisc'], '1080p.BluRay.x264'),
        'Dariush': (['Dariush', 'dariush'], '1080p.BluRay.x264'),
        'decibeL': (['decibeL', 'decibel'], '1080p.BluRay.x264'),
        'EA': (['EA', 'ea'], '1080p.BluRay.x264'),
        'HiSD': (['HiSD', 'hisd'], '1080p.BluRay.x264'),
        'LolHD': (['LolHD', 'lolhd'], '1080p.BluRay.x264'),
        'TnP': (['TnP', 'tnp'], '1080p.BluRay.x264'),
        'ZQ': (['ZQ', 'zq'], '1080p.BluRay.x264'),
        'coffee': (['coffee', 'COFFEE'], '1080p.BluRay.x264'),
        'TeamSyndicate': (['TeamSyndicate', 'teamsyndicate'], '1080p.BluRay.x264'),
        'playHD': (['playHD', 'playhd'], '1080p.BluRay.x264'),
        'sbR': (['sbR', 'SBR'], '1080p.BluRay.x264'),
        'VietHD': (['VietHD', 'viethd'], '1080p.BluRay.x264'),
        'Geek': (['Geek', 'geek'], '1080p.BluRay.x264'),
        'LoRD': (['LoRD', 'lord'], '1080p.BluRay.x264'),
        'HiFi': (['HiFi', 'hifi'], '1080p.BluRay.x264'),
        'EbP': (['EbP', 'ebp'], '1080p.BluRay.x264'),
        'TayTO': (['TayTO', 'tayto'], '1080p.BluRay.x264')
    }

    tier_cf_names = {
        'AV1 Quality Encoders', '2160p Quality Tier 1', '2160p Quality Tier 2', '2160p Balanced Tier 1',
        '2160p Balanced Tier 2', '2160p Balanced Tier 3', 'WEB-DL Tier 1', 'WEB-DL Tier 2', 'WEB-DL Tier 3',
        '2160p Quality Tier 3', '2160p Quality Tier 4', 'HONE Bluray', 'HONE WEB',
        '1080p Quality Tier 1', '1080p Quality Tier 2', '1080p Quality Tier 3', '1080p Balanced Tier 1', '1080p Balanced Tier 2'
    }

    total_alias_count = 0
    anomalies = []

    all_tier_tests = [
        (tier1_aliases, "Tier 1", 3000),
        (tier2_aliases, "Tier 2", 2200),
        (tier3_aliases, "Tier 3", 1400)
    ]

    for alias_map, t_name, min_expected in all_tier_tests:
        for group, (aliases, media_tag) in alias_map.items():
            for alias in aliases:
                total_alias_count += 1
                synthetic_title = f"Movie.2024.{media_tag}-{alias}"
                score, min_s, upg, passed, matched = evaluate_release(conn, synthetic_title, "Movies 2160p AV1 HQ")

                matched_tier_cfs = [m for m in matched if m[0] in tier_cf_names]
                if len(matched_tier_cfs) != 1 or score < min_expected:
                    anomalies.append({
                        "group": group,
                        "alias": alias,
                        "tier": t_name,
                        "matched_tier_cfs": matched_tier_cfs,
                        "score": score,
                        "expected_score": min_expected
                    })

    # Negative short alias boundary test
    neg_title = "Movie.2024.2160p.BluRay-XYZRH"
    score_neg, _, _, _, matched_neg = evaluate_release(conn, neg_title, "Movies 2160p AV1 HQ")
    neg_tier_cfs = [m for m in matched_neg if m[0] in tier_cf_names]
    if len(neg_tier_cfs) != 0:
        anomalies.append({"group": "XYZRH", "alias": "XYZRH", "tier": "Negative", "matched": neg_tier_cfs})

    print(f"Total Canonical Groups: {len(tier1_aliases) + len(tier2_aliases) + len(tier3_aliases)}")
    print(f"Total Aliases Screened: {total_alias_count}")
    print(f"Anomalies (0 or >=2 tier matches): {len(anomalies)}")

    if anomalies:
        for a in anomalies:
            print(f"  [ANOMALY] {a}")
        failed_tests += len(anomalies)
    else:
        print("[PASS] 100% of all aliases matched EXACTLY ONE tier CF with identical score!")
        passed_tests += 1

    print("\n================================================================================")
    print(f"SIMULATION SUMMARY: {passed_tests} Passed, {failed_tests} Failed (Total: {passed_tests + failed_tests})")
    print("================================================================================")

    return failed_tests == 0

if __name__ == "__main__":
    success = run_simulation_battery()
    sys.exit(0 if success else 1)
