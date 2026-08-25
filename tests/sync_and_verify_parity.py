#!/usr/bin/env python3
"""
Sync all AV1 Custom Formats and Quality Profiles from Profilarr to Radarr4k / Sonarr4k
with cooldown handling, and verify byte-for-byte pattern parity between repository and Arr API.

Requires the following environment variables:
  RADARR_API_KEY  - API key for Radarr instance
  SONARR_API_KEY  - API key for Sonarr instance
Optional environment variables:
  PROFILARR_URL   - Base URL for Profilarr (default: http://127.0.0.1:5656)
  RADARR_URL      - Base URL for Radarr (default: http://127.0.0.1:7879)
  SONARR_URL      - Base URL for Sonarr (default: http://127.0.0.1:8990)
  PROFILARR_COOKIE - Optional session cookie for Profilarr if auth is required
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate_scoring import build_compiled_db

PROFILARR_URL = os.environ.get("PROFILARR_URL", "http://127.0.0.1:5656")
PROFILARR_COOKIE = os.environ.get("PROFILARR_COOKIE", "")
RADARR_URL = os.environ.get("RADARR_URL", "http://127.0.0.1:7879")
SONARR_URL = os.environ.get("SONARR_URL", "http://127.0.0.1:8990")
RADARR_API_KEY = os.environ.get("RADARR_API_KEY")
SONARR_API_KEY = os.environ.get("SONARR_API_KEY")

def get_required_api_keys():
    errors = []
    if not RADARR_API_KEY:
        errors.append("RADARR_API_KEY environment variable is required but not set.")
    if not SONARR_API_KEY:
        errors.append("SONARR_API_KEY environment variable is required but not set.")
    if errors:
        for err in errors:
            print(f"Error: {err}", file=sys.stderr)
        print("\nUsage example:", file=sys.stderr)
        print("  RADARR_API_KEY='your_radarr_key' SONARR_API_KEY='your_sonarr_key' python3 tests/sync_and_verify_parity.py", file=sys.stderr)
        sys.exit(1)

def send_profilarr_post(endpoint, body):
    headers = {"Content-Type": "application/json"}
    if PROFILARR_COOKIE:
        headers["Cookie"] = PROFILARR_COOKIE
        
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                f"{PROFILARR_URL}{endpoint}",
                data=json.dumps(body).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode("utf-8")
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return {"auth_required": True, "raw": raw[:100]}
        except urllib.error.HTTPError as e:
            if e.code == 409:
                time.sleep(5.5)
            elif e.code == 401 or e.code == 403:
                return {"auth_required": True}
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
        if isinstance(res, dict) and res.get("auth_required"):
            print("  [INFO] Profilarr web authentication is required to trigger sync via HTTP.")
            print("         (Provide PROFILARR_COOKIE if automated remote resync is needed).")
            print("         Skipping HTTP resync step and proceeding to live API byte parity check.")
            return
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
    get_required_api_keys()
    conn = build_compiled_db()
    all_match = True
    
    # 1. RADARR4K
    print("\n=== VERIFYING BYTE-FOR-BYTE PATTERN PARITY (RADARR4K API vs PCD DB) ===")
    req = urllib.request.Request(f"{RADARR_URL}/api/v3/customformat", headers={"X-Api-Key": RADARR_API_KEY})
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
    req_sonarr = urllib.request.Request(f"{SONARR_URL}/api/v3/customformat", headers={"X-Api-Key": SONARR_API_KEY})
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
    get_required_api_keys()
    sync_entities()
    parity = verify_byte_for_byte_parity()
    if not parity:
        sys.exit(1)
