#!/usr/bin/env python3
"""
Op 911: Library Quality Audit & Measured-File Telemetry Tool
================================================================================
Derives per-group quality fingerprints from measured files in Radarr4k/Sonarr4k
libraries and grab history, cross-checking against PCD tier placements.

Security & Execution Rules:
  - READ-ONLY: Only HTTP GET requests to Radarr and Sonarr APIs.
  - RADARR_URL, RADARR_API_KEY, SONARR_URL, SONARR_API_KEY from os.environ.
  - Output report written to telemetry/ (gitignored, contains user library titles).
  - Console prints only aggregate counts and contradiction flags (no titles).
"""

import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

# Import PCD compiled database loader
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate_scoring import build_compiled_db

# -----------------------------------------------------------------------------
# CONFIGURATION & ENVIRONMENT
# -----------------------------------------------------------------------------
RADARR_URL = os.environ.get("RADARR_URL", "http://127.0.0.1:7879")
SONARR_URL = os.environ.get("SONARR_URL", "http://127.0.0.1:8990")
RADARR_API_KEY = os.environ.get("RADARR_API_KEY")
SONARR_API_KEY = os.environ.get("SONARR_API_KEY")

def get_required_env():
    errors = []
    if not RADARR_API_KEY:
        errors.append("RADARR_API_KEY environment variable is required but not set.")
    if not SONARR_API_KEY:
        errors.append("SONARR_API_KEY environment variable is required but not set.")
    if errors:
        for err in errors:
            print(f"Error: {err}", file=sys.stderr)
        print("\nUsage example:", file=sys.stderr)
        print("  RADARR_API_KEY='...' SONARR_API_KEY='...' python3 tests/library_audit.py", file=sys.stderr)
        sys.exit(1)

# -----------------------------------------------------------------------------
# PCD DB TIER & REGEX LOADER
# -----------------------------------------------------------------------------
def load_tier_patterns_from_pcd():
    conn = build_compiled_db()
    
    def get_pattern(cf_name):
        row = conn.execute("""
            SELECT re.pattern FROM custom_formats cf
            JOIN custom_format_conditions cfc ON cf.name = cfc.custom_format_name
            JOIN condition_patterns cp ON cfc.custom_format_name = cp.custom_format_name AND cfc.name = cp.condition_name
            JOIN regular_expressions re ON cp.regular_expression_name = re.name
            WHERE cf.name = ?
        """, (cf_name,)).fetchone()
        return row[0] if row else None

    patterns = {
        "AV1": get_pattern("AV1"),
        "Quality": get_pattern("AV1 Quality Encoders"),
        "Compact": get_pattern("AV1 Compact Encoders"),
        "Storage": get_pattern("AV1 Storage Savers"),
        "Anime": get_pattern("AV1 Anime Encoders"),
    }
    return patterns

# -----------------------------------------------------------------------------
# PARSING & CLASSIFICATION LOGIC
# -----------------------------------------------------------------------------
def parse_runtime_minutes(runtime_str, default_minutes=None):
    """
    Parses 'HH:MM:SS', 'MM:SS', or float seconds into minutes.
    """
    if not runtime_str:
        return default_minutes
        
    if isinstance(runtime_str, (int, float)):
        return float(runtime_str) / 60.0 if runtime_str > 500 else float(runtime_str)
        
    parts = str(runtime_str).strip().split(":")
    try:
        if len(parts) == 3:
            h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
            return (h * 3600 + m * 60 + s) / 60.0
        elif len(parts) == 2:
            m, s = float(parts[0]), float(parts[1])
            return (m * 60 + s) / 60.0
        elif len(parts) == 1:
            val = float(parts[0])
            return val if val < 500 else val / 60.0
    except (ValueError, TypeError):
        pass
    return default_minutes

