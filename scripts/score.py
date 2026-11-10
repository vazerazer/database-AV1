"""Radarr custom-format scoring for a compiled PCD.

Required conditions are AND. Optional conditions are grouped by condition
type: one match in that type is enough, and a required match in the same
type also satisfies the group. That is Radarr's SpecificationMatchesGroup.

Release-title patterns see Radarr's simple release title: the movie name is
replaced with "A.Movie" / "A Movie" before the regex runs, so a title like
Cam.2018 does not match the CAM source tag.
"""

from __future__ import annotations

import collections
import functools
import sqlite3

import regex as re

from pcdlib import PROFILE_NAME

EDITION = (
    r"\(?\b(?<edition>(((Recut.|Extended.|Ultimate.)?(Director.?s|Collector.?s|Theatrical|"
    r"Ultimate|Extended|Despecialized|(Special|Rouge|Final|Assembly|Imperial|Diamond|Signature|"
    r"Hunter|Rekall)(?=(.(Cut|Edition|Version)))|\d{2,3}(th)?.Anniversary)(?:.(Cut|Edition|Version))?"
    r"(.(Extended|Uncensored|Remastered|Unrated|Uncut|Open.?Matte|IMAX|Fan.?Edit))?|"
    r"((Uncensored|Remastered|Unrated|Uncut|Open?.Matte|IMAX|Fan.?Edit|Restored|((2|3|4)in1))))))\b\)?"
)

_TITLE_PATTERNS = [
    re.compile(pattern, re.I)
    for pattern in (
        r"^(?:\[(?<subgroup>.+?)\][-_. ]?)(?<title>(?![(\[]).+?)\s*\((?<year>(1(8|9)|20)\d{2})\).*?(?<hash>\[\w{8}\])?(?:$|\.)",
        r"^(?:\[(?<subgroup>.+?)\][-_. ]?)(?<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)\[!]))*(?<year>(1(8|9)|20)\d{2}(?!p|i|x|\d+|\]|\W\d+)))+.*?(?<hash>\[\w{8}\])?(?:$|\.)",
        r"^(?:\[(?<subgroup>.+?)\][-_. ]?)(?<title>(?![(\[]).+?)((v)(?:\d{1,2})(?:([-_. ])))(\[.*)?(?:[\[(][^])])?.*?(?<hash>\[\w{8}\])(?:$|\.)",
        r"^(?:\[(?<subgroup>.+?)\][-_. ]?)(?<title>(?![(\[]).+?)(\[.*).*?(?<hash>\[\w{8}\])(?:$|\.)",
        r"^(?:\[(?<subgroup>.+?)\][-_. ]?)(?<title>(?![(\[]).+)(?:[\[(][^])]).*?(?<hash>\[\w{8}\])(?:$|\.)",
        r"^(?<title>(?![(\[]).+?)((\W|_))("
        + EDITION
        + r".{1,3})?(?:(?<!(19|20)\d{2}.*?)(?<!(?:Good|The)[_ .-])(German|TrueFrench))(.+?)(?=((19|20)\d{2}|$))(?<year>(19|20)\d{2}(?!p|i|\d+|\]|\W\d+))?(\W+|_|$)(?!\\)",
        r"^(?<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)\[!]))*"
        + EDITION
        + r".{1,3}(?<year>(1(8|9)|20)\d{2}(?!p|i|\d+|\]|\W\d+)))+(\W+|_|$)(?!\\)",
        r"^(?<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)\[!]))*(?<year>(1(8|9)|20)\d{2}(?!p|i|(1(8|9)|20)\d{2}|\]|\W(1(8|9)|20)\d{2})))+(\W+|_|$)(?!\\)",
        r"^(?<title>.+?)?(?:(?:[-_\W](?<![()\[!]))*(?<year>(\[\w *\])))+(\W+|_|$)(?!\\)",
        r"^(?<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)!]))*(?<year>(1(8|9)|20)\d{2}(?!p|i|\d+|\W\d+)))+(\W+|_|$)(?!\\)",
        r"^(?<title>.+?)?(?:(?:[-_\W](?<![)\[!]))*(?<year>(1(8|9)|20)\d{2}(?!p|i|\d+|\]|\W\d+)))+(\W+|_|$)(?!\\)",
    )
]

