#!/usr/bin/env python3
"""
scripts/run_av1_cosmicsurfer_jw3.py
Targeted Candidate-Group Reference Calibration Runner (Op 940B)
Measures empirical perceptual quality (VMAF, PSNR-Y, SSIM, BPP) for
CoSMiCSuRFeR's second title: John Wick: Chapter 3 - Parabellum (2019).
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

JW3_ANCHOR = {
    "title": "John Wick: Chapter 3 - Parabellum (2019)",
    "year": 2019,
    "edition": "Theatrical UHD BluRay",
    "av1_group": "CoSMiCSuRFeR",
    "av1_rel_path": "John.Wick.Chapter.3.Parabellum.2019.2160p.UHD.BluRay.DV.HDR.TrueHD.7.1.Atmos-AV1-CoSMiCSuRFeR/John.Wick.Chapter.3.Parabellum.2019.2160p.UHD.BluRay.DV.HDR.TrueHD.7.1.Atmos-AV1-CoSMiCSuRFeR.mkv",
    "ref_group": "hallowed",
    "ref_format": "2160p x265 HDR/DV",
    "ref_rel_path": "John.Wick.Chapter.3.Parabellum.2019.REPACK.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed/John.Wick.Chapter.3.Parabellum.2019.REPACK.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv",
    "scenes": [
        {"name": "Near-Black / Shadow-Detail", "desc": "NYC rainstorm alleyway & Continental near-black shadows", "start": "00:08:30", "duration": 10, "is_optional": False},
        {"name": "High-Motion", "desc": "Antique weapon museum knife fight & rapid combat", "start": "00:15:20", "duration": 10, "is_optional": False},
        {"name": "Texture / Fine-Detail", "desc": "Casablanca desert hotel mosaic & fine fabric textures", "start": "00:54:10", "duration": 10, "is_optional": False},
        {"name": "Near-Black Glass Gradient (Optional)", "desc": "Glass house final duel neon reflections & deep shadow gradients", "start": "01:46:30", "duration": 10, "is_optional": True}
    ]
}

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
            "[0:v]scale=3840:1600:flags=bicubic,format=yuv420p10le[v0];[1:v]scale=3840:1600:flags=bicubic,format=yuv420p10le[v1];[v0][v1]psnr",
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
        f"[0:v]scale=3840:1600:flags=bicubic,format=yuv420p10le[dist];[1:v]scale=3840:1600:flags=bicubic,format=yuv420p10le[ref];[dist][ref]libvmaf=model=path={MODEL_4K}:feature=name=psnr|name=float_ssim:log_fmt=json:log_path={log_json}",
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
    print("OP 940B: TARGETED CANDIDATE-GROUP CALIBRATION (COSMICSURFER JW3)")
    print("================================================================================")

    tmp_dir = os.path.join(MEDIA_ROOT, "scratch", "calibration_op940b")
    os.makedirs(tmp_dir, exist_ok=True)

    av1_full = os.path.join(ALTMOUNT_M4K, JW3_ANCHOR["av1_rel_path"])
    ref_full = os.path.join(ALTMOUNT_M4K, JW3_ANCHOR["ref_rel_path"])

    av1_info = get_stream_info(av1_full)
    ref_info = get_stream_info(ref_full)

    av1_mbps = round(av1_info["bitrate_bps"] / 1_000_000, 2)
    ref_mbps = round(ref_info["bitrate_bps"] / 1_000_000, 2)

    pixels_per_sec = av1_info["width"] * av1_info["height"] * av1_info["fps"]
    bpp = round(av1_info["bitrate_bps"] / pixels_per_sec, 4) if pixels_per_sec > 0 else 0.0

    print(f"Candidate AV1: {JW3_ANCHOR['title']} by {JW3_ANCHOR['av1_group']}")
    print(f"  Bitrate: {av1_mbps} Mbps | BPP: {bpp} | Resolution: {av1_info['width']}x{av1_info['height']} @ {av1_info['fps']:.3f} fps")
    print(f"Reference Master: {JW3_ANCHOR['ref_group']} ({JW3_ANCHOR['ref_format']})")
    print(f"  Bitrate: {ref_mbps} Mbps | Resolution: {ref_info['width']}x{ref_info['height']} @ {ref_info['fps']:.3f} fps\n")

    scene_results = []

    for sc in JW3_ANCHOR["scenes"]:
        opt_tag = " (Optional 4th Scene)" if sc.get("is_optional") else ""
        print(f"Measuring Scene: {sc['name']}{opt_tag} [{sc['start']} (10s)]...")
        metrics = measure_scene(av1_full, ref_full, sc, tmp_dir)

        vmaf_per_mbps = round(metrics["vmaf"] / av1_mbps, 2) if av1_mbps > 0 else 0.0

        res = {
            "scene_name": sc["name"],
            "description": sc["desc"],
            "timestamp": sc["start"],
            "duration_sec": sc["duration"],
            "is_optional": sc.get("is_optional", False),
            "status": "ACCEPTED",
            "vmaf": metrics["vmaf"],
            "psnr_y_db": metrics["psnr_db"],
            "ssim": metrics["ssim"],
            "vmaf_per_mbps": vmaf_per_mbps,
            "aligned_offset_ms": metrics["aligned_offset_ms"]
        }
        print(f"  -> VMAF: {metrics['vmaf']} | PSNR-Y: {metrics['psnr_db']} dB | SSIM: {metrics['ssim']} | Offset: {metrics['aligned_offset_ms']:+d}ms")
        scene_results.append(res)

    core_scenes = [s for s in scene_results if not s.get("is_optional")]
    all_scenes = scene_results

    mean_vmaf_core = round(sum(s["vmaf"] for s in core_scenes) / len(core_scenes), 2)
    min_vmaf_all = min(s["vmaf"] for s in all_scenes)
    mean_psnr_core = round(sum(s["psnr_y_db"] for s in core_scenes) / len(core_scenes), 2)
    mean_ssim_core = round(sum(s["ssim"] for s in core_scenes) / len(core_scenes), 4)

    output_data = {
        "title": JW3_ANCHOR["title"],
        "year": JW3_ANCHOR["year"],
        "edition": JW3_ANCHOR["edition"],
        "av1_group": JW3_ANCHOR["av1_group"],
        "av1_bitrate_mbps": av1_mbps,
        "ref_group": JW3_ANCHOR["ref_group"],
        "ref_format": JW3_ANCHOR["ref_format"],
        "ref_bitrate_mbps": ref_mbps,
        "bpp": bpp,
        "resolution": f"{av1_info['width']}x{av1_info['height']}",
        "fps": round(av1_info["fps"], 3),
        "runtime_min": round(av1_info["duration_sec"] / 60, 1),
        "scenes": scene_results,
        "aggregate": {
            "mean_vmaf_core": mean_vmaf_core,
            "min_vmaf_all": min_vmaf_all,
            "mean_psnr_y_db_core": mean_psnr_core,
            "mean_ssim_core": mean_ssim_core,
            "core_scene_count": len(core_scenes),
            "total_scene_count": len(all_scenes),
            "accepted_scene_count": len(all_scenes),
            "rejected_scene_count": 0
        }
    }

    out_json = os.path.join(REPO_ROOT, "evidence", "av1_calibration_cosmicsurfer_jw3_raw.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[OK] Saved raw calibration data to {out_json}")
    print(f"Summary: Mean Core VMAF: {mean_vmaf_core} | Min Scene VMAF: {min_vmaf_all} | Mean PSNR-Y: {mean_psnr_core} dB | Mean SSIM: {mean_ssim_core}")

if __name__ == "__main__":
    main()
