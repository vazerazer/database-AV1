#!/usr/bin/env python3
"""
scripts/run_av1_expanded_three_way_campaign_944a.py
AV1 Library Group Inventory and Expanded Three-Way Baseline Campaign Runner (Op 944A)
Measures:
- Hallowed 2160p x265 -> AV1 candidate (Incremental quality delta against accepted baseline)
Outputs evidence/av1_expanded_three_way_campaign_raw_944a.json.
"""

import os
import re
import sys
import json
import statistics
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.dirname(REPO_ROOT)

FFMPEG_BIN = os.environ.get("FFMPEG_BIN") or os.path.join(MEDIA_ROOT, "scratch", "bin", "ffmpeg")
FFPROBE_BIN = os.environ.get("FFPROBE_BIN") or os.path.join(MEDIA_ROOT, "scratch", "bin", "ffprobe")
MODEL_4K = os.environ.get("VMAF_MODEL_4K") or os.path.join(MEDIA_ROOT, "scratch", "models", "vmaf_4k_v0.6.1.json")

ALTMOUNT_M4K = os.path.join(MEDIA_ROOT, "library", "altmount", "complete", "movies4k")

def get_stream_info(path):
    if not path or not os.path.exists(path):
        return None
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
        h = int(stream.get("height", 1600))
        r_fr = stream.get("r_frame_rate", "24000/1001")
        fps = eval(r_fr) if "/" in r_fr else float(r_fr)
        br = int(fmt.get("bit_rate") or stream.get("bit_rate") or 0)
        dur = float(fmt.get("duration", 0))
        sz = int(fmt.get("size", 0))
        if br == 0 and dur > 0 and sz > 0:
            br = int((sz * 8) / dur)
        return {"width": w, "height": h, "fps": fps, "bitrate_bps": br, "duration_sec": dur, "size_bytes": sz}
    except Exception:
        return {"width": 3840, "height": 1600, "fps": 23.976, "bitrate_bps": 0, "duration_sec": 0, "size_bytes": 0}

def measure_pair(ref_path, dist_path, start, dur_sec, scale_w, scale_h, ref_crop_str, dist_crop_str, offset_sec, tmp_dir, label):
    sanitized_label = re.sub(r'[^a-zA-Z0-9_-]', '_', label)
    log_json = os.path.join(tmp_dir, f"vmaf_{os.getpid()}_{sanitized_label}.json")
    if os.path.exists(log_json):
        os.remove(log_json)

    start_sec = 0.0
    if isinstance(start, str) and ":" in start:
        parts = start.split(":")
        start_sec = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    else:
        start_sec = float(start)

    dist_start_sec = start_sec + offset_sec
    if dist_start_sec < 0:
        dist_start_sec = 0.0

    filter_chain = (
        f"[0:v]{ref_crop_str}scale={scale_w}:{scale_h}:flags=bicubic,format=yuv420p10le[ref];"
        f"[1:v]{dist_crop_str}scale={scale_w}:{scale_h}:flags=bicubic,format=yuv420p10le[dist];"
        f"[dist][ref]libvmaf=model=path={MODEL_4K}:feature=name=psnr|name=float_ssim:log_fmt=json:log_path={log_json}"
    )

    cmd = [
        FFMPEG_BIN,
        "-ss", str(start_sec), "-t", str(dur_sec), "-i", ref_path,
        "-ss", str(dist_start_sec), "-t", str(dur_sec), "-i", dist_path,
        "-filter_complex", filter_chain,
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
        "psnr_y_db": round(psnr, 2),
        "ssim": round(ssim, 4)
    }

