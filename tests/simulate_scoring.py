#!/usr/bin/env python3
"""
PCD compact 4K HEVC scoring battery.

Movies 2160p HEVC Compact prefers a mid-size 2160p Blu-ray (hallowed,
BHDStudio, in-window HONE), then a smaller disc such as QxR, then a compact
streaming WEB-DL, then a PSA micro, then a big WEB-DL. 4K quality
definitions cap bitrate at 200 MB/min. There is no gigabyte penalty, so a
long movie at a mid-size bitrate keeps its score.
TV 2160p HEVC Compact still prefers WEB over disc. Feature bonuses stay
inside the 700-point gap, and Movies Anywhere does not flip a WEB over a disc.
"""

import sqlite3
import os
import re
import sys
import subprocess
import glob

def build_compiled_db():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_dir = os.environ.get("PCD_SCHEMA_PATH")
    if not schema_dir:
        candidate_deps_ops = os.path.join(repo_root, "deps", "schema", "ops")
        candidate_deps_root = os.path.join(repo_root, "deps", "schema")

        # Check standard sibling/parent deployment paths relative to repo root
        parent_dir = os.path.dirname(repo_root)
        candidate_sibling_deps = os.path.join(parent_dir, "deps", "schema", "ops")
        profilarr_matches = sorted(glob.glob(os.path.join(parent_dir, "config", "profilarr", "data", "databases", "*", "deps", "schema", "ops")))
        candidate_profilarr_deps = profilarr_matches[-1] if profilarr_matches else None

        if os.path.exists(candidate_deps_ops) and os.path.isdir(candidate_deps_ops):
            schema_dir = candidate_deps_ops
        elif os.path.exists(candidate_deps_root) and os.path.isdir(candidate_deps_root) and any(f.endswith(".sql") for f in os.listdir(candidate_deps_root)):
            schema_dir = candidate_deps_root
        elif os.path.exists(candidate_sibling_deps) and os.path.isdir(candidate_sibling_deps):
            schema_dir = candidate_sibling_deps
        elif candidate_profilarr_deps and os.path.exists(candidate_profilarr_deps):
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

def quality_limits(conn, quality_name, arr_type="radarr"):
    table = "radarr_quality_definitions" if arr_type == "radarr" else "sonarr_quality_definitions"
    return conn.execute(
        f"SELECT min_size, preferred_size, max_size FROM {table} WHERE quality_name = ?",
        (quality_name,),
    ).fetchall()

def bitrate_blocked(limits, mb_per_min):
    if mb_per_min is None or not limits:
        return False
    for min_size, _preferred, max_size in limits:
        if mb_per_min < min_size or mb_per_min > max_size:
            return True
    return False

