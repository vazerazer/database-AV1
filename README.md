# radarr-2160p-database

[![Tests](https://github.com/vazerazer/radarr-2160p-database/actions/workflows/ci.yml/badge.svg?branch=v2)](https://github.com/vazerazer/radarr-2160p-database/actions/workflows/ci.yml)

A Profilarr database with one Radarr profile, **Movies 2160p**. The profile is Dumpstarr's [Movies 2160p](https://github.com/Dumpstarr/Database) from the `stable` branch, plus a small layer. The profile name is unchanged so an existing Radarr profile of that name is updated in place.

Dumpstarr's scores, quality order, minimum of 1000, upgrade-until of 10000, MA Preferred, WEB tiers, Group Missing, HONE (Bad Name), and the untagged-audio penalty stay as Dumpstarr ships them. The layer only changes the two things below.

## The layer

**Audio.** DTS-HD MA, DTS-HD HRA, and DTS-X score 0 instead of -10000. Those tracks carry a playable DTS core. TrueHD and Atmos, including Dumpstarr's TrueHD-missing rule, stay at -10000 unless the release group is on the trusted list. That list is Dumpstarr's 4K and HD Blu-ray tiers, Baseline, hallowed, BHDStudio, and HONE, plus Dictionarry's 2160p, 1080p, and 720p Quality, Balanced, and Remux tiers, without the TRaSH low-quality groups (Tigole, WiKi, and the rest of that list). TrueHD from any other group stays blocked unless the name also shows DD, DD+, AC3, or E-AC3, which is the exemption Dumpstarr already had. There is no size cap on HD audio.

**Preferred-size Blu-ray.** `UHD Bluray Mid-Size Tier` scores **+4200** for a 2160p Blu-ray encode that is not a remux and is above 25 GB through 60 GB. The groups are Dumpstarr's UHD tiers except hallowed and BHDStudio (so CtrlHD, W4NK3R, DON, MainFrame, SPHD, and the other tiered disc groups), plus the same Dictionarry 2160p quality tiers 3 through 5 as before, including TRUNKS, plus dkore and TAoE. The bonus stacks on Dumpstarr's UHD tier score, so inside the window a tier-1 encode still ranks above SPHD, and SPHD still ranks above TRUNKS. A preferred disc in the window beats hallowed, BHDStudio, and an MA WEB-DL. hallowed and BHDStudio get no size bonus, so one of their own 25-60 GB releases still loses to W4NK3R, SPHD, or TRUNKS in the window. They remain the pick when no preferred disc is available. A release below 25 GB or above 60 GB does not get the bonus, and there is no penalty for being larger. Remux qualities stay disabled. A title that says Remux misses this format and the UHD tiers, so a 75 GB remux loses to a 45 GB encode in the window. A lone encode above 60 GB can still be grabbed when nothing in the window exists.

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

The sync changes scores. Radarr will not move the library to another profile, but the next search can upgrade a movie when a 25-60 GB preferred disc encode outscores the file on disk. On the 45-movie sample, 16 picks differ from Dumpstarr. Fourteen are disc encodes in that window: W4NK3R for The Dark Knight and Jack Reacher, SPHD for Fury and Supergirl, TRUNKS for The Odyssey, Mutiny, and Toy Story 5, MainFrame for The Substance, DON for Thor: Love and Thunder, RandomBytes for Predator: Badlands, Moana, and Disclosure Day, and j3rico for Sisu: Road to Revenge and The Furious. The Black Cauldron and Cast Away still change only because DTS-HD is allowed; their lists have no preferred disc. The other 29 movies keep the Dumpstarr pick.

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
