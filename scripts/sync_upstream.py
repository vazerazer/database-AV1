#!/usr/bin/env python3
"""Rebuild the pruned Movies 2160p base, the local layer, and the TRaSH profile.

Dumpstarr stable is the base. Dictionarry v2 supplies the tier lists the
layer uses. TRaSH Guides supplies Remux + WEB 2160p when --trash is set.
The script writes ops/ and tweaks/ only. It does not run tests and it does
not push; the workflow does that after the tests pass.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcdlib import (  # noqa: E402
    DICTIONARRY_BRANCH,
    DICTIONARRY_REPO,
    DUMPSTARR_BRANCH,
    DUMPSTARR_REPO,
    build_layer_sql,
    compile_layers,
    connect,
    execute_dir,
    export_base_sql,
)
from trash_profile import (  # noqa: E402
    PROFILE_ID,
    TRASH_BRANCH,
    TRASH_PROFILE_NAME,
    TRASH_REPO,
    build_trash_sql,
)


def git_sha(path: str) -> str:
    return subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--schema", required=True, help="Dictionarry schema ops directory")
    parser.add_argument("--dumpstarr", required=True, help="Dumpstarr checkout (stable)")
    parser.add_argument("--dictionarry", required=True, help="Dictionarry checkout (v2)")
    parser.add_argument("--trash", help="TRaSH-Guides/Guides checkout (master)")
    parser.add_argument("--check", action="store_true", help="Exit 1 if generated files differ")
    args = parser.parse_args()

    dumpstarr_ops = os.path.join(args.dumpstarr, "ops")
    dictionarry_ops = os.path.join(args.dictionarry, "ops")
    dumpstarr = compile_layers(args.schema, dumpstarr_ops)
    dictionarry = compile_layers(args.schema, dictionarry_ops)
    dumpstarr_sha = git_sha(args.dumpstarr)
    dictionarry_sha = git_sha(args.dictionarry)

    base_sql = export_base_sql(dumpstarr, dumpstarr_sha)
    layer_sql = build_layer_sql(dumpstarr, dictionarry)
    upstream = {
        "dumpstarr": {
            "repository": DUMPSTARR_REPO,
            "branch": DUMPSTARR_BRANCH,
            "sha": dumpstarr_sha,
        },
        "dictionarry": {
            "repository": DICTIONARRY_REPO,
            "branch": DICTIONARRY_BRANCH,
            "sha": dictionarry_sha,
        },
    }
    files = {
        os.path.join(args.repo, "ops", "0.movies-2160p.sql"): base_sql,
        os.path.join(args.repo, "tweaks", "1.layer.sql"): layer_sql,
    }
    if args.trash:
        trash_sha = git_sha(args.trash)
        preview = connect()
        execute_dir(preview, args.schema)
        preview.executescript(base_sql)
        preview.executescript(layer_sql)
        try:
            trash_sql = build_trash_sql(preview, args.trash, trash_sha)
        finally:
            preview.close()
        files[os.path.join(args.repo, "tweaks", "2.trash-remux.sql")] = trash_sql
        upstream["trash"] = {
            "repository": TRASH_REPO,
            "branch": TRASH_BRANCH,
            "sha": trash_sha,
            "profile": TRASH_PROFILE_NAME,
            "trash_id": PROFILE_ID,
        }
    else:
        upstream_path = os.path.join(args.repo, ".github", "upstream.json")
        if os.path.exists(upstream_path):
            with open(upstream_path, encoding="utf-8") as handle:
                current_upstream = json.load(handle)
            if "trash" in current_upstream:
                upstream["trash"] = current_upstream["trash"]
    files[os.path.join(args.repo, ".github", "upstream.json")] = json.dumps(upstream, indent=2) + "\n"
    changed = []
    for path, contents in files.items():
        current = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8") as handle:
                current = handle.read()
        if current != contents:
            changed.append(os.path.relpath(path, args.repo))
            if not args.check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(contents)
    if args.check and changed:
        print("generated files differ:", ", ".join(changed))
        return 1
    if changed:
        print("updated", ", ".join(changed))
    else:
        print("already matches upstream")
    print(f"dumpstarr {dumpstarr_sha}")
    print(f"dictionarry {dictionarry_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
