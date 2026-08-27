# 🛡️ Op 930 Profile 64 / Profile 67 Diff vs Pre-930 Baseline

**Pre-930 Baseline Commit:** `1d6c310`  
**Current Commit:** `c8f68ce`  
**Verification Invariant:** Production Profile 64 edits strictly limited to `Micro Hard Floor` (-10000), `Legacy Trusted x264` (+5400), and `1080p Quality Tier 2` legacy group expansion.

---

```diff
diff --git a/ops/profile_snapshot.json b/ops/profile_snapshot.json
index ede79ef..e4872fa 100644
--- a/ops/profile_snapshot.json
+++ b/ops/profile_snapshot.json
@@ -47,9 +47,11 @@
       "HONE WEB": 2750,
       "HULU": 50,
       "Heavy 2160p Fallback": -400,
+      "Legacy Trusted x264": 5400,
       "Legacy x264 Codec": -5000,
       "Lossless Audio": 100,
       "MAX": 50,
+      "Micro Hard Floor": -10000,
       "Not AV1": -2000,
       "Opus 5.1 / 7.1": 250,
       "Oversized 2160p Fallback": -1500,
@@ -111,9 +113,11 @@
       "HONE WEB": 2750,
       "HULU": 50,
       "Heavy 2160p Fallback": -400,
+      "Legacy Trusted x264": 5400,
       "Legacy x264 Codec": -5000,
       "Lossless Audio": 100,
       "MAX": 50,
+      "Micro Hard Floor": -10000,
       "Not AV1": -2000,
       "Opus 5.1 / 7.1": 250,
       "Oversized 2160p Fallback": -1500,
```
