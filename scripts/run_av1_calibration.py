#!/usr/bin/env python3
"""
scripts/run_av1_calibration.py
AV1 Fidelity Calibration Runner (Op 938)
Measures empirical perceptual quality (VMAF, PSNR, SSIM, bpp, and fidelity-per-bit)
across 4 calibrated UHD BluRay AV1 vs Reference Master pairs.
"""

import os
import sys
import json
import shutil
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.dirname(REPO_ROOT)

FFMPEG_BIN = os.environ.get("FFMPEG_BIN") or os.path.join(MEDIA_ROOT, "scratch", "bin", "ffmpeg")
FFPROBE_BIN = os.environ.get("FFPROBE_BIN") or os.path.join(MEDIA_ROOT, "scratch", "bin", "ffprobe")
MODEL_4K = os.environ.get("VMAF_MODEL_4K") or os.path.join(MEDIA_ROOT, "scratch", "models", "vmaf_4k_v0.6.1.json")
MODEL_HD = os.environ.get("VMAF_MODEL_HD") or os.path.join(MEDIA_ROOT, "scratch", "models", "vmaf_v0.6.1.json")

ALTMOUNT_M4K = os.path.join(MEDIA_ROOT, "library", "altmount", "complete", "movies4k")

ANCHORS = [
    {
        "title": "Fury (2014)",
        "year": 2014,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "Smokindevil",
        "av1_tier": "Quality Tier 2",
        "av1_rel_path": "Fury.2014.2160p.UHD.BluRay.DV.HDR10.TrueHD.7.1.Atmos.AV1-Smokindevil/Fury.2014.2160p.UHD.BluRay.DV.HDR10.TrueHD.7.1.Atmos.AV1-Smokindevil.mkv",
        "ref_group": "BHDStudio",
        "ref_format": "2160p x265 HDR/DV",
        "ref_rel_path": "Fury.2014.PROPER.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-BHDStudio/Fury.2014.PROPER.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-BHDStudio.mp4",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Dusk tank interior & low-key shadows", "start": "00:45:00", "duration": 10},
            {"name": "High-Motion", "desc": "Town square crossfire & rapid artillery", "start": "01:18:20", "duration": 10},
            {"name": "Film Grain", "desc": "Muddy tank column 35mm film texture", "start": "00:12:30", "duration": 10}
        ]
    },
    {
        "title": "John Wick: Chapter 4 (2023)",
        "year": 2023,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "CoSMiCSuRFeR",
        "av1_tier": "Quality Tier 1",
        "av1_rel_path": "John.Wick.Chapter.4.2023.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR/John.Wick.Chapter.4.2023.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR/DV",
        "ref_rel_path": "John.Wick.Chapter.4.2023.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed/John.Wick.Chapter.4.2023.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Osaka Continental neon hallway shadows", "start": "00:28:10", "duration": 10},
            {"name": "High-Motion", "desc": "Arc de Triomphe vehicular gunfight", "start": "01:42:00", "duration": 10},
            {"name": "Film Grain / Texture", "desc": "Sacre-Cœur dawn steps fine architecture", "start": "02:05:30", "duration": 10}
        ]
    },
    {
        "title": "The Shawshank Redemption (1994)",
        "year": 1994,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "Smokindevil",
        "av1_tier": "Quality Tier 2",
        "av1_rel_path": "The.Shawshank.Redemption.1994.2160p.UHD.BluRay.DD+5.1.HDR.AV1-Smokindevil/The.Shawshank.Redemption.1994.2160p.UHD.BluRay.DD+5.1.HDR.AV1-Smokindevil.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR/DV",
        "ref_rel_path": "The.Shawshank.Redemption.1994.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed/The.Shawshank.Redemption.1994.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Cell block night solitary shadows", "start": "00:15:30", "duration": 10},
            {"name": "High-Motion", "desc": "Rainstorm sewage pipe lightning escape", "start": "01:52:10", "duration": 10},
            {"name": "Film Grain", "desc": "Prison yard 35mm atmospheric film grain", "start": "00:38:00", "duration": 10}
        ]
    },
    {
        "title": "Interstellar (2014)",
        "year": 2014,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "RandH",
        "av1_tier": "Compact Tier",
        "av1_rel_path": "Interstellar.2014.2160p.BluRay.DTS-HD.MA.5.1.DV.HDR.AV1-R and H/Interstellar.2014.2160p.BluRay.DTS-HD.MA.5.1.DV.HDR.AV1-R and H.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR/DV",
        "ref_rel_path": "Interstellar 2014 IMAX UHD BluRay 2160p DDP 5 1 DV HDR x265-hallowed/Interstellar 2014 IMAX UHD BluRay 2160p DDP 5 1 DV HDR x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Wormhole entry dark cabin instrumentation", "start": "01:02:10", "duration": 10},
            {"name": "High-Motion", "desc": "Miller's planet tidal wave escape", "start": "01:21:40", "duration": 10},
            {"name": "Film Grain / Texture", "desc": "Dust storm cornfield 35mm IMAX texture", "start": "00:08:20", "duration": 10}
        ]
    }
]

