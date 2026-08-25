#!/usr/bin/env python3
"""
Refined AV1 Regex Test Battery with Site Tags, New Groups, and Strict Anchoring
Runs under re.IGNORECASE to replicate Radarr's RegexSpecificationBase.cs runtime.
"""

import re
import sys

REGEX_PATTERNS = {
    # 1. Anime Encoders: Strictly anchored to leading bracket prefix ^\[(Group)\]
    "AV1 Anime Encoders": r"(?i)^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1|Ironclad|Valenciano)\]",
    
    # 2. Quality Encoders: Anchored to trailing group hyphen, optional site tag, and optional extension
    "AV1 Quality Encoders": r"(?i)(?:^\[(?:CoSMiCSuRFeR|Waldek|PRL|CHD|CHOPPERHITLER|TAoE)\]|-(?:CoSMiCSuRFeR|Waldek|PRL|CHD|CHOPPERHITLER|TAoE|\[CoSMiCSuRFeR\]|\[Waldek\]|\[PRL\]|\[CHD\]|\[CHOPPERHITLER\]|\[TAoE\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)",

    # 3. Compact Encoders: Anchored to trailing group hyphen, optional site tag, and optional extension
    "AV1 Compact Encoders": r"(?i)(?:^\[(?:dAV1nci|UnAV1Chain|RAV1NE|UserHEVC|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG)\]|-(?:dAV1nci|WhiskeyJack|WhiskyJack|UH|edge2020|UnAV1Chain|Smokindevil|SmokinDevil|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|\[dAV1nci\]|\[UnAV1Chain\]|\[RAV1NE\]|\[UserHEVC\]|\[LAZARUS\]|\[DKV\]|\[TiZU\]|\[Saon\]|\[onlyfaffs\]|\[KIMJI\]|\[heTOrico\]|\[Rosy\]|\[anomoomin\]|\[CMCT\]|\[GRiMM\]|\[Dust\]|\[DIN\]|\[GanG\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)",
    
    # 4. Storage Savers: Anchored to trailing group hyphen, optional site tag, and optional extension
    "AV1 Storage Savers": r"(?i)(?:^\[(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART|LUCY|DKong|Rapta|GubrakZ|Retr0|SWAXXON|FELIX12345)\]|-(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART|LUCY|DKong|Rapta|GubrakZ|Retr0|SWAXXON|FELIX12345|\[PSA\]|\[GalaxyRG\]|\[MeGusta\]|\[VXT\]|\[d3g\]|\[Ghost\]|\[rartv\]|\[ELiTE\]|\[LAMA\]|\[KaKa\]|\[YAWNTIC\]|\[BONE\]|\[GZ\]|\[CART\]|\[LUCY\]|\[DKong\]|\[Rapta\]|\[GubrakZ\]|\[Retr0\]|\[SWAXXON\]|\[FELIX12345\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)",

    # 5. Banned Groups
    "Banned ENTROPY": r"(?i)(?<![a-zA-Z0-9])ENTROPY\b"
}

