#!/usr/bin/env python3
"""
Refined AV1 Regex Test Battery with Site Tags and Strict Anchoring
Runs under re.IGNORECASE to replicate Radarr's RegexSpecificationBase.cs runtime.
"""

import re
import sys

# Refined, strictly anchored regexes:
REGEX_PATTERNS = {
    # 1. Anime Encoders: Strictly anchored to leading bracket prefix ^\[(Group)\]
    "AV1 Anime Encoders": r"^\[(?:Trix|Breeze|INDEX|AkihitoSubs|NanDesuKa|CTR)\]",
    
    # 2. Compact Encoders: Anchored to trailing group hyphen, optional site tag, and optional extension
    # Tolerate site tags like [TGx], [ettv], [rarbg], [rartv], [eztv], etc.
    "AV1 Compact Encoders": r"-(?:dAV1nci|WhiskeyJack|WhiskyJack|UH|edge2020|UnAV1Chain|R[-._ ]and[-._ ]H|\[dAV1nci\]|\[UnAV1Chain\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$",
    
    # 3. Storage Savers: Anchored to trailing group hyphen, optional site tag, and optional extension
    "AV1 Storage Savers": r"-(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART)(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$"
}

TEST_CASES = {
    "AV1 Anime Encoders": {
        "positive": [
            "[Trix] Frieren - Beyond Journey's End (01-28) [AV1 10bit 1080p Opus].mkv",
            "[Breeze] Jujutsu Kaisen - S02 [1080p AV1 10bit Opus].mkv",
            "[INDEX] Cyberpunk: Edgerunners [1080p AV1 10bit DDP].mkv",
            "[AkihitoSubs] Cyberpunk Edgerunners - 01 [1080p AV1 10bit].mkv",
            "[NanDesuKa] Dungeon Meshi - 01 [1080p AV1].mkv",
            "[CTR] Oshi no Ko - 01 [1080p AV1 10bit].mkv"
        ],
        "adversarial_negatives": [
            "The.Breeze.Of.Summer.2024.1080p.AV1-PSA.mkv",         # Contains 'Breeze' mid-title
            "Kaleido.Star.S01E01.1080p.AV1-d3g.mkv",               # Dropped / Non-AV1 group
            "Kawa.no.Nushi.Tsuri.1080p.AV1-PSA.mkv",              # Dropped / Non-AV1 group
            "[HorribleSubs] Bleach - 01 [720p].mkv",              # Non-AV1 legacy group
            "[Judas] Sousou no Frieren - 01 [1080p x265].mkv",    # x265 group
            "[Erai-raws] Dungeon Meshi - 01 [1080p HEVC].mkv",    # HEVC group
            "[VARYG] Kimi no Na wa [1080p H.264].mkv",            # Dropped H.264 group
            "[YTS] Ghost in the Shell 1995.mp4",                  # Banned group
            "Sousou.no.Frieren.S01E01.1080p.x265-DON"             # Legacy x265
        ]
    },
    "AV1 Compact Encoders": {
        "positive": [
            "The.Lord.of.the.Rings.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "The.Lord.of.the.Rings.2003.Extended.2160p.AV1-dAV1nci[rarbg].mkv",       # Site tag: rarbg
            "The.Lord.of.the.Rings.2003.Extended.1080p.AV1.DDP.Atmos-[UnAV1Chain].mkv",
            "LOTR.The.Return.Of.The.King.2003.PROPER.Bluray.2160p.AV1.HDR10.OPUS.7.1-UH",
            "The.Lord.of.the.Rings.2003.Extended.1080p.Bluray.OPUS.7.1.AV1-WhiskeyJack",
            "The.Lord.of.the.Rings.2003.Extended.1080p.Bluray.OPUS.7.1.AV1-WhiskyJack", # Alternate spelling
            "Inception.2010.1080p.BluRay.AV1.Opus.5.1-edge2020",
            "Gladiator.2000.2160p.AV1.HDR-R and H"
        ],
        "adversarial_negatives": [
            "The.UH.Oh.Files.2021.1080p.AV1-PSA.mkv",             # Contains 'UH' in title
            "Oppenheimer.2023.1080p.x265-Vyndros.mkv",            # Dropped x265 encoder
            "Ghost.in.the.Shell.1995.1080p.AV1-d3g.mkv",          # Storage saver group
            "Fallout.S01E01.1080p.AV1-MeGusta.mkv",               # Storage saver group
            "The.Lord.of.the.Rings.2003.Extended.2160p.x265-DON"  # Legacy x265 group
        ]
    },
    "AV1 Storage Savers": {
        "positive": [
            "Fallout.S01E01.1080p.AV1-MeGusta.mkv",
            "Gladiator.2000.1080p.10bit.AV1-PSA.mkv",
            "Gladiator.2000.1080p.10bit.AV1-PSA[ettv].mkv",       # Site tag: ettv
            "Dune.Part.Two.2024.1080p.AV1-GalaxyRG.mkv",
            "Dune.Part.Two.2024.1080p.AV1-GalaxyRG[TGx].mkv",     # Site tag: TGx
            "House.of.the.Dragon.S02E01.1080p.AV1-LAMA.mkv",
            "Shogun.2024.S01E01.1080p.AV1-ELiTE.mkv",
            "Baby.Reindeer.S01E01.1080p.AV1-KaKa.mkv",
            "Movie.2023.1080p.AV1-Ghost.mkv",
            "Movie.2023.1080p.AV1-BONE.mkv",
            "Movie.2023.1080p.AV1-CART.mkv"
        ],
        "adversarial_negatives": [
            "Ghost.in.the.Shell.1995.1080p.AV1-dAV1nci.mkv",      # Title contains 'Ghost'
            "[YTS] Ghost in the Shell 1995.mp4",                  # Title contains 'Ghost'
            "Bone.Tomahawk.2015.1080p.AV1-WhiskeyJack.mkv",       # Title contains 'Bone'
            "The.Cart.Bandit.2020.1080p.AV1-edge2020.mkv",        # Title contains 'Cart'
            "Ghostbusters.2016.2160p.AV1-dAV1nci.mkv",            # Title contains 'Ghostbusters'
            "The.Lord.of.the.Rings.2003.Extended.2160p.AV1-dAV1nci" # Compact group
        ]
    }
}

