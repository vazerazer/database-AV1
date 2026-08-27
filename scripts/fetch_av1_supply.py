#!/usr/bin/env python3
"""
scripts/fetch_av1_supply.py
Harvests the complete AV1 release supply across configured Newznab indexers.
Supports --all-indexers mode, per-indexer checkpointing, title-based normalization/deduplication,
cross-indexer presence aggregation, sanitized GUID generation (no URLs, no 32-hex patterns),
and API rate-limit politeness.
"""

import os
import sys
import time
import json
import csv
import re
import argparse
import hashlib
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from collections import defaultdict

FOREIGN_DUB_REGEX = re.compile(
    r'(?i)\b(?:(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)|(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)[._ -]+DL|DL[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB))\b'
)

NON_GROUPS = {
    'nlsub', 'nl', 'dutch', 'german', 'french', 'ita', 'spanish', 'swe', 'dk', 'nor', 'fi',
    'xpost', 'av1', 'av01', 'hevc', 'x265', 'x264', 'hdr', 'dv', '10bit', '8bit',
    'brrip', 'bdrip', 'webdl', 'web-dl', 'webrip', 'bluray', 'uhd', '2160p', '1080p', '720p',
    'aac', 'ddp', 'ac3', 'truehd', 'atmos', 'dts', 'dts-hd', 'opus'
}

def clean_guid(indexer: str, raw_guid: str) -> str:
    """Normalizes raw GUIDs/URLs into a safe <indexer>:<first 12 hex chars> slug."""
    idx_slug = re.sub(r'[^a-zA-Z0-9]', '', indexer.lower()) if indexer else 'idx'
    m_hex = re.search(r'([0-9a-fA-F]{8,64})', raw_guid)
    if m_hex:
        hex_str = m_hex.group(1).lower()
        return f"{idx_slug}:{hex_str[:12]}"
    h = hashlib.sha256(raw_guid.encode('utf-8')).hexdigest()[:12]
    return f"{idx_slug}:{h}"

def normalize_title_key(title: str) -> str:
    """Collapses whitespace, dots, hyphens, underscores and strips file extensions for deduplication."""
    t = re.sub(r'\.(mkv|mp4|avi|ts)$', '', title, flags=re.IGNORECASE).strip()
    t = re.sub(r'[\s._-]+', ' ', t.lower()).strip()
    return t

def normalize_group_alias(g: str) -> str:
    g_clean = g.strip()
    if re.match(r'^(?:RandH|R&H|R and H|R_and_H|RH)$', g_clean, re.I):
        return 'R and H'
    if re.match(r'^dAV1nci$', g_clean, re.I):
        return 'dAV1nci'
    if re.match(r'^TAoE$', g_clean, re.I):
        return 'TAoE'
    if re.match(r'^PRL[\s.]*Waldek$', g_clean, re.I):
        return 'PRL Waldek'
    if re.match(r'^Smokindevil$', g_clean, re.I):
        return 'Smokindevil'
    if re.match(r'^(?:WhiskeyJack|WhiskyJack)$', g_clean, re.I):
        return 'WhiskeyJack'
    if re.match(r'^Toasty$', g_clean, re.I):
        return 'Toasty'
    if re.match(r'^CoSMiCSuRFeR$', g_clean, re.I):
        return 'CoSMiCSuRFeR'
    return g_clean

def extract_group(title: str) -> str:
    title_clean = title.strip()
    title_clean = re.sub(r'\.(mkv|mp4|avi|ts|iso|nfo|rar|par2)$', '', title_clean, flags=re.I).strip()
    title_clean = re.sub(r'[\s._-]+$', '', title_clean).strip()
    title_clean = re.sub(r'\[(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv|xpost)\]$', '', title_clean, flags=re.I).strip()
    title_clean = re.sub(r'[\s._-]+$', '', title_clean).strip()
    
    # 1. Trailing bracket group e.g. .[TAoE]
    m_tail_bracket = re.search(r'\[([A-Za-z0-9._ -]+)\]$', title_clean)
    if m_tail_bracket:
        g = m_tail_bracket.group(1).strip()
        if g and not re.search(r'\b(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv|xpost)\b', g, re.I):
            return normalize_group_alias(g)

    # 2. Leading bracket
    m_prefix = re.match(r'^\[([A-Za-z0-9._ -]+)\]', title_clean)
    if m_prefix:
        g = m_prefix.group(1).strip()
        if g and not re.search(r'\b(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\b', g, re.I):
            return normalize_group_alias(g)

    # 3. Last hyphen
    if '-' in title_clean:
        parts = title_clean.rsplit('-', 1)
        suffix = parts[1].strip()
        
        if suffix.lower() == 'xpost' and '-' in parts[0]:
            sub_parts = parts[0].rsplit('-', 1)
            suffix = sub_parts[1].strip()
            
        if suffix.lower() in NON_GROUPS:
            return ''
            
        suffix = re.sub(r'^\[|\]$', '', suffix).strip()
        suffix = re.sub(r'\.(mkv|mp4|avi|ts)$', '', suffix, flags=re.I).strip()
        
        if len(suffix) <= 35 and re.match(r'^[A-Za-z0-9_&. -]+$', suffix):
            return normalize_group_alias(suffix)
            
    return ''