def main():
    manifest_path = os.path.join(REPO_ROOT, "evidence", "av1_expanded_three_way_manifest_944a.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("================================================================================")
    print("OP 944A: AV1 EXPANDED THREE-WAY BASELINE CAMPAIGN")
    print("================================================================================")

    tmp_dir = os.path.join(MEDIA_ROOT, "scratch", "calibration_op944a")
    os.makedirs(tmp_dir, exist_ok=True)

    results = []

    for title_entry in manifest["planned_titles"]:
        title = title_entry["title"]
        yr = title_entry["year"]
        grp = title_entry["group"]
        offset_sec = float(title_entry.get("alignment_offset_ms", 0)) / 1000.0

        print(f"\n>>> Calibrating Group [{grp}]: {title} ({yr})")

        if title == "X-Men: Dark Phoenix":
            hal_path = os.path.join(ALTMOUNT_M4K, "X-Men.Dark.Phoenix.2019.UHD.BluRay.2160p.DDP.7.1.HDR10Plus.x265-hallowed", "X-Men.Dark.Phoenix.2019.UHD.BluRay.2160p.DDP.7.1.HDR10Plus.x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "X-Men Dark Phoenix-2019-UHD BluRay AV1 10bit HDR10 AC3 5.1 AV1-ChopperHitler", "X-Men Dark Phoenix-2019-UHD BluRay AV1 10bit HDR10 AC3 5.1 AV1-ChopperHitler.mkv")
            scale_w, scale_h = 3840, 1604
        elif title == "The Bourne Ultimatum" and grp == "RandH":
            hal_path = os.path.join(ALTMOUNT_M4K, "The.Bourne.Ultimatum.2007.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed", "The.Bourne.Ultimatum.2007.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "The.Bourne.Ultimatum.2007-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H", "The.Bourne.Ultimatum.2007-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H.mkv")
            scale_w, scale_h = 3840, 1600
        elif title == "The Bourne Ultimatum" and grp == "Bi0hazard":
            hal_path = os.path.join(ALTMOUNT_M4K, "The.Bourne.Ultimatum.2007.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed", "The.Bourne.Ultimatum.2007.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "Das.Bourne.Ultimatum.2007.German.DUBBED.DL.EAC3.2160p.HDR.BluRay.AV1-Bi0hazard", "Das.Bourne.Ultimatum.2007.German.DUBBED.DL.EAC3.2160p.HDR.BluRay.AV1-Bi0hazard.mkv")
            scale_w, scale_h = 3840, 1600
        elif title == "The Shawshank Redemption":
            hal_path = os.path.join(ALTMOUNT_M4K, "The.Shawshank.Redemption.1994.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed", "The.Shawshank.Redemption.1994.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "The.Shawshank.Redemption.1994.2160p.UHD.BluRay.DD+5.1.HDR.AV1-Smokindevil", "The.Shawshank.Redemption.1994.2160p.UHD.BluRay.DD+5.1.HDR.AV1-Smokindevil.mkv")
            scale_w, scale_h = 3840, 2076
        elif title == "The Sixth Sense":
            hal_path = os.path.join(ALTMOUNT_M4K, "The.Sixth.Sense.1999.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed", "The.Sixth.Sense.1999.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "The.Sixth.Sense.1999.2160p.UHD.BluRay.HDR10.DD+5.1.AV1-Smokindevil", "The.Sixth.Sense.1999.2160p.UHD.BluRay.HDR10.DD+5.1.AV1-Smokindevil.mkv")
            scale_w, scale_h = 3840, 2076
        elif title == "John Wick: Chapter 2":
            hal_path = os.path.join(ALTMOUNT_M4K, "John.Wick.Chapter.2.2017.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed", "John.Wick.Chapter.2.2017.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "John.Wick.Chapter.2.2017.BluRay.2160p.UHD.AV1.HDR10.TrueHD.7.1.Atmos.PRL.Waldek", "John.Wick.Chapter.2.2017.BluRay.2160p.UHD.AV1.HDR10.TrueHD.7.1.Atmos.PRL.Waldek.mkv")
            scale_w, scale_h = 3840, 1600
        else:
            print(f"Unknown title: {title}")
            continue

        hal_info = get_stream_info(hal_path)
        av1_info = get_stream_info(av1_path)

        hal_mbps = round(hal_info["bitrate_bps"] / 1e6, 2) if hal_info else 0.0
        av1_mbps = round(av1_info["bitrate_bps"] / 1e6, 2) if av1_info else 0.0

        pixels_per_sec = scale_w * scale_h * hal_info["fps"]
        hal_bpp = round(hal_info["bitrate_bps"] / pixels_per_sec, 4) if pixels_per_sec > 0 else 0.0
        av1_bpp = round(av1_info["bitrate_bps"] / pixels_per_sec, 4) if pixels_per_sec > 0 else 0.0

        print(f"  Hallowed Baseline: {hal_mbps} Mbps | Size: {round(hal_info['size_bytes']/1e9, 2)} GB | BPP: {hal_bpp}")
        print(f"  AV1 Candidate:     {av1_mbps} Mbps | Size: {round(av1_info['size_bytes']/1e9, 2)} GB | BPP: {av1_bpp}")

        scene_measurements = []
        for sc in title_entry["scenes"]:
            opt_tag = " (Optional 4th Scene)" if sc.get("is_optional") else ""
            print(f"  Measuring Scene {sc['scene_number']}: {sc['name']}{opt_tag} [{sc['start_timestamp']} (10s)]...")

            res_hal_av1 = measure_pair(
                hal_path, av1_path,
                sc["start_timestamp"], sc["duration_sec"],
                scale_w, scale_h,
                "", "", offset_sec,
                tmp_dir, f"{grp}_{title}_s{sc['scene_number']}"
            )
            print(f"    [Hallowed -> AV1]  VMAF: {res_hal_av1['vmaf']} | PSNR-Y: {res_hal_av1['psnr_y_db']} dB | SSIM: {res_hal_av1['ssim']}")

            sc_record = {
                "scene_number": sc["scene_number"],
                "scene_name": sc["name"],
                "category": sc["category"],
                "start_timestamp": sc["start_timestamp"],
                "duration_sec": sc["duration_sec"],
                "rationale": sc["rationale"],
                "is_optional": sc.get("is_optional", False),
                "status": "ACCEPTED",
                "comparisons": {
                    "hallowed_to_av1": res_hal_av1
                }
            }
            scene_measurements.append(sc_record)

        core_scenes = [s for s in scene_measurements if not s.get("is_optional")]
        core_vmafs = [s["comparisons"]["hallowed_to_av1"]["vmaf"] for s in core_scenes]
        all_vmafs = [s["comparisons"]["hallowed_to_av1"]["vmaf"] for s in scene_measurements]

        mean_vmaf = round(sum(core_vmafs) / len(core_vmafs), 2)
        med_vmaf = round(statistics.median(core_vmafs), 2)
        min_vmaf = min(all_vmafs)
        mean_psnr = round(sum(s["comparisons"]["hallowed_to_av1"]["psnr_y_db"] for s in core_scenes) / len(core_scenes), 2)
        mean_ssim = round(sum(s["comparisons"]["hallowed_to_av1"]["ssim"] for s in core_scenes) / len(core_scenes), 4)

        title_summary = {
            "title": title,
            "year": yr,
            "edition": title_entry["edition"],
            "group": grp,
            "hallowed_identity": title_entry["hallowed_identity"],
            "av1_identity": title_entry["av1_identity"],
            "hallowed_bitrate_mbps": hal_mbps,
            "av1_bitrate_mbps": av1_mbps,
            "hallowed_bpp": hal_bpp,
            "av1_bpp": av1_bpp,
            "resolution": f"{scale_w}x{scale_h}",
            "alignment_offset_ms": title_entry.get("alignment_offset_ms", 0),
            "scenes": scene_measurements,
            "aggregates": {
                "hallowed_to_av1": {
                    "mean_vmaf_core": mean_vmaf,
                    "median_vmaf_core": med_vmaf,
                    "min_vmaf_all": min_vmaf,
                    "mean_psnr_y_db_core": mean_psnr,
                    "mean_ssim_core": mean_ssim
                }
            }
        }
        results.append(title_summary)

    out_json = os.path.join(REPO_ROOT, "evidence", "av1_expanded_three_way_campaign_raw_944a.json")
    output_data = {
        "campaign": manifest["manifest_metadata"]["campaign_name"],
        "date": manifest["manifest_metadata"]["date"],
        "purpose": manifest["manifest_metadata"]["purpose"],
        "acceptance_premise": manifest["manifest_metadata"]["acceptance_premise"],
        "guardrails": manifest["manifest_metadata"]["guardrails"],
        "titles": results
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[OK] Saved expanded campaign raw metrics to {out_json}")

if __name__ == "__main__":
    main()
