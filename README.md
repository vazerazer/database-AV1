# radarr-2160p-database

[![Tests](https://github.com/vazerazer/radarr-2160p-database/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/radarr-2160p-database/actions/workflows/ci.yml)

A Profilarr database with two Radarr profiles. **Movies 2160p** is Dumpstarr's [Movies 2160p](https://github.com/Dumpstarr/Database) from the `stable` branch, plus a small layer. That profile name is unchanged so an existing Radarr profile of that name is updated in place. **TRaSH Remux + WEB 2160p** is a second profile, the TRaSH Guides [Remux + WEB 2160p](https://trash-guides.info/Radarr/radarr-setup-quality-profiles/#remux-web-2160p) profile, and it does not change Movies 2160p.

Dumpstarr's scores, quality order, minimum of 1000, upgrade-until of 10000, MA Preferred, WEB tiers, Group Missing, HONE (Bad Name), and the untagged-audio penalty stay as Dumpstarr ships them. The layer only changes the two things below.

## The layer

**Audio.** DTS-HD MA, DTS-HD HRA, DTS-X, and plain DTS score the same as Dolby Digital +. Those tracks carry a playable DTS core. Dumpstarr scores the HD formats at -10000 and does not score plain DTS on this profile, so the layer sets all four to the DD+ score. TrueHD and TrueHD Atmos score -10000 for every release group. The shared TrueHD format still matches only when the group is not on the trusted list, so Movies 2160p adds `TrueHD Block`, also scored -10000, for groups that are on that list. The block is scored on this profile only, and the shared TrueHD format is not rewritten, so another profile that uses it keeps its own match rules. Dumpstarr's TrueHD-missing rule still skips trusted groups. The trusted list is Dumpstarr's 4K and HD Blu-ray tiers, Baseline, hallowed, BHDStudio, and HONE, plus Dictionarry's 2160p, 1080p, and 720p Quality, Balanced, and Remux tiers, without the TRaSH low-quality groups (Tigole, WiKi, and the rest of that list). A title that also shows DD, DD+, AC3, or E-AC3 misses both TrueHD formats, which is the exemption Dumpstarr already had. There is no size cap on HD audio.

**Preferred-size Blu-ray.** `UHD Bluray Mid-Size Tier` scores **+4200** for a 2160p Blu-ray encode that is not a remux and is above 20 GB through 60 GB. The groups are Dumpstarr's UHD tiers except hallowed and BHDStudio (so CtrlHD, W4NK3R, DON, MainFrame, SPHD, and the other tiered disc groups), plus the same Dictionarry 2160p quality tiers 3 through 5 as before, including TRUNKS, plus dkore, TAoE, and ZAX. ZAX is not on the trusted list, so TrueHD from ZAX still scores -10000. The bonus stacks on Dumpstarr's UHD tier score, so inside the window a tier-1 encode still ranks above SPHD, and SPHD still ranks above TRUNKS. A preferred disc in the window beats hallowed, BHDStudio, and an MA WEB-DL. hallowed and BHDStudio get no size bonus, so one of their own 20-60 GB releases still loses to W4NK3R, SPHD, or TRUNKS in the window. They remain the pick when no preferred disc is available. A release at or below 20 GB, or above 60 GB, does not get the bonus, and there is no penalty for being larger. Remux qualities stay disabled. A title that says Remux misses this format and the UHD tiers, so a 75 GB remux loses to a 45 GB encode in the window. A lone encode above 60 GB can still be grabbed when nothing in the window exists.

## TRaSH Remux + WEB 2160p

This profile is generated from the TRaSH Guides JSON (`remux-web-2160p`, plus the custom formats that profile turns on by default). It is not the Movies 2160p layer.

Upgrade until is Remux-2160p. WEB 2160p (WEBRip-2160p and WEBDL-2160p) is allowed under that. Every other quality is disabled. The minimum custom format score is 0 and the upgrade-until score is 10000. Custom format scores are the TRaSH default scores: TrueHD Atmos 5000, DTS X 4500, DD+ Atmos 3000, DD+ 1750, DTS-HD MA 2500, Remux Tier 01 1950, and BR-DISK and LQ at -10000. TrueHD is not blocked, and DTS-HD MA is not tied to DD+.

Formats already in the database are reused when the Radarr conditions match. TRaSH formats whose names are already used by a different definition are stored under a `TRaSH` prefix (`TRaSH WEB Tier 01`, `TRaSH LQ`, `TRaSH TrueHD`, and so on). DV Boost, HDR10+ Boost, and DV (w/o HDR fallback) are included because the TRaSH profile page lists them as required; their cf-groups are otherwise left unchecked in the sync UI. Optional groups that TRaSH does not enable by default (movie versions, SDR, scene, and the rest of that list) are not imported. MP3, Opus, and x265 (HD) are in default groups but are not the checked formats. HDTV-480p is not in the TRaSH quality list; it is included disabled because the schema lists it. TRaSH quality size minimums are not imported, because PCD keeps one shared Radarr size row per quality and those rows already belong to Movies 2160p.

## What was removed

Movies 2160p is the only Dumpstarr profile. Other Dumpstarr profiles, and formats or regexes neither profile uses, are not included. Naming presets are not included, so a sync does not rename the library.

`Default Delay` is included (prefer usenet, 60 minutes) because that is the delay profile Dumpstarr pairs with Movies 2160p.

## How updates flow

Profilarr compiles a database in four layers: schema, `ops/`, `tweaks/`, then local user ops. Current Profilarr always loads `tweaks/` during compile. The tweaks tab in the UI is hidden; the loader is not.

`ops/0.movies-2160p.sql` is Dumpstarr's Movies 2160p profile and the formats, regexes, and quality definitions it uses, and nothing else. `tweaks/1.layer.sql` is the layer above. `tweaks/2.trash-remux.sql` is the TRaSH profile. A nightly GitHub Action pulls Dumpstarr `stable`, Dictionarry `v2`, and TRaSH Guides, rebuilds those files, and runs the tests. It commits and pushes only when those tests pass. A failed build or a failed test leaves the previous commit in place.

If Dumpstarr renames a format or regex the layer updates, the tweak fails to compile and the job stops. `.github/upstream.json` records the Dumpstarr, Dictionarry, and TRaSH commits the files were built from.

To rebuild locally:

```bash
./scripts/sync_upstream.sh
```

The script clones Dumpstarr, Dictionarry, and TRaSH Guides, writes `ops/` and `tweaks/`, and runs the tests before it commits. It does not push. Push the result yourself, or let the nightly job do that on `v2` after the tests pass.

## Use it in Profilarr

1. Add a database with repository `https://github.com/vazerazer/radarr-2160p-database` and branch `v2`.
2. On radarr4k, point the quality-profile sync for **Movies 2160p** at this database. Remove radarr4k from the Dumpstarr sync for that profile so the nightly Dumpstarr pull does not write the old scores back. Point a separate sync at **TRaSH Remux + WEB 2160p** when that profile is wanted. Do not map it onto Movies 2160p.
3. Sync. Profilarr matches a quality profile by name and updates the existing Radarr profile. Movies already on Movies 2160p stay on that profile. Do not delete the profile, do not rename it, and do not add a second Movies 2160p. TRaSH Remux + WEB 2160p is a different profile and does not replace it.

The sync changes scores. Radarr will not move the library to another profile, but the next search can upgrade a movie when a 20-60 GB preferred disc encode outscores the file on disk. A TrueHD disc, including one from SPHD, DON, j3rico, or ZAX, stays under the minimum and does not replace the current file. On the 45-movie sample, 11 picks differ from Dumpstarr, and none of them are TrueHD. Four are DTS-HD MA encodes: W4NK3R for The Dark Knight (36.6 GB) and Jack Reacher, MainFrame for The Substance, and TRUNKS for The Odyssey. Fury picks a 22.5 GB HONE DD+ encode that sat under the old 25 GB floor. Plain DTS now ties DD+, so a DON or CtrlHD DTS encode wins Prisoners, Blue Valentine, and Melancholia, and TayTO wins A Royal Affair. The Black Cauldron and Cast Away still change only because DTS-HD is allowed; their lists have no preferred disc. The other 34 movies keep the Dumpstarr pick. Robin Hood's ~30 GB ZAX DD+ encode receives the mid-size bonus and was already the pick.

To apply the profile without those upgrades yet, turn upgrades off on Movies 2160p, sync, confirm the Radarr profile id is unchanged, and turn upgrades back on when the new grabs are wanted.

If Default Delay is synced as well, map it onto the existing delay profile of that name. Root folders, download clients, and indexers stay in Radarr.

## Tests

```bash
export PCD_SCHEMA_PATH=deps/schema/ops
python3 tests/test_database.py
```

The schema checkout is [Dictionarry-Hub/schema](https://github.com/Dictionarry-Hub/schema) at the version in `pcd.json`. Install `regex` from `requirements.txt` first. The tests compile the database, check that Dumpstarr scores stay put except where the layer fires, and rescore the saved release lists.

## License

MIT. See [LICENSE](LICENSE).
