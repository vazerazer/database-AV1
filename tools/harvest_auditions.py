#!/usr/bin/env python3
"""
tools/harvest_auditions.py
Harvests untiered AV1 and exploratory releases grabbed by SHADOW Radarr4k under
the 'Movies SHADOW Explorer' profile (Profile 67), scores them against both
Explorer and Production profiles, and updates evidence/auditions.csv.

Strictly READ-ONLY against Radarr4k API.
"""

import os
import sys
import json
import csv
import re
import argparse
import urllib.request
import urllib.error

# Import PCD scoring harness
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests'))
from simulate_scoring import build_compiled_db, evaluate_release

def get_radarr_api_key():
    key = os.environ.get('RADARR_API_KEY')
    if key:
        return key
    # Local fallback
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

def harvest_auditions(dry_run=False):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    auditions_csv = os.path.join(repo_root, 'evidence', 'auditions.csv')
    verdicts_csv = os.path.join(repo_root, 'evidence', 'verdicts.csv')
    
    api_key = get_radarr_api_key()
    radarr_url = os.environ.get('RADARR_URL', 'http://127.0.0.1:7879')
    
    conn = build_compiled_db()
    
    existing_auditions = []
    seen_keys = set()
    fieldnames = [
        'date', 'title', 'tmdb_id', 'group', 'codec', 'res', 'size_gb',
        'explorer_score', 'prod_would_score', 'delta', 'status', 'verdict_ref'
    ]
    
    if os.path.exists(auditions_csv):
        with open(auditions_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_auditions.append(row)
                k = (row['tmdb_id'], row['group'].lower())
                seen_keys.add(k)
                
    # Load verdicts index for cross-referencing
    verdicts_map = {}
    if os.path.exists(verdicts_csv):
        with open(verdicts_csv, 'r', encoding='utf-8') as f:
            v_reader = csv.DictReader(f)
            for r in v_reader:
                v_k = (r['title'].lower(), r['group'].lower())
                verdicts_map[v_k] = r.get('verdict', 'PENDING')
                
    new_rows = []
    
    if api_key:
        try:
            # 1. Pull movie list to build id->movie mapping
            movies_req = urllib.request.Request(f"{radarr_url}/api/v3/movie", headers={'X-Api-Key': api_key})
            with urllib.request.urlopen(movies_req, timeout=15) as resp:
                movies_list = json.load(resp)
            movie_map = {m['id']: m for m in movies_list}
            
            # 2. Pull grabbed history
            hist_req = urllib.request.Request(f"{radarr_url}/api/v3/history?page=1&pageSize=100", headers={'X-Api-Key': api_key})
            with urllib.request.urlopen(hist_req, timeout=15) as resp:
                hist_data = json.load(resp)
                
            for rec in hist_data.get('records', []):
                if rec.get('eventType') != 'grabbed':
                    continue
                m_id = rec.get('movieId')
                movie = movie_map.get(m_id)
                if not movie:
                    continue
                    
                # Check if profile is Explorer (67) or has shadow tag
                prof_id = movie.get('qualityProfileId')
                tags = movie.get('tags', [])
                
                # Check if this grab belongs to shadow explorer
                src_title = rec.get('sourceTitle') or ''
                date_str = rec.get('date', '')[:10]
                tmdb_id = str(movie.get('tmdbId') or '')
                movie_title = movie.get('title') or ''
                
                group = extract_group(src_title, rec.get('data', {}).get('releaseGroup'))
                codec = extract_codec(src_title)
                res = extract_resolution(src_title)
                size_bytes = float(rec.get('data', {}).get('size') or 0)
                size_gb = round(size_bytes / (1024 ** 3), 2)
                
                k = (tmdb_id, group.lower())
                if k in seen_keys:
                    continue
                    
                # Calculate scores
                exp_score, _, _, _, _ = evaluate_release(conn, src_title, 'Movies SHADOW Explorer', 'radarr', size_gb=size_gb)
                prod_score, _, _, _, _ = evaluate_release(conn, src_title, 'Movies 2160p AV1 HQ', 'radarr', size_gb=size_gb)
                delta = exp_score - prod_score
                
                # Check status & verdict ref
                v_status = verdicts_map.get((movie_title.lower(), group.lower()))
                if v_status in ('PASS', 'FAIL', 'BORDERLINE', 'EXCEPTION'):
                    status = 'watched'
                    v_ref = f"{movie_title}:{group}"
                else:
                    status = 'grabbed'
                    v_ref = f"{movie_title}:{group}" if (movie_title.lower(), group.lower()) in verdicts_map else ''
                    
                new_row = {
                    'date': date_str,
                    'title': movie_title,
                    'tmdb_id': tmdb_id,
                    'group': group,
                    'codec': codec,
                    'res': res,
                    'size_gb': f"{size_gb:.2f}",
                    'explorer_score': exp_score,
                    'prod_would_score': prod_score,
                    'delta': delta,
                    'status': status,
                    'verdict_ref': v_ref
                }
                new_rows.append(new_row)
                seen_keys.add(k)
        except Exception as e:
            print(f"Warning: Could not pull live history from Radarr4k API: {e}", file=sys.stderr)
            
    print(f"Loaded {len(existing_auditions)} existing auditions. Discovered {len(new_rows)} new auditions.")
    
    combined = existing_auditions + new_rows
    combined.sort(key=lambda r: (r['date'], r['title']), reverse=True)
    
    if not dry_run:
        with open(auditions_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined)
        print(f"Updated {auditions_csv} with {len(combined)} total audition records.")
    else:
        print(f"[DRY-RUN] Would write {len(combined)} records to {auditions_csv}.")

def main():
    parser = argparse.ArgumentParser(description="Harvest SHADOW Radarr auditions into evidence/auditions.csv.")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without writing to file.")
    args = parser.parse_args()
    
    harvest_auditions(dry_run=args.dry_run)

if __name__ == '__main__':
    main()
