#!/usr/bin/env python3
"""
Sync all AV1 Custom Formats and Quality Profiles from Profilarr to Radarr4k / Sonarr4k
with cooldown handling, and verify byte-for-byte pattern parity between repository and Arr API.
"""

import urllib.request
import json
import time
import sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate_scoring import build_compiled_db

PROFILARR_URL = "http://127.0.0.1:5656"
SESSION_COOKIE = "session=868c6ac4-d0c2-43a2-bde2-bd8bda1a5d68"

def send_profilarr_post(endpoint, body):
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                f"{PROFILARR_URL}{endpoint}",
                data=json.dumps(body).encode("utf-8"),
                headers={
                    "Cookie": SESSION_COOKIE,
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 409:
                # Cooldown active, wait 5.5s
                time.sleep(5.5)
            else:
                raise

def sync_entities():
    cfs = [
        "AV1", "Not AV1", "10-bit Depth", "8-bit Depth", "Opus 5.1 / 7.1", "Opus Stereo",
        "AV1 Anime Encoders", "AV1 Compact Encoders", "AV1 Storage Savers", "AV1 Quality Encoders",
        "Legacy x265 Codec", "Legacy x264 Codec", "CAM", "Banned Groups"
    ]
    
    profiles_radarr = [
        "Movies 2160p AV1 HQ"
    ]
    
    profiles_sonarr = [
        "TV 2160p AV1"
    ]
    
    print("=== SYNCING TO RADARR4K (Instance 2) ===")
    for cf in cfs:
        res = send_profilarr_post("/arr/2/resync", {
            "databaseId": 9, "entityType": "customFormat", "entityName": cf
        })
        print(f"  CF '{cf}': {res}")
        time.sleep(5.5)
        
    for p in profiles_radarr:
        res = send_profilarr_post("/arr/2/resync", {
            "databaseId": 9, "entityType": "qualityProfile", "entityName": p
        })
        print(f"  Profile '{p}': {res}")
        time.sleep(5.5)

    print("\n=== SYNCING TO SONARR4K (Instance 4) ===")
    for cf in cfs:
        res = send_profilarr_post("/arr/4/resync", {
            "databaseId": 9, "entityType": "customFormat", "entityName": cf
        })
        print(f"  CF '{cf}': {res}")
        time.sleep(5.5)
        
    for p in profiles_sonarr:
        res = send_profilarr_post("/arr/4/resync", {
            "databaseId": 9, "entityType": "qualityProfile", "entityName": p
        })
        print(f"  Profile '{p}': {res}")
        time.sleep(5.5)

def verify_byte_for_byte_parity():
    conn = build_compiled_db()
    all_match = True
    
    # 1. RADARR4K
    print("\n=== VERIFYING BYTE-FOR-BYTE PATTERN PARITY (RADARR4K API vs PCD DB) ===")
    radarr_key = "***REMOVED***"
    req = urllib.request.Request("http://127.0.0.1:7879/api/v3/customformat", headers={"X-Api-Key": radarr_key})
    with urllib.request.urlopen(req) as resp:
        radarr_cfs = json.loads(resp.read().decode("utf-8"))
    radarr_cfs_by_name = {cf["name"]: cf for cf in radarr_cfs}
    
    cfs_to_check = [
        "AV1", "10-bit Depth", "8-bit Depth", "Opus 5.1 / 7.1", "Opus Stereo",
        "AV1 Anime Encoders", "AV1 Compact Encoders", "AV1 Storage Savers", "AV1 Quality Encoders",
        "Legacy x265 Codec", "Legacy x264 Codec", "CAM"
    ]
    
    for cf_name in cfs_to_check:
        pcd_pat = conn.execute("""
            SELECT re.pattern FROM custom_formats cf
            JOIN custom_format_conditions cfc ON cf.name = cfc.custom_format_name
            JOIN condition_patterns cp ON cfc.custom_format_name = cp.custom_format_name AND cfc.name = cp.condition_name
            JOIN regular_expressions re ON cp.regular_expression_name = re.name
            WHERE cf.name = ?
        """, (cf_name,)).fetchone()[0]
        
        radarr_cf = radarr_cfs_by_name.get(cf_name)
        if not radarr_cf:
            print(f"[FAIL] Missing in Radarr4k: {cf_name}")
            all_match = False
            continue
            
        deployed_pat = radarr_cf["specifications"][0]["fields"][0]["value"]
        if pcd_pat == deployed_pat:
            print(f"[MATCH] {cf_name:<25}")
            print(f"        PCD:      {repr(pcd_pat)}")
            print(f"        Deployed: {repr(deployed_pat)}")
        else:
            print(f"[MISMATCH] {cf_name:<25}")
            print(f"        PCD:      {repr(pcd_pat)}")
            print(f"        Deployed: {repr(deployed_pat)}")
            all_match = False

    # Check ENTROPY in Banned Groups (Radarr4k)
    pcd_entropy = conn.execute("SELECT pattern FROM regular_expressions WHERE name = 'ENTROPY'").fetchone()[0]
    banned_cfs = radarr_cfs_by_name.get("Banned Groups", {})
    deployed_entropy_spec = next((s for s in banned_cfs.get("specifications", []) if s.get("name") == "ENTROPY"), None)
    if deployed_entropy_spec:
        deployed_entropy = deployed_entropy_spec["fields"][0]["value"]
        if pcd_entropy == deployed_entropy:
            print(f"[MATCH] {'Banned Groups (ENTROPY)':<25}")
            print(f"        PCD:      {repr(pcd_entropy)}")
            print(f"        Deployed: {repr(deployed_entropy)}")
        else:
            print(f"[MISMATCH] {'Banned Groups (ENTROPY)':<25}")
            print(f"        PCD:      {repr(pcd_entropy)}")
            print(f"        Deployed: {repr(deployed_entropy)}")
            all_match = False
    else:
        print("[FAIL] Missing ENTROPY condition in Radarr4k Banned Groups")
        all_match = False

    # 2. SONARR4K
    print("\n=== VERIFYING BYTE-FOR-BYTE PATTERN PARITY (SONARR4K API vs PCD DB) ===")
    sonarr_key = "***REMOVED***"
    req_sonarr = urllib.request.Request("http://127.0.0.1:8990/api/v3/customformat", headers={"X-Api-Key": sonarr_key})
    with urllib.request.urlopen(req_sonarr) as resp:
        sonarr_cfs = json.loads(resp.read().decode("utf-8"))
    sonarr_cfs_by_name = {cf["name"]: cf for cf in sonarr_cfs}

    for cf_name in cfs_to_check:
        pcd_pat = conn.execute("""
            SELECT re.pattern FROM custom_formats cf
            JOIN custom_format_conditions cfc ON cf.name = cfc.custom_format_name
            JOIN condition_patterns cp ON cfc.custom_format_name = cp.custom_format_name AND cfc.name = cp.condition_name
            JOIN regular_expressions re ON cp.regular_expression_name = re.name
            WHERE cf.name = ?
        """, (cf_name,)).fetchone()[0]
        
        sonarr_cf = sonarr_cfs_by_name.get(cf_name)
        if not sonarr_cf:
            print(f"[FAIL] Missing in Sonarr4k: {cf_name}")
            all_match = False
            continue
            
        deployed_pat = sonarr_cf["specifications"][0]["fields"][0]["value"]
        if pcd_pat == deployed_pat:
            print(f"[MATCH] {cf_name:<25}")
            print(f"        PCD:      {repr(pcd_pat)}")
            print(f"        Deployed: {repr(deployed_pat)}")
        else:
            print(f"[MISMATCH] {cf_name:<25}")
            print(f"        PCD:      {repr(pcd_pat)}")
            print(f"        Deployed: {repr(deployed_pat)}")
            all_match = False

    # Check ENTROPY in Banned Groups (Sonarr4k)
    banned_cfs_sonarr = sonarr_cfs_by_name.get("Banned Groups", {})
    deployed_entropy_spec_s = next((s for s in banned_cfs_sonarr.get("specifications", []) if s.get("name") == "ENTROPY"), None)
    if deployed_entropy_spec_s:
        deployed_entropy_s = deployed_entropy_spec_s["fields"][0]["value"]
        if pcd_entropy == deployed_entropy_s:
            print(f"[MATCH] {'Banned Groups (ENTROPY)':<25}")
            print(f"        PCD:      {repr(pcd_entropy)}")
            print(f"        Deployed: {repr(deployed_entropy_s)}")
        else:
            print(f"[MISMATCH] {'Banned Groups (ENTROPY)':<25}")
            print(f"        PCD:      {repr(pcd_entropy)}")
            print(f"        Deployed: {repr(deployed_entropy_s)}")
            all_match = False
    else:
        print("[FAIL] Missing ENTROPY condition in Sonarr4k Banned Groups")
        all_match = False

    return all_match

if __name__ == "__main__":
    sync_entities()
    parity = verify_byte_for_byte_parity()
    if not parity:
        sys.exit(1)