_SIMPLE_TITLE = re.compile(
    r"(?:(480|540|576|720|1080|2160)[ip]|[xh][\W_]?26[45]|DD\W?5\W1|[<>?*]|"
    r"848x480|1280x720|1920x1080|3840x2160|4096x2160|(8|10)b(it)?|10-bit)\s*?(?![a-b0-9])",
    re.I,
)
_SIMPLE_RELEASE = re.compile(r"\s*(?:[<>?*|])", re.I)
_WEBSITE_PREFIX = re.compile(
    r"^(?:(?:\[|\()\s*)?(?:www\.)?[-a-z0-9-]{1,256}\.(?<!Naruto-Kun\.)"
    r"(?:[a-z]{2,6}\.[a-z]{2,6}|xn--[a-z0-9-]{4,}|[a-z]{2,})\b(?:\s*(?:\]|\))|[ -]{2,})[ -]*",
    re.I,
)
_TORRENT_SUFFIX = re.compile(r"\[(?:ettv|rartv|rarbg|cttv|publichd)\]$", re.I)

SOURCE_MAP = {
    "webdl": "web_dl",
    "webrip": "webrip",
    "bluray": "bluray",
    "dvd": "dvd",
    "tv": "television",
    "television": "television",
    "cam": "cam",
    "telesync": "telesync",
    "telecine": "telecine",
    "workprint": "workprint",
    "unknown": "unknown",
}


def simple_release_title(title: str) -> str:
    """Radarr Parser.ParseMovieTitle simple-release-title substitution."""
    original = title or ""
    simple = _WEBSITE_PREFIX.sub("", _SIMPLE_TITLE.sub("", original))
    simple = _TORRENT_SUFFIX.sub("", simple)
    release = _SIMPLE_RELEASE.sub("", original)
    for pattern in _TITLE_PATTERNS:
        match = pattern.search(simple)
        if not match or "title" not in match.groupdict() or match.group("title") is None:
            continue
        found = match.group("title")
        if not found.strip():
            continue
        start, end = match.span("title")
        if start < 0 or end > len(release) or start > end:
            continue
        replacement = "A.Movie" if "." in found else "A Movie"
        return release[:start] + replacement + release[end:]
    return release


@functools.lru_cache(maxsize=20000)
def cached_simple_title(title: str) -> str:
    return simple_release_title(title)


