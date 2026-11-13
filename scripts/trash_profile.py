#!/usr/bin/env python3
"""Build the TRaSH Remux + WEB 2160p profile from the Guides JSON.

The profile is a separate quality profile. It does not change Movies 2160p.
Custom formats already in the database are reused only when they match the
same Radarr conditions. A TRaSH format whose name is already used by a
different definition is added under a TRaSH-prefixed name.

Selection follows the TRaSH JSON, plus the HDR formats the Remux + WEB 2160p
guide page lists as required:

- every custom format in the quality profile's formatItems
- every custom format checked by default in a cf-group that includes this
  profile (the group is default, and the format is required or default)
- DV Boost, HDR10+ Boost, and DV (w/o HDR fallback), which that guide page
  lists as required even though their cf-groups are not default
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcdlib import (  # noqa: E402
    TRASH_PROFILE_NAME,
    connect,
    execute_dir,
    sql_quote,
)

TRASH_REPO = "https://github.com/TRaSH-Guides/Guides"
TRASH_BRANCH = "master"
PROFILE_ID = "fd161a61e3ab826d3a22d53f935696dd"
PROFILE_JSON = os.path.join("docs", "json", "radarr", "quality-profiles", "remux-web-2160p.json")
# The profile guide lists these with the required HDR formats. Their cf-groups
# are opt-in (no default flag), so formatItems and default groups omit them.
GUIDE_REQUIRED_HDR = {
    "b337d6812e06c200ec9a2d3cfa9d20a7": "DV Boost",
    "caa37d0df9c348912df1fb1d88f9273a": "HDR10+ Boost",
    "923b6abef9b17f937fab56cfcf89e1f1": "DV (w/o HDR fallback)",
}

SOURCE = {
    0: "unknown",
    1: "cam",
    2: "telesync",
    3: "telecine",
    4: "workprint",
    5: "dvd",
    6: "television",
    7: "web_dl",
    8: "webrip",
    9: "bluray",
}
MODIFIER = {
    0: "none",
    1: "regional",
    2: "screener",
    3: "remaster",
    4: "director",
    5: "remux",
    6: "brdisk",
}
RESOLUTION = {480: "480p", 576: "576p", 720: "720p", 1080: "1080p", 2160: "2160p"}

OUTPUT_SQL = os.path.join("tweaks", "2.trash-remux.sql")


def _truthy(value) -> bool:
    return value is True or (isinstance(value, str) and value.lower() == "true")


def _field(fields, key="value"):
    if isinstance(fields, dict):
        if key not in fields:
            raise KeyError(key)
        return fields[key]
    if isinstance(fields, list):
        for item in fields:
            if item.get("name") == key:
                return item.get("value")
    raise TypeError(f"unsupported fields payload: {fields!r}")


def _load_json(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _load_custom_formats(trash_root: str) -> dict:
    directory = os.path.join(trash_root, "docs", "json", "radarr", "cf")
    found = {}
    for name in os.listdir(directory):
        if not name.endswith(".json"):
            continue
        data = _load_json(os.path.join(directory, name))
        found[data["trash_id"]] = data
    return found


def _load_groups(trash_root: str) -> list:
    directory = os.path.join(trash_root, "docs", "json", "radarr", "cf-groups")
    groups = []
    for name in sorted(os.listdir(directory)):
        if name.endswith(".json"):
            groups.append(_load_json(os.path.join(directory, name)))
    return groups


def _score(custom_format: dict) -> int:
    scores = custom_format.get("trash_scores") or {}
    value = scores.get("default", 0)
    if value is None:
        return 0
    return int(value)


def select_formats(trash_root: str) -> tuple[dict, dict, list, list]:
    """Return chosen trash_id -> reason, plus notes about what was left out."""
    profile = _load_json(os.path.join(trash_root, PROFILE_JSON))
    if profile["trash_id"] != PROFILE_ID:
        raise RuntimeError(f"unexpected profile id {profile['trash_id']}")
    chosen = {}
    for name, trash_id in profile["formatItems"].items():
        chosen[trash_id] = f"formatItems ({name})"
    skipped_groups = []
    unchecked = []
    for group in _load_groups(trash_root):
        included = set((group.get("quality_profiles") or {}).get("include", {}).values())
        if PROFILE_ID not in included:
            continue
        if not _truthy(group.get("default")):
            skipped_groups.append(group["name"])
            continue
        for item in group["custom_formats"]:
            if item.get("required") or _truthy(item.get("default")):
                chosen.setdefault(item["trash_id"], f"default group {group['name']}")
            else:
                unchecked.append(f"{item['name']} ({group['name']})")
    for trash_id, name in GUIDE_REQUIRED_HDR.items():
        chosen.setdefault(trash_id, f"guide-required HDR format ({name})")
    return profile, chosen, skipped_groups, unchecked


def _canonical(rows: list[tuple]) -> tuple:
    """Match key for Radarr. One condition in a type ignores required vs optional.

    A lone condition has to match either way. Several conditions keep the
    required/optional split Radarr uses inside a specification group.
    """
    grouped: dict[str, list] = {}
    for typ, negate, required, payload in rows:
        grouped.setdefault(typ, []).append((negate, required, payload))
    parts = []
    for typ in sorted(grouped):
        items = grouped[typ]
        if len(items) == 1:
            negate, _required, payload = items[0]
            parts.append((typ, "single", negate, payload))
            continue
        items.sort(key=lambda item: (item[1], item[0], repr(item[2])))
        for negate, required, payload in items:
            parts.append((typ, "required" if required else "optional", negate, payload))
    return tuple(parts)


def _existing_index(conn):
    """Map a Radarr match key to the custom formats that already implement it."""
    names = [row["name"] for row in conn.execute("SELECT name FROM custom_formats ORDER BY name")]
    index: dict[tuple, list[str]] = {}
    regex_names = set()
    patterns: dict[str, list[str]] = {}
    for row in conn.execute("SELECT name, pattern FROM regular_expressions ORDER BY name"):
        regex_names.add(row["name"])
        patterns.setdefault(row["pattern"], []).append(row["name"])
    cf_names = set(names)
    for name in names:
        rows = []
        conditions = conn.execute(
            """
            SELECT name, type, negate, required, arr_type
            FROM custom_format_conditions
            WHERE custom_format_name = ?
            ORDER BY name
            """,
            (name,),
        ).fetchall()
        for cond in conditions:
            if cond["arr_type"] not in ("all", "radarr"):
                continue
            payload = _existing_payload(conn, name, cond["name"], cond["type"])
            rows.append((cond["type"], int(cond["negate"]), int(cond["required"]), payload))
        index.setdefault(_canonical(rows), []).append(name)
    return index, cf_names, regex_names, patterns


def _existing_payload(conn, custom_format: str, condition: str, typ: str):
    if typ in ("release_title", "release_group", "edition"):
        row = conn.execute(
            """
            SELECT re.pattern
            FROM condition_patterns cp
            JOIN regular_expressions re ON re.name = cp.regular_expression_name
            WHERE cp.custom_format_name = ? AND cp.condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        if row is None:
            raise RuntimeError(f"{custom_format}/{condition} has no pattern")
        return ("pattern", row["pattern"])
    if typ == "source":
        row = conn.execute(
            "SELECT source FROM condition_sources WHERE custom_format_name = ? AND condition_name = ?",
            (custom_format, condition),
        ).fetchone()
        return ("source", row["source"])
    if typ == "resolution":
        row = conn.execute(
            "SELECT resolution FROM condition_resolutions WHERE custom_format_name = ? AND condition_name = ?",
            (custom_format, condition),
        ).fetchone()
        return ("resolution", row["resolution"])
    if typ == "quality_modifier":
        row = conn.execute(
            """
            SELECT quality_modifier FROM condition_quality_modifiers
            WHERE custom_format_name = ? AND condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        return ("modifier", row["quality_modifier"])
    if typ == "language":
        row = conn.execute(
            """
            SELECT language_name, except_language FROM condition_languages
            WHERE custom_format_name = ? AND condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        return ("language", row["language_name"], int(row["except_language"]))
    if typ == "indexer_flag":
        row = conn.execute(
            """
            SELECT flag FROM condition_indexer_flags
            WHERE custom_format_name = ? AND condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        return ("flag", row["flag"])
    if typ == "size":
        row = conn.execute(
            """
            SELECT min_bytes, max_bytes FROM condition_sizes
            WHERE custom_format_name = ? AND condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        return ("size", row["min_bytes"], row["max_bytes"])
    if typ == "release_type":
        row = conn.execute(
            """
            SELECT release_type FROM condition_release_types
            WHERE custom_format_name = ? AND condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        return ("release_type", row["release_type"])
    if typ == "year":
        row = conn.execute(
            """
            SELECT min_year, max_year FROM condition_years
            WHERE custom_format_name = ? AND condition_name = ?
            """,
            (custom_format, condition),
        ).fetchone()
        return ("year", row["min_year"], row["max_year"])
    raise RuntimeError(f"unsupported existing condition type {typ} on {custom_format}")


def _trash_rows(custom_format: dict) -> list[tuple]:
    rows = []
    for spec in custom_format["specifications"]:
        impl = spec["implementation"]
        negate = 1 if spec.get("negate") else 0
        required = 1 if spec.get("required") else 0
        if impl == "ReleaseTitleSpecification":
            typ, payload = "release_title", ("pattern", _field(spec["fields"]))
        elif impl == "ReleaseGroupSpecification":
            typ, payload = "release_group", ("pattern", _field(spec["fields"]))
        elif impl == "SourceSpecification":
            value = int(_field(spec["fields"]))
            if value not in SOURCE:
                raise RuntimeError(f"{custom_format['name']} source {value} is not mapped")
            typ, payload = "source", ("source", SOURCE[value])
        elif impl == "ResolutionSpecification":
            value = int(_field(spec["fields"]))
            if value not in RESOLUTION:
                raise RuntimeError(f"{custom_format['name']} resolution {value} is not mapped")
            typ, payload = "resolution", ("resolution", RESOLUTION[value])
        elif impl == "QualityModifierSpecification":
            value = int(_field(spec["fields"]))
            if value not in MODIFIER:
                raise RuntimeError(f"{custom_format['name']} modifier {value} is not mapped")
            typ, payload = "quality_modifier", ("modifier", MODIFIER[value])
        else:
            raise RuntimeError(
                f"{custom_format['name']} specification {impl} cannot be represented in PCD"
            )
        rows.append((spec["name"], typ, negate, required, payload))
    return rows


def _fit(name: str, used: set[str]) -> str:
    cleaned = " ".join(name.split())
    if not cleaned:
        cleaned = "TRaSH regex"
    if len(cleaned) > 100:
        digest = hashlib.sha1(cleaned.encode()).hexdigest()[:8]
        cleaned = cleaned[:91].rstrip() + "-" + digest
    candidate = cleaned
    number = 2
    while candidate in used or not candidate:
        suffix = f" {number}"
        candidate = cleaned[: 100 - len(suffix)].rstrip() + suffix
        number += 1
    return candidate


def _prefer_existing(trash_name: str, matches: list[str]) -> str:
    for name in matches:
        if name == trash_name:
            return name
    folded = trash_name.casefold()
    for name in matches:
        if name.casefold() == folded:
            return name
    return sorted(matches)[0]


def _compile_patterns(patterns: list[tuple[str, str, str]]) -> None:
    try:
        import regex as re
    except ImportError:
        return
    failures = []
    for custom_format, spec, pattern in patterns:
        try:
            re.compile(pattern, re.I)
        except Exception as exc:  # noqa: BLE001 - report every pattern the scorer would reject
            failures.append(f"{custom_format} / {spec}: {exc}")
    if failures:
        preview = "\n".join(failures[:12])
        raise RuntimeError(f"{len(failures)} TRaSH patterns did not compile:\n{preview}")


def build_trash_sql(conn, trash_root: str, trash_sha: str) -> str:
    profile, chosen, skipped_groups, unchecked = select_formats(trash_root)
    formats = _load_custom_formats(trash_root)
    missing = [trash_id for trash_id in chosen if trash_id not in formats]
    if missing:
        raise RuntimeError(f"missing TRaSH custom formats: {missing}")
    index, cf_names, regex_names, patterns = _existing_index(conn)
    qualities = {row["name"] for row in conn.execute("SELECT name FROM qualities")}
    languages = {row["name"] for row in conn.execute("SELECT name FROM languages")}
    if "Original" not in languages:
        raise RuntimeError("schema has no Original language")
    tag_names = {row["name"] for row in conn.execute("SELECT name FROM tags")}

    reused = []
    added = []
    claimed: dict[str, str] = {}
    new_regexes = []
    new_formats = []
    pattern_checks = []
    scores = []

    for trash_id, reason in sorted(chosen.items(), key=lambda item: formats[item[0]]["name"].lower()):
        data = formats[trash_id]
        trash_name = data["name"]
        score = _score(data)
        spec_rows = _trash_rows(data)
        key = _canonical([(typ, negate, required, payload) for _name, typ, negate, required, payload in spec_rows])
        # A format already claimed by another TRaSH CF cannot take a second score.
        available = [name for name in index.get(key, []) if name not in claimed]
        target = _prefer_existing(trash_name, available) if available else None
        if target is not None:
            claimed[target] = trash_name
            reused.append((trash_name, target, score, reason))
            scores.append((target, score))
            continue
        output = trash_name if trash_name not in cf_names else f"TRaSH {trash_name}"
        output = _fit(output, cf_names)
        cf_names.add(output)
        claimed[output] = trash_name
        conditions = []
        used_conditions: set[str] = set()
        for spec_name, typ, negate, required, payload in spec_rows:
            condition = _fit(spec_name, used_conditions)
            used_conditions.add(condition)
            kind, value = payload[0], payload[1]
            regex_name = None
            if kind == "pattern":
                if "\n" in value or "\x00" in value:
                    raise RuntimeError(f"{trash_name} / {spec_name} pattern contains a newline")
                pattern_checks.append((trash_name, spec_name, value))
                existing_names = patterns.get(value) or []
                if spec_name in existing_names:
                    regex_name = spec_name
                elif existing_names:
                    regex_name = existing_names[0]
                else:
                    regex_name = _fit(spec_name, regex_names)
                    regex_names.add(regex_name)
                    patterns.setdefault(value, []).append(regex_name)
                    new_regexes.append((regex_name, value, f"TRaSH {trash_name} / {spec_name}."))
            conditions.append((condition, typ, negate, required, payload, regex_name))
        rename = 1 if data.get("includeCustomFormatWhenRenaming") else 0
        if output == trash_name:
            description = f"TRaSH custom format {trash_id}."
        else:
            description = (
                f"TRaSH custom format {trash_name} ({trash_id}). "
                f"Stored as {output} because {trash_name} is already a different format."
            )
        new_formats.append((output, description, rename, conditions, trash_name, score, reason))
        added.append((trash_name, output, score, reason))
        scores.append((output, score))

    _compile_patterns(pattern_checks)

    quality_rows, group_rows, missing_qualities = _qualities(profile, qualities)
    lines = [
        f"-- {TRASH_PROFILE_NAME} from {TRASH_REPO} {TRASH_BRANCH} @ {trash_sha}.",
        "-- Generated by scripts/trash_profile.py. Do not edit by hand.",
        "-- Separate from Movies 2160p. Scores are the TRaSH default scores.",
        "-- Movies 2160p audio overrides are not applied.",
        "--",
        "-- Reused custom formats (TRaSH name -> existing name, score):",
    ]
    for trash_name, target, score, reason in reused:
        lines.append(f"--   {trash_name} -> {target} = {score} [{reason}]")
    lines.append("-- Added custom formats (TRaSH name -> stored name, score):")
    for trash_name, output, score, reason in added:
        lines.append(f"--   {trash_name} -> {output} = {score} [{reason}]")
    lines.append("-- Cf-groups that include this profile but are not enabled by default:")
    for name in skipped_groups:
        lines.append(f"--   {name}")
    lines.append("-- Unchecked formats inside default groups (not part of the default profile):")
    for name in unchecked:
        lines.append(f"--   {name}")
    if missing_qualities:
        lines.append(
            "-- Qualities absent from the TRaSH profile and included disabled so every schema quality is listed:"
        )
        for name in missing_qualities:
            lines.append(f"--   {name}")
    lines.append(
        "-- Quality size minimums from TRaSH are not imported. PCD stores one Radarr size row per quality,"
    )
    lines.append("-- shared with Movies 2160p, so those rows are left as they are.")
    lines.append("")

    for name, pattern, description in sorted(new_regexes):
        lines.append(
            "INSERT INTO regular_expressions (name, pattern, regex101_id, description) VALUES ("
            f"{sql_quote(name)}, {sql_quote(pattern)}, NULL, {sql_quote(description)});"
        )
    for output, description, rename, conditions, _trash_name, _points, _reason in sorted(new_formats):
        lines.append(
            "INSERT INTO custom_formats (name, description, include_in_rename) VALUES ("
            f"{sql_quote(output)}, {sql_quote(description)}, {rename});"
        )
        if "TRaSH" in tag_names:
            lines.append(
                "INSERT INTO custom_format_tags (custom_format_name, tag_name) VALUES ("
                f"{sql_quote(output)}, 'TRaSH');"
            )
        for condition, typ, negate, required, payload, regex_name in conditions:
            lines.append(
                "INSERT INTO custom_format_conditions "
                "(custom_format_name, name, type, arr_type, negate, required) VALUES ("
                f"{sql_quote(output)}, {sql_quote(condition)}, {sql_quote(typ)}, 'all', {negate}, {required});"
            )
            kind = payload[0]
            if kind == "pattern":
                lines.append(
                    "INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ("
                    f"{sql_quote(output)}, {sql_quote(condition)}, {sql_quote(regex_name)});"
                )
            elif kind == "source":
                lines.append(
                    "INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ("
                    f"{sql_quote(output)}, {sql_quote(condition)}, {sql_quote(payload[1])});"
                )
            elif kind == "resolution":
                lines.append(
                    "INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ("
                    f"{sql_quote(output)}, {sql_quote(condition)}, {sql_quote(payload[1])});"
                )
            elif kind == "modifier":
                lines.append(
                    "INSERT INTO condition_quality_modifiers (custom_format_name, condition_name, quality_modifier) VALUES ("
                    f"{sql_quote(output)}, {sql_quote(condition)}, {sql_quote(payload[1])});"
                )
            else:
                raise RuntimeError(f"unexpected payload {payload}")

    description = (
        "TRaSH Guides profile Remux + WEB 2160p "
        f"({PROFILE_ID}), {TRASH_REPO} @ {trash_sha}. "
        "Upgrade until Remux-2160p. WEB 2160p (WEBRip-2160p, WEBDL-2160p) is allowed below it. "
        "Other qualities are disabled. Minimum custom format score 0, upgrade until score 10000, "
        "upgrade increment 1. Custom format scores are the TRaSH default scores, including "
        "TrueHD Atmos, DTS-X, and DD+ Atmos. The Movies 2160p audio layer is not applied."
    )
    lines.append(
        "INSERT INTO quality_profiles (name, description, upgrades_allowed, minimum_custom_format_score, "
        "upgrade_until_score, upgrade_score_increment) VALUES ("
        f"{sql_quote(TRASH_PROFILE_NAME)}, {sql_quote(description)}, "
        f"{1 if profile.get('upgradeAllowed', True) else 0}, {int(profile['minFormatScore'])}, "
        f"{int(profile['cutoffFormatScore'])}, {int(profile['minUpgradeFormatScore'])});"
    )
    lines.append(
        "INSERT INTO quality_profile_languages (quality_profile_name, language_name, type) VALUES ("
        f"{sql_quote(TRASH_PROFILE_NAME)}, 'Original', 'must');"
    )
    for tag in ("2160p", "Radarr", "TRaSH"):
        if tag in tag_names:
            lines.append(
                "INSERT INTO quality_profile_tags (quality_profile_name, tag_name) VALUES ("
                f"{sql_quote(TRASH_PROFILE_NAME)}, {sql_quote(tag)});"
            )
    for group_name, members in group_rows:
        lines.append(
            "INSERT INTO quality_groups (quality_profile_name, name) VALUES ("
            f"{sql_quote(TRASH_PROFILE_NAME)}, {sql_quote(group_name)});"
        )
        for position, quality in enumerate(members):
            lines.append(
                "INSERT INTO quality_group_members "
                "(quality_profile_name, quality_group_name, quality_name, position) VALUES ("
                f"{sql_quote(TRASH_PROFILE_NAME)}, {sql_quote(group_name)}, {sql_quote(quality)}, {position});"
            )
    for position, quality_name, group_name, enabled, upgrade_until in quality_rows:
        lines.append(
            "INSERT INTO quality_profile_qualities "
            "(quality_profile_name, quality_name, quality_group_name, position, enabled, upgrade_until) VALUES ("
            f"{sql_quote(TRASH_PROFILE_NAME)}, {sql_quote(quality_name)}, {sql_quote(group_name)}, "
            f"{position}, {enabled}, {upgrade_until});"
        )
    for name, score in sorted(scores):
        lines.append(
            "INSERT INTO quality_profile_custom_formats "
            "(quality_profile_name, custom_format_name, arr_type, score) VALUES ("
            f"{sql_quote(TRASH_PROFILE_NAME)}, {sql_quote(name)}, 'radarr', {score});"
        )
    sql = "\n".join(lines) + "\n"
    _validate(conn, sql, set(qualities), len(scores))
    return sql


def _qualities(profile: dict, known: set[str]):
    cutoff = profile["cutoff"]
    rows = []
    groups = []
    covered = set()
    position = 0
    for item in profile["items"]:
        enabled = 1 if item.get("allowed") else 0
        if item.get("items"):
            group_name = item["name"]
            members = list(item["items"])
            unknown = [name for name in members if name not in known]
            if unknown:
                raise RuntimeError(f"TRaSH group {group_name} lists unknown qualities {unknown}")
            if covered.intersection(members):
                raise RuntimeError(f"duplicate qualities in {group_name}")
            covered.update(members)
            groups.append((group_name, members))
            upgrade = 1 if group_name == cutoff else 0
            rows.append((position, None, group_name, enabled, upgrade))
        else:
            quality = item["name"]
            if quality not in known:
                raise RuntimeError(f"TRaSH quality is not in the schema: {quality}")
            if quality in covered:
                raise RuntimeError(f"duplicate quality {quality}")
            covered.add(quality)
            upgrade = 1 if quality == cutoff else 0
            rows.append((position, quality, None, enabled, upgrade))
        position += 1
    missing = sorted(known - covered)
    for quality in missing:
        rows.append((position, quality, None, 0, 0))
        position += 1
    if sum(row[4] for row in rows) != 1:
        raise RuntimeError(f"expected one upgrade-until quality, cutoff={cutoff}")
    return rows, groups, missing


def _validate(conn, sql: str, qualities: set[str], score_count: int) -> None:
    conn.executescript(sql)
    problems = conn.execute("PRAGMA foreign_key_check").fetchall()
    if problems:
        raise RuntimeError(f"foreign key check failed: {problems[:5]}")
    row = conn.execute(
        "SELECT minimum_custom_format_score, upgrade_until_score FROM quality_profiles WHERE name = ?",
        (TRASH_PROFILE_NAME,),
    ).fetchone()
    if row["minimum_custom_format_score"] != 0 or row["upgrade_until_score"] != 10000:
        raise RuntimeError(f"unexpected profile scores {tuple(row)}")
    count = conn.execute(
        "SELECT COUNT(*) AS n FROM quality_profile_custom_formats WHERE quality_profile_name = ?",
        (TRASH_PROFILE_NAME,),
    ).fetchone()["n"]
    if count != score_count:
        raise RuntimeError(f"score rows {count} != {score_count}")
    listed = set()
    for item in conn.execute(
        """
        SELECT quality_name FROM quality_profile_qualities
        WHERE quality_profile_name = ? AND quality_name IS NOT NULL
        """,
        (TRASH_PROFILE_NAME,),
    ):
        listed.add(item["quality_name"])
    for item in conn.execute(
        "SELECT quality_name FROM quality_group_members WHERE quality_profile_name = ?",
        (TRASH_PROFILE_NAME,),
    ):
        listed.add(item["quality_name"])
    if listed != qualities:
        raise RuntimeError(f"quality coverage mismatch: {sorted(qualities - listed)} {sorted(listed - qualities)}")
    movies = conn.execute(
        """
        SELECT score FROM quality_profile_custom_formats
        WHERE quality_profile_name = 'Movies 2160p' AND custom_format_name = 'TrueHD'
        """
    ).fetchone()
    if movies is None or movies["score"] != -10000:
        raise RuntimeError("Movies 2160p TrueHD score changed while building the TRaSH profile")


def compile_base(schema_dir: str, repo: str):
    """Schema, Dumpstarr ops, and the Movies 2160p layer. Not the TRaSH file."""
    conn = connect()
    execute_dir(conn, schema_dir)
    execute_dir(conn, os.path.join(repo, "ops"))
    layer = os.path.join(repo, "tweaks", "1.layer.sql")
    with open(layer, encoding="utf-8") as handle:
        conn.executescript(handle.read())
    return conn


def write_profile(repo: str, schema_dir: str, trash_root: str, trash_sha: str) -> str:
    conn = compile_base(schema_dir, repo)
    try:
        sql = build_trash_sql(conn, trash_root, trash_sha)
    finally:
        conn.close()
    path = os.path.join(repo, OUTPUT_SQL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(sql)
    _update_upstream(repo, trash_sha)
    return path


def _update_upstream(repo: str, trash_sha: str) -> None:
    path = os.path.join(repo, ".github", "upstream.json")
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    data["trash"] = {
        "repository": TRASH_REPO,
        "branch": TRASH_BRANCH,
        "sha": trash_sha,
        "profile": TRASH_PROFILE_NAME,
        "trash_id": PROFILE_ID,
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--schema", required=True, help="Dictionarry schema ops directory")
    parser.add_argument("--trash", required=True, help="TRaSH-Guides/Guides checkout")
    args = parser.parse_args()
    import subprocess

    sha = subprocess.check_output(["git", "-C", args.trash, "rev-parse", "HEAD"], text=True).strip()
    path = write_profile(args.repo, args.schema, args.trash, sha)
    print(f"wrote {path}")
    print(f"trash {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
