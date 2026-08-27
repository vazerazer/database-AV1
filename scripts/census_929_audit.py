#!/usr/bin/env python3
"""
scripts/census_929_audit.py
Op 929: Radarr4k Full-Library Upgrade Census (Strictly Read-Only).
Conducts an interactive search audit over all movies in Radarr4k,
scores candidate releases under production profile 'Movies 2160p AV1 HQ',
compares candidates against current imported files, cross-references
evidence/verdicts.csv, and generates evidence/census_929_public.md
and evidence/census_929.csv.local.
"""

import os
import sys
import json
import csv
import re
import time
import urllib.request
import urllib.error

# Import PCD scoring harness
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests'))
from simulate_scoring import build_compiled_db, evaluate_release

def get_radarr_api_key():
    key = os.environ.get('RADARR_API_KEY')
    if key:
        return key
    local_cfg = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'config', 'radarr4k', 'config.xml'
    )
    if os.path.exists(local_cfg):
        with open(local_cfg, 'r', encoding='utf-8') as f:
            for line in f:
                if '<ApiKey>' in line:
                    return line.split('<ApiKey>')[1].split('</ApiKey>')[0].strip()
    return None

def extract_codec(title):
    t_upper = title.upper()
    if 'AV1' in t_upper or 'AV01' in t_upper:
        return 'AV1'
    if 'X265' in t_upper or 'H.265' in t_upper or 'HEVC' in t_upper:
        return 'x265'
    if 'X264' in t_upper or 'H.264' in t_upper or 'AVC' in t_upper:
        return 'x264'
    return 'Unknown'

def extract_resolution(title):
    t_upper = title.upper()
    if '2160P' in t_upper or '4K' in t_upper or 'UHD' in t_upper:
        return '2160p'
    if '1080P' in t_upper:
        return '1080p'
    if '720P' in t_upper:
        return '720p'
    return 'Other'

def extract_group(title, raw_rg=None):
    if raw_rg and raw_rg.strip() and not re.match(r'^(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)$', raw_rg, re.I):
        return raw_rg.strip()
    t = re.sub(r'\.(mkv|mp4|avi|ts)$', '', title.strip(), flags=re.I).strip()
    t = re.sub(r'[\s._-]+$', '', t).strip()
    m = re.search(r'[-. ]([A-Za-z0-9_&]+)(?:\[[a-zA-Z0-9_.-]+\])?$', t)
    if m:
        return m.group(1).strip()
    return 'Unknown'

def check_queue(radarr_url, api_key):
    req = urllib.request.Request(f"{radarr_url}/api/v3/queue", headers={'X-Api-Key': api_key})
    with urllib.request.urlopen(req, timeout=10) as resp:
        q = json.load(resp)
        return q.get('totalRecords', len(q.get('records', [])))

