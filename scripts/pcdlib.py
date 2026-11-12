"""Compile, prune, and layer a Profilarr PCD.

Profilarr replays schema, then ops/, then tweaks/, then local user ops.
This repo keeps Dumpstarr's Movies 2160p profile as one base operation and
puts the local layer in tweaks/, which current Profilarr always compiles
(the tweaks tab is hidden, the loader is not).
"""

from __future__ import annotations

import os
import re
import sqlite3
from typing import Iterable

PROFILE_NAME = "Movies 2160p"
DATABASE_NAME = "radarr-2160p-database"

DUMPSTARR_REPO = "https://github.com/Dumpstarr/Database"
DUMPSTARR_BRANCH = "stable"
DICTIONARRY_REPO = "https://github.com/Dictionarry-Hub/database"
DICTIONARRY_BRANCH = "v2"

# Dictionarry 2160p Quality tiers that are encodes, not the heavy transparent
# tier. Dumpstarr's own UHD tiers are included too, except the compact
# hallowed and BHDStudio groups, which stay the fallback outside this window.
MID_TIER_FORMATS = (
    "2160p Quality Tier 3",
    "2160p Quality Tier 4",
    "2160p Quality Tier 5",
)
MID_TIER_EXTRA = ("dkore", "TAoE", "ZAX")
MID_TIER_EXCLUDE = {"hallowed", "bhdstudio", "wiki", "reborn", "sa89", "solar"}
# Radarr treats the minimum as exclusive and the maximum as inclusive.
MID_MIN_GB = 20
MID_MAX_GB = 60
MID_MIN_BYTES = MID_MIN_GB * 1024 * 1024 * 1024
MID_MAX_BYTES = MID_MAX_GB * 1024 * 1024 * 1024
MID_SIZE_LABEL = f"{MID_MIN_GB}-{MID_MAX_GB} GB"
MID_TIER_SCORE = 4200
MID_TIER_NAME = "UHD Bluray Mid-Size Tier"
# These are the DTS formats Movies 2160p already scores. Plain DTS is copied
# from Dumpstarr when this profile does not score it. Each is set to the
# current Dolby Digital + score. TrueHD is left at -10000.
DTS_SCORE_FORMATS = ("DTS-HD MA", "DTS-HD HRA", "DTS-X")
PLAIN_DTS = "DTS"
DDPLUS = "Dolby Digital +"
TRUEHD_BLOCK = "TrueHD Block"
TRUEHD_BLOCK_SCORE = -10000
TRUSTED_REGEX = "TrueHD Trusted Groups"
MID_REGEX = "UHD Mid-Size Groups"


