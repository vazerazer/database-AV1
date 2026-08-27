#!/usr/bin/env python3
"""
Op 912: Supply-Side Search Audit & Prospective Telemetry Tool
================================================================================
Queries candidate releases from Radarr4k/Sonarr4k interactive search APIs,
scores them locally via compiled PCD SQLite DB harness, fingerprints indexer
supply groups, calculates win-rates, and flags tier supply gaps or anomalies.

Hard Safety Rules:
  - STRICTLY READ-ONLY: Only HTTP GET requests. Never POST/PUT/DELETE.
  - Never call POST /api/v3/command (which auto-grabs).
  - Indexer quota respect: Configurable sample size and search delay.
  - Output report written to telemetry/ (gitignored, contains candidate titles).
  - Console prints only aggregate counts and flags (no library titles).
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

# Import PCD database and scoring harness
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate_scoring import build_compiled_db, evaluate_release
from library_audit import extract_release_group, classify_group_tier, is_av1_release, load_tier_patterns_from_pcd, parse_runtime_minutes

# -----------------------------------------------------------------------------
# CONFIGURATION & ENVIRONMENT
# -----------------------------------------------------------------------------
RADARR_URL = os.environ.get("RADARR_URL", "http://127.0.0.1:7879")
SONARR_URL = os.environ.get("SONARR_URL", "http://127.0.0.1:8990")
RADARR_API_KEY = os.environ.get("RADARR_API_KEY")
SONARR_API_KEY = os.environ.get("SONARR_API_KEY")

SAMPLE_SIZE = int(os.environ.get("SAMPLE_SIZE", "30"))
SEARCH_DELAY = float(os.environ.get("SEARCH_DELAY", "1.5"))

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
        print("  RADARR_API_KEY='...' SONARR_API_KEY='...' python3 tests/supply_audit.py", file=sys.stderr)
        sys.exit(1)

def fetch_json(url, api_key):
    req = urllib.request.Request(url, headers={"X-Api-Key": api_key})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

# -----------------------------------------------------------------------------
# TIER ROSTER EXTRACTOR (FROM PCD DB)
# -----------------------------------------------------------------------------
def get_all_tiered_groups_from_db(conn):
    """
    Extracts all distinct group names explicitly referenced in AV1 tier CFs.
    """
    tiered_groups = {}
    tier_cf_names = {
        "AV1 Quality Encoders": "Quality",
        "AV1 Compact Encoders": "Compact",
        "AV1 Storage Savers": "Storage",
        "AV1 Anime Encoders": "Anime"
    }
    
    for cf_name, tier in tier_cf_names.items():
        rows = conn.execute("""
            SELECT re.pattern FROM custom_formats cf
            JOIN custom_format_conditions cfc ON cf.name = cfc.custom_format_name
            JOIN condition_patterns cp ON cfc.custom_format_name = cp.custom_format_name AND cfc.name = cp.condition_name
            JOIN regular_expressions re ON cp.regular_expression_name = re.name
            WHERE cf.name = ?
        """, (cf_name,)).fetchall()
        
        for r in rows:
            pat = r[0]
            cleaned = re.sub(r"\(\?i\)", "", pat)
            cleaned = re.sub(r"\(\?:", "|", cleaned)
            cleaned = re.sub(r"\[[a-z0-9_\\-\\.]+\]", "", cleaned, flags=re.I)
            cleaned = re.sub(r"\(\?:\\[\.\s]+[a-zA-Z0-9_-]+\)\?", "", cleaned)
            raw_tokens = re.split(r"[|()\[\]]", cleaned)
            for tok in raw_tokens:
                clean_g = re.sub(r"^[^\w&]+|[^\w&]+$", "", tok).strip()
                clean_g = clean_g.replace("[-._ ]", " ").replace("[-._]?", "").replace("[-._ ]?", " ")
                clean_g = re.sub(r"\s+", " ", clean_g).strip()
                if clean_g and len(clean_g) >= 2 and not clean_g.isdigit() and clean_g.lower() not in ("and", "or", "a-z0-9", "mkv", "mp4"):
                    if not clean_g.startswith("a-z") and not clean_g.startswith("0-9") and not clean_g.startswith("2,4") and not clean_g.startswith("s+"):
                        tiered_groups[clean_g] = tier
                        
    return tiered_groups

# -----------------------------------------------------------------------------
# CANDIDATE RELEASE SCORER & FINGERPRINTER
# -----------------------------------------------------------------------------
def parse_title_tokens(title):
    t_upper = title.upper()
    is_hdr = bool(re.search(r"\b(HDR10\+|HDR10|HDR)\b", t_upper))
    is_dv = bool(re.search(r"\b(DV|DOVI|DOLBY[-._ ]?VISION)\b", t_upper))
    is_atmos = bool(re.search(r"\b(ATMOS|DTS[-._ ]?X)\b", t_upper))
    is_truehd = bool(re.search(r"\bTRUEHD\b", t_upper))
    is_lossless = bool(re.search(r"\b(TRUEHD|DTS[-._ ]?HD|FLAC|PCM)\b", t_upper))
    is_x265 = bool(re.search(r"(?<![a-zA-Z0-9])([XH][-._ ]?265|HEVC)(?![a-zA-Z0-9])", t_upper, re.IGNORECASE))
    is_x264 = bool(re.search(r"(?<![a-zA-Z0-9])([XH][-._ ]?264|AVC)(?![a-zA-Z0-9])", t_upper, re.IGNORECASE))
    
    return {
        "is_hdr": is_hdr,
        "is_dv": is_dv,
        "is_atmos": is_atmos,
        "is_truehd": is_truehd,
        "is_lossless": is_lossless,
        "is_x265": is_x265,
        "is_x264": is_x264
    }

def analyze_supply_candidates(candidates_by_title, conn, tier_patterns):
    """
    Processes all candidate releases across searched titles, scores them
    under PCD AV1 profiles, and generates per-group fingerprints and flags.
    """
    all_tiered_groups = get_all_tiered_groups_from_db(conn)
    av1_pat = tier_patterns["AV1"]
    
    group_supply = {}
    flags = []
    title_evaluations = []
    
    total_candidates_evaluated = 0
    seen_groups_in_supply = set()
    
    for item in candidates_by_title:
        t_info = item["title_info"]
        arr_type = item["arr_type"]
        primary_profile = item["primary_profile"]
        releases = item["releases"]
        current_file = item.get("current_file", {})
        runtime_mins = item.get("runtime_mins")
        
        scored_releases = []
        
        for r in releases:
            total_candidates_evaluated += 1
            rel_title = r.get("title") or ""
            rg = r.get("releaseGroup")
            group = extract_release_group(rg, source_title=rel_title)
            tier = classify_group_tier(group, tier_patterns)
            
            size_bytes = float(r.get("size") or 0)
            size_gb = size_bytes / (1024 ** 3)
            indexer = r.get("indexer") or "Unknown"
            
            is_av1 = is_av1_release(rel_title, av1_pat)
            tokens = parse_title_tokens(rel_title)
            
            # Local PCD scoring
            score, min_score, upgrade_until, passed_cutoff, matched = evaluate_release(
                conn, rel_title, primary_profile, arr_type
            )
            
            # Check Absurdity / Fake release (e.g. 1080p/2160p < 50MB)
            if size_bytes > 0 and size_bytes < (50 * 1024 * 1024):
                if re.search(r"\b(2160p|1080p|720p)\b", rel_title, re.IGNORECASE) and re.search(r"\b(WEB[-._ ]?DL|WEBRip|BluRay)\b", rel_title, re.IGNORECASE):
                    flags.append({
                        "kind": "ABSURDITY_BAN_CANDIDATE",
                        "group": group,
                        "tier": tier,
                        "title_id": t_info.get("id"),
                        "detail": f"Absurdly small candidate ({size_bytes / (1024**2):.1f} MB) claiming HD/UHD: '{rel_title}' via {indexer}"
                    })
                    
            scored_releases.append({
                "title": rel_title,
                "group": group,
                "tier": tier,
                "size_gb": size_gb,
                "size_bytes": size_bytes,
                "indexer": indexer,
                "is_av1": is_av1,
                "score": score,
                "min_score": min_score,
                "passed_cutoff": passed_cutoff,
                "matched_cfs": matched,
                "tokens": tokens
            })
            
            # Aggregate per-group metrics
            if group not in group_supply:
                group_supply[group] = {
                    "tier": tier,
                    "appearances": 0,
                    "av1_appearances": 0,
                    "x265_appearances": 0,
                    "x264_appearances": 0,
                    "sizes_gb": [],
                    "mb_per_min_vals": [],
                    "scores": [],
                    "passed_cutoff_count": 0,
                    "hdr_count": 0,
                    "dv_count": 0,
                    "atmos_count": 0,
                    "truehd_count": 0,
                    "lossless_count": 0,
                    "wins": 0,
                    "indexers": set()
                }
                
            gs = group_supply[group]
            gs["appearances"] += 1
            if is_av1:
                gs["av1_appearances"] += 1
            if tokens["is_x265"]:
                gs["x265_appearances"] += 1
            if tokens["is_x264"]:
                gs["x264_appearances"] += 1
                
            gs["sizes_gb"].append(size_gb)
            if runtime_mins and runtime_mins > 0 and size_bytes > 0:
                mb_min = (size_bytes / (1024 ** 2)) / runtime_mins
                gs["mb_per_min_vals"].append(mb_min)
                
            gs["scores"].append(score)
            if passed_cutoff:
                gs["passed_cutoff_count"] += 1
            if tokens["is_hdr"]:
                gs["hdr_count"] += 1
            if tokens["is_dv"]:
                gs["dv_count"] += 1
            if tokens["is_atmos"]:
                gs["atmos_count"] += 1
            if tokens["is_truehd"]:
                gs["truehd_count"] += 1
            if tokens["is_lossless"]:
                gs["lossless_count"] += 1
                
            gs["indexers"].add(indexer)
            seen_groups_in_supply.add(group)
            
        # Determine Top Scoring Candidate (Winner) for this title
        valid_candidates = [r for r in scored_releases if r["passed_cutoff"]]
        top_candidate = max(valid_candidates, key=lambda x: x["score"]) if valid_candidates else None
        
        if top_candidate:
            winner_group = top_candidate["group"]
            group_supply[winner_group]["wins"] += 1
            
            # Check Upgrade Opportunity vs currently held file
            curr_size_gb = current_file.get("size_gb", 0)
            curr_is_av1 = current_file.get("is_av1", False)
            curr_score = current_file.get("score", 0)
            
            if not curr_is_av1 and top_candidate["is_av1"]:
                if top_candidate["score"] >= curr_score + 300:
                    flags.append({
                        "kind": "UPGRADE_OPPORTUNITY",
                        "group": winner_group,
                        "tier": top_candidate["tier"],
                        "title_id": t_info.get("id"),
                        "detail": f"AV1 upgrade available from {winner_group} (Score: {top_candidate['score']} vs Current: {curr_score}, Delta: +{top_candidate['score'] - curr_score})"
                    })
                    
        title_evaluations.append({
            "title_info": t_info,
            "arr_type": arr_type,
            "profile": primary_profile,
            "total_candidates": len(releases),
            "top_candidate": top_candidate,
            "current_file": current_file
        })

    # 1. Flag: Tiered Groups with Zero Supply
    for grp, tier in all_tiered_groups.items():
        if grp not in seen_groups_in_supply:
            flags.append({
                "kind": "TIERED_ZERO_SUPPLY",
                "group": grp,
                "tier": tier,
                "title_id": None,
                "detail": f"Tiered group '{grp}' ({tier} Tier) had ZERO candidate releases across the {len(candidates_by_title)} searched titles"
            })

    # 2. Flag: Profile Blind Spot (AV1 or Tiered Group where top score < cutoff)
    for grp, gs in group_supply.items():
        if (gs["av1_appearances"] > 0 or gs["tier"] != "Untiered") and gs["passed_cutoff_count"] == 0:
            max_s = max(gs["scores"]) if gs["scores"] else 0
            flags.append({
                "kind": "PROFILE_BLIND_SPOT",
                "group": grp,
                "tier": gs["tier"],
                "title_id": None,
                "detail": f"Group appeared {gs['appearances']} times ({gs['av1_appearances']} AV1) but all releases fell below min cutoff (Max Score: {max_s})"
            })

    return group_supply, flags, title_evaluations, total_candidates_evaluated

# -----------------------------------------------------------------------------
# LIVE DATA HARVESTER (READ-ONLY SEARCHES)
# -----------------------------------------------------------------------------
def harvest_live_supply_sample(conn, tier_patterns):
    print("=" * 80, flush=True)
    print(f"HARVESTING PROSPECTIVE SUPPLY SAMPLE (Target: ~{SAMPLE_SIZE} titles)", flush=True)
    print("=" * 80, flush=True)
    
    # 1. PULL MOVIES (RADARR)
    movies = fetch_json(f"{RADARR_URL}/api/v3/movie", RADARR_API_KEY)
    
    target_movies_count = max(5, int(SAMPLE_SIZE * 0.7))
    target_tv_count = max(2, SAMPLE_SIZE - target_movies_count)
    
    # Stratified selection: mix of recent additions + catalog titles
    selected_movies = []
    if len(movies) <= target_movies_count:
        selected_movies = movies
    else:
        half = target_movies_count // 2
        recent = movies[-half:]
        catalog = movies[:(target_movies_count - half)]
        selected_movies = recent + catalog
        
    # 2. PULL TV SERIES & EPISODES (SONARR)
    series_list = fetch_json(f"{SONARR_URL}/api/v3/series", SONARR_API_KEY)
    selected_episodes = []
    
    for s in series_list[:target_tv_count]:
        s_id = s.get("id")
        if not s_id:
            continue
        ep_list = fetch_json(f"{SONARR_URL}/api/v3/episode?seriesId={s_id}", SONARR_API_KEY)
        # Select first standard episode (e.g. S01E01)
        std_eps = [e for e in ep_list if e.get("seasonNumber", 0) > 0 and e.get("episodeNumber", 0) > 0]
        if std_eps:
            ep = std_eps[0]
            ep["seriesTitle"] = s.get("title")
            selected_episodes.append(ep)

    candidates_by_title = []
    search_count = 0
    
    # Search Radarr Movies
    print(f"\nPerforming interactive candidate queries on {len(selected_movies)} movies...", flush=True)
    for m in selected_movies:
        m_id = m.get("id")
        search_count += 1
        print(f"  [{search_count}/{len(selected_movies) + len(selected_episodes)}] Querying Radarr candidates for Movie ID {m_id}...", flush=True)
        
        releases = fetch_json(f"{RADARR_URL}/api/v3/release?movieId={m_id}", RADARR_API_KEY)
        
        mf = m.get("movieFile") or {}
        curr_rel_path = mf.get("relativePath") or ""
        curr_group = extract_release_group(mf.get("releaseGroup"), relative_path=curr_rel_path)
        curr_score, _, _, _, _ = evaluate_release(conn, curr_rel_path, "Movies 2160p AV1 HQ", "radarr") if curr_rel_path else (0, 0, 0, False, [])
        
        candidates_by_title.append({
            "title_info": {"id": m_id, "type": "Movie", "title": m.get("title"), "year": m.get("year")},
            "arr_type": "radarr",
            "primary_profile": "Movies 2160p AV1 HQ",
            "runtime_mins": parse_runtime_minutes(mf.get("mediaInfo", {}).get("runTime"), default_minutes=m.get("runtime")),
            "current_file": {
                "group": curr_group,
                "size_gb": (mf.get("size") or 0) / (1024 ** 3),
                "is_av1": is_av1_release(curr_rel_path, tier_patterns["AV1"]),
                "score": curr_score,
                "file_name": curr_rel_path
            },
            "releases": releases
        })
        time.sleep(SEARCH_DELAY)

    # Search Sonarr Episodes
    print(f"\nPerforming interactive candidate queries on {len(selected_episodes)} TV episodes...", flush=True)
    for ep in selected_episodes:
        ep_id = ep.get("id")
        search_count += 1
        print(f"  [{search_count}/{len(selected_movies) + len(selected_episodes)}] Querying Sonarr candidates for Episode ID {ep_id}...", flush=True)
        
        releases = fetch_json(f"{SONARR_URL}/api/v3/release?episodeId={ep_id}", SONARR_API_KEY)
        
        candidates_by_title.append({
            "title_info": {"id": ep_id, "type": "TV", "title": ep.get("seriesTitle"), "season": ep.get("seasonNumber"), "episode": ep.get("episodeNumber")},
            "arr_type": "sonarr",
            "primary_profile": "TV 2160p AV1",
            "runtime_mins": None,
            "current_file": {},
            "releases": releases
        })
        time.sleep(SEARCH_DELAY)

    print(f"\nSuccessfully executed {search_count} interactive search queries with zero write/grab side-effects.\nScoring candidate releases locally...", flush=True)
    return candidates_by_title

# -----------------------------------------------------------------------------
# MARKDOWN REPORT EXPORT (GITIGNORED TELEMETRY)
# -----------------------------------------------------------------------------
def generate_supply_report(group_supply, flags, title_evaluations, total_evaluated, output_dir="telemetry"):
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.utcnow().strftime("%Y%m%d")
    report_path = os.path.join(output_dir, f"supply_quality_audit_{today_str}.md")
    
    total_titles = len(title_evaluations)
    total_av1_candidates = sum(g["av1_appearances"] for g in group_supply.values())
    
    lines = [
        f"# 📡 Supply-Side Search Audit & Prospective Telemetry Report",
        f"",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
        f"**Searched Sample Size:** {total_titles} Titles  ",
        f"**Total Candidates Evaluated:** {total_evaluated} releases  ",
        f"**AV1 Candidate Supply:** {total_av1_candidates}/{total_evaluated} ({total_av1_candidates/total_evaluated*100:.1f}%)  ",
        f"",
        f"> [!NOTE]",
        f"> **Supply Context:** Measures prospective indexer supply across live Usenet indexers under our PCD AV1 Quality Profiles. No releases were grabbed or modified during this audit.",
        f"",
        f"---",
        f"",
        f"## 1. Supply Contradiction Flags & Diagnostic Findings",
        f""
    ]
    
    if flags:
        lines.append(f"| Flag Kind | Group | Current Tier | Finding & Telemetry Detail |")
        lines.append(f"| :--- | :--- | :---: | :--- |")
        for f in flags:
            lines.append(f"| `{f['kind']}` | **{f['group']}** | `{f['tier']}` | {f['detail']} |")
    else:
        lines.append("✅ **No supply contradictions or blind spots detected across sample.**")
        
    lines.extend([
        f"",
        f"---",
        f"",
        f"## 2. Per-Group Supply Fingerprint & Win-Rate Roster",
        f"",
        f"| Group | Tier | Supply Count (% AV1) | Median Size | MB/min | Median Score | Win Rate (%) | Indexers |",
        f"| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])
    
    sorted_groups = sorted(group_supply.items(), key=lambda x: x[1]["appearances"], reverse=True)
    for grp, gs in sorted_groups:
        tier = gs["tier"]
        app = gs["appearances"]
        av1_app = gs["av1_appearances"]
        av1_pct = f"{av1_app/app*100:.0f}%" if app else "0%"
        med_sz = f"{statistics.median(gs['sizes_gb']):.2f} GB" if gs["sizes_gb"] else "-"
        mb_min = f"{statistics.median(gs['mb_per_min_vals']):.1f}" if gs["mb_per_min_vals"] else "-"
        med_sc = f"{statistics.median(gs['scores']):.0f}" if gs["scores"] else "-"
        win_pct = f"{gs['wins']/total_titles*100:.1f}% ({gs['wins']})" if total_titles else "0%"
        idx_count = len(gs["indexers"])
        
        lines.append(f"| **{grp}** | `{tier}` | {app} ({av1_pct}) | {med_sz} | {mb_min} | {med_sc} | {win_pct} | {idx_count} |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 3. Title-by-Title Candidate Winners vs Current Library File",
        f""
    ])
    
    for idx, te in enumerate(title_evaluations, 1):
        t_info = te["title_info"]
        top_c = te["top_candidate"]
        curr_f = te["current_file"]
        
        lines.append(f"### Sample Title #{idx}: {t_info.get('title')} ({t_info.get('type')})")
        lines.append(f"- **Total Candidates Available:** {te['total_candidates']}")
        if curr_f.get("file_name"):
            lines.append(f"- **Current File in Library:** `{curr_f.get('file_name')}` ({curr_f.get('size_gb', 0):.2f} GB, Group: **{curr_f.get('group')}**, Score: {curr_f.get('score', 0)})")
        else:
            lines.append(f"- **Current File in Library:** *None / Missing*")
            
        if top_c:
            lines.append(f"- **Top Scoring Candidate (PCD Winner):** `{top_c['title']}`")
            lines.append(f"  - Group: **{top_c['group']}** (`{top_c['tier']}`) | Score: **{top_c['score']}** | Size: {top_c['size_gb']:.2f} GB | AV1: `{top_c['is_av1']}` | Indexer: {top_c['indexer']}")
        else:
            lines.append(f"- **Top Scoring Candidate:** *No candidate cleared minimum score cutoff*")
        lines.append("")
        
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    return report_path

# -----------------------------------------------------------------------------
# CONSOLE SUMMARY (NO TITLES OUTPUTTED)
# -----------------------------------------------------------------------------
def print_console_summary(group_supply, flags, total_titles, total_evaluated, report_path):
    total_av1 = sum(g["av1_appearances"] for g in group_supply.values())
    
    print("\n" + "=" * 80)
    print("OP 912: SUPPLY-SIDE SEARCH AUDIT & TELEMETRY SUMMARY")
    print("=" * 80)
    print(f"Titles Searched              : {total_titles}")
    print(f"Candidate Releases Evaluated : {total_evaluated}")
    print(f"AV1 Candidates Available     : {total_av1} ({total_av1/total_evaluated*100:.1f}%)" if total_evaluated else "0")
    print(f"Non-AV1 Fallback Candidates  : {total_evaluated - total_av1}")
    print(f"Distinct Release Groups Found: {len(group_supply)}")
    
    print("\n--- Top Winning Groups by Grab Priority ---")
    winning_groups = [item for item in group_supply.items() if item[1]["wins"] > 0]
    for grp, gs in sorted(winning_groups, key=lambda x: x[1]["wins"], reverse=True):
        print(f"  - Group: {grp:<16} Tier: {gs['tier']:<8} Wins: {gs['wins']:>2} / {total_titles} ({gs['wins']/total_titles*100:.1f}%) | Median Score: {statistics.median(gs['scores']):>5.0f}")

    print("\n--- Supply Contradiction & Diagnostic Flags ---")
    if flags:
        for idx, flag in enumerate(flags, 1):
            print(f"  [{idx}] {flag['kind']:<28} Group: {flag['group']:<16} Tier: {flag['tier']:<8}")
            print(f"      Detail: {flag['detail']}")
    else:
        print("  [OK] Zero supply anomalies or blind spots detected.")
        
    print("\n" + "=" * 80)
    print(f"Full Private Prospective Report Written: {report_path}")
    print("=" * 80 + "\n")

# -----------------------------------------------------------------------------
# MAIN CLI
# -----------------------------------------------------------------------------
def main():
    get_required_env()
    conn = build_compiled_db()
    tier_patterns = load_tier_patterns_from_pcd()
    
    candidates_by_title = harvest_live_supply_sample(conn, tier_patterns)
    group_supply, flags, title_evaluations, total_evaluated = analyze_supply_candidates(
        candidates_by_title, conn, tier_patterns
    )
    
    report_path = generate_supply_report(group_supply, flags, title_evaluations, total_evaluated)
    print_console_summary(group_supply, flags, len(title_evaluations), total_evaluated, report_path)

if __name__ == "__main__":
    main()
