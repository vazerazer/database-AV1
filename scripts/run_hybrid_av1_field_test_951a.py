#!/usr/bin/env python3
"""
scripts/run_hybrid_av1_field_test_951a.py
Hybrid AV1 Profile Field Test Harness (Op 951A)

Runs interactive release searches in Radarr4k (Profile 64 Movies 2160p AV1 HQ)
for 25 curated movies across eras, content types, and group tiers, validating
actual winning release arbitration against expected tier behavior.
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_RAW_PATH = os.path.join(REPO_ROOT, "evidence", "hybrid_av1_profile_field_test_951a_raw.json")

TEST_MOVIE_IDS = [
    861,  # X-Men (2000)
    863,  # X2 (2003)
    859,  # X-Men: First Class (2011)
    915,  # The Bourne Supremacy (2004)
    916,  # The Bourne Ultimatum (2007)
    700,  # Gladiator (2000)
    838,  # Fury (2014)
    578,  # Blade Runner (1982)
    906,  # Interstellar (2014)
    920,  # John Wick (2014)
    922,  # John Wick: Chapter 2 (2017)
    921,  # John Wick: Chapter 3 - Parabellum (2019)
    923,  # John Wick: Chapter 4 (2023)
    584,  # The Shawshank Redemption (1994)
    771,  # The Sixth Sense (1999)
    928,  # Jurassic Park (1993)
    929,  # The Lost World: Jurassic Park (1997)
    934,  # Jurassic World (2015)
    835,  # The Lord of the Rings: The Fellowship of the Ring (2001)
    918,  # The Lord of the Rings: The Two Towers (2002)
    917,  # The Lord of the Rings: The Return of the King (2003)
    884,  # Apocalypse Now (1979)
    766,  # 2001: A Space Odyssey (1968)
    702,  # Akira (1988)
    909   # Logan (2017)
]

def get_api_key():
    env_key = os.environ.get("RADARR4K_API_KEY") or os.environ.get("RADARR_API_KEY")
    if env_key:
        return env_key
    candidates = [
        os.path.join(os.path.dirname(REPO_ROOT), "config", "radarr4k", "config.xml"),
        os.path.join(REPO_ROOT, "..", "config", "radarr4k", "config.xml")
    ]
    for c in candidates:
        if os.path.exists(c):
            tree = ET.parse(c)
            return tree.getroot().find('ApiKey').text
    raise FileNotFoundError("Could not find Radarr4k config.xml")

def main():
    api_key = get_api_key()
    headers = {"X-Api-Key": api_key}

    # Fetch all movies
    movies_res = requests.get("http://127.0.0.1:7879/api/v3/movie", headers=headers)
    movies_map = {m["id"]: m for m in movies_res.json()}

    results = []
    tier_counts = {"Tier 1": 0, "Tier 2": 0, "Tier 3": 0, "Tier 4": 0}
    matches = 0
    mismatches = 0

    print(f"Executing Op 951A Field Test on {len(TEST_MOVIE_IDS)} movies in Radarr4k Profile 64...")

    for mid in TEST_MOVIE_IDS:
        m = movies_map.get(mid)
        if not m:
            print(f"[WARN] Movie ID {mid} not found in Radarr4k")
            continue

        m_title = m["title"]
        m_year = m.get("year", 0)

        rel_res = requests.get(f"http://127.0.0.1:7879/api/v3/release?movieId={mid}", headers=headers)
        releases = rel_res.json() if rel_res.status_code == 200 else []

        # Profile 64 is 2160p UHD profile. Filter 2160p releases first.
        rels_2160p = [r for r in releases if "2160p" in r.get("title", "") or r.get("quality", {}).get("quality", {}).get("resolution", 0) == 2160]
        has_2160p = len(rels_2160p) > 0

        # Radarr resolution order: 2160p releases are evaluated first if available, otherwise 1080p
        eval_pool = rels_2160p if has_2160p else releases
        sorted_pool = sorted(eval_pool, key=lambda x: x.get("customFormatScore", 0), reverse=True)

        top_release = sorted_pool[0] if sorted_pool else None

        if top_release:
            rel_title = top_release.get("title", "Unknown")
            rel_score = top_release.get("customFormatScore", 0)
            rel_size_gb = round(top_release.get("size", 0) / (1024**3), 2)
            cfs = [cf["name"] for cf in top_release.get("customFormats", [])]
            res_str = top_release.get("quality", {}).get("quality", {}).get("name", "Unknown")

            # Determine actual tier
            if "AV1 Quality Encoders" in cfs or "AV1" in cfs and any(g in rel_title.lower() for g in ["chopperhitler", "cosmicsurfer", "-uh"]):
                actual_tier = "Tier 1"
            elif "AV1 Compact Encoders" in cfs or "AV1" in cfs and any(g in rel_title.lower() for g in ["randh", "r and h", "smokindevil", "rob74k", "whiskeyjack"]):
                actual_tier = "Tier 2"
            elif "AV1" in cfs and "AV1 Nameless" in cfs:
                actual_tier = "Tier 4"
            else:
                actual_tier = "Tier 3"

            tier_counts[actual_tier] += 1

            # Expected behavior validation:
            # If Tier 1 AV1 exists in pool, expect Tier 1.
            # Else if unpenalized Tier 2 AV1 exists in pool, expect Tier 2.
            # Else expect Tier 3 x265.
            has_t1_in_pool = any("AV1 Quality Encoders" in [cf["name"] for cf in r.get("customFormats", [])] for r in eval_pool)
            has_t2_in_pool = any("AV1 Compact Encoders" in [cf["name"] for cf in r.get("customFormats", [])] and "AV1 Lean 2160p" not in [cf["name"] for cf in r.get("customFormats", [])] for r in eval_pool)

            if has_t1_in_pool:
                expected_tier = "Tier 1"
            elif has_t2_in_pool:
                expected_tier = "Tier 2"
            else:
                expected_tier = "Tier 3"

            is_match = (actual_tier == expected_tier)
            if is_match:
                matches += 1
            else:
                mismatches += 1

            results.append({
                "movie_id": mid,
                "title": m_title,
                "year": m_year,
                "has_2160p_pool": has_2160p,
                "selected_release": rel_title,
                "quality": res_str,
                "size_gb": rel_size_gb,
                "score": rel_score,
                "matched_custom_formats": cfs,
                "selected_tier": actual_tier,
                "expected_tier": expected_tier,
                "status": "MATCH" if is_match else "MISMATCH",
                "notes": f"Winning score {rel_score} in {res_str}."
            })
            print(f"  [{actual_tier}] Score {rel_score:<5} | {m_title} ({m_year}) -> {rel_title[:65]}")

    raw_data = {
        "test_metadata": {
            "operation": "OP 951A",
            "test_name": "Hybrid AV1 Profile Field Test (25 Titles)",
            "date": "2026-08-28",
            "profile_scope": "2160p-only (Movies 2160p AV1 HQ, ID 64)",
            "total_titles_tested": len(results),
            "matches": matches,
            "mismatches": mismatches,
            "match_rate_pct": round((matches / len(results)) * 100, 1) if results else 0,
            "tier_distribution": tier_counts
        },
        "per_title_results": results
    }

    with open(OUTPUT_RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2)

    print(f"\n[OK] Field test completed! Tested {len(results)} movies: {matches} matches ({raw_data['test_metadata']['match_rate_pct']}%), {mismatches} mismatches.")
    print(f"     Tier Breakdown: Tier 1: {tier_counts['Tier 1']}, Tier 2: {tier_counts['Tier 2']}, Tier 3: {tier_counts['Tier 3']}, Tier 4: {tier_counts['Tier 4']}")
    print(f"     Saved raw data to: {OUTPUT_RAW_PATH}")

if __name__ == "__main__":
    main()
