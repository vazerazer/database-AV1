#!/usr/bin/env python3
"""
PCD compact 4K HEVC scoring battery.

Movies 2160p HEVC Compact prefers a mid-size 2160p Blu-ray. The whole elite
list shares one score (hallowed, BHDStudio, HONE, and the rest). Then a
smaller disc such as QxR, then compact streaming WEB, then PSA. A 4K
micro (RARBG, UTR, iVy, Joy, t0paz, POF) scores 0 and misses the minimum,
the same way an untouched 4K WEB-DL such as BYNDR or NTb does. The next
grab is 1080p: elite HEVC, then the circle, then FLUX/Kitsune/CMRG, then
PSA, then a micro that still clears 3000. An unrecognized 1080p HEVC
Blu-ray, WEB-DL, or WEBRip scores that same 3000, and so does any 1080p
AVC from those sources. Neither stacks on a 1080p tier that already
matched, and neither matches 2160p. A 720p HEVC or AVC Blu-ray, WEB-DL,
or WEBRip then scores 3000 in its own quality group under every 1080p
quality. Inside a class, Dolby Vision is +1000, HDR is +500, and
HDR10+ is +600 (our HDR format excludes HDR10+, so that is Dumpstarr's
500+100 stack). Dolby Digital + is +125, Dolby Digital is +115, Atmos is
+25, and AAC is +10. The 4K class gap is wider than that stack. 4K Blu-ray
with no HDR is rejected. A Dolby Vision WEB with no HDR token misses the
cutoff. TrueHD and the DTS-HD formats are rejected for direct play. LPCM,
FLAC, and lossy DTS are not. CAM, hardcoded subtitles, 3D, upscales,
extras, sing-along, audio description, and a non-HEVC codec on a tiered
disc miss the same way. Radarr max size stays 0, so nothing is rejected
for bitrate. Preferred size is the tie-break: 130 MB/min on 2160p encode
qualities and 18 MB/min on 1080p encode qualities. Remux stays preferred
1999 and stays off the compact profiles. There is no gigabyte penalty,
so a long movie keeps its score. TV 2160p HEVC Compact still prefers WEB
over disc. Its scores and Sonarr size rows are unchanged. Movies Anywhere
does not flip a WEB over a disc.
"""

import sqlite3
import os
import re
import sys
import subprocess
import glob

def build_compiled_db():
    global _GLOBAL_SCORING_CONTEXT
    _GLOBAL_SCORING_CONTEXT = None
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

    # Radarr QualityParser: UHD is a resolution, not a Blu-ray source.
    # Bare scene ".WEB." / "2160p.WEB." is WEB-DL. WEBRip stays WEBRip.
    is_bluray = bool(re.search(
        r"\b(?:M?Blu[-_. ]?Ray|HD[-_. ]?DVD(?:Rip)?|BDRip|BDLight|UHDBDRip|UHD2?BD|BDISO|BDMux|BD25|BD50|BR[-_. ]?DISK|BD(?!$))\b",
        title,
        re.IGNORECASE,
    ))
    is_webrip = bool(re.search(r"\b(?:WEB[-_. ]?Rip|WEBRip|WEBMux)\b", title, re.IGNORECASE))
    is_webdl = bool(re.search(
        r"\b(?:WEB[-_. ]?DL(?:mux)?|WEBDL)\b"
        r"|[. ]WEB[. ](?:[xh][ .]?26[45]|AVC|HEVC|DDP?5[. ]1)"
        r"|(?:\d{3,4}0p)[-. ](?:Hybrid[-_. ]?)?WEB[-. ]"
        r"|[-. ]WEB[-. ]\d{3,4}0p"
        r"|(?:AMZN|NF|DP)[. -]WEB[. -](?!Rip)",
        title,
        re.IGNORECASE,
    ))
    if is_webrip and not re.search(r"\b(?:WEB[-_. ]?DL(?:mux)?|WEBDL)\b", title, re.IGNORECASE):
        is_webdl = False
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
                # Radarr tests the parsed release group, not the whole title.
                # Searching the title made "Ben.Hur" and "E-AC-3" look banned.
                group_name = tokens["group"]
                if group_name:
                    for compiled_re, raw_pat in cond["pats"]:
                        if compiled_re:
                            if compiled_re.search(group_name):
                                cond_matched = True
                                break
                        elif raw_pat and regex_match(raw_pat, group_name):
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

        # Radarr: every required spec must match, and if any optional specs
        # exist then at least one of them must match. Remux is optional on
        # the title OR the quality modifier OR the source, not all three.
        if optional_types:
            cf_matched = all_required_met and bool(matched_optional_types)
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
    """Radarr rejects a release outside min/max MB/min.

    Min 0 is no floor. Max 0 is unlimited, which is how Dumpstarr stores
    an uncapped quality after op 367 and how Radarr treats a null max.
    Preferred size is not a reject.
    """
    if mb_per_min is None or not limits:
        return False
    for min_size, _preferred, max_size in limits:
        if min_size and mb_per_min < min_size:
            return True
        if max_size and mb_per_min > max_size:
            return True
    return False