def extract_release_group(release_group, relative_path=None, scene_name=None, source_title=None):
    """
    Extracts group name using releaseGroup or falls back to end-anchored token matching.
    """
    rg = str(release_group).strip() if release_group is not None else ""
    if rg and rg.lower() not in ("unknown", "none", "null", "r"):
        return rg
        
    candidates = [s for s in (source_title, scene_name, relative_path) if s]
    for c in candidates:
        if not c:
            continue
        # Check specific compound variants like R&H / R and H
        if re.search(r"-(?:R[-._ ]?(?:and|&)[-._ ]?H)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$", str(c), re.IGNORECASE):
            return "R&H"

        # Check leading anime group prefix: [GROUP]
        m_anime = re.match(r"^\[(?P<grp>[^\]]+)\]", str(c))
        if m_anime:
            return m_anime.group("grp").strip()
            
        # Check standard release group suffix: -GROUP or -GROUP[site]
        m = re.search(r"-(?P<grp>[a-zA-Z0-9_& ]+?)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$", str(c), re.IGNORECASE)
        if m:
            grp = m.group("grp").strip()
            if grp:
                return grp

    if rg and rg.lower() not in ("unknown", "none", "null"):
        return rg
            
    return "Unknown"

def classify_group_tier(group_name, tier_patterns):
    """
    Determines PCD tier for a given release group name.
    """
    if not group_name or group_name == "Unknown":
        return "Untiered"
        
    test_str_suffix = f"-{group_name}"
    test_str_bracket = f"[{group_name}]"
    
    # Check Quality
    q_pat = tier_patterns.get("Quality")
    if q_pat and (re.search(q_pat, test_str_suffix, re.IGNORECASE) or re.search(q_pat, test_str_bracket, re.IGNORECASE)):
        return "Quality"
        
    # Check Compact
    c_pat = tier_patterns.get("Compact")
    if c_pat and (re.search(c_pat, test_str_suffix, re.IGNORECASE) or re.search(c_pat, test_str_bracket, re.IGNORECASE)):
        return "Compact"
        
    # Check Storage
    s_pat = tier_patterns.get("Storage")
    if s_pat and (re.search(s_pat, test_str_suffix, re.IGNORECASE) or re.search(s_pat, test_str_bracket, re.IGNORECASE)):
        return "Storage"
        
    # Check Anime
    a_pat = tier_patterns.get("Anime")
    if a_pat and (re.search(a_pat, test_str_bracket, re.IGNORECASE) or re.search(a_pat, test_str_suffix, re.IGNORECASE)):
        return "Anime"
        
    return "Untiered"

def is_av1_release(title_or_codec, av1_pattern):
    """
    Checks if a release is AV1 using the repository canonical AV1 regex.
    """
    if not title_or_codec or not av1_pattern:
        return False
    return bool(re.search(av1_pattern, title_or_codec, re.IGNORECASE))

# -----------------------------------------------------------------------------
# HTTP DATA PULL (READ-ONLY GET)
# -----------------------------------------------------------------------------
def fetch_json(url, api_key):
    req = urllib.request.Request(url, headers={"X-Api-Key": api_key})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def pull_radarr_data():
    movies_url = f"{RADARR_URL}/api/v3/movie"
    history_url = f"{RADARR_URL}/api/v3/history?pageSize=2000"
    
    movies = fetch_json(movies_url, RADARR_API_KEY)
    history_data = fetch_json(history_url, RADARR_API_KEY)
    history_records = history_data.get("records", []) if isinstance(history_data, dict) else []
    
    return movies, history_records

def pull_sonarr_data():
    series_url = f"{SONARR_URL}/api/v3/series"
    history_url = f"{SONARR_URL}/api/v3/history?pageSize=2000"
    
    series_list = fetch_json(series_url, SONARR_API_KEY)
    history_data = fetch_json(history_url, SONARR_API_KEY)
    history_records = history_data.get("records", []) if isinstance(history_data, dict) else []
    
    episode_files = []
    for s in series_list:
        s_id = s.get("id")
        if s_id:
            epf_url = f"{SONARR_URL}/api/v3/episodefile?seriesId={s_id}"
            ep_files = fetch_json(epf_url, SONARR_API_KEY)
            for ef in ep_files:
                ef["seriesTitle"] = s.get("title")
                episode_files.append(ef)
                
    return series_list, episode_files, history_records

