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
        "AV1 Anime Encoders", "AV1 Compact Encoders", "AV1 Storage Savers",
        "Legacy x265 Codec", "Legacy x264 Codec"
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
    print("\n=== VERIFYING BYTE-FOR-BYTE PATTERN PARITY (RADARR4K API vs PCD DB) ===")
    conn = build_compiled_db()
    
    radarr_key = "***REMOVED***"
    req = urllib.request.Request("http://127.0.0.1:7879/api/v3/customformat", headers={"X-Api-Key": radarr_key})
    with urllib.request.urlopen(req) as resp:
        radarr_cfs = json.loads(resp.read().decode("utf-8"))
        
    radarr_cfs_by_name = {cf["name"]: cf for cf in radarr_cfs}
    
    cfs_to_check = [
        "AV1", "10-bit Depth", "8-bit Depth", "Opus 5.1 / 7.1", "Opus Stereo",
        "AV1 Anime Encoders", "AV1 Compact Encoders", "AV1 Storage Savers",
        "Legacy x265 Codec", "Legacy x264 Codec"
    ]
    
    all_match = True
    for cf_name in cfs_to_check:
        # Query PCD DB
        pcd_pat = conn.execute("""
            SELECT re.pattern FROM custom_formats cf
            JOIN custom_format_conditions cfc ON cf.name = cfc.custom_format_name
            JOIN condition_patterns cp ON cfc.custom_format_name = cp.custom_format_name AND cfc.name = cp.condition_name
            JOIN regular_expressions re ON cp.regular_expression_name = re.name
            WHERE cf.name = ?
        """, (cf_name,)).fetchone()[0]
        
        radarr_cf = radarr_cfs_by_name.get(cf_name)
        if not radarr_cf:
            print(f"[FAIL] Missing in Radarr: {cf_name}")
            all_match = False
            continue
            
        deployed_pat = radarr_cf["specifications"][0]["fields"][0]["value"]
        
        if pcd_pat == deployed_pat:
            print(f"[MATCH] {cf_name}")
            print(f"        PCD:      {repr(pcd_pat)}")
            print(f"        Deployed: {repr(deployed_pat)}")
        else:
            print(f"[MISMATCH] {cf_name}")
            print(f"        PCD:      {repr(pcd_pat)}")
            print(f"        Deployed: {repr(deployed_pat)}")
            all_match = False
            
    return all_match

if __name__ == "__main__":
    sync_entities()
    parity = verify_byte_for_byte_parity()
    if not parity:
        sys.exit(1)