def parse_release_metadata(title: str, size_bytes: int, raw_date: str, category: str, guid: str, indexers_list: list) -> dict:
    # Resolution
    if re.search(r'\b(2160p|4K|UHD)\b', title, re.I):
        res = '2160p'
    elif re.search(r'\b(1080p|1080i)\b', title, re.I):
        res = '1080p'
    elif re.search(r'\b(720p)\b', title, re.I):
        res = '720p'
    else:
        res = 'Other'
        
    # Codec
    codec_tags = 'AV01' if re.search(r'\bAV01\b', title, re.I) else 'AV1'
    
    # Group
    group = extract_group(title)
    
    # Upscale
    upscale_flag = 1 if re.search(r'(?i)\b(?:upscale|ai[-._ ]?upscale)\b', title) else 0
    
    # Language Flags
    lang_flags = []
    if FOREIGN_DUB_REGEX.search(title):
        lang_flags.append('FOREIGN_DUB')
    for tag in ['MULTi', 'VF2', 'PRL', 'NORDiC', 'NLsub', 'SWE', 'DK', 'NOR', 'GERMAN', 'FRENCH', 'ITALIAN', 'SPANISH', 'RUSSIAN', 'POLISH', 'DUTCH']:
        if re.search(rf'\b{tag}\b', title, re.I) and tag not in lang_flags:
            lang_flags.append(tag)
            
    # Date Posted
    date_posted = ''
    if raw_date:
        try:
            dt = parsedate_to_datetime(raw_date)
            date_posted = dt.strftime('%Y-%m-%d')
        except Exception:
            date_posted = raw_date[:10]
            
    # Semicolon-delimited list of indexers
    idx_str = ';'.join(sorted(list(set(indexers_list))))
    first_idx = indexers_list[0] if indexers_list else 'idx'
    safe_guid = clean_guid(first_idx, guid if guid else title)
            
    return {
        'date_posted': date_posted,
        'indexers': idx_str,
        'category': category,
        'title': title,
        'size_bytes': size_bytes,
        'res': res,
        'codec_tags': codec_tags,
        'group': group,
        'upscale_flag': upscale_flag,
        'lang_flags': '|'.join(lang_flags),
        'guid': safe_guid
    }

def get_all_prowlarr_indexers(all_indexers: bool = True) -> list:
    """Discovers all Newznab/Torznab indexers from Prowlarr without logging secrets."""
    indexers = []
    prowlarr_db = os.environ.get(
        'PROWLARR_DB_PATH',
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config', 'prowlarr', 'prowlarr.db')
    )
    if os.path.exists(prowlarr_db):
        import sqlite3
        conn = sqlite3.connect(prowlarr_db)
        cursor = conn.cursor()
        rows = cursor.execute('SELECT Id, Name, Implementation, Settings, Enable FROM Indexers').fetchall()
        for r_id, r_name, r_impl, r_settings, r_enabled in rows:
            if r_impl.lower() not in ['newznab', 'torznab']:
                print(f"Skipping non-Newznab indexer: {r_name} ({r_impl})")
                continue
            if not all_indexers and r_name not in ['Indexer-C', 'Indexer-A']:
                continue
            try:
                s = json.loads(r_settings)
                api_key = s.get('apiKey')
                base_url = s.get('baseUrl', '').rstrip('/')
                if api_key and base_url:
                    indexers.append({
                        'id': r_id,
                        'name': r_name,
                        'baseUrl': base_url,
                        'apiKey': api_key,
                        'enabled': r_enabled
                    })
            except Exception as e:
                print(f"Failed to parse settings for {r_name}: {e}", file=sys.stderr)
    return indexers

