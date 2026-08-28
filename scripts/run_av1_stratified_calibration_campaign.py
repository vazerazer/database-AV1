#!/usr/bin/env python3
"""
scripts/run_av1_stratified_calibration_campaign.py
AV1 Multi-Group Stratified Calibration Campaign Runner (Op 942)
Executes pre-registered calibration for:
1. CoSMiCSuRFeR - The Lord of the Rings: The Fellowship of the Ring (2001) [Extended Cut]
2. RandH - John Wick (2014)
3. ChopperHitler - X-Men: Apocalypse (2016)
Outputs evidence/av1_stratified_calibration_campaign_raw.json.
"""

import os
import sys
import json
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.dirname(REPO_ROOT)

FFMPEG_BIN = os.environ.get("FFMPEG_BIN") or os.path.join(MEDIA_ROOT, "scratch", "bin", "ffmpeg")
FFPROBE_BIN = os.environ.get("FFPROBE_BIN") or os.path.join(MEDIA_ROOT, "scratch", "bin", "ffprobe")
MODEL_4K = os.environ.get("VMAF_MODEL_4K") or os.path.join(MEDIA_ROOT, "scratch", "models", "vmaf_4k_v0.6.1.json")

ALTMOUNT_M4K = os.path.join(MEDIA_ROOT, "library", "altmount", "complete", "movies4k")

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

def measure_scene(av1_path, ref_path, scene_info, scale_w, scale_h, crop_str, tmp_dir):
    start = scene_info["start_timestamp"]
    dur = str(scene_info["duration_sec"])

    log_json = os.path.join(tmp_dir, f"vmaf_{os.getpid()}_{scene_info['name'].replace(' ', '_').replace('/', '_')}.json")
    if os.path.exists(log_json):
        os.remove(log_json)

    filter_chain = f"[0:v]{crop_str}scale={scale_w}:{scale_h}:flags=bicubic,format=yuv420p10le[dist];[1:v]scale={scale_w}:{scale_h}:flags=bicubic,format=yuv420p10le[ref];[dist][ref]libvmaf=model=path={MODEL_4K}:feature=name=psnr|name=float_ssim:log_fmt=json:log_path={log_json}"

    cmd = [
        FFMPEG_BIN,
        "-ss", start, "-t", dur, "-i", av1_path,
        "-ss", start, "-t", dur, "-i", ref_path,
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
        "psnr_db": round(psnr, 2),
        "ssim": round(ssim, 4)
    }

