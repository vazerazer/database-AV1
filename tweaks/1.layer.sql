-- Local layer for Movies 2160p. Runs after the Dumpstarr base.
-- DTS-HD is allowed (the core track plays). TrueHD stays blocked
-- except for trusted tiered groups. The 14-40 GB window is only
-- the mid-tier bonus, not a penalty and not a cap on HD audio.
UPDATE quality_profile_custom_formats
SET score = 0
WHERE quality_profile_name = 'Movies 2160p'
  AND custom_format_name = 'DTS-HD MA'
  AND arr_type = 'radarr'
  AND score = -10000;
UPDATE quality_profile_custom_formats
SET score = 0
WHERE quality_profile_name = 'Movies 2160p'
  AND custom_format_name = 'DTS-HD HRA'
  AND arr_type = 'radarr'
  AND score = -10000;
UPDATE quality_profile_custom_formats
SET score = 0
WHERE quality_profile_name = 'Movies 2160p'
  AND custom_format_name = 'DTS-X'
  AND arr_type = 'radarr'
  AND score = -10000;
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite TrueHD Trusted Groups', '^(0BSiDiAN|147|3L|4KDVS|aBa|ADE|AFKI|afm72|Aio|AJP69|aNDy|ARiN|ASD87|ATELiER|AViATOR|AZVD|b0mbardiers|Baer|BakedFEL|Bandi|BAT1|BBQ|BBW|BeiTai|BHDStudio|BiZKiT|Bluespots|BLURANiUM|BlzT|BMF|BNL|BRUTE|BSTD|BTN|BV|c0kE|Cache|CALiGARi|CART|Celdra|cFc|Chotab|CiNEPHiLES|CJ|CMCT|coffee|CONSORTiUM|CREATiVE|CRiME|CRiSC|CRX|CtrlHD|D-Z0N3|Dariush|DarQ|de[42]|decibeL|DEFLATE|DEPTH|DiRTY|DiscoD|dkore|DON|E.N.D|E1|E76|EA|EBCP|EbP|Eby|eckomega|edge2020|EDPH|EMERALD|ENDSkY|EPSiLON|ESiR|EwT|EXCiSION|eXterminator|faBR|FANDANGO|FLAME|FoRM|FraMeSToR|FreetheFish|Friday|FTO|Funner|G4MBiT|GALAXY|GALVANiZE|Garshasp|Geek|Ghost|GL|GOLIATN|GR|GrapeHD|greenHD|GS88|GUHZER|GutS|Gyroscope|GZ|H@M|HaB|hallowed|HANDJOB|hdalx|HDC|HDChina|HDL|HDMaNiAcS|HDmonSK|HDmux|HDV|HDv0T|HDxT|HiDt|HiFi|HiP|HiSD|HONE|HQMUX|HR|HypStu|IAMABLE|IDE|iFT|iLL|iLoveHD|Ime|IMF|IMNEWHERE|iNFLiKTED|iON|Ivandro|J2G|j3rico|JewelBox|JKP|JM|JustWatch|KamiKaze|KAN3D2M|Kappa|KASHMiR|Kitsune|KnG|KRaLiMaRKo|Krispy|Kururun|Langbard|LAZARUS|LAZY|LEGi0N|LESTiN|LiNG|LION|LM|LolHD|LoRD|Lulz|luvBB|MaG|MainFrame|maniac|MCR|MDR|MGs|MiLQ|MiMiC|MKu|MONOLITH|Moshy|Narkyy|Natty|Natuyuki|NCmt|NiBuRu|NiP|nmd|NorTV|NoVA|NTb|NyHD|O2STK|OB1|OmertaHD|ORBiT|ORiGEN|Otaibi|P0W4HD|Palm|Panda|pcroland|Penumbra|PerfectionHD|PiG30N|PiMP|PiPicK|PiRAMiDHEAD|PiRaTeS|playBD|playHD|PmP|POH|Positive|PP|Prestige|PriMeHD|PTer|PTP|PussyFoot|PuTao|QOQ|QxR|r00t|RandomBytes|RCVR|RDK123|ReaLHD|REBORN|REPTiLE|ReQuEsT|RiCO|RightSIZE|RO|ROCiNANTE|RoJYA|Rose3Thorn|rttr|RZeroX|SA89|SaL|SAMPA|SaNcTi|sbR|Seal|ShAnKs|SiCFoI|Silence|SillyBird|SiMPLE|Skazhutin|Slappy|Softboat|SoLaR|SOP|SpaceHD|SPEED|Spekt0r|SPHD|STRiKES|SuBHD|SuccessfulCrab|SUPER|SURCODE|SWTYBLZ|t3nzin|TAiCHi|TayTO|TBB|TDD|TeamSyndicate|TEPES|TERMiNAL|ThD|TnP|ToK|TRiToN|TRUNKS|Uld|ULTRAHDCLUB|UxO|VD|VietHD|ViSUM|VLAD|VorteX|Vyndros|W4NK3R|WATCHABLE|Weasley|WEBDV|WESTSiDE|WhiteRhino|WiHD|WiLDCAT|WiLF|WMING|xander|XFR|YOGI|ZAL|ZIMBO|ZiNC|ZnP|ZoroSenpai|ZQ)$', 'Blu-ray, baseline, and Dictionarry quality/balanced/remux groups, minus TRaSH LQ.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('TrueHD', 'Not Trusted Group', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('TrueHD', 'Not Trusted Group', 'Lite TrueHD Trusted Groups');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('TrueHD Missing', 'Not Trusted Group', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('TrueHD Missing', 'Not Trusted Group', 'Lite TrueHD Trusted Groups');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite Mid UHD Groups', '^(4KDVS|ATELiER|b0mbardiers|BakedFEL|BlzT|BSTD|BV|c0kE|Chotab|D-Z0N3|DEFLATE|DEPTH|dkore|EDPH|ESiR|faBR|iFT|j3rico|JustWatch|Kitsune|LESTiN|NCmt|NTb|ORBiT|RoJYA|Softboat|SURCODE|TAoE|TDD|TnP|TRUNKS|WATCHABLE)$', 'Mid-size 4K Blu-ray encoders.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite T3 Tail', '(?<=[-._ \[(])(?:(?:Weasley|DiscoD|DarQ)[ ._-])?(?:BHDStudio|hallowed|WEBDV|HONE|PTer|SPHD)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed UHD tier 3 group at the end of the name.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite hallowed Tail', '(?<=[-._ \[(])(?:hallowed)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed hallowed group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite BHDStudio Tail', '(?<=[-._ \[(])(?:BHDStudio)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed BHDStudio group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite WEB T1 Tail', '(?<=[-._ \[(])(?:(?:Weasley|DiscoD|DarQ)[ ._-])?(?:ZoroSenpai|BLUTONiUM|Kitsune|NOSiViD|TheFarm|MADSKY|ABBIE|AJP69|BYNDR|GNOME|KiNGS|TEPES|APEX|CMRG|CRFW|CRUD|FLUX|HONE|PAXA|PEXA|RAWR|XEPA|NTb|NTG|SiC)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed WEB tier 1 group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite WEB T2 Tail', '(?<=[-._ \[(])(?:Flights|PHOENiX|playWEB|monkee|4KBEC|CEBEX|MZABI|SMURF|TOMMY|XEBEC|MiU|SbR|dB)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed WEB tier 2 group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite WEB Any Tail', '(?<=[-._ \[(])(?:(?:Weasley|DiscoD|DarQ)[ ._-])?(?:NINJACENTRAL|GNOMiSSiON|SwAgLaNdEr|ZoroSenpai|BLUTONiUM|SLiGNOME|Flights|Kitsune|NOSiViD|PHOENiX|playWEB|TheFarm|MADSKY|monkee|ROCCaT|4KBEC|ABBIE|AJP69|BLOOM|BYNDR|CEBEX|Dooky|GNOME|KiNGS|MZABI|SiGMA|SMURF|TEPES|TOMMY|XEBEC|APEX|CMRG|CRFW|CRUD|FLUX|HONE|NPMS|PAXA|PEXA|RAWR|XEPA|MiU|NTb|NTG|SbR|SiC|dB)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed WEB tier 1-3 group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite Trusted Tail', '(?<=[-._ \[(])(?:(?:Weasley|DiscoD|DarQ)[ ._-])?(?:SuccessfulCrab|NINJACENTRAL|GNOMiSSiON|SwAgLaNdEr|ZoroSenpai|BHDStudio|BLUTONiUM|hallowed|SLiGNOME|Flights|Kitsune|NOSiViD|PHOENiX|PiRaTeS|playWEB|TheFarm|Vyndros|Weasley|DiscoD|MADSKY|monkee|ROCCaT|4KBEC|ABBIE|AJP69|BLOOM|BYNDR|CEBEX|Dooky|GNOME|KiNGS|MZABI|SiGMA|SMURF|TEPES|TOMMY|WEBDV|XEBEC|APEX|CMRG|CRFW|CRUD|DarQ|FLUX|HONE|NPMS|PAXA|PEXA|PTer|RAWR|SPHD|XEPA|MiU|NTb|NTG|SbR|SiC|dB)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed trusted group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite Baseline Tail', '(?<=[-._ \[(])(?:SuccessfulCrab|PiRaTeS|Vyndros|Weasley|DiscoD|DarQ)(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'Misparsed baseline group.');
INSERT INTO regular_expressions (name, pattern, description) VALUES ('Lite HONE Family', '(?<=[-._ \[(])(?:Weasley|DiscoD|DarQ)[ ._-]HONE(?:\.mkv|\.mp4|_mp4)?(?:-(?!HONE\b)[A-Za-z0-9]{2,10})?(?:-xpost)?(?:\[[A-Za-z0-9.]+\])?-?\)?\]?$', 'HONE member names Dumpstarr already trusts.');
INSERT INTO custom_formats (name, description) VALUES ('Lite UHD Mid Tier',
'2160p Blu-ray encode, not a remux, 14-40 GB, from Dictionarry T3-T5 groups that Dumpstarr does not already tier, plus dkore and TAoE.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Mid Tier', '2160p', 'resolution', 'all', 0, 1);
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('Lite UHD Mid Tier', '2160p', '2160p');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Mid Tier', 'Bluray', 'source', 'all', 0, 1);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite UHD Mid Tier', 'Bluray', 'bluray');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Mid Tier', 'Not Remux', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite UHD Mid Tier', 'Not Remux', 'Remux');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Mid Tier', '14-40 GB', 'size', 'all', 0, 1);
INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes) VALUES ('Lite UHD Mid Tier', '14-40 GB', 15032385536, 42949672960);
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Mid Tier', 'Mid Groups', 'release_group', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite UHD Mid Tier', 'Mid Groups', 'Lite Mid UHD Groups');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite UHD Mid Tier', 'radarr', 1800);
INSERT INTO custom_formats (name, description) VALUES ('Lite UHD Tier 03 (Name Fallback)',
'UHD Blu-ray tier 3 when the group is only visible at the end of the name.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Tier 03 (Name Fallback)', '2160p', 'resolution', 'all', 0, 1);
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('Lite UHD Tier 03 (Name Fallback)', '2160p', '2160p');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'Bluray', 'source', 'all', 0, 1);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'Bluray', 'bluray');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'Not Remux', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'Not Remux', 'Remux');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'T3 tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'T3 tail', 'Lite T3 Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'Not T3 group', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite UHD Tier 03 (Name Fallback)', 'Not T3 group', 'TRaSH UHD Bluray Tier 03');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite UHD Tier 03 (Name Fallback)', 'radarr', 1800);
INSERT INTO custom_formats (name, description) VALUES ('Lite hallowed (Name Fallback)',
'hallowed bonus when the group is only visible at the end of the name.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite hallowed (Name Fallback)', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite hallowed (Name Fallback)', 'tail', 'Lite hallowed Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite hallowed (Name Fallback)', 'Not hallowed', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite hallowed (Name Fallback)', 'Not hallowed', 'hallowed');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite hallowed (Name Fallback)', 'radarr', 600);
INSERT INTO custom_formats (name, description) VALUES ('Lite BHDStudio (Name Fallback)',
'BHDStudio bonus when the group is only visible at the end of the name.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite BHDStudio (Name Fallback)', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite BHDStudio (Name Fallback)', 'tail', 'Lite BHDStudio Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite BHDStudio (Name Fallback)', 'Not BHDStudio', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite BHDStudio (Name Fallback)', 'Not BHDStudio', 'BHDStudio');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite BHDStudio (Name Fallback)', 'radarr', 550);
INSERT INTO custom_formats (name, description) VALUES ('Lite Baseline (Name Fallback)',
'Baseline bonus for DarQ, DiscoD, PiRaTeS, SuccessfulCrab, Vyndros, and Weasley when the group was not parsed.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite Baseline (Name Fallback)', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite Baseline (Name Fallback)', 'tail', 'Lite Baseline Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite Baseline (Name Fallback)', 'Not baseline', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite Baseline (Name Fallback)', 'Not baseline', 'Dumpstarr Baseline Groups');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite Baseline (Name Fallback)', 'radarr', 500);
INSERT INTO custom_formats (name, description) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'WEB tier when the group is only visible at the end of the name.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'WEB-DL', 'source', 'all', 0, 0);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'WEB-DL', 'web_dl');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'WEBRip', 'source', 'all', 0, 0);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'WEBRip', 'webrip');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'tail', 'Lite WEB T1 Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'Not T1', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite WEB Tier 01 (Name Fallback)', 'Not T1', 'TRaSH WEB Tier 01 (Radarr)');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite WEB Tier 01 (Name Fallback)', 'radarr', 1500);
INSERT INTO custom_formats (name, description) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'WEB tier when the group is only visible at the end of the name.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'WEB-DL', 'source', 'all', 0, 0);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'WEB-DL', 'web_dl');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'WEBRip', 'source', 'all', 0, 0);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'WEBRip', 'webrip');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'tail', 'Lite WEB T2 Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'Not T2', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite WEB Tier 02 (Name Fallback)', 'Not T2', 'TRaSH WEB Tier 02 (Radarr)');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite WEB Tier 02 (Name Fallback)', 'radarr', 1450);
INSERT INTO custom_formats (name, description) VALUES ('Lite MA Preferred (Name Fallback)',
'MA Preferred when the WEB group is only visible at the end of the name.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'DD+', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'DD+', 'Dolby Digital +');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'HDR', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'HDR', 'HDR');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'MA', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'MA', 'Movies Anywhere');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'WEB-DL', 'source', 'all', 0, 1);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('Lite MA Preferred (Name Fallback)', 'WEB-DL', 'web_dl');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'tail', 'Lite WEB Any Tail');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'Not T1', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'Not T1', 'TRaSH WEB Tier 01 (Radarr)');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'Not T2', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'Not T2', 'TRaSH WEB Tier 02 (Radarr)');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite MA Preferred (Name Fallback)', 'Not T3', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite MA Preferred (Name Fallback)', 'Not T3', 'TRaSH WEB Tier 03 (Radarr)');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite MA Preferred (Name Fallback)', 'radarr', 2000);
INSERT INTO custom_formats (name, description) VALUES ('Lite Group Missing Offset',
'Cancels Group Missing when the name ends in a group Dumpstarr already scores.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite Group Missing Offset', 'Group missing', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite Group Missing Offset', 'Group missing', 'Release Group Missing');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite Group Missing Offset', 'tail', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite Group Missing Offset', 'tail', 'Lite Trusted Tail');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite Group Missing Offset', 'radarr', 10000);
INSERT INTO custom_formats (name, description) VALUES ('Lite HONE Family Offset',
'Cancels HONE (Bad Name) for DarQ, DiscoD, and Weasley HONE names.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite HONE Family Offset', 'HONE title', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite HONE Family Offset', 'HONE title', 'HONE Release Title');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite HONE Family Offset', 'Not HONE group', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite HONE Family Offset', 'Not HONE group', 'HONE');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('Lite HONE Family Offset', 'family', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('Lite HONE Family Offset', 'family', 'Lite HONE Family');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'Lite HONE Family Offset', 'radarr', 10000);
UPDATE quality_profiles SET description = description || char(10) || 'Local layer: DTS-HD scores 0, TrueHD stays blocked except for trusted groups, and a 14-40 GB mid-size Blu-ray tier scores 1800.' WHERE name = 'Movies 2160p' AND description NOT LIKE '%Local layer:%';