class Scorer:
    def __init__(self, conn: sqlite3.Connection, profile: str = PROFILE_NAME, arr_type: str = "radarr"):
        self.profile = profile
        self.arr_type = arr_type
        self.scores: dict[str, int] = {}
        for row in conn.execute(
            """
            SELECT custom_format_name, score FROM quality_profile_custom_formats
            WHERE quality_profile_name = ? AND arr_type = ?
            """,
            (profile, arr_type),
        ):
            self.scores[row["custom_format_name"]] = row["score"]
        allowed = ("all", arr_type)
        self.conditions: dict[str, list[dict]] = collections.defaultdict(list)
        if self.scores:
            marks = ",".join("?" * len(self.scores))
            for row in conn.execute(
                f"""
                SELECT custom_format_name, name, type, arr_type, negate, required
                FROM custom_format_conditions
                WHERE custom_format_name IN ({marks})
                """,
                list(self.scores),
            ):
                if row["arr_type"] in allowed:
                    self.conditions[row["custom_format_name"]].append(dict(row))
        self._regex: dict[tuple[str, str], re.Pattern | None] = {}
        for row in conn.execute(
            """
            SELECT cp.custom_format_name, cp.condition_name, re.pattern
            FROM condition_patterns cp
            JOIN regular_expressions re ON re.name = cp.regular_expression_name
            """
        ):
            self._regex[(row["custom_format_name"], row["condition_name"])] = re.compile(
                row["pattern"], re.I
            )
        self._source = {
            (row["custom_format_name"], row["condition_name"]): row["source"]
            for row in conn.execute(
                "SELECT custom_format_name, condition_name, source FROM condition_sources"
            )
        }
        self._resolution = {
            (row["custom_format_name"], row["condition_name"]): row["resolution"]
            for row in conn.execute(
                "SELECT custom_format_name, condition_name, resolution FROM condition_resolutions"
            )
        }
        self._size = {
            (row["custom_format_name"], row["condition_name"]): (row["min_bytes"], row["max_bytes"])
            for row in conn.execute(
                "SELECT custom_format_name, condition_name, min_bytes, max_bytes FROM condition_sizes"
            )
        }
        self.ranks = _quality_ranks(conn, profile)
        self.minimum = conn.execute(
            "SELECT minimum_custom_format_score FROM quality_profiles WHERE name = ?",
            (profile,),
        ).fetchone()["minimum_custom_format_score"]

    def score(self, release: dict) -> tuple[int, list[str]]:
        total = 0
        matched: list[str] = []
        simple = cached_simple_title(release.get("title") or "")
        for name, points in self.scores.items():
            if self._matches(name, release, simple):
                total += points
                matched.append(name)
        matched.sort()
        return total, matched

    def _matches(self, name: str, release: dict, simple: str) -> bool:
        conditions = self.conditions.get(name)
        if not conditions:
            return False
        groups: dict[str, list[dict]] = collections.defaultdict(list)
        for condition in conditions:
            groups[condition["type"]].append(condition)
        for group in groups.values():
            saw_true = False
            required_failed = False
            for condition in group:
                ok = self._condition(condition, release, simple)
                saw_true = saw_true or ok
                if condition["required"] and not ok:
                    required_failed = True
            if required_failed or not saw_true:
                return False
        return True

    def _condition(self, condition: dict, release: dict, simple: str) -> bool:
        key = (condition["custom_format_name"], condition["name"])
        kind = condition["type"]
        quality = (release.get("quality") or {}).get("quality") or {}
        if kind in ("release_title", "edition"):
            pattern = self._regex.get(key)
            ok = bool(pattern.search(simple)) if pattern is not None else False
        elif kind == "release_group":
            pattern = self._regex.get(key)
            group = release.get("releaseGroup") or ""
            ok = bool(pattern.search(group)) if pattern is not None and group else False
        elif kind == "source":
            source = quality.get("source") or ""
            ok = SOURCE_MAP.get(source, source) == self._source.get(key)
        elif kind == "resolution":
            resolution = quality.get("resolution") or 0
            ok = self._resolution.get(key) == f"{resolution}p"
        elif kind == "size":
            minimum, maximum = self._size[key]
            size = release.get("size") or 0
            ok = True
            if minimum is not None and not size > minimum:
                ok = False
            if maximum is not None and not size <= maximum:
                ok = False
        else:
            ok = False
        if condition["negate"]:
            ok = not ok
        return ok


def _quality_ranks(conn: sqlite3.Connection, profile: str) -> dict[str, int]:
    ranks: dict[str, int] = {}
    rows = conn.execute(
        """
        SELECT position, enabled, quality_name, quality_group_name
        FROM quality_profile_qualities
        WHERE quality_profile_name = ?
        ORDER BY position
        """,
        (profile,),
    ).fetchall()
    members: dict[str, list[str]] = collections.defaultdict(list)
    for row in conn.execute(
        """
        SELECT quality_group_name, quality_name FROM quality_group_members
        WHERE quality_profile_name = ?
        """,
        (profile,),
    ):
        members[row["quality_group_name"]].append(row["quality_name"])
    for row in rows:
        if not row["enabled"]:
            continue
        if row["quality_name"]:
            ranks[row["quality_name"]] = row["position"]
        elif row["quality_group_name"]:
            for quality in members[row["quality_group_name"]]:
                ranks[quality] = row["position"]
    return ranks


def hard_reject(release: dict) -> bool:
    """Rejections that are not the profile score or the current file."""
    for reason in release.get("rejections") or []:
        if reason.startswith("Unknown Movie"):
            return True
        if reason.startswith("Unable to parse"):
            return True
        if reason.startswith("Wrong movie"):
            return True
        if reason.startswith("Release is blocklisted"):
            return True
        if reason.startswith("Original Language"):
            return True
        if reason == "Sample":
            return True
        if reason.startswith("Raw Bluray"):
            return True
    return False


def pick(releases: list[dict], scorer: Scorer):
    best = None
    best_key = None
    for release in releases:
        if hard_reject(release):
            continue
        quality = ((release.get("quality") or {}).get("quality") or {}).get("name")
        rank = scorer.ranks.get(quality)
        if rank is None:
            continue
        score, matched = scorer.score(release)
        if score < scorer.minimum:
            continue
        key = (rank, -score, -(release.get("size") or 0), release.get("title") or "")
        if best_key is None or key < best_key:
            best_key = key
            best = (release, score, matched)
    return best