def fetch_category_page(indexer_name: str, base_url: str, api_key: str, cat: str, query: str, offset: int, limit: int = 100) -> tuple:
    url = f"{base_url}/api?t=search&q={query}&cat={cat}&limit={limit}&offset={offset}&apikey={api_key}&extended=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'AV1SupplyCensus/2.0 (Linux; x86_64)'})
    
    retries = 2
    while retries >= 0:
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read()
                root = ET.fromstring(raw)
                items = []
                for item_elem in root.findall('.//item'):
                    title = item_elem.find('title')
                    pubDate = item_elem.find('pubDate')
                    guid = item_elem.find('guid')
                    cat_elem = item_elem.find('category')
                    
                    size_bytes = 0
                    enc = item_elem.find('enclosure')
                    if enc is not None and enc.attrib.get('length'):
                        try:
                            size_bytes = int(enc.attrib['length'])
                        except ValueError:
                            pass
                    if size_bytes == 0:
                        for attr in item_elem.findall('.//{http://www.newznab.com/DTD/2010/feeds/attributes/}attr'):
                            if attr.attrib.get('name') == 'size':
                                try:
                                    size_bytes = int(attr.attrib.get('value', 0))
                                except ValueError:
                                    pass
                                    
                    items.append({
                        'indexer': indexer_name,
                        'category': cat_elem.text if cat_elem is not None else cat,
                        'title': title.text if title is not None else '',
                        'pubDate': pubDate.text if pubDate is not None else '',
                        'guid': guid.text if guid is not None else '',
                        'size_bytes': size_bytes
                    })
                    
                total_elem = root.find('.//{http://www.newznab.com/DTD/2010/feeds/attributes/}response')
                total_count = int(total_elem.attrib.get('total', len(items))) if total_elem is not None else len(items)
                return items, total_count
        except urllib.error.HTTPError as he:
            if he.code == 429:
                print(f"    [429 Rate Limit] {indexer_name} - backing off for 10s...", file=sys.stderr)
                time.sleep(10.0)
                retries -= 1
                continue
            else:
                print(f"    [HTTP {he.code}] {indexer_name} cat={cat} offset={offset}: {he.reason}", file=sys.stderr)
                return [], 0
        except Exception as e:
            if retries > 0:
                time.sleep(3.0)
                retries -= 1
                continue
            print(f"    [ERROR] {indexer_name} cat={cat} offset={offset}: {e}", file=sys.stderr)
            return [], 0
    return [], 0