def run_suite():
    total_passed = 0
    total_failed = 0
    
    print("================================================================================")
    print("REFINED ANCHORED AV1 REGEX TEST BATTERY (WITH SITE TAGS & ADVERSARIAL CASES)")
    print("================================================================================")
    
    for pat_name, cases in TEST_CASES.items():
        pattern_str = REGEX_PATTERNS[pat_name]
        compiled = re.compile(pattern_str, re.IGNORECASE)
        
        print(f"\n--- Pattern: {pat_name} ---")
        print(f"Regex: {pattern_str}")
        
        print("\n  [Positive Tests]")
        for pos in cases["positive"]:
            m = compiled.search(pos)
            if m:
                print(f"    [PASS] (+) '{pos}' -> matched: '{m.group(0)}'")
                total_passed += 1
            else:
                print(f"    [FAIL] (+) '{pos}' -> UNEXPECTED REJECTION!")
                total_failed += 1
                
        print("\n  [Adversarial Negative Tests]")
        for neg in cases["adversarial_negatives"]:
            m = compiled.search(neg)
            if not m:
                print(f"    [PASS] (-) '{neg}' -> correctly rejected")
                total_passed += 1
            else:
                print(f"    [FAIL] (-) '{neg}' -> FALSE POSITIVE: '{m.group(0)}'!")
                total_failed += 1
                
    print("\n================================================================================")
    print(f"SUMMARY: {total_passed} Passed, {total_failed} Failed (Total: {total_passed + total_failed})")
    print("================================================================================")
    return total_failed == 0

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)