def run_simulation_battery():
    conn = build_compiled_db()

    movies = "Movies 2160p HEVC Compact"
    tv = "TV 2160p HEVC Compact"
    tier_cfs = {
        "2160p Compact Bluray Tier 1",
        "2160p Compact Bluray Tier 2",
        "2160p Compact Bluray Tier 3",
        "2160p Compact Bluray Tier 4",
        "2160p Compact WEB Tier 1",
        "2160p Compact WEB Tier 2",
        "2160p Compact WEB Tier 3",
        "2160p Compact WEB Tier 4",
        "2160p WEB-DL HEVC",
        "2160p Compact Streaming WEB-DL",
        "1080p Compact HEVC Tier 1",
        "1080p Compact HEVC Tier 2",
        "1080p Compact HEVC Tier 3",
        "1080p Compact HEVC Tier 4",
    }

    test_corpus = [
        {
            "category": "Movie elite disc (HONE)",
            "title": "Movie.2024.2160p.BluRay.x265-HONE",
            "profile": movies,
            "expect_pass": True,
            "exact": 8100,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "category": "Movie elite disc parenthetical (Vyndros)",
            "title": "Movie (2024) (2160p BluRay x265 HDR DV Atmos - Vyndros).mkv",
            "profile": movies,
            "expect_pass": True,
            "min_band": 8100,
            "max_band": 8800,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "category": "Movie circle disc (Tigole / QxR)",
            "title": "Movie (2024) (2160p BluRay x265 10bit HDR - Tigole).mkv",
            "profile": movies,
            "expect_pass": True,
            "min_band": 7400,
            "max_band": 8000,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "category": "Movie circle supergroup suffix (Goki / TAoE)",
            "title": "Movie.2024.2160p.BluRay.x265-Goki)[TAoE].mkv",
            "profile": movies,
            "expect_pass": True,
            "exact": 7400,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "category": "Movie mid-size WEB stays under both disc tiers (hallowed)",
            "title": "Movie.2024.2160p.WEB-DL.H265-hallowed",
            "profile": movies,
            "expect_pass": True,
            "exact": 6700,
            "tier": "2160p Compact WEB Tier 1",
        },
        {
            "category": "Movie edge2020 WEB is the lower circle",
            "title": "Movie.2024.2160p.WEB-DL.H265-edge2020",
            "profile": movies,
            "expect_pass": True,
            "exact": 6000,
            "tier": "2160p Compact WEB Tier 2",
        },
        {
            "category": "Movie small-good disc (PSA)",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-PSA",
            "profile": movies,
            "expect_pass": True,
            "min_band": 5300,
            "max_band": 5999,
            "tier": "2160p Compact Bluray Tier 3",
        },
        {
            "category": "Movie micro-ok WEB (UTR) below PSA",
            "title": "Movie.2024.2160p.WEB-DL.x265-UTR",
            "profile": movies,
            "expect_pass": True,
            "exact": 3200,
            "tier": "2160p Compact WEB Tier 4",
        },
        {
            "category": "Movie RARBG disc is allowed and below PSA",
            "title": "Movie.2024.2160p.BluRay.x265-RARBG",
            "profile": movies,
            "expect_pass": True,
            "exact": 4600,
            "tier": "2160p Compact Bluray Tier 4",
        },
        {
            "category": "Movie d3g disc is allowed under QxR",
            "title": "Movie.2024.2160p.BluRay.x265-d3g",
            "profile": movies,
            "expect_pass": True,
            "exact": 5300,
            "tier": "2160p Compact Bluray Tier 3",
        },
        {
            "category": "Movie iVy WEB is the low small tier",
            "title": "Show.Name.S01E01.2160p.WEBRip.x265-iVy",
            "profile": movies,
            "expect_pass": True,
            "exact": 3200,
            "tier": "2160p Compact WEB Tier 4",
        },
        {
            "category": "Movie untouched WEB-DL fallback (NTb)",
            "title": "The.Silence.of.the.Lambs.1991.2160p.WEB-DL.H265-NTb",
            "profile": movies,
            "expect_pass": True,
            "exact": 2500,
            "tier": "2160p WEB-DL HEVC",
        },
        {
            "category": "Movie 1080p compact fallback (Vyndros)",
            "title": "Movie.2024.1080p.BluRay.x265-Vyndros",
            "profile": movies,
            "expect_pass": True,
            "exact": 1800,
            "tier": "1080p Compact HEVC Tier 1",
        },
        {
            "category": "Movie 1080p circle fallback (TAoE)",
            "title": "Movie.2024.1080p.WEBRip.H.265-TAoE",
            "profile": movies,
            "expect_pass": True,
            "exact": 1100,
            "tier": "1080p Compact HEVC Tier 2",
        },
        {
            "category": "Features cannot invert circle over elite",
            "title": "Movie.2024.2160p.BluRay.DV.HDR10+.HDR.DDP5.1.Atmos.x265-Tigole",
            "profile": movies,
            "expect_pass": True,
            "min_band": 7400,
            "max_band": 8099,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "category": "Untiered transparent disc stays under cutoff",
            "title": "Movie.2024.2160p.BluRay.DV.HDR.x265-FraMeSToR",
            "profile": movies,
            "expect_pass": False,
            "max_band": 399,
        },
        {
            "category": "AV1 disc is rejected",
            "title": "Movie.2024.2160p.BluRay.AV1.HDR-dAV1nci",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "Hybrid AV1 tag cannot ride a compact group",
            "title": "Movie.2024.2160p.BluRay.x265.AV1-Vyndros",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "Remux is rejected",
            "title": "Movie.2024.2160p.BluRay.Remux.HEVC-HONE",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "4K x264 is rejected",
            "title": "Movie.2024.2160p.BluRay.x264-HONE",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "YTS still rejected on a 4K panel",
            "title": "Movie.2024.2160p.BluRay.x265-YTS",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "YTS.mx is rejected",
            "title": "Movie.2024.2160p.BluRay.x265-YTS.mx",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "MeGusta is rejected",
            "title": "Movie.2024.2160p.WEBRip.x265-MeGusta",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "edge2020HD is not edge2020",
            "title": "Movie.2024.2160p.BluRay.x265-edge2020HD",
            "profile": movies,
            "expect_pass": False,
            "max_band": 399,
        },
        {
            "category": "Ghostbusters does not match the Ghost encoder",
            "title": "Ghostbusters.2016.2160p.BluRay.x265-HONE",
            "profile": movies,
            "expect_pass": True,
            "exact": 8100,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "category": "TV compact WEB outranks the same group's disc",
            "title": "Show.S01E01.2160p.WEB-DL.H265-HONE",
            "profile": tv,
            "expect_pass": True,
            "exact": 8100,
            "tier": "2160p Compact WEB Tier 1",
        },
        {
            "category": "TV disc is the lower tier",
            "title": "Show.S01E01.2160p.BluRay.x265-HONE",
            "profile": tv,
            "expect_pass": True,
            "exact": 5300,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "category": "TV circle WEB (RZeroX)",
            "title": "Show.S02E04.2160p.WEBRip.H265-RZeroX",
            "profile": tv,
            "expect_pass": True,
            "exact": 7400,
            "tier": "2160p Compact WEB Tier 2",
        },
        {
            "category": "Bracket prefix still matches",
            "title": "[TAoE] Movie.2024.2160p.BluRay.x265.mkv",
            "profile": movies,
            "expect_pass": True,
            "exact": 7400,
            "tier": "2160p Compact Bluray Tier 2",
        },
    ]

    print("================================================================================")
    print("COMPACT 4K HEVC PROFILE SIMULATION")
    print("================================================================================")

    passed_tests = 0
    failed_tests = 0

    def check(case):
        nonlocal passed_tests, failed_tests
        score, min_score, upgrade_until, passed_cutoff, matched = evaluate_release(
            conn, case["title"], case["profile"], case.get("arr_type", "radarr")
        )
        ok = passed_cutoff == case["expect_pass"]
        if "exact" in case and score != case["exact"]:
            ok = False
        if "min_band" in case and score < case["min_band"]:
            ok = False
        if "max_band" in case and score > case["max_band"]:
            ok = False
        tier_hits = [name for name, _ in matched if name in tier_cfs]
        if "tier" in case and tier_hits != [case["tier"]]:
            ok = False
        status = "PASS" if ok else "FAIL"
        if ok:
            passed_tests += 1
        else:
            failed_tests += 1
        print(f"\n[{status}] {case['category']}")
        print(f"  Title: {case['title']}")
        print(f"  Score: {score} cutoff {min_score} pass {passed_cutoff} expected {case['expect_pass']}")
        if tier_hits or "tier" in case:
            print(f"  Tier: {tier_hits} expected {case.get('tier')}")
        if not ok:
            for cf, s in matched:
                print(f"    - {cf}: {s:+}")
        return ok

    for case in test_corpus:
        check(case)

    print("\n=== MOVIES ANYWHERE DOES NOT BEAT A DISC ===")
    disc_title = "Movie.2024.2160p.BluRay.x265.DV.HDR.DDP5.1.10bit-HONE"
    plain_web = "Movie.2024.2160p.WEB-DL.x265.DV.HDR.DDP5.1.Atmos.10bit-HONE"
    ma_web = "Movie.2024.2160p.MA.WEB-DL.x265.DV.HDR.DDP5.1.Atmos.10bit-HONE"
    lower_ma = "Movie.2024.2160p.MA.WEB-DL.x265.DV.HDR.DDP5.1.Atmos.10bit-Tigole"
    disc_score, _, _, _, disc_matched = evaluate_release(conn, disc_title, movies)
    plain_score, _, _, _, plain_matched = evaluate_release(conn, plain_web, movies)
    ma_score, _, _, _, ma_matched = evaluate_release(conn, ma_web, movies, size_gb=16)
    lower_score, _, _, _, lower_matched = evaluate_release(conn, lower_ma, movies, size_gb=12)
    comparisons = (
        ("Plain HONE WEB stays under the HONE Blu-ray", plain_score < disc_score),
        ("Compact HONE Movies Anywhere WEB stays under the HONE Blu-ray", ma_score < disc_score),
        ("QxR Movies Anywhere WEB stays under the HONE Blu-ray", lower_score < disc_score),
        ("Movies Anywhere tag scored", any(name == "MA" and s == 15 for name, s in ma_matched)),
    )
    print(f"  disc {disc_score} plain {plain_score} ma {ma_score} lower {lower_score}")
    for name, ok in comparisons:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if ok:
            passed_tests += 1
        else:
            failed_tests += 1
            for label, matched in (("disc", disc_matched), ("plain", plain_matched), ("ma", ma_matched), ("lower", lower_matched)):
                print(f"  {label}: {matched}")

    print("\n=== LIBRARY PROOF (radarr4k 2026-11-06) ===")
    bluray_limits = quality_limits(conn, "Bluray-2160p")
    web_limits = quality_limits(conn, "WEBDL-2160p")
    limit_rows = conn.execute(
        """
        SELECT quality_name, min_size, preferred_size, max_size
        FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p')
        """
    ).fetchall()
    print("  2160p quality definitions:", limit_rows)

    def score_of(title, size_gb=None):
        score, _min_s, _until, passed, matched = evaluate_release(conn, title, movies, size_gb=size_gb)
        return score, passed, matched

    # Ocean's Twelve. History deleted BHDStudio 14.6 GiB / 119 MB/min for a
    # Tier 1 disc at 20.14 GiB / 165.0 MB/min. Both carry DV, HDR, DD+ and 10-bit.
    oceans_bhd, oceans_bhd_pass, oceans_bhd_matched = score_of(
        "Oceans.Twelve.2004.2160p.BluRay.DV.HDR.DDP5.1.10bit.x265-BHDStudio", 14.6
    )
    oceans_hone, oceans_hone_pass, oceans_hone_matched = score_of(
        "Oceans.Twelve.2004.2160p.BluRay.DV.HDR.DDP5.1.10bit.x265-HONE", 20.14
    )
    # Two Towers / Fellowship. Compact disc versus the 40 GiB HONE MA WEB.
    towers_disc, _, towers_disc_matched = score_of(
        "The.Lord.of.the.Rings.The.Two.Towers.2002.2160p.BluRay.DV.HDR.DDP5.1.10bit.x265-hallowed", 24.0
    )
    towers_bhd, _, _ = score_of(
        "The.Lord.of.the.Rings.The.Two.Towers.2002.2160p.BluRay.DV.HDR.DDP5.1.10bit.x265-BHDStudio", 23.5
    )
    towers_web_title = "The.Lord.of.the.Rings.The.Two.Towers.2002.Extended.2160p.MA.WEB-DL.DV.HDR.DDP5.1.Atmos.Hybrid.10bit.x265-HONE"
    towers_web, towers_web_pass, towers_web_matched = score_of(towers_web_title, 41.52)
    towers_web_small, _, _ = score_of(towers_web_title, 16.0)
    fellowship_web, fellowship_web_pass, fellowship_web_matched = score_of(
        "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.Extended.2160p.MA.WEB-DL.DV.HDR.DDP5.1.Atmos.Hybrid.10bit.x265-HONE",
        40.23,
    )
    # PSA beats a typical BYNDR (18.9 GB / ~181 MB/min) because BYNDR is in the
    # untouched bucket, not because the file is over 30 GiB. The same BYNDR
    # title at 36 GiB must score identically when its bitrate stays under the cap.
    psa, psa_pass, psa_matched = score_of(
        "The.Lord.of.the.Rings.The.Two.Towers.2002.2160p.BluRay.HDR.x265-PSA", 8.0
    )
    byndr_title = "The.Lord.of.the.Rings.The.Two.Towers.2002.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-BYNDR"
    byndr, byndr_pass, byndr_matched = score_of(byndr_title, 18.9)
    byndr_long, byndr_long_pass, byndr_long_matched = score_of(byndr_title, 36.0)
    # A 3-hour-plus HONE WEB at ~160 MB/min can exceed 30 GiB without being bloated.
    long_web_title = "Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.10bit.x265-HONE"
    long_web, long_web_pass, long_web_matched = score_of(long_web_title, 36.0)
    long_web_small, _, long_web_small_matched = score_of(long_web_title, 16.0)
    # Compact streaming WEB (Apple / Amazon / Netflix) beats PSA and loses to a compact disc.
    flux, flux_pass, flux_matched = score_of(
        "Movie.2024.2160p.ATVP.WEB-DL.DV.HDR.DDP5.1.H.265-FLUX", 15.9
    )
    kitsune, _, kitsune_matched = score_of(
        "Movie.2024.2160p.AMZN.WEB-DL.DV.HDR.DDP5.1.H.265-Kitsune", 15.3
    )
    cmrg, _, cmrg_matched = score_of(
        "Movie.2024.2160p.NF.WEB-DL.H.265-CMRG", 12.6
    )
    rotk, rotk_pass, rotk_matched = score_of(
        "The.Lord.of.the.Rings.The.Return.of.the.King.2003.Extended.2160p.BluRay.DV.HDR.DDP5.1.x265-hallowed",
        35.2,
    )

    oceans_bhd_blocked = bitrate_blocked(bluray_limits, 119)
    oceans_hone_blocked = bitrate_blocked(bluray_limits, 165)
    towers_web_blocked = bitrate_blocked(web_limits, 237.5)
    fellowship_blocked = bitrate_blocked(web_limits, 230.1)
    rotk_blocked = bitrate_blocked(bluray_limits, 179)
    hone_cap_blocked = bitrate_blocked(bluray_limits, 230)
    byndr_blocked = bitrate_blocked(web_limits, 181)
    byndr_long_blocked = bitrate_blocked(web_limits, 160)
    long_web_blocked = bitrate_blocked(web_limits, 160)
    flux_blocked = bitrate_blocked(web_limits, 147)
    no_size_penalty = conn.execute(
        "SELECT COUNT(*) FROM custom_formats WHERE name = '2160p Bloated WEB'"
    ).fetchone()[0] == 0

    upgrade_inc = conn.execute(
        "SELECT upgrade_score_increment FROM quality_profiles WHERE name = ?",
        (movies,),
    ).fetchone()[0]
    oceans_would_upgrade = (oceans_hone - oceans_bhd) >= upgrade_inc and not oceans_hone_blocked

    proof = (
        ("4K max size is 200 MB/min", all(row[3] == 200 for row in limit_rows) and len(limit_rows) == 4),
        ("4K preferred size is the 130 MB/min window", all(row[2] == 130 for row in limit_rows)),
        ("Ocean's Twelve BHDStudio is inside the cap", oceans_bhd_pass and not oceans_bhd_blocked),
        ("Ocean's Twelve HONE replacement is inside the cap", oceans_hone_pass and not oceans_hone_blocked),
        ("Ocean's Twelve BHDStudio scores at least the HONE replacement", oceans_bhd >= oceans_hone),
        ("Ocean's Twelve HONE does not upgrade BHDStudio", not oceans_would_upgrade),
        ("Two Towers compact disc outscores the HONE MA WEB", towers_disc > towers_web and towers_bhd > towers_web),
        ("Fellowship HONE MA WEB loses to that compact disc on score", towers_disc > fellowship_web),
        ("230 MB/min HONE MA WEB is rejected by the bitrate cap", towers_web_blocked and fellowship_blocked),
        ("HONE MA WEB score does not depend on file gigabytes", towers_web == towers_web_small),
        ("Return of the King hallowed at 179 MB/min stays inside the cap", rotk_pass and not rotk_blocked),
        ("A 230 MB/min HONE disc is rejected", hone_cap_blocked),
        ("PSA beats a typical BYNDR WEB-DL", psa > byndr and psa_pass and byndr_pass and not byndr_blocked),
        ("A 36 GiB BYNDR at 160 MB/min scores the same and still loses to PSA", byndr_long == byndr and psa > byndr_long and byndr_long_pass and not byndr_long_blocked),
        ("A 36 GiB HONE WEB at 160 MB/min is not bitrate-blocked", long_web_pass and not long_web_blocked),
        ("A long in-cap WEB scores the same as the small copy", long_web == long_web_small and long_web_matched == long_web_small_matched),
        ("That long WEB stays under the compact disc and above PSA", towers_disc > long_web > psa),
        ("No gigabyte WEB custom format exists", no_size_penalty),
        ("Compact FLUX WEB beats PSA", flux > psa and flux_pass and not flux_blocked),
        ("Compact FLUX WEB loses to the Two Towers disc", towers_disc > flux),
        ("Amazon Kitsune and Netflix CMRG beat PSA and lose to the disc", kitsune > psa and cmrg > psa and towers_disc > kitsune and towers_disc > cmrg),
        ("Apple TV tag scored on FLUX", any(name == "ATVP" for name, _ in flux_matched)),
        ("Amazon tag scored on Kitsune", any(name == "AMZN" for name, _ in kitsune_matched)),
        ("Netflix tag scored on CMRG", any(name == "NF" for name, _ in cmrg_matched)),
        ("YTS still banned", not score_of("Movie.2024.2160p.BluRay.x265-YTS")[1]),
    )
    print(f"  Ocean's Twelve BHD {oceans_bhd} HONE {oceans_hone} upgrade {oceans_would_upgrade}")
    print(f"  Two Towers disc {towers_disc} BHD {towers_bhd} MA WEB {towers_web} pass {towers_web_pass} blocked {towers_web_blocked}")
    print(f"  Fellowship MA WEB {fellowship_web} blocked {fellowship_blocked}")
    print(f"  PSA {psa} BYNDR {byndr} BYNDR 36 GiB {byndr_long}")
    print(f"  long HONE WEB {long_web} same title at 16 GiB {long_web_small}")
    print(f"  FLUX {flux} Kitsune {kitsune} CMRG {cmrg}")
    print(f"  ROTK hallowed {rotk} blocked {rotk_blocked}")
    for name, ok in proof:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if ok:
            passed_tests += 1
        else:
            failed_tests += 1
    if failed_tests:
        print("  Ocean's Twelve BHD", oceans_bhd_matched)
        print("  Ocean's Twelve HONE", oceans_hone_matched)
        print("  Two Towers disc", towers_disc_matched)
        print("  Two Towers WEB", towers_web_matched)
        print("  Fellowship WEB", fellowship_web_matched)
        print("  PSA", psa_matched)
        print("  BYNDR", byndr_matched)
        print("  BYNDR long", byndr_long_matched)
        print("  long WEB", long_web_matched)
        print("  FLUX", flux_matched)
        print("  ROTK", rotk_matched)

    inc = conn.execute(
        "SELECT upgrade_score_increment FROM quality_profiles WHERE name = ?",
        (movies,),
    ).fetchone()[0]
    print(f"\n=== UPGRADE INCREMENT ({inc}) ===")
    for name, existing, new, expect in (
        ("Same score does not swap", 8100, 8100, False),
        ("HDR tie-break upgrades inside a tier", 8100, 8280, True),
        ("1080p compact upgrades to 4K circle", 1800, 7400, True),
    ):
        fires = (new - existing) >= inc
        ok = fires == expect
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if ok:
            passed_tests += 1
        else:
            failed_tests += 1

    elite = ["HONE","Vyndros","dkore","GRiMM","TimeDistortion","DarQ","Vialle","Chivaman","Ralphy","YELLO","noxxus","ToNaTo","R1GY3B","bluegreeen","Weasley","DiscoD","hallowed","HQMUX","PTer","BHDStudio"]
    circle = ["QxR","afm72","Bandi","Bluespots","Celdra","FreetheFish","Garshasp","Ghost","Ime","Kappa","Langbard","LION","Panda","MONOLITH","Natty","r00t","RCVR","RZeroX","SAMPA","Silence","t3nzin","Tigole","YOGI","TAoE","Ainz","AJJMIN","ANONAZ","ArcX","bccornfo","DNU","DrainedDay","DUHIT","Erie","Frys","Goki","HxD","jb2049","JBENT","Nostradamus","r0b0t","Species180","TheSickle","xtrem3x","WEM","NAN0","SQS","LSt","SARTRE","honeyvera","MNHD","edge2020","HeVK","KeepFRDS","Prof"]
    streaming = ["FLUX","Kitsune","CMRG","CMaRG","CMRioG"]
    webdl = ["NTb","TEPES","MZABI","SMURF","XEBEC","4KBEC","CEBEX","BYNDR","HHWEB","DUSKLiGHT","playWEB","ABBIE","AJP69","BLUTONiUM","NOSiViD","SiC","SiGMA","RAWR","TOMMY"]
    small = ["PSA","PSARips","d3g","ELiTE","ReELiTE","SEV","Kira","D0ct0rLew","HODL","HiQVE","SIQ","PSYPHER","POOTLED","kronox","yawnix","DEFLATE","LEGi0N","IAMABLE"]
    micro_ok = ["UTR","Joy","RARBG","iVy","t0paz","POF","UTRcorp"]
    micro_ban = ["YTS","YIFY","MeGusta","GalaxyRG","Pahe","TGx","aXXo","ION10","ION265","RMTeam","QxC","EVO","HDHub4u"]

    print("\n=== GROUP LADDER ===")
    anomalies = []
    for group in elite:
        title = f"Movie.2024.2160p.BluRay.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Bluray Tier 1"] or score != 8100 or not passed:
            anomalies.append((group, "elite-disc", score, hits, [(n, s) for n, s in matched if s < 0]))
        web = f"Show.S01E01.2160p.WEB-DL.H265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, web, tv)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact WEB Tier 1"] or score != 8100:
            anomalies.append((group, "elite-web", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in circle:
        title = f"Movie.2024.2160p.BluRay.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Bluray Tier 2"] or score != 7400:
            anomalies.append((group, "circle-disc", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in small:
        title = f"Movie.2024.2160p.BluRay.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Bluray Tier 3"] or score != 5300:
            anomalies.append((group, "small-disc", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in micro_ok:
        title = f"Movie.2024.2160p.WEB-DL.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact WEB Tier 4"] or score != 3200:
            anomalies.append((group, "micro-ok-web", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in streaming:
        title = f"Movie.2024.2160p.WEB-DL.H265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Streaming WEB-DL"] or score != 6000:
            anomalies.append((group, "streaming-web", score, hits, [(n, s) for n, s in matched if s < 0]))
        tv_title = f"Show.S01E01.2160p.WEB-DL.H265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, tv_title, tv)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Streaming WEB-DL"] or score != 5300:
            anomalies.append((group, "streaming-tv", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in webdl:
        title = f"Movie.2024.2160p.WEB-DL.H265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p WEB-DL HEVC"] or score != 2500:
            anomalies.append((group, "webdl", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in micro_ban:
        title = f"Movie.2024.2160p.WEB-DL.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        if passed or score > 0:
            anomalies.append((group, "micro-ban", score, [n for n, _ in matched], []))

    # Negative boundaries
    for title in (
        "Movie.2024.2160p.BluRay.x265-XYZRH",
        "Movie.2024.2160p.BluRay.x265-edge2020HD",
        "The.Silence.of.the.Lambs.1991.2160p.BluRay.x265-NTb",
    ):
        score, _, _, _, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        # NTb bluray must not take the WEB-DL tier (source is bluray). Silence must not take the circle.
        if title.endswith("-NTb"):
            if hits:
                anomalies.append(("NTb-bluray", "negative", score, hits, []))
        elif hits:
            anomalies.append((title, "negative", score, hits, []))

    print(f"Aliases screened: {len(elite) + len(circle) + len(small) + len(micro_ok) + len(streaming) + len(webdl) + len(micro_ban)}")
    print(f"Anomalies: {len(anomalies)}")
    if anomalies:
        for row in anomalies:
            print("  [ANOMALY]", row)
        failed_tests += len(anomalies)
    else:
        print("[PASS] Every compact alias landed on exactly one tier")
        passed_tests += 1

    print("\n================================================================================")
    print(f"SIMULATION SUMMARY: {passed_tests} Passed, {failed_tests} Failed")
    print("================================================================================")
    return failed_tests == 0


if __name__ == "__main__":
    success = run_simulation_battery()
    sys.exit(0 if success else 1)
