#!/usr/bin/env python3
"""
scripts/fetch_av1_supply.py
Harvests the complete AV1 release supply across configured Newznab indexers.
Supports per-indexer checkpointing, title-based normalization/deduplication,
sanitized GUID generation (no URLs, no 32-hex patterns), and API politeness.
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

def extract_group(title: str) -> str:
    title_clean = re.sub(r'\.(mkv|mp4|avi|ts)$', '', title, flags=re.IGNORECASE)
    
    # 1. Leading bracket
    m_prefix = re.match(r'^\[([A-Za-z0-9._ -]+)\]', title_clean)
    if m_prefix:
        g = m_prefix.group(1).strip()
        if g and not re.search(r'\b(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\b', g, re.I):
            return g

    # 2. Strip only known indexer site tags at the end
    title_clean = re.sub(r'\[(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv|xpost)\]$', '', title_clean, flags=re.I).strip()

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
        
        if re.match(r'^(?:RandH|R&H|R and H|R_and_H)$', suffix, re.I):
            return 'R and H'
            
        if len(suffix) <= 30 and re.match(r'^[A-Za-z0-9_&. -]+$', suffix):
            return suffix
            
    return ''

def parse_release_metadata(title: str, size_bytes: int, raw_date: str, category: str, guid: str, indexer: str) -> dict:
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
            
    # Clean, sanitized GUID (no URLs, no 32-hex characters)
    safe_guid = clean_guid(indexer, guid if guid else title)
            
    return {
        'date_posted': date_posted,
        'indexer': indexer,
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

def get_indexers_config():
    indexers = []
    
    # Check env vars first
    ds_key = os.environ.get('DRUNKENSLUG_API_KEY')
    ds_url = os.environ.get('DRUNKENSLUG_URL', 'https://indexer-c.com')
    if ds_key:
        indexers.append({'name': 'Indexer-C', 'baseUrl': ds_url, 'apiKey': ds_key})
        
    dog_key = os.environ.get('DOGNZB_API_KEY')
    dog_url = os.environ.get('DOGNZB_URL', 'https://api.indexer-a.cr')
    if dog_key:
        indexers.append({'name': 'Indexer-A', 'baseUrl': dog_url, 'apiKey': dog_key})
        
    # If not in env, lookup safely from local prowlarr.db without writing keys to disk/logs
    if not indexers:
        prowlarr_db = os.environ.get(
            'PROWLARR_DB_PATH',
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config', 'prowlarr', 'prowlarr.db')
        )
        if os.path.exists(prowlarr_db):
            import sqlite3
            conn = sqlite3.connect(prowlarr_db)
            cursor = conn.cursor()
            rows = cursor.execute('SELECT Name, Settings FROM Indexers').fetchall()
            for r_name, r_settings in rows:
                if r_name in ['Indexer-C', 'Indexer-A']:
                    try:
                        s = json.loads(r_settings)
                        if s.get('apiKey'):
                            indexers.append({
                                'name': r_name,
                                'baseUrl': s.get('baseUrl', '').rstrip('/'),
                                'apiKey': s.get('apiKey')
                            })
                    except Exception:
                        pass
    return indexers

def fetch_category_page(indexer_name: str, base_url: str, api_key: str, cat: str, query: str, offset: int, limit: int = 100) -> tuple:
    url = f"{base_url}/api?t=search&q={query}&cat={cat}&limit={limit}&offset={offset}&apikey={api_key}&extended=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'AV1SupplyCensus/1.0 (Linux; x86_64)'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
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
    except Exception as e:
        print(f"  [ERROR] {indexer_name} cat={cat} q={query} offset={offset}: {e}", file=sys.stderr)
        return [], 0

def regenerate_from_checkpoints(evidence_dir: str, output_csv: str):
    """Regenerates evidence/supply_av1.csv from local checkpoint JSONL files."""
    checkpoint_files = [os.path.join(evidence_dir, 'supply_checkpoint.jsonl')]
    checkpoints_subdir = os.path.join(evidence_dir, 'checkpoints')
    if os.path.exists(checkpoints_subdir):
        for f in os.listdir(checkpoints_subdir):
            if f.endswith('.jsonl'):
                checkpoint_files.append(os.path.join(checkpoints_subdir, f))

    all_items = {}
    for cp_path in checkpoint_files:
        if os.path.exists(cp_path):
            with open(cp_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            obj = json.loads(line)
                            k = obj.get('guid') or obj.get('title')
                            if k and k not in all_items:
                                all_items[k] = obj
                        except Exception:
                            pass

    print(f"Loaded {len(all_items)} unique raw items from local checkpoints.")

    fieldnames = [
        'date_posted', 'indexer', 'category', 'title', 'size_bytes',
        'res', 'codec_tags', 'group', 'upscale_flag', 'lang_flags', 'guid'
    ]

    records = []
    for k, it in all_items.items():
        norm = parse_release_metadata(
            title=it.get('title', ''),
            size_bytes=it.get('size_bytes', 0),
            raw_date=it.get('pubDate', ''),
            category=it.get('category', ''),
            guid=it.get('guid', ''),
            indexer=it.get('indexer', 'Indexer-C')
        )
        records.append(norm)

    records.sort(key=lambda r: (r['date_posted'] or '0000-00-00', r['title']), reverse=True)

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Sanitized & normalized {len(records)} records written to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Fetch or regenerate AV1 supply census.")
    parser.add_argument('--regenerate', action='store_true', default=False, help="Regenerate CSV from local JSONL checkpoints without API calls")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evidence_dir = os.path.join(base_dir, 'evidence')
    os.makedirs(evidence_dir, exist_ok=True)
    
    checkpoint_file = os.path.join(evidence_dir, 'supply_checkpoint.jsonl')
    output_csv = os.path.join(evidence_dir, 'supply_av1.csv')

    if args.regenerate or not os.environ.get('DRUNKENSLUG_API_KEY') and os.path.exists(checkpoint_file):
        regenerate_from_checkpoints(evidence_dir, output_csv)
        return

    # Normal fetch logic
    existing_items = {}
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        obj = json.loads(line)
                        guid = obj.get('guid') or obj.get('title')
                        if guid:
                            existing_items[guid] = obj
                    except Exception:
                        pass

    indexers = get_indexers_config()
    if not indexers:
        regenerate_from_checkpoints(evidence_dir, output_csv)
        return

    matrix = [
        ('2045', 'av1'),   # Movies UHD
        ('2045', 'av01'),  # Movies UHD alternate
        ('2040', 'av1'),   # Movies HD
        ('2040', 'av01'),  # Movies HD alternate
        ('2000', 'av1'),   # Movies All
        ('2000', 'av01')   # Movies All alternate
    ]

    new_fetched = 0
    with open(checkpoint_file, 'a', encoding='utf-8') as cp_out:
        for idx in indexers:
            print(f"\n--- Harvesting Indexer: {idx['name']} ---")
            for cat, q in matrix:
                offset = 0
                limit = 100
                while True:
                    items, total_reported = fetch_category_page(
                        idx['name'], idx['baseUrl'], idx['apiKey'], cat, q, offset, limit
                    )
                    if not items:
                        break
                    for it in items:
                        guid = it.get('guid') or it.get('title')
                        if guid and guid not in existing_items:
                            existing_items[guid] = it
                            cp_out.write(json.dumps(it) + '\n')
                            cp_out.flush()
                            new_fetched += 1
                    offset += limit
                    if offset >= total_reported or len(items) < limit or offset >= 5000:
                        break
                    time.sleep(2.0)

    regenerate_from_checkpoints(evidence_dir, output_csv)

if __name__ == '__main__':
    main()