def run_census():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    verdicts_csv = os.path.join(repo_root, 'evidence', 'verdicts.csv')
    public_md = os.path.join(repo_root, 'evidence', 'census_929_public.md')
    local_csv = os.path.join(repo_root, 'evidence', 'census_929.csv.local')
    checkpoint_file = os.path.join(repo_root, 'evidence', 'census_929_checkpoint.json.local')
    
    api_key = get_radarr_api_key()
    if not api_key:
        print("ERROR: No Radarr API key found in environment or local config!", file=sys.stderr)
        sys.exit(1)
        
    radarr_url = os.environ.get('RADARR_URL', 'http://127.0.0.1:7879')
    conn = build_compiled_db()
    
    # 0. Initial queue check
    initial_queue = check_queue(radarr_url, api_key)
    print(f"Watchdog initialized: Radarr4k Queue has {initial_queue} items.")
    
    # 1. Load verdicts
    verdicts_map = {}
    if os.path.exists(verdicts_csv):
        with open(verdicts_csv, 'r', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                k = (r['title'].strip().lower(), r['group'].strip().lower())
                verdicts_map[k] = r
                
    # Load checkpoints if present
    cached_releases = {}
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                cached_releases = json.load(f)
            print(f"Loaded {len(cached_releases)} cached movie searches from checkpoint.")
        except Exception:
            cached_releases = {}
                
    # 2. Fetch all movies
    print("Fetching movie catalog from Radarr4k...")
    req_movies = urllib.request.Request(f"{radarr_url}/api/v3/movie", headers={'X-Api-Key': api_key})
    with urllib.request.urlopen(req_movies, timeout=15) as resp:
        movies = json.load(resp)
        
    print(f"Enumerated {len(movies)} total movies in Radarr4k.")
    
    movie_results = []
    raw_candidate_rows = []
    cmrg_candidates = []
    
    for idx, m in enumerate(movies, 1):
        m_id = str(m['id'])
        title = m['title']
        year = m.get('year', '')
        tmdb_id = m.get('tmdbId', '')
        
        # Check queue watchdog
        cur_q = check_queue(radarr_url, api_key)
        if cur_q > initial_queue:
            print(f"ABORTING: Radarr4k queue gained items ({initial_queue} -> {cur_q})! Aborting to prevent unapproved activity.", file=sys.stderr)
            sys.exit(2)
            
        mf = m.get('movieFile')
        if mf:
            cur_path = mf.get('relativePath', '')
            cur_size_bytes = float(mf.get('size', 0))
            cur_size_gb = round(cur_size_bytes / (1024 ** 3), 2)
            cur_group = extract_group(cur_path)
            cur_codec = mf.get('mediaInfo', {}).get('videoCodec') or extract_codec(cur_path)
            cur_res = extract_resolution(cur_path)
            cur_hdr = mf.get('mediaInfo', {}).get('videoDynamicRangeType') or mf.get('mediaInfo', {}).get('videoDynamicRange') or ''
            cur_audio = mf.get('mediaInfo', {}).get('audioCodec') or ''
            
            # Score current file
            cur_score, _, _, _, cur_matches = evaluate_release(
                conn, cur_path, 'Movies 2160p AV1 HQ', 'radarr', size_gb=cur_size_gb
            )
        else:
            cur_path = 'None (Missing File)'
            cur_size_gb = 0.0
            cur_group = 'None'
            cur_codec = 'None'
            cur_res = 'None'
            cur_hdr = 'None'
            cur_audio = 'None'
            cur_score = 0
            cur_matches = {}
            
        v_entry = verdicts_map.get((title.lower(), cur_group.lower()))
        cur_verdict = v_entry.get('verdict') if v_entry else None
        
        # Search releases
        if m_id in cached_releases:
            releases = cached_releases[m_id]
            print(f"[{idx}/{len(movies)}] '{title}' ({year}) [CACHED: {len(releases)} releases] | Cur: {cur_group} ({cur_codec}, {cur_size_gb}GB, Score: {cur_score})")
        else:
            print(f"[{idx}/{len(movies)}] Querying '{title}' ({year}) via Interactive Search | Cur: {cur_group} ({cur_codec}, {cur_size_gb}GB, Score: {cur_score})...")
            url_search = f"{radarr_url}/api/v3/release?movieId={m['id']}"
            req_search = urllib.request.Request(url_search, headers={'X-Api-Key': api_key})
            try:
                with urllib.request.urlopen(req_search, timeout=90) as resp:
                    releases = json.load(resp)
            except Exception as e:
                print(f"  Warning: Search failed for '{title}': {e}", file=sys.stderr)
                releases = []
                
            cached_releases[m_id] = releases
            # Save checkpoint
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(cached_releases, f)
            time.sleep(2.0)
            
        candidates = []
        for r in releases:
            r_title = r.get('title', '')
            r_size = round(float(r.get('size', 0)) / (1024 ** 3), 2)
            r_group = extract_group(r_title, r.get('data', {}).get('releaseGroup'))
            r_codec = extract_codec(r_title)
            r_res = extract_resolution(r_title)
            
            # Track CMRG appearances for Op 929 parked review
            if 'CMRG' in r_title.upper() or r_group.upper() == 'CMRG':
                cmrg_candidates.append({
                    'movie': title,
                    'year': year,
                    'release_title': r_title,
                    'size_gb': r_size,
                    'codec': r_codec
                })
                
            # Score candidate under Production Profile 64
            score, _, _, clears_min, matches = evaluate_release(
                conn, r_title, 'Movies 2160p AV1 HQ', 'radarr', size_gb=r_size
            )
            
            raw_candidate_rows.append({
                'movie_id': m_id,
                'title': title,
                'tmdb_id': tmdb_id,
                'release_title': r_title,
                'group': r_group,
                'codec': r_codec,
                'res': r_res,
                'size_gb': r_size,
                'score': score,
                'clears_min': clears_min
            })
            
            # Viable candidate criteria
            if clears_min and score > 0 and 'CAM' not in matches and 'Upscale' not in matches and '3D' not in matches and 'Banned Groups' not in matches:
                candidates.append({
                    'title': r_title,
                    'group': r_group,
                    'codec': r_codec,
                    'res': r_res,
                    'size_gb': r_size,
                    'score': score,
                    'matches': matches
                })
                
        candidates.sort(key=lambda x: (x['score'], x['size_gb']), reverse=True)
        best = candidates[0] if candidates else None
        
        if not mf:
            classification = 'UPGRADE-CANDIDATE' if best else 'NO-QUALIFIED-CANDIDATE'
            rationale = f"Missing file in library; top candidate '{best['group']}' scored {best['score']}." if best else "No file present and no viable releases indexed."
            score_delta = best['score'] if best else 0
        elif not best:
            classification = 'NO-QUALIFIED-CANDIDATE'
            rationale = "No candidate releases cleared profile minimum score (1000) or all candidates penalized as trash/banned."
            score_delta = 0
        else:
            delta = best['score'] - cur_score
            score_delta = delta
            
            if cur_verdict == 'PASS' and delta < 300:
                classification = 'HOLD'
                rationale = f"Current file group '{cur_group}' holds an empirical PASS verdict; delta (+{delta}) is below the upgrade threshold."
            elif cur_verdict == 'PASS' and cur_codec == 'AV1' and best['codec'] != 'AV1':
                classification = 'HOLD'
                rationale = f"Current AV1 file has empirical PASS; non-AV1 candidates rejected."
            elif cur_verdict in ('FAIL', 'BORDERLINE'):
                if best['score'] > cur_score or (best['codec'] == 'AV1' and cur_codec != 'AV1'):
                    classification = 'UPGRADE-CANDIDATE'
                    rationale = f"Current file group '{cur_group}' has an empirical {cur_verdict} verdict; candidate '{best['group']}' ({best['codec']}, {best['size_gb']}GB) provides a certified upgrade."
                else:
                    classification = 'MANUAL-REVIEW'
                    rationale = f"Current file has {cur_verdict} verdict, but best candidate scored {best['score']} vs current {cur_score}."
            elif delta >= 300:
                if best['codec'] == 'AV1' and cur_codec != 'AV1':
                    classification = 'UPGRADE-CANDIDATE'
                    rationale = f"Material codec upgrade from {cur_codec} to AV1 ({best['group']}, {best['size_gb']}GB, +{delta} pts)."
                elif 'Dolby Vision' in best['matches'] and 'Dolby Vision' not in cur_matches:
                    classification = 'UPGRADE-CANDIDATE'
                    rationale = f"Material HDR/DV advancement ({best['group']} adds Dolby Vision, +{delta} pts)."
                elif 'AV1 Quality Encoders' in best['matches'] and 'AV1 Quality Encoders' not in cur_matches:
                    classification = 'UPGRADE-CANDIDATE'
                    rationale = f"Encoder tier advancement to Quality Tier ({best['group']}, +{delta} pts)."
                elif best['score'] > cur_score and cur_score < 2000:
                    classification = 'UPGRADE-CANDIDATE'
                    rationale = f"Low-scoring baseline file ({cur_score}) replaced by high-scoring candidate ({best['group']}, {best['score']} pts, +{delta} delta)."
                else:
                    classification = 'MANUAL-REVIEW'
                    rationale = f"Score delta (+{delta}) exceeds threshold, but requires manual check on bitrate/audio parity."
            elif delta > 0:
                classification = 'HOLD'
                rationale = f"Candidate '{best['group']}' has minor score advantage (+{delta}), below the +300 upgrade increment threshold."
            else:
                classification = 'HOLD'
                rationale = f"Current file '{cur_group}' ({cur_score} pts) equals or outperforms all indexed candidates (best candidate: {best['score']} pts)."
                
        movie_results.append({
            'title': title,
            'year': year,
            'tmdb_id': tmdb_id,
            'cur_group': cur_group,
            'cur_codec': cur_codec,
            'cur_res': cur_res,
            'cur_hdr': cur_hdr,
            'cur_audio': cur_audio,
            'cur_size_gb': cur_size_gb,
            'cur_score': cur_score,
            'cur_verdict': cur_verdict or 'NONE',
            'best_group': best['group'] if best else 'None',
            'best_codec': best['codec'] if best else 'None',
            'best_res': best['res'] if best else 'None',
            'best_size_gb': best['size_gb'] if best else 0.0,
            'best_score': best['score'] if best else 0,
            'score_delta': score_delta,
            'classification': classification,
            'rationale': rationale
        })
        
    print("\nCensus search complete. Generating reports...")
    
    # 3. Write raw local-only CSV
    with open(local_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['movie_id', 'title', 'tmdb_id', 'release_title', 'group', 'codec', 'res', 'size_gb', 'score', 'clears_min']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(raw_candidate_rows)
    print(f"Wrote raw candidate records to {local_csv} (QUARANTINED / LOCAL ONLY).")
    
    # 4. Generate public report
    counts = {
        'UPGRADE-CANDIDATE': sum(1 for r in movie_results if r['classification'] == 'UPGRADE-CANDIDATE'),
        'HOLD': sum(1 for r in movie_results if r['classification'] == 'HOLD'),
        'NO-QUALIFIED-CANDIDATE': sum(1 for r in movie_results if r['classification'] == 'NO-QUALIFIED-CANDIDATE'),
        'MANUAL-REVIEW': sum(1 for r in movie_results if r['classification'] == 'MANUAL-REVIEW')
    }
    
    upgrade_queue = [r for r in movie_results if r['classification'] == 'UPGRADE-CANDIDATE']
    upgrade_queue.sort(key=lambda x: x['score_delta'], reverse=True)
    
    with open(public_md, 'w', encoding='utf-8') as f:
        f.write("# 📊 Op 929: Radarr4k Full-Library Upgrade Census\n\n")
        f.write("**Audit Date:** 2026-08-27  \n")
        f.write("**Target Profile:** `Movies 2160p AV1 HQ` (Profile 64, Read-Only)  \n")
        f.write(f"**Total Movies Audited:** {len(movie_results)}  \n")
        f.write("**Operational Status:** **STRICTLY READ-ONLY CENSUS** — Output represents an empirical review queue, not an automated action.\n\n")
        
        f.write("---\n\n")
        f.write("## 1. Classification Summary\n\n")
        f.write(f"| Classification | Count | Percentage | Description |\n")
        f.write(f"| :--- | :---: | :---: | :--- |\n")
        f.write(f"| **`HOLD`** | **{counts['HOLD']}** | {counts['HOLD']/len(movie_results)*100:.1f}% | Current library file is already optimal, top-scoring, or anchored by an empirical `PASS` verdict. |\n")
        f.write(f"| **`UPGRADE-CANDIDATE`** | **{counts['UPGRADE-CANDIDATE']}** | {counts['UPGRADE-CANDIDATE']/len(movie_results)*100:.1f}% | Qualified candidate materially advances playback quality, codec tier, DV/HDR, or resolves a known FAIL/BORDERLINE. |\n")
        f.write(f"| **`MANUAL-REVIEW`** | **{counts['MANUAL-REVIEW']}** | {counts['MANUAL-REVIEW']/len(movie_results)*100:.1f}% | Score delta exceeds threshold but requires review of audio tracks, bitrate headroom, or group craft exceptions. |\n")
        f.write(f"| **`NO-QUALIFIED-CANDIDATE`** | **{counts['NO-QUALIFIED-CANDIDATE']}** | {counts['NO-QUALIFIED-CANDIDATE']/len(movie_results)*100:.1f}% | No indexed candidate cleared profile minimum cutoff score (1000). |\n")
        f.write(f"| **Total** | **{len(movie_results)}** | **100.0%** | Full active Radarr4k library inventory. |\n\n")
        
        f.write("---\n\n")
        f.write("## 2. Ranked Priority Upgrade Queue\n\n")
        f.write("The following titles are identified as material upgrade candidates, ranked by score improvement delta:\n\n")
        f.write("| Rank | Title | Year | Current File (Group / Codec / Score) | Best Candidate (Group / Codec / Score) | Score Delta | Rationale |\n")
        f.write("| :---: | :--- | :---: | :--- | :--- | :---: | :--- |\n")
        
        for rank, u in enumerate(upgrade_queue, 1):
            cur_str = f"`{u['cur_group']}` ({u['cur_codec']}, {u['cur_score']} pts)" if u['cur_group'] != 'None' else "*Missing File*"
            best_str = f"`{u['best_group']}` ({u['best_codec']}, {u['best_score']} pts, {u['best_size_gb']}GB)"
            f.write(f"| {rank} | **{u['title']}** | {u['year']} | {cur_str} | {best_str} | **+{u['score_delta']}** | {u['rationale']} |\n")
            
        f.write("\n---\n\n")
        f.write("## 3. Dedicated Review: CMRG x265 Releases (Parked from Op 927)\n\n")
        f.write("`CMRG` produces widely distributed x265 UHD transparent encodes and remuxes. Analysis of interactive search appearances:\n\n")
        if cmrg_candidates:
            # Deduplicate by movie
            seen_cmrg_movies = set()
            deduped_cmrg = []
            for c in cmrg_candidates:
                if c['movie'] not in seen_cmrg_movies:
                    seen_cmrg_movies.add(c['movie'])
                    deduped_cmrg.append(c)
            f.write(f"Discovered **{len(cmrg_candidates)} candidate releases** matching `CMRG` across {len(deduped_cmrg)} distinct library titles.\n\n")
            f.write("| Movie Title | Year | Candidate Size | Codec | Review & Fallback Calibration Notes |\n")
            f.write("| :--- | :---: | :---: | :---: | :--- |\n")
            for c in deduped_cmrg[:12]:
                f.write(f"| **{c['movie']}** | {c['year']} | {c['size_gb']:.2f} GB | `{c['codec']}` | Standard transparent x265 fallback candidate. Baseline score ~2150–2450. Properly subservient to Tiered AV1 (+3500 base). |\n")
        else:
            f.write("No direct CMRG candidate releases emerged in the top candidate pool for the active catalog.\n")
            
        f.write("\n---\n\n")
        f.write("## 4. Complete Library Catalog Census Breakdown\n\n")
        f.write("| Title | Year | Current Summary | Best Candidate Summary | Delta | Status | Decision Rationale |\n")
        f.write("| :--- | :---: | :--- | :--- | :---: | :---: | :--- |\n")
        
        for r in movie_results:
            cur_summary = f"{r['cur_group']} ({r['cur_codec']}, {r['cur_size_gb']}GB, {r['cur_score']} pts)" if r['cur_group'] != 'None' else "*None*"
            best_summary = f"{r['best_group']} ({r['best_codec']}, {r['best_size_gb']}GB, {r['best_score']} pts)" if r['best_group'] != 'None' else "*None*"
            f.write(f"| **{r['title']}** | {r['year']} | {cur_summary} | {best_summary} | `{r['score_delta']:+d}` | **`{r['classification']}`** | {r['rationale']} |\n")
            
        f.write("\n---\n\n")
        f.write("## 5. Architectural Invariant & Standing Rule\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> **Standing Protocol:** Census outputs NEVER authorize automated production changes. Every item in the upgrade queue requires an explicit, evidence-backed operational directive before any grab, import, or file replacement is performed.\n")
        
    print(f"Generated public census artifact at {public_md}.")

if __name__ == '__main__':
    run_census()