def regenerate_from_checkpoints(evidence_dir: str, output_csv: str):
    """Regenerates evidence/supply_av1.csv from local checkpoint JSONL files with cross-indexer deduplication."""
    checkpoint_files = []
    cp_main = os.path.join(evidence_dir, 'supply_checkpoint.jsonl')
    if os.path.exists(cp_main):
        checkpoint_files.append(cp_main)
        
    checkpoints_subdir = os.path.join(evidence_dir, 'checkpoints')
    if os.path.exists(checkpoints_subdir):
        for f in os.listdir(checkpoints_subdir):
            if f.endswith('.jsonl'):
                checkpoint_files.append(os.path.join(checkpoints_subdir, f))

    all_raw_items = []
    seen_guid_per_file = set()
    for cp_path in checkpoint_files:
        if os.path.exists(cp_path):
            with open(cp_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            obj = json.loads(line)
                            all_raw_items.append(obj)
                        except Exception:
                            pass

    print(f"Loaded {len(all_raw_items)} raw checkpoint records across {len(checkpoint_files)} files.")

    # Deduplicate & merge across indexers by normalized title
    merged_by_title = {}
    for raw in all_raw_items:
        title = raw.get('title', '').strip()
        if not title:
            continue
            
        norm_key = normalize_title_key(title)
        indexer = raw.get('indexer', 'Indexer-C')
        
        if norm_key not in merged_by_title:
            merged_by_title[norm_key] = {
                'title': title,
                'size_bytes': raw.get('size_bytes', 0),
                'date_posted': raw.get('pubDate', ''),
                'category': raw.get('category', ''),
                'guid': raw.get('guid', ''),
                'indexers': {indexer}
            }
        else:
            entry = merged_by_title[norm_key]
            entry['indexers'].add(indexer)
            if raw.get('size_bytes', 0) > entry['size_bytes']:
                entry['size_bytes'] = raw.get('size_bytes', 0)
            if raw.get('pubDate') and (not entry['date_posted'] or raw.get('pubDate') < entry['date_posted']):
                entry['date_posted'] = raw.get('pubDate')

    fieldnames = [
        'date_posted', 'indexers', 'category', 'title', 'size_bytes',
        'res', 'codec_tags', 'group', 'upscale_flag', 'lang_flags', 'guid'
    ]

    records = []
    for norm_key, data in merged_by_title.items():
        norm = parse_release_metadata(
            title=data['title'],
            size_bytes=data['size_bytes'],
            raw_date=data['date_posted'],
            category=data['category'],
            guid=data['guid'],
            indexers_list=list(data['indexers'])
        )
        records.append(norm)

    records.sort(key=lambda r: (r['date_posted'] or '0000-00-00', r['title']), reverse=True)

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Sanitized & deduplicated {len(records):,} unique records written to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Harvest AV1 supply across all configured Prowlarr indexers.")
    parser.add_argument('--all-indexers', action='store_true', default=False, help="Harvest from all Prowlarr indexers")
    parser.add_argument('--regenerate', action='store_true', default=False, help="Regenerate CSV from local JSONL checkpoints without API calls")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evidence_dir = os.path.join(base_dir, 'evidence')
    checkpoints_dir = os.path.join(evidence_dir, 'checkpoints')
    os.makedirs(checkpoints_dir, exist_ok=True)
    
    output_csv = os.path.join(evidence_dir, 'supply_av1.csv')

    if args.regenerate:
        regenerate_from_checkpoints(evidence_dir, output_csv)
        return

    indexers = get_all_prowlarr_indexers(all_indexers=args.all_indexers)
    if not indexers:
        print("ERROR: No configured Newznab indexers found in Prowlarr DB.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Harvesting from {len(indexers)} indexers: {[idx['name'] for idx in indexers]}")
    
    matrix = [
        ('2045', 'av1'),   # Movies UHD
        ('2045', 'av01'),  # Movies UHD alternate
        ('2040', 'av1'),   # Movies HD
        ('2040', 'av01'),  # Movies HD alternate
        ('2000', 'av1'),   # Movies All
        ('2000', 'av01')   # Movies All alternate
    ]

    for idx in indexers:
        idx_slug = re.sub(r'[^a-zA-Z0-9_-]', '_', idx['name'].lower())
        idx_cp_file = os.path.join(checkpoints_dir, f"{idx_slug}.jsonl")
        
        idx_items = {}
        if os.path.exists(idx_cp_file):
            with open(idx_cp_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            obj = json.loads(line)
                            k = obj.get('guid') or obj.get('title')
                            if k:
                                idx_items[k] = obj
                        except Exception:
                            pass
            print(f"\n[{idx['name']}] Loaded {len(idx_items)} existing checkpoint records.")
            
        print(f"\n--- Harvesting Indexer: {idx['name']} ---")
        new_for_idx = 0
        
        with open(idx_cp_file, 'a', encoding='utf-8') as cp_out:
            for cat, q in matrix:
                offset = 0
                limit = 100
                print(f"  Querying {idx['name']}: cat={cat} q={q}...")
                
                while True:
                    items, total_reported = fetch_category_page(
                        idx['name'], idx['baseUrl'], idx['apiKey'], cat, q, offset, limit
                    )
                    
                    if not items:
                        break
                        
                    for it in items:
                        k = it.get('guid') or it.get('title')
                        if k and k not in idx_items:
                            idx_items[k] = it
                            cp_out.write(json.dumps(it) + '\n')
                            cp_out.flush()
                            new_for_idx += 1
                            
                    print(f"    Offset {offset:<5} | Page items: {len(items):<3} | Total reported: {total_reported:<5} | Cumulative for {idx['name']}: {len(idx_items)}")
                    
                    offset += limit
                    if offset >= total_reported or len(items) < limit or offset >= 5000:
                        break
                        
                    time.sleep(2.0)  # Politeness interval between pages
                    
        print(f"[{idx['name']}] Finished harvesting. Total unique items: {len(idx_items)} (New: {new_for_idx})")

    regenerate_from_checkpoints(evidence_dir, output_csv)

if __name__ == '__main__':
    main()