TEST_CASES = {
    "AV1 Anime Encoders": {
        "positive": [
            "[Trix] Frieren - Beyond Journey's End (01-28) [AV1 10bit 1080p Opus].mkv",
            "[Breeze] Jujutsu Kaisen - S02 [1080p AV1 10bit Opus].mkv",
            "[INDEX] Cyberpunk: Edgerunners [1080p AV1 10bit DDP].mkv",
            "[Ironclad] Sousou no Frieren - 01 [AV1 1080p].mkv",
            "[Valenciano] One Piece - 1060 [1080p][AV1 10bit][AAC][Multi-Sub].mkv"
        ],
        "adversarial_negatives": [
            "Trix the Girl Who Leapt Through Time 2006 BD 1080p Av1 Fc875ba4.mkv", # Real release: title contains Trix
            "The.Breeze.Of.Summer.2024.1080p.AV1-PSA.mkv",
            "[AkihitoSubs] Gate [HEVC][x265][10Bit][Opus].mkv",
            "[NanDesuKa] Dungeon Meshi - 01 [1080p].mkv",
            "[CTR] Oshi no Ko - 01 [1080p].mkv",
            "[Judas] Sousou no Frieren - 01 [1080p x265].mkv",
            "[Erai-raws] Dungeon Meshi - 01 [1080p HEVC].mkv",
            "[HorribleSubs] Bleach - 01 [720p].mkv"
        ]
    },
    "AV1 Quality Encoders": {
        "positive": [
            "The.Matrix.1999.2160p.AV1.TrueHD.Atmos-Waldek.mkv",
            "The.Matrix.1999.2160p.AV1.TrueHD.Atmos-PRL.mkv",
            "Interstellar.2014.2160p.AV1.DTS-HD.MA-CHD.mkv",
            "X-Men.2000.2160p.HDR10.AV1-CHOPPERHITLER.mkv",
            "Dune.Part.Two.2024.2160p.DV.HDR10.AV1-TAoE.mkv",
            "Dune.Part.Two.2024.2160p.DV.HDR10.AV1-TAoE[rarbg].mkv",
            "[TAoE] Dune Part Two 2024 2160p AV1.mkv",
            "The.Fellowship.of.the.Ring.2001.Extended.2160p.AV1-CoSMiCSuRFeR.mkv"
        ],
        "adversarial_negatives": [
            "The.Waldek.Mystery.2020.1080p.AV1-PSA.mkv",
            "American.Gangster.2007.1080p.AV1-dAV1nci.mkv"
        ]
    },
    "AV1 Compact Encoders": {
        "positive": [
            "The.Lord.of.the.Rings.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "The.Lord.of.the.Rings.2003.Extended.2160p.AV1-dAV1nci[rarbg].mkv",
            "The.Lord.of.the.Rings.2003.Extended.1080p.AV1.DDP.Atmos-[UnAV1Chain].mkv",
            "LOTR.The.Return.Of.The.King.2003.PROPER.Bluray.2160p.AV1.HDR10.OPUS.7.1-UH",
            "The.Lord.of.the.Rings.2003.Extended.1080p.Bluray.OPUS.7.1.AV1-WhiskeyJack",
            "The.Shawshank.Redemption.1994.2160p.AV1-R&H.mkv",
            "The.Shawshank.Redemption.1994.2160p.AV1-R and H.mkv",
            "Movie.2024.1080p.AV1-LAZARUS.mkv",
            "Movie.2024.1080p.AV1-LAZARUS[TGx].mkv",
            "Movie.2024.1080p.AV1-DKV.mkv",
            "Movie.2024.1080p.AV1-TiZU.mkv",
            "Movie.2024.1080p.AV1-Saon.mkv",
            "Movie.2024.1080p.AV1-onlyfaffs.mkv",
            "Movie.2024.1080p.AV1-KIMJI.mkv",
            "Movie.2024.1080p.AV1-heTOrico.mkv",
            "Movie.2024.1080p.AV1-Rosy.mkv",
            "Movie.2024.1080p.AV1-Rosy[rarbg].mkv",
            "Movie.2024.1080p.AV1-anomoomin.mkv",
            "Movie.2024.1080p.AV1-CMCT.mkv",
            "Movie.2024.1080p.AV1-GRiMM.mkv",
            "Gladiator.2000.1080p.AV1-Dust.mkv",
            "Gladiator.2000.1080p.AV1-Dust[rarbg].mkv",
            "Movie.2024.1080p.AV1-DIN.mkv",
            "Movie.2024.1080p.AV1-GanG.mkv"
        ],
        "adversarial_negatives": [
            "Dust.to.Dust.2002.1080p.AV1-OtherGroup.mkv",          # Short word Dust in title
            "Dust.in.the.Wind.1986.1080p.AV1.mkv",
            "Red.Dust.2004.1080p.AV1.mkv",
            "Rosy.Business.2009.1080p.AV1-OtherGroup.mkv",        # Short word Rosy in title
            "The.Rosy.Life.1988.1080p.AV1.mkv",
            "Season.1.Episode.1.1080p.AV1.mkv",                   # Saon false positive
            "Saone.River.2020.1080p.AV1.mkv",
            "The.Dinner.2017.1080p.AV1-OtherGroup.mkv",           # DIN false positive
            "Dinosaur.2000.1080p.AV1.mkv",
            "Aladdin.2019.1080p.AV1.mkv",
            "American.Gangster.2007.1080p.AV1-OtherGroup.mkv",    # GanG false positive
            "Gang.Related.1997.1080p.AV1.mkv",
            "Gangs.of.New.York.2002.1080p.AV1.mkv",
            "The.Gang.1977.1080p.AV1.mkv",
            "The.UH.Oh.Files.2021.1080p.AV1-PSA.mkv",
            "Top.Gun.Maverick.2022.1080p.AV1-edge2020HD.mkv"
        ]
    },
    "AV1 Storage Savers": {
        "positive": [
            "Fallout.S01E01.1080p.AV1-PSA[ettv].mkv",
            "Fallout.S01E01.1080p.AV1-GalaxyRG[TGx].mkv",
            "Fallout.S01E01.1080p.AV1-MeGusta.mkv",
            "Fallout.S01E01.1080p.AV1-LUCY.mkv",
            "Fallout.S01E01.1080p.AV1-LUCY[TGx].mkv",
            "Fallout.S01E01.1080p.AV1-DKong.mkv",
            "Fallout.S01E01.1080p.AV1-Rapta.mkv",
            "Fallout.S01E01.1080p.AV1-GubrakZ.mkv",
            "Fallout.S01E01.1080p.AV1-Retr0.mkv",
            "Fallout.S01E01.1080p.AV1-SWAXXON.mkv",
            "Fallout.S01E01.1080p.AV1-FELIX12345.mkv"
        ],
        "adversarial_negatives": [
            "Lucy.2014.1080p.AV1-dAV1nci.mkv",                    # LUCY in title
            "I.Love.Lucy.S01E01.1080p.AV1-UH.mkv",
            "Donkey.Kong.Country.S01E01.1080p.AV1.mkv",
            "The.Matrix.1999.2160p.AV1-dAV1nci.mkv"
        ]
    },
    "Banned ENTROPY": {
        "positive": [
            "Movie.Title.2024.1080p.WEBRip.AV1-ENTROPY.mkv",
            "Movie.Title.2024.CAM.AV1-ENTROPY.mkv"
        ],
        "adversarial_negatives": [
            "Movie.Title.2024.1080p.AV1-dAV1nci.mkv"
        ]
    }
}

