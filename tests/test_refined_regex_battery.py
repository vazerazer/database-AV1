#!/usr/bin/env python3
"""
Refined AV1 Regex Test Battery with Site Tags, New Groups, and Strict Anchoring
Runs under re.IGNORECASE to replicate Radarr's RegexSpecificationBase.cs runtime.
Updated for Op 925: Census-Driven Tier Expansion & Alias Consolidation.
"""

import re
import sys

REGEX_PATTERNS = {
    # 1. Anime Encoders: Strictly anchored to leading bracket prefix ^\[(Group)\]
    "AV1 Anime Encoders": r"(?i)^\[(?:Trix|Breeze|INDEX|Sav1or|AV1ARY|Sokudo|RigAV1|Ironclad|Valenciano)\]",
    
    # 2. Quality Encoders: Anchored to trailing group hyphen, optional site tag, and optional extension
    # Op 925: Promotes dAV1nci, UH, Smokindevil; consolidates PRL.Waldek & case variants (DAV1NCI, TAOE)
    # Op 932: Tolerates trailing indexer dupe tags (_1, _2, _3, -xpost)
    "AV1 Quality Encoders": r"(?i)(?:^\[(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil)\]|-(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil|\[(?:CoSMiCSuRFeR|Waldek|PRL(?:\.Waldek|\s+Waldek)?|CHD|CHOPPERHITLER|TAoE|dAV1nci|UH|Smokindevil)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)",

    # 3. Compact Encoders: Anchored to trailing group hyphen, optional site tag, and optional extension
    # Op 925: Adds Toasty; consolidates R&H family (R&H, RandH, R and H, RH, extension artifacts)
    # Op 932: Tolerates trailing indexer dupe tags (_1, _2, _3, -xpost)
    "AV1 Compact Encoders": r"(?i)(?:^\[(?:UnAV1Chain|UserHEVC|RAV1NE|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH)\]|-(?:WhiskeyJack|WhiskyJack|edge2020|UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty|\[(?:UnAV1Chain|UserHEVC|RAV1NE|R[-._ ]?(?:and|&)[-._ ]?H|RandH|RH|LAZARUS|DKV|TiZU|Saon|onlyfaffs|KIMJI|heTOrico|Rosy|anomoomin|CMCT|GRiMM|Dust|DIN|GanG|Toasty)\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$)",
    
    # 4. Storage Savers: Anchored to trailing group hyphen, optional site tag, and optional extension
    "AV1 Storage Savers": r"(?i)(?:^\[(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART|LUCY|DKong|Rapta|GubrakZ|Retr0|SWAXXON|FELIX12345)\]|-(?:PSA|GalaxyRG|MeGusta|VXT|d3g|Ghost|rartv|ELiTE|LAMA|KaKa|YAWNTIC|BONE|GZ|CART|LUCY|DKong|Rapta|GubrakZ|Retr0|SWAXXON|FELIX12345|\[PSA\]|\[GalaxyRG\]|\[MeGusta\]|\[VXT\]|\[d3g\]|\[Ghost\]|\[rartv\]|\[ELiTE\]|\[LAMA\]|\[KaKa\]|\[YAWNTIC\]|\[BONE\]|\[GZ\]|\[CART\]|\[LUCY\]|\[DKong\]|\[Rapta\]|\[GubrakZ\]|\[Retr0\]|\[SWAXXON\]|\[FELIX12345\])(?:\[[a-z0-9_\-\.]+\])?(?:\.[a-z0-9]{2,4})?$)",

    # 5. Banned Groups
    "Banned ENTROPY": r"(?i)(?<![a-zA-Z0-9])ENTROPY\b",

    # 6. Plausible Release Group (Op 920: Provenance detection for nameless penalty)
    "Plausible Release Group": r"(?i)(?:^\[[A-Za-z0-9._ -]+\]|-(?:\s*\[(?!(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\])[A-Za-z0-9_.-]+\]|(?!(?:NL[- .]?sub|NL|DUTCH|GERMAN|FRENCH|ITA|SPANISH|SWE|DK|NOR|Fi|xpost|AV1|AV01|HEVC|x265|x264|HDR|DV|10bit|8bit|BRRip|BDRip|WEB[- .]?DL|WEBRip|BluRay|UHD|2160p|1080p|720p|AAC|DDP|AC3|TrueHD|Atmos|DTS|DTS-HD|Opus)(?:[\[\].\s-]|$)|\s*(?:NL[- .]?sub|NL|DUTCH|GERMAN|FRENCH|ITA|SPANISH|SWE|DK|NOR|Fi|xpost|AV1|AV01)(?:[\[\].\s-]|$)|\[(?:N-Z-B|TGx|rarbg|eztv|EtHD|YTS|ettv|rartv)\])\s*[A-Za-z0-9_&]+(?:[-. ][A-Za-z0-9_&]+)*(?:\[[a-zA-Z0-9_.-]+\])?)(?:\.[a-zA-Z0-9]{2,4})?$)",

    # 7. Foreign Dub (Op 922: Explicit foreign dub tags demotion)
    "Foreign Dub": r"(?i)\b(?:(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)[._ -]+(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)|(?:DUBBED|DUB|SYNCHRONISIERT|SYNCHRO)[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|CASTELLANO|RUSSIAN|POLISH|TURKISH|HINDI|DUTCH|DANISH|SWEDISH|NORWEGIAN|FINNISH|CZECH|HUNGARIAN|GER|FRE|FRA|ITA|ESP|SPA|RUS|POL|TUR|HIN)|(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB)[._ -]+DL|DL[._ -]+(?:GERMAN|FRENCH|ITALIAN|SPANISH|RUSSIAN|POLISH|TURKISH|HINDI)[._ -]+(?:DUBBED|DUB))\b",

    # 8. Legacy Trusted x264 (Op 930: Archival reference groups; Op 932: dupe tag tolerance)
    "Legacy Trusted x264": r"(?i)(?:^|[\s._-])(?:CtrlHD|GRiM|PiRaTeS|BHDStudio|TAoE|DON|EbP|playHD|Z0N3|LoRD|MrTentsaw)(?:\[[^\]]*\])?(?:\.[a-z0-9]{2,4})?(?:[-._ ]?(?:[0-9]+|xpost))*$",

    # 9. LQ Release Title (Op 932: Cleaned naming hygiene specifications)
    "LQ Release Title": r"(?i)\b(?:1XBET|BEN[ ._-]THE[ ._-]MEN|Feranki1980|GalaxyRG|SWTYBLZ|TeeWee|TEKNO3D|Will1869|READ(\s|\.)+NOTE)\b|(?:[-._]D3US|D3US[-._])"
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
            "Trix the Girl Who Leapt Through Time 2006 BD 1080p Av1 Fc875ba4.mkv",
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
            "Stalker.1979.1080p.AV1-PRL.Waldek.mkv",
            "Stalker.1979.1080p.AV1-PRL Waldek.mkv",
            "Interstellar.2014.2160p.AV1.DTS-HD.MA-CHD.mkv",
            "X-Men.2000.2160p.HDR10.AV1-CHOPPERHITLER.mkv",
            "Dune.Part.Two.2024.2160p.DV.HDR10.AV1-TAoE.mkv",
            "Dune.Part.Two.2024.2160p.DV.HDR10.AV1-TAOE.mkv",
            "Dune.Part.Two.2024.2160p.DV.HDR10.AV1-TAoE[rarbg].mkv",
            "[TAoE] Dune Part Two 2024 2160p AV1.mkv",
            "The.Fellowship.of.the.Ring.2001.Extended.2160p.AV1-CoSMiCSuRFeR.mkv",
            "The.Lord.of.the.Rings.2003.Extended.2160p.HDR.UHD.BluRay.AV1.DDP5.1.Atmos-dAV1nci",
            "The.Lord.of.the.Rings.2003.Extended.2160p.AV1-DAV1NCI.mkv",
            "[dAV1nci] The Matrix 1999 2160p UHD BluRay",
            "Inception.2010.2160p.UHD.BluRay.AV1-UH",
            "Fury.2014.2160p.UHD.BluRay.AV1.TrueHD.Atmos-Smokindevil.mkv",
            "Fury.2014.2160p.UHD.BluRay.AV1.TrueHD.Atmos-SmokinDevil.mkv"
        ],
        "adversarial_negatives": [
            "The.Waldek.Mystery.2020.1080p.AV1-PSA.mkv",
            "The.Thing.1982.2160p.UHD.BluRay.AV1-Toasty.mkv",
            "Blade.Runner.1982.2160p.UHD.BluRay.AV1-R and H.mkv",
            "Something.2020.2160p.AV1-FLUX.mkv",
            "Something.2020.2160p.AV1-Bi0hazard.mkv"
        ]
    },
    "AV1 Compact Encoders": {
        "positive": [
            "The.Lord.of.the.Rings.2003.Extended.1080p.AV1.DDP.Atmos-[UnAV1Chain].mkv",
            "The.Lord.of.the.Rings.2003.Extended.1080p.Bluray.OPUS.7.1.AV1-WhiskeyJack",
            "The.Shawshank.Redemption.1994.2160p.AV1-R&H.mkv",
            "The.Shawshank.Redemption.1994.2160p.AV1-R and H.mkv",
            "The.Shawshank.Redemption.1994.2160p.AV1-RandH.mkv",
            "Blade.Runner.1982.2160p.UHD.BluRay.AV1-RH",
            "Blade.Runner.1982.2160p.UHD.BluRay.AV1-RH.mkv",
            "Blade.Runner.1982.2160p.UHD.BluRay.AV1-R&H.mkv",
            "[R and H] Blade Runner 1982 2160p UHD BluRay",
            "[RH] Blade Runner 1982 2160p UHD BluRay",
            "The.Thing.1982.2160p.UHD.BluRay.AV1-Toasty",
            "[Toasty] The Thing 1982 2160p UHD BluRay AV1",
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
            "The.Lord.of.the.Rings.2003.Extended.2160p.AV1-dAV1nci",     # Promoted to Quality
            "Inception.2010.2160p.UHD.BluRay.AV1-UH",                    # Promoted to Quality
            "Fury.2014.2160p.UHD.BluRay.AV1.TrueHD.Atmos-Smokindevil",    # Promoted to Quality
            "Durham.1988.2160p.UHD.BluRay.AV1-OtherGroup.mkv",          # Mid-title 'rh'
            "The.Rhino.2020.2160p.AV1-Unknown.mkv",                      # Mid-title 'rh'
            "Movie.2020.2160p.AV1-RHGroupX.mkv",                         # Non-isolated 'RH'
            "Dust.to.Dust.2002.1080p.AV1-OtherGroup.mkv",
            "Dust.in.the.Wind.1986.1080p.AV1.mkv",
            "Red.Dust.2004.1080p.AV1.mkv",
            "Rosy.Business.2009.1080p.AV1-OtherGroup.mkv"
        ]
    },
    "AV1 Storage Savers": {
        "positive": [
            "Movie.2024.1080p.AV1-PSA.mkv",
            "Movie.2024.1080p.AV1-GalaxyRG.mkv",
            "Movie.2024.1080p.AV1-MeGusta.mkv",
            "Movie.2024.1080p.AV1-VXT.mkv",
            "Movie.2024.1080p.AV1-d3g.mkv",
            "Movie.2024.1080p.AV1-Ghost.mkv",
            "Movie.2024.1080p.AV1-rartv.mkv",
            "Movie.2024.1080p.AV1-ELiTE.mkv",
            "Movie.2024.1080p.AV1-LAMA.mkv",
            "Movie.2024.1080p.AV1-KaKa.mkv",
            "Movie.2024.1080p.AV1-YAWNTIC.mkv",
            "Movie.2024.1080p.AV1-BONE.mkv",
            "Movie.2024.1080p.AV1-GZ.mkv",
            "Movie.2024.1080p.AV1-CART.mkv",
            "Movie.2024.1080p.AV1-LUCY.mkv",
            "Movie.2024.1080p.AV1-DKong.mkv",
            "Movie.2024.1080p.AV1-Rapta.mkv",
            "Movie.2024.1080p.AV1-GubrakZ.mkv",
            "Movie.2024.1080p.AV1-Retr0.mkv",
            "Movie.2024.1080p.AV1-SWAXXON.mkv",
            "Movie.2024.1080p.AV1-FELIX12345.mkv"
        ],
        "adversarial_negatives": [
            "The.Ghost.Writer.2010.1080p.AV1-dAV1nci.mkv",
            "A.Bone.to.Pick.2015.1080p.AV1-WhiskeyJack.mkv",
            "Lucy.in.the.Sky.2019.1080p.AV1-Waldek.mkv",
            "Elite.Squad.2007.1080p.AV1-CHD.mkv"
        ]
    },
    "Banned ENTROPY": {
        "positive": [
            "Movie.Title.2024.1080p.WEBRip.AV1-ENTROPY.mkv",
            "Movie.Title.2024.CAM.AV1-ENTROPY.mkv",
            "Movie.Title.2024.1080p.WEBRip.AV1-entropy.mkv",
            "Movie.Title.2024.1080p.WEBRip.AV1-Entropy.mkv"
        ],
        "adversarial_negatives": [
            "Movie.Title.2024.1080p.AV1-dAV1nci.mkv"
        ]
    },
    "Plausible Release Group": {
        "positive": [
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-RandH.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-R&H.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-R and H.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-Smokindevil.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-CoSMiCSuRFeR[rarbg].mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-Rosy-xpost.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-DarQ.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-hallowed.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-MainFrame.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-BYNDR.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-D-Z0N3.mkv",
            "[TAoE] The Bourne Supremacy 2004 2160p AV1.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-[dAV1nci].mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-UnknownGroup.mkv"
        ],
        "adversarial_negatives": [
            "The Bourne Supremacy (2004) - 2160p HDR - AV1 BRRip - NLsub",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1.BRRip-NLsub.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-NLsub",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1 - NLsub.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-xpost.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-[N-Z-B].mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-[TGx].mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-[rarbg].mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-NL.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-DUTCH.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-SWE.mkv",
            "The.Bourne.Supremacy.2004.2160p.HDR.AV1-FRENCH.mkv"
        ]
    },
    "Foreign Dub": {
        "positive": [
            "Das.Bourne.Ultimatum.2007.German.DUBBED.DL.EAC3.2160p.HDR.BluRay.AV1-Bi0hazard",
            "The.Matrix.1999.German.DUBBED.2160p.AV1-Group",
            "Inception.2010.French.DUBBED.1080p.AV1-Group",
            "Interstellar.2014.Italian.DUB.2160p.HDR.AV1",
            "Gladiator.2000.Spanish.DUBBED.2160p.AV1",
            "Dune.2021.Russian.DUB.1080p.AV1",
            "Avatar.2009.Polish.DUBBED.2160p.AV1",
            "Movie.2024.Turkish.DUBBED.1080p",
            "Movie.2024.Hindi.DUBBED.1080p",
            "Movie.2024.DUBBED.German.1080p",
            "Movie.2024.German-DUBBED-DL.1080p",
            "Movie.2024.DL.German.DUBBED.1080p",
            "Movie.2024.GER.DUB.1080p",
            "Movie.2024.German.SYNCHRONISIERT.1080p"
        ],
        "adversarial_negatives": [
            "Blade.Runner.1982.Final.Cut.2160p.UHD.BluRay.DTS.5.1.DV.HDR.AV1-RandH",
            "The.Bourne.Supremacy.2004.2160p.MA.WEB-DL.DTS-X.7.1.DV.HDR.H.265-BYNDR",
            "The.Matrix.1999.MULTi.2160p.AV1-Group",
            "Inception.2010.MULTi.VF2.1080p.AV1-Group",
            "Movie.2024.Dual.Audio.1080p.AV1",
            "Movie.2024.Dual-Audio.2160p.x265",
            "Dublin.Murders.2019.S01E01.1080p.AV1",
            "The.Dub.2020.1080p.AV1",
            "Dubliners.1987.1080p.BluRay.x265",
            "Movie.2024.German.Subbed.1080p.AV1",
            "Movie.2024.German.Sub.1080p",
            "Movie.2024.NLsub.1080p"
        ]
    },
    "Legacy Trusted x264": {
        "positive": [
            "Blue.Valentine.2010.1080p.BluRay.DTS.x264-CtrlHD",
            "Project.X.2012.1080p.BluRay.DTS.x264-CtrlHD.mkv",
            "Hoosiers.1986.1080p.BluRay.DTS.x264-PiRaTeS",
            "The.Right.Stuff.1983.1080p.BluRay.DTS.x264-BHDStudio",
            "The.Perks.of.Being.a.Wallflower.2012.1080p.BluRay.DTS.x264-PiRaTeS",
            "The.Ides.of.March.2011.1080p.BluRay.DTS.x264-Z0N3",
            "Locke.2014.1080p.BluRay.DTS.x264-LoRD",
            "The.Hunt.2012.1080p.BluRay.DD5.1.x264-EbP",
            "A.Royal.Affair.2012.1080p.BluRay.DTS.x264-MrTentsaw",
            "The.Matrix.1999.1080p.BluRay.x264-DON"
        ],
        "adversarial_negatives": [
            "Generic.Movie.2024.1080p.BluRay.x264-SPARKS",
            "Movie.2024.1080p.BluRay.x264-YIFY",
            "Movie.2024.1080p.BluRay.x264-YTS",
            "Movie.2024.1080p.BluRay.x264-RARBG",
            "Movie.2024.1080p.BluRay.x264-FLUX",
            "Movie.2024.1080p.BluRay.x264-hallowed"
        ]
    },
    "LQ Release Title": {
        "positive": [
            "Movie.Title.2024.1080p.1XBET.x265",
            "Movie.Title.2024.1080p.BEN_THE_MEN",
            "Movie.Title.2024.1080p.Feranki1980",
            "Movie.Title.2024.1080p.GalaxyRG",
            "Movie.Title.2024.1080p.TEKNO3D",
            "Movie.Title.2024.1080p.READ.NOTE.x265",
            "Movie.Title.2024.1080p.HDTV.D3US"
        ],
        "adversarial_negatives": [
            "The.Wolverine.2013.2160p.AMZN.WEB-DL.AV1-R&H_1",
            "The.Wolverine.2013.2160p.AMZN.WEB-DL.AV1-R&H.mkv",
            "The.Wolverine.2013.2160p.AMZN.WEB-DL.AV1-R&H.mkv-xpost",
            "X-Men.2000.2160p.AV1-ChopperHitler_3",
            "Hoosiers.1986.1080p.AMZN.WEB-DL.DDP.5.1.H.264-PiRaTeS",
            "The.Perks.of.Being.a.Wallflower.2012.1080p.BluRay.DTS.x264-PiRaTeS"
        ]
    }
}

def run_tests():
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    print("================================================================================")
    print("REFINED AV1 REGEX TEST BATTERY (OP 925: TIER EXPANSION & ALIAS CONSOLIDATION)")
    print("================================================================================")

    for cf_name, test_data in TEST_CASES.items():
        pattern = REGEX_PATTERNS[cf_name]
        compiled = re.compile(pattern)
        print(f"\n--- Testing Custom Format: {cf_name} ---")
        
        # 1. Positives
        for title in test_data.get("positive", []):
            total_tests += 1
            if compiled.search(title):
                passed_tests += 1
            else:
                failed_tests += 1
                print(f"  [FAIL - POSITIVE MISSED] {title}")

        # 2. Adversarial Negatives
        for title in test_data.get("adversarial_negatives", []):
            total_tests += 1
            if not compiled.search(title):
                passed_tests += 1
            else:
                failed_tests += 1
                print(f"  [FAIL - FALSE POSITIVE] {title}")

    print("\n================================================================================")
    print(f"RESULTS: {passed_tests}/{total_tests} tests passed ({failed_tests} failures)")
    print("================================================================================")

    if failed_tests > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
