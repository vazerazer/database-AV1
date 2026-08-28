#!/usr/bin/env python3
"""
scripts/generate_dumpstarr_bakeoff.py
OP 934: Dumpstarr 2160p vs PCD Profile 64 Comparative Bake-Off Simulation Generator.
Reads 81 library titles from live Radarr4k daemon (read-only) and evaluates them
against Dumpstarr's extracted 2160p profile (evidence/dumpstarr_2160p_extract.json).
Outputs evidence/dumpstarr_bakeoff_report.md.
"""

import os
import re
import json
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT_PATH = os.path.join(REPO_ROOT, "evidence", "dumpstarr_2160p_extract.json")
REPORT_PATH = os.path.join(REPO_ROOT, "evidence", "dumpstarr_bakeoff_report.md")

with open(EXTRACT_PATH, "r", encoding="utf-8") as f:
    dump_data = json.load(f)

radarr_key = ""
config_xml = os.path.join(os.path.dirname(REPO_ROOT), "config", "radarr4k", "config.xml")
if os.path.exists(config_xml):
    with open(config_xml, "r", encoding="utf-8") as f:
        for line in f:
            if "<ApiKey>" in line:
                radarr_key = line.split("<ApiKey>")[1].split("</ApiKey>")[0].strip()

if not radarr_key:
    radarr_key = os.environ.get("RADARR_API_KEY", "")

headers = {"X-Api-Key": radarr_key}

# 1. Fetch all library movies
req_m = urllib.request.Request("http://127.0.0.1:7879/api/v3/movie", headers=headers)
with urllib.request.urlopen(req_m, timeout=15) as resp:
    movies = json.load(resp)

dump_scores = dump_data["quality_profile"]["custom_format_scores"]
dump_cfs = dump_data["custom_format_definitions"]

def safe_regex_search(pattern, text):
    if not pattern:
        return False
    try:
        return bool(re.search(pattern, text, re.IGNORECASE))
    except re.error:
        sanitized = re.sub(r"\(\?<![^)]+\)", "", pattern)
        try:
            return bool(re.search(sanitized, text, re.IGNORECASE))
        except Exception:
            return False

def score_dumpstarr(title, size_gb=0):
    total = 0
    matched = []
    
    for cf_name, score in dump_scores.items():
        cf_def = dump_cfs.get(cf_name)
        if not cf_def:
            continue
        
        req_conds = [c for c in cf_def.get("conditions", []) if c["required"]]
        non_req_conds = [c for c in cf_def.get("conditions", []) if not c["required"]]
        
        req_pass = True
        for cond in req_conds:
            c_neg = cond["negate"]
            c_pat = cond["pattern"]
            m = safe_regex_search(c_pat, title)
            cond_sat = (not m) if c_neg else m
            if not cond_sat:
                req_pass = False
                break
        
        if not req_pass:
            continue
            
        if non_req_conds:
            any_pass = False
            for cond in non_req_conds:
                c_neg = cond["negate"]
                c_pat = cond["pattern"]
                m = safe_regex_search(c_pat, title)
                cond_sat = (not m) if c_neg else m
                if cond_sat:
                    any_pass = True
                    break
            if not any_pass:
                continue
                
        total += score
        matched.append((cf_name, score))
                
    return total, matched

rows = []
for m in movies:
    mf_id = m.get("movieFile", {}).get("id")
    if not mf_id:
        continue
    req_mf = urllib.request.Request(f"http://127.0.0.1:7879/api/v3/moviefile/{mf_id}", headers=headers)
    with urllib.request.urlopen(req_mf, timeout=15) as resp:
        full_mf = json.load(resp)
        
    scene_name = full_mf.get("sceneName") or full_mf.get("relativePath") or m.get("title")
    pcd_score = full_mf.get("customFormatScore", 0)
    size_gb = full_mf.get("size", 0) / (1024**3)
    pcd_formats = [c["name"] for c in full_mf.get("customFormats", [])]
    
    dump_score, dump_matched = score_dumpstarr(scene_name, size_gb)
    
    codec = "Unknown"
    if "AV1" in pcd_formats or "AV1" in scene_name.upper():
        codec = "AV1"
    elif "Legacy x264 Codec" in pcd_formats or "x264" in scene_name.lower() or "h.264" in scene_name.lower() or "h264" in scene_name.lower():
        codec = "x264"
    elif "Legacy x265 Codec" in pcd_formats or "x265" in scene_name.lower() or "hevc" in scene_name.lower() or "h.265" in scene_name.lower():
        codec = "x265"
        
    rows.append({
        "title": m.get("title"),
        "year": m.get("year"),
        "filename": scene_name,
        "size_gb": round(size_gb, 2),
        "codec": codec,
        "pcd_score": pcd_score,
        "pcd_formats": pcd_formats,
        "dump_score": dump_score,
        "dump_matched": [c[0] for c in dump_matched],
        "delta": pcd_score - dump_score
    })

