# radarr-2160p-database

[![Tests](https://github.com/vazerazer/radarr-2160p-database/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/radarr-2160p-database/actions/workflows/ci.yml)

A Profilarr database with one Radarr profile, **Movies 2160p**. The profile is Dumpstarr's [Movies 2160p](https://github.com/Dumpstarr/Database) from the `stable` branch, plus a small layer. The profile name is unchanged so an existing Radarr profile of that name is updated in place.

Dumpstarr's scores, quality order, minimum of 1000, upgrade-until of 10000, MA Preferred, WEB tiers, and the untagged-audio penalty stay as Dumpstarr ships them. The layer only changes the three things below.

## The layer

**Audio.** DTS-HD MA, DTS-HD HRA, and DTS-X score 0 instead of -10000. Those tracks carry a playable DTS core. TrueHD and Atmos, including Dumpstarr's TrueHD-missing rule, stay at -10000 unless the release group is on the trusted list. That list is Dumpstarr's 4K and HD Blu-ray tiers, Baseline, hallowed, BHDStudio, and HONE, plus Dictionarry's 2160p, 1080p, and 720p Quality, Balanced, and Remux tiers, without the TRaSH low-quality groups (Tigole, WiKi, and the rest of that list). TrueHD from any other group stays blocked unless the name also shows DD, DD+, AC3, or E-AC3, which is the exemption Dumpstarr already had. There is no size cap on HD audio.

**Mid-size Blu-ray.** 2160p Blu-ray encodes that are not remuxes, from 14 GB to 40 GB, from Dictionarry's 2160p Quality tiers 3 through 5 plus dkore and TAoE, score +1800. That is the same score as Dumpstarr's UHD Blu-ray tier 3. Heavy tier-1 groups and WiKi are not in it, and neither are groups Dumpstarr already tiers, so the bonus does not stack. A release outside 14-40 GB simply does not get the bonus. hallowed, BHDStudio, and MA WEB-DLs stay above it.

**Names Radarr parses short.** The layer fills in the group score when the name still has the group but Radarr's parsed group does not:

- dot-joined names such as `.x265.hallowed`, `.PiRaTeS`, and `.DiscoD.HONE`, which otherwise take Group Missing
- repost suffixes such as `.mkv-WtF-xpost`, `.mp4-nEwZ-xpost`, `-CMRG-4u7c`, and `BHDStudio_mp4`
- HONE member names such as `- DarQ HONE)` and `-Weasley-HONE`, which otherwise hit HONE (Bad Name) even though Dumpstarr trusts DarQ, DiscoD, and Weasley

Names Dumpstarr already scores, including `Kitsune[TGx]` and a trailing `HONE-`, are left alone. The fallback does not add a second copy of a score the parsed group already received.

## What was removed

The database ships this profile only. Other Dumpstarr profiles, and formats or regexes Movies 2160p does not use, are not included. Naming presets are not included, so a sync does not rename the library.

`Default Delay` is included (prefer usenet, 60 minutes) because that is the delay profile Dumpstarr pairs with Movies 2160p.

## How updates flow

Profilarr compiles a database in four layers: schema, `ops/`, `tweaks/`, then local user ops. Current Profilarr always loads `tweaks/` during compile. The tweaks tab in the UI is hidden; the loader is not.

`ops/0.movies-2160p.sql` is Dumpstarr's Movies 2160p profile and the formats, regexes, and quality definitions it uses, and nothing else. `tweaks/1.layer.sql` is the layer above. A nightly GitHub Action pulls Dumpstarr `stable` and Dictionarry `v2`, rebuilds both files, and runs the tests. It commits and pushes only when those tests pass. A failed build or a failed test leaves the previous commit in place.

If Dumpstarr renames a format or regex the layer updates, the tweak fails to compile and the job stops. `.github/upstream.json` records the Dumpstarr and Dictionarry commits the files were built from.

To rebuild locally:

```bash
./scripts/sync_upstream.sh
```

The script clones both upstreams, writes `ops/` and `tweaks/`, and runs the tests before it commits. It does not push. Push the result yourself, or let the nightly job do that on `v2` after the tests pass.

## Use it in Profilarr

1. Add a database with repository `https://github.com/vazerazer/radarr-2160p-database` and branch `v2`.
2. On radarr4k, point the quality-profile sync for **Movies 2160p** at this database. Remove radarr4k from the Dumpstarr sync for that profile so the nightly Dumpstarr pull does not write the old scores back.
3. Sync. Profilarr matches a quality profile by name and updates the existing Radarr profile. Movies already on Movies 2160p stay on that profile. Do not delete the profile, do not rename it, and do not add a second Movies 2160p.

The sync changes scores. Radarr will not move the library to another profile, but the next search can upgrade a movie whose new score beats the file on disk. That is the audio rule and the name fixes, not a library-wide re-grab. On a sample of 45 movies the new picks were the SiC DTS-HD MA WEB-DL for The Black Cauldron, the XEBEC DTS-HD MA WEB-DL for Cast Away, the W4NK3R UHD Blu-ray for Jack Reacher, and the 1080p CMRG for Cam. Supergirl stays on a HONE MA WEB-DL at the same score; a previously unparsed copy of that release ties and the larger file wins. Everything else in the sample kept its Dumpstarr pick.

To apply the profile without those upgrades yet, turn upgrades off on Movies 2160p, sync, confirm the Radarr profile id is unchanged, and turn upgrades back on when the new grabs are wanted.

If Default Delay is synced as well, map it onto the existing delay profile of that name. Root folders, download clients, and indexers stay in Radarr.

## Tests

```bash
export PCD_SCHEMA_PATH=deps/schema/ops
python3 tests/test_database.py
```

The schema checkout is [Dictionarry-Hub/schema](https://github.com/Dictionarry-Hub/schema) at the version in `pcd.json`. Install `regex` from `requirements.txt` first. The tests compile the database, check the name fixes, check that Dumpstarr scores stay put except where the layer fires, and rescore the saved release lists.

## License

MIT. See [LICENSE](LICENSE).