def get_stream_info(path):
    cmd = [
        FFPROBE_BIN, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,bit_rate",
        "-show_entries", "format=size,duration,bit_rate",
        "-of", "json", path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(res.stdout)
        stream = data.get("streams", [{}])[0]
        fmt = data.get("format", {})
        w = int(stream.get("width", 3840))
        h = int(stream.get("height", 2160))
        r_fr = stream.get("r_frame_rate", "24/1")
        fps = eval(r_fr) if "/" in r_fr else float(r_fr)
        br = int(fmt.get("bit_rate") or stream.get("bit_rate") or 0)
        return {"width": w, "height": h, "fps": fps, "bitrate_bps": br}
    except Exception:
        return {"width": 3840, "height": 2160, "fps": 23.976, "bitrate_bps": 0}

def find_best_offset(av1_path, ref_path, timestamp_str):
    parts = timestamp_str.split(":")
    t_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    
    best_offset_ms = 0
    best_psnr = -1.0
    
    for offset_ms in [-84, -42, 0, 42, 84]:
        t_ref = t_sec + (offset_ms / 1000.0)
        cmd = [
            FFMPEG_BIN,
            "-ss", str(t_sec), "-t", "1", "-i", av1_path,
            "-ss", str(t_ref), "-t", "1", "-i", ref_path,
            "-filter_complex",
            "[0:v]crop=3840:1600:(in_w-3840)/2:(in_h-1600)/2,format=yuv420p10le[v0];[1:v]crop=3840:1600:(in_w-3840)/2:(in_h-1600)/2,format=yuv420p10le[v1];[v0][v1]psnr",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        psnr_line = [l for l in res.stderr.splitlines() if "PSNR y:" in l]
        if psnr_line:
            try:
                val = float(psnr_line[0].split("average:")[1].split()[0])
                if val > best_psnr:
                    best_psnr = val
                    best_offset_ms = offset_ms
            except Exception:
                pass
    return best_offset_ms

def measure_scene(av1_path, ref_path, scene_info, tmp_dir):
    start = scene_info["start"]
    dur = str(scene_info["duration"])
    offset_ms = find_best_offset(av1_path, ref_path, start)
    
    parts = start.split(":")
    t_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    t_ref = str(t_sec + (offset_ms / 1000.0))
    
    log_json = os.path.join(tmp_dir, f"vmaf_{os.getpid()}_{scene_info['name'].replace(' ', '_').replace('/', '_')}.json")
    if os.path.exists(log_json):
        os.remove(log_json)
        
    cmd = [
        FFMPEG_BIN,
        "-ss", start, "-t", dur, "-i", av1_path,
        "-ss", t_ref, "-t", dur, "-i", ref_path,
        "-filter_complex",
        f"[0:v]crop=3840:1600:(in_w-3840)/2:(in_h-1600)/2,format=yuv420p10le[dist];[1:v]crop=3840:1600:(in_w-3840)/2:(in_h-1600)/2,format=yuv420p10le[ref];[dist][ref]libvmaf=model=path={MODEL_4K}:feature=name=psnr|name=float_ssim:log_fmt=json:log_path={log_json}",
        "-f", "null", "-"
    ]
    
    subprocess.run(cmd, capture_output=True, text=True)
    
    vmaf = 0.0
    psnr = 0.0
    ssim = 0.0
    
    if os.path.exists(log_json):
        try:
            with open(log_json, "r") as f:
                d = json.load(f)
            pooled = d.get("pooled_metrics", {})
            vmaf = float(pooled.get("vmaf", {}).get("mean", 0.0))
            psnr = float(pooled.get("psnr_y", {}).get("mean", 0.0))
            ssim = float(pooled.get("float_ssim", {}).get("mean", 0.0))
        except Exception:
            pass
        finally:
            if os.path.exists(log_json):
                os.remove(log_json)
                
    return {
        "vmaf": round(vmaf, 2),
        "psnr_db": round(psnr, 2),
        "ssim": round(ssim, 4),
        "aligned_offset_ms": offset_ms
    }

def main():
    print("================================================================================")
    print("OP 938: AV1 FIDELITY CALIBRATION STUDY (MEASUREMENT SUITE)")
    print("================================================================================")
    
    tmp_dir = os.path.join(MEDIA_ROOT, "scratch", "calibration")
    os.makedirs(tmp_dir, exist_ok=True)
    
    results = []
    
    for anchor in ANCHORS:
        title = anchor["title"]
        print(f"\n>>> Analyzing Anchor: {title} ({anchor['av1_group']} vs {anchor['ref_group']})")
        
        av1_full = os.path.join(ALTMOUNT_M4K, anchor["av1_rel_path"])
        ref_full = os.path.join(ALTMOUNT_M4K, anchor["ref_rel_path"])
        
        av1_info = get_stream_info(av1_full)
        ref_info = get_stream_info(ref_full)
        
        av1_mbps = round(av1_info["bitrate_bps"] / 1_000_000, 2)
        ref_mbps = round(ref_info["bitrate_bps"] / 1_000_000, 2)
        
        pixels_per_sec = av1_info["width"] * av1_info["height"] * av1_info["fps"]
        bpp = round(av1_info["bitrate_bps"] / pixels_per_sec, 4) if pixels_per_sec > 0 else 0.0
        
        anchor_data = {
            "title": title,
            "year": anchor["year"],
            "edition": anchor["edition"],
            "av1_group": anchor["av1_group"],
            "av1_tier": anchor["av1_tier"],
            "av1_bitrate_mbps": av1_mbps,
            "ref_group": anchor["ref_group"],
            "ref_format": anchor["ref_format"],
            "ref_bitrate_mbps": ref_mbps,
            "bpp": bpp,
            "scenes": []
        }
        
        for sc in anchor["scenes"]:
            print(f"  Measuring Scene: {sc['name']} [{sc['start']} (10s)]...")
            metrics = measure_scene(av1_full, ref_full, sc, tmp_dir)
            
            vmaf_per_mbps = round(metrics["vmaf"] / av1_mbps, 2) if av1_mbps > 0 else 0.0
            
            sc_result = {
                "scene_name": sc["name"],
                "description": sc["desc"],
                "timestamp": sc["start"],
                "duration_sec": sc["duration"],
                "vmaf": metrics["vmaf"],
                "psnr_db": metrics["psnr_db"],
                "ssim": metrics["ssim"],
                "vmaf_per_mbps": vmaf_per_mbps,
                "offset_ms": metrics["aligned_offset_ms"]
            }
            print(f"    -> VMAF: {metrics['vmaf']} | PSNR: {metrics['psnr_db']} dB | SSIM: {metrics['ssim']} | Offset: {metrics['aligned_offset_ms']:+d}ms")
            anchor_data["scenes"].append(sc_result)
            
        avg_vmaf = round(sum(s["vmaf"] for s in anchor_data["scenes"]) / len(anchor_data["scenes"]), 2)
        avg_psnr = round(sum(s["psnr_db"] for s in anchor_data["scenes"]) / len(anchor_data["scenes"]), 2)
        avg_ssim = round(sum(s["ssim"] for s in anchor_data["scenes"]) / len(anchor_data["scenes"]), 4)
        avg_vmaf_per_mbps = round(avg_vmaf / av1_mbps, 2) if av1_mbps > 0 else 0.0
        
        anchor_data["aggregate"] = {
            "mean_vmaf": avg_vmaf,
            "mean_psnr_db": avg_psnr,
            "mean_ssim": avg_ssim,
            "mean_vmaf_per_mbps": avg_vmaf_per_mbps
        }
        results.append(anchor_data)
        
    out_json = os.path.join(REPO_ROOT, "evidence", "av1_calibration_raw.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Saved raw calibration data to {out_json}")

if __name__ == "__main__":
    main()
