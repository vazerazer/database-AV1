#!/usr/bin/env python3
"""
scripts/run_av1_calibration_expansion.py
AV1 Fidelity Calibration Expansion Runner (Op 939)
Measures empirical perceptual quality (VMAF, PSNR, SSIM, bpp, and fidelity-per-bit)
across 4 new UHD BluRay AV1 vs Reference Master pairs (Rob74K and ChopperHitler).
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

EXPANSION_ANCHORS = [
    {
        "title": "John Wick (2014)",
        "year": 2014,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "Rob74K",
        "av1_tier": "Quality Tier 1 Candidate",
        "av1_rel_path": "John.Wick.2014.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-Rob74K/John.Wick.2014.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HDR.AV1-Rob74K.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR/DV",
        "ref_rel_path": "John.Wick.2014.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed/John.Wick.2014.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Red Circle VIP lounge near-black shadows", "start": "00:48:30", "duration": 10},
            {"name": "High-Motion", "desc": "Red Circle dance floor gunfight & strobes", "start": "00:52:10", "duration": 10},
            {"name": "Film Grain / Texture", "desc": "Home night robbery textured 35mm grain", "start": "00:18:20", "duration": 10},
            {"name": "Near-Black Gradient", "desc": "Continental weapon room deep shadows", "start": "00:36:00", "duration": 10, "is_optional": True}
        ]
    },
    {
        "title": "X-Men (2000)",
        "year": 2000,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "ChopperHitler",
        "av1_tier": "Compact / Storage Candidate",
        "av1_rel_path": "X-Men.2000.2160p.BluRay.AV1.10bit.5.1ch.AC3.AV1-ChopperHitler/X-Men.2000.2160p.BluRay.AV1.10bit.5.1ch.AC3.AV1-ChopperHitler.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR",
        "ref_rel_path": "X-Men.2000.UHD.BluRay.2160p.DDP.5.1.HDR.x265-hallowed/X-Men.2000.UHD.BluRay.2160p.DDP.5.1.HDR.x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Poland 1944 rainstorm night gate opening", "start": "00:01:20", "duration": 10},
            {"name": "High-Motion", "desc": "Statue of Liberty torch battle & machinery", "start": "01:19:10", "duration": 10},
            {"name": "Film Grain / Texture", "desc": "Northern Alberta tavern heavy 35mm grain", "start": "00:15:30", "duration": 10}
        ]
    },
    {
        "title": "X-Men: Days of Future Past (2014)",
        "year": 2014,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "ChopperHitler",
        "av1_tier": "Compact / Storage Candidate",
        "av1_rel_path": "X-Men.Days.of.Future.Past.2014.2160p.BluRay.AV1.10bit.HDR10.AC3.5.0ch.AV1-ChopperHitler/X-Men.Days.of.Future.Past.2014.2160p.BluRay.AV1.10bit.HDR10.AC3.5.0ch.AV1-ChopperHitler.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR",
        "ref_rel_path": "X-Men.Days.of.Future.Past.2014.UHD.BluRay.2160p.DDP.7.1.HDR.x265-hallowed/X-Men.Days.of.Future.Past.2014.UHD.BluRay.2160p.DDP.7.1.HDR.x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Moscow underground bunker near-black shadows", "start": "00:03:40", "duration": 10},
            {"name": "High-Motion", "desc": "Future Sentinel ambush & portal action", "start": "00:06:30", "duration": 10},
            {"name": "Film Grain / Texture", "desc": "Paris peace summit 1973 period grain", "start": "00:48:20", "duration": 10},
            {"name": "Near-Black Gradient", "desc": "Temple final stand near-black storm", "start": "01:48:10", "duration": 10, "is_optional": True}
        ]
    },
    {
        "title": "John Wick: Chapter 2 (2017)",
        "year": 2017,
        "edition": "Theatrical UHD BluRay",
        "av1_group": "Rob74K",
        "av1_tier": "Quality Tier 1 Candidate",
        "av1_rel_path": "John.Wick.Chapter.2.2017.UHD.BluRay.2160p.TrueHD.Atmos.7.1.AV1-Rob74K/John.Wick.Chapter.2.2017.UHD.BluRay.2160p.TrueHD.Atmos.7.1.AV1-Rob74K.mkv",
        "ref_group": "hallowed",
        "ref_format": "2160p x265 HDR/DV",
        "ref_rel_path": "John.Wick.Chapter.2.2017.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed/John.Wick.Chapter.2.2017.UHD.BluRay.2160p.DDP.7.1.DV.HDR.x265-hallowed.mkv",
        "scenes": [
            {"name": "Dark / Low-Light", "desc": "Rome catacombs concert underground shadows", "start": "00:42:10", "duration": 10},
            {"name": "High-Motion", "desc": "Catacombs tactical gunfight & reload chase", "start": "00:49:30", "duration": 10},
            {"name": "Film Grain / Texture", "desc": "Museum hall of mirrors fine geometry", "start": "01:38:00", "duration": 10},
            {"name": "Near-Black Gradient", "desc": "NYC subway platform deep shadow gradients", "start": "01:05:20", "duration": 10, "is_optional": True}
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
    print("OP 939: AV1 FIDELITY CALIBRATION EXPANSION (MEASUREMENT SUITE)")
    print("================================================================================")

    tmp_dir = os.path.join(MEDIA_ROOT, "scratch", "calibration_op939")
    os.makedirs(tmp_dir, exist_ok=True)

    results = []

    for anchor in EXPANSION_ANCHORS:
        title = anchor["title"]
        print(f"\n>>> Analyzing Expansion Anchor: {title} ({anchor['av1_group']} vs {anchor['ref_group']})")

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
            opt_tag = " (Optional)" if sc.get("is_optional") else ""
            print(f"  Measuring Scene: {sc['name']}{opt_tag} [{sc['start']} (10s)]...")
            metrics = measure_scene(av1_full, ref_full, sc, tmp_dir)

            vmaf_per_mbps = round(metrics["vmaf"] / av1_mbps, 2) if av1_mbps > 0 else 0.0

            sc_result = {
                "scene_name": sc["name"],
                "description": sc["desc"],
                "timestamp": sc["start"],
                "duration_sec": sc["duration"],
                "is_optional": sc.get("is_optional", False),
                "vmaf": metrics["vmaf"],
                "psnr_db": metrics["psnr_db"],
                "ssim": metrics["ssim"],
                "vmaf_per_mbps": vmaf_per_mbps,
                "offset_ms": metrics["aligned_offset_ms"]
            }
            print(f"    -> VMAF: {metrics['vmaf']} | PSNR: {metrics['psnr_db']} dB | SSIM: {metrics['ssim']} | Offset: {metrics['aligned_offset_ms']:+d}ms")
            anchor_data["scenes"].append(sc_result)

        standard_scenes = [s for s in anchor_data["scenes"] if not s.get("is_optional")]
        all_scenes = anchor_data["scenes"]

        avg_vmaf = round(sum(s["vmaf"] for s in standard_scenes) / len(standard_scenes), 2)
        avg_psnr = round(sum(s["psnr_db"] for s in standard_scenes) / len(standard_scenes), 2)
        avg_ssim = round(sum(s["ssim"] for s in standard_scenes) / len(standard_scenes), 4)
        avg_vmaf_per_mbps = round(avg_vmaf / av1_mbps, 2) if av1_mbps > 0 else 0.0

        anchor_data["aggregate"] = {
            "mean_vmaf_standard": avg_vmaf,
            "mean_psnr_db_standard": avg_psnr,
            "mean_ssim_standard": avg_ssim,
            "mean_vmaf_per_mbps_standard": avg_vmaf_per_mbps,
            "min_scene_vmaf": min(s["vmaf"] for s in all_scenes)
        }
        results.append(anchor_data)

    out_json = os.path.join(REPO_ROOT, "evidence", "av1_calibration_expansion_raw.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Saved raw calibration expansion data to {out_json}")

if __name__ == "__main__":
    main()
