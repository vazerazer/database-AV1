#!/usr/bin/env python3
"""
scripts/census_report.py
Analyzes evidence/supply_av1.csv and generates evidence/census_924.md.
Includes multi-indexer cross-referencing, group robustness statistics,
coverage gap analysis, Op 925 tier promotions, and alias consolidation.
"""

import os
import re
import csv
import statistics
from collections import defaultdict, Counter

def percentile(data, p):
    if not data:
        return 0.0
    sorted_d = sorted(data)
    k = (len(sorted_d) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_d) - 1)
    d0 = sorted_d[f]
    d1 = sorted_d[c]
    return round(d0 + (d1 - d0) * (k - f), 2)

TIER_MAP = {
    # Quality Encoders (Op 925 expanded)
    'cosmicsurfer': 'Quality Encoders',
    'waldek': 'Quality Encoders',
    'prl': 'Quality Encoders',
    'prl waldek': 'Quality Encoders',
    'chd': 'Quality Encoders',
    'chopperhitler': 'Quality Encoders',
    'taoe': 'Quality Encoders',
    'dav1nci': 'Quality Encoders',    # Op 925 promoted
    'uh': 'Quality Encoders',         # Op 925 promoted
    'smokindevil': 'Quality Encoders',# Op 925 promoted
    
    # Compact Encoders
    'whiskeyjack': 'Compact Encoders',
    'whiskyjack': 'Compact Encoders',
    'edge2020': 'Compact Encoders',
    'unav1chain': 'Compact Encoders',
    'userhevc': 'Compact Encoders',
    'rav1ne': 'Compact Encoders',
    'r and h': 'Compact Encoders',
    'randh': 'Compact Encoders',
    'r&h': 'Compact Encoders',
    'rh': 'Compact Encoders',
    'lazarus': 'Compact Encoders',
    'dkv': 'Compact Encoders',
    'tizu': 'Compact Encoders',
    'saon': 'Compact Encoders',
    'onlyfaffs': 'Compact Encoders',
    'kimji': 'Compact Encoders',
    'hetorico': 'Compact Encoders',
    'rosy': 'Compact Encoders',
    'anomoomin': 'Compact Encoders',
    'cmct': 'Compact Encoders',
    'grimm': 'Compact Encoders',
    'dust': 'Compact Encoders',
    'din': 'Compact Encoders',
    'gang': 'Compact Encoders',
    'toasty': 'Compact Encoders',      # Op 925 added
    
    # Storage Savers
    'psa': 'Storage Savers',
    'galaxyrg': 'Storage Savers',
    'megusta': 'Storage Savers',
    'vxt': 'Storage Savers',
    'd3g': 'Storage Savers',
    'ghost': 'Storage Savers',
    'rartv': 'Storage Savers',
    'elite': 'Storage Savers',
    'lama': 'Storage Savers',
    'kaka': 'Storage Savers',
    'yawntic': 'Storage Savers',
    'bone': 'Storage Savers',
    'gz': 'Storage Savers',
    'cart': 'Storage Savers',
    'lucy': 'Storage Savers',
    'dkong': 'Storage Savers',
    'rapta': 'Storage Savers',
    'gubrakz': 'Storage Savers',
    'retr0': 'Storage Savers',
    'swaxxon': 'Storage Savers',
    'felix12345': 'Storage Savers',
    
    # Anime Encoders
    'trix': 'Anime Encoders',
    'breeze': 'Anime Encoders',
    'index': 'Anime Encoders',
    'sav1or': 'Anime Encoders',
    'av1ary': 'Anime Encoders',
    'sokudo': 'Anime Encoders',
    'rigav1': 'Anime Encoders',
    'ironclad': 'Anime Encoders',
    'valenciano': 'Anime Encoders',
    
    # Banned
    'entropy': 'Banned'
}

