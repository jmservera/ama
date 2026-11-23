---
title: Research for issue 1274 live run 5 (2026-11-23)
---

Scope: unticked criteria 1 and 4. Synthetic demo, desktop only; CI-only issue, no Azure app or credential used.

Research disposition: executed (builds on the 2026-11-23 run 4 note).

Findings:

* Criterion 1: actionlint 504 proven from job 128696067639; AWF and #1273 logs not retained (see run 4 note).
* Code-satisfiable gap: tests cover the installer, but nothing pins the workflow wiring (src-ci calls the installer, expected version equals VERSION, no raw release-download fetch in native workflows). A regression test closes that for criterion 4's "affected actual integration".
* The axe curl step in src-ci uses retry plus pinned sha256 (CDN, not a release).

Planning Readiness: Ready.
