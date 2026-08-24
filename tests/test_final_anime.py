#!/usr/bin/env python3
"""
Verify Final Anime Regex with Confirmed AV1 Encoders
Trix, Breeze, INDEX, Sav1or, AV1ARY, Sokudo, RigAV1
"""

import re
import sys

ANIME_REGEX = r"^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1)\]"

POS_CASES = [
    "[Trix] Frieren - Beyond Journey's End (01-28) [AV1 10bit 1080p Opus].mkv",
    "[Breeze] Jujutsu Kaisen - S02 [1080p AV1 10bit Opus].mkv",
    "[INDEX] Cyberpunk: Edgerunners [1080p AV1 10bit DDP].mkv",
    "[Sav1or] Oshi no Ko [1080p AV1 10bit Opus].mkv",
    "[AV1ARY] Dungeon Meshi [1080p AV1 10bit Dual-Audio].mkv",
    "[Sokudo] Bleach Sennen Kessen-hen [1080p AV1 10bit].mkv",
    "[RigAV1] Solo Leveling [1080p AV1 10bit Opus].mkv"
]

NEG_CASES = [
    "The.Breeze.Of.Summer.2024.1080p.AV1-PSA.mkv",
    "[AkihitoSubs] Gate [HEVC][x265][10Bit][Opus].mkv",
    "[NanDesuKa] Dungeon Meshi - 01 [1080p].mkv",
    "[CTR] Oshi no Ko - 01 [1080p].mkv",
    "[Judas] Sousou no Frieren - 01 [1080p x265].mkv",
    "[Erai-raws] Dungeon Meshi - 01 [1080p HEVC].mkv",
    "[HorribleSubs] Bleach - 01 [720p].mkv"
]

compiled = re.compile(ANIME_REGEX, re.IGNORECASE)
failed = 0

print("--- Testing Final Confirmed Anime Encoders Regex ---")
print(f"Pattern: {ANIME_REGEX}\n")

for p in POS_CASES:
    m = compiled.search(p)
    if m:
        print(f"  [PASS] (+) '{p}' -> matched '{m.group(0)}'")
    else:
        print(f"  [FAIL] (+) '{p}' -> NOT MATCHED!")
        failed += 1

for n in NEG_CASES:
    m = compiled.search(n)
    if not m:
        print(f"  [PASS] (-) '{n}' -> correctly rejected")
    else:
        print(f"  [FAIL] (-) '{n}' -> FALSE POSITIVE: '{m.group(0)}'!")
        failed += 1

print(f"\nTotal: {len(POS_CASES) + len(NEG_CASES)}, Failed: {failed}")
sys.exit(0 if failed == 0 else 1)