# -----------------------------------------------------------------------------
# AUDIT CORE: FINGERPRINTING & CONTRADICTION DETECTION
# -----------------------------------------------------------------------------
def analyze_library(movies, radarr_history, series_list, episode_files, sonarr_history, tier_patterns):
    av1_pat = tier_patterns["AV1"]
    
    parsed_files = []
    contradiction_flags = []
    
    # 1. PROCESS RADARR MOVIES
    for m in movies:
        if not m.get("hasFile"):
            continue
        mf = m.get("movieFile")
        if not mf:
            continue
            
        rel_path = mf.get("relativePath") or ""
        scene_name = mf.get("sceneName") or ""
        rg = mf.get("releaseGroup")
        group = extract_release_group(rg, relative_path=rel_path, scene_name=scene_name)
        
        media_info = mf.get("mediaInfo") or {}
        v_codec = media_info.get("videoCodec") or ""
        is_av1 = is_av1_release(v_codec, av1_pat) or is_av1_release(rel_path, av1_pat) or is_av1_release(scene_name, av1_pat)
        
        size_bytes = mf.get("size") or 0
        size_gb = size_bytes / (1024 ** 3)
        
        runtime_mins = parse_runtime_minutes(media_info.get("runTime"), default_minutes=m.get("runtime"))
        mb_per_min = (size_bytes / (1024 ** 2)) / runtime_mins if (runtime_mins and runtime_mins > 0 and size_bytes > 0) else None
        mbps = (size_bytes * 8) / (runtime_mins * 60 * 1_000_000) if (runtime_mins and runtime_mins > 0 and size_bytes > 0) else None
        
        height = media_info.get("height") or 0
        res_label = "2160p" if height >= 1400 or "2160p" in rel_path else ("1080p" if height >= 900 or "1080p" in rel_path else "720p")
        
        dyn_range = str(media_info.get("videoDynamicRange") or "")
        dyn_type = str(media_info.get("videoDynamicRangeType") or "")
        is_hdr = "HDR" in dyn_range or "HDR" in dyn_type or "HDR" in rel_path or "HDR" in scene_name
        is_dv = "DV" in dyn_type or "Dolby Vision" in dyn_type or "DV" in rel_path or "DoVi" in rel_path
        
        a_codec = str(media_info.get("audioCodec") or "")
        is_lossless = any(lc in a_codec for lc in ("TrueHD", "DTS-HD", "FLAC", "PCM"))
        is_atmos = "Atmos" in a_codec or "DTS:X" in a_codec or "Atmos" in str(media_info.get("audioStreamTitle") or "")
        bit_depth = media_info.get("videoBitDepth") or 8
        
        tier = classify_group_tier(group, tier_patterns)
        
        record = {
            "type": "Movie",
            "title": m.get("title"),
            "year": m.get("year"),
            "id": m.get("id"),
            "group": group,
            "tier": tier,
            "is_av1": is_av1,
            "size_gb": size_gb,
            "runtime_mins": runtime_mins,
            "mb_per_min": mb_per_min,
            "mbps": mbps,
            "resolution": res_label,
            "is_hdr": is_hdr,
            "is_dv": is_dv,
            "is_lossless": is_lossless,
            "is_atmos": is_atmos,
            "bit_depth": bit_depth,
            "audio_codec": a_codec,
            "video_codec": v_codec,
            "file_name": rel_path or scene_name
        }
        parsed_files.append(record)
        
        # Check Metadata Mismatches
        search_text = f"{rel_path} {scene_name}"
        if "TrueHD" in search_text and not is_lossless and "TrueHD" not in a_codec:
            contradiction_flags.append({
                "kind": "METADATA_MISMATCH",
                "group": group,
                "tier": tier,
                "title": m.get("title"),
                "detail": f"Title claimed TrueHD but mediaInfo audioCodec is '{a_codec}' ({size_gb:.2f} GB)"
            })
        elif "Atmos" in search_text and not is_atmos:
            contradiction_flags.append({
                "kind": "METADATA_MISMATCH",
                "group": group,
                "tier": tier,
                "title": m.get("title"),
                "detail": f"Title claimed Atmos but mediaInfo audioCodec is '{a_codec}' ({size_gb:.2f} GB)"
            })
        if ("DV" in search_text or "Dolby.Vision" in search_text) and not is_dv:
            contradiction_flags.append({
                "kind": "METADATA_MISMATCH",
                "group": group,
                "tier": tier,
                "title": m.get("title"),
                "detail": f"Title claimed Dolby Vision but mediaInfo dynamicRange is '{dyn_type or dyn_range or 'SDR'}' ({size_gb:.2f} GB)"
            })

    # 2. PROCESS SONARR EPISODE FILES
    for ef in episode_files:
        rel_path = ef.get("relativePath") or ""
        scene_name = ef.get("sceneName") or ""
        rg = ef.get("releaseGroup")
        group = extract_release_group(rg, relative_path=rel_path, scene_name=scene_name)
        
        media_info = ef.get("mediaInfo") or {}
        v_codec = media_info.get("videoCodec") or ""
        is_av1 = is_av1_release(v_codec, av1_pat) or is_av1_release(rel_path, av1_pat) or is_av1_release(scene_name, av1_pat)
        
        size_bytes = ef.get("size") or 0
        size_gb = size_bytes / (1024 ** 3)
        
        runtime_mins = parse_runtime_minutes(media_info.get("runTime"))
        mb_per_min = (size_bytes / (1024 ** 2)) / runtime_mins if (runtime_mins and runtime_mins > 0 and size_bytes > 0) else None
        mbps = (size_bytes * 8) / (runtime_mins * 60 * 1_000_000) if (runtime_mins and runtime_mins > 0 and size_bytes > 0) else None
        
        height = media_info.get("height") or 0
        res_label = "2160p" if height >= 1400 or "2160p" in rel_path else ("1080p" if height >= 900 or "1080p" in rel_path else "720p")
        
        dyn_range = str(media_info.get("videoDynamicRange") or "")
        dyn_type = str(media_info.get("videoDynamicRangeType") or "")
        is_hdr = "HDR" in dyn_range or "HDR" in dyn_type or "HDR" in rel_path or "HDR" in scene_name
        is_dv = "DV" in dyn_type or "Dolby Vision" in dyn_type or "DV" in rel_path or "DoVi" in rel_path
        
        a_codec = str(media_info.get("audioCodec") or "")
        is_lossless = any(lc in a_codec for lc in ("TrueHD", "DTS-HD", "FLAC", "PCM"))
        is_atmos = "Atmos" in a_codec or "DTS:X" in a_codec
        bit_depth = media_info.get("videoBitDepth") or 8
        
        tier = classify_group_tier(group, tier_patterns)
        
        record = {
            "type": "TV",
            "title": ef.get("seriesTitle") or "TV Series",
            "year": None,
            "id": ef.get("seriesId"),
            "group": group,
            "tier": tier,
            "is_av1": is_av1,
            "size_gb": size_gb,
            "runtime_mins": runtime_mins,
            "mb_per_min": mb_per_min,
            "mbps": mbps,
            "resolution": res_label,
            "is_hdr": is_hdr,
            "is_dv": is_dv,
            "is_lossless": is_lossless,
            "is_atmos": is_atmos,
            "bit_depth": bit_depth,
            "audio_codec": a_codec,
            "video_codec": v_codec,
            "file_name": rel_path or scene_name
        }
        parsed_files.append(record)
        
        # Check Metadata Mismatches for Episode File
        search_text = f"{rel_path} {scene_name}"
        if "TrueHD" in search_text and not is_lossless and "TrueHD" not in a_codec:
            contradiction_flags.append({
                "kind": "METADATA_MISMATCH",
                "group": group,
                "tier": tier,
                "title": ef.get("seriesTitle") or "TV Episode",
                "detail": f"Title claimed TrueHD but mediaInfo audioCodec is '{a_codec}' ({size_gb:.2f} GB)"
            })
        elif "Atmos" in search_text and not is_atmos:
            contradiction_flags.append({
                "kind": "METADATA_MISMATCH",
                "group": group,
                "tier": tier,
                "title": ef.get("seriesTitle") or "TV Episode",
                "detail": f"Title claimed Atmos but mediaInfo audioCodec is '{a_codec}' ({size_gb:.2f} GB)"
            })
        if ("DV" in search_text or "Dolby.Vision" in search_text) and not is_dv:
            contradiction_flags.append({
                "kind": "METADATA_MISMATCH",
                "group": group,
                "tier": tier,
                "title": ef.get("seriesTitle") or "TV Episode",
                "detail": f"Title claimed Dolby Vision but mediaInfo dynamicRange is '{dyn_type or dyn_range or 'SDR'}' ({size_gb:.2f} GB)"
            })

    # 3. GROUP AGGREGATIONS & FINGERPRINTING
    groups_data = {}
    for f in parsed_files:
        grp = f["group"]
        if grp not in groups_data:
            groups_data[grp] = {
                "tier": f["tier"],
                "total_files": 0,
                "av1_files": 0,
                "sizes_2160p": [],
                "sizes_1080p": [],
                "sizes_all": [],
                "mb_per_min_vals": [],
                "mbps_vals": [],
                "hdr_count": 0,
                "dv_count": 0,
                "lossless_count": 0,
                "atmos_count": 0,
                "bit_depths": [],
                "resolutions": {"2160p": 0, "1080p": 0, "720p": 0}
            }
            
        g = groups_data[grp]
        g["total_files"] += 1
        if f["is_av1"]:
            g["av1_files"] += 1
            
        g["sizes_all"].append(f["size_gb"])
        if f["resolution"] == "2160p":
            g["sizes_2160p"].append(f["size_gb"])
        elif f["resolution"] == "1080p":
            g["sizes_1080p"].append(f["size_gb"])
            
        if f["mb_per_min"] is not None:
            g["mb_per_min_vals"].append(f["mb_per_min"])
        if f["mbps"] is not None:
            g["mbps_vals"].append(f["mbps"])
            
        if f["is_hdr"]:
            g["hdr_count"] += 1
        if f["is_dv"]:
            g["dv_count"] += 1
        if f["is_lossless"]:
            g["lossless_count"] += 1
        if f["is_atmos"]:
            g["atmos_count"] += 1
            
        g["bit_depths"].append(f["bit_depth"])
        g["resolutions"][f["resolution"]] = g["resolutions"].get(f["resolution"], 0) + 1

    # 4. EVALUATE CONTRADICTION FLAGS
    for grp, g in groups_data.items():
        tier = g["tier"]
        total = g["total_files"]
        med_all = statistics.median(g["sizes_all"]) if g["sizes_all"] else 0
        med_2160p = statistics.median(g["sizes_2160p"]) if g["sizes_2160p"] else 0
        med_1080p = statistics.median(g["sizes_1080p"]) if g["sizes_1080p"] else 0
        
        # Flag 1: Quality Under-sized (<10 GB 2160p or <6 GB 1080p)
        if tier == "Quality":
            if g["sizes_2160p"] and med_2160p < 10.0:
                contradiction_flags.append({
                    "kind": "QUALITY_UNDERSIZED",
                    "group": grp,
                    "tier": tier,
                    "detail": f"Quality-tier group median 2160p size is {med_2160p:.2f} GB (< 10 GB threshold across {len(g['sizes_2160p'])} files)"
                })
            elif not g["sizes_2160p"] and g["sizes_1080p"] and med_1080p < 6.0:
                contradiction_flags.append({
                    "kind": "QUALITY_UNDERSIZED",
                    "group": grp,
                    "tier": tier,
                    "detail": f"Quality-tier group median 1080p size is {med_1080p:.2f} GB (< 6 GB threshold across {len(g['sizes_1080p'])} files)"
                })

        # Flag 2: Storage Over-sized (>8 GB)
        if tier == "Storage":
            if med_all > 8.0:
                contradiction_flags.append({
                    "kind": "STORAGE_OVERSIZED",
                    "group": grp,
                    "tier": tier,
                    "detail": f"Storage-tier group median size is {med_all:.2f} GB (> 8 GB threshold across {total} files)"
                })

        # Flag 3: Compact Over-sized (Quality Candidate > 15 GB)
        if tier == "Compact":
            if g["sizes_2160p"] and len(g["sizes_2160p"]) >= 2 and med_2160p > 15.0:
                contradiction_flags.append({
                    "kind": "COMPACT_OVERSIZED_QUALITY_CANDIDATE",
                    "group": grp,
                    "tier": tier,
                    "detail": f"Compact-tier group median 2160p size is {med_2160p:.2f} GB (> 15 GB threshold across {len(g['sizes_2160p'])} files) -> Quality Tier Candidate"
                })

        # Flag 4: Untiered Group with >= 5 files (Tiering Candidate)
        if tier == "Untiered" and grp != "Unknown":
            if total >= 5:
                contradiction_flags.append({
                    "kind": "UNTIERED_TIERING_CANDIDATE",
                    "group": grp,
                    "tier": tier,
                    "detail": f"Untiered group has {total} files in library (Median size: {med_all:.2f} GB, AV1: {g['av1_files']}/{total}) -> Tiering Candidate"
                })

    # 5. HEAD-TO-HEADS FROM RADARR HISTORY
    head_to_heads = []
    grabs_by_movie = {}
    for r in radarr_history:
        if r.get("eventType") in ("grabbed", "downloadFolderImported", 1):
            m_id = r.get("movieId")
            if not m_id:
                continue
            src_title = r.get("sourceTitle") or ""
            d_data = r.get("data") or {}
            grp = extract_release_group(d_data.get("releaseGroup"), source_title=src_title)
            size_val = float(d_data.get("size") or 0)
            if size_val > 0:
                size_gb = size_val / (1024 ** 3)
            else:
                size_gb = 0
            if m_id not in grabs_by_movie:
                grabs_by_movie[m_id] = []
            grabs_by_movie[m_id].append({
                "group": grp,
                "title": src_title,
                "size_gb": size_gb,
                "date": r.get("date")
            })

    for m_id, grabs in grabs_by_movie.items():
        distinct_groups = set(g["group"] for g in grabs if g["group"] != "Unknown")
        if len(distinct_groups) >= 2:
            head_to_heads.append({
                "movieId": m_id,
                "grabs": grabs
            })

    return parsed_files, groups_data, contradiction_flags, head_to_heads