# Movie class bases. 3200 is wider than the largest realistic extra stack.
# HDR in a title also matches 10-bit Depth (+30) because that regex treats
# the letters HDR as a 10-bit marker. HDR10+ does not also match HDR, so
# its score is Dumpstarr's combined HDR + HDR10+ weight.
M_BR1 = 38400
M_BR2 = 35200
M_WEB1 = 32000
M_STREAM = 28800
M_WEB2 = 28800
M_BR3 = 25600
M_BR4 = 0  # 4K micro disc misses min 3000 so Radarr can take 1080p instead
M_WEB3 = 19200
M_WEB4 = 0  # 4K micro WEB misses min 3000; the format stays assigned
M_WEBDL = 0  # untouched 4K WEB-DL is identified and does not clear min 3000
M_HD1 = 9600
M_HD2 = 6400
M_HD_STREAM = 5200
M_HD3 = 4100
M_HD4 = 3000
M_HDR = 530  # HDR +500 and 10-bit Depth +30
M_HDR10 = 600
M_DV = 1000
M_DDP = 125
M_DD = 115
M_ATMOS = 25
M_AAC = 10
M_SE = 125
M_DTS = 0
M_MA = 15
M_DSNP = 10  # Disney+ and iTunes
M_ATVP = 5   # Apple TV+, Max, HBO Max
M_SHOP = 2   # Amazon, Netflix, ATV, Hulu
M_IMF = 75
M_DV_BARE = -100000


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
        "1080p Compact Streaming WEB-DL",
        "1080p Compact HEVC Tier 3",
        "1080p Compact HEVC Tier 4",
    }

    test_corpus = [
        {
            "category": "Movie elite disc (HONE)",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-HONE",
            "profile": movies,
            "expect_pass": True,
            "exact": M_BR1 + M_HDR,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "category": "SDR 4K Blu-ray is rejected",
            "title": "Movie.2024.2160p.BluRay.x265-HONE",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "TrueHD disc is rejected for direct play",
            "title": "Movie.2024.2160p.BluRay.HDR.TrueHD.Atmos.x265-hallowed",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "DTS-HD MA disc is rejected for direct play",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.MA.x265-BHDStudio",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "DTS-HD HRA disc is rejected for direct play",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.HRA.x265-HONE",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "DTS-X disc is rejected for direct play",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-X.x265-DarQ",
            "profile": movies,
            "expect_pass": False,
            "max_band": 0,
        },
        {
            "category": "Movie elite disc parenthetical (Vyndros)",
            "title": "Movie (2024) (2160p BluRay x265 HDR DV Atmos - Vyndros).mkv",
            "profile": movies,
            "expect_pass": True,
            "min_band": M_BR1,
            "max_band": M_BR1 + 2500,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "category": "Movie circle disc (Tigole / QxR)",
            "title": "Movie (2024) (2160p BluRay x265 10bit HDR - Tigole).mkv",
            "profile": movies,
            "expect_pass": True,
            "min_band": M_BR2,
            "max_band": M_BR1 - 1,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "category": "Movie circle supergroup suffix (Goki / TAoE)",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-Goki)[TAoE].mkv",
            "profile": movies,
            "expect_pass": True,
            "exact": M_BR2 + M_HDR,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "category": "Movie mid-size WEB stays under both disc tiers (hallowed)",
            "title": "Movie.2024.2160p.WEB-DL.H265-hallowed",
            "profile": movies,
            "expect_pass": True,
            "exact": M_WEB1,
            "tier": "2160p Compact WEB Tier 1",
        },
        {
            "category": "Movie edge2020 WEB is the lower circle",
            "title": "Movie.2024.2160p.WEB-DL.H265-edge2020",
            "profile": movies,
            "expect_pass": True,
            "exact": M_WEB2,
            "tier": "2160p Compact WEB Tier 2",
        },
        {
            "category": "Movie small-good disc (PSA)",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-PSA",
            "profile": movies,
            "expect_pass": True,
            "min_band": M_BR3,
            "max_band": M_STREAM - 1,
            "tier": "2160p Compact Bluray Tier 3",
        },
        {
            "category": "Movie micro-ok WEB (UTR) misses the minimum",
            "title": "Movie.2024.2160p.WEB-DL.x265-UTR",
            "profile": movies,
            "expect_pass": False,
            "exact": M_WEB4,
            "max_band": 2999,
            "tier": "2160p Compact WEB Tier 4",
        },
        {
            "category": "Movie RARBG disc misses the minimum",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-RARBG",
            "profile": movies,
            "expect_pass": False,
            "exact": M_BR4 + M_HDR,
            "max_band": 2999,
            "tier": "2160p Compact Bluray Tier 4",
        },
        {
            "category": "Movie d3g disc is allowed under QxR",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-d3g",
            "profile": movies,
            "expect_pass": True,
            "exact": M_BR3 + M_HDR,
            "tier": "2160p Compact Bluray Tier 3",
        },
        {
            "category": "Movie iVy WEB misses the minimum",
            "title": "Show.Name.S01E01.2160p.WEBRip.x265-iVy",
            "profile": movies,
            "expect_pass": False,
            "exact": M_WEB4,
            "max_band": 2999,
            "tier": "2160p Compact WEB Tier 4",
        },
        {
            "category": "Movie untouched WEB-DL is not a 4K grab (NTb)",
            "title": "The.Silence.of.the.Lambs.1991.2160p.WEB-DL.H265-NTb",
            "profile": movies,
            "expect_pass": False,
            "exact": M_WEBDL,
            "max_band": 2999,
            "tier": "2160p WEB-DL HEVC",
        },
        {
            "category": "Movie 1080p compact fallback (Vyndros)",
            "title": "Movie.2024.1080p.BluRay.x265-Vyndros",
            "profile": movies,
            "expect_pass": True,
            "exact": M_HD1,
            "tier": "1080p Compact HEVC Tier 1",
        },
        {
            "category": "Movie 1080p circle fallback (TAoE)",
            "title": "Movie.2024.1080p.WEBRip.H.265-TAoE",
            "profile": movies,
            "expect_pass": True,
            "exact": M_HD2,
            "tier": "1080p Compact HEVC Tier 2",
        },
        {
            "category": "Features cannot invert circle over elite",
            "title": "Movie.2024.2160p.BluRay.DV.HDR10+.HDR.DDP5.1.Atmos.x265-Tigole",
            "profile": movies,
            "expect_pass": True,
            "min_band": M_BR2,
            "max_band": M_BR1 - 1,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "category": "Untiered transparent disc stays under cutoff",
            "title": "Movie.2024.2160p.BluRay.DV.HDR.x265-FraMeSToR",
            "profile": movies,
            "expect_pass": False,
            "max_band": 2999,
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
            "title": "Ghostbusters.2016.2160p.BluRay.HDR.x265-HONE",
            "profile": movies,
            "expect_pass": True,
            "exact": M_BR1 + M_HDR,
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
            "title": "[TAoE] Movie.2024.2160p.BluRay.HDR.x265.mkv",
            "profile": movies,
            "expect_pass": True,
            "exact": M_BR2 + M_HDR,
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
    hd_limits = quality_limits(conn, "Bluray-1080p")
    limit_rows = conn.execute(
        """
        SELECT quality_name, min_size, preferred_size, max_size
        FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p')
        """
    ).fetchall()
    hd_rows = conn.execute(
        """
        SELECT quality_name, min_size, preferred_size, max_size
        FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p')
        """
    ).fetchall()
    remux_rows = conn.execute(
        """
        SELECT quality_name, min_size, preferred_size, max_size
        FROM radarr_quality_definitions
        WHERE quality_name IN ('Remux-2160p', 'Remux-1080p')
        """
    ).fetchall()
    untouched_rows = conn.execute(
        """
        SELECT quality_name, min_size, preferred_size, max_size
        FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-720p', 'WEBDL-720p', 'WEBRip-720p', 'HDTV-720p')
        """
    ).fetchall()
    sonarr_2160 = quality_limits(conn, "Bluray-2160p", "sonarr")
    sonarr_1080 = quality_limits(conn, "Bluray-1080p", "sonarr")
    print("  2160p quality definitions:", limit_rows)
    print("  1080p quality definitions:", hd_rows)
    print("  remux quality definitions:", remux_rows)

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
    # Above the old 1080p max of 40. Ralphy, DarQ, HONE, Tigole and TAoE
    # fallbacks already in a library often sit here.
    hd_large_blocked = bitrate_blocked(hd_limits, 80)
    def size_window(rows, n, preferred):
        return len(rows) == n and all(row[1] == 0 and row[2] == preferred and row[3] == 0 for row in rows)
    no_size_penalty = conn.execute(
        "SELECT COUNT(*) FROM custom_formats WHERE name = '2160p Bloated WEB'"
    ).fetchone()[0] == 0

    upgrade_inc = conn.execute(
        "SELECT upgrade_score_increment FROM quality_profiles WHERE name = ?",
        (movies,),
    ).fetchone()[0]
    oceans_would_upgrade = (oceans_hone - oceans_bhd) >= upgrade_inc and not oceans_hone_blocked

    proof = (
        ("4K size is min 0, preferred 130, max 0", size_window(limit_rows, 4, 130)),
        ("1080p size is min 0, preferred 18, max 0", size_window(hd_rows, 4, 18)),
        ("Remux size is min 0, preferred 1999, max 0", size_window(remux_rows, 2, 1999)),
        ("720p stays min 0, preferred 1990, max 0", len(untouched_rows) == 4 and all(row[1] == 0 and row[2] == 1990 and row[3] == 0 for row in untouched_rows)),
        ("Sonarr 2160p size stays 6 / 130 / 200", sonarr_2160 == [(6, 130, 200)]),
        ("Sonarr 1080p size stays 2 / 10 / 30", sonarr_1080 == [(2, 10, 30)]),
        ("Ocean's Twelve BHDStudio is not size-rejected", oceans_bhd_pass and not oceans_bhd_blocked),
        ("Ocean's Twelve HONE replacement is not size-rejected", oceans_hone_pass and not oceans_hone_blocked),
        ("Ocean's Twelve BHDStudio scores at least the HONE replacement", oceans_bhd >= oceans_hone),
        ("Ocean's Twelve HONE does not upgrade BHDStudio", not oceans_would_upgrade),
        ("Two Towers compact disc outscores the HONE MA WEB", towers_disc > towers_web and towers_bhd > towers_web),
        ("Fellowship HONE MA WEB loses to that compact disc on score", towers_disc > fellowship_web),
        ("230 MB/min HONE MA WEB is not size-rejected", (not towers_web_blocked) and (not fellowship_blocked)),
        ("HONE MA WEB score does not depend on file gigabytes", towers_web == towers_web_small),
        ("Return of the King hallowed at 179 MB/min is not size-rejected", rotk_pass and not rotk_blocked),
        ("A 230 MB/min HONE disc is not size-rejected", not hone_cap_blocked),
        ("An 80 MB/min 1080p encode is not size-rejected", not hd_large_blocked),
        ("PSA outscores BYNDR, and BYNDR misses the minimum", psa > byndr and psa_pass and (not byndr_pass) and byndr < 3000 and not byndr_blocked),
        ("A 36 GiB BYNDR at 160 MB/min scores the same and still misses the minimum", byndr_long == byndr and (not byndr_long_pass) and byndr_long < 3000 and not byndr_long_blocked),
        ("A 36 GiB HONE WEB at 160 MB/min is not bitrate-blocked", long_web_pass and not long_web_blocked),
        ("A long WEB scores the same as the small copy", long_web == long_web_small and long_web_matched == long_web_small_matched),
        ("That long WEB stays under the compact disc and above PSA", towers_disc > long_web > psa),
        ("No gigabyte WEB custom format exists", no_size_penalty),
        ("Compact FLUX WEB beats PSA", flux > psa and flux_pass and not flux_blocked),
        ("Compact FLUX WEB loses to the Two Towers disc", towers_disc > flux),
        ("Amazon Kitsune and Netflix CMRG beat PSA and lose to the disc", kitsune > psa and cmrg > psa and towers_disc > kitsune and towers_disc > cmrg),
        ("Apple TV tag scored on FLUX", any(name == "ATVP" for name, _ in flux_matched)),
        ("Amazon tag scored on Kitsune", any(name == "AMZN" for name, _ in kitsune_matched)),
        ("Netflix tag scored on CMRG", any(name == "NF" for name, _ in cmrg_matched)),
        ("YTS still banned", not score_of("Movie.2024.2160p.BluRay.x265-YTS")[1]),
        ("MeGusta still banned", not score_of("Movie.2024.2160p.WEBRip.x265-MeGusta")[1]),
        ("Dolby Vision scores +1000 on the compact disc", any(name == "Dolby Vision" and s == M_DV for name, s in towers_disc_matched)),
        ("HDR scores +500 on the compact disc", any(name == "HDR" and s == 500 for name, s in towers_disc_matched)),
        ("DD+ scores +125 on the compact disc", any(name == "Dolby Digital +" and s == M_DDP for name, s in towers_disc_matched)),
        ("hallowed, BHDStudio and HONE HDR discs share one score", len({score_of(f"Movie.2024.2160p.BluRay.HDR.x265-{g}")[0] for g in ("hallowed", "BHDStudio", "HONE", "DarQ", "DiscoD", "dkore", "HQMUX", "PTer", "Chivaman", "Weasley", "Vyndros")}) == 1),
        ("IMAX adds no movie score, so it cannot beat Atmos", score_of("Movie.2024.2160p.BluRay.HDR.IMAX.x265-hallowed")[0] - score_of("Movie.2024.2160p.BluRay.HDR.x265-hallowed")[0] == 0),
        ("PSARip micro beats BYNDR", score_of("Movie.2024.2160p.BluRay.HDR.x265-PSARips")[0] > byndr),
        ("d3g micro beats NTb", score_of("Movie.2024.2160p.BluRay.HDR.x265-d3g")[0] > score_of("Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-NTb")[0]),
        ("Coyote-style PSA WEBRip beats a much larger BYNDR", score_of("Coyote.vs.Acme.2026.2160p.WEBRip.HDR.x265-PSA")[0] > score_of("Coyote.vs.Acme.2026.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-BYNDR")[0]),
        ("TV still prefers HONE WEB over HONE disc", evaluate_release(conn, "Show.S01E01.2160p.WEB-DL.H265-HONE", tv)[0] > evaluate_release(conn, "Show.S01E01.2160p.BluRay.HDR.x265-HONE", tv)[0]),
        ("TV TrueHD disc is still allowed", evaluate_release(conn, "Show.S01E01.2160p.BluRay.HDR.TrueHD.x265-HONE", tv)[3]),
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
        ("Same score does not swap", M_BR1, M_BR1, False),
        ("HDR tie-break upgrades inside a tier", M_BR1, M_BR1 + M_HDR, True),
        ("1080p compact upgrades to 4K circle", M_HD1, M_BR2, True),
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
        title = f"Movie.2024.2160p.BluRay.HDR.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Bluray Tier 1"] or score != M_BR1 + M_HDR or not passed:
            anomalies.append((group, "elite-disc", score, hits, [(n, s) for n, s in matched if s < 0]))
        web = f"Show.S01E01.2160p.WEB-DL.H265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, web, tv)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact WEB Tier 1"] or score != 8100:
            anomalies.append((group, "elite-web", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in circle:
        title = f"Movie.2024.2160p.BluRay.HDR.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Bluray Tier 2"] or score != M_BR2 + M_HDR:
            anomalies.append((group, "circle-disc", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in small:
        title = f"Movie.2024.2160p.BluRay.HDR.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Bluray Tier 3"] or score != M_BR3 + M_HDR:
            anomalies.append((group, "small-disc", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in micro_ok:
        title = f"Movie.2024.2160p.WEB-DL.x265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact WEB Tier 4"] or score != M_WEB4 or passed:
            anomalies.append((group, "micro-ok-web", score, hits, [(n, s) for n, s in matched if s < 0]))
    for group in streaming:
        title = f"Movie.2024.2160p.WEB-DL.H265-{group}"
        score, _, _, passed, matched = evaluate_release(conn, title, movies)
        hits = [n for n, _ in matched if n in tier_cfs]
        if hits != ["2160p Compact Streaming WEB-DL"] or score != M_STREAM:
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
        if hits != ["2160p WEB-DL HEVC"] or score != M_WEBDL or passed:
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

    stress_passed, stress_failed = run_identification_stress(conn, movies, tv)
    passed_tests += stress_passed
    failed_tests += stress_failed

    tie_passed, tie_failed = run_dumpstarr_tiebreak_order(conn)
    passed_tests += tie_passed
    failed_tests += tie_failed

    ladder_passed, ladder_failed = run_movie_fallback_ladder(conn, movies, tv)
    passed_tests += ladder_passed
    failed_tests += ladder_failed

    empty_passed, empty_failed = run_empty_assigned_format_guard(conn, movies, tv)
    passed_tests += empty_passed
    failed_tests += empty_failed

    last_passed, last_failed = run_1080p_last_resort(conn, movies, tv)
    passed_tests += last_passed
    failed_tests += last_failed

    sd_passed, sd_failed = run_720p_last_resort(conn, movies, tv)
    passed_tests += sd_passed
    failed_tests += sd_failed

    print("\n================================================================================")
    print(f"SIMULATION SUMMARY: {passed_tests} Passed, {failed_tests} Failed")
    print("================================================================================")
    return failed_tests == 0


def _compact_parity_cases():
    """Dumpstarr/Dictionarry edge cases for Movies 2160p HEVC Compact.

    Hard rejects on a tiered HDR disc have to miss cutoff 3000. A -10000
    penalty does not, because the class base is 38400. Dolby Vision WEB
    without an HDR token misses cutoff the same way. German scene dubs
    with a channel count (DDP5.1.DL) are a -750 penalty, not a ban.
    Disney+ and Apple TV+ still count when the plus sign sits against a dot.
    """
    out = []

    def add(name, title, **kw):
        if "absent" in kw:
            kw["not"] = kw.pop("absent")
        if "not_" in kw:
            kw["not"] = kw.pop("not_")
        out.append({"name": name, "title": title, **kw})

    elite = M_BR1 + M_HDR
    ban = elite - 100000
    stream = M_STREAM + M_HDR

    # Each of these is a real reject stacked on an elite HDR encode.
    # The tier still matches. The penalty has to clear it.
    for name, title, flag in (
        ("Elite HDR CAM misses cutoff", "Movie.2024.2160p.BluRay.HDR.CAM.x265-HONE", "CAM"),
        ("Elite HDR HDCAM misses cutoff", "Movie.2024.2160p.BluRay.HDR.HDCAM.x265-HONE", "CAM"),
        ("Elite HDR TELESYNC misses cutoff", "Movie.2024.2160p.BluRay.HDR.TELESYNC.x265-hallowed", "CAM"),
        ("Elite HDR TS misses cutoff", "Movie.2024.2160p.BluRay.HDR.TS.x265-HONE", "CAM"),
        ("Elite HDR SCREENER misses cutoff", "Movie.2024.2160p.BluRay.HDR.SCREENER.x265-HONE", "CAM"),
        ("Elite HDR WORKPRINT misses cutoff", "Movie.2024.2160p.BluRay.HDR.WORKPRINT.x265-HONE", "CAM"),
        ("Elite HDR ProRes misses cutoff", "Movie.2024.2160p.BluRay.HDR.ProRes.x265-HONE", "CAM"),
        ("Elite HDR HC misses cutoff", "Movie.2024.2160p.BluRay.HDR.HC.x265-HONE", "Hardcoded Subtitles"),
        ("Elite HDR HARDSUB misses cutoff", "Movie.2024.2160p.BluRay.HDR.HARDSUB.x265-HONE", "Hardcoded Subtitles"),
        ("Elite HDR HARDSUBBED misses cutoff", "Movie.2024.2160p.BluRay.HDR.HARDSUBBED.x265-HONE", "Hardcoded Subtitles"),
        ("Elite HDR KORSUB misses cutoff", "Movie.2024.2160p.BluRay.HDR.KORSUB.x265-HONE", "Hardcoded Subtitles"),
        ("Elite HDR VFF.HC misses cutoff", "Movie.2024.2160p.BluRay.HDR.VFF.HC.x265-HONE", "Hardcoded Subtitles"),
        ("Subbed before the resolution misses cutoff", "Movie.2024.Subbed.2160p.BluRay.HDR.x265-HONE", "Hardcoded Subtitles"),
        ("Elite HDR 3D misses cutoff", "Movie.2024.2160p.BluRay.HDR.3D.x265-HONE", "3D"),
        ("Elite HDR Upscaled misses cutoff", "Movie.2024.2160p.BluRay.HDR.Upscaled.x265-HONE", "Upscale"),
        ("Elite HDR AI Enhanced misses cutoff", "Movie.2024.2160p.BluRay.HDR.AI.Enhanced.HEVC-HONE", "Upscale"),
        ("Elite HDR Extras misses cutoff", "Movie.2024.2160p.BluRay.HDR.Extras.x265-HONE", "Extras"),
        ("Elite HDR Bonus misses cutoff", "Movie.2024.2160p.BluRay.HDR.Bonus.x265-HONE", "Extras"),
        ("Elite HDR Deleted Scenes misses cutoff", "Movie.2024.2160p.BluRay.HDR.Deleted.Scenes.x265-HONE", "Extras"),
        ("Elite HDR Extended Clip is extras and misses cutoff", "Movie.2024.2160p.BluRay.HDR.Extended.Clip.x265-HONE", "Extras"),
        ("Elite HDR Sing Along misses cutoff", "Movie.2024.2160p.BluRay.HDR.Sing.Along.x265-HONE", "Sing Along"),
        ("Elite HDR Audio Description misses cutoff", "Movie.2024.2160p.BluRay.HDR.Audio.Description.x265-HONE", "Audio Description"),
        ("Elite HDR ASL misses cutoff", "Movie.2024.2160p.BluRay.HDR.ASL.x265-HONE", "Audio Description"),
        ("Elite HDR DVS misses cutoff", "Movie.2024.2160p.BluRay.HDR.DVS.x265-HONE", "Audio Description"),
        ("Elite HDR BSL misses cutoff", "Movie.2024.2160p.BluRay.HDR.BSL.x265-HONE", "Audio Description"),
        ("AVC named beside x265 misses cutoff", "Movie.2024.2160p.BluRay.HDR.AVC.x265-HONE", "x264 (2160p)"),
        ("VP9 named beside x265 misses cutoff", "Movie.2024.2160p.BluRay.HDR.VP9.x265-HONE", "VP9"),
        ("VVC named beside HEVC misses cutoff", "Movie.2024.2160p.BluRay.HDR.HEVC.VVC-HONE", "VVC"),
    ):
        add(
            name,
            title,
            exact=ban,
            passes=False,
            has=[flag, "2160p Compact Bluray Tier 1", "HDR"],
            absent=["2160p SDR Bluray", "Dolby Vision (Without Fallback)"],
        )
    add(
        "Special Features is extras and also the loose Special token",
        "Movie.2024.2160p.BluRay.HDR.Special.Features.x265-HONE",
        exact=ban + M_SE,
        passes=False,
        has=["Extras", "Special Edition", "2160p Compact Bluray Tier 1"],
        absent=["2160p SDR Bluray"],
    )

    add(
        "English Subbed after the resolution is not hardcoded",
        "Movie.2024.2160p.BluRay.HDR.English.Subbed.x265-HONE",
        exact=elite,
        passes=True,
        has=["2160p Compact Bluray Tier 1"],
        absent=["Hardcoded Subtitles", "CAM", "Extras"],
    )
    add(
        "Anchorman is not hardcoded",
        "Anchorman.The.Legend.of.Ron.Burgundy.2004.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        passes=True,
        absent=["Hardcoded Subtitles", "CAM", "Banned Groups"],
    )
    add(
        "The Machinist is not hardcoded",
        "The.Machinist.2004.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        passes=True,
        absent=["Hardcoded Subtitles"],
    )
    add(
        "Chapter is not hardcoded and not a special edition",
        "John.Wick.Chapter.4.2023.2160p.BluRay.HDR.DDP5.1.x265-HONE",
        exact=M_BR1 + M_HDR + M_DDP,
        passes=True,
        absent=["Hardcoded Subtitles", "Special Edition", "Extras", "CAM"],
    )
    add(
        "A plain elite HDR disc matches none of the hard rejects",
        "Movie.2024.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        passes=True,
        has=["2160p Compact Bluray Tier 1", "HDR", "10-bit Depth"],
        absent=[
            "CAM", "Hardcoded Subtitles", "3D", "Upscale", "Extras", "Sing Along",
            "Audio Description", "x264 (2160p)", "AV1", "VP9", "VVC", "Full Disc",
            "Remux", "Foreign Dub", "2160p SDR Bluray", "Banned Groups",
            "Dolby Vision (Without Fallback)", "Special Edition",
        ],
    )

    # HDR implies one 10-bit score. A second 10bit token does not add another +30.
    add(
        "HDR implies 10-bit without a 10bit token",
        "Movie.2024.2160p.BluRay.HDR.x265-hallowed",
        exact=elite,
        has=["10-bit Depth", "HDR"],
        absent=["HDR10+", "8-bit Depth"],
    )
    add(
        "Explicit 10bit next to HDR is still one 10-bit score",
        "Movie.2024.2160p.BluRay.HDR.10bit.x265-hallowed",
        exact=elite,
        has=["10-bit Depth", "HDR"],
    )
    add(
        "8-bit token is a tie-break, not a ban",
        "Movie.2024.2160p.BluRay.8bit.HDR.x265-dkore",
        exact=elite - 800,
        passes=True,
        has=["8-bit Depth", "HDR", "2160p Compact Bluray Tier 1"],
        absent=["2160p SDR Bluray"],
    )

    # Editions. DC after the year is a director's cut. Words before the year are not.
    for name, title in (
        ("Directors Cut is a special edition", "Movie.2024.2160p.BluRay.HDR.Directors.Cut.x265-HONE"),
        ("DC token is a special edition", "Movie.2024.2160p.BluRay.HDR.DC.x265-HONE"),
        ("Extended is a special edition", "Movie.2024.2160p.BluRay.HDR.Extended.x265-HONE"),
        ("Unrated is a special edition", "Movie.2024.2160p.BluRay.HDR.Unrated.x265-HONE"),
        ("Uncut after the year is a special edition", "Movie.2024.2160p.BluRay.HDR.Uncut.x265-HONE"),
        ("Special Edition words score once", "Movie.2024.2160p.BluRay.HDR.Special.Edition.x265-HONE"),
    ):
        add(name, title, exact=elite + M_SE, passes=True, has=["Special Edition"], absent=["Extras", "2160p SDR Bluray"])
    add(
        "Uncut Gems before the year is not a special edition",
        "Uncut.Gems.2019.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        absent=["Special Edition", "Extras"],
    )
    add(
        "Dune Part Two is not a special edition",
        "Dune.Part.Two.2024.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        absent=["Special Edition", "Extras", "3D"],
    )
    add(
        "The Batman is not a special edition",
        "The.Batman.2022.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        absent=["Special Edition"],
    )
    add(
        "Theatrical is not a special edition",
        "Movie.2024.2160p.BluRay.Theatrical.HDR.x265-HONE",
        exact=elite,
        absent=["Special Edition", "Extras"],
    )
    add(
        "Open Matte is not a special edition",
        "Movie.2024.2160p.BluRay.Open.Matte.HDR.x265-HONE",
        exact=elite,
        absent=["Special Edition"],
    )
    add(
        "Extended Clip is extras, not a special edition",
        "Movie.2024.2160p.BluRay.Extended.Clip.HDR.x265-HONE",
        exact=ban,
        passes=False,
        has=["Extras"],
        absent=["Special Edition"],
    )

    # Disc vs WEB, encode vs full disc.
    add(
        "HEVC word on a Blu-ray encode is not a full disc",
        "Movie.2024.2160p.UHD.BluRay.HEVC.HDR.x265-BHDStudio",
        exact=elite,
        passes=True,
        has=["2160p Compact Bluray Tier 1"],
        absent=["Full Disc", "Remux", "2160p Compact WEB Tier 1"],
    )
    add(
        "COMPLETE next to HEVC is an encode, not a full disc",
        "Movie.2024.2160p.UHD.BluRay.COMPLETE.HDR.HEVC-HONE",
        exact=elite,
        passes=True,
        absent=["Full Disc", "Remux"],
    )
    add(
        "BD50 next to HEVC is an encode, not a full disc",
        "Movie.2024.2160p.BluRay.BD50.HDR.HEVC-HONE",
        exact=elite,
        passes=True,
        absent=["Full Disc"],
    )
    add(
        "COMPLETE UHD Blu-ray without a codec is a full disc",
        "Movie.2024.COMPLETE.UHD.BLURAY-TERRA",
        passes=False,
        has=["Full Disc"],
        absent=["2160p Compact Bluray Tier 1", "2160p Compact WEB Tier 1", "HDR"],
    )
    add(
        "COMPLETE UHD Blu-ray HDR without a codec misses cutoff",
        "Movie.2024.COMPLETE.UHD.BLURAY.HDR-HONE",
        passes=False,
        has=["Full Disc", "HDR"],
        absent=["2160p Compact Bluray Tier 1", "2160p SDR Bluray"],
    )
    add(
        "BD50 without a codec is a full disc",
        "Movie.2024.UHD.BluRay.BD50-GROUP",
        passes=False,
        has=["Full Disc"],
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "UHD66 without a codec is a full disc",
        "Movie.2024.UHD66.BluRay-GROUP",
        passes=False,
        has=["Full Disc"],
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "ISO without a codec is a full disc",
        "Movie.2024.2160p.BluRay.ISO-HONE",
        passes=False,
        has=["Full Disc"],
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "REMUX does not take a compact tier",
        "Movie.2024.2160p.UHD.BluRay.REMUX.HDR.HEVC-HONE",
        passes=False,
        has=["Remux", "HDR"],
        absent=["2160p Compact Bluray Tier 1", "Full Disc", "2160p SDR Bluray"],
    )
    add(
        "HONE Blu-ray is not a WEB tier",
        "Movie.2024.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        tier="2160p Compact Bluray Tier 1",
        absent=["2160p Compact WEB Tier 1", "2160p Compact Streaming WEB-DL", "2160p WEB-DL HEVC"],
    )
    add(
        "HONE WEB is not a Blu-ray tier",
        "Movie.2024.2160p.WEB-DL.HDR.x265-HONE",
        exact=M_WEB1 + M_HDR,
        tier="2160p Compact WEB Tier 1",
        absent=["2160p Compact Bluray Tier 1", "2160p SDR Bluray", "2160p Compact Streaming WEB-DL"],
    )
    add(
        "Scene WEB token is WEB-DL",
        "Movie.2024.2160p.WEB.HDR.H.265-HONE",
        exact=M_WEB1 + M_HDR,
        tier="2160p Compact WEB Tier 1",
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "WEBRip is not a disc tier",
        "Movie.2024.2160p.WEBRip.HDR.x265-PSA",
        exact=M_WEB3 + M_HDR,
        tier="2160p Compact WEB Tier 3",
        absent=["2160p Compact Bluray Tier 3"],
    )
    add(
        "FLUX on Blu-ray is not streaming and not elite disc",
        "Movie.2024.2160p.BluRay.HDR.x265-FLUX",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Streaming WEB-DL", "2160p Compact Bluray Tier 1", "2160p Compact WEB Tier 1"],
    )
    add(
        "HDTV is not a compact tier",
        "Movie.2024.2160p.HDTV.HDR.x265-HONE",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Bluray Tier 1", "2160p Compact WEB Tier 1"],
    )

    # German scene dubs, including a channel count between the codec and DL.
    dub_web = 30 + 500 + 125 - 750
    add(
        "German DDP5.1.DL WEB GHOST is a dub and not circle WEB",
        "Movie.2024.GERMAN.DDP5.1.DL.2160p.WEB.HDR.x265-GHOST",
        exact=dub_web,
        passes=False,
        has=["Foreign Dub", "Dolby Digital +", "HDR"],
        absent=["CAM", "2160p Compact WEB Tier 2", "2160p Compact Bluray Tier 2", "2160p SDR Bluray"],
    )
    add(
        "German DDP.5.1.DL WEB GHOST is a dub and not circle WEB",
        "Movie.2024.German.DDP.5.1.DL.2160p.WEB.HDR.x265-GHOST",
        exact=dub_web,
        passes=False,
        has=["Foreign Dub"],
        absent=["2160p Compact WEB Tier 2", "CAM"],
    )
    add(
        "German EAC3.5.1.DL WEB GHOST is a dub and not circle WEB",
        "Movie.2024.German.EAC3.5.1.DL.2160p.WEB.x265-GHOST",
        exact=125 - 750,
        passes=False,
        has=["Foreign Dub", "Dolby Digital +"],
        absent=["2160p Compact WEB Tier 2", "Dolby Digital", "CAM"],
    )
    add(
        "German DD+.5.1.DL WEB GHOST is a dub",
        "Movie.2024.German.DD+.5.1.DL.2160p.WEB.HDR.x265-GHOST",
        exact=dub_web,
        passes=False,
        has=["Foreign Dub", "Dolby Digital +"],
        absent=["2160p Compact WEB Tier 2"],
    )
    add(
        "German EC3.DL WEB GHOST is a dub",
        "Movie.2024.German.EC3.DL.2160p.WEB.HDR.x265-GHOST",
        exact=dub_web,
        passes=False,
        has=["Foreign Dub", "Dolby Digital +"],
        absent=["2160p Compact WEB Tier 2", "Dolby Digital"],
    )
    add(
        "German DD5.1.DL WEB GHOST is a dub",
        "Movie.2024.German.DD5.1.DL.2160p.WEB.HDR.x265-GHOST",
        exact=30 + 500 + M_DD - 750,
        passes=False,
        has=["Foreign Dub", "Dolby Digital"],
        absent=["Dolby Digital +", "2160p Compact WEB Tier 2"],
    )
    add(
        "German AC3.5.1.DL Blu-ray keeps the elite tier",
        "Movie.2024.German.AC3.5.1.DL.2160p.BluRay.HDR.x265-hallowed",
        exact=M_BR1 + M_HDR + M_DD - 750,
        passes=True,
        has=["2160p Compact Bluray Tier 1", "Foreign Dub", "Dolby Digital"],
        absent=["CAM", "Full Disc", "Dolby Digital +", "2160p Compact WEB Tier 2"],
    )
    add(
        "German DDP5.1.DL on a Ghost Blu-ray stays circle disc",
        "Movie.2024.German.DDP5.1.DL.2160p.BluRay.HDR.x265-Ghost",
        exact=M_BR2 + M_HDR + M_DDP - 750,
        passes=True,
        tier="2160p Compact Bluray Tier 2",
        has=["Foreign Dub", "Dolby Digital +"],
        absent=["CAM", "2160p Compact WEB Tier 2", "Full Disc"],
    )
    add(
        "Italian AC3.MD WEB GHOST is a dub and not circle",
        "Movie.2024.Italian.AC3.MD.2160p.WEB.HDR.x265-GHOST",
        exact=30 + 500 + M_DD - 750,
        passes=False,
        has=["Foreign Dub", "Dolby Digital"],
        absent=["CAM", "2160p Compact WEB Tier 2"],
    )
    add(
        "Spanish DL WEB GHOST is a dub",
        "Movie.2024.Spanish.DL.2160p.WEB.x265-GHOST",
        exact=-750,
        passes=False,
        has=["Foreign Dub"],
        absent=["CAM", "2160p Compact WEB Tier 2"],
    )
    add(
        "French AC3.LD Blu-ray Ghost stays circle",
        "Movie.2024.FRENCH.AC3.LD.2160p.BluRay.HDR.x265-Ghost",
        exact=M_BR2 + M_HDR + M_DD - 750,
        passes=True,
        tier="2160p Compact Bluray Tier 2",
        has=["Foreign Dub"],
        absent=["CAM", "2160p Compact WEB Tier 2"],
    )
    add(
        "German DDP5.1 WEB-DL without a dub tag is not a dub",
        "Movie.2024.German.DDP5.1.2160p.WEB-DL.HDR.x265-FLUX",
        exact=stream + M_DDP,
        passes=True,
        tier="2160p Compact Streaming WEB-DL",
        absent=["Foreign Dub", "CAM", "2160p Compact WEB Tier 2"],
    )
    add(
        "German.WEB-DL is not a dub",
        "Movie.2024.German.WEB-DL.2160p.HDR.x265-FLUX",
        exact=stream,
        passes=True,
        absent=["Foreign Dub", "CAM"],
    )
    add(
        "WEB-DL.German is not a dub",
        "Movie.2024.WEB-DL.German.2160p.HDR.x265-FLUX",
        exact=stream,
        passes=True,
        absent=["Foreign Dub"],
    )
    add(
        "GERMAN.ML is not a dub",
        "Movie.2024.GERMAN.ML.2160p.BluRay.HDR.x265-hallowed",
        exact=elite,
        passes=True,
        absent=["Foreign Dub", "CAM", "Full Disc"],
    )
    add(
        "English GHOST WEB stays circle",
        "Movie.2024.2160p.WEB-DL.HDR.x265-GHOST",
        exact=M_WEB2 + M_HDR,
        passes=True,
        tier="2160p Compact WEB Tier 2",
        absent=["Foreign Dub", "CAM"],
    )
    add(
        "GHOSTS is not the Ghost encoder",
        "Movie.2024.2160p.BluRay.HDR.x265-GHOSTS",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Bluray Tier 2", "2160p Compact WEB Tier 2", "Foreign Dub"],
    )
    add(
        "Ghostbusters is not the Ghost encoder",
        "Ghostbusters.2016.2160p.BluRay.HDR.x265-HONE",
        exact=elite,
        tier="2160p Compact Bluray Tier 1",
        absent=["2160p Compact Bluray Tier 2"],
    )

    # Audio. Lossy DTS beside DD+ keeps DTS. HD audio beside DD+ still rejects.
    add(
        "TrueHD Atmos DDP rejects on TrueHD and not on DD+",
        "Movie.2024.2160p.BluRay.HDR.TrueHD.Atmos.DDP5.1.x265-hallowed",
        exact=elite + M_ATMOS - 100000,
        passes=False,
        has=["TrueHD", "Atmos"],
        absent=["Dolby Digital +", "Dolby Digital", "DTS-HD MA"],
    )
    add(
        "DTS-HD MA beside DD+ rejects",
        "Movie.2024.2160p.BluRay.HDR.DTS-HD.MA.DDP5.1.x265-BHDStudio",
        exact=elite - 100000,
        passes=False,
        has=["DTS-HD MA"],
        absent=["Dolby Digital +", "DTS", "MA"],
    )
    add(
        "DTS-HD HRA beside DD+ rejects",
        "Movie.2024.2160p.BluRay.HDR.DTS-HD.HRA.DDP5.1.x265-HONE",
        exact=elite - 100000,
        passes=False,
        has=["DTS-HD HRA"],
        absent=["Dolby Digital +", "DTS-HD MA"],
    )
    add(
        "DTS-X beside DD+ rejects",
        "Movie.2024.2160p.BluRay.HDR.DTS-X.DDP5.1.x265-DarQ",
        exact=elite - 100000,
        passes=False,
        has=["DTS-X"],
        absent=["Dolby Digital +", "DTS"],
    )
    add(
        "WEB FLUX DTS-HD MA beside DDP still rejects",
        "Movie.2024.2160p.WEB-DL.DTS-HD.MA.7.1.DDP.5.1.HDR.H.265-FLUX",
        passes=False,
        has=["DTS-HD MA", "2160p Compact Streaming WEB-DL"],
        absent=["Dolby Digital +", "MA"],
    )
    add(
        "Lossy DTS beside DD+ keeps DTS",
        "Movie.2024.2160p.BluRay.HDR.DTS.DDP5.1.x265-hallowed",
        exact=elite + M_DTS,
        passes=True,
        has=["DTS"],
        absent=["Dolby Digital +", "DTS-HD MA", "TrueHD"],
    )
    add(
        "EC3 is Dolby Digital Plus",
        "Movie.2024.2160p.BluRay.HDR.EC3.5.1.x265-hallowed",
        exact=elite + M_DDP,
        has=["Dolby Digital +"],
        absent=["Dolby Digital", "Banned Groups"],
    )
    add(
        "LPCM is not TrueHD and is not banned",
        "Movie.2024.2160p.BluRay.HDR.LPCM.5.1.x265-hallowed",
        exact=elite,
        passes=True,
        has=["2160p Compact Bluray Tier 1", "HDR"],
        absent=["TrueHD", "DTS-HD MA", "DTS-X", "Dolby Digital +", "2160p SDR Bluray"],
    )
    add(
        "PCM is not TrueHD and is not banned",
        "Movie.2024.2160p.BluRay.HDR.PCM.7.1.x265-hallowed",
        exact=elite,
        passes=True,
        absent=["TrueHD", "DTS-HD MA"],
    )

    # Storefronts stay small. Dumpstarr's order, divided by 5 so MA stays +15:
    # MA, then DSNP and iTunes, then ATVP / MAX / HMAX, then ATV / AMZN / NF / HULU.
    add(
        "ATVP is +5 and not ATV",
        "Movie.2024.2160p.ATVP.WEB-DL.HDR.H.265-Kitsune",
        exact=stream + M_ATVP,
        passes=True,
        has=["ATVP", "2160p Compact Streaming WEB-DL"],
        absent=["ATV", "iT"],
    )
    add(
        "ATV is +2 and not ATVP",
        "Movie.2024.2160p.ATV.WEB-DL.HDR.H.265-Kitsune",
        exact=stream + M_SHOP,
        passes=True,
        has=["ATV", "2160p Compact Streaming WEB-DL"],
        absent=["ATVP", "iT"],
    )
    add(
        "Apple.TV+ scores ATVP",
        "Movie.2024.2160p.Apple.TV+.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_ATVP,
        passes=True,
        has=["ATVP"],
        absent=["ATV", "iT"],
    )
    add(
        "Apple TV+ with a space scores ATVP",
        "Movie.2024.2160p.Apple TV+.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_ATVP,
        has=["ATVP"],
        absent=["ATV"],
    )
    add(
        "DSNP is +10",
        "Movie.2024.2160p.DSNP.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_DSNP,
        has=["DSNP"],
        absent=["HULU", "ATVP"],
    )
    add(
        "Disney+ before a dot scores DSNP",
        "Movie.2024.2160p.Disney+.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_DSNP,
        passes=True,
        has=["DSNP"],
        absent=["HULU", "ATVP"],
    )
    add(
        "DSNY scores DSNP",
        "Movie.2024.2160p.DSNY.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_DSNP,
        has=["DSNP"],
    )
    add(
        "Glued DSNPWEB does not score DSNP",
        "Movie.2024.2160p.DSNPWEB.WEB-DL.HDR.H.265-FLUX",
        exact=stream,
        absent=["DSNP"],
    )
    add(
        "HMAX is +5 and not MAX",
        "Movie.2024.2160p.HMAX.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_ATVP,
        has=["HMAX"],
        absent=["MAX"],
    )
    add(
        "MAX.WEB-DL is +5 and not HMAX",
        "Movie.2024.2160p.MAX.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_ATVP,
        has=["MAX"],
        absent=["HMAX"],
    )
    add(
        "HBO.MAX.WEB-DL is HMAX and not MAX",
        "Movie.2024.2160p.HBO.MAX.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_ATVP,
        has=["HMAX"],
        absent=["MAX"],
    )
    add(
        "AMZN is +2",
        "Movie.2024.2160p.AMZN.WEB-DL.HDR.H.265-Kitsune",
        exact=stream + M_SHOP,
        has=["AMZN"],
    )
    add(
        "AMAZON.WEB-DL is AMZN",
        "Movie.2024.2160p.AMAZON.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_SHOP,
        has=["AMZN"],
    )
    add(
        "NF is +2",
        "Movie.2024.2160p.NF.WEB-DL.HDR.H.265-CMRG",
        exact=stream + M_SHOP,
        has=["NF"],
    )
    add(
        "Netflix word is NF",
        "Movie.2024.2160p.Netflix.WEB-DL.HDR.H.265-CMRG",
        exact=stream + M_SHOP,
        has=["NF"],
    )
    add(
        "iT.WEB-DL is +10",
        "Movie.2024.2160p.iT.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_DSNP,
        has=["iT"],
        absent=["ATVP", "ATV"],
    )
    add(
        "iTunes.WEB-DL is iT",
        "Movie.2024.2160p.iTunes.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_DSNP,
        has=["iT"],
        absent=["ATVP"],
    )
    add(
        "HULU is +2",
        "Movie.2024.2160p.HULU.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_SHOP,
        has=["HULU"],
        absent=["DSNP"],
    )
    add(
        "MA WEB is +15 and does not beat an elite disc",
        "Movie.2024.2160p.MA.WEB-DL.DV.HDR.DDP5.1.H.265-HONE",
        passes=True,
        has=["MA", "2160p Compact WEB Tier 1", "Dolby Vision"],
        absent=["2160p Compact Bluray Tier 1", "DTS-HD MA"],
        above="Movie.2024.2160p.BluRay.HDR.x265-PSA",
    )
    add(
        "Elite disc beats that MA WEB",
        "Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-hallowed",
        above="Movie.2024.2160p.MA.WEB-DL.DV.HDR.DDP5.1.H.265-HONE",
    )
    add(
        "MA on a Blu-ray without WEB does not score",
        "Movie.2024.2160p.MA.BluRay.HDR.x265-hallowed",
        exact=elite,
        absent=["MA"],
    )
    add(
        "DTS-HD MA Blu-ray is not Movies Anywhere",
        "Movie.2024.2160p.BluRay.DTS-HD.MA.7.1.HDR.x265-hallowed",
        passes=False,
        has=["DTS-HD MA"],
        absent=["MA"],
    )

    # HDR spellings, DV fallback, hybrid, IMAX.
    for name, title, has, absent in (
        ("HDR10PLUS uppercase is HDR10+", "Movie.2024.2160p.UHD.BluRay.HDR10PLUS.x265-hallowed", ["HDR10+"], ["HDR", "2160p SDR Bluray"]),
        ("Bracketed HDR10Plus is HDR10+", "Movie.2024.2160p.UHD.BluRay.[HDR10Plus].x265-hallowed", ["HDR10+", "2160p Compact Bluray Tier 1"], ["2160p SDR Bluray", "HDR"]),
        ("Bracketed DV HDR10Plus scores both once", "Dark.Phoenix.2019.2160p.BluRay.[DV.HDR10Plus].x265-BHDStudio", ["Dolby Vision", "HDR10+", "2160p Compact Bluray Tier 1"], ["HDR", "2160p SDR Bluray", "Dolby Vision (Without Fallback)"]),
        ("Scene HDR is HDR, not HDR10+", "X-Men.Dark.Phoenix.2019.UHD.BluRay.2160p.HDR.x265-BHDStudio", ["HDR", "2160p Compact Bluray Tier 1"], ["HDR10+", "2160p SDR Bluray"]),
    ):
        add(name, title, has=has, not_=absent)

    add(
        "WEB DV without HDR from FLUX misses cutoff",
        "Movie.2024.2160p.WEB-DL.DV.x265-FLUX",
        exact=M_STREAM + 30 + M_DV + M_DV_BARE,
        passes=False,
        has=["2160p Compact Streaming WEB-DL", "Dolby Vision", "Dolby Vision (Without Fallback)"],
        absent=["HDR", "HDR10+", "2160p SDR Bluray"],
    )
    add(
        "Untiered WEB DV without HDR misses cutoff",
        "Movie.2024.2160p.WEB-DL.DV.x265-NOGROUP",
        passes=False,
        has=["Dolby Vision", "Dolby Vision (Without Fallback)"],
        absent=["2160p Compact Streaming WEB-DL", "HDR"],
    )
    add(
        "WEB DV with HDR is not without-fallback",
        "Movie.2024.2160p.WEB-DL.DV.HDR.x265-FLUX",
        exact=stream + 1000,
        passes=True,
        has=["Dolby Vision", "HDR"],
        absent=["Dolby Vision (Without Fallback)", "2160p SDR Bluray"],
    )
    add(
        "WEB DoVi SDR is without-fallback and misses cutoff",
        "Movie.2024.2160p.WEB-DL.DoVi.SDR.x265-FLUX",
        exact=M_STREAM + 30 + M_DV + M_DV_BARE,
        passes=False,
        has=["Dolby Vision (Without Fallback)"],
        absent=["HDR", "2160p SDR Bluray"],
    )
    add(
        "Blu-ray DV without HDR is not SDR and not without-fallback",
        "Movie.2024.2160p.BluRay.DV.x265-hallowed",
        exact=M_BR1 + 30 + 1000,
        passes=True,
        has=["Dolby Vision"],
        absent=["2160p SDR Bluray", "Dolby Vision (Without Fallback)", "HDR"],
    )
    add(
        "WEB SDR without HDR is allowed",
        "Movie.2024.2160p.WEB.SDR.x265-FLUX",
        exact=M_STREAM,
        passes=True,
        has=["2160p Compact Streaming WEB-DL"],
        absent=["2160p SDR Bluray", "HDR", "Dolby Vision"],
    )
    add(
        "WEB SDR plus HDR scores HDR and is not an SDR Blu-ray",
        "Movie.2024.2160p.WEB-DL.SDR.HDR.x265-FLUX",
        exact=stream,
        has=["HDR"],
        absent=["2160p SDR Bluray", "Dolby Vision (Without Fallback)"],
    )
    add(
        "Hybrid Blu-ray is a tie-break inside the elite class",
        "Movie.2024.2160p.Hybrid.BluRay.HDR.x265-hallowed",
        exact=elite + 15,
        passes=True,
        has=["Hybrid", "2160p Compact Bluray Tier 1"],
        absent=["2160p Compact Streaming WEB-DL"],
    )
    add(
        "The Hybrid as a title still only adds the tie-break",
        "The.Hybrid.2024.2160p.BluRay.HDR.x265-HONE",
        exact=elite + 15,
        has=["Hybrid"],
    )
    add(
        "HYBRID WEB scores Hybrid and not a disc tier",
        "Movie.2024.2160p.HYBRID.WEB-DL.DV.HDR.H.265-FLUX",
        exact=stream + 1000 + 15,
        has=["Hybrid", "Dolby Vision", "HDR"],
        absent=["Dolby Vision (Without Fallback)", "2160p Compact Bluray Tier 1"],
    )
    add(
        "Plain IMAX is IMAX and not IMAX Enhanced",
        "Movie.2024.2160p.BluRay.HDR.IMAX.x265-hallowed",
        exact=elite,
        has=["IMAX"],
        absent=["IMAX Enhanced"],
    )
    add(
        "WEB IMAX without a Disney token is IMAX",
        "Movie.2024.2160p.WEB-DL.IMAX.HDR.H.265-FLUX",
        exact=stream,
        has=["IMAX", "2160p Compact Streaming WEB-DL"],
        absent=["IMAX Enhanced"],
    )
    add(
        "DSNP IMAX is IMAX Enhanced and not IMAX",
        "Movie.2024.2160p.IMAX.Enhanced.DSNP.WEB-DL.HDR.H.265-FLUX",
        exact=stream + M_DSNP,
        has=["IMAX Enhanced", "DSNP"],
        absent=["IMAX"],
    )
    add(
        "DSNP IMAX without the Enhanced words is still IMAX Enhanced",
        "Movie.2024.2160p.DSNP.WEB-DL.IMAX.HDR.H.265-CMRG",
        exact=stream + M_DSNP,
        has=["IMAX Enhanced", "DSNP"],
        absent=["IMAX"],
    )
    add(
        "NON-IMAX is neither IMAX format",
        "Movie.2024.2160p.BluRay.NON-IMAX.HDR.x265-hallowed",
        exact=elite,
        absent=["IMAX", "IMAX Enhanced"],
    )

    # Groups that must not be promoted, and short banned-group traps.
    add(
        "Release group E is banned",
        "Movie.2024.2160p.BluRay.HDR.x265-E",
        passes=False,
        has=["Banned Groups"],
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "E-AC-3 is not the banned group E",
        "Movie.2024.2160p.BluRay.HDR.E-AC-3.x265-HONE",
        exact=elite + M_DDP,
        passes=True,
        absent=["Banned Groups"],
    )
    add(
        "E.T. is not the banned group E",
        "E.T.1982.2160p.BluRay.HDR.x265-hallowed",
        exact=elite,
        absent=["Banned Groups"],
    )
    add(
        "ELiTE is the small tier and not banned",
        "Movie.2024.2160p.BluRay.HDR.x265-ELiTE",
        exact=M_BR3 + M_HDR,
        passes=True,
        tier="2160p Compact Bluray Tier 3",
        absent=["Banned Groups", "2160p Compact Bluray Tier 1"],
    )
    add(
        "Saon is banned",
        "Movie.2024.2160p.BluRay.HDR.x265-Saon",
        passes=False,
        has=["Banned Groups"],
        absent=["2160p Compact Bluray Tier 1", "2160p Compact Bluray Tier 2"],
    )
    add(
        "Saonara is not Saon",
        "Movie.2024.2160p.BluRay.HDR.x265-Saonara",
        exact=M_HDR,
        passes=False,
        absent=["Banned Groups", "2160p Compact Bluray Tier 1"],
    )
    add(
        "PiRaTeS is not added to a tier",
        "Movie.2024.2160p.BluRay.HDR.x265-PiRaTeS",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Bluray Tier 1", "2160p WEB-DL HEVC", "2160p Compact Streaming WEB-DL"],
    )
    add(
        "PiRaTeS WEB is not added to a tier",
        "Movie.2024.2160p.WEB-DL.HDR.x265-PiRaTeS",
        exact=M_HDR,
        passes=False,
        absent=["2160p WEB-DL HEVC", "2160p Compact WEB Tier 1"],
    )
    add(
        "ZAX is not added to a tier",
        "Movie.2024.2160p.BluRay.HDR.x265-ZAX",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "edge2020HD is not edge2020",
        "Movie.2024.2160p.BluRay.HDR.x265-edge2020HD",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Bluray Tier 2", "2160p Compact Bluray Tier 1"],
    )
    add(
        "HONE-HiFi is not HONE",
        "Movie.2024.2160p.BluRay.HDR.x265-HONE-HiFi",
        exact=M_HDR,
        passes=False,
        absent=["2160p Compact Bluray Tier 1"],
    )
    add(
        "Silence of the Lambs from hallowed is elite, not the Silence encoder",
        "The.Silence.of.the.Lambs.1991.2160p.BluRay.HDR.x265-hallowed",
        exact=elite,
        tier="2160p Compact Bluray Tier 1",
        absent=["2160p Compact Bluray Tier 2"],
    )
    add(
        "YTS.mx stays banned",
        "Movie.2024.2160p.BluRay.HDR.x265-YTS.mx",
        passes=False,
        has=["Banned Micro Encodes"],
        absent=["2160p Compact Bluray Tier 4"],
    )
    add(
        "REPACK3 is only the third repack score",
        "Movie.2024.REPACK3.2160p.BluRay.HDR.x265-HONE",
        exact=elite + 7,
        has=["Repack3"],
        absent=["Repack1", "Repack2"],
    )
    add(
        "Streaming WEB still beats PSA and loses to an elite disc",
        "Movie.2024.2160p.ATVP.WEB-DL.DV.HDR.DDP5.1.H.265-FLUX",
        above="Movie.2024.2160p.BluRay.HDR.x265-PSA",
    )
    add(
        "Elite disc still beats compact streaming WEB",
        "Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-hallowed",
        above="Movie.2024.2160p.ATVP.WEB-DL.DV.HDR.DDP5.1.H.265-FLUX",
    )
    add(
        "PSA still beats untouched BYNDR",
        "Movie.2024.2160p.BluRay.HDR.x265-PSA",
        above="Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-BYNDR",
    )

    return out


def run_identification_stress(conn, movies, tv):
    """Adversarial titles for every Movies 2160p HEVC Compact format class.

    Scores below are the direct-play ladder (elite disc 38400, circle disc
    35200, elite WEB 32000, circle/streaming WEB 28800) plus the feature
    weights that actually match the name. HDR implies 10-bit (+30).
    """
    print("\n=== IDENTIFICATION STRESS ===")
    passed = 0
    failed = 0
    tier_names = {
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
        "1080p Compact Streaming WEB-DL",
        "1080p Compact HEVC Tier 3",
        "1080p Compact HEVC Tier 4",
    }

    cases = [
        {
            "name": "Ministry hallowed HDR10Plus is not SDR",
            "title": "The.Ministry.of.Ungentlemanly.Warfare.2024.UHD.BluRay.2160p.DDP.7.1.HDR10Plus.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10 + M_DDP,
            "has": ["2160p Compact Bluray Tier 1", "HDR10+", "Dolby Digital +", "10-bit Depth"],
            "not": ["2160p SDR Bluray", "HDR", "CAM", "Dolby Digital"],
        },
        {
            "name": "HDR10+ symbol is HDR10+ and 10-bit, not SDR",
            "title": "Movie.2024.2160p.UHD.BluRay.DDP.7.1.HDR10+.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10 + M_DDP,
            "has": ["HDR10+", "10-bit Depth"],
            "not": ["2160p SDR Bluray", "HDR"],
        },
        {
            "name": "HDR10P is HDR10+ and 10-bit, not SDR",
            "title": "Movie.2024.2160p.UHD.BluRay.DDP.7.1.HDR10P.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10 + M_DDP,
            "has": ["HDR10+"],
            "not": ["2160p SDR Bluray", "HDR"],
        },
        {
            "name": "HDR10plus is HDR10+ and 10-bit, not SDR",
            "title": "Movie.2024.2160p.UHD.BluRay.DDP.7.1.HDR10plus.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10 + M_DDP,
            "has": ["HDR10+"],
            "not": ["2160p SDR Bluray", "HDR"],
        },
        {
            "name": "HDR+ is the HDR10+ format",
            "title": "Movie.2024.2160p.BluRay.HDR+.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10,
            "has": ["HDR10+", "10-bit Depth"],
            "not": ["HDR", "2160p SDR Bluray"],
        },
        {
            "name": "Plain HDR is HDR, not HDR10+ and not SDR",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-hallowed",
            "exact": M_BR1 + M_HDR,
            "has": ["HDR", "10-bit Depth"],
            "not": ["HDR10+", "2160p SDR Bluray"],
        },
        {
            "name": "HDR10 is HDR, not a second HDR10+ score",
            "title": "Movie.2024.2160p.BluRay.HDR10.x265-hallowed",
            "exact": M_BR1 + M_HDR,
            "has": ["HDR"],
            "not": ["HDR10+", "2160p SDR Bluray"],
        },
        {
            "name": "HDR and HDR10+ together score HDR10+ once",
            "title": "Movie.2024.2160p.BluRay.HDR.HDR10+.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10,
            "has": ["HDR10+"],
            "not": ["HDR", "2160p SDR Bluray"],
        },
        {
            "name": "HLG is HDR and 10-bit, not SDR",
            "title": "Movie.2024.2160p.BluRay.HLG.x265-hallowed",
            "exact": M_BR1 + 30 + 500,
            "has": ["HDR", "10-bit Depth"],
            "not": ["2160p SDR Bluray", "HDR10+"],
        },
        {
            "name": "PQ is HDR and 10-bit, not SDR",
            "title": "Movie.2024.2160p.BluRay.PQ.x265-hallowed",
            "exact": M_BR1 + 30 + 500,
            "has": ["HDR", "10-bit Depth"],
            "not": ["2160p SDR Bluray"],
        },
        {
            "name": "PQ10 is HDR and 10-bit, not SDR",
            "title": "Movie.2024.2160p.BluRay.PQ10.x265-hallowed",
            "exact": M_BR1 + 30 + 500,
            "has": ["HDR"],
            "not": ["2160p SDR Bluray"],
        },
        {
            "name": "Dark Phoenix hallowed HDR10Plus is not SDR",
            "title": "X-Men.Dark.Phoenix.2019.UHD.BluRay.2160p.DDP.7.1.HDR10Plus.x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10 + M_DDP,
            "has": ["2160p Compact Bluray Tier 1", "HDR10+", "Dolby Digital +"],
            "not": ["2160p SDR Bluray", "HDR"],
        },
        {
            "name": "Ralphy DV+HDR Ministry matches the live 40055 file",
            "title": "The.Ministry.Of.Ungentlemanly.Warfare.2024.2160p.UHD.BluRay.DD+.7.1.DV.HDR.X265-Ralphy",
            "exact": 40055,
            "has": ["2160p Compact Bluray Tier 1", "Dolby Vision", "HDR", "Dolby Digital +", "10-bit Depth"],
            "not": ["2160p SDR Bluray", "HDR10+", "Dolby Vision (Without Fallback)"],
        },
        {
            "name": "Mutiny hallowed HDR10Plus disc is elite, not SDR",
            "title": "Mutiny 2026 UHD BluRay 2160p DDP 5 1 Atmos HDR10Plus x265-hallowed",
            "exact": M_BR1 + 30 + M_HDR10 + M_DDP + M_ATMOS,
            "has": ["2160p Compact Bluray Tier 1", "HDR10+", "Dolby Digital +", "Atmos", "10-bit Depth"],
            "not": ["2160p SDR Bluray", "CAM"],
        },
        {
            "name": "Yi Yi dkore with no HDR token stays SDR",
            "title": "Yi.Yi.2000.2160p.BluRay.x265-dkore",
            "exact": M_BR1 - 100000,
            "has": ["2160p Compact Bluray Tier 1", "2160p SDR Bluray"],
            "not": ["HDR", "HDR10+", "Dolby Vision"],
        },
        {
            "name": "Promised Land dkore with no HDR token stays SDR",
            "title": "The.Promised.Land.2023.2160p.BluRay.x265-dkore",
            "exact": M_BR1 - 100000,
            "has": ["2160p SDR Bluray"],
            "not": ["HDR", "HDR10+", "Dolby Vision"],
        },
        {
            "name": "10-bit SDR with no HDR token stays SDR",
            "title": "Movie.2024.2160p.BluRay.10bit.SDR.x265-dkore",
            "exact": M_BR1 + 30 - 100000,
            "has": ["2160p SDR Bluray", "10-bit Depth"],
            "not": ["HDR", "HDR10+"],
        },
        {
            "name": "Blu-ray DV without an HDR token is not SDR and not without-fallback",
            "title": "Movie.2024.2160p.BluRay.DV.x265-hallowed",
            "exact": M_BR1 + 30 + 1000,
            "has": ["Dolby Vision", "10-bit Depth"],
            "not": ["2160p SDR Bluray", "Dolby Vision (Without Fallback)", "HDR"],
        },
        {
            "name": "DoVi plus HDR scores both and is not SDR",
            "title": "Movie.2024.2160p.BluRay.DoVi.HDR.x265-hallowed",
            "exact": M_BR1 + 30 + 1000 + 500,
            "has": ["Dolby Vision", "HDR"],
            "not": ["2160p SDR Bluray", "Dolby Vision (Without Fallback)"],
        },
        {
            "name": "Dolby Vision words plus HDR10",
            "title": "Movie.2024.2160p.BluRay.Dolby.Vision.HDR10.x265-hallowed",
            "exact": M_BR1 + 30 + 1000 + 500,
            "has": ["Dolby Vision", "HDR"],
            "not": ["2160p SDR Bluray", "HDR10+"],
        },
        {
            "name": "DV plus HDR10Plus scores DV and HDR10+ once",
            "title": "Movie.2024.2160p.BluRay.DV.HDR10Plus.x265-hallowed",
            "exact": M_BR1 + 30 + M_DV + M_HDR10,
            "has": ["Dolby Vision", "HDR10+", "10-bit Depth"],
            "not": ["HDR", "2160p SDR Bluray", "Dolby Vision (Without Fallback)"],
        },
        {
            "name": "WEB DV without HDR is Dolby Vision without fallback",
            "title": "Movie.2024.2160p.WEB-DL.DV.x265-FLUX",
            "exact": M_STREAM + 30 + M_DV + M_DV_BARE,
            "passes": False,
            "has": ["2160p Compact Streaming WEB-DL", "Dolby Vision", "Dolby Vision (Without Fallback)"],
            "not": ["HDR", "2160p SDR Bluray", "2160p Compact Bluray Tier 1"],
        },
        {
            "name": "WEB DV with HDR has a fallback",
            "title": "Movie.2024.2160p.WEB-DL.DV.HDR.x265-FLUX",
            "exact": 28800 + 30 + 1000 + 500,
            "has": ["Dolby Vision", "HDR"],
            "not": ["Dolby Vision (Without Fallback)", "2160p SDR Bluray"],
        },
        {
            "name": "WEB DV with HDR10Plus has a fallback",
            "title": "Movie.2024.2160p.WEB-DL.DV.HDR10Plus.x265-FLUX",
            "exact": M_STREAM + 30 + M_DV + M_HDR10,
            "has": ["HDR10+", "Dolby Vision"],
            "not": ["Dolby Vision (Without Fallback)", "HDR", "2160p SDR Bluray"],
        },
        {
            "name": "WEB DV with HLG has a fallback",
            "title": "Movie.2024.2160p.WEB-DL.DV.HLG.x265-FLUX",
            "exact": 28800 + 30 + 1000 + 500,
            "has": ["HDR", "Dolby Vision"],
            "not": ["Dolby Vision (Without Fallback)"],
        },
        {
            "name": "Hulu DV stays out of without-fallback (regex treats Hulu as fallback)",
            "title": "Movie.2024.2160p.DV.HULU.WEB-DL.x265-FLUX",
            "has": ["Dolby Vision", "HULU", "2160p Compact Streaming WEB-DL"],
            "not": ["Dolby Vision (Without Fallback)", "2160p SDR Bluray"],
        },
        {
            "name": "German AC3.LD WEB is not CAM and is not circle WEB",
            "title": "Mutiny.2026.German.AC3.LD.DL.2160p.WEB.HDR.x265-GHOST",
            "exact": 30 + M_DD + 500 - 750,
            "has": ["Foreign Dub", "HDR", "Dolby Digital", "10-bit Depth"],
            "not": ["CAM", "2160p Compact WEB Tier 2", "2160p Compact Bluray Tier 2", "2160p SDR Bluray", "HDR10+"],
        },
        {
            "name": "German AC3.MD Blu-ray is not CAM; disc Ghost stays circle",
            "title": "Mutiny.2026.German.AC3.MD.DL.2160p.BluRay.HDR.x265-GHOST",
            "exact": M_BR2 + 30 + M_DD + 500 - 750,
            "has": ["2160p Compact Bluray Tier 2", "Foreign Dub", "HDR"],
            "not": ["CAM", "2160p Compact WEB Tier 2", "2160p SDR Bluray"],
        },
        {
            "name": "German.DL scene WEB is not circle WEB",
            "title": "Movie.2024.German.DL.2160p.WEB.x265-GHOST",
            "exact": -750,
            "has": ["Foreign Dub"],
            "not": ["CAM", "2160p Compact WEB Tier 2", "2160p Compact Bluray Tier 2"],
        },
        {
            "name": "French.DL scene WEB is not circle WEB",
            "title": "Movie.2024.FRENCH.DL.2160p.WEB.H.265-GHOST",
            "exact": -750,
            "has": ["Foreign Dub"],
            "not": ["CAM", "2160p Compact WEB Tier 2"],
        },
        {
            "name": "1080p German scene WEB is not circle",
            "title": "Movie.2024.German.DL.1080p.WEB.x265-GHOST",
            "exact": -750,
            "has": ["Foreign Dub"],
            "not": ["1080p Compact HEVC Tier 2", "CAM"],
        },
        {
            "name": "WEBRip before the German tag is still not circle WEB",
            "title": "Movie.2024.2160p.WEBRip.German.AC3.LD.DL.x265-GHOST",
            "exact": M_DD - 750,
            "has": ["Foreign Dub", "Dolby Digital"],
            "not": ["2160p Compact WEB Tier 2", "CAM", "2160p SDR Bluray"],
        },
        {
            "name": "Glued AC3LD scene WEB is not circle and not CAM",
            "title": "Movie.2024.German.AC3LD.2160p.WEB.x265-GHOST",
            "exact": -750,
            "has": ["Foreign Dub"],
            "not": ["2160p Compact WEB Tier 2", "CAM"],
        },
        {
            "name": "1080p German scene Blu-ray still matches disc circle",
            "title": "Movie.2024.German.DL.1080p.BluRay.HDR.x265-GHOST",
            "exact": 6400 + 30 + 500 - 750,
            "has": ["1080p Compact HEVC Tier 2", "Foreign Dub", "HDR"],
            "not": ["CAM", "2160p Compact WEB Tier 2"],
        },
        {
            "name": "Compact Ghost WEB is still circle WEB",
            "title": "Movie.2024.2160p.WEB-DL.HDR.x265-Ghost",
            "exact": M_WEB2 + M_HDR,
            "tier": "2160p Compact WEB Tier 2",
            "has": ["2160p Compact WEB Tier 2", "HDR"],
            "not": ["Foreign Dub", "CAM", "2160p Compact Bluray Tier 2"],
        },
        {
            "name": "Compact Ghost disc is still circle disc",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-Ghost",
            "exact": M_BR2 + M_HDR,
            "tier": "2160p Compact Bluray Tier 2",
            "not": ["Foreign Dub", "CAM", "2160p Compact WEB Tier 2"],
        },
        {
            "name": "Ghost QxR parenthetical is circle via QxR",
            "title": "Movie (2024) (2160p BluRay x265 HDR - Ghost QxR)",
            "exact": M_BR2 + M_HDR,
            "tier": "2160p Compact Bluray Tier 2",
        },
        {
            "name": "German in the movie title is not a scene dub",
            "title": "The.German.Doctor.2013.2160p.WEB.x265-Ghost",
            "exact": M_WEB2,
            "tier": "2160p Compact WEB Tier 2",
            "not": ["Foreign Dub", "CAM"],
        },
        {
            "name": "The French Dispatch is not a French dub",
            "title": "The.French.Dispatch.2021.2160p.BluRay.HDR.x265-hallowed",
            "exact": M_BR1 + M_HDR,
            "tier": "2160p Compact Bluray Tier 1",
            "not": ["Foreign Dub"],
        },
        {
            "name": "German dubbed elite disc keeps the dub penalty and the tier",
            "title": "Movie.2024.GERMAN.DUBBED.DL.2160p.BluRay.HDR.x265-hallowed",
            "exact": M_BR1 + M_HDR - 750,
            "has": ["2160p Compact Bluray Tier 1", "Foreign Dub"],
            "not": ["CAM"],
        },
        {
            "name": "WEB-DL alone is not a foreign dub",
            "title": "Movie.2024.2160p.WEB-DL.HDR.x265-FLUX",
            "exact": 28800 + M_HDR,
            "has": ["2160p Compact Streaming WEB-DL"],
            "not": ["Foreign Dub", "CAM"],
        },
        {
            "name": "Real CAM still matches",
            "title": "Movie.2024.2160p.CAM.x265-SAMPLE",
            "has": ["CAM"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "HDCAM still matches",
            "title": "Movie.2024.2160p.HDCAM.x264-SAMPLE",
            "has": ["CAM", "x264 (2160p)"],
        },
        {
            "name": "HDTS still matches",
            "title": "Movie.2024.2160p.HDTS.x264-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "HDTC still matches",
            "title": "Movie.2024.2160p.HDTC.x264-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "SCREENER still matches",
            "title": "Movie.2024.2160p.WEB-DL.SCREENER.x265-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "TELESYNC still matches",
            "title": "Movie.2024.TELESYNC.2160p.x264-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "TELECINE still matches",
            "title": "Movie.2024.TELECINE.2160p.x264-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "DVDScr still matches",
            "title": "Movie.2024.2160p.DVDScr.x264-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "LINE.DUBBED still matches CAM",
            "title": "Movie.2024.2160p.LINE.DUBBED.x264-SAMPLE",
            "has": ["CAM"],
        },
        {
            "name": "Bare LD after the year is not CAM",
            "title": "Movie.2024.LD.2160p.BluRay.HDR.x265-hallowed",
            "has": ["2160p Compact Bluray Tier 1", "HDR"],
            "not": ["CAM"],
        },
        {
            "name": "Bare MD after the year is not CAM",
            "title": "Movie.2024.MD.2160p.BluRay.HDR.x265-hallowed",
            "not": ["CAM"],
        },
        {
            "name": "A normal elite disc is not CAM",
            "title": "Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-hallowed",
            "exact": M_BR1 + M_HDR + M_DDP,
            "not": ["CAM", "2160p SDR Bluray"],
        },
        {
            "name": "TrueHD still rejects",
            "title": "Movie.2024.2160p.BluRay.HDR.TrueHD.Atmos.x265-hallowed",
            "exact": M_BR1 + 30 + 500 + M_ATMOS - 100000,
            "has": ["TrueHD", "Atmos"],
            "not": ["Dolby Digital +", "Dolby Digital"],
        },
        {
            "name": "TrueHD plus DD+ still rejects on TrueHD",
            "title": "Movie.2024.2160p.BluRay.HDR.TrueHD.Atmos.DDP.5.1.x265-hallowed",
            "exact": M_BR1 + 30 + 500 + M_ATMOS - 100000,
            "has": ["TrueHD", "Atmos"],
            "not": ["Dolby Digital +", "Dolby Digital"],
        },
        {
            "name": "DTS-HD MA still rejects",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.MA.7.1.x265-BHDStudio",
            "exact": M_BR1 + 30 + 500 - 100000,
            "has": ["DTS-HD MA"],
            "not": ["DTS", "DTS-HD HRA", "DTS-X", "Dolby Digital +"],
        },
        {
            "name": "DTS-HD MA plus DD+ still rejects on DTS-HD MA",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.MA.7.1.DDP.5.1.x265-BHDStudio",
            "exact": M_BR1 + 30 + 500 - 100000,
            "has": ["DTS-HD MA"],
            "not": ["Dolby Digital +", "Dolby Digital", "DTS"],
        },
        {
            "name": "DTS-X plus DD+ still rejects on DTS-X",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-X.7.1.DDP.5.1.x265-hallowed",
            "has": ["DTS-X"],
            "not": ["Dolby Digital +", "DTS", "DTS-HD MA"],
        },
        {
            "name": "DTS-HD HRA plus DD+ still rejects on HRA",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.HRA.DDP.5.1.x265-hallowed",
            "has": ["DTS-HD HRA"],
            "not": ["Dolby Digital +", "DTS-HD MA", "DTS"],
        },
        {
            "name": "DTSHDMA still matches DTS-HD MA",
            "title": "Movie.2024.2160p.BluRay.HDR.DTSHDMA.7.1.x265-hallowed",
            "has": ["DTS-HD MA"],
            "not": ["DTS"],
        },
        {
            "name": "DTS-HD HRA matches HRA, not MA",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.HRA.x265-hallowed",
            "exact": M_BR1 + 30 + 500 - 100000,
            "has": ["DTS-HD HRA"],
            "not": ["DTS-HD MA", "DTS"],
        },
        {
            "name": "DTS-X matches",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-X.7.1.x265-hallowed",
            "has": ["DTS-X"],
            "not": ["DTS-HD MA", "DTS", "Dolby Digital +"],
        },
        {
            "name": "DTSX matches DTS-X",
            "title": "Movie.2024.2160p.BluRay.HDR.DTSX.7.1.x265-hallowed",
            "has": ["DTS-X"],
            "not": ["DTS"],
        },
        {
            "name": "DTS-HD MA plus DTS-X keeps DTS-X",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS-HD.MA.7.1.DTS-X.x265-hallowed",
            "has": ["DTS-X"],
            "not": ["DTS-HD MA", "DTS"],
        },
        {
            "name": "Lossy DTS is DTS, not an HD-audio reject",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS.5.1.x265-hallowed",
            "exact": M_BR1 + 30 + 500 + M_DTS,
            "has": ["DTS"],
            "not": ["DTS-HD MA", "DTS-HD HRA", "DTS-X", "TrueHD"],
        },
        {
            "name": "DTS plus DD+ keeps DTS",
            "title": "Movie.2024.2160p.BluRay.HDR.DTS.5.1.DDP.5.1.x265-hallowed",
            "exact": M_BR1 + 30 + 500 + M_DTS,
            "has": ["DTS"],
            "not": ["Dolby Digital +", "Dolby Digital"],
        },
        {
            "name": "DDP is Dolby Digital Plus",
            "title": "Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-hallowed",
            "exact": M_BR1 + M_HDR + M_DDP,
            "has": ["Dolby Digital +"],
            "not": ["Dolby Digital"],
        },
        {
            "name": "DD+ symbol is Dolby Digital Plus",
            "title": "Movie.2024.2160p.BluRay.HDR.DD+.5.1.x265-hallowed",
            "has": ["Dolby Digital +"],
            "not": ["Dolby Digital"],
        },
        {
            "name": "EAC3 is Dolby Digital Plus",
            "title": "Movie.2024.2160p.BluRay.HDR.EAC3.5.1.x265-hallowed",
            "has": ["Dolby Digital +"],
            "not": ["Dolby Digital", "Banned Groups"],
        },
        {
            "name": "E-AC-3 is Dolby Digital Plus and not a banned group",
            "title": "Movie.2024.2160p.BluRay.HDR.E-AC-3.5.1.x265-hallowed",
            "exact": M_BR1 + M_HDR + M_DDP,
            "has": ["Dolby Digital +"],
            "not": ["Dolby Digital", "Banned Groups"],
        },
        {
            "name": "EAC-3 is Dolby Digital Plus",
            "title": "Movie.2024.2160p.BluRay.HDR.EAC-3.5.1.x265-hallowed",
            "exact": M_BR1 + M_HDR + M_DDP,
            "has": ["Dolby Digital +"],
            "not": ["Dolby Digital", "Banned Groups"],
        },
        {
            "name": "DD 5.1 is Dolby Digital, not Plus",
            "title": "Movie.2024.2160p.BluRay.HDR.DD.5.1.x265-hallowed",
            "exact": M_BR1 + 30 + 500 + M_DD,
            "has": ["Dolby Digital"],
            "not": ["Dolby Digital +"],
        },
        {
            "name": "AC3 is Dolby Digital",
            "title": "Movie.2024.2160p.BluRay.HDR.AC3.5.1.x265-hallowed",
            "has": ["Dolby Digital"],
            "not": ["Dolby Digital +", "CAM"],
        },
        {
            "name": "AAC alone matches AAC",
            "title": "Movie.2024.2160p.BluRay.HDR.AAC.2.0.x265-hallowed",
            "exact": M_BR1 + 30 + 500 + M_AAC,
            "has": ["AAC"],
            "not": ["Dolby Digital", "Dolby Digital +"],
        },
        {
            "name": "AAC plus DD+ keeps DD+",
            "title": "Movie.2024.2160p.BluRay.HDR.AAC2.0.DDP5.1.x265-hallowed",
            "exact": M_BR1 + M_HDR + M_DDP,
            "has": ["Dolby Digital +"],
            "not": ["AAC", "Dolby Digital"],
        },
        {
            "name": "FLAC matches",
            "title": "Movie.2024.2160p.BluRay.HDR.FLAC.2.0.x265-hallowed",
            "has": ["FLAC"],
            "not": ["Dolby Digital", "AAC"],
        },
        {
            "name": "FLAC plus DD+ keeps DD+",
            "title": "Movie.2024.2160p.BluRay.HDR.FLAC.2.0.DDP5.1.x265-hallowed",
            "has": ["Dolby Digital +"],
            "not": ["FLAC"],
        },
        {
            "name": "Atmos plus DD+ scores both",
            "title": "Movie.2024.2160p.BluRay.HDR.Atmos.DDP5.1.x265-hallowed",
            "exact": M_BR1 + M_HDR + M_DDP + M_ATMOS,
            "has": ["Atmos", "Dolby Digital +"],
        },
        {
            "name": "WEB DTS-HD MA still rejects and is not Movies Anywhere",
            "title": "Movie.2024.2160p.WEB-DL.HDR.DTS-HD.MA.5.1.x265-HONE",
            "has": ["DTS-HD MA", "2160p Compact WEB Tier 1"],
            "not": ["MA", "Dolby Digital +"],
        },
        {
            "name": "Movies Anywhere stays +15",
            "title": "Movie.2024.2160p.MA.WEB-DL.HDR.x265-HONE",
            "exact": M_WEB1 + M_HDR + 15,
            "has": ["MA"],
            "not": ["DTS-HD MA"],
        },
        {
            "name": "HMAX scores the same +5 storefront tie-break as MAX",
            "title": "Movie.2024.2160p.HMAX.WEB-DL.HDR.H.265-FLUX",
            "exact": M_STREAM + M_HDR + M_ATVP,
            "has": ["HMAX", "2160p Compact Streaming WEB-DL"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "MAX.WEB-DL scores MAX +5",
            "title": "Movie.2024.2160p.MAX.WEB-DL.HDR.H.265-FLUX",
            "exact": M_STREAM + M_HDR + M_ATVP,
            "has": ["MAX"],
        },
        {
            "name": "UHD WEB-DL is WEB, not Blu-ray",
            "title": "Movie.2024.2160p.UHD.WEB-DL.HDR.x265-HONE",
            "exact": M_WEB1 + M_HDR,
            "tier": "2160p Compact WEB Tier 1",
            "not": ["2160p Compact Bluray Tier 1", "2160p SDR Bluray"],
        },
        {
            "name": "Scene 2160p.WEB. is WEB-DL",
            "title": "Movie.2024.2160p.WEB.HDR.x265-HONE",
            "exact": M_WEB1 + M_HDR,
            "tier": "2160p Compact WEB Tier 1",
        },
        {
            "name": "WEBRip PSA is WEB tier 3, not a disc tier",
            "title": "Movie.2024.2160p.WEBRip.HDR.x265-PSA",
            "exact": M_WEB3 + M_HDR,
            "tier": "2160p Compact WEB Tier 3",
        },
        {
            "name": "FLUX on a Blu-ray is not a streaming or disc tier",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-FLUX",
            "exact": M_HDR,
            "not": list(tier_names),
        },
        {
            "name": "NTb on a Blu-ray is not untouched WEB",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-NTb",
            "exact": M_HDR,
            "not": ["2160p WEB-DL HEVC", "2160p Compact Bluray Tier 1"],
        },
        {
            "name": "HEVC word encode is not a full disc",
            "title": "Movie.2024.2160p.BluRay.HDR.HEVC-hallowed",
            "exact": M_BR1 + M_HDR,
            "has": ["2160p Compact Bluray Tier 1", "HDR"],
            "not": ["Full Disc", "x264 (2160p)", "2160p SDR Bluray"],
        },
        {
            "name": "HEVC word SDR disc is SDR and not a full disc",
            "title": "Movie.2024.2160p.BluRay.HEVC-hallowed",
            "exact": M_BR1 - 100000,
            "has": ["2160p SDR Bluray"],
            "not": ["Full Disc", "HDR"],
        },
        {
            "name": "Complete UHD Blu-ray is still a full disc",
            "title": "Movie.2024.COMPLETE.UHD.BLURAY-TERRA",
            "has": ["Full Disc", "2160p SDR Bluray"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "Remux in the name matches Remux and not a compact tier",
            "title": "Movie.2024.2160p.BluRay.REMUX.HDR.HEVC-HONE",
            "has": ["Remux", "HDR"],
            "not": ["2160p Compact Bluray Tier 1", "Full Disc", "2160p SDR Bluray"],
        },
        {
            "name": "x264 2160p matches and an x265 disc does not",
            "title": "Movie.2024.2160p.BluRay.x264-HONE",
            "has": ["x264 (2160p)", "2160p SDR Bluray"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "x265 is not x264",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-HONE",
            "not": ["x264 (2160p)", "AV1", "Full Disc"],
        },
        {
            "name": "AVC word is x264 and not a full disc",
            "title": "Movie.2024.2160p.BluRay.AVC-HONE",
            "has": ["x264 (2160p)"],
            "not": ["Full Disc", "2160p Compact Bluray Tier 1"],
        },
        {
            "name": "AV1 is rejected and blocks the compact tier",
            "title": "Movie.2024.2160p.BluRay.HDR.x265.AV1-hallowed",
            "has": ["AV1"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "3D matches",
            "title": "Movie.2024.2160p.BluRay.3D.HDR.x265-hallowed",
            "has": ["3D", "2160p Compact Bluray Tier 1"],
        },
        {
            "name": "A flat disc is not 3D",
            "title": "Movie.2024.2160p.BluRay.HDR.DDP5.1.Atmos.x265-hallowed",
            "not": ["3D", "Upscale", "Extras", "CAM", "Hardcoded Subtitles"],
        },
        {
            "name": "Hardcoded HC matches",
            "title": "Movie.2024.2160p.BluRay.HDR.HC.x265-hallowed",
            "has": ["Hardcoded Subtitles"],
        },
        {
            "name": "HARDSUB matches",
            "title": "Movie.2024.2160p.BluRay.HDR.HARDSUB.x265-hallowed",
            "has": ["Hardcoded Subtitles"],
        },
        {
            "name": "Audio Description matches",
            "title": "Movie.2024.2160p.BluRay.HDR.Audio.Description.x265-hallowed",
            "has": ["Audio Description"],
        },
        {
            "name": "DVS matches Audio Description",
            "title": "Movie.2024.2160p.BluRay.HDR.DVS.x265-hallowed",
            "has": ["Audio Description"],
        },
        {
            "name": "Ad Astra is not audio description",
            "title": "Ad.Astra.2019.2160p.BluRay.HDR.DDP5.1.x265-hallowed",
            "not": ["Audio Description", "Banned Groups"],
        },
        {
            "name": "AI upscale matches",
            "title": "Movie.2024.2160p.BluRay.HDR.AI.Upscale.x265-SAMPLE",
            "has": ["Upscale"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "A normal disc is not an upscale",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-hallowed",
            "not": ["Upscale", "Extras", "3D", "Banned Groups"],
        },
        {
            "name": "Extras match",
            "title": "Movie.2024.2160p.BluRay.HDR.Extras.x265-hallowed",
            "has": ["Extras"],
        },
        {
            "name": "IMAX matches and NON-IMAX does not",
            "title": "Movie.2024.2160p.BluRay.IMAX.HDR.x265-hallowed",
            "has": ["IMAX"],
            "not": ["IMAX Enhanced"],
        },
        {
            "name": "NON-IMAX does not match IMAX",
            "title": "Movie.2024.2160p.BluRay.NON-IMAX.HDR.x265-hallowed",
            "not": ["IMAX", "IMAX Enhanced"],
        },
        {
            "name": "Disney IMAX Enhanced matches that format only",
            "title": "Movie.2024.2160p.IMAX.Enhanced.DSNP.WEB-DL.HDR.H.265-FLUX",
            "has": ["IMAX Enhanced", "DSNP", "2160p Compact Streaming WEB-DL"],
            "not": ["IMAX"],
        },
        {
            "name": "edge2020HD is not edge2020",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-edge2020HD",
            "exact": M_HDR,
            "not": list(tier_names),
        },
        {
            "name": "PSARips stays small, not PSA plus another tier",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-PSARips",
            "exact": M_BR3 + M_HDR,
            "tier": "2160p Compact Bluray Tier 3",
        },
        {
            "name": "ReELiTE stays small and is not also ELiTE twice",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-ReELiTE",
            "exact": M_BR3 + M_HDR,
            "tier": "2160p Compact Bluray Tier 3",
        },
        {
            "name": "Ghostbusters does not match the Ghost encoder",
            "title": "Ghostbusters.2016.2160p.BluRay.HDR.x265-HONE",
            "exact": M_BR1 + M_HDR,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "name": "Silence of the Lambs does not match the Silence encoder",
            "title": "The.Silence.of.the.Lambs.1991.2160p.BluRay.HDR.x265-hallowed",
            "exact": M_BR1 + M_HDR,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "name": "Ben-Hur is not the banned group BEN",
            "title": "Ben.Hur.2016.2160p.BluRay.HDR.x265-hallowed",
            "exact": M_BR1 + M_HDR,
            "not": ["Banned Groups"],
        },
        {
            "name": "Mama the movie is not the banned group MAMA",
            "title": "Mama.2013.2160p.BluRay.HDR.x265-hallowed",
            "exact": M_BR1 + M_HDR,
            "not": ["Banned Groups"],
        },
        {
            "name": "Release group MAMA is banned",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-MAMA",
            "has": ["Banned Groups"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "Release group BTM is banned",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-BTM",
            "has": ["Banned Groups"],
        },
        {
            "name": "Release group Saon is banned",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-Saon",
            "has": ["Banned Groups"],
            "not": ["2160p Compact Bluray Tier 1"],
        },
        {
            "name": "Opus 5.1 matches",
            "title": "Movie.2024.2160p.BluRay.HDR.Opus.5.1.x265-hallowed",
            "has": ["Opus 5.1 / 7.1"],
        },
        {
            "name": "Hybrid matches",
            "title": "Movie.2024.2160p.Hybrid.BluRay.HDR.x265-hallowed",
            "has": ["Hybrid", "2160p Compact Bluray Tier 1"],
        },
        {
            "name": "Proper matches Repack",
            "title": "Movie.2024.PROPER.2160p.BluRay.HDR.x265-hallowed",
            "has": ["Repack1"],
            "not": ["Repack2", "Repack3"],
        },
        {
            "name": "8-bit token matches",
            "title": "Movie.2024.2160p.BluRay.8bit.SDR.x265-dkore",
            "has": ["8-bit Depth", "2160p SDR Bluray"],
        },
        {
            "name": "Compact disc still beats compact streaming WEB",
            "title": "Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-hallowed",
            "above": "Movie.2024.2160p.ATVP.WEB-DL.DV.HDR.DDP5.1.H.265-FLUX",
        },
        {
            "name": "Compact streaming WEB still beats PSA",
            "title": "Movie.2024.2160p.ATVP.WEB-DL.DV.HDR.DDP5.1.H.265-FLUX",
            "above": "Movie.2024.2160p.BluRay.HDR.x265-PSA",
        },
        {
            "name": "PSA still beats untouched BYNDR",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-PSA",
            "above": "Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-BYNDR",
        },
        {
            "name": "HMAX WEB does not beat an elite disc",
            "title": "Movie.2024.2160p.BluRay.HDR.x265-hallowed",
            "above": "Movie.2024.2160p.HMAX.WEB-DL.HDR.H.265-FLUX",
        },
    ]

    tv_cases = [
        {
            "name": "TV HONE WEB score is unchanged",
            "title": "Show.S01E01.2160p.WEB-DL.H265-HONE",
            "profile": tv,
            "exact": 8100,
            "tier": "2160p Compact WEB Tier 1",
        },
        {
            "name": "TV HONE disc score is unchanged",
            "title": "Show.S01E01.2160p.BluRay.x265-HONE",
            "profile": tv,
            "exact": 5300,
            "tier": "2160p Compact Bluray Tier 1",
        },
        {
            "name": "TV Ghost WEB is still circle WEB",
            "title": "Show.S01E01.2160p.WEB-DL.H265-Ghost",
            "profile": tv,
            "exact": 7400,
            "tier": "2160p Compact WEB Tier 2",
        },
        {
            "name": "TV German scene GHOST WEB is not circle",
            "title": "Show.S01E01.German.AC3.LD.DL.2160p.WEB.x265-GHOST",
            "profile": tv,
            "not": ["2160p Compact WEB Tier 2", "CAM"],
            "has": ["Foreign Dub"],
        },
        {
            "name": "TV TrueHD plus DD+ still allows the file and scores TrueHD",
            "title": "Show.S01E01.2160p.BluRay.TrueHD.DDP5.1.x265-HONE",
            "profile": tv,
            "exact": 5300 + 15,
            "has": ["TrueHD", "2160p Compact Bluray Tier 1"],
            "not": ["Dolby Digital +"],
        },
    ]

    def check(case):
        nonlocal passed, failed
        profile = case.get("profile", movies)
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, case["title"], profile)
        names = [name for name, _score in matched]
        name_set = set(names)
        ok = True
        if "exact" in case and score != case["exact"]:
            ok = False
        for needed in case.get("has", []):
            if needed not in name_set:
                ok = False
        for banned in case.get("not", []):
            if banned in name_set:
                ok = False
        if "tier" in case:
            hits = [name for name in names if name in tier_names]
            if hits != [case["tier"]]:
                ok = False
        if "above" in case:
            other, _mn, _up, _ok, _matched = evaluate_release(conn, case["above"], profile)
            if not score > other:
                ok = False
        if "passes" in case and passed_cutoff != case["passes"]:
            ok = False
        if ok:
            passed += 1
            print(f"[PASS] {case['name']}")
        else:
            failed += 1
            print(f"[FAIL] {case['name']}")
            print(f"  Title: {case['title']}")
            print(f"  Score: {score} pass {passed_cutoff}")
            if "exact" in case:
                print(f"  Expected score: {case['exact']}")
            if "tier" in case:
                print(f"  Tier: {[name for name in names if name in tier_names]} expected {case['tier']}")
            missing = [name for name in case.get("has", []) if name not in name_set]
            extra = [name for name in case.get("not", []) if name in name_set]
            if missing:
                print(f"  Missing: {missing}")
            if extra:
                print(f"  Unexpected: {extra}")
            for cf, cf_score in matched:
                print(f"    - {cf}: {cf_score:+}")
        return ok

    cases.extend(_compact_parity_cases())

    for case in cases:
        check(case)
    for case in tv_cases:
        check(case)

    tv_truehd = conn.execute(
        "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = 'TrueHD'",
        (tv,),
    ).fetchone()[0]
    movie_ma = conn.execute(
        "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = 'MA'",
        (movies,),
    ).fetchone()[0]
    guards = (
        ("TV TrueHD score is still +15", tv_truehd == 15),
        ("Movies Anywhere score is still +15", movie_ma == 15),
    )
    for label, ok in guards:
        if ok:
            passed += 1
            print(f"[PASS] {label}")
        else:
            failed += 1
            print(f"[FAIL] {label}")
    print(f"Identification stress: {passed} passed, {failed} failed")
    return passed, failed


def run_dumpstarr_tiebreak_order(conn):
    """Dumpstarr-relative extras inside one Movies 2160p HEVC Compact class.

    HDR and HDR10+ are mutually exclusive here, so HDR10+ carries Dumpstarr's
    combined 500+100. Audio order is DD+ Atmos, DD Atmos, DD+, DD, Atmos, AAC,
    then lossy DTS with no bonus. Storefronts keep that same order under a
    +15 ceiling. HD audio Dumpstarr denies misses cutoff. LPCM, FLAC, and
    lossy DTS do not, because Dumpstarr does not deny them. A tiered DV WEB
    with no HDR token misses cutoff. Class order is unchanged.
    """
    movies = "Movies 2160p HEVC Compact"
    tv = "TV 2160p HEVC Compact"
    passed = 0
    failed = 0

    def score(title, profile=movies):
        return evaluate_release(conn, title, profile)

    def expect(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"[PASS] {name}")
        else:
            failed += 1
            print(f"[FAIL] {name} {detail}")

    base_title = "Movie.2024.2160p.BluRay.HDR.x265-hallowed"
    base = score(base_title)[0]

    def disc(extra):
        return score(f"Movie.2024.2160p.BluRay.HDR.{extra}.x265-hallowed")[0]

    hdr10 = score("Movie.2024.2160p.BluRay.HDR10+.x265-hallowed")[0]
    dv_hdr = score("Movie.2024.2160p.BluRay.DV.HDR.x265-hallowed")[0]
    dv_hdr10 = score("Movie.2024.2160p.BluRay.DV.HDR10+.x265-hallowed")[0]
    expect(
        "DV+HDR10+ beats DV+HDR beats HDR10+ beats HDR",
        dv_hdr10 > dv_hdr > hdr10 > base,
        f"{dv_hdr10} {dv_hdr} {hdr10} {base}",
    )
    expect("HDR10+ leads plain HDR by 100", hdr10 - base == 100, f"delta {hdr10 - base}")
    expect("Dolby Vision adds 1000 on top of HDR", dv_hdr - base == M_DV, f"delta {dv_hdr - base}")

    ddp_atmos = disc("DDP5.1.Atmos")
    dd_atmos = disc("DD.5.1.Atmos")
    ddp = disc("DDP5.1")
    dd = disc("DD.5.1")
    atmos = disc("Atmos")
    aac = disc("AAC.2.0")
    dts = disc("DTS.5.1")
    expect(
        "DD+ Atmos > DD Atmos > DD+ > DD > Atmos > AAC > lossy DTS",
        ddp_atmos > dd_atmos > ddp > dd > atmos > aac > dts and dts == base,
        f"{ddp_atmos} {dd_atmos} {ddp} {dd} {atmos} {aac} {dts} base {base}",
    )
    expect("DD+ Atmos is +150", ddp_atmos - base == M_DDP + M_ATMOS)
    expect("DD Atmos is +140", dd_atmos - base == M_DD + M_ATMOS)
    expect("DD+ is +125", ddp - base == M_DDP)
    expect("DD is +115", dd - base == M_DD)
    expect("Atmos is +25", atmos - base == M_ATMOS)
    expect("AAC is +10", aac - base == M_AAC)

    dts_ddp, _, _, dts_ddp_ok, dts_ddp_matched = score(
        "Movie.2024.2160p.BluRay.HDR.DTS.5.1.DDP.5.1.x265-hallowed"
    )
    dts_names = [name for name, _s in dts_ddp_matched]
    expect(
        "Lossy DTS beside DD+ scores DTS and not DD+",
        dts_ddp == dts and dts_ddp_ok and "DTS" in dts_names and "Dolby Digital +" not in dts_names,
        f"score {dts_ddp} names {dts_names}",
    )
    truehd, truehd_min, _, truehd_ok, truehd_matched = score(
        "Movie.2024.2160p.BluRay.HDR.TrueHD.Atmos.DDP5.1.x265-hallowed"
    )
    truehd_names = [name for name, _s in truehd_matched]
    expect(
        "TrueHD beside DD+ still misses cutoff",
        (not truehd_ok) and truehd < truehd_min and "TrueHD" in truehd_names and "Dolby Digital +" not in truehd_names,
        f"score {truehd}",
    )

    extended = disc("Extended")
    expect("Special Edition matches the DD+ weight", extended - base == M_SE and extended == ddp)

    def web(tag):
        if tag:
            title = f"Movie.2024.2160p.{tag}.WEB-DL.HDR.H.265-FLUX"
        else:
            title = "Movie.2024.2160p.WEB-DL.HDR.H.265-FLUX"
        return score(title)[0]

    plain = web("")
    ma = web("MA")
    dsnp = web("DSNP")
    itunes = web("iT")
    atvp = web("ATVP")
    hmax = web("HMAX")
    max_web = web("MAX")
    atv = web("ATV")
    amzn = web("AMZN")
    nf = web("NF")
    hulu = web("HULU")
    expect(
        "MA > DSNP = iTunes > ATVP = HMAX = MAX > ATV = AMZN = NF = HULU",
        ma > dsnp == itunes > atvp == hmax == max_web > atv == amzn == nf == hulu > plain,
        f"{ma} {dsnp} {itunes} {atvp} {hmax} {max_web} {atv} {amzn} {nf} {hulu} {plain}",
    )
    expect("MA storefront is +15", ma - plain == M_MA)
    expect("DSNP storefront is +10", dsnp - plain == M_DSNP)
    expect("ATVP storefront is +5", atvp - plain == M_ATVP)
    expect("AMZN storefront is +2", amzn - plain == M_SHOP)

    elite_ddp = score("Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-hallowed")[0]
    bhdstudio = score("Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-BHDStudio")[0]
    darq = score("Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-DarQ")[0]
    discod = score("Movie.2024.2160p.BluRay.HDR.DDP5.1.x265-DiscoD")[0]
    flux_ma = score("Movie.2024.2160p.MA.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-FLUX")[0]
    hone_ma = score("Movie.2024.2160p.MA.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-HONE")[0]
    psa = score("Movie.2024.2160p.BluRay.HDR.x265-PSA")[0]
    byndr = score("Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-BYNDR")[0]
    expect("hallowed DD+ HDR beats FLUX MA WEB", elite_ddp > flux_ma, f"{elite_ddp} vs {flux_ma}")
    expect("hallowed DD+ HDR beats HONE MA WEB", elite_ddp > hone_ma, f"{elite_ddp} vs {hone_ma}")
    expect("hallowed DD+ HDR beats PSA", elite_ddp > psa, f"{elite_ddp} vs {psa}")
    expect("BHDStudio, DarQ, and DiscoD tie that hallowed disc", bhdstudio == darq == discod == elite_ddp)
    expect("PSA beats a stacked untouched WEB", psa > byndr, f"{psa} vs {byndr}")

    circle = score("Movie.2024.2160p.BluRay.DV.HDR10+.DDP5.1.Atmos.Extended.Hybrid.x265-QxR")[0]
    expect(
        "A stacked circle disc still loses to a plain elite HDR disc",
        circle < base,
        f"{circle} vs {base}",
    )

    for label, title in (
        ("TrueHD", "Movie.2024.2160p.BluRay.HDR.TrueHD.Atmos.x265-hallowed"),
        ("DTS-HD MA", "Movie.2024.2160p.BluRay.HDR.DTS-HD.MA.x265-hallowed"),
        ("DTS-HD HRA", "Movie.2024.2160p.BluRay.HDR.DTS-HD.HRA.x265-hallowed"),
        ("DTS-X", "Movie.2024.2160p.BluRay.HDR.DTS-X.x265-hallowed"),
    ):
        total, minimum, _until, ok, _matched = score(title)
        expect(f"{label} on an elite HDR disc misses cutoff", (not ok) and total < minimum, f"score {total}")

    for label, title in (
        ("LPCM", "Movie.2024.2160p.BluRay.HDR.LPCM.5.1.x265-hallowed"),
        ("PCM", "Movie.2024.2160p.BluRay.HDR.PCM.7.1.x265-hallowed"),
        ("FLAC", "Movie.2024.2160p.BluRay.HDR.FLAC.2.0.x265-hallowed"),
        ("lossy DTS", "Movie.2024.2160p.BluRay.HDR.DTS.5.1.x265-hallowed"),
    ):
        total, minimum, _until, ok, matched = score(title)
        names = [name for name, _s in matched]
        expect(
            f"{label} stays playable on an elite HDR disc",
            ok and total >= minimum and "TrueHD" not in names and "DTS-HD MA" not in names,
            f"score {total} names {names}",
        )

    for group in ("FLUX", "Kitsune", "CMRG"):
        total, minimum, _until, ok, matched = score(f"Movie.2024.2160p.WEB-DL.DV.x265-{group}")
        names = [name for name, _s in matched]
        expect(
            f"{group} DV WEB with no HDR token misses cutoff",
            (not ok) and total < minimum and "Dolby Vision (Without Fallback)" in names and "HDR" not in names,
            f"score {total} names {names}",
        )
    fallback, _mn, _until, fallback_ok, fallback_matched = score("Movie.2024.2160p.WEB-DL.DV.HDR.x265-FLUX")
    fallback_names = [name for name, _s in fallback_matched]
    expect(
        "FLUX DV with an HDR token still clears cutoff",
        fallback_ok and "Dolby Vision (Without Fallback)" not in fallback_names,
        f"score {fallback}",
    )

    dub, _mn, _until, dub_ok, dub_matched = score("Movie.2024.German.AC3.LD.2160p.BluRay.HDR.x265-hallowed")
    dub_names = [name for name, _s in dub_matched]
    plain_dd = score("Movie.2024.2160p.BluRay.HDR.DD.5.1.x265-hallowed")[0]
    dub_dd = score("Movie.2024.German.AC3.5.1.DL.2160p.BluRay.HDR.x265-hallowed")[0]
    ddp_dub, _mn, _until, ddp_dub_ok, ddp_dub_matched = score(
        "Movie.2024.German.DDP5.1.DL.2160p.BluRay.HDR.x265-hallowed"
    )
    expect(
        "German AC3.LD is a dub and still clears cutoff",
        dub_ok and "Foreign Dub" in dub_names and "CAM" not in dub_names,
        f"score {dub} names {dub_names}",
    )
    expect(
        "German DDP5.1.DL is a dub and still clears cutoff",
        ddp_dub_ok and "Foreign Dub" in [name for name, _s in ddp_dub_matched] and "CAM" not in [name for name, _s in ddp_dub_matched],
        f"score {ddp_dub}",
    )
    expect("German dub penalty is -750, not a hard reject", plain_dd - dub_dd == 750, f"{plain_dd} - {dub_dd}")

    imf = score("Coyote.vs.Acme.2026.2160p.WEBRip.IMF.HDR.x265-PSA")[0]
    no_imf = score("Coyote.vs.Acme.2026.2160p.WEBRip.HDR.x265-PSA")[0]
    expect("IMF WEBRip is +75 and still loses to streaming WEB", imf - no_imf == M_IMF and imf < plain)

    gates = conn.execute(
        "SELECT minimum_custom_format_score, upgrade_until_score, upgrade_score_increment FROM quality_profiles WHERE name = ?",
        (movies,),
    ).fetchone()
    expect("min, cutoff, and upgrade increment are unchanged", gates == (3000, 41600, 1), f"{gates}")
    uhd_pref = conn.execute(
        """
        SELECT COUNT(*) FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-2160p', 'WEBDL-2160p', 'WEBRip-2160p', 'HDTV-2160p')
          AND min_size = 0 AND preferred_size = 130 AND max_size = 0
        """
    ).fetchone()[0]
    hd_pref = conn.execute(
        """
        SELECT COUNT(*) FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-1080p', 'WEBDL-1080p', 'WEBRip-1080p', 'HDTV-1080p')
          AND min_size = 0 AND preferred_size = 18 AND max_size = 0
        """
    ).fetchone()[0]
    remux_pref = conn.execute(
        """
        SELECT COUNT(*) FROM radarr_quality_definitions
        WHERE quality_name IN ('Remux-2160p', 'Remux-1080p')
          AND min_size = 0 AND preferred_size = 1999 AND max_size = 0
        """
    ).fetchone()[0]
    expect("4K encode size is min 0, preferred 130, max 0", uhd_pref == 4, f"rows {uhd_pref}")
    expect("1080p encode size is min 0, preferred 18, max 0", hd_pref == 4, f"rows {hd_pref}")
    expect("Remux size stays min 0, preferred 1999, max 0", remux_pref == 2, f"rows {remux_pref}")
    untouched = conn.execute(
        "SELECT COUNT(*) FROM radarr_quality_definitions WHERE quality_name = 'Bluray-720p' AND min_size = 0 AND preferred_size = 1990 AND max_size = 0"
    ).fetchone()[0]
    expect("720p Bluray stays min 0, preferred 1990, max 0", untouched == 1, f"rows {untouched}")
    streaming = conn.execute(
        "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = '1080p Compact Streaming WEB-DL'",
        (movies,),
    ).fetchone()[0]
    expect("1080p streaming score stays 5200", streaming == 5200, f"score {streaming}")

    positive = conn.execute(
        "SELECT COALESCE(SUM(score), 0) FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND score > 0 AND score < 3000",
        (movies,),
    ).fetchone()[0]
    expect("Every positive extra together stays under the 3200 class gap", positive < 3200, f"sum {positive}")

    def tv_score(fmt):
        return conn.execute(
            "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = ?",
            (tv, fmt),
        ).fetchone()[0]

    expect("TV TrueHD stays +15", tv_score("TrueHD") == 15)
    expect("TV HDR10+ stays +50", tv_score("HDR10+") == 50)
    expect("TV Atmos stays +80", tv_score("Atmos") == 80)
    expect("TV Dolby Digital stays +20", tv_score("Dolby Digital") == 20)
    expect("TV IMAX stays +40", tv_score("IMAX") == 40)
    expect("TV DV without fallback stays -10000", tv_score("Dolby Vision (Without Fallback)") == -10000)
    tv_truehd, _mn, _until, tv_ok, tv_matched = score("Show.S01E01.2160p.BluRay.HDR.TrueHD.x265-HONE", tv)
    expect(
        "TV TrueHD disc is still allowed",
        tv_ok and "TrueHD" in [name for name, _s in tv_matched],
        f"score {tv_truehd}",
    )

    print(f"Tie-break order: {passed} passed, {failed} failed")
    return passed, failed


def run_movie_fallback_ladder(conn, movies, tv):
    """Pickup order after the 4K class scores from op 972.

    Untouched 4K WEB-DL stays on the profile at 0, under min 3000, including
    when Dolby Vision and HDR are named. 4K streaming stays at 28800, above
    PSA at 25600, and keeps its 2160p resolution requirement. 4K Tier 4
    scores 0, so a micro misses the minimum and Radarr can grab 1080p
    instead. 1080p repeats the ladder under that: elite, circle,
    FLUX/Kitsune/CMRG, PSA, micro. The 1080p micro still clears 3000.
    TV scores are not part of this ladder.
    """
    print("\n=== MOVIE FALLBACK LADDER ===")
    passed = 0
    failed = 0

    def expect(name, ok, detail=""):
        nonlocal passed, failed
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
        if ok:
            passed += 1
        else:
            failed += 1

    def score(title, profile=movies):
        return evaluate_release(conn, title, profile)

    def tier_score(fmt, profile=movies):
        row = conn.execute(
            "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = ?",
            (profile, fmt),
        ).fetchone()
        return None if row is None else row[0]

    for fmt, expected in (
        ("2160p Compact Bluray Tier 1", M_BR1),
        ("2160p Compact Bluray Tier 2", M_BR2),
        ("2160p Compact WEB Tier 1", M_WEB1),
        ("2160p Compact Streaming WEB-DL", M_STREAM),
        ("2160p Compact WEB Tier 2", M_WEB2),
        ("2160p Compact Bluray Tier 3", M_BR3),
        ("2160p Compact Bluray Tier 4", M_BR4),
        ("2160p Compact WEB Tier 3", M_WEB3),
        ("2160p Compact WEB Tier 4", M_WEB4),
        ("2160p WEB-DL HEVC", M_WEBDL),
        ("1080p Compact HEVC Tier 1", M_HD1),
        ("1080p Compact HEVC Tier 2", M_HD2),
        ("1080p Compact Streaming WEB-DL", M_HD_STREAM),
        ("1080p Compact HEVC Tier 3", M_HD3),
        ("1080p Compact HEVC Tier 4", M_HD4),
    ):
        expect(f"{fmt} scores {expected}", tier_score(fmt) == expected, f"got {tier_score(fmt)}")

    streaming_res = conn.execute(
        "SELECT resolution FROM condition_resolutions WHERE custom_format_name = '2160p Compact Streaming WEB-DL'"
    ).fetchall()
    expect(
        "4K streaming format still requires 2160p",
        streaming_res == [("2160p",)],
        f"{streaming_res}",
    )
    hd_streaming_res = conn.execute(
        "SELECT resolution FROM condition_resolutions WHERE custom_format_name = '1080p Compact Streaming WEB-DL'"
    ).fetchall()
    expect(
        "1080p streaming format requires 1080p",
        hd_streaming_res == [("1080p",)],
        f"{hd_streaming_res}",
    )

    byndr = score("Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.H.265-BYNDR")
    ntb = score("The.Silence.of.the.Lambs.1991.2160p.WEB-DL.H265-NTb")
    xebec = score("Movie.2024.2160p.WEB-DL.HDR.H.265-XEBEC")
    hhweb = score("Movie.2024.2160p.WEB-DL.DV.HDR10+.H.265-HHWEB")
    for label, result in (("BYNDR", byndr), ("NTb", ntb), ("XEBEC", xebec), ("HHWEB", hhweb)):
        total, minimum, _until, ok, matched = result
        names = [name for name, _s in matched]
        expect(
            f"{label} untouched 4K WEB-DL scores below 3000",
            (not ok) and total < minimum and total < 3000 and "2160p WEB-DL HEVC" in names,
            f"score {total} names {names}",
        )

    elite_disc = score("Movie.2024.2160p.BluRay.HDR.x265-Ralphy")
    circle_disc = score("Movie.2024.2160p.BluRay.HDR.x265-QxR")
    psa = score("Movie.2024.2160p.BluRay.HDR.x265-PSA")
    micro = score("Movie.2024.2160p.WEB-DL.x265-iVy")
    expect(
        "4K PSA clears the minimum and beats a 4K micro that misses it",
        psa[3] and psa[0] >= 3000 and psa[0] > micro[0] and micro[0] < 3000 and not micro[3],
        f"PSA {psa[0]} micro {micro[0]} pass {micro[3]}",
    )
    streaming_plain = score("Movie.2024.2160p.WEB-DL.H265-FLUX")
    expect(
        "4K streaming stays above PSA",
        streaming_plain[0] == M_STREAM and streaming_plain[0] > psa[0],
        f"streaming {streaming_plain[0]} PSA {psa[0]}",
    )
    rarbg_4k = score("Movie.2024.2160p.BluRay.HDR.x265-RARBG")
    stacked_micro = score("Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.Atmos.10bit.x265-iVy")
    expect(
        "4K RARBG and iVy micros score below 3000",
        (not rarbg_4k[3]) and rarbg_4k[0] < 3000 and (not micro[3]) and micro[0] < 3000
        and "2160p Compact Bluray Tier 4" in [name for name, _s in rarbg_4k[4]]
        and "2160p Compact WEB Tier 4" in [name for name, _s in micro[4]],
        f"RARBG {rarbg_4k[0]} iVy {micro[0]}",
    )
    expect(
        "4K micro plus the feature stack still misses 3000",
        (not stacked_micro[3]) and stacked_micro[0] < 3000,
        f"stacked {stacked_micro[0]}",
    )

    for group in ("FLUX", "Kitsune", "CMRG"):
        plain = score(f"Movie.2024.2160p.WEB-DL.H265-{group}")
        tagged = score(f"Movie.2024.2160p.WEB-DL.DV.HDR.DDP5.1.H.265-{group}")
        names = [name for name, _s in plain[4]]
        expect(
            f"4K {group} stays in the streaming class",
            plain[3] and plain[0] == M_STREAM and names == ["2160p Compact Streaming WEB-DL"],
            f"score {plain[0]} names {names}",
        )
        expect(
            f"4K {group} beats PSA and loses to a compact Blu-ray encode",
            tagged[0] > psa[0] and tagged[0] < circle_disc[0] and tagged[0] < elite_disc[0],
            f"{group} {tagged[0]} PSA {psa[0]} circle {circle_disc[0]} elite {elite_disc[0]}",
        )

    ralphy = score("Movie.2024.1080p.BluRay.x265-Ralphy")
    hallowed = score("Movie.2024.1080p.BluRay.HEVC-hallowed")
    bhdstudio = score("Movie.2024.1080p.BluRay.x265-BHDStudio")
    circle_hd = score("Movie.2024.1080p.BluRay.x265-TAoE")
    flux_hd = score("Movie.2024.1080p.WEB-DL.H265-FLUX")
    kitsune_hd = score("Movie.2024.1080p.WEB-DL.H.265-Kitsune")
    cmrg_hd = score("Movie.2024.1080p.WEB-DL.x265-CMRG")
    psa_hd = score("Movie.2024.1080p.BluRay.x265-PSA")
    ivy_hd = score("Movie.2024.1080p.WEB-DL.x265-iVy")
    rarbg_hd = score("Movie.2024.1080p.BluRay.x265-RARBG")
    expect(
        "1080p elite encodes share one score",
        ralphy[0] == hallowed[0] == bhdstudio[0] == M_HD1 and ralphy[3],
        f"Ralphy {ralphy[0]} hallowed {hallowed[0]} BHDStudio {bhdstudio[0]}",
    )
    expect(
        "1080p elite is grabbed when the 4K micro misses the minimum",
        ralphy[3] and ralphy[0] == M_HD1 and ralphy[0] >= 3000 and not micro[3] and not rarbg_4k[3],
        f"1080p {ralphy[0]} iVy {micro[0]} RARBG {rarbg_4k[0]}",
    )
    expect(
        "1080p elite beats streaming, which beats PSA, which beats a micro",
        ralphy[0] > flux_hd[0] > psa_hd[0] > ivy_hd[0]
        and flux_hd[0] == kitsune_hd[0] == cmrg_hd[0] == M_HD_STREAM
        and psa_hd[0] == M_HD3
        and ivy_hd[0] == rarbg_hd[0] == M_HD4
        and circle_hd[0] == M_HD2
        and circle_hd[0] > flux_hd[0],
        f"elite {ralphy[0]} circle {circle_hd[0]} stream {flux_hd[0]} PSA {psa_hd[0]} micro {ivy_hd[0]}",
    )
    flux_hd_names = [name for name, _s in flux_hd[4]]
    expect(
        "1080p FLUX does not receive the 4K streaming score",
        flux_hd[0] != M_STREAM
        and flux_hd[0] == M_HD_STREAM
        and "2160p Compact Streaming WEB-DL" not in flux_hd_names
        and "1080p Compact Streaming WEB-DL" in flux_hd_names,
        f"score {flux_hd[0]} names {flux_hd_names}",
    )
    expect(
        "1080p micro still clears the minimum",
        ivy_hd[3] and rarbg_hd[3] and ivy_hd[0] >= 3000 and rarbg_hd[0] >= 3000,
        f"iVy {ivy_hd[0]} RARBG {rarbg_hd[0]}",
    )
    flux_dv = score("Movie.2024.1080p.WEB-DL.DV.HDR.H.265-FLUX")
    expect(
        "1080p streaming with Dolby Vision still loses to a plain elite encode",
        flux_dv[0] < ralphy[0] and flux_dv[0] < M_STREAM,
        f"FLUX {flux_dv[0]} Ralphy {ralphy[0]}",
    )

    expect("TV 4K bluray tier 4 stays 3200", tier_score("2160p Compact Bluray Tier 4", tv) == 3200)
    expect("TV 4K web tier 4 stays 6000", tier_score("2160p Compact WEB Tier 4", tv) == 6000)
    expect("TV untouched WEB-DL stays 2500", tier_score("2160p WEB-DL HEVC", tv) == 2500)
    expect("TV streaming WEB stays 5300", tier_score("2160p Compact Streaming WEB-DL", tv) == 5300)
    expect("TV 1080p tier 1 stays 1800", tier_score("1080p Compact HEVC Tier 1", tv) == 1800)
    expect("TV 1080p tier 4 stays 400", tier_score("1080p Compact HEVC Tier 4", tv) == 400)
    expect(
        "TV does not score the 1080p streaming format",
        tier_score("1080p Compact Streaming WEB-DL", tv) is None,
    )
    gates = conn.execute(
        "SELECT minimum_custom_format_score, upgrade_until_score FROM quality_profiles WHERE name = ?",
        (movies,),
    ).fetchone()
    expect("Movie minimum and cutoff stay 3000 / 41600", gates == (3000, 41600), f"{gates}")

    print(f"Fallback ladder: {passed} passed, {failed} failed")
    return passed, failed


def run_empty_assigned_format_guard(conn, movies, tv):
    """Empty assigned formats cannot sync.

    Op 974 counted Banned Groups (Efficient) and Banned Groups (Regular)
    among the hard rejects (18 at -100000 on movies, 19 at -10000 on TV).
    Op 968 had already removed their last condition, RARBG. An assigned
    format with zero conditions compiles to specifications: [] and Radarr
    rejects it. Unassigning them drops those counts by 2. The shared
    Banned Groups list and Banned Micro Encodes stay. Class scores do not
    move, and Micro OK groups are not put back on a ban list.
    """
    print("\n=== EMPTY ASSIGNED FORMATS ===")
    passed = 0
    failed = 0

    def expect(name, ok, detail=""):
        nonlocal passed, failed
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
        if ok:
            passed += 1
        else:
            failed += 1

    movie_rejects = (
        "3D", "AV1", "Audio Description", "Banned Groups", "Banned Groups (Efficient)",
        "Banned Groups (Regular)", "Banned Micro Encodes", "CAM", "Extras", "Full Disc",
        "Full Disc (Quality Match)", "Hardcoded Subtitles", "Remux", "Sing Along",
        "Upscale", "VP9", "VVC", "x264 (2160p)",
    )
    tv_rejects = movie_rejects + ("Dolby Vision (Without Fallback)",)
    empty_names = ("Banned Groups (Efficient)", "Banned Groups (Regular)")

    def score_span(profile, names, score_filter=False):
        placeholders = ",".join("?" for _ in names)
        sql = f"""
            SELECT COUNT(*), MIN(score), MAX(score)
            FROM quality_profile_custom_formats
            WHERE quality_profile_name = ?
              AND custom_format_name IN ({placeholders})
        """
        params = [profile, *names]
        if score_filter:
            sql += " AND score = -10000"
        return conn.execute(sql, params).fetchone()

    movie_span = score_span(movies, movie_rejects)
    tv_span = score_span(tv, tv_rejects, score_filter=True)
    expect(
        "Movies keeps 16 hard rejects at -100000",
        movie_span == (16, -100000, -100000),
        f"got {movie_span}",
    )
    expect(
        "TV keeps 17 hard rejects at -10000",
        tv_span == (17, -10000, -10000),
        f"got {tv_span}",
    )

    still_assigned = conn.execute(
        f"""
        SELECT quality_profile_name, custom_format_name, arr_type, score
        FROM quality_profile_custom_formats
        WHERE custom_format_name IN ({",".join("?" for _ in empty_names)})
        ORDER BY custom_format_name, quality_profile_name, arr_type
        """,
        empty_names,
    ).fetchall()
    expect(
        "Empty profile-specific ban formats are unassigned on every profile",
        still_assigned == [],
        f"still assigned {still_assigned}",
    )

    empty_assigned = conn.execute("""
        SELECT quality_profile_name, custom_format_name
        FROM quality_profile_custom_formats qpcf
        WHERE NOT EXISTS (
            SELECT 1 FROM custom_format_conditions cfc
            WHERE cfc.custom_format_name = qpcf.custom_format_name
        )
    """).fetchall()
    expect(
        "No quality profile assigns a custom format with zero conditions",
        empty_assigned == [],
        f"empty assignments {empty_assigned}",
    )

    definitions = conn.execute(
        f"""
        SELECT COUNT(*) FROM custom_formats
        WHERE name IN ({",".join("?" for _ in empty_names)})
        """,
        empty_names,
    ).fetchone()[0]
    conditions = conn.execute(
        f"""
        SELECT COUNT(*) FROM custom_format_conditions
        WHERE custom_format_name IN ({",".join("?" for _ in empty_names)})
        """,
        empty_names,
    ).fetchone()[0]
    expect("Empty ban definitions are kept", definitions == 2, f"definitions {definitions}")
    expect("Those definitions still have zero conditions", conditions == 0, f"conditions {conditions}")

    for profile, expected in ((movies, -100000), (tv, -10000)):
        for fmt in ("Banned Groups", "Banned Micro Encodes"):
            row = conn.execute(
                "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = ?",
                (profile, fmt),
            ).fetchone()
            got = None if row is None else row[0]
            expect(f"{profile} still scores {fmt} at {expected}", got == expected, f"got {got}")

    banned_group_conditions = conn.execute(
        "SELECT COUNT(*) FROM custom_format_conditions WHERE custom_format_name = 'Banned Groups'"
    ).fetchone()[0]
    expect("Shared Banned Groups list still has its conditions", banned_group_conditions >= 50, f"count {banned_group_conditions}")

    micro_ok = conn.execute(
        "SELECT pattern FROM regular_expressions WHERE name = 'HEVC Compact Micro OK'"
    ).fetchone()[0]
    for token in ("RARBG", "UTR", "iVy", "Joy", "t0paz", "POF"):
        on_ban = conn.execute(
            """
            SELECT COUNT(*) FROM custom_format_conditions
            WHERE name = ? AND custom_format_name LIKE 'Banned%'
            """,
            (token,),
        ).fetchone()[0]
        expect(f"{token} stays on the Micro OK list", token in micro_ok, "missing from HEVC Compact Micro OK")
        expect(f"{token} is not a condition on a ban format", on_ban == 0, f"ban rows {on_ban}")

    unchanged = (
        ("2160p WEB-DL HEVC", 0),
        ("1080p Compact Streaming WEB-DL", 5200),
        ("1080p Compact HEVC Tier 3", 4100),
        ("1080p Compact HEVC Tier 4", 3000),
        ("2160p Compact Bluray Tier 1", 38400),
    )
    for fmt, expected in unchanged:
        row = conn.execute(
            "SELECT score FROM quality_profile_custom_formats WHERE quality_profile_name = ? AND custom_format_name = ?",
            (movies, fmt),
        ).fetchone()
        got = None if row is None else row[0]
        expect(f"{fmt} stays {expected}", got == expected, f"got {got}")
    gates = conn.execute(
        "SELECT minimum_custom_format_score, upgrade_until_score FROM quality_profiles WHERE name = ?",
        (movies,),
    ).fetchone()
    expect("Movie minimum and cutoff stay 3000 / 41600", gates == (3000, 41600), f"{gates}")

    print(f"Empty assigned formats: {passed} passed, {failed} failed")
    return passed, failed


def run_1080p_last_resort(conn, movies, tv):
    """Unrecognized 1080p HEVC and any 1080p AVC clear min 3000.

    The sixteen released movies in the radarr4k search failed only because
    their usable 1080p release scored under 3000. Nine are HEVC from groups
    outside the compact ladder. Seven are AVC. Both new formats score 3000,
    the same band as 1080p Tier 4. They do not stack on Tier 1-4 or 1080p
    streaming, and they do not match 2160p, so a 4K micro or untouched 4K
    WEB that already scores 0 stays under the minimum.
    """
    print("\n=== 1080P LAST RESORT ===")
    passed = 0
    failed = 0
    hevc = "1080p Compact HEVC Last Resort"
    avc = "1080p Compact AVC Last Resort"
    sd = "720p Compact Last Resort"
    tiers = (
        "1080p Compact HEVC Tier 1",
        "1080p Compact HEVC Tier 2",
        "1080p Compact Streaming WEB-DL",
        "1080p Compact HEVC Tier 3",
        "1080p Compact HEVC Tier 4",
    )

    def expect(name, ok, detail=""):
        nonlocal passed, failed
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
        if ok:
            passed += 1
        else:
            failed += 1

    def names(matched):
        return [name for name, _score in matched]

    def check(title, exact, present, absent=(), profile=movies):
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, title, profile)
        got = names(matched)
        ok = score == exact and passed_cutoff == (exact >= 3000)
        missing = [fmt for fmt in present if fmt not in got]
        extra = [fmt for fmt in absent if fmt in got]
        if missing or extra:
            ok = False
        expect(
            title,
            ok,
            f"score {score} expected {exact} missing {missing} unexpected {extra} matched {matched}",
        )

    # Extras on these titles are what Radarr already scored. +3000 clears 3000.
    hevc_cases = (
        ("The.Perks.of.Being.a.Wallflower.2012.1080p.BluRay.10bit.DD5.1.With.Commentary.x265-POIASD", 3145),
        ("Riders.of.Justice.2020.1080p.ZEE5.WEB-DL.MULTi.AAC2.0.H.265-TR", 3010),
        ("En.kongelig.affaere.2012.DANiSH.1080p.WEB-DL.H.265.DDP5.1-CiNEMiX", 3125),
        ("The.Party.1968.1080p.BDRip.DTS.x265.10bit-MarkII", 3030),
        ("Drishyam.2.2021.1080p.AMZN.WEB-DL.DDP5.1.H.265-PMi-XDMovies", 3127),
        ("Runner 2026 1080p WEBRip 10Bit DDP5 1 x265-NeoNoir", 3155),
        ("Colony.2026.1080p.WEBRip.DUAL.DD5.1.10bits.x265-Rapta", 3115),
        ("Forgotten.Island.2026.1080p.MA.WEBRip.10bit.DDP5.1.x265-NeoNoir", 3155),
        ("The.Mongoose.2026.1080p.WEBRip.10Bit.DDP5.1.x265-NeoNoir", 3155),
    )
    for title, exact in hevc_cases:
        check(title, exact, (hevc,), tiers + (avc, sd))

    avc_cases = (
        ("Cam.2018.1080p.NF.WEB-DL.DDP5.1.H.264-POWER", 3127),
        ("Cam.2018.1080p.WEBRip.x264-RARBG", 3000),
        ("Sallskapsresan.II.Snowroller.1985.SWEDiSH.1080p.BluRay.x264-NAPTiME", 3000),
        ("Den.Ofrivillige.Golfaren.1991.SWEDiSH.1080p.BluRay.x264-NAPTiME", 3000),
        ("Sallskapsresan.1980.iNTERNAL.SWEDiSH.1080p.BluRay.x264-NAPTiME", 3000),
        ("Swedes.at.Sea.1988.SWEDiSH.1080p.iT.WEB-DL.AAC.2.0.H264-WoKE", 3020),
        ("Halsoresan.1999.SWEDiSH.1080p.BluRay.x264-NAPTiME", 3000),
        ("The.Stig.Helmer.Story.2011.SWEDiSH.1080p.BluRay.x264-SHUNPO", 3000),
    )
    for title, exact in avc_cases:
        check(title, exact, (avc,), tiers + (hevc, sd))

    # Existing 1080p ladder scores do not pick up another 3000.
    ladder = (
        ("Movie.2024.1080p.BluRay.x265-Ralphy", M_HD1, "1080p Compact HEVC Tier 1"),
        ("Movie.2024.1080p.BluRay.x265-TAoE", M_HD2, "1080p Compact HEVC Tier 2"),
        ("Movie.2024.1080p.WEB-DL.H265-FLUX", M_HD_STREAM, "1080p Compact Streaming WEB-DL"),
        ("Movie.2024.1080p.BluRay.x265-PSA", M_HD3, "1080p Compact HEVC Tier 3"),
        ("Movie.2024.1080p.WEB-DL.x265-iVy", M_HD4, "1080p Compact HEVC Tier 4"),
        ("Movie.2024.1080p.BluRay.x265-RARBG", M_HD4, "1080p Compact HEVC Tier 4"),
    )
    for title, exact, tier in ladder:
        check(title, exact, (tier,), (hevc, avc, sd))

    # A tier group's AVC release is the generic last resort, not that HEVC tier.
    check("Movie.2024.1080p.BluRay.x264-PSA", 3000, (avc,), tiers + (hevc, sd))
    check("Movie.2024.1080p.BluRay.x264-Ralphy", 3000, (avc,), tiers + (hevc, sd))
    # Both codecs: HEVC wins, and an elite group still stays on its tier only.
    check("Movie.2024.1080p.BluRay.x265.x264-POIASD", 3000, (hevc,), (avc, sd) + tiers)
    check("Movie.2024.1080p.BluRay.x265.x264-Ralphy", M_HD1, ("1080p Compact HEVC Tier 1",), (hevc, avc, sd))

    # Guards. These must not clear 3000 by way of either new format.
    blocked = (
        ("Movie.2024.2160p.BluRay.x265-POIASD", hevc),
        ("Movie.2024.2160p.WEB-DL.H265-NTb", hevc),
        ("Movie.2024.2160p.BluRay.HDR.x265-RARBG", hevc),
        ("Forgotten.Island.2026.2160p.WEBRip.DDP5.1.Atmos.DV.HDR10Plus.x265.10bit-MarkII", hevc),
        ("The.Mongoose.2026.2160p.AMZN.WEB-DL.DDP5.1.DV.HDR10+.H.265-ZAX", hevc),
        ("Drishyam.2.2021.2160p.AMZN.WEB-DL.DDP5.1.H.265-WADU", hevc),
        ("Movie.2024.2160p.BluRay.x264-HONE", avc),
        ("Movie.2024.1080p.HDTV.x265-POIASD", hevc),
        ("Movie.2024.1080p.HDTV.x264-NAPTiME", avc),
        ("Movie.2024.1080p.BluRay.REMUX.x265-POIASD", hevc),
        ("Movie.2024.1080p.BluRay.REMUX.x264-NAPTiME", avc),
        ("Movie.2024.1080p.WEB-DL.AV1-POIASD", hevc),
        ("Movie.2024.1080p.WEB-DL.x265.AV1-POIASD", hevc),
        ("Movie.2024.1080p.WEBRip.x264.AV1-RARBG", avc),
        ("Vielleicht.lieber.morgen.2012.German.DL.AC3.1080p.BluRay.x265-FuN", hevc),
        ("Movie.2024.German.DL.1080p.BluRay.x264-FuN", avc),
    )
    for title, banned in blocked:
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, title, movies)
        got = names(matched)
        expect(
            f"blocked {title}",
            banned not in got and hevc not in got and avc not in got and sd not in got and not passed_cutoff and score < 3000,
            f"score {score} pass {passed_cutoff} matched {matched}",
        )

    # YTS and MeGusta stay rejected. Banned Micro Encodes is -100000, so a
    # last-resort match still misses the minimum.
    for title in (
        "Movie.2024.1080p.BluRay.x265-YTS",
        "Movie.2024.1080p.BluRay.x264-YTS",
        "Movie.2024.1080p.WEBRip.x265-MeGusta",
        "Movie.2024.2160p.WEB-DL.x265-YTS",
    ):
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, title, movies)
        expect(
            f"still rejected {title}",
            not passed_cutoff and score < 3000 and "Banned Micro Encodes" in names(matched),
            f"score {score} pass {passed_cutoff} matched {matched}",
        )

    # 4K extras that already sit near 1780 must not gain 3000.
    forgotten = evaluate_release(
        conn,
        "Forgotten.Island.2026.2160p.WEBRip.DDP5.1.Atmos.DV.HDR10Plus.x265.10bit-MarkII",
        movies,
    )
    mongoose = evaluate_release(
        conn,
        "The.Mongoose.2026.2160p.AMZN.WEB-DL.DDP5.1.DV.HDR10+.H.265-ZAX",
        movies,
    )
    expect("Forgotten Island 4K stays 1780", forgotten[0] == 1780 and not forgotten[3], f"score {forgotten[0]}")
    expect("Mongoose 4K stays 1757", mongoose[0] == 1757 and not mongoose[3], f"score {mongoose[0]}")

    tv_rows = conn.execute(
        """
        SELECT COUNT(*) FROM quality_profile_custom_formats
        WHERE quality_profile_name = ? AND custom_format_name IN (?, ?)
        """,
        (tv, hevc, avc),
    ).fetchone()[0]
    expect("TV profile does not assign either last resort", tv_rows == 0, f"rows {tv_rows}")
    tv_score, _, _, _, tv_matched = evaluate_release(
        conn, "Movie.2024.1080p.BluRay.x265-POIASD", tv
    )
    expect(
        "TV scoring ignores the movie last resort",
        hevc not in names(tv_matched) and avc not in names(tv_matched) and sd not in names(tv_matched),
        f"score {tv_score} matched {tv_matched}",
    )

    print(f"1080p last resort: {passed} passed, {failed} failed")
    return passed, failed


def run_720p_last_resort(conn, movies, tv):
    """720p is its own rank under every 1080p quality.

    Bluray-1080p, WEBDL-1080p, and WEBRip-1080p already share one group, so
    720p mirrors that as one group below it. The format scores 3000, the
    same as a bare 1080p last resort. Extras can exceed that gap, which is
    why the quality rank, not the score, keeps 720p from winning.
    """
    print("\n=== 720P LAST RESORT ===")
    passed = 0
    failed = 0
    sd = "720p Compact Last Resort"
    hevc = "1080p Compact HEVC Last Resort"
    avc = "1080p Compact AVC Last Resort"

    def expect(name, ok, detail=""):
        nonlocal passed, failed
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
        if ok:
            passed += 1
        else:
            failed += 1

    def names(matched):
        return [name for name, _score in matched]

    def check(title, exact, present, absent=()):
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, title, movies)
        got = names(matched)
        missing = [fmt for fmt in present if fmt not in got]
        extra = [fmt for fmt in absent if fmt in got]
        ok = score == exact and passed_cutoff == (exact >= 3000) and not missing and not extra
        expect(
            title,
            ok,
            f"score {score} expected {exact} missing {missing} unexpected {extra} matched {matched}",
        )

    for title in (
        "Movie.2024.720p.BluRay.x265-NAPTiME",
        "Movie.2024.720p.BluRay.x265-POIASD",
        "Movie.2024.720p.WEB-DL.H.265-NeoNoir",
        "Movie.2024.720p.WEBRip.HEVC-POWER",
        "Movie.2024.720p.BluRay.x264-NAPTiME",
        "Movie.2024.720p.BluRay.H.264-SHUNPO",
        "Movie.2024.720p.WEB-DL.H264-WoKE",
        "Movie.2024.720p.WEBRip.x264-RARBG",
        "Movie.2024.720p.WEB.x265-POIASD",
    ):
        check(title, 3000, (sd,), (hevc, avc))

    # A name that is 1080p or 2160p does not take the 720p format.
    for title in (
        "Movie.2024.1080p.BluRay.x265-POIASD",
        "Movie.2024.1080p.WEB-DL.x264-NAPTiME",
        "Movie.2024.2160p.BluRay.x265-POIASD",
        "Movie.2024.2160p.WEB-DL.x264-NAPTiME",
        "Movie.2024.720p.1080p.BluRay.x265-NAPTiME",
        "Movie.2024.1080p.720p.WEB-DL.x264-SHUNPO",
    ):
        score, _min_s, _until, _passed_cutoff, matched = evaluate_release(conn, title, movies)
        expect(f"not 720p {title}", sd not in names(matched), f"score {score} matched {matched}")

    for title in (
        "Movie.2024.720p.BluRay.x265-YTS",
        "Movie.2024.720p.WEBRip.x264-MeGusta",
        "Movie.2024.720p.BluRay.x265-YIFY",
        "Movie.2024.720p.WEB-DL.H.264-GalaxyRG",
    ):
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, title, movies)
        got = names(matched)
        expect(
            f"banned micro {title}",
            sd not in got and not passed_cutoff and score < 3000 and "Banned Micro Encodes" in got,
            f"score {score} pass {passed_cutoff} matched {matched}",
        )

    for title in (
        "Movie.2024.720p.HDTV.x265-NAPTiME",
        "Movie.2024.720p.BluRay.REMUX.x265-NAPTiME",
        "Movie.2024.720p.WEB-DL.AV1-NAPTiME",
        "Movie.2024.480p.BluRay.x265-NAPTiME",
        "Movie.2024.German.DL.720p.BluRay.x265-FuN",
    ):
        score, _min_s, _until, passed_cutoff, matched = evaluate_release(conn, title, movies)
        expect(
            f"blocked {title}",
            sd not in names(matched) and not passed_cutoff and score < 3000,
            f"score {score} pass {passed_cutoff} matched {matched}",
        )

    truehd_score, _min_s, _until, truehd_ok, truehd_matched = evaluate_release(
        conn, "Movie.2024.720p.BluRay.TrueHD.x265-NAPTiME", movies
    )
    expect(
        "720p TrueHD still misses the minimum",
        not truehd_ok and truehd_score < 3000 and "TrueHD" in names(truehd_matched),
        f"score {truehd_score} matched {truehd_matched}",
    )

    # DV + HDR on a 720p name scores above a bare 1080p last resort. The
    # quality rank is what keeps that 720p from winning.
    tagged = evaluate_release(conn, "Movie.2024.720p.BluRay.DV.HDR.x265-NAPTiME", movies)
    bare_hd = evaluate_release(conn, "Movie.2024.1080p.BluRay.x264-NAPTiME", movies)
    extras = conn.execute(
        """
        SELECT COALESCE(SUM(score), 0) FROM quality_profile_custom_formats
        WHERE quality_profile_name = ? AND score > 0 AND score < 3000
        """,
        (movies,),
    ).fetchone()[0]
    ranks = dict(conn.execute(
        """
        SELECT quality_group_name, position FROM quality_profile_qualities
        WHERE quality_profile_name = ? AND enabled = 1
        """,
        (movies,),
    ).fetchall())
    expect(
        "Tagged 720p outscores a bare 1080p on custom formats alone",
        tagged[0] > bare_hd[0] and tagged[0] >= 3000 and bare_hd[0] == 3000 and extras > 1000,
        f"720p {tagged[0]} 1080p {bare_hd[0]} extras {extras} matched {tagged[4]}",
    )
    expect(
        "720p rank is below the whole 1080p rank",
        ranks.get("2160p", 99) < ranks.get("1080p Fallback", 99) < ranks.get("720p Fallback", -1),
        f"ranks {ranks}",
    )
    shared = conn.execute(
        """
        SELECT COUNT(*) FROM quality_group_members a
        JOIN quality_group_members b
          ON b.quality_profile_name = a.quality_profile_name
         AND b.quality_name = a.quality_name
         AND b.quality_group_name != a.quality_group_name
        WHERE a.quality_profile_name = ?
          AND a.quality_group_name = '720p Fallback'
        """,
        (movies,),
    ).fetchone()[0]
    expect("720p qualities are not also 1080p qualities", shared == 0, f"shared {shared}")
    hd_audio = conn.execute(
        """
        SELECT score FROM quality_profile_custom_formats
        WHERE quality_profile_name = ? AND custom_format_name = 'x265 (HD)'
        """,
        (movies,),
    ).fetchone()
    expect("Movie profile does not score x265 (HD)", hd_audio is None, f"score {hd_audio}")
    tv_rows = conn.execute(
        """
        SELECT COUNT(*) FROM quality_profile_custom_formats
        WHERE quality_profile_name = ? AND custom_format_name = ?
        """,
        (tv, sd),
    ).fetchone()[0]
    tv_qualities = conn.execute(
        """
        SELECT COUNT(*) FROM quality_group_members
        WHERE quality_profile_name = ? AND quality_name LIKE '%720p%'
        """,
        (tv,),
    ).fetchone()[0]
    expect("TV does not score or enable 720p", tv_rows == 0 and tv_qualities == 0, f"scores {tv_rows} qualities {tv_qualities}")
    size = conn.execute(
        """
        SELECT COUNT(*) FROM radarr_quality_definitions
        WHERE quality_name IN ('Bluray-720p', 'WEBDL-720p', 'WEBRip-720p')
          AND min_size = 0 AND preferred_size = 1990 AND max_size = 0
        """
    ).fetchone()[0]
    expect("720p size stays min 0, preferred 1990, max 0", size == 3, f"rows {size}")

    print(f"720p last resort: {passed} passed, {failed} failed")
    return passed, failed


if __name__ == "__main__":
    success = run_simulation_battery()
    sys.exit(0 if success else 1)
