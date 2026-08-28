#!/usr/bin/env python3
"""
scripts/run_hallowed_baseline_calibration.py
Hallowed x265 Quality-Baseline Calibration Runner (Op 943A)
Measures:
A. UHD Reference / Remux -> Hallowed 2160p x265 (Hallowed baseline fidelity)
B. Hallowed 2160p x265 -> AV1 candidate (Incremental AV1 loss relative to baseline)
C. UHD Reference / Remux -> AV1 candidate (Total end-to-end loss)
Outputs evidence/hallowed_baseline_calibration_raw.json.
"""

import os
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

def measure_pair(ref_path, dist_path, start, dur_sec, scale_w, scale_h, ref_crop_str, dist_crop_str, tmp_dir, label):
    log_json = os.path.join(tmp_dir, f"vmaf_{os.getpid()}_{label}.json")
    if os.path.exists(log_json):
        os.remove(log_json)

    filter_chain = (
        f"[0:v]{ref_crop_str}scale={scale_w}:{scale_h}:flags=bicubic,format=yuv420p10le[ref];"
        f"[1:v]{dist_crop_str}scale={scale_w}:{scale_h}:flags=bicubic,format=yuv420p10le[dist];"
        f"[dist][ref]libvmaf=model=path={MODEL_4K}:feature=name=psnr|name=float_ssim:log_fmt=json:log_path={log_json}"
    )

    cmd = [
        FFMPEG_BIN,
        "-ss", start, "-t", str(dur_sec), "-i", ref_path,
        "-ss", start, "-t", str(dur_sec), "-i", dist_path,
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
    manifest_path = os.path.join(REPO_ROOT, "evidence", "hallowed_baseline_calibration_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("================================================================================")
    print("OP 943A: HALLOWED X265 QUALITY-BASELINE CALIBRATION")
    print("================================================================================")

    tmp_dir = os.path.join(MEDIA_ROOT, "scratch", "calibration_op943a")
    os.makedirs(tmp_dir, exist_ok=True)

    results = []

    for title_entry in manifest["planned_titles"]:
        title = title_entry["title"]
        yr = title_entry["year"]

        print(f"\n>>> Calibrating Title: {title} ({yr})")

        if title == "Jurassic World":
            ref_path = os.path.join(ALTMOUNT_M4K, "Jurassic.World.2015.MULTi.iNTERNAL.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR10.REMUX-seedpool", "Jurassic.World.2015.MULTi.iNTERNAL.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR10.REMUX-seedpool.mkv")
            hal_path = os.path.join(ALTMOUNT_M4K, "Jurassic.World.2015.PROPER.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed", "Jurassic.World.2015.PROPER.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv")
            av1_path = None
            scale_w, scale_h = 3840, 1920
            ref_crop = "crop=3840:1920:0:120,"
            hal_crop = ""
            av1_crop = ""
        elif title == "The Bourne Supremacy":
            ref_path = os.path.join(ALTMOUNT_M4K, "The.Bourne.Supremacy.2004.2160p.BluRay.DTS-X.7.1.DV.HDR10.x265-MainFrame", "The.Bourne.Supremacy.2004.2160p.BluRay.DTS-X.7.1.DV.HDR10.x265-MainFrame.mkv")
            hal_path = os.path.join(ALTMOUNT_M4K, "The Bourne Supremacy 2004 UHD BluRay 2160p DDP 7 1 DV HDR x265-hallowed", "The Bourne Supremacy 2004 UHD BluRay 2160p DDP 7 1 DV HDR x265-hallowed.mkv")
            av1_path = os.path.join(ALTMOUNT_M4K, "The.Bourne.Supremacy.2004-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H", "The.Bourne.Supremacy.2004-2160p.BluRay.HDR10.10.bit.Encode.AV1.DTS.5.1-R and H.mkv")
            scale_w, scale_h = 3840, 1632
            ref_crop = ""
            hal_crop = ""
            av1_crop = ""
        elif title == "Jurassic Park III":
            ref_path = os.path.join(ALTMOUNT_M4K, "Jurassic.Park.III.2001.MULTi.iNTERNAL.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR10.REMUX-seedpool", "Jurassic.Park.III.2001.MULTi.iNTERNAL.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR10.REMUX-seedpool.mkv")
            hal_path = os.path.join(ALTMOUNT_M4K, "Jurassic.Park.III.2001.PROPER.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed", "Jurassic.Park.III.2001.PROPER.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv")
            av1_path = None
            scale_w, scale_h = 3840, 2076
            ref_crop = "crop=3840:2076:0:42,"
            hal_crop = ""
            av1_crop = ""
        elif title == "The Drama":
            ref_path = os.path.join(ALTMOUNT_M4K, "The.Drama.2026.iNTERNAL.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR10.REMUX-seedpool", "The.Drama.2026.iNTERNAL.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR10.REMUX-seedpool.mkv")
            hal_path = os.path.join(ALTMOUNT_M4K, "The.Drama.2026.UHD.BluRay.2160p.DDP.Atmos.5.1.DV.HDR.x265-hallowed", "The.Drama.2026.UHD.BluRay.2160p.DDP.Atmos.5.1.DV.HDR.x265-hallowed.mkv")
            av1_path = None
            scale_w, scale_h = 3840, 2076
            ref_crop = "crop=3840:2076:0:42,"
            hal_crop = ""
            av1_crop = ""

        ref_info = get_stream_info(ref_path)
        hal_info = get_stream_info(hal_path)
        av1_info = get_stream_info(av1_path)

        ref_mbps = round(ref_info["bitrate_bps"] / 1e6, 2) if ref_info else 0.0
        hal_mbps = round(hal_info["bitrate_bps"] / 1e6, 2) if hal_info else 0.0
        av1_mbps = round(av1_info["bitrate_bps"] / 1e6, 2) if av1_info else None

        pixels_per_sec = scale_w * scale_h * hal_info["fps"]
        hal_bpp = round(hal_info["bitrate_bps"] / pixels_per_sec, 4) if pixels_per_sec > 0 else 0.0
        av1_bpp = round(av1_info["bitrate_bps"] / pixels_per_sec, 4) if av1_info and pixels_per_sec > 0 else None

        print(f"  Reference Master: {ref_mbps} Mbps | Size: {round(ref_info['size_bytes']/1e9, 2)} GB")
        print(f"  Hallowed Baseline: {hal_mbps} Mbps | Size: {round(hal_info['size_bytes']/1e9, 2)} GB | BPP: {hal_bpp}")
        if av1_info:
            print(f"  AV1 Candidate: {av1_mbps} Mbps | Size: {round(av1_info['size_bytes']/1e9, 2)} GB | BPP: {av1_bpp}")

        scene_measurements = []
        for sc in title_entry["scenes"]:
            opt_tag = " (Optional 4th Scene)" if sc.get("is_optional") else ""
            print(f"  Measuring Scene {sc['scene_number']}: {sc['name']}{opt_tag} [{sc['start_timestamp']} (10s)]...")

            # Direction A: Ref -> Hallowed
            res_ref_hal = measure_pair(ref_path, hal_path, sc["start_timestamp"], sc["duration_sec"], scale_w, scale_h, ref_crop, hal_crop, tmp_dir, f"{title.replace(' ','_')}_s{sc['scene_number']}_ref_hal")
            print(f"    [Ref -> Hallowed]  VMAF: {res_ref_hal['vmaf']} | PSNR-Y: {res_ref_hal['psnr_y_db']} dB | SSIM: {res_ref_hal['ssim']}")

            # Direction B: Hallowed -> AV1 (if available)
            res_hal_av1 = None
            res_ref_av1 = None
            if av1_path:
                res_hal_av1 = measure_pair(hal_path, av1_path, sc["start_timestamp"], sc["duration_sec"], scale_w, scale_h, hal_crop, av1_crop, tmp_dir, f"{title.replace(' ','_')}_s{sc['scene_number']}_hal_av1")
                print(f"    [Hallowed -> AV1]  VMAF: {res_hal_av1['vmaf']} | PSNR-Y: {res_hal_av1['psnr_y_db']} dB | SSIM: {res_hal_av1['ssim']}")

                res_ref_av1 = measure_pair(ref_path, av1_path, sc["start_timestamp"], sc["duration_sec"], scale_w, scale_h, ref_crop, av1_crop, tmp_dir, f"{title.replace(' ','_')}_s{sc['scene_number']}_ref_av1")
                print(f"    [Ref -> AV1]       VMAF: {res_ref_av1['vmaf']} | PSNR-Y: {res_ref_av1['psnr_y_db']} dB | SSIM: {res_ref_av1['ssim']}")

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
                    "reference_to_hallowed": res_ref_hal,
                    "hallowed_to_av1": res_hal_av1,
                    "reference_to_av1": res_ref_av1
                }
            }
            scene_measurements.append(sc_record)

        core_scenes = [s for s in scene_measurements if not s.get("is_optional")]

        # Aggregate Ref -> Hallowed
        ref_hal_core_vmafs = [s["comparisons"]["reference_to_hallowed"]["vmaf"] for s in core_scenes]
        ref_hal_all_vmafs = [s["comparisons"]["reference_to_hallowed"]["vmaf"] for s in scene_measurements]
        ref_hal_mean = round(sum(ref_hal_core_vmafs) / len(ref_hal_core_vmafs), 2)
        ref_hal_med = round(statistics.median(ref_hal_core_vmafs), 2)
        ref_hal_min = min(ref_hal_all_vmafs)
        ref_hal_psnr_mean = round(sum(s["comparisons"]["reference_to_hallowed"]["psnr_y_db"] for s in core_scenes) / len(core_scenes), 2)
        ref_hal_ssim_mean = round(sum(s["comparisons"]["reference_to_hallowed"]["ssim"] for s in core_scenes) / len(core_scenes), 4)

        aggregates = {
            "reference_to_hallowed": {
                "mean_vmaf_core": ref_hal_mean,
                "median_vmaf_core": ref_hal_med,
                "min_vmaf_all": ref_hal_min,
                "mean_psnr_y_db_core": ref_hal_psnr_mean,
                "mean_ssim_core": ref_hal_ssim_mean
            }
        }

        if av1_path:
            hal_av1_core_vmafs = [s["comparisons"]["hallowed_to_av1"]["vmaf"] for s in core_scenes]
            hal_av1_all_vmafs = [s["comparisons"]["hallowed_to_av1"]["vmaf"] for s in scene_measurements]
            aggregates["hallowed_to_av1"] = {
                "mean_vmaf_core": round(sum(hal_av1_core_vmafs) / len(hal_av1_core_vmafs), 2),
                "median_vmaf_core": round(statistics.median(hal_av1_core_vmafs), 2),
                "min_vmaf_all": min(hal_av1_all_vmafs),
                "mean_psnr_y_db_core": round(sum(s["comparisons"]["hallowed_to_av1"]["psnr_y_db"] for s in core_scenes) / len(core_scenes), 2),
                "mean_ssim_core": round(sum(s["comparisons"]["hallowed_to_av1"]["ssim"] for s in core_scenes) / len(core_scenes), 4)
            }
            ref_av1_core_vmafs = [s["comparisons"]["reference_to_av1"]["vmaf"] for s in core_scenes]
            ref_av1_all_vmafs = [s["comparisons"]["reference_to_av1"]["vmaf"] for s in scene_measurements]
            aggregates["reference_to_av1"] = {
                "mean_vmaf_core": round(sum(ref_av1_core_vmafs) / len(ref_av1_core_vmafs), 2),
                "median_vmaf_core": round(statistics.median(ref_av1_core_vmafs), 2),
                "min_vmaf_all": min(ref_av1_all_vmafs),
                "mean_psnr_y_db_core": round(sum(s["comparisons"]["reference_to_av1"]["psnr_y_db"] for s in core_scenes) / len(core_scenes), 2),
                "mean_ssim_core": round(sum(s["comparisons"]["reference_to_av1"]["ssim"] for s in core_scenes) / len(core_scenes), 4)
            }

        title_summary = {
            "title": title,
            "year": yr,
            "edition": title_entry["edition"],
            "reference_identity": title_entry["reference_identity"],
            "hallowed_identity": title_entry["hallowed_identity"],
            "av1_identity": title_entry.get("av1_identity"),
            "ref_bitrate_mbps": ref_mbps,
            "hallowed_bitrate_mbps": hal_mbps,
            "av1_bitrate_mbps": av1_mbps,
            "hallowed_bpp": hal_bpp,
            "av1_bpp": av1_bpp,
            "resolution": f"{scale_w}x{scale_h}",
            "scenes": scene_measurements,
            "aggregates": aggregates
        }
        results.append(title_summary)

    out_json = os.path.join(REPO_ROOT, "evidence", "hallowed_baseline_calibration_raw.json")
    output_data = {
        "campaign": manifest["campaign"],
        "date": manifest["date"],
        "purpose": manifest["purpose"],
        "acceptance_premise": manifest["acceptance_premise"],
        "guardrails": manifest["guardrails"],
        "titles": results
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[OK] Saved Hallowed baseline raw metrics to {out_json}")

if __name__ == "__main__":
    main()
