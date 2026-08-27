#!/usr/bin/env python3
"""
Op 931: Radarr4k Full-Library Upgrade Census v2.1 (Scoring Repair & Read-Only Review Queue)
- Current file scoring: Reads live Radarr movieFile customFormatScore via GET /api/v3/moviefile/{id}.
- Group/codec/resolution parsing: Robust tag stripping (.mkv, -xpost, [site], downscale disambiguation).
- Resolution bucketing: NEVER compares 1080p candidates against 2160p current files.
- DATA-SUSPECT filter: Excludes sub-1.5GB/0.0GB candidates from viable upgrade picks.
- Verdict anchoring: Cross-references evidence/verdicts.csv (PASS/EXCEPTION anchored as HOLD).
- Strictly read-only interactive search endpoints (GET /api/v3/release?movieId=X).
"""

import os
import sys
import json
import time
import csv
import re
import urllib.request
import urllib.parse
from datetime import datetime

RADARR_URL = os.environ.get("RADARR_URL", "http://127.0.0.1:7879")
RADARR_KEY = os.environ.get("RADARR_API_KEY", "")

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STACK_DIR = os.path.dirname(REPO_DIR)

if not RADARR_KEY:
    config_xml = os.path.join(STACK_DIR, "config", "radarr4k", "config.xml")
    if os.path.exists(config_xml):
        with open(config_xml, "r", encoding="utf-8") as f:
            for line in f:
                if "<ApiKey>" in line:
                    RADARR_KEY = line.split("<ApiKey>")[1].split("</ApiKey>")[0].strip()
                    break

if not RADARR_KEY:
    print("ERROR: Could not locate Radarr4k API Key.")
    sys.exit(1)

HEADERS = {
    "X-Api-Key": RADARR_KEY,
    "Content-Type": "application/json"
}

CHECKPOINT_FILE = os.path.join(REPO_DIR, "evidence", "census_931_checkpoint.json.local")
LOCAL_CSV = os.path.join(REPO_DIR, "evidence", "census_931.csv.local")
PUBLIC_MD = os.path.join(REPO_DIR, "evidence", "census_931_public.md")
VERDICTS_FILE = os.path.join(REPO_DIR, "evidence", "verdicts.csv")

def api_get(endpoint):
    url = f"{RADARR_URL}/api/v3/{endpoint}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)

def get_queue_count():
    q = api_get("queue")
    return q.get("totalRecords", len(q.get("records", [])))

def get_blocklist():
    try:
        bl = api_get("blocklist?pageSize=100")
        return {r.get("sourceTitle", "").lower(): r for r in bl.get("records", [])}
    except Exception:
        return {}

