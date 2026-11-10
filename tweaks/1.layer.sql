-- Local layer for Movies 2160p. Runs after the Dumpstarr base.
-- DTS-HD is allowed (the core track plays). TrueHD stays blocked
-- except for trusted tiered groups. The 14-40 GB window is only
-- the mid-tier bonus, not a penalty and not a cap on HD audio.
-- Group Missing and HONE (Bad Name) are left as Dumpstarr ships them.
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
INSERT INTO regular_expressions (name, pattern, description) VALUES ('UHD Mid-Size Groups', '^(4KDVS|ATELiER|b0mbardiers|BakedFEL|BlzT|BSTD|BV|c0kE|Chotab|D-Z0N3|DEFLATE|DEPTH|dkore|EDPH|ESiR|faBR|iFT|j3rico|JustWatch|Kitsune|LESTiN|NCmt|NTb|ORBiT|RoJYA|Softboat|SURCODE|TAoE|TDD|TnP|TRUNKS|WATCHABLE)$', 'Mid-size 4K Blu-ray encoders.');
INSERT INTO custom_formats (name, description) VALUES ('UHD Bluray Mid-Size Tier',
'2160p Blu-ray encode, not a remux, 14-40 GB, from Dictionarry T3-T5 groups that Dumpstarr does not already tier, plus dkore and TAoE.');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', '2160p', 'resolution', 'all', 0, 1);
INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ('UHD Bluray Mid-Size Tier', '2160p', '2160p');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', 'Bluray', 'source', 'all', 0, 1);
INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ('UHD Bluray Mid-Size Tier', 'Bluray', 'bluray');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', 'Not Remux', 'release_title', 'all', 1, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('UHD Bluray Mid-Size Tier', 'Not Remux', 'Remux');
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', '14-40 GB', 'size', 'all', 0, 1);
INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes) VALUES ('UHD Bluray Mid-Size Tier', '14-40 GB', 15032385536, 42949672960);
INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ('UHD Bluray Mid-Size Tier', 'Mid Groups', 'release_group', 'all', 0, 1);
INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ('UHD Bluray Mid-Size Tier', 'Mid Groups', 'UHD Mid-Size Groups');
INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ('Movies 2160p', 'UHD Bluray Mid-Size Tier', 'radarr', 1800);
UPDATE quality_profiles SET description = description || char(10) || 'Local layer: DTS-HD scores 0, TrueHD stays blocked except for trusted groups, and a 14-40 GB mid-size Blu-ray tier scores 1800.' WHERE name = 'Movies 2160p' AND description NOT LIKE '%Local layer:%';