def sql_quote(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def op_order(filename: str) -> int:
    match = re.match(r"^(\d+)\.", filename)
    return int(match.group(1)) if match else 10**9


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    def lookup(table: str, name: str):
        row = conn.execute(f"SELECT id FROM {table} WHERE name = ?", (name,)).fetchone()
        if row is None:
            raise sqlite3.OperationalError(f"{table} not found: {name}")
        return row[0]

    conn.create_function("qp", 1, lambda name: lookup("quality_profiles", name))
    conn.create_function("cf", 1, lambda name: lookup("custom_formats", name))
    conn.create_function("dp", 1, lambda name: lookup("delay_profiles", name))
    conn.create_function("tag", 1, lambda name: lookup("tags", name))
    return conn


def sql_files(directory: str) -> list[str]:
    if not directory or not os.path.isdir(directory):
        return []
    names = [name for name in os.listdir(directory) if name.endswith(".sql")]
    return sorted(names, key=lambda name: (op_order(name), name))


def execute_dir(conn: sqlite3.Connection, directory: str) -> None:
    for name in sql_files(directory):
        path = os.path.join(directory, name)
        with open(path, encoding="utf-8") as handle:
            try:
                conn.executescript(handle.read())
            except sqlite3.Error as exc:
                raise sqlite3.Error(f"{path}: {exc}") from exc


def compile_layers(schema_dir: str, *layer_dirs: str) -> sqlite3.Connection:
    conn = connect()
    execute_dir(conn, schema_dir)
    for layer in layer_dirs:
        execute_dir(conn, layer)
    return conn


def _split_alts(pattern: str) -> list[str] | None:
    """Return top-level alternatives inside ^(...)$ , or None."""
    if not (pattern.startswith("^(") and pattern.endswith(")$")):
        return None
    inner = pattern[2:-2]
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    escaped = False
    for char in inner:
        if escaped:
            buf.append(char)
            escaped = False
            continue
        if char == "\\":
            buf.append(char)
            escaped = True
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char == "|" and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(char)
    parts.append("".join(buf))
    return [part for part in parts if part]


_DICT_PREFIX = "(?<=^|[\\s.-])"


def pattern_tokens(pattern: str, name: str) -> list[str]:
    """Pieces that can sit inside ^(?:a|b)$.

    Dumpstarr stores ^(?:Group|Group)$. Dictionarry stores a single group
    as (?<=^|[\\s.-])Group\\b, and a few of those groups are themselves
    small regexes (de[42], CM(a)?R(io)?G).
    """
    alts = _split_alts(pattern)
    if alts:
        return alts
    if pattern.startswith(_DICT_PREFIX) and pattern.endswith("\\b"):
        return [pattern[len(_DICT_PREFIX) : -2]]
    raise ValueError(f"{name} is not a group pattern: {pattern[:80]}")


def group_tokens(conn: sqlite3.Connection, regex_names: Iterable[str]) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    for name in regex_names:
        row = conn.execute(
            "SELECT pattern FROM regular_expressions WHERE name = ?", (name,)
        ).fetchone()
        if row is None:
            raise KeyError(f"regular expression not found: {name}")
        for alt in pattern_tokens(row["pattern"], name):
            key = alt.lower()
            if key not in seen:
                seen.add(key)
                tokens.append(alt)
    return tokens


def regex_names_for(conn: sqlite3.Connection, custom_format: str, arr_types: tuple[str, ...]) -> list[str]:
    rows = conn.execute(
        """
        SELECT re.name
        FROM custom_format_conditions c
        JOIN condition_patterns cp
          ON cp.custom_format_name = c.custom_format_name
         AND cp.condition_name = c.name
        JOIN regular_expressions re ON re.name = cp.regular_expression_name
        WHERE c.custom_format_name = ?
          AND c.type = 'release_group'
          AND c.arr_type IN ({})
        ORDER BY re.name
        """.format(",".join("?" * len(arr_types))),
        (custom_format, *arr_types),
    ).fetchall()
    return [row["name"] for row in rows]


def dictionarry_group_regexes(conn: sqlite3.Connection, custom_format: str) -> list[str]:
    return regex_names_for(conn, custom_format, ("all", "radarr"))


def _lq_keys(conn: sqlite3.Connection) -> set[str]:
    names = regex_names_for(conn, "LQ", ("radarr",))
    return {token.lower() for token in group_tokens(conn, names)}


def trusted_group_tokens(dumpstarr: sqlite3.Connection, dictionarry: sqlite3.Connection) -> list[str]:
    """Blu-ray tiers, baseline, and Dictionarry quality, balanced, and remux tiers, minus TRaSH LQ."""
    dumpstarr_formats = (
        "UHD Bluray Tier 01",
        "UHD Bluray Tier 02",
        "UHD Bluray Tier 03",
        "HD Bluray Tier 01",
        "HD Bluray Tier 02",
        "HD Bluray Tier 03",
        "Baseline Groups",
        "hallowed",
        "BHDStudio",
    )
    dictionarry_formats = (
        "2160p Quality Tier 1",
        "2160p Quality Tier 2",
        "2160p Quality Tier 3",
        "2160p Quality Tier 4",
        "2160p Quality Tier 5",
        "2160p Quality Tier 6",
        "2160p Balanced Tier 1",
        "2160p Balanced Tier 2",
        "2160p Balanced Tier 3",
        "HONE Blurays",
        "1080p Quality Tier 1",
        "1080p Quality Tier 2",
        "1080p Quality Tier 3",
        "1080p Quality Tier 4",
        "1080p Quality Tier 5",
        "1080p Quality Tier 6",
        "1080p Balanced Tier 1",
        "1080p Balanced Tier 2",
        "720p Quality Tier 1",
        "720p Quality Tier 2",
        "720p Quality Tier 3",
        "720p Quality Tier 4",
        "720p Quality Tier 5",
        "720p Quality Tier 6",
        "720p Balanced Tier 1",
        "Remux Tier 1",
        "Remux Tier 2",
        "Remux Tier 3",
        "Remux Tier 4",
    )
    raw: list[str] = []
    for custom_format in dumpstarr_formats:
        raw.extend(
            group_tokens(
                dumpstarr,
                regex_names_for(dumpstarr, custom_format, ("all", "radarr", "sonarr")),
            )
        )
    for custom_format in dictionarry_formats:
        raw.extend(group_tokens(dictionarry, dictionarry_group_regexes(dictionarry, custom_format)))
    blocked = _lq_keys(dumpstarr)
    tokens: list[str] = []
    seen: set[str] = set()
    for token in raw:
        key = token.lower()
        if key in blocked or key in seen:
            continue
        seen.add(key)
        tokens.append(token)
    tokens.sort(key=lambda item: (item.lower(), item))
    return tokens


def mid_tier_tokens(dumpstarr: sqlite3.Connection, dictionarry: sqlite3.Connection) -> list[str]:
    """Groups that earn the 20-60 GB bonus.

    Dumpstarr UHD tiers are included so a large W4NK3R, CtrlHD, or SPHD
    encode outranks a compact hallowed release. hallowed and BHDStudio
    themselves are left out: they stay the acceptable compact fallback.
    Dictionarry tiers 3-5 fill in groups Dumpstarr does not tier, such as
    TRUNKS. The bonus stacks on top of an existing UHD tier score.
    """
    tokens: list[str] = []
    seen: set[str] = set()

    def add(token: str) -> None:
        key = token.lower()
        if key in MID_TIER_EXCLUDE or key in seen:
            return
        seen.add(key)
        tokens.append(token)

    for custom_format in ("UHD Bluray Tier 01", "UHD Bluray Tier 02", "UHD Bluray Tier 03"):
        for token in group_tokens(
            dumpstarr, regex_names_for(dumpstarr, custom_format, ("all", "radarr"))
        ):
            add(token)
    for custom_format in MID_TIER_FORMATS:
        for token in group_tokens(dictionarry, dictionarry_group_regexes(dictionarry, custom_format)):
            add(token)
    for extra in MID_TIER_EXTRA:
        add(extra)
    tokens.sort(key=lambda item: (item.lower(), item))
    return tokens


def profile_score(conn: sqlite3.Connection, name: str) -> int | None:
    row = conn.execute(
        """
        SELECT score FROM quality_profile_custom_formats
        WHERE quality_profile_name = ? AND custom_format_name = ? AND arr_type = 'radarr'
        """,
        (PROFILE_NAME, name),
    ).fetchone()
    return None if row is None else row["score"]


def build_layer_sql(dumpstarr: sqlite3.Connection, dictionarry: sqlite3.Connection) -> str:
    trusted = trusted_group_tokens(dumpstarr, dictionarry)
    mid = mid_tier_tokens(dumpstarr, dictionarry)
    dd_plus = profile_score(dumpstarr, DDPLUS)
    if dd_plus is None:
        raise RuntimeError(f"{DDPLUS} is not scored on {PROFILE_NAME}")
    lines = [
        "-- Local layer for Movies 2160p. Runs after the Dumpstarr base.",
        "-- DTS-HD MA, DTS-HD HRA, DTS-X, and plain DTS score the same as DD+.",
        "-- TrueHD, including TrueHD Atmos, scores -10000 for every release",
        "-- group. The shared TrueHD format still skips trusted groups; TrueHD",
        f"-- Block covers those groups on this profile only. The {MID_SIZE_LABEL}",
        "-- window is only a bonus for preferred disc groups, not a penalty",
        "-- and not a cap on HD audio. Remuxes and releases outside the window",
        "-- get nothing extra. Group Missing and HONE (Bad Name) are left as",
        "-- Dumpstarr ships them.",
    ]
    for name in DTS_SCORE_FORMATS:
        lines.extend(_set_audio_score(name, dd_plus))
    lines.extend(_plain_dts(dumpstarr, dd_plus))
    lines.extend([
        _insert_regex(
            TRUSTED_REGEX,
            "^(" + "|".join(trusted) + ")$",
            "Blu-ray, baseline, and Dictionarry quality/balanced/remux groups, minus TRaSH LQ.",
        ),
        "INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)",
        "VALUES ('TrueHD', 'Not Trusted Group', 'release_group', 'all', 1, 1);",
        "INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)",
        f"VALUES ('TrueHD', 'Not Trusted Group', {sql_quote(TRUSTED_REGEX)});",
        "INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required)",
        "VALUES ('TrueHD Missing', 'Not Trusted Group', 'release_group', 'all', 1, 1);",
        "INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name)",
        f"VALUES ('TrueHD Missing', 'Not Trusted Group', {sql_quote(TRUSTED_REGEX)});",
    ])
    lines.extend(_format_truehd_block())
    lines.append(
        _insert_regex(
            MID_REGEX,
            "^(" + "|".join(mid) + ")$",
            f"Disc groups preferred at {MID_SIZE_LABEL}: Dumpstarr UHD tiers except hallowed and BHDStudio, plus Dictionarry T3-T5, dkore, TAoE, and ZAX.",
        )
    )
    lines.extend(_format_mid())
    lines.append(
        "UPDATE quality_profiles SET description = description || char(10) || "
        + sql_quote(
            "Local layer: DTS-HD MA, DTS-HD HRA, DTS-X, and DTS score the same as DD+, "
            "TrueHD scores -10000 for every group, "
            f"and a {MID_SIZE_LABEL} Blu-ray encode from the preferred groups scores 4200."
        )
        + " WHERE name = 'Movies 2160p' AND description NOT LIKE '%Local layer:%';"
    )
    return "\n".join(lines) + "\n"


def _set_audio_score(name: str, score: int) -> list[str]:
    """Replace Dumpstarr's -10000 audio penalty with the DD+ score."""
    return [
        "UPDATE quality_profile_custom_formats",
        f"SET score = {score}",
        "WHERE quality_profile_name = 'Movies 2160p'",
        f"  AND custom_format_name = {sql_quote(name)}",
        "  AND arr_type = 'radarr'",
        "  AND score = -10000;",
    ]


def _plain_dts(dumpstarr: sqlite3.Connection, dd_plus: int) -> list[str]:
    """Score plain DTS the same as DD+ when this profile scores it lower, or not at all.

    Movies 2160p does not include Dumpstarr's DTS format, so a plain DTS release
    currently gets no audio score. The format is copied, with its negations, so
    a DTS-HD or DTS-X title does not take this score as well.
    """
    current = profile_score(dumpstarr, PLAIN_DTS)
    if current is None:
        return _copy_release_title_format(dumpstarr, PLAIN_DTS) + [_score(PLAIN_DTS, dd_plus)]
    if current < dd_plus:
        return [
            "UPDATE quality_profile_custom_formats",
            f"SET score = {dd_plus}",
            "WHERE quality_profile_name = 'Movies 2160p'",
            f"  AND custom_format_name = {sql_quote(PLAIN_DTS)}",
            "  AND arr_type = 'radarr'",
            f"  AND score = {current};",
        ]
    return []


def _copy_release_title_format(conn: sqlite3.Connection, name: str) -> list[str]:
    row = conn.execute(
        "SELECT description FROM custom_formats WHERE name = ?",
        (name,),
    ).fetchone()
    if row is None:
        raise RuntimeError(f"custom format not found: {name}")
    lines = [
        f"INSERT INTO custom_formats (name, description) VALUES ({sql_quote(name)},",
        sql_quote(row["description"] or "") + ");",
    ]
    conditions = conn.execute(
        """
        SELECT name, type, arr_type, negate, required
        FROM custom_format_conditions
        WHERE custom_format_name = ?
        ORDER BY name
        """,
        (name,),
    ).fetchall()
    if not conditions:
        raise RuntimeError(f"custom format has no conditions: {name}")
    for cond in conditions:
        if cond["type"] != "release_title" or cond["arr_type"] != "all":
            raise RuntimeError(
                f"{name} condition {cond['name']} is {cond['type']}/{cond['arr_type']}"
            )
        lines.append(_cond(name, cond["name"], cond["type"], cond["negate"], cond["required"]))
        patterns = conn.execute(
            """
            SELECT regular_expression_name FROM condition_patterns
            WHERE custom_format_name = ? AND condition_name = ?
            ORDER BY regular_expression_name
            """,
            (name, cond["name"]),
        ).fetchall()
        if len(patterns) != 1:
            raise RuntimeError(f"{name} condition {cond['name']} has {len(patterns)} patterns")
        lines.append(_pat(name, cond["name"], patterns[0]["regular_expression_name"]))
    return lines


def _insert_regex(name: str, pattern: str, description: str) -> str:
    return (
        "INSERT INTO regular_expressions (name, pattern, description) VALUES ("
        f"{sql_quote(name)}, {sql_quote(pattern)}, {sql_quote(description)});"
    )


def _format_truehd_block() -> list[str]:
    """Block trusted-group TrueHD without rewriting the shared TrueHD format.

    The shared format keeps its negated trusted-group condition, so any other
    profile that uses it is unchanged. This format matches the same audio
    rules (TrueHD present, and no DD, DD+, DTS, or FLAC) only when the group
    is trusted, and it is scored on Movies 2160p alone. Untrusted TrueHD stays
    on the original -10000 and does not take a second penalty.
    """
    return [
        f"INSERT INTO custom_formats (name, description) VALUES ({sql_quote(TRUEHD_BLOCK)},",
        sql_quote(
            "TrueHD, including TrueHD Atmos, from a trusted release group. "
            "Movies 2160p scores this at -10000. The shared TrueHD format still "
            "skips those groups. A title that also shows DD, DD+, DTS, or FLAC does not match."
        )
        + ");",
        _cond(TRUEHD_BLOCK, "Not DTS", "release_title", 1, 1),
        _pat(TRUEHD_BLOCK, "Not DTS", "DTS"),
        _cond(TRUEHD_BLOCK, "Not Dolby Digital", "release_title", 1, 1),
        _pat(TRUEHD_BLOCK, "Not Dolby Digital", "Dolby Digital"),
        _cond(TRUEHD_BLOCK, "Not Dolby Digital +", "release_title", 1, 1),
        _pat(TRUEHD_BLOCK, "Not Dolby Digital +", "Dolby Digital +"),
        _cond(TRUEHD_BLOCK, "Not FLAC", "release_title", 1, 1),
        _pat(TRUEHD_BLOCK, "Not FLAC", "FLAC"),
        _cond(TRUEHD_BLOCK, "TrueHD", "release_title", 0, 1),
        _pat(TRUEHD_BLOCK, "TrueHD", "TrueHD"),
        _cond(TRUEHD_BLOCK, "Trusted Group", "release_group", 0, 1),
        _pat(TRUEHD_BLOCK, "Trusted Group", TRUSTED_REGEX),
        _score(TRUEHD_BLOCK, TRUEHD_BLOCK_SCORE),
    ]


def _format_mid() -> list[str]:
    return [
        f"INSERT INTO custom_formats (name, description) VALUES ({sql_quote(MID_TIER_NAME)},",
        sql_quote(
            f"2160p Blu-ray encode, not a remux, above {MID_MIN_GB} GB through {MID_MAX_GB} GB, from "
            "Dumpstarr UHD tiers except hallowed and BHDStudio, plus Dictionarry "
            f"T3-T5 groups, dkore, TAoE, and ZAX. Nothing extra below {MID_MIN_GB} GB or above {MID_MAX_GB} GB."
        )
        + ");",
        _cond(MID_TIER_NAME, "2160p", "resolution", 0, 1),
        f"INSERT INTO condition_resolutions (custom_format_name, condition_name, resolution) VALUES ({sql_quote(MID_TIER_NAME)}, '2160p', '2160p');",
        _cond(MID_TIER_NAME, "Bluray", "source", 0, 1),
        f"INSERT INTO condition_sources (custom_format_name, condition_name, source) VALUES ({sql_quote(MID_TIER_NAME)}, 'Bluray', 'bluray');",
        _cond(MID_TIER_NAME, "Not Remux", "release_title", 1, 1),
        _pat(MID_TIER_NAME, "Not Remux", "Remux"),
        _cond(MID_TIER_NAME, MID_SIZE_LABEL, "size", 0, 1),
        f"INSERT INTO condition_sizes (custom_format_name, condition_name, min_bytes, max_bytes) VALUES ({sql_quote(MID_TIER_NAME)}, {sql_quote(MID_SIZE_LABEL)}, {MID_MIN_BYTES}, {MID_MAX_BYTES});",
        _cond(MID_TIER_NAME, "Mid Groups", "release_group", 0, 1),
        _pat(MID_TIER_NAME, "Mid Groups", MID_REGEX),
        _score(MID_TIER_NAME, MID_TIER_SCORE),
    ]


def _cond(custom_format: str, name: str, kind: str, negate: int, required: int) -> str:
    return (
        "INSERT INTO custom_format_conditions (custom_format_name, name, type, arr_type, negate, required) VALUES ("
        f"{sql_quote(custom_format)}, {sql_quote(name)}, {sql_quote(kind)}, 'all', {negate}, {required});"
    )


def _pat(custom_format: str, condition: str, regex_name: str) -> str:
    return (
        "INSERT INTO condition_patterns (custom_format_name, condition_name, regular_expression_name) VALUES ("
        f"{sql_quote(custom_format)}, {sql_quote(condition)}, {sql_quote(regex_name)});"
    )


def _score(custom_format: str, score: int) -> str:
    return (
        "INSERT INTO quality_profile_custom_formats (quality_profile_name, custom_format_name, arr_type, score) VALUES ("
        f"'Movies 2160p', {sql_quote(custom_format)}, 'radarr', {score});"
    )


def _insert_row(table: str, columns: list[str], row: sqlite3.Row) -> str:
    values = ", ".join(sql_quote(row[column]) for column in columns)
    cols = ", ".join(columns)
    return f"INSERT INTO {table} ({cols}) VALUES ({values});"


def export_base_sql(conn: sqlite3.Connection, dumpstarr_sha: str) -> str:
    """Serialize the Movies 2160p closure. Other profiles and unused formats are omitted."""
    formats = [
        row["custom_format_name"]
        for row in conn.execute(
            """
            SELECT custom_format_name FROM quality_profile_custom_formats
            WHERE quality_profile_name = ? ORDER BY custom_format_name, arr_type
            """,
            (PROFILE_NAME,),
        )
    ]
    if not formats:
        raise RuntimeError(f"profile not found: {PROFILE_NAME}")
    marks = ",".join("?" * len(formats))
    regexes = [
        row["regular_expression_name"]
        for row in conn.execute(
            f"""
            SELECT DISTINCT cp.regular_expression_name AS regular_expression_name
            FROM condition_patterns cp
            WHERE cp.custom_format_name IN ({marks})
            ORDER BY cp.regular_expression_name
            """,
            formats,
        )
    ]
    regex_marks = ",".join("?" * len(regexes))
    tag_names = set()
    for row in conn.execute(
        "SELECT tag_name FROM quality_profile_tags WHERE quality_profile_name = ?",
        (PROFILE_NAME,),
    ):
        tag_names.add(row["tag_name"])
    for row in conn.execute(
        f"SELECT tag_name FROM custom_format_tags WHERE custom_format_name IN ({marks})",
        formats,
    ):
        tag_names.add(row["tag_name"])
    if regexes:
        for row in conn.execute(
            f"SELECT tag_name FROM regular_expression_tags WHERE regular_expression_name IN ({regex_marks})",
            regexes,
        ):
            tag_names.add(row["tag_name"])

    qualities = set()
    for row in conn.execute(
        """
        SELECT quality_name FROM quality_profile_qualities
        WHERE quality_profile_name = ? AND quality_name IS NOT NULL
        """,
        (PROFILE_NAME,),
    ):
        qualities.add(row["quality_name"])
    for row in conn.execute(
        "SELECT quality_name FROM quality_group_members WHERE quality_profile_name = ?",
        (PROFILE_NAME,),
    ):
        qualities.add(row["quality_name"])

    lines = [
        f"-- {PROFILE_NAME} pruned from {DUMPSTARR_REPO} {DUMPSTARR_BRANCH} @ {dumpstarr_sha}.",
        "-- Generated by scripts/sync_upstream.py. The nightly job replaces this file.",
    ]
    if tag_names:
        for row in conn.execute(
            f"SELECT name FROM tags WHERE name IN ({','.join('?' * len(tag_names))}) ORDER BY name",
            sorted(tag_names),
        ):
            lines.append(_insert_row("tags", ["name"], row))
    for row in conn.execute(
        f"""
        SELECT name, pattern, regex101_id, description
        FROM regular_expressions
        WHERE name IN ({regex_marks})
        ORDER BY name
        """,
        regexes,
    ):
        lines.append(_insert_row("regular_expressions", ["name", "pattern", "regex101_id", "description"], row))
    if regexes and tag_names:
        for row in conn.execute(
            f"""
            SELECT regular_expression_name, tag_name FROM regular_expression_tags
            WHERE regular_expression_name IN ({regex_marks})
            ORDER BY regular_expression_name, tag_name
            """,
            regexes,
        ):
            if row["tag_name"] in tag_names:
                lines.append(_insert_row("regular_expression_tags", ["regular_expression_name", "tag_name"], row))
    for row in conn.execute(
        f"""
        SELECT name, description, include_in_rename FROM custom_formats
        WHERE name IN ({marks}) ORDER BY name
        """,
        formats,
    ):
        lines.append(_insert_row("custom_formats", ["name", "description", "include_in_rename"], row))
    for row in conn.execute(
        f"""
        SELECT custom_format_name, tag_name FROM custom_format_tags
        WHERE custom_format_name IN ({marks})
        ORDER BY custom_format_name, tag_name
        """,
        formats,
    ):
        lines.append(_insert_row("custom_format_tags", ["custom_format_name", "tag_name"], row))
    for row in conn.execute(
        f"""
        SELECT custom_format_name, name, type, arr_type, negate, required
        FROM custom_format_conditions
        WHERE custom_format_name IN ({marks})
        ORDER BY custom_format_name, name
        """,
        formats,
    ):
        lines.append(
            _insert_row(
                "custom_format_conditions",
                ["custom_format_name", "name", "type", "arr_type", "negate", "required"],
                row,
            )
        )
    type_tables = [
        ("condition_patterns", ["custom_format_name", "condition_name", "regular_expression_name"]),
        ("condition_languages", ["custom_format_name", "condition_name", "language_name", "except_language"]),
        ("condition_indexer_flags", ["custom_format_name", "condition_name", "flag"]),
        ("condition_sources", ["custom_format_name", "condition_name", "source"]),
        ("condition_resolutions", ["custom_format_name", "condition_name", "resolution"]),
        ("condition_quality_modifiers", ["custom_format_name", "condition_name", "quality_modifier"]),
        ("condition_sizes", ["custom_format_name", "condition_name", "min_bytes", "max_bytes"]),
        ("condition_release_types", ["custom_format_name", "condition_name", "release_type"]),
        ("condition_years", ["custom_format_name", "condition_name", "min_year", "max_year"]),
    ]
    for table, columns in type_tables:
        rows = conn.execute(
            f"""
            SELECT {", ".join(columns)} FROM {table}
            WHERE custom_format_name IN ({marks})
            ORDER BY custom_format_name, condition_name
            """,
            formats,
        ).fetchall()
        for row in rows:
            lines.append(_insert_row(table, columns, row))
    for row in conn.execute(
        """
        SELECT name, preferred_protocol, usenet_delay, torrent_delay,
               bypass_if_highest_quality, bypass_if_above_custom_format_score,
               minimum_custom_format_score
        FROM delay_profiles
        WHERE name = 'Default Delay'
        """
    ):
        lines.append(
            _insert_row(
                "delay_profiles",
                [
                    "name",
                    "preferred_protocol",
                    "usenet_delay",
                    "torrent_delay",
                    "bypass_if_highest_quality",
                    "bypass_if_above_custom_format_score",
                    "minimum_custom_format_score",
                ],
                row,
            )
        )
    for row in conn.execute(
        """
        SELECT name, description, upgrades_allowed, minimum_custom_format_score,
               upgrade_until_score, upgrade_score_increment
        FROM quality_profiles WHERE name = ?
        """,
        (PROFILE_NAME,),
    ):
        lines.append(
            _insert_row(
                "quality_profiles",
                [
                    "name",
                    "description",
                    "upgrades_allowed",
                    "minimum_custom_format_score",
                    "upgrade_until_score",
                    "upgrade_score_increment",
                ],
                row,
            )
        )
    for row in conn.execute(
        """
        SELECT quality_profile_name, language_name, type
        FROM quality_profile_languages WHERE quality_profile_name = ?
        ORDER BY language_name
        """,
        (PROFILE_NAME,),
    ):
        lines.append(_insert_row("quality_profile_languages", ["quality_profile_name", "language_name", "type"], row))
    for row in conn.execute(
        """
        SELECT quality_profile_name, tag_name FROM quality_profile_tags
        WHERE quality_profile_name = ? ORDER BY tag_name
        """,
        (PROFILE_NAME,),
    ):
        lines.append(_insert_row("quality_profile_tags", ["quality_profile_name", "tag_name"], row))
    for row in conn.execute(
        "SELECT quality_profile_name, name FROM quality_groups WHERE quality_profile_name = ? ORDER BY name",
        (PROFILE_NAME,),
    ):
        lines.append(_insert_row("quality_groups", ["quality_profile_name", "name"], row))
    member_columns = ["quality_profile_name", "quality_group_name", "quality_name", "position"]
    for row in conn.execute(
        """
        SELECT quality_profile_name, quality_group_name, quality_name, position
        FROM quality_group_members WHERE quality_profile_name = ?
        ORDER BY quality_group_name, position, quality_name
        """,
        (PROFILE_NAME,),
    ):
        lines.append(_insert_row("quality_group_members", member_columns, row))
    for row in conn.execute(
        """
        SELECT quality_profile_name, quality_name, quality_group_name, position, enabled, upgrade_until
        FROM quality_profile_qualities WHERE quality_profile_name = ?
        ORDER BY position, COALESCE(quality_name, quality_group_name)
        """,
        (PROFILE_NAME,),
    ):
        lines.append(
            _insert_row(
                "quality_profile_qualities",
                [
                    "quality_profile_name",
                    "quality_name",
                    "quality_group_name",
                    "position",
                    "enabled",
                    "upgrade_until",
                ],
                row,
            )
        )
    for row in conn.execute(
        """
        SELECT quality_profile_name, custom_format_name, arr_type, score
        FROM quality_profile_custom_formats WHERE quality_profile_name = ?
        ORDER BY custom_format_name, arr_type
        """,
        (PROFILE_NAME,),
    ):
        lines.append(
            _insert_row(
                "quality_profile_custom_formats",
                ["quality_profile_name", "custom_format_name", "arr_type", "score"],
                row,
            )
        )
    if qualities:
        qmarks = ",".join("?" * len(qualities))
        for row in conn.execute(
            f"""
            SELECT name, quality_name, min_size, max_size, preferred_size
            FROM radarr_quality_definitions
            WHERE quality_name IN ({qmarks})
            ORDER BY name, quality_name
            """,
            sorted(qualities),
        ):
            lines.append(
                _insert_row(
                    "radarr_quality_definitions",
                    ["name", "quality_name", "min_size", "max_size", "preferred_size"],
                    row,
                )
            )
    return "\n".join(lines) + "\n"
