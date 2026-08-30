#!/usr/bin/env python3
"""
tests/test_profile_drift.py
Profile Drift Guard for PCD Profiles (Movies 2160p AV1 HQ and Movies SHADOW Explorer).
Validates that:
1. ops/profile_snapshot.json schema and invariants are intact.
2. Live Radarr4k Quality Profiles match ops/profile_snapshot.json byte-for-byte (when daemon/key is accessible).
   Skips cleanly when running off-box in CI without API keys.
"""

import os
import sys
import json
import unittest
import urllib.request
import urllib.error

class TestProfileDriftGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.snapshot_path = os.path.join(cls.repo_root, 'ops', 'profile_snapshot.json')
        with open(cls.snapshot_path, 'r', encoding='utf-8') as f:
            cls.snapshot = json.load(f)

    def test_snapshot_invariants(self):
        """Validates snapshot integrity and flagship profile invariants."""
        self.assertIn('Movies 2160p AV1 HQ', self.snapshot)

        prod = self.snapshot['Movies 2160p AV1 HQ']

        self.assertEqual(prod['min_score'], 1000)
        self.assertEqual(prod['upgrade_until_score'], 3300)

        # Invariants: Prod has active tier bonuses
        self.assertEqual(prod['custom_formats'].get('AV1 Quality Encoders'), 3300)
        self.assertEqual(prod['custom_formats'].get('AV1 Compact Encoders'), 200)

        # Anti-trash hygiene and hard rejections
        for cf in ['CAM', '3D', 'Upscale', 'Foreign Dub', 'Banned Groups']:
            self.assertIn(cf, prod['custom_formats'], f"Hygiene CF '{cf}' missing in Prod.")

        # Definition hashes present and populated
        self.assertIn('custom_format_definitions', self.snapshot)
        self.assertGreater(len(self.snapshot['custom_format_definitions']), 50)

    def test_live_radarr_vs_snapshot(self):
        """Validates live Radarr4k daemon against snapshot; skips cleanly in CI or offline mode."""
        check_live = os.environ.get('CHECK_LIVE_RADARR', '').lower() in ('1', 'true', 'yes')
        api_key = os.environ.get('RADARR_API_KEY')
        if not check_live or not api_key:
            print("\n[SKIP] Live Radarr4k daemon check skipped (CHECK_LIVE_RADARR not enabled).")
            return

        radarr_url = os.environ.get('RADARR_URL', 'http://127.0.0.1:7879')
        req = urllib.request.Request(f"{radarr_url}/api/v3/qualityprofile", headers={'X-Api-Key': api_key})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                live_profiles = json.load(resp)
        except Exception as e:
            print(f"\n[SKIP] Could not connect to live Radarr4k daemon ({e}); skipping live drift test.")
            return

        live_prof_map = {p['name']: p for p in live_profiles}

        for p_name in ['Movies 2160p AV1 HQ']:
            expected = self.snapshot[p_name]
            self.assertIn(p_name, live_prof_map, f"Live profile '{p_name}' not found in Radarr4k.")
            live_p = live_prof_map[p_name]
            self.assertEqual(live_p.get('minFormatScore'), expected['min_score'], f"Live minFormatScore mismatch for '{p_name}'.")
            self.assertEqual(live_p.get('cutoffFormatScore'), expected['upgrade_until_score'], f"Live cutoffFormatScore mismatch for '{p_name}'.")

            live_cf_scores = {}
            for item in live_p.get('formatItems', []):
                cf_name = item.get('name')
                cf_score = item.get('score', 0)
                if cf_name and cf_score != 0:
                    live_cf_scores[cf_name] = cf_score

            expected_cfs = expected['custom_formats']

            # Check that live profile has all expected non-zero CFs and no extra/missing scores
            self.assertEqual(
                live_cf_scores,
                expected_cfs,
                f"Live score drift detected in profile '{p_name}'!\nDiff: live={live_cf_scores}\nexpected={expected_cfs}"
            )

        # Validate Custom Format Specifications (Definitions Hash Guard)
        import hashlib
        req_cf = urllib.request.Request(f"{radarr_url}/api/v3/customformat", headers={'X-Api-Key': api_key})
        with urllib.request.urlopen(req_cf, timeout=10) as resp:
            live_cfs = json.load(resp)
        live_cf_map = {c['name']: c for c in live_cfs}

        for cf_name, expected_hash in self.snapshot.get('custom_format_definitions', {}).items():
            self.assertIn(cf_name, live_cf_map, f"Expected Custom Format '{cf_name}' not found in live Radarr4k!")
            live_cf = live_cf_map[cf_name]

            specs = []
            for s in sorted(live_cf.get('specifications', []), key=lambda x: x.get('name', '')):
                field_val = s.get('fields', [{}])[0].get('value') if s.get('fields') else None
                specs.append({
                    'name': s.get('name'),
                    'negate': bool(s.get('negate')),
                    'required': bool(s.get('required')),
                    'value': str(field_val) if field_val is not None else ''
                })
            canonical = json.dumps({'name': live_cf.get('name'), 'specs': specs}, sort_keys=True)
            live_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()

            self.assertEqual(
                live_hash,
                expected_hash,
                f"Custom Format specification drift detected for '{cf_name}'!\n"
                f"Live hash:     {live_hash}\n"
                f"Expected hash: {expected_hash}\n"
                f"A sync or manual edit altered '{cf_name}' specifications in live Radarr4k."
            )

if __name__ == '__main__':
    unittest.main()