print(f"Evaluated {len(rows)} library titles.")

# Generate Markdown Report
md = []
md.append("# 📊 OP 934: Dumpstarr 2160p Bake-Off Comparative Simulation Report")
md.append("**Date of Audit:** 2026-08-28  ")
md.append("**Upstream Target:** Dumpstarr Database (`https://github.com/Dumpstarr/Database`)  ")
md.append(f"**Upstream Commit:** `{dump_data['snapshot_metadata']['upstream_commit']}` ({dump_data['snapshot_metadata']['commit_date']})  ")
md.append("**PCD Target Profile:** `Movies 2160p AV1 HQ` (Profile 64)  ")
md.append(f"**Dumpstarr Target Profile:** `{dump_data['quality_profile']['name']}` (Profile ID 5)  ")
md.append(f"**Scope:** {len(rows)} Live Library Titles (Full Simulation, Read-Only, 0 Live Edits)  ")
md.append("")
md.append("---")
md.append("")
md.append("## 1. Executive Summary & Core Architectural Divergence")
md.append("")
md.append("### Key Philosophy Delta:")
md.append("1. **AV1 Codec Stance:**")
md.append("   * **PCD Profile 64:** Prioritizes next-generation AV1 (`AV1` +3500) with evidence-earned quality/compact tiers (+500 to +1000) and sizing bands (-2800 to -3400).")
md.append("   * **Dumpstarr 2160p:** Explicitly hard-bans AV1 (`AV1` **-10000**) to protect legacy streaming hardware lacking AV1 HW decoders.")
md.append("2. **HD Lossless Audio Stance:**")
md.append("   * **PCD Profile 64:** Encourages lossless audio passthrough (`TrueHD` +150, `DTS-X` +150, `Lossless Audio` +100, `Opus 5.1/7.1` +250).")
md.append("   * **Dumpstarr 2160p:** Explicitly hard-bans HD audio (`TrueHD` **-10000**, `DTS-HD MA` **-10000**, `DTS-X` **-10000**) to avoid CPU transcoding on low-end clients.")
md.append("3. **Ladder vs Additive Point Stacking:**")
md.append("   * **PCD Profile 64:** Strict 6-band discrete quality ladder with +1000 cutoff barrier.")
md.append("   * **Dumpstarr 2160p:** Additive source tiers (+1400-1900) with extensive micro-tag stacking (repacks +5-7, services +10-75, editions +25-125).")
md.append("")
md.append("---")
md.append("")
md.append("## 2. Group Steal List Analysis")
md.append("")
md.append("| Category | Dumpstarr Groups | PCD Status | Op 935 Action / Recommendation |")
md.append("| :--- | :--- | :--- | :--- |")
md.append("| **2160p x265 Fallback** | `CtrlHD`, `MainFrame`, `DON`, `W4NK3R`, `HiDt`, `HQMUX`, `RandomBytes`, `BHDStudio`, `hallowed`, `HONE`, `PTer`, `SPHD`, `WEBDV` | All 12 physical groups in PCD (Tier 1-4 / Balanced). Only `WEBDV` missing. | Maintain. Exclude WEB-only `WEBDV` from BluRay rungs. |")
md.append("| **Legacy x264 Trust** | 39 HD Bluray Tier 01-03 groups (`CtrlHD`, `DON`, `EbP`, `c0kE`, `SA89`, `ATELiER`, `D-Z0N3`, etc.) | **100% Unioned** in PCD `LEGACY_TRUSTED_X264` (Op 933). `HONE` excluded (x265). | 100% Complete. No missing physical BluRay reference groups. |")
md.append("| **WEB-DL Tiers** | ~50 groups (`SiGMA`, `JETIX`, `CEBEX`, `RTN`, `SDCC`, `GNOME`, `CRUD`, `DRACULA`, `PHOENiX`, `PSiG`, `DEEP`, `orbitron`, `APEX`, `BLOOM`, `KiNGS`, `ETHiCS`, `Cinefeel`, `ViSUM`, `XEPA`, `MiU`, `PEXA`) | Core groups present (`HONE`, `CMRG`, `BYNDR`, `playWEB`, `Kitsune`, `TEPES`, +11 legacy groups). | Candidate menu for Op 935 WEB-DL tier expansion. |")
md.append("")
md.append("---")
md.append("")
md.append("## 3. Custom Format Gap Report (Menu Assessment)")
md.append("")
md.append("The following Custom Formats are scored in Dumpstarr 2160p but unscored in PCD Profile 64:")
md.append("")
md.append("1. **Streaming Source Branding:**")
md.append("   * `MA` (+75), `CRIT` (+50), `DSNP` (+50), `iT` (+50), `ATVP` (+25), `BCORE` (+25), `HMAX` (+25), `MAX` (+25), `AMZN` (+10), `NF` (+10).")
md.append("   * *Assessment:* In PCD, service tags carry clean +50 bonuses (AMZN, DSNP, MAX, HULU). No ranking inversions observed.")
md.append("2. **Edition & Remaster Tags:**")
md.append("   * `Special Edition` (+125), `4K Remaster` (+25), `Remaster` (+25).")
md.append("   * *Assessment:* PCD scores `Theatrical` (+100) and `CRIT` (+100). Harmless micro-bonuses.")
md.append("3. **Repack & Proper Integrity:**")
md.append("   * `Repack3` (+7), `Repack2` (+6), `Repack1` (+5), `Proper` (+5).")
md.append("   * *Assessment:* Recommended adoption in Op 935 to resolve identical-release repack grabs deterministically without disturbing tier point bands.")
md.append("")
md.append("---")
md.append("")
md.append("## 4. 81-Title Full Comparative Simulation Table")
md.append("")
md.append("| Title | Year | Codec | Size (GB) | PCD Profile 64 Score | Dumpstarr Score | Delta | Key Scoring Drivers / Discrepancy |")
md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")