def run_battery():
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    print("================================================================================")
    print("REFINED CODEC & ENCODER REGEX AUDIT BATTERY")
    print("================================================================================")
    
    for category, pattern in REGEX_PATTERNS.items():
        print(f"\n--- Category: {category} ---")
        print(f"Pattern: {pattern}")
        regex = re.compile(pattern, re.IGNORECASE)
        
        pos_list = TEST_CASES.get(category, {}).get("positive", [])
        neg_list = TEST_CASES.get(category, {}).get("adversarial_negatives", [])
        
        for pos in pos_list:
            total_tests += 1
            if regex.search(pos):
                passed_tests += 1
                print(f"  [PASS] (+) '{pos}'")
            else:
                failed_tests += 1
                print(f"  [FAIL] (+) FALSE NEGATIVE: '{pos}' did not match!")
                
        for neg in neg_list:
            total_tests += 1
            if not regex.search(neg):
                passed_tests += 1
                print(f"  [PASS] (-) '{neg}'")
            else:
                failed_tests += 1
                print(f"  [FAIL] (-) FALSE POSITIVE: '{neg}' unexpectedly matched!")
                
    print("\n================================================================================")
    print(f"SUMMARY: {passed_tests} Passed, {failed_tests} Failed (Total: {total_tests})")
    print("================================================================================")
    
    return failed_tests == 0

if __name__ == "__main__":
    success = run_battery()
    sys.exit(0 if success else 1)