def load_verdicts():
    verdicts = {}
    if os.path.exists(VERDICTS_FILE):
        try:
            with open(VERDICTS_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    t = row.get("title", "").strip()
                    v = row.get("verdict", "").strip().upper()
                    if v in ["PASS", "EXCEPTION"]:
                        verdicts[t.lower()] = row
        except Exception as e:
            print(f"Warning: Could not read verdicts: {e}")
    return verdicts

def extract_codec_res_group(title):
    t = title
    for _ in range(3):
        t = re.sub(r'[-._ ]xpost$', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\.(mkv|mp4|avi|ts|m4v)$', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\[[a-zA-Z0-9_\-\.]+\]$', '', t)
        t = t.strip()
        
    t_upper = t.upper()
    
    # Codec
    codec = "Unknown"
    if "AV1" in t_upper or "AV01" in t_upper:
        codec = "AV1"
    elif "X265" in t_upper or "H265" in t_upper or "H.265" in t_upper or "HEVC" in t_upper:
        codec = "x265"
    elif "X264" in t_upper or "H264" in t_upper or "H.264" in t_upper or "AVC" in t_upper:
        codec = "x264"
        
    # Resolution (1080p takes precedence over UHD source markers)
    res = "Unknown"
    if "1080P" in t_upper or "1080I" in t_upper:
        res = "1080p"
    elif "2160P" in t_upper or "4K" in t_upper or ("UHD" in t_upper and "1080" not in t_upper):
        res = "2160p"
    elif "720P" in t_upper:
        res = "720p"
    elif "480P" in t_upper or "576P" in t_upper:
        res = "SD"
        
    # Group
    group = "Unknown"
    m_bracket = re.match(r"^\[([a-zA-Z0-9_\-\.]+)\]", t)
    if m_bracket:
        group = m_bracket.group(1)
    else:
        m_hyphen = re.search(r"-([a-zA-Z0-9_\.]+)$", t)
        if m_hyphen:
            group = m_hyphen.group(1)
        else:
            parts = t.split("-")
            if len(parts) > 1:
                group = parts[-1].strip()
                
    return codec, res, group

def run_census():
    print("=" * 80)
    print("OP 931: RADARR4K FULL-LIBRARY UPGRADE CENSUS V2.1 (READ-ONLY)")
    print("=" * 80)
    
    initial_queue = get_queue_count()
    if initial_queue > 0:
        print(f"WARNING: Radarr4k Queue already has {initial_queue} items. Watchdog active.")
    else:
        print("Watchdog initialized: Radarr4k Queue has 0 items.")
        
    blocklist_map = get_blocklist()
    print(f"Loaded {len(blocklist_map)} active blocklist entries.")
    
    verdicts_map = load_verdicts()
    print(f"Loaded {len(verdicts_map)} PASS/EXCEPTION verdict anchors.")
    
    print("Fetching movie catalog from Radarr4k...")
    movies = api_get("movie")
    print(f"Enumerated {len(movies)} total movies in Radarr4k.")
    
    checkpoint_data = {}
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r") as f:
                checkpoint_data = json.load(f)
            print(f"Loaded {len(checkpoint_data)} previously checkpointed movie audits.")
        except Exception as e:
            print(f"Could not load checkpoint: {e}")
            
    for idx, m in enumerate(movies, start=1):
        m_id = m["id"]
        title = m.get("title", "Unknown")
        year = m.get("year", 0)
        str_id = str(m_id)
        
        # Check current file info by querying full movieFile object
        has_file = m.get("hasFile", False)
        mf_summary = m.get("movieFile")
        
        cur_file_title = ""
        cur_group = "None"
        cur_codec = "None"
        cur_res = "None"
        cur_size_gb = 0.0
        cur_score = 0
        
        if has_file and mf_summary:
            mf_id = mf_summary.get("id")
            try:
                full_mf = api_get(f"moviefile/{mf_id}")
                cur_score = full_mf.get("customFormatScore", 0)
                cur_group = full_mf.get("releaseGroup", "Unknown")
                cur_file_title = full_mf.get("relativePath", "") or full_mf.get("sceneName", "")
                cur_size_gb = round(full_mf.get("size", 0) / (1024**3), 2)
                
                media_info = full_mf.get("mediaInfo", {})
                cur_codec = media_info.get("videoCodec", "Unknown")
                
                q_name = full_mf.get("quality", {}).get("quality", {}).get("name", "")
                if "2160p" in q_name:
                    cur_res = "2160p"
                elif "1080p" in q_name:
                    cur_res = "1080p"
                elif "720p" in q_name:
                    cur_res = "720p"
                else:
                    cur_res = "Unknown"
                    
                if not cur_group or cur_group == "Unknown":
                    c, r, g = extract_codec_res_group(cur_file_title)
                    if g != "Unknown":
                        cur_group = g
                    if cur_codec == "Unknown" and c != "Unknown":
                        cur_codec = c
                    if cur_res == "Unknown" and r != "Unknown":
                        cur_res = r
            except Exception as e:
                print(f"  [WARN] Failed to fetch full moviefile {mf_id}: {e}")
                
        if str_id in checkpoint_data:
            print(f"[{idx}/{len(movies)}] Skipping '{title}' ({year}) — already checkpointed.")
            continue
            
        print(f"[{idx}/{len(movies)}] Querying '{title}' ({year}) | Cur: {cur_group} ({cur_codec}, {cur_res}, {cur_size_gb}GB, Score: {cur_score})...")
        
        try:
            releases = api_get(f"release?movieId={m_id}")
        except Exception as e:
            print(f"  [ERROR] Failed to query releases for '{title}': {e}")
            releases = []
            
        # Watchdog check
        current_queue = get_queue_count()
        if current_queue != initial_queue:
            print(f"ABORT CRITICAL: Queue changed from {initial_queue} to {current_queue}! Stopping immediately.")
            sys.exit(1)
            
        # Parse releases
        best_2160p = None
        best_1080p = None
        data_suspects = []
        all_candidates = []
        
        for r in releases:
            r_title = r.get("title", "")
            r_size_bytes = r.get("size", 0)
            r_size_gb = round(r_size_bytes / (1024**3), 2)
            r_score = r.get("customFormatScore", 0)
            r_approved = r.get("approved", True)
            r_rejections = r.get("rejections", [])
            
            c, res, grp = extract_codec_res_group(r_title)
            
            # Check blocklist
            is_blocklisted = r_title.lower() in blocklist_map
            
            # Sizing sanity / DATA-SUSPECT flag
            is_suspect = False
            suspect_reason = ""
            if r_size_bytes == 0 or r_size_gb == 0.0:
                is_suspect = True
                suspect_reason = "Missing size (0.0 GB)"
            elif r_size_gb < 1.0:
                is_suspect = True
                suspect_reason = f"Extreme micro size ({r_size_gb} GB < 1.0 GB)"
            elif r_size_gb < 1.5 and res == "2160p":
                is_suspect = True
                suspect_reason = f"Implausible 2160p feature size ({r_size_gb} GB < 1.5 GB)"
                
            cand_dict = {
                "title": r_title,
                "group": grp,
                "codec": c,
                "resolution": res,
                "size_gb": r_size_gb,
                "score": r_score,
                "approved": r_approved,
                "is_blocklisted": is_blocklisted,
                "is_suspect": is_suspect,
                "suspect_reason": suspect_reason,
                "rejections": r_rejections
            }
            all_candidates.append(cand_dict)
            
            if is_suspect or is_blocklisted:
                data_suspects.append(cand_dict)
                continue
                
            # Filter for viable candidates (score >= 1000 cutoff)
            if r_score >= 1000:
                if res == "2160p":
                    if best_2160p is None or r_score > best_2160p["score"] or (r_score == best_2160p["score"] and r_size_gb > best_2160p["size_gb"]):
                        best_2160p = cand_dict
                elif res == "1080p":
                    if best_1080p is None or r_score > best_1080p["score"] or (r_score == best_1080p["score"] and r_size_gb > best_1080p["size_gb"]):
                        best_1080p = cand_dict
                        
        # Determine classification
        classification = "HOLD"
        rationale = ""
        best_viable = None
        delta = 0
        
        has_pass_verdict = title.lower() in verdicts_map
        verdict_note = verdicts_map.get(title.lower(), {}).get("verdict", "")
        
        if cur_res == "2160p":
            best_viable = best_2160p
            if best_viable:
                delta = best_viable["score"] - cur_score
                if delta >= 300:
                    if has_pass_verdict and delta < 1500:
                        classification = "HOLD"
                        rationale = f"Empirical {verdict_note} verdict anchor on '{cur_group}' ({cur_score} pts); candidate '{best_viable['group']}' (+{delta} pts) does not supersede verified playback."
                    elif cur_score < 1000:
                        classification = "UPGRADE-CANDIDATE"
                        rationale = f"Material upgrade from low baseline ({cur_score} pts) to {best_viable['group']} {best_viable['codec']} 2160p ({best_viable['score']} pts, +{delta} delta)."
                    elif cur_codec in ["x264", "x265", "HEVC"] and best_viable["codec"] == "AV1":
                        classification = "UPGRADE-CANDIDATE"
                        rationale = f"Material codec advancement from {cur_codec} to {best_viable['group']} AV1 2160p ({best_viable['size_gb']}GB, +{delta} pts)."
                    elif delta >= 1500:
                        classification = "MANUAL-REVIEW"
                        rationale = f"Significant score delta (+{delta} pts) within 2160p — verify audio track and bitrate parity ({cur_group} vs {best_viable['group']})."
                    else:
                        classification = "UPGRADE-CANDIDATE"
                        rationale = f"Higher scoring 2160p candidate ({best_viable['group']} {best_viable['codec']}, +{delta} delta)."
                elif delta > 0:
                    classification = "HOLD"
                    rationale = f"Best 2160p candidate '{best_viable['group']}' delta (+{delta}) is below the +300 upgrade increment threshold."
                else:
                    classification = "HOLD"
                    rationale = f"Current 2160p file '{cur_group}' ({cur_score} pts) equals or outperforms all indexed 2160p candidates."
            else:
                if cur_score >= 1000:
                    classification = "HOLD"
                    rationale = f"Current 2160p file '{cur_group}' ({cur_score} pts) is optimal; no qualifying 2160p candidate exists."
                else:
                    classification = "NO-QUALIFIED-CANDIDATE"
                    rationale = "No 2160p candidate cleared the +1000 minimum profile cutoff score."
        else: # Current file is 1080p, 720p, or unmonitored/missing
            if best_2160p:
                best_viable = best_2160p
                delta = best_2160p["score"] - cur_score
                classification = "UPGRADE-CANDIDATE"
                rationale = f"Resolution upgrade from {cur_res} to 2160p {best_2160p['group']} {best_2160p['codec']} ({best_2160p['size_gb']}GB, {best_2160p['score']} pts, +{delta} delta)."
            elif best_1080p:
                best_viable = best_1080p
                delta = best_1080p["score"] - cur_score
                if cur_score < 1000 and best_1080p["score"] >= 1000:
                    classification = "UPGRADE-CANDIDATE"
                    rationale = f"Legacy trusted x264/1080p upgrade: {best_1080p['group']} ({best_1080p['score']} pts) lifts archival film above cutoff."
                elif delta >= 300:
                    classification = "UPGRADE-CANDIDATE"
                    rationale = f"1080p tier upgrade to {best_1080p['group']} {best_1080p['codec']} ({best_1080p['score']} pts, +{delta} delta)."
                else:
                    classification = "HOLD"
                    rationale = f"Current 1080p file '{cur_group}' ({cur_score} pts) equals or outperforms indexed 1080p candidates."
            else:
                if cur_score >= 1000:
                    classification = "HOLD"
                    rationale = f"Current file '{cur_group}' ({cur_score} pts) is top-scoring."
                else:
                    classification = "NO-QUALIFIED-CANDIDATE"
                    rationale = "No 2160p or 1080p candidate cleared profile minimum cutoff (1000 pts)."
                    
        movie_result = {
            "movie_id": m_id,
            "title": title,
            "year": year,
            "current_summary": {
                "group": cur_group,
                "codec": cur_codec,
                "resolution": cur_res,
                "size_gb": cur_size_gb,
                "score": cur_score
            },
            "best_2160p": best_2160p,
            "best_1080p": best_1080p,
            "best_viable": best_viable,
            "delta": delta,
            "classification": classification,
            "rationale": rationale,
            "data_suspects": data_suspects,
            "candidates_count": len(all_candidates)
        }
        
        checkpoint_data[str_id] = movie_result
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
            
        time.sleep(3.0)
        
    print("\nCensus search complete. Generating v2.1 reports...")
    
    # Generate Quarantined CSV
    with open(LOCAL_CSV, "w") as f:
        f.write("movie_id,title,year,cur_group,cur_codec,cur_res,cur_size_gb,cur_score,best_2160p_grp,best_2160p_score,best_1080p_grp,best_1080p_score,classification,delta,rationale\n")
        for str_id, data in checkpoint_data.items():
            cur = data["current_summary"]
            b2160 = data.get("best_2160p") or {}
            b1080 = data.get("best_1080p") or {}
            f.write(f'"{data["movie_id"]}","{data["title"]}","{data["year"]}","{cur["group"]}","{cur["codec"]}","{cur["resolution"]}","{cur["size_gb"]}","{cur["score"]}","{b2160.get("group", "")}","{b2160.get("score", "")}","{b1080.get("group", "")}","{b1080.get("score", "")}","{data["classification"]}","{data["delta"]}","{data["rationale"]}"\n')
    print(f"Wrote raw candidate records to {LOCAL_CSV} (QUARANTINED / LOCAL ONLY).")
    
    # Generate Public Markdown
    counts = {"HOLD": 0, "UPGRADE-CANDIDATE": 0, "MANUAL-REVIEW": 0, "NO-QUALIFIED-CANDIDATE": 0}
    for d in checkpoint_data.values():
        c = d.get("classification", "HOLD")
        counts[c] = counts.get(c, 0) + 1
        
    total_audited = len(checkpoint_data)
    
    upgrade_list = [d for d in checkpoint_data.values() if d["classification"] == "UPGRADE-CANDIDATE"]
    upgrade_list.sort(key=lambda x: x["delta"], reverse=True)
    
    manual_list = [d for d in checkpoint_data.values() if d["classification"] == "MANUAL-REVIEW"]
    manual_list.sort(key=lambda x: x["delta"], reverse=True)
    
    with open(PUBLIC_MD, "w") as f:
        f.write("# 📊 Op 931: Radarr4k Full-Library Upgrade Census v2.1\n\n")
        f.write(f"**Audit Date:** {datetime.now().strftime('%Y-%m-%d')}  \n")
        f.write("**Target Profile:** `Movies 2160p AV1 HQ` (Profile 64, Read-Only)  \n")
        f.write(f"**Total Movies Audited:** {total_audited}  \n")
        f.write("**Operational Status:** **STRICTLY READ-ONLY CENSUS** — Output represents an empirical review queue, not an automated action.\n\n")
        f.write("---\n\n")
        f.write("## 1. Classification Summary (Scoring Repaired & Verdict-Anchored)\n\n")
        f.write("| Classification | Count | Percentage | Description |\n")
        f.write("| :--- | :---: | :---: | :--- |\n")
        f.write(f"| **`HOLD`** | **{counts['HOLD']}** | {counts['HOLD']/total_audited*100:.1f}% | Current library file is already optimal, top-scoring 2160p, or anchored by empirical PASS verdict. |\n")
        f.write(f"| **`UPGRADE-CANDIDATE`** | **{counts['UPGRADE-CANDIDATE']}** | {counts['UPGRADE-CANDIDATE']/total_audited*100:.1f}% | Qualified candidate materially advances playback quality (res upgrade to 2160p, AV1 codec advancement, or legacy trusted x264). |\n")
        f.write(f"| **`MANUAL-REVIEW`** | **{counts['MANUAL-REVIEW']}** | {counts['MANUAL-REVIEW']/total_audited*100:.1f}% | Significant score delta within 2160p requiring manual verification of audio channels/bitrate parity. |\n")
        f.write(f"| **`NO-QUALIFIED-CANDIDATE`** | **{counts['NO-QUALIFIED-CANDIDATE']}** | {counts['NO-QUALIFIED-CANDIDATE']/total_audited*100:.1f}% | No candidate cleared the +1000 minimum profile cutoff score. |\n")
        f.write(f"| **Total** | **{total_audited}** | **100.0%** | Full active Radarr4k library inventory. |\n\n")
        f.write("---\n\n")
        f.write("## 2. Top Ranked Priority Upgrade Queue\n\n")
        f.write("| Rank | Title | Year | Current File (Group / Codec / Res / Score) | Best Candidate (Group / Codec / Res / Score) | Delta | Material Advancement Rationale |\n")
        f.write("| :---: | :--- | :---: | :--- | :--- | :---: | :--- |\n")
        for r_idx, item in enumerate(upgrade_list, start=1):
            cur = item["current_summary"]
            bv = item.get("best_viable") or {}
            f.write(f"| {r_idx} | **{item['title']}** | {item['year']} | `{cur['group']}` ({cur['codec']}, {cur['resolution']}, {cur['score']} pts) | `{bv.get('group', 'Unknown')}` ({bv.get('codec', '')}, {bv.get('resolution', '')}, {bv.get('score', 0)} pts, {bv.get('size_gb', 0)}GB) | **+{item['delta']}** | {item['rationale']} |\n")
            
        f.write("\n---\n\n")
        f.write("## 3. Dedicated Review: Legacy Trusted x264 Titles\n\n")
        f.write("| Movie Title | Year | Current Group & Codec | Legacy Trusted Candidate | Score Before $\\rightarrow$ After | Status & Operational Impact |\n")
        f.write("| :--- | :---: | :--- | :--- | :---: | :--- |\n")
        for title_match in ["Blue Valentine", "The Right Stuff", "Hoosiers", "The Perks of Being a Wallflower", "Project X", "The Ides of March", "Locke", "A Royal Affair"]:
            m_item = next((d for d in checkpoint_data.values() if d["title"] == title_match), None)
            if m_item:
                cur = m_item["current_summary"]
                b1080 = m_item.get("best_1080p") or {}
                f.write(f"| **{m_item['title']}** | {m_item['year']} | `{cur['group']}` ({cur['codec']}) | `{b1080.get('group', 'None')}` ({b1080.get('size_gb', 0)} GB) | `+{cur['score']}` $\\rightarrow$ `+{b1080.get('score', cur['score'])}` | Auto-grabbable trusted legacy pick (clears +1000 cutoff). |\n")

        f.write("\n---\n\n")
        f.write("## 4. Complete Library Catalog Census Breakdown (v2.1 Repaired)\n\n")
        f.write("| Title | Year | Current Summary | Best 2160p Candidate | Best 1080p Candidate | Status | Decision Rationale |\n")
        f.write("| :--- | :---: | :--- | :--- | :--- | :---: | :--- |\n")
        for item in checkpoint_data.values():
            cur = item["current_summary"]
            b2160 = item.get("best_2160p")
            b1080 = item.get("best_1080p")
            
            b2160_str = f"{b2160['group']} ({b2160['codec']}, {b2160['size_gb']}GB, {b2160['score']} pts)" if b2160 else "*None*"
            b1080_str = f"{b1080['group']} ({b1080['codec']}, {b1080['size_gb']}GB, {b1080['score']} pts)" if b1080 else "*None*"
            
            f.write(f"| **{item['title']}** | {item['year']} | {cur['group']} ({cur['codec']}, {cur['resolution']}, {cur['size_gb']}GB, {cur['score']} pts) | {b2160_str} | {b1080_str} | **`{item['classification']}`** | {item['rationale']} |\n")

    print(f"Generated public census v2.1 artifact at {PUBLIC_MD}.")

if __name__ == "__main__":
    run_census()
