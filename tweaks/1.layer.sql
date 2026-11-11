-- Local layer for Movies 2160p. Runs after the Dumpstarr base.
-- DTS-HD is allowed (the core track plays). TrueHD, including
-- TrueHD Atmos, scores -10000 for every release group. The shared
-- TrueHD format still skips trusted groups; TrueHD Block covers
-- those groups on this profile only. The 25-60 GB window is only
-- a bonus for preferred disc groups, not a penalty and not a cap
-- on HD audio. Remuxes and releases outside the window get nothing
-- extra. Group Missing and HONE (Bad Name) are left as Dumpstarr ships them.
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
INSERT INTO regular_expressions (name, pattern, description) VALUES ('TrueHD Trusted Groups', '^(0BSiDiAN|147|3L|4KDVS|aBa|ADE|AFKI|afm72|Aio|AJP69|aNDy|ARiN|ASD87|ATELiER|AViATOR|AZVD|b0mbardiers|Baer|BakedFEL|Bandi|BAT1|BBQ|BBW|BeiTai|BHDStudio|BiZKiT|Bluespots|BLURANiUM|BlzT|BMF|BNL|BRUTE|BSTD|BTN|BV|c0kE|Cache|CALiGARi|CART|Celdra|cFc|Chotab|CiNEPHiLES|CJ|CMCT|coffee|CONSORTiUM|CREATiVE|CRiME|CRiSC|CRX|CtrlHD|D-Z0N3|Dariush|DarQ|de[42]|decibeL|DEFLATE|DEPTH|DiRTY|DiscoD|dkore|DON|E.N.D|E1|E76|EA|EBCP|EbP|Eby|eckomega|edge2020|EDPH|EMERALD|ENDSkY|EPSiLON|ESiR|EwT|EXCiSION|eXterminator|faBR|FANDANGO|FLAME|FoRM|FraMeSToR|FreetheFish|Friday|FTO|Funner|G4MBiT|GALAXY|GALVANiZE|Garshasp|Geek|Ghost|GL|GOLIATN|GR|GrapeHD|greenHD|GS88|GUHZER|GutS|Gyroscope|GZ|H@M|HaB|hallowed|HANDJOB|hdalx|HDC|HDChina|HDL|HDMaNiAcS|HDmonSK|HDmux|HDV|HDv0T|HDxT|HiDt|HiFi|HiP|HiSD|HONE|HQMUX|HR|HypStu|IAMABLE|IDE|iFT|iLL|iLoveHD|Ime|IMF|IMNEWHERE|iNFLiKTED|iON|Ivandro|J2G|j3rico|JewelBox|JKP|JM|JustWatch|KamiKaze|KAN3D2M|Kappa|KASHMiR|Kitsune|KnG|KRaLiMaRKo|Krispy|Kururun|Langbard|LAZARUS|LAZY|LEGi0N|LESTiN|LiNG|LION|LM|LolHD|LoRD|Lulz|luvBB|MaG|MainFrame|maniac|MCR|MDR|MGs|MiLQ|MiMiC|MKu|MONOLITH|Moshy|Narkyy|Natty|Natuyuki|NCmt|NiBuRu|NiP|nmd|NorTV|NoVA|NTb|NyHD|O2STK|OB1|OmertaHD|ORBiT|ORiGEN|Otaibi|P0W4HD|Palm|Panda|pcroland|Penumbra|PerfectionHD|PiG30N|PiMP|PiPicK|PiRAMiDHEAD|PiRaTeS|playBD|playHD|PmP|POH|Positive|PP|Prestige|PriMeHD|PTer|PTP|PussyFoot|PuTao|QOQ|QxR|r00t|RandomBytes|RCVR|RDK123|ReaLHD|REBORN|REPTiLE|ReQuEsT|RiCO|RightSIZE|RO|ROCiNANTE|RoJYA|Rose3Thorn|rttr|RZeroX|SA89|SaL|SAMPA|SaNcTi|sbR|Seal|ShAnKs|SiCFoI|Silence|SillyBird|SiMPLE|Skazhutin|Slappy|Softboat|SoLaR|SOP|SpaceHD|SPEED|Spekt0r|SPHD|STRiKES|SuBHD|SuccessfulCrab|SUPER|SURCODE|SWTYBLZ|t3nzin|TAiCHi|TayTO|TBB|TDD|TeamSyndicate|TEPES|TERMiNAL|ThD|TnP|ToK|TRiToN|TRUNKS|Uld|ULTRAHDCLUB|UxO|VD|VietHD|ViSUM|VLAD|VorteX|Vyndros|W4NK3R|WATCHABLE|Weasley|WEBDV|WESTSiDE|WhiteRhino|WiHD|WiLDCAT|WiLF|WMING|xander|XFR|YOGI|ZAL|ZIMBO|ZiNC|ZnP|ZoroSenpai|ZQ)$', 'Blu-ray, baseline, and Dictionarry quality/balanced/remux groups, minus TRaSH LQ.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('TrueHD', 'Not Trusted Group', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('TrueHD', 'Not Trusted Group', 'TrueHD Trusted Groups');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)
VALUES ('TrueHD Missing', 'Not Trusted Group', 'release_group', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)
VALUES ('TrueHD Missing', 'Not Trusted Group', 'TrueHD Trusted Groups');
INSERT INTO custom_formats (name, description) VALUES ('TrueHD Block',
'TrueHD, including TrueHD Atmos, from a trusted release group. Movies 2160p scores this at -10000. The shared TrueHD format still skips those groups. A title that also shows DD, DD+, DTS, or FLAC does not match.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('TrueHD Block', 'Not DTS', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('TrueHD Block', 'Not DTS', 'DTS');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('TrueHD Block', 'Not Dolby Digital', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('TrueHD Block', 'Not Dolby Digital', 'Dolby Digital');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('TrueHD Block', 'Not Dolby Digital +', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('TrueHD Block', 'Not Dolby Digital +', 'Dolby Digital +');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('TrueHD Block', 'Not FLAC', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('TrueHD Block', 'Not FLAC', 'FLAC');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('TrueHD Block', 'TrueHD', 'release_title', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('TrueHD Block', 'TrueHD', 'TrueHD');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('TrueHD Block', 'Trusted Group', 'release_group', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('TrueHD Block', 'Trusted Group', 'TrueHD Trusted Groups');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'TrueHD Block', 'radarr', -10000);
INSERT INTO regular_expressions (name, pattern, description) VALUES ('UHD Mid-Size Groups', '^(4KDVS|ATELiER|b0mbardiers|BakedFEL|BlzT|BSTD|BV|c0kE|Chotab|CtrlHD|D-Z0N3|DEFLATE|DEPTH|dkore|DON|EDPH|ESiR|faBR|HiDt|HONE|HQMUX|iFT|j3rico|JustWatch|Kitsune|LESTiN|MainFrame|NCmt|NTb|ORBiT|PTer|RandomBytes|RoJYA|Softboat|SPHD|SURCODE|TAoE|TDD|TnP|TRUNKS|W4NK3R|WATCHABLE|WEBDV)$', 'Disc groups preferred at 25-60 GB: Dumpstarr UHD tiers except hallowed and BHDStudio, plus Dictionarry T3-T5, dkore, and TAoE.');
INSERT INTO custom_formats (name, description) VALUES ('UHD Bluray Mid-Size Tier',
'2160p Blu-ray encode, not a remux, above 25 GB through 60 GB, from Dumpstarr UHD tiers except hallowed and BHDStudio, plus Dictionarry T3-T5 groups, dkore, and TAoE. Nothing extra below 25 GB or above 60 GB.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', '2160p', 'resolution', 'all', 0, 1);
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('UHD Bluray Mid-Size Tier', '2160p', '2160p');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', 'Bluray', 'source', 'all', 0, 1);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('UHD Bluray Mid-Size Tier', 'Bluray', 'bluray');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', 'Not Remux', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('UHD Bluray Mid-Size Tier', 'Not Remux', 'Remux');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', '25-60 GB', 'size', 'all', 0, 1);
INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes) VALUES ('UHD Bluray Mid-Size Tier', '25-60 GB', 26843545600, 64424509440);
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', 'Mid Groups', 'release_group', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('UHD Bluray Mid-Size Tier', 'Mid Groups', 'UHD Mid-Size Groups');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'UHD Bluray Mid-Size Tier', 'radarr', 4200);
UPDATE quality_profiles SET description = description || char(10) || 'Local layer: DTS-HD scores 0, TrueHD scores -10000 for every group, and a 25-60 GB Blu-ray encode from the preferred groups scores 4200.' WHERE name = 'Movies 2160p' AND description NOT LIKE '%Local layer:%';