# -----------------------------------------------------------------------------
# REPORT GENERATION (MARKDOWN EXPORT)
# -----------------------------------------------------------------------------
def generate_markdown_report(parsed_files, groups_data, contradiction_flags, head_to_heads, output_dir="telemetry"):
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.utcnow().strftime("%Y%m%d")
    report_path = os.path.join(output_dir, f"library_quality_audit_{today_str}.md")
    
    total_files = len(parsed_files)
    av1_count = sum(1 for f in parsed_files if f["is_av1"])
    movie_count = sum(1 for f in parsed_files if f["type"] == "Movie")
    tv_count = sum(1 for f in parsed_files if f["type"] == "TV")
    
    lines = [
        f"# 📊 Library Quality Audit & Measured-File Telemetry Report",
        f"",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
        f"**Sample Size:** {total_files} active library files ({movie_count} Movies, {tv_count} TV Episodes)  ",
        f"**AV1 Penetration:** {av1_count}/{total_files} ({av1_count/total_files*100:.1f}%)  ",
        f"",
        f"> [!NOTE]",
        f"> **Selection Bias Caveat:** Active library files reflect releases admitted by active Quality Profiles. Grab history is included to provide head-to-head comparisons for releases later upgraded or replaced.",
        f"",
        f"---",
        f"",
        f"## 1. Executive Summary & Contradiction Flags",
        f""
    ]
    
    if contradiction_flags:
        lines.append(f"| Flag Type | Release Group | Current Tier | Finding & Telemetry Detail |")
        lines.append(f"| :--- | :--- | :---: | :--- |")
        for flag in contradiction_flags:
            lines.append(f"| `{flag['kind']}` | **{flag['group']}** | `{flag['tier']}` | {flag['detail']} |")
    else:
        lines.append("✅ **No contradictory tier anomalies or metadata mismatches detected.**")
        
    lines.extend([
        f"",
        f"---",
        f"",
        f"## 2. Per-Group Measured Quality Fingerprints",
        f"",
        f"| Group | Tier | Files (AV1) | Median 2160p | Median 1080p | MB/min Proxy | % HDR/DV | % Lossless | % Atmos | 10-bit |",
        f"| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])
    
    sorted_groups = sorted(groups_data.items(), key=lambda x: x[1]["total_files"], reverse=True)
    for grp, g in sorted_groups:
        tier = g["tier"]
        tot = g["total_files"]
        av1_f = g["av1_files"]
        med_2160p = f"{statistics.median(g['sizes_2160p']):.2f} GB" if g["sizes_2160p"] else "-"
        med_1080p = f"{statistics.median(g['sizes_1080p']):.2f} GB" if g["sizes_1080p"] else "-"
        mb_min = f"{statistics.median(g['mb_per_min_vals']):.1f}" if g["mb_per_min_vals"] else "-"
        hdr_pct = f"{g['hdr_count']/tot*100:.0f}%" if tot else "0%"
        lossless_pct = f"{g['lossless_count']/tot*100:.0f}%" if tot else "0%"
        atmos_pct = f"{g['atmos_count']/tot*100:.0f}%" if tot else "0%"
        bit10_pct = f"{sum(1 for b in g['bit_depths'] if b >= 10)/tot*100:.0f}%" if tot else "0%"
        
        lines.append(f"| **{grp}** | `{tier}` | {tot} ({av1_f}) | {med_2160p} | {med_1080p} | {mb_min} | {hdr_pct} | {lossless_pct} | {atmos_pct} | {bit10_pct} |")
        
    lines.extend([
        f"",
        f"---",
        f"",
        f"## 3. Per-Title Head-to-Head Comparisons (Grab History vs Active)",
        f""
    ])
    
    if head_to_heads:
        for idx, h2h in enumerate(head_to_heads, 1):
            lines.append(f"### Head-to-Head #{idx} (Movie ID: `{h2h['movieId']}`)")
            lines.append(f"| Release Group | Size (GB) | Date Grabbed | Release Title |")
            lines.append(f"| :--- | :---: | :--- | :--- |")
            for g in h2h["grabs"]:
                lines.append(f"| **{g['group']}** | {g['size_gb']:.2f} | {g.get('date', '-')} | `{g['title']}` |")
            lines.append("")
    else:
        lines.append("No multi-group grab history recorded for the current library corpus.")
        
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    return report_path

# -----------------------------------------------------------------------------
# CONSOLE SUMMARY (PRIVACY SAFE - NO TITLES)
# -----------------------------------------------------------------------------
def print_console_summary(parsed_files, groups_data, contradiction_flags, report_path):
    total = len(parsed_files)
    av1_total = sum(1 for f in parsed_files if f["is_av1"])
    tier_counts = {}
    for f in parsed_files:
        tier_counts[f["tier"]] = tier_counts.get(f["tier"], 0) + 1
        
    print("\n" + "=" * 80)
    print("OP 911: LIBRARY QUALITY AUDIT & TELEMETRY SUMMARY")
    print("=" * 80)
    print(f"Total Measured Library Files : {total}")
    print(f"AV1 Codec Files              : {av1_total} ({av1_total/total*100:.1f}%)" if total else "0")
    print(f"Non-AV1 Fallback Files       : {total - av1_total}")
    print(f"Distinct Release Groups      : {len(groups_data)}")
    print("\n--- File Distribution by PCD Tier ---")
    for t, cnt in sorted(tier_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {t:<12} : {cnt:>4} files ({cnt/total*100:.1f}%)")
        
    print("\n--- Contradiction Flags Detected ---")
    if contradiction_flags:
        for idx, flag in enumerate(contradiction_flags, 1):
            print(f"  [{idx}] {flag['kind']:<30} Group: {flag['group']:<16} Tier: {flag['tier']:<8}")
            print(f"      Detail: {flag['detail']}")
    else:
        print("  [OK] No contradictory tier anomalies or flag mismatches found.")
        
    print("\n" + "=" * 80)
    print(f"Full Private Audit Report Written: {report_path}")
    print("=" * 80 + "\n")

# -----------------------------------------------------------------------------
# MAIN CLI ENTRYPOINT
# -----------------------------------------------------------------------------
def main():
    get_required_env()
    tier_patterns = load_tier_patterns_from_pcd()
    
    print("Pulling live library telemetry from Radarr4k & Sonarr4k...")
    movies, radarr_hist = pull_radarr_data()
    series_list, episode_files, sonarr_hist = pull_sonarr_data()
    
    parsed_files, groups_data, contradiction_flags, head_to_heads = analyze_library(
        movies, radarr_hist, series_list, episode_files, sonarr_hist, tier_patterns
    )
    
    report_path = generate_markdown_report(
        parsed_files, groups_data, contradiction_flags, head_to_heads
    )
    
    print_console_summary(parsed_files, groups_data, contradiction_flags, report_path)

if __name__ == "__main__":
    main()