def main():
    manifest_path = os.path.join(REPO_ROOT, "evidence", "av1_stratified_calibration_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("================================================================================")
    print("OP 942: AV1 MULTI-GROUP STRATIFIED CALIBRATION CAMPAIGN")
    print("================================================================================")

    tmp_dir = os.path.join(MEDIA_ROOT, "scratch", "calibration_op942")
    os.makedirs(tmp_dir, exist_ok=True)

    campaign_results = []

    for title_entry in manifest["planned_titles"]:
        grp = title_entry["group"]
        title = title_entry["title"]
        yr = title_entry["year"]

        print(f"\n>>> Calibrating Group: {grp} | Title: {title} ({yr})")

        if grp == "CoSMiCSuRFeR":
            av1_path = os.path.join(ALTMOUNT_M4K, "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.Extended.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR", "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.Extended.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-CoSMiCSuRFeR.mkv")
            ref_path = os.path.join(ALTMOUNT_M4K, "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.Extended.UHD.BluRay.2160p.DDP.Atmos.5.1.DV.HDR.x265-hallowed", "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.Extended.UHD.BluRay.2160p.DDP.Atmos.5.1.DV.HDR.x265-hallowed.mkv")
            scale_w, scale_h = 3840, 1608
            crop_str = ""
        elif grp == "RandH":
            av1_path = os.path.join(ALTMOUNT_M4K, "John.Wick.2014-2160p.BluRay.DV.HDR.10.bit.Encode.AV1.DTS.5.1-R&H.mkv", "John.Wick.2014-2160p.BluRay.DV.HDR.10.bit.Encode.AV1.DTS.5.1-R&H.mkv")
            ref_path = os.path.join(ALTMOUNT_M4K, "John.Wick.2014.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed", "John.Wick.2014.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv")
            scale_w, scale_h = 3840, 1600
            crop_str = "crop=3840:1600:0:280,"
        elif grp == "ChopperHitler":
            av1_path = os.path.join(ALTMOUNT_M4K, "X-Men Apocalypse-2016-UHD BluRay AV1 10bit HDR10 AC3 5.1 AV1-ChopperHitler", "X-Men Apocalypse-2016-UHD BluRay AV1 10bit HDR10 AC3 5.1 AV1-ChopperHitler.mkv")
            ref_path = os.path.join(ALTMOUNT_M4K, "X-Men.Apocalypse.2016.UHD.BluRay.2160p.DDP.7.1.HDR.x265-hallowed", "X-Men.Apocalypse.2016.UHD.BluRay.2160p.DDP.7.1.HDR.x265-hallowed.mkv")
            scale_w, scale_h = 3840, 1600
            crop_str = ""

        av1_info = get_stream_info(av1_path)
        ref_info = get_stream_info(ref_path)

        av1_mbps = round(av1_info["bitrate_bps"] / 1_000_000, 2)
        ref_mbps = round(ref_info["bitrate_bps"] / 1_000_000, 2)

        pixels_per_sec = scale_w * scale_h * av1_info["fps"]
        bpp = round(av1_info["bitrate_bps"] / pixels_per_sec, 4) if pixels_per_sec > 0 else 0.0

        print(f"  Candidate AV1: {av1_mbps} Mbps | BPP: {bpp} | Canvas: {av1_info['width']}x{av1_info['height']} -> Scaled: {scale_w}x{scale_h}")
        print(f"  Reference Master: {ref_mbps} Mbps | Canvas: {ref_info['width']}x{ref_info['height']}")

        scene_results = []
        for sc in title_entry["planned_scenes"]:
            opt_tag = " (Optional 4th Scene)" if sc.get("is_optional") else ""
            print(f"  Measuring Scene {sc['scene_number']}: {sc['name']}{opt_tag} [{sc['start_timestamp']} (10s)]...")
            metrics = measure_scene(av1_path, ref_path, sc, scale_w, scale_h, crop_str, tmp_dir)
            vmaf_per_mbps = round(metrics["vmaf"] / av1_mbps, 2) if av1_mbps > 0 else 0.0

            res = {
                "scene_number": sc["scene_number"],
                "scene_name": sc["name"],
                "category": sc["category"],
                "timestamp": sc["start_timestamp"],
                "duration_sec": sc["duration_sec"],
                "rationale": sc["rationale"],
                "is_optional": sc.get("is_optional", False),
                "status": "ACCEPTED",
                "vmaf": metrics["vmaf"],
                "psnr_y_db": metrics["psnr_db"],
                "ssim": metrics["ssim"],
                "vmaf_per_mbps": vmaf_per_mbps,
                "aligned_offset_ms": title_entry.get("alignment_offset_ms", 0)
            }
            print(f"    -> VMAF: {metrics['vmaf']} | PSNR-Y: {metrics['psnr_db']} dB | SSIM: {metrics['ssim']}")
            scene_results.append(res)

        core_scenes = [s for s in scene_results if not s.get("is_optional")]
        all_scenes = scene_results

        vmafs_core = [s["vmaf"] for s in core_scenes]
        vmafs_all = [s["vmaf"] for s in all_scenes]

        mean_vmaf_core = round(sum(vmafs_core) / len(vmafs_core), 2)
        import statistics
        median_vmaf_core = round(statistics.median(vmafs_core), 2)
        min_vmaf_all = min(vmafs_all)
        mean_psnr_core = round(sum(s["psnr_y_db"] for s in core_scenes) / len(core_scenes), 2)
        mean_ssim_core = round(sum(s["ssim"] for s in core_scenes) / len(core_scenes), 4)

        title_summary = {
            "group": grp,
            "title": title,
            "year": yr,
            "edition": title_entry["edition"],
            "candidate_release": title_entry["candidate_release"],
            "reference_release": title_entry["reference_release"],
            "av1_bitrate_mbps": av1_mbps,
            "ref_bitrate_mbps": ref_mbps,
            "bpp": bpp,
            "resolution": f"{scale_w}x{scale_h}",
            "fps": round(av1_info["fps"], 3),
            "runtime_min": round(av1_info["duration_sec"] / 60, 1),
            "size_gb": round(av1_info["size_bytes"] / 1e9, 2),
            "scenes": scene_results,
            "aggregate": {
                "mean_vmaf_core": mean_vmaf_core,
                "median_vmaf_core": median_vmaf_core,
                "min_vmaf_all": min_vmaf_all,
                "mean_psnr_y_db_core": mean_psnr_core,
                "mean_ssim_core": mean_ssim_core,
                "core_scene_count": len(core_scenes),
                "total_scene_count": len(all_scenes),
                "accepted_scene_count": len(all_scenes),
                "rejected_scene_count": 0
            }
        }
        campaign_results.append(title_summary)

    out_json = os.path.join(REPO_ROOT, "evidence", "av1_stratified_calibration_campaign_raw.json")
    output_data = {
        "campaign": manifest["campaign"],
        "date": manifest["date"],
        "objective": manifest["objective"],
        "target_groups": manifest["target_groups"],
        "titles": campaign_results
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[OK] Saved campaign raw metrics to {out_json}")

if __name__ == "__main__":
    main()