def get_tier(group_name: str) -> str:
    if not group_name or group_name.startswith('('):
        return 'Nameless'
    return TIER_MAP.get(group_name.lower().strip(), 'Untiered')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_dir, 'evidence', 'supply_av1.csv')
    output_md = os.path.join(base_dir, 'evidence', 'census_924.md')
    
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} does not exist. Run fetch_av1_supply.py first.", file=sys.stderr)
        sys.exit(1)
        
    with open(input_csv, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        
    total_records = len(rows)
    
    # Distributions
    res_counts = defaultdict(int)
    group_res = defaultdict(lambda: defaultdict(int))
    group_2160p_items = defaultdict(list)
    group_all_items = defaultdict(list)
    
    # Indexer metrics
    indexer_presence_counts = Counter()
    indexer_exclusive_counts = Counter()
    multi_indexer_releases = 0
    group_indexers = defaultdict(set)
    
    for r in rows:
        res = r['res']
        res_counts[res] += 1
        g = r['group'].strip() if r['group'].strip() else '(Nameless/Untagged)'
        group_res[g][res] += 1
        group_res[g]['total'] += 1
        group_all_items[g].append(r)
        if res == '2160p':
            group_2160p_items[g].append(r)
            
        raw_idx = r.get('indexers', '').strip()
        idx_list = [i.strip() for i in raw_idx.split(';') if i.strip()]
        for idx in idx_list:
            indexer_presence_counts[idx] += 1
            group_indexers[g].add(idx)
            
        if len(idx_list) == 1:
            indexer_exclusive_counts[idx_list[0]] += 1
        elif len(idx_list) > 1:
            multi_indexer_releases += 1
            
    # Markdown generation
    lines = []
    lines.append("# OP 924b: Multi-Indexer AV1 Supply Census Report")
    lines.append("### Comprehensive Empirical Inventory Across All Indexers\n")
    lines.append(f"- **Total Deduplicated Unique Titles:** {total_records:,} (vs. 6,552 dual-indexer baseline)")
    lines.append(f"- **Multi-Indexer Propagated Titles (≥2 Indexers):** {multi_indexer_releases:,} ({multi_indexer_releases*100.0/total_records:.1f}%)")
    lines.append(f"- **2160p UHD Releases:** {res_counts['2160p']:,} ({res_counts['2160p']*100.0/total_records:.1f}%)")
    lines.append(f"- **1080p HD Releases:** {res_counts['1080p']:,} ({res_counts['1080p']*100.0/total_records:.1f}%)")
    lines.append(f"- **720p Releases:** {res_counts['720p']:,} ({res_counts['720p']*100.0/total_records:.1f}%)")
    lines.append(f"- **Other / Unclassified:** {res_counts['Other']:,}\n")
    lines.append("---\n")
    
    # 1. Indexer Coverage Analysis
    lines.append("## 1. Indexer Coverage & Overlap Matrix\n")
    lines.append("| Indexer Name | Total Releases Indexed | Exclusive to Indexer | Shared Across Indexers | Propagation % |")
    lines.append("| :--- | :---: | :---: | :---: | :---: |")
    
    for idx_name, tot_seen in sorted(indexer_presence_counts.items(), key=lambda x: x[1], reverse=True):
        excl = indexer_exclusive_counts[idx_name]
        shared = tot_seen - excl
        prop_pct = (shared * 100.0 / tot_seen) if tot_seen > 0 else 0.0
        lines.append(f"| **`{idx_name}`** | {tot_seen:,} | {excl:,} | {shared:,} | {prop_pct:.1f}% |")
        
    lines.append("\n---\n")
    
    # 2. Top 30 2160p Groups Stats Table (with Multi-Indexer Robustness & Post-Op 925 Tiers)
    lines.append("## 2. Top 2160p Release Groups (Empirical Statistics & Robustness)\n")
    lines.append("| Release Group | 2160p Count | Median Size | p25 - p75 Band | % Upscale | % Lang/Dub | Indexer Count | Current Tier |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    sorted_2160p = sorted([(g, len(items)) for g, items in group_2160p_items.items()], key=lambda x: x[1], reverse=True)
    
    for g, cnt in sorted_2160p[:35]:
        items = group_2160p_items[g]
        sizes = [float(it['size_bytes'])/(1024**3) for it in items if float(it.get('size_bytes', 0)) > 0]
        p25 = percentile(sizes, 25)
        med = round(statistics.median(sizes), 2) if sizes else 0.0
        p75 = percentile(sizes, 75)
        upscales = sum(1 for it in items if it['upscale_flag'] == '1')
        up_pct = upscales * 100.0 / cnt
        langs = sum(1 for it in items if it['lang_flags'].strip())
        lang_pct = langs * 100.0 / cnt
        tier = get_tier(g)
        num_idx = len(group_indexers[g])
        idx_robust = f"**{num_idx} indexers**" if num_idx >= 2 else f"{num_idx} indexer"
        lines.append(f"| **`{g}`** | {cnt} | {med:.2f} GB | {p25:.2f} - {p75:.2f} GB | {up_pct:.1f}% | {lang_pct:.1f}% | {idx_robust} | {tier} |")
        
    lines.append("\n---\n")
    
    # 3. Group x Resolution Histogram (Top 25 Total Supply)
    lines.append("## 3. Group × Resolution Histogram (Top 25 Total Supply)\n")
    lines.append("| Release Group | Total Supply | 2160p UHD | 1080p HD | 720p / Other | Cross-Indexer Count | Primary Tier |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    sorted_total = sorted([(g, data['total']) for g, data in group_res.items()], key=lambda x: x[1], reverse=True)
    for g, tot in sorted_total[:25]:
        c2160 = group_res[g].get('2160p', 0)
        c1080 = group_res[g].get('1080p', 0)
        c_other = tot - c2160 - c1080
        tier = get_tier(g)
        num_idx = len(group_indexers[g])
        lines.append(f"| **`{g}`** | {tot} | {c2160} | {c1080} | {c_other} | {num_idx} indexers | {tier} |")
        
    lines.append("\n---\n")
    
    # 4. Tier Coverage Gap Analysis
    lines.append("## 4. Tier Coverage Gap Analysis\n")
    lines.append("Analysis of high-frequency groups that are currently **Untiered** in `Movies 2160p AV1 HQ`:\n")
    
    untiered_2160p = [(g, len(items)) for g, items in group_2160p_items.items() if get_tier(g) == 'Untiered']
    untiered_2160p.sort(key=lambda x: x[1], reverse=True)
    
    lines.append("| Untiered Group | 2160p Count | Median Size | % Upscale | % Lang/Dub | Indexer Presence | Assessment & Strategic Note |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    for g, cnt in untiered_2160p[:15]:
        items = group_2160p_items[g]
        sizes = [float(it['size_bytes'])/(1024**3) for it in items if float(it.get('size_bytes', 0)) > 0]
        med = round(statistics.median(sizes), 2) if sizes else 0.0
        upscales = sum(1 for it in items if it['upscale_flag'] == '1')
        up_pct = upscales * 100.0 / cnt
        langs = sum(1 for it in items if it['lang_flags'].strip())
        lang_pct = langs * 100.0 / cnt
        num_idx = len(group_indexers[g])
        
        note = "Candidate for future evaluation"
        if g in ['HODENSACK', 'OSKOREIA']:
            note = "Micro sample / clip files (<0.5GB), ignore"
        elif g == 'SHADOW':
            note = "100% French audio dubs; guarded by Foreign Dub CF (-750)"
        elif g == 'THESYNDiCATE':
            note = "Foreign audio multi releases"
        elif g == 'Bi0hazard':
            note = "German.DUBBED.DL releases; guarded by Foreign Dub CF (-750)"
        elif g == 'Don':
            note = "Watch-list only (12.35 GB median, 1 indexer); hold for more supply"
        elif g == 'WtF':
            note = "Watch-list only (13.37 GB median, 20% upscale); hold for consistency"
        elif g == 'JeRi':
            note = "Micro encodes (3.24 GB median); falls in Micro/Lean band"
        elif g == 'WOTT':
            note = "100% Polish audio tag; foreign dub guarded"
            
        lines.append(f"| **`{g}`** | {cnt} | {med:.2f} GB | {up_pct:.1f}% | {lang_pct:.1f}% | {num_idx} indexers | {note} |")
        
    lines.append("\n---\n")
    
    # 5. Op 925 Promotion Outcomes
    lines.append("## 5. Op 925 Promotion Outcomes (Evidence & Census Keyed)\n")
    lines.append("1. **`dAV1nci`** (*Promoted to Quality Encoders +1000*): $N=12$ in 2160p (Median 11.97 GB, 0% upscale, 0% dub) and $N=90$ in 1080p (Median 3.28 GB) across **8 indexers**. Zero empirical failure records; consistent master encoder.\n")
    lines.append("2. **`UH`** (*Promoted to Quality Encoders +1000*): $N=22$ in 2160p (Median 12.94 GB, 0% upscale, 0% dub) across **6 indexers**. Solid transparent master encodings (dormant catalog value).\n")
    lines.append("3. **`Smokindevil`** (*Promoted to Quality Encoders +1000*): $N=10$ in 2160p (Median 11.11 GB, 0% upscale, 0% dub, TrueHD Atmos tracks) across **5 indexers**. Double-keyed promotion backed by 1 empirical PASS (*Fury* watch).\n")
    lines.append("4. **`Toasty`** (*Added to Compact Encoders +500*): $N=2$ in 2160p (Median 21.65 GB, 0% upscale, 0% dub). High-bitrate reference supply tiered at Compact ceiling pending direct watch verdicts.\n")
    lines.append("5. **`R and H` Family Consolidation**: Unified `R&H`, `RandH`, `R and H`, `RH`, and file extension artifacts into single canonical `R and H` family ($N=1,486$ in 2160p, 7 indexers) in Compact Encoders.\n")
    lines.append("6. **`PRL Waldek` Suffix Expansion**: Unified `PRL.Waldek` and `PRL Waldek` in Quality Encoders.\n")

    report_content = '\n'.join(lines) + '\n'
    
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"Census report generated successfully at {output_md}")

if __name__ == '__main__':
    main()