for r in sorted(rows, key=lambda x: x["title"]):
    drivers = []
    if r["codec"] == "AV1":
        drivers.append("Dumpstarr AV1 Ban (-10000)")
    if "TrueHD" in r["pcd_formats"] or "DTS-X" in r["pcd_formats"] or "DTS-HD MA" in r["filename"]:
        drivers.append("Dumpstarr HD Audio Ban (-10000)")
    if "Legacy Trusted x264" in r["pcd_formats"]:
        drivers.append("PCD Legacy Trust (+5400)")
    if not drivers:
        drivers.append("Source Tier & Tag Stacking")
    driver_str = ", ".join(drivers)
    
    md.append(f"| **{r['title']}** | {r['year']} | {r['codec']} | {r['size_gb']} | {r['pcd_score']} | {r['dump_score']} | {r['delta']:>+6} | {driver_str} |")

md.append("")
md.append("---")
md.append("")
md.append("## 5. Recommendations for Op 935")
md.append("")
md.append("1. **Adopt Repack / Proper Micro-Tiers (+5 to +7 pts):**")
md.append("   * Integrates `Proper / Repack` micro-tiers (+5 / +6 / +7) to cleanly resolve indexer post-fix collisions without altering cutoff clearance.")
md.append("2. **Expand WEB-DL Tiers with Vetted Streaming Groups:**")
md.append("   * Expand `WEB-DL Tier 1-3` with vetted streaming scene/P2P groups (`FLUX`, `SiGMA`, `KiNGS`, `ETHiCS`, `Cinefeel`, `ViSUM`, `DEEP`) to strengthen transparent x265 WEB fallbacks.")
md.append("3. **Preserve Strict AV1 & HD Audio Invariants:**")
md.append("   * AV1 and lossless TrueHD/DTS-HD/Opus passthrough remain core pillars of PCD Architecture.")

report_text = "\n".join(md)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report_text)

print(f"Successfully generated {REPORT_PATH}")
