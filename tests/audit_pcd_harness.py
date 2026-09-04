#!/usr/bin/env python3
"""
Profilarr Compliant Database (PCD) Validation Harness
Standard library only (sqlite3, json, os, re, sys, argparse)
Strictly audits PCD repository against Profilarr v2 Architecture & DDL specifications.
"""

import sqlite3
import json
import os
import re
import sys
import glob

def run_audit(pcd_dir, schema_dir=None):
    findings = []
    
    print("================================================================================")
    print(f"PROFILARR PCD AUDIT HARNESS: {pcd_dir}")
    print("================================================================================")
    
    # -------------------------------------------------------------------------
    # CHECK 1: Manifest (pcd.json) Validation
    # -------------------------------------------------------------------------
    manifest_path = os.path.join(pcd_dir, "pcd.json")
    manifest = None
    if not os.path.exists(manifest_path):
        findings.append({
            "id": "F-01",
            "severity": "BLOCKER",
            "file": "pcd.json",
            "line": 1,
            "title": "Missing pcd.json manifest",
            "detail": "Repository root is missing pcd.json. Profilarr will fail loadManifest() immediately."
        })
    else:
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            
            # Required fields check per manifest.ts:53-139
            for field in ["name", "version", "description"]:
                if field not in manifest or not isinstance(manifest[field], str) or not manifest[field]:
                    findings.append({
                        "id": f"F-02-{field}",
                        "severity": "BLOCKER",
                        "file": "pcd.json",
                        "line": 1,
                        "title": f"Missing or invalid required field: {field}",
                        "detail": f"Manifest field '{field}' must be a non-empty string."
                    })
            
            if "profilarr" not in manifest or not isinstance(manifest["profilarr"], dict):
                findings.append({
                    "id": "F-03",
                    "severity": "BLOCKER",
                    "file": "pcd.json",
                    "line": 1,
                    "title": "Missing required field: profilarr",
                    "detail": "Manifest must contain a 'profilarr' object with 'minimum_version'."
                })
            elif "minimum_version" not in manifest["profilarr"] or not manifest["profilarr"]["minimum_version"]:
                findings.append({
                    "id": "F-04",
                    "severity": "BLOCKER",
                    "file": "pcd.json",
                    "line": 1,
                    "title": "Missing required field: profilarr.minimum_version",
                    "detail": "'profilarr.minimum_version' is required for compatibility checking."
                })
                
            deps = manifest.get("dependencies", {})
            if not isinstance(deps, dict):
                findings.append({
                    "id": "F-05",
                    "severity": "BLOCKER",
                    "file": "pcd.json",
                    "line": 1,
                    "title": "Invalid dependencies field",
                    "detail": "Field 'dependencies' must be an object."
                })
            else:
                has_schema = any("/schema" in k for k in deps.keys())
                if not has_schema:
                    findings.append({
                        "id": "F-06",
                        "severity": "BLOCKER",
                        "file": "pcd.json",
                        "line": 1,
                        "title": "Missing schema dependency in pcd.json",
                        "detail": "Dependencies must include 'https://github.com/Dictionarry-Hub/schema'."
                    })
                else:
                    schema_ver = [v for k, v in deps.items() if "/schema" in k][0]
                    if schema_ver != "1.1.0" and not schema_ver.startswith("^1.1"):
                        findings.append({
                            "id": "F-07",
                            "severity": "MAJOR",
                            "file": "pcd.json",
                            "line": 1,
                            "title": "Outdated or non-standard schema dependency version",
                            "detail": f"Schema version is '{schema_ver}', expected '^1.1.0' or '1.1.0'."
                        })
        except Exception as e:
            findings.append({
                "id": "F-08",
                "severity": "BLOCKER",
                "file": "pcd.json",
                "line": 1,
                "title": "Invalid JSON in pcd.json",
                "detail": str(e)
            })

    # -------------------------------------------------------------------------
    # CHECK 2: Repository Structure & Base Migration Invariant
    # -------------------------------------------------------------------------
    ops_dir = os.path.join(pcd_dir, "ops")
    if not os.path.exists(ops_dir) or not os.path.isdir(ops_dir):
        findings.append({
            "id": "F-09",
            "severity": "BLOCKER",
            "file": "ops/",
            "line": 1,
            "title": "Missing ops/ directory",
            "detail": "Directory ops/ does not exist. Profilarr cannot discover base operations."
        })
        op_files = []
    else:
        op_files = sorted([f for f in os.listdir(ops_dir) if f.endswith(".sql")])
        
        # Check for 0.* base op
        has_0_base = any(re.match(r"^0\.", f) for f in op_files)
        if not has_0_base:
            findings.append({
                "id": "F-10",
                "severity": "BLOCKER",
                "file": "ops/",
                "line": 1,
                "title": "Missing 0.* base operation (0.rosettarr.sql)",
                "detail": "PCD lacks 0.*.sql base op. A monolithic 1.initial.sql breaks PCD append-only history and upstream sync."
            })
            
        # Check for monolithic squashing
        if len(op_files) == 1 and op_files[0] == "1.initial.sql":
            findings.append({
                "id": "F-11",
                "severity": "MAJOR",
                "file": "ops/1.initial.sql",
                "line": 1,
                "title": "Anti-Pattern: Monolithic single-op repository",
                "detail": "The repository squashed all 280 upstream migrations into a single monolithic 1.initial.sql file, destroying upstream Dictionarry branch lineage and incremental migration safety."
            })

    # -------------------------------------------------------------------------
    # CHECK 3: SQLite DDL & Compilation Simulation
    # -------------------------------------------------------------------------
    # Resolve schema files
    if not schema_dir:
        schema_dir = os.environ.get("PCD_SCHEMA_PATH")
    if not schema_dir:
        # Check repo-relative paths
        candidate_deps_ops = os.path.join(pcd_dir, "deps", "schema", "ops")
        candidate_deps_root = os.path.join(pcd_dir, "deps", "schema")
        
        parent_dir = os.path.dirname(os.path.abspath(pcd_dir))
        candidate_sibling_deps = os.path.join(parent_dir, "deps", "schema", "ops")
        profilarr_matches = sorted(glob.glob(os.path.join(parent_dir, "config", "profilarr", "data", "databases", "*", "deps", "schema", "ops")))
        candidate_profilarr_deps = profilarr_matches[-1] if profilarr_matches else None

        if os.path.exists(candidate_deps_ops) and os.path.isdir(candidate_deps_ops):
            schema_dir = candidate_deps_ops
        elif os.path.exists(candidate_deps_root) and os.path.isdir(candidate_deps_root) and any(f.endswith(".sql") for f in os.listdir(candidate_deps_root)):
            schema_dir = candidate_deps_root
        elif os.path.exists(candidate_sibling_deps) and os.path.isdir(candidate_sibling_deps):
            schema_dir = candidate_sibling_deps
        elif candidate_profilarr_deps and os.path.exists(candidate_profilarr_deps):
            schema_dir = candidate_profilarr_deps
        else:
            raise FileNotFoundError(
                "Could not automatically locate Dictionarry schema ops directory. "
                "Please specify --schema-dir <path> or set the PCD_SCHEMA_PATH environment variable."
            )

    print(f"Loading PCD Schema from: {schema_dir}")
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # Register helper functions matching Profilarr cache.ts:362-405
    def qp_fn(name):
        row = conn.execute("SELECT id FROM quality_profiles WHERE name = ?", (name,)).fetchone()
        if not row: raise sqlite3.OperationalError(f"Quality profile not found: {name}")
        return row[0]
    def cf_fn(name):
        row = conn.execute("SELECT id FROM custom_formats WHERE name = ?", (name,)).fetchone()
        if not row: raise sqlite3.OperationalError(f"Custom format not found: {name}")
        return row[0]
    def dp_fn(name):
        row = conn.execute("SELECT id FROM delay_profiles WHERE name = ?", (name,)).fetchone()
        if not row: raise sqlite3.OperationalError(f"Delay profile not found: {name}")
        return row[0]
    def tag_fn(name):
        row = conn.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()
        if not row: raise sqlite3.OperationalError(f"Tag not found: {name}")
        return row[0]
        
    conn.create_function("qp", 1, qp_fn)
    conn.create_function("cf", 1, cf_fn)
    conn.create_function("dp", 1, dp_fn)
    conn.create_function("tag", 1, tag_fn)

    # 3a. Execute Schema Layer
    schema_loaded = False
    if os.path.exists(schema_dir):
        schema_files = sorted([f for f in os.listdir(schema_dir) if f.endswith(".sql")])
        for sf in schema_files:
            sf_path = os.path.join(schema_dir, sf)
            with open(sf_path, "r", encoding="utf-8") as f:
                try:
                    conn.executescript(f.read())
                    schema_loaded = True
                except Exception as e:
                    findings.append({
                        "id": "F-12",
                        "severity": "BLOCKER",
                        "file": sf,
                        "line": 1,
                        "title": "Schema layer DDL execution failure",
                        "detail": str(e)
                    })
    else:
        findings.append({
            "id": "F-13",
            "severity": "BLOCKER",
            "file": "deps/schema/ops",
            "line": 1,
            "title": "Schema layer directory not found",
            "detail": f"Could not find schema directory at {schema_dir}"
        })

    # 3b. Execute Base Layer Ops
    executed_ops = []
    if schema_loaded and os.path.exists(ops_dir):
        # Sort ops by numeric prefix per Profilarr extractOrderFromFilename()
        def get_order(fn):
            m = re.match(r"^(\d+)\.", fn)
            return int(m.group(1)) if m else float("inf")
            
        sorted_ops = sorted(op_files, key=get_order)
        
        for op in sorted_ops:
            op_path = os.path.join(ops_dir, op)
            with open(op_path, "r", encoding="utf-8") as f:
                op_sql = f.read()
                try:
                    conn.executescript(op_sql)
                    executed_ops.append(op)
                except sqlite3.IntegrityError as e:
                    findings.append({
                        "id": f"F-14-{op}",
                        "severity": "BLOCKER",
                        "file": f"ops/{op}",
                        "line": 1,
                        "title": f"Integrity error in op: {op}",
                        "detail": f"SQLite IntegrityError: {e}"
                    })
                except sqlite3.OperationalError as e:
                    findings.append({
                        "id": f"F-15-{op}",
                        "severity": "BLOCKER",
                        "file": f"ops/{op}",
                        "line": 1,
                        "title": f"Operational error in op: {op}",
                        "detail": f"SQLite OperationalError: {e}"
                    })
                except Exception as e:
                    findings.append({
                        "id": f"F-16-{op}",
                        "severity": "BLOCKER",
                        "file": f"ops/{op}",
                        "line": 1,
                        "title": f"Fatal execution error in op: {op}",
                        "detail": str(e)
                    })

    # -------------------------------------------------------------------------
    # CHECK 4: PRAGMA Integrity and Foreign Key Checks
    # -------------------------------------------------------------------------
    integrity_result = conn.execute("PRAGMA integrity_check;").fetchall()
    fk_violations = conn.execute("PRAGMA foreign_key_check;").fetchall()
    
    if integrity_result != [("ok",)]:
        findings.append({
            "id": "F-17",
            "severity": "BLOCKER",
            "file": "database",
            "line": 0,
            "title": "PRAGMA integrity_check failed",
            "detail": f"Integrity check returned: {integrity_result}"
        })
        
    if fk_violations:
        for fkv in fk_violations:
            table, rowid, parent_table, fkid = fkv
            findings.append({
                "id": f"F-18-{table}-{rowid}",
                "severity": "BLOCKER",
                "file": "ops/1.initial.sql",
                "line": rowid,
                "title": f"Foreign key violation in table '{table}'",
                "detail": f"Rowid {rowid} references missing parent in '{parent_table}' (FK id {fkid})"
            })

    # -------------------------------------------------------------------------
    # CHECK 5: Referential Integrity & Relational Verification
    # -------------------------------------------------------------------------
    # 5a. Profile -> Custom Format Scores
    missing_cfs_in_scores = conn.execute("""
        SELECT qpcf.quality_profile_name, qpcf.custom_format_name
        FROM quality_profile_custom_formats qpcf
        LEFT JOIN custom_formats cf ON qpcf.custom_format_name = cf.name
        WHERE cf.name IS NULL
    """).fetchall()
    for qp_name, cf_name in missing_cfs_in_scores:
        findings.append({
            "id": f"F-19-{qp_name}-{cf_name}",
            "severity": "BLOCKER",
            "file": "ops/1.initial.sql",
            "line": 1,
            "title": f"Score references non-existent Custom Format '{cf_name}'",
            "detail": f"Profile '{qp_name}' assigns a score to '{cf_name}', but '{cf_name}' does not exist in custom_formats."
        })

    # 5b. Condition Patterns -> Regular Expressions
    missing_regex_in_patterns = conn.execute("""
        SELECT cp.custom_format_name, cp.condition_name, cp.regular_expression_name
        FROM condition_patterns cp
        LEFT JOIN regular_expressions re ON cp.regular_expression_name = re.name
        WHERE re.name IS NULL
    """).fetchall()
    for cf_name, cond_name, re_name in missing_regex_in_patterns:
        findings.append({
            "id": f"F-20-{cf_name}-{re_name}",
            "severity": "BLOCKER",
            "file": "ops/1.initial.sql",
            "line": 1,
            "title": f"Pattern references non-existent Regular Expression '{re_name}'",
            "detail": f"Custom Format '{cf_name}' (condition '{cond_name}') references '{re_name}', but '{re_name}' does not exist in regular_expressions."
        })

    # 5c. Profile Qualities Upgrade Until Constraint
    multi_upgrade_profiles = conn.execute("""
        SELECT quality_profile_name, COUNT(*) as cnt
        FROM quality_profile_qualities
        WHERE upgrade_until = 1
        GROUP BY quality_profile_name
        HAVING cnt > 1
    """).fetchall()
    for qp_name, cnt in multi_upgrade_profiles:
        findings.append({
            "id": f"F-21-{qp_name}",
            "severity": "BLOCKER",
            "file": "ops/1.initial.sql",
            "line": 1,
            "title": f"Multiple upgrade_until=1 in profile '{qp_name}'",
            "detail": f"Profile '{qp_name}' has {cnt} items with upgrade_until=1. Schema idx_one_upgrade_until_per_profile allows at most 1."
        })

    # -------------------------------------------------------------------------
    # Table Counts
    # -------------------------------------------------------------------------
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = [r[0] for r in cursor.fetchall()]
    table_counts = {}
    for t in tables:
        try:
            cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            table_counts[t] = cnt
        except Exception:
            pass

    # Print Report
    print("\n--- TABLE ROW COUNTS ---")
    for t, c in table_counts.items():
        if c > 0:
            print(f"  {t:<35}: {c:>6} rows")
    print(f"  Total tables tracked              : {len(table_counts):>6}")

    print("\n--- COMPILED ENTITY SUMMARY ---")
    print(f"  Quality Profiles                  : {table_counts.get('quality_profiles', 0):>6}")
    print(f"  Custom Formats                    : {table_counts.get('custom_formats', 0):>6}")
    print(f"  Custom Format Conditions          : {table_counts.get('custom_format_conditions', 0):>6}")
    print(f"  Regular Expressions               : {table_counts.get('regular_expressions', 0):>6}")
    print(f"  Quality Profile Scoring Rules     : {table_counts.get('quality_profile_custom_formats', 0):>6}")
    print(f"  Quality Groups                    : {table_counts.get('quality_groups', 0):>6}")
    print(f"  Quality Group Members             : {table_counts.get('quality_group_members', 0):>6}")
    print(f"  Profile Quality Items             : {table_counts.get('quality_profile_qualities', 0):>6}")
    print(f"  Integrity Check                   : {integrity_result[0][0]}")
    print(f"  Foreign Key Violations            : {len(fk_violations)}")

    print("\n================================================================================")
    print(f"AUDIT FINDINGS: {len(findings)} Total Findings")
    print("================================================================================")
    for f in findings:
        print(f"[{f['severity']}] {f['id']} - {f['title']}")
        print(f"  File: {f['file']} (Line {f['line']})")
        print(f"  Detail: {f['detail']}\n")

    return findings, table_counts

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PCD Validation Harness")
    parser.add_argument("pcd_dir", nargs="?", default=".", help="Path to PCD repository root")
    parser.add_argument("--schema-dir", default=os.environ.get("PCD_SCHEMA_PATH"), help="Path to Dictionarry schema ops directory")
    args = parser.parse_args()
    findings, _ = run_audit(args.pcd_dir, args.schema_dir)
    sys.exit(0 if not findings else 1)
